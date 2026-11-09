"""Turn mirrored Mintlify/MDX pages into clean Pandoc Markdown.

The output is meant for `config.PANDOC_READER` (run Pandoc with
--preserve-tabs, or tabs in code are expanded). Components become fenced
divs from a small vocabulary that the Texinfo writer renders:

    callout(kind, title)       tabs > tab(title)      steps > step(title)
    codegroup > code blocks and tab(title) for text-only languages
    accordion(title)           accordiongroup > accordion
    cards > card(title, href, image)                  frame(caption)
    field(kind, name, location, type, required, deprecated, default)
    component(name, ...)       anything else, with a warning

Divs and code blocks may carry an #identifier taken from the source `id`.
Code blocks use attribute syntax (```` ```{.lang title="..."} ````) and keep
their content byte for byte. HTML tables become pipe tables; a `<br>` inside
a table cell or heading becomes the empty span `[]{.linebreak}`, elsewhere a
hard line break. Everything dropped or not understood is reported in
`NormalizedPage.warnings` as "kind: detail".

    uv run python -m claude_info.normalize --check [source ...]

normalizes every mirrored page, parses it with Pandoc and reports raw HTML
left in the AST, code blocks that are missing or not byte-exact, lost words,
heading/table/component structure that differs from the source, unexpected
Pandoc constructs, and all warnings. `--show <source>/pages/<path>` prints
one normalized page.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import PurePosixPath
from urllib.parse import unquote, urljoin, urlsplit

from .config import PANDOC_READER


@dataclass
class NormalizedPage:
    markdown: str
    meta: dict[str, str]
    warnings: list[str]


def normalize(text: str, page_url: str) -> NormalizedPage:
    """Normalize one mirrored page; `page_url` is its canonical URL (no .md)."""
    return _normalize(text, page_url)[0]


# --------------------------------------------------------------------------
# Vocabulary

CALLOUTS = {
    "Note", "Tip", "Warning", "Info", "Check", "Danger", "Caution",
    "Important", "Success", "Error", "Callout",
}
ALERT = re.compile(r"\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][ \t]*$", re.I)
# Link-like components that render as a card with their text as the title.
CARD_LINKS = {"HomeJourneyLink", "HomeCardLink", "HomeQuickChip", "HomeCloudPartnerLink"}
# Layout wrappers whose content is kept as is.
UNWRAP = {"HomePage", "HomeSection", "div", "span", "section", "article", "main",
          "center", "p", "Fragment", "React.Fragment"}
# Attributes that only affect presentation on the website.
DECORATIVE = {
    "icon", "iconType", "color", "cols", "exclude", "defaultLanguage", "pictogram",
    "horizontal", "arrow", "class", "className", "style", "width", "height",
    "autoPlay", "autoplay", "muted", "loop", "playsInline", "controls", "preload",
    "align", "valign", "last", "type", "media", "noZoom", "zoom", "status",
    "imageDark", "imageHeight", "imageOffsetLeft", "layout", "defaultOpen",
}
# Mintlify-only words in code fence info strings.
FENCE_FLAGS = {"wrap", "expandable", "lines", "focus", "numberLines", "noCopy", "copy"}
# Elements that start a block even in the middle of a line.
BLOCK_TAGS = {
    "details", "pre", "ul", "ol", "table", "blockquote", "video", "iframe", "audio",
    "figure", "h1", "h2", "h3", "h4", "h5", "h6", "hr",
} | CALLOUTS | {
    "Tabs", "Tab", "CodeGroup", "Steps", "Step", "Accordion", "AccordionGroup",
    "CardGroup", "Card", "Columns", "Frame", "ParamField", "ResponseField", "Expandable",
    "FileExplorer", "File",
}
HTML_VOID = {"br", "hr", "img", "source", "input", "wbr", "col", "area", "embed",
             "track", "meta", "link", "param"}
HTML_TAGS = HTML_VOID | {
    "a", "abbr", "b", "blockquote", "caption", "center", "cite", "code", "colgroup",
    "dd", "del", "details", "dfn", "div", "dl", "dt", "em", "figcaption", "figure",
    "font", "h1", "h2", "h3", "h4", "h5", "h6", "i", "iframe", "ins", "kbd", "label",
    "li", "mark", "ol", "p", "picture", "pre", "q", "s", "samp", "section", "small",
    "span", "strike", "strong", "sub", "summary", "sup", "table", "tbody", "td",
    "tfoot", "th", "thead", "tr", "tt", "u", "ul", "var", "video", "audio", "article",
    "main", "nav", "header", "footer", "aside", "script", "style", "svg", "button",
}
HTML_BLOCK = {"div", "p", "section", "article", "main", "center", "nav", "header", "footer",
              "aside", "script", "style", "svg", "picture", "dl", "form"} | (BLOCK_TAGS - CALLOUTS)
# Components that live inside a line of text.
INLINE_COMPONENTS = {"Badge", "Eligible", "Tooltip", "Icon", "Kbd"}
GROUPS = {"card": "cards", "step": "steps", "tab": "tabs"}

FENCE_OPEN = re.compile(r"^([ \t]*)(`{3,}|~{3,})(.*)$")
FENCE_CLOSE = re.compile(r"^([ \t]*)(`{3,}|~{3,})[ \t]*$")
LIST_ITEM = re.compile(r"^([ \t]*)([-+*]|\d{1,9}[.)])([ \t]+|$)")
HEADING = re.compile(r"^[ \t]*#{1,6}(?:[ \t]|$)")
NAME = re.compile(r"[A-Za-z][\w.:-]*")
ATTR_NAME = re.compile(r"[A-Za-z_:@][\w.:-]*")
UNQUOTED = re.compile(r"[^\s\"'=<>`]+")
AUTOLINK = re.compile(r"<([A-Za-z][A-Za-z0-9+.-]{1,31}:[^\s<>]*|[\w.!#$%&'*+/=?^`{|}~-]+@[\w-]+(?:\.[\w-]+)*)>")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
BOILERPLATE = re.compile(
    r"\A> ## Documentation Index\n"
    r"> Fetch the complete documentation index at: (\S+)\n"
    r"> Use this file to discover all available pages before exploring further\.\n"
)
LINEBREAK = "[]{.linebreak}"
FENCED = re.compile(r"(`{3,}|~{3,}|:{3,})")
INTERRUPTS = re.compile(r"(?:[-+*]|1[.)])[ \t]+\S|>")
REFDEF = re.compile(r"(\[[^\]\n]+\]:[ \t]*)([^\s<>][^\s]*)")


class JsxExpr(str):
    """A JSX attribute expression that is not a plain literal."""


@dataclass
class Tag:
    name: str
    attrs: dict[str, object]
    closing: bool
    selfclosing: bool
    start: int
    end: int


# --------------------------------------------------------------------------
# Small helpers


def indent_of(line: str) -> int:
    """Leading whitespace width in columns (tabs stop every 4)."""
    col = 0
    for ch in line:
        if ch == " ":
            col += 1
        elif ch == "\t":
            col += 4 - col % 4
        else:
            break
    return col


def strip_cols(line: str, n: int) -> str:
    """Remove up to `n` columns of leading whitespace, splitting tabs."""
    col = i = 0
    while i < len(line) and col < n:
        ch = line[i]
        if ch == " ":
            col += 1
        elif ch == "\t":
            width = 4 - col % 4
            if col + width > n:
                return " " * (col + width - n) + line[i + 1 :]
            col += width
        else:
            break
        i += 1
    return line[i:]


def trim_blank(lines: list[str]) -> list[str]:
    a, b = 0, len(lines)
    while a < b and not lines[a].strip():
        a += 1
    while b > a and not lines[b - 1].strip():
        b -= 1
    return lines[a:b]


def skip_ws(s: str, i: int) -> int:
    while i < len(s) and s[i] in " \t\r\n":
        i += 1
    return i


def match_brace(s: str, i: int) -> int:
    """Index after the `}` matching the `{` at s[i], or -1."""
    depth = 0
    j = i
    while j < len(s):
        ch = s[j]
        if ch in "\"'`":
            k = j + 1
            while k < len(s) and s[k] != ch:
                k += 2 if s[k] == "\\" else 1
            j = k + 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    return -1


def jsx_value(expr: str) -> object:
    e = expr.strip()
    if re.fullmatch(r"-?\d+(\.\d+)?", e):
        return e
    if e in ("true", "false"):
        return e == "true"
    if e in ("null", "undefined"):
        return None
    if len(e) >= 2 and e[0] == e[-1] and e[0] in "\"'":
        try:
            return json.loads(e) if e[0] == '"' else e[1:-1].replace("\\'", "'")
        except json.JSONDecodeError:
            return e[1:-1]
    if len(e) >= 2 and e[0] == e[-1] == "`" and "${" not in e:
        return e[1:-1]
    return JsxExpr(e)


def parse_tag(s: str, i: int) -> Tag | None:
    """Parse an HTML/JSX tag starting at s[i] == '<'."""
    j = i + 1
    closing = s.startswith("/", j)
    if closing:
        j += 1
    m = NAME.match(s, j)
    if not m:
        return None
    name, j = m.group(), m.end()
    attrs: dict[str, object] = {}
    while True:
        k = skip_ws(s, j)
        if s.startswith("/>", k):
            return Tag(name, attrs, closing, True, i, k + 2)
        if s.startswith(">", k):
            return Tag(name, attrs, closing, False, i, k + 1)
        if k == j or closing:  # attributes must be separated by whitespace
            return None
        if s.startswith("{", k):  # {...spread}
            e = match_brace(s, k)
            if e < 0:
                return None
            attrs[s[k:e]] = JsxExpr(s[k + 1 : e - 1])
            j = e
            continue
        m = ATTR_NAME.match(s, k)
        if not m:
            return None
        an, j = m.group(), m.end()
        k = skip_ws(s, j)
        if not s.startswith("=", k):
            attrs[an] = True
            continue
        k = skip_ws(s, k + 1)
        if k >= len(s):
            return None
        if s[k] in "\"'":
            e = s.find(s[k], k + 1)
            if e < 0:
                return None
            attrs[an] = html.unescape(s[k + 1 : e])
            j = e + 1
        elif s[k] == "{":
            e = match_brace(s, k)
            if e < 0:
                return None
            attrs[an] = jsx_value(s[k + 1 : e - 1])
            j = e
        else:
            m = UNQUOTED.match(s, k)
            if not m:
                return None
            attrs[an] = html.unescape(m.group())
            j = m.end()


def code_span_end(s: str, i: int) -> int:
    """If s[i] starts a code span, the index after it; else -1."""
    j = i
    while j < len(s) and s[j] == "`":
        j += 1
    run = j - i
    k = j
    while True:
        k = s.find("`" * run, k)
        if k < 0:
            return -1
        e = k + run
        if (e >= len(s) or s[e] != "`") and s[k - 1] != "`":
            return e
        while k < len(s) and s[k] == "`":
            k += 1


def mask_code(s: str) -> str:
    """Blank out code spans and backslash escapes, keeping offsets."""
    out = list(s)
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            out[i] = " "
            if s[i + 1] != "\n":
                out[i + 1] = " "
            i += 2
            continue
        if ch == "`":
            e = code_span_end(s, i)
            if e < 0:
                while i < len(s) and s[i] == "`":
                    i += 1
                continue
            for k in range(i, e):
                if out[k] != "\n":
                    out[k] = " "
            i = e
            continue
        i += 1
    return "".join(out)


def md_escape(text: str) -> str:
    """Escape text so Markdown reads it literally (single line)."""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"([\\`*_\[\]<>#|~^])", r"\\\1", text)
    return re.sub(r"^([-+=:]|\d+[.)])", r"\\\1", text)


def plain(markdown: str) -> str:
    """Rough plain text of inline Markdown, for attribute values."""
    s = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", markdown)
    s = re.sub(r"\\([!-/:-@\[-`{-~])", r"\1", s)
    s = re.sub(r"\*\*(.+?)\*\*|__(.+?)__", lambda m: m.group(1) or m.group(2), s)
    return re.sub(r"\s+", " ", s).strip()


def div_attr(value: str) -> str:
    value = re.sub(r"\s+", " ", str(value)).strip()
    return value.replace("&", "&amp;").replace('"', "&quot;")


def div(cls: str, attrs: dict[str, object], body: list[str], ident: str | None = None) -> list[str]:
    parts = [f"#{ident}"] if ident else []
    parts.append(f".{cls}")
    parts += [f'{k}="{div_attr(v)}"' for k, v in attrs.items() if v not in (None, "")]
    depth = max((len(m.group(1)) for line in body if (m := re.match(r"\s*(:{3,})", line))), default=2)
    fence = ":" * (depth + 1)
    body = trim_blank(body)
    return [f"{fence} {{{' '.join(parts)}}}", "", *body, *([""] if body else []), fence]


def fence_lines(lang: str, title: str | None, content: list[str], warn, ident: str | None = None) -> list[str]:
    """A fenced code block in attribute syntax around `content` lines."""
    parts = [f"#{ident}"] if ident else []
    if lang:
        if re.fullmatch(r"[A-Za-z0-9_][\w+#.-]*", lang):
            parts.append("." + lang)
        else:
            warn("code-lang", f"unusable language {lang!r} dropped")
    tick = "`"
    if title:
        title = re.sub(r"\s+", " ", title).strip()
        if '"' in title:
            warn("code-title", f"double quote in title {title!r} replaced")
            title = title.replace('"', "'")
        if "`" in title:
            tick = "~"
        title = title.replace("\\", "\\\\").replace("&", "&amp;")
        parts.append(f'title="{title}"')
    longest = max((len(m.group(1)) for line in content
                   if (m := re.match(r"[ \t]*(" + re.escape(tick) + "+)", line))), default=0)
    fence = tick * max(3, longest + 1)
    return [fence + ("{" + " ".join(parts) + "}" if parts else ""), *content, fence]


def parse_info(info: str) -> tuple[str, str | None, list[str]]:
    """Split a Mintlify fence info string into (language, title, dropped)."""
    tokens: list[str] = []
    i = 0
    s = info.strip()
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        j = i
        while j < len(s) and not s[j].isspace():
            if s[j] == "{":
                e = match_brace(s, j)
                j = e if e > 0 else len(s)
            elif s[j] in "\"'" and j > i and s[j - 1] == "=":
                e = s.find(s[j], j + 1)
                j = e + 1 if e > 0 else len(s)
            else:
                j += 1
        tokens.append(s[i:j])
        i = j
    lang = ""
    if tokens and "=" not in tokens[0] and not tokens[0].startswith("{"):
        lang = tokens.pop(0)
    title = None
    words, dropped = [], []
    for t in tokens:
        key, eq, val = t.partition("=")
        if eq and key == "title":
            title = val[1:-1] if val[:1] in "\"'" and val[-1:] == val[:1] else val
        elif eq and re.fullmatch(r"[\w-]+", key):
            dropped.append(t)
        elif t.startswith("{") or t in FENCE_FLAGS:
            dropped.append(t)
        else:
            words.append(t)
    if words and title is None:
        title = " ".join(words)
    elif words:
        dropped += words
    return lang, title, dropped


def open_fence(line: str) -> tuple[int, str, str] | None:
    m = FENCE_OPEN.match(line)
    if not m or (m.group(2)[0] == "`" and "`" in m.group(3)):
        return None
    return indent_of(line), m.group(2), m.group(3)


def fence_end(lines: list[str], i: int, ind: int, marker: str) -> tuple[int, bool]:
    """Index of the closing fence of the fence opened at lines[i]."""
    for j in range(i + 1, len(lines)):
        m = FENCE_CLOSE.match(lines[j])
        if (m and m.group(2)[0] == marker[0] and len(m.group(2)) >= len(marker)
                and indent_of(lines[j]) <= ind + 3):
            return j, True
    return len(lines), False


def code_lines(lines: list[str]) -> list[bool]:
    """Mark lines that are fence content or closers (not openers)."""
    marks = [False] * len(lines)
    i = 0
    while i < len(lines):
        f = open_fence(lines[i])
        if f:
            j, _ = fence_end(lines, i, f[0], f[1])
            for k in range(i + 1, min(j + 1, len(lines))):
                marks[k] = True
            i = j + 1
        else:
            i += 1
    return marks


def absolute(url: str, base: str) -> str:
    url = url.strip()
    if not url or url.startswith("#") or SCHEME.match(url) or url.startswith("//"):
        return url
    return urljoin(base, url)


# --------------------------------------------------------------------------
# Frontmatter


def parse_yaml(lines: list[str]) -> object:
    """The small YAML subset used in frontmatter: maps, lists, scalars."""
    items = [(indent_of(l), l.strip()) for l in lines if l.strip() and not l.strip().startswith("#")]

    def scalar(v: str) -> str:
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] == '"':
            return json.loads(v)
        if len(v) >= 2 and v[0] == v[-1] == "'":
            return v[1:-1].replace("''", "'")
        return re.sub(r"\s+#.*$", "", v)

    def block(i: int, ind: int) -> tuple[object, int]:
        if items[i][1] == "-" or items[i][1].startswith("- "):
            seq: list[object] = []
            while i < len(items) and items[i][0] == ind and (items[i][1] == "-" or items[i][1].startswith("- ")):
                rest = items[i][1][1:].strip()
                i += 1
                if rest:
                    seq.append(scalar(rest))
                elif i < len(items) and items[i][0] > ind:
                    v, i = block(i, items[i][0])
                    seq.append(v)
                else:
                    seq.append("")
            return seq, i
        out: dict[str, object] = {}
        while i < len(items) and items[i][0] == ind:
            m = re.match(r'^("(?:[^"\\]|\\.)*"|\'[^\']*\'|[^:]+?)[ \t]*:(?:[ \t]+(.*))?$', items[i][1])
            if not m:
                raise ValueError(f"cannot parse {items[i][1]!r}")
            key, rest = scalar(m.group(1)), (m.group(2) or "").strip()
            i += 1
            if rest in ("|", ">", "|-", ">-", "|+", ">+"):
                body = []
                while i < len(items) and items[i][0] > ind:
                    body.append(items[i][1])
                    i += 1
                out[key] = ("\n" if rest[0] == "|" else " ").join(body)
            elif rest:
                parts = [rest]
                while i < len(items) and items[i][0] > ind:  # folded plain scalar
                    parts.append(items[i][1])
                    i += 1
                out[key] = scalar(" ".join(parts))
            elif i < len(items) and items[i][0] > ind:
                out[key], i = block(i, items[i][0])
            elif i < len(items) and items[i][0] == ind and items[i][1].startswith("- "):
                out[key], i = block(i, ind)
            else:
                out[key] = ""
        return out, i

    if not items:
        return {}
    value, i = block(0, items[0][0])
    if i != len(items):
        raise ValueError(f"unexpected {items[i][1]!r}")
    return value


def flatten(value: object, prefix: str = "") -> dict[str, str]:
    if isinstance(value, dict):
        out: dict[str, str] = {}
        for k, v in value.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else str(k)))
        return out
    if isinstance(value, list):
        if all(not isinstance(v, (dict, list)) for v in value):
            return {prefix: "\n".join(str(v) for v in value)}
        out = {}
        for n, v in enumerate(value):
            out.update(flatten(v, f"{prefix}.{n}"))
        return out
    return {prefix: "" if value is None else str(value)}


# --------------------------------------------------------------------------
# Converter


class Converter:
    def __init__(self, page_url: str, mdx: bool):
        self.base = page_url
        self.mdx = mdx  # the page is MDX source rather than exported Markdown
        self.warnings: list[str] = []
        self.dropped: list[str] = []  # text removed on purpose (for --check)
        self.permalinks = 0  # [Permalink](#...) anchors in exported schema pages
        self.copy_labels = 0  # "Copy" button labels inside exported <pre>

    def warn(self, kind: str, detail: str) -> None:
        self.warnings.append(f"{kind}: {detail}")

    def drop(self, text: str, kind: str | None = None, detail: str | None = None) -> None:
        self.dropped.append(text)
        if kind:
            self.warn(kind, detail or text[:80])

    # -- blocks -------------------------------------------------------------

    def convert(self, lines: list[str], parent: str = "") -> list[str]:
        """Convert container content (already dedented) to Pandoc Markdown."""
        lines = list(lines)
        out: list[str] = []
        para: list[str] = []
        lists: list[int] = []
        group: list = []  # [kind, indent, [blocks]]
        prev_blank = True
        shift = 0
        marker = ""  # a list marker whose item starts with the next block

        def blank() -> None:
            if out and out[-1] != "":
                out.append("")

        def flush_group() -> None:
            if group:
                kind, ind, blocks = group
                body: list[str] = []
                for b in blocks:
                    body += ["", *b]
                emit(div(GROUPS[kind], {}, body), ind, grouped=True)
                group.clear()

        def emit(block: list[str], ind: int, kind: str | None = None, grouped: bool = False) -> None:
            nonlocal marker
            if not grouped and not marker and kind in GROUPS and parent != GROUPS[kind]:
                if group and (group[0] != kind or group[1] != ind):
                    flush_group()
                if not group:
                    group.extend([kind, ind, []])
                group[2].append(block)
                return
            if not grouped:
                flush_group()
            # Blank lines only where Markdown needs them: extra ones would
            # turn a tight list loose. Fences, lists and quotes interrupt a
            # paragraph; only a closing fence ends a block without one.
            if not (FENCED.match(block[0]) or INTERRUPTS.match(block[0])):
                blank()
            first = marker + block[0] if marker else " " * ind + block[0]
            out.append(first)
            out.extend(" " * ind + l if l else "" for l in block[1:])
            marker = ""
            if not FENCED.match(block[-1]):
                out.append("")

        def flush_para() -> None:
            if not para:
                return
            flush_group()
            run: list[str] = []
            for line in para + [None]:
                special = line is not None and (line.lstrip().startswith("|") or HEADING.match(line))
                if line is None or special:
                    if run:
                        out.extend(self.inline("\n".join(run)).split("\n"))
                        run = []
                    if line is not None:
                        out.append(trim_breaks(self.inline(line, cell=True)))
                else:
                    run.append(line)
            para.clear()

        def out_indent(ind: int) -> int:
            return max((c for c in lists if c <= ind), default=0)

        i = 0
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                flush_para()
                blank()
                prev_blank = True
                i += 1
                continue
            ind = indent_of(line)
            if prev_blank or not para:
                while lists and lists[-1] > ind:
                    lists.pop()
            stripped = line.lstrip(" \t")

            f = open_fence(line)
            if f:
                flush_para()
                j, closed = fence_end(lines, i, f[0], f[1])
                if not closed:
                    self.warn("unclosed-fence", stripped[:60])
                k = out_indent(ind)
                emit(self.fence(f[2], [strip_cols(l, ind) for l in lines[i + 1 : j]]), k)
                i, prev_blank = j + 1, False
                continue

            if stripped.startswith(">") and ind <= out_indent(ind) + 3:
                flush_para()
                j = i
                while j < len(lines) and lines[j].strip() and indent_of(lines[j]) == ind \
                        and lines[j].lstrip(" \t").startswith(">"):
                    j += 1
                inner = [re.sub(r"^> ?", "", strip_cols(l, ind)) for l in lines[i:j]]
                k = out_indent(ind)
                if inner and ALERT.match(inner[0].strip()):
                    kind = ALERT.match(inner[0].strip()).group(1).lower()
                    self.drop(inner[0])
                    emit(div("callout", {"kind": kind}, self.convert(inner[1:], "callout")), k)
                else:
                    body = self.convert(inner, "blockquote")
                    emit(["> " + l if l else ">" for l in body], k)
                i, prev_blank = j, False
                continue

            if stripped.startswith("<!--"):
                flush_para()
                text = "\n".join(lines[i:])
                start = len(line) - len(stripped)
                e = text.find("-->", start)
                end = len(text) if e < 0 else e + 3
                self.drop(text[start:end], "html-comment", re.sub(r"\s+", " ", text[start:end])[:80])
                rest = text[end:]
                consumed = text[:end].count("\n")
                tail = rest.split("\n", 1)[0]
                lines[i + consumed] = " " * ind + tail if tail.strip() else ""
                i += consumed
                continue

            if stripped.startswith("<"):
                r = self.block_element(lines, i, ind)
                if r:
                    flush_para()
                    block, kind, nxt = r
                    if block:
                        emit(block, out_indent(ind), kind)
                    elif marker:
                        para.append(marker.rstrip())
                        marker = ""
                    i, prev_blank = nxt, False
                    continue

            m = LIST_ITEM.match(line)
            rest = line[m.end() :] if m else ""
            if m and rest and (open_fence(rest) or rest.startswith(">") or self.starts_block(rest)):
                flush_para()
                marker = line[: m.end()].expandtabs(4)
                while lists and lists[-1] >= len(marker):
                    lists.pop()
                lists.append(len(marker))
                lines[i] = " " * len(marker) + rest
                continue
            col = ind
            if m:
                while lists and lists[-1] > ind:
                    lists.pop()
                gap = len(m.group(3).expandtabs(4))
                col = indent_of(m.group(1)) + len(m.group(2)) + (gap if 0 < gap <= 4 else 1)
                if not lists or lists[-1] < col:
                    lists.append(col)

            if not stripped.startswith("|"):
                pos = self.block_tag_pos(line, ind)
                if pos is not None:
                    lines[i : i + 1] = [line[:pos].rstrip(), " " * col + line[pos:]]
                    if not lines[i].strip():
                        del lines[i]
                    continue

            if not para:
                # MDX has no indented code blocks; CommonMark would make one.
                base = out_indent(ind)
                shift = ind - base if ind - base >= 4 and not m else 0
                if shift and not self.mdx:
                    self.warn("indented-code", stripped[:60])
                    shift = 0
            line = strip_cols(line, shift) if shift else line
            if marker:
                line, marker = marker + line.lstrip(), ""
            para.append(line)
            prev_blank = False
            i += 1
        flush_para()
        flush_group()
        while out and out[-1] == "":
            out.pop()
        return out

    def fence(self, info: str, content: list[str]) -> list[str]:
        lang, title, dropped = parse_info(info)
        if dropped:
            self.drop(" ".join(dropped))
        return fence_lines(lang, title, content, self.warn)

    def starts_block(self, text: str) -> bool:
        """Whether text begins with a block-level tag."""
        if not text.startswith("<"):
            return False
        tag = parse_tag(text, 0)
        return bool(tag and not tag.closing and tag.name in BLOCK_TAGS | HTML_BLOCK)

    def block_tag_pos(self, line: str, ind: int) -> int | None:
        """Offset of a block-level tag in the middle of a text line."""
        masked = mask_code(line)
        for m in re.finditer(r"<([A-Za-z][\w.]*)", masked):
            if m.start() <= ind or m.group(1) not in BLOCK_TAGS:
                continue
            tag = parse_tag(line, m.start())
            if tag and not tag.closing:
                return m.start()
        return None

    def body_window(self, lines: list[str], i: int) -> tuple[str, list[int]]:
        text = "\n".join(lines[i:])
        starts, pos = [], 0
        for l in lines[i:]:
            starts.append(pos)
            pos += len(l) + 1
        return text, starts

    def block_element(self, lines: list[str], i: int, ind: int) -> tuple[list[str], str | None, int] | None:
        """Convert the element whose tag starts lines[i]; None if not a tag."""
        text, starts = self.body_window(lines, i)
        col = len(lines[i]) - len(lines[i].lstrip(" \t"))
        tag = parse_tag(text, col)
        if tag is None or not self.known(tag.name):
            return None
        if tag.closing:
            self.drop(text[tag.start : tag.end], "stray-close", f"</{tag.name}>")
            return self.after(lines, i, starts, tag.end, ind, [], None)
        if tag.selfclosing or tag.name.lower() in HTML_VOID:
            block, kind = self.element(tag, None)
            return self.after(lines, i, starts, tag.end, ind, block, kind)
        close = self.find_close(text, tag)
        if tag.name == "pre" and close:  # whitespace inside <pre> is content
            return self.after(lines, i, starts, close[1], ind, self.pre(tag, text[tag.end : close[0]]), None)
        if close is None:
            if tag.name not in BLOCK_TAGS | HTML_BLOCK | CARD_LINKS | UNWRAP:
                return None  # a placeholder such as <T> at the start of a line
            self.warn("unclosed-tag", f"<{tag.name}>")
            block, kind = self.element(tag, self.split_body(text[tag.end :]))
            return block, kind, len(lines)
        block, kind = self.element(tag, self.split_body(text[tag.end : close[0]]))
        return self.after(lines, i, starts, close[1], ind, block, kind)

    def after(self, lines, i, starts, end, ind, block, kind):
        """Put the text after an element back as a line; return the next index."""
        li = max(k for k, s in enumerate(starts) if s <= end)
        rest = lines[i + li][end - starts[li] :]
        if rest.strip():
            lines[i + li] = " " * ind + rest.lstrip()
            return block, kind, i + li
        return block, kind, i + li + 1

    def known(self, name: str) -> bool:
        """Whether a tag at the start of a line opens a block element."""
        if name in INLINE_COMPONENTS:
            return False
        return name in BLOCK_TAGS or name in HTML_BLOCK or name in CARD_LINKS \
            or name[:1].isupper() and not name.isupper()

    def find_close(self, text: str, tag: Tag) -> tuple[int, int] | None:
        """(start, end) of the tag closing `tag` in text, skipping code."""
        lines = text[tag.end :].split("\n")
        marks = code_lines(lines)
        masked = "\n".join(" " * len(l) if marks[k] or open_fence(l) else mask_code(l)
                            for k, l in enumerate(lines))
        pat = re.compile(r"<(/?)" + re.escape(tag.name) + r"(?=[\s/>])")
        depth = 1
        for m in pat.finditer(masked):
            t = parse_tag(text, tag.end + m.start())
            if t is None:
                continue
            if t.closing:
                depth -= 1
                if depth == 0:
                    return tag.end + m.start(), t.end
            elif not t.selfclosing:
                depth += 1
        return None

    def split_body(self, body: str) -> list[str]:
        """Body text of an element as dedented lines."""
        lines = body.split("\n")
        first = lines[0].strip()
        rest = lines[1:]
        marks = code_lines(rest)
        indents = [indent_of(l) for k, l in enumerate(rest) if l.strip() and not marks[k]]
        if rest and not rest[-1].strip():
            rest = rest[:-1]
        d = min(indents, default=0)
        rest = [strip_cols(l, d) for l in rest]
        return ([first] if first else []) + rest

    # -- elements -----------------------------------------------------------

    def attrs_used(self, tag: Tag, used: set[str]) -> None:
        for k, v in tag.attrs.items():
            if k in used:
                continue
            if v is not True and v is not None:
                self.dropped.append(str(v))
            self.dropped.append(k)
            if k not in DECORATIVE:
                self.warn("dropped-attribute", f"{tag.name}.{k}={v!r}"[:100])

    def ident(self, tag: Tag) -> str | None:
        v = tag.attrs.get("id")
        if isinstance(v, str) and re.fullmatch(r"[A-Za-z][\w.:-]*", v):
            return v
        if v is not None:
            self.warn("dropped-attribute", f"{tag.name}.id={v!r}")
        return None

    def text_attr(self, tag: Tag, name: str) -> str | None:
        v = tag.attrs.get(name)
        if v is None or v is False:
            return None
        if v is True:
            return "true"
        if isinstance(v, JsxExpr):
            self.warn("jsx-expression", f"{tag.name}.{name}={{{v}}}"[:100])
        return str(v)

    def element(self, tag: Tag, body: list[str] | None) -> tuple[list[str], str | None]:
        name = tag.name
        body = body or []
        conv = lambda parent="": self.convert(body, parent)  # noqa: E731
        if name in CALLOUTS:
            self.attrs_used(tag, {"title", "id"})
            attrs = {"kind": name.lower(), "title": self.text_attr(tag, "title")}
            return div("callout", attrs, conv("callout"), self.ident(tag)), None
        if name in ("Tabs", "HomeJourney"):
            self.attrs_used(tag, set())
            return div("tabs", {}, self.only(conv("tabs"), name, "tab")), None
        if name in ("Tab", "HomeJourneyTab"):
            self.attrs_used(tag, {"title", "label", "id"})
            title = self.text_attr(tag, "title") or self.text_attr(tag, "label")
            return div("tab", {"title": title}, conv("tab"), self.ident(tag)), "tab"
        if name == "CodeGroup":
            self.attrs_used(tag, set())
            return div("codegroup", {}, conv("codegroup")), None
        if name == "CodeGroupItem":
            self.attrs_used(tag, {"language", "title"})
            title = self.text_attr(tag, "language") or self.text_attr(tag, "title")
            return (div("tab", {"title": title}, conv("tab")) if title else conv()), None
        if name == "FileExplorer":
            self.attrs_used(tag, set())
            return div("codegroup", {}, conv("codegroup")), None
        if name == "File":
            self.attrs_used(tag, {"filename"})
            return self.titled_code(body, self.text_attr(tag, "filename"), tag), None
        if name == "Steps":
            self.attrs_used(tag, set())
            return div("steps", {}, self.only(conv("steps"), name, "step")), None
        if name in ("Step", "HomeJourneyStep"):
            self.attrs_used(tag, {"title", "id"})
            return div("step", {"title": self.text_attr(tag, "title")}, conv("step"), self.ident(tag)), "step"
        if name in ("Accordion", "Expandable"):
            self.attrs_used(tag, {"title", "id"})
            return div("accordion", {"title": self.text_attr(tag, "title")}, conv("accordion"), self.ident(tag)), None
        if name == "AccordionGroup":
            self.attrs_used(tag, set())
            return div("accordiongroup", {}, conv("accordiongroup")), None
        if name == "details":
            return self.details(tag, body), None
        if name in ("CardGroup", "Columns", "HomePlatformCards"):
            self.attrs_used(tag, set())
            return div("cards", {}, conv("cards")), None
        if name in ("Card", "HomePlatformCard"):
            return self.card(tag, body), "card"
        if name in CARD_LINKS:
            self.attrs_used(tag, {"href", "title"})
            label = plain(" ".join(body))
            title = self.text_attr(tag, "title") or label
            if label and title != label:
                self.warn("card-label", f"{name} label {label!r} dropped")
            href = self.text_attr(tag, "href")
            return div("card", {"title": title, "href": absolute(href, self.base) if href else None}, []), "card"
        if name == "Frame":
            self.attrs_used(tag, {"caption"})
            return div("frame", {"caption": self.text_attr(tag, "caption")}, conv("frame")), None
        if name in ("ParamField", "ResponseField"):
            return self.field(tag, body), None
        if name in ("HomeHero", "HomeSectionHeader", "HomePartnerLinks"):
            return self.heading_block(tag, body), None
        if name in UNWRAP:
            self.attrs_used(tag, {"id"} if name[0].islower() else set())
            return conv(), None
        if name in ("img", "Image"):
            return [self.image(tag)], None
        if name in ("video", "iframe", "audio", "embed", "object"):
            return [self.media(tag, body)], None
        if name == "pre":
            return self.pre(tag, "\n".join(body)), None
        if name == "table":
            return self.table(tag, "\n".join(body)), None
        if name in ("ul", "ol"):
            return self.html_list(tag, "\n".join(body)), None
        if name == "blockquote":
            self.attrs_used(tag, set())
            return ["> " + l if l else ">" for l in conv("blockquote")], None
        if re.fullmatch(r"h[1-6]", name):
            self.attrs_used(tag, {"id"})
            return ["#" * int(name[1]) + " " + self.inline(" ".join(body), cell=True)], None
        if name == "hr":
            return ["* * *"], None
        if name in ("br", "source", "wbr"):
            return [], None
        if name in ("script", "style", "svg", "button"):
            self.drop(" ".join(body), "dropped-element", f"<{name}>")
            return [], None
        return self.component(tag, body), None

    def only(self, lines: list[str], name: str, child: str) -> list[str]:
        """Warn about content in a container that is not one of its children."""
        depth = 0
        for line in lines:
            s = line.strip()
            m = re.match(r"(:{3,})\s*(\{.*)?$", s)
            if m:
                if m.group(2):
                    if depth == 0 and not re.match(r"\{(#\S+ )?\." + child + r"[ }]", m.group(2)):
                        self.warn("stray-content", f"<{name}> holds {m.group(2)[:40]}")
                    depth += 1
                else:
                    depth -= 1
            elif s and depth == 0:
                self.warn("stray-content", f"<{name}> holds text {s[:50]!r}")
                break
        return lines

    def titled_code(self, body: list[str], title: str | None, tag: Tag) -> list[str]:
        """A <File filename> holding one code block: the block, titled."""
        lines = trim_blank(body)
        f = open_fence(lines[0]) if lines else None
        if f and title:
            j, closed = fence_end(lines, 0, f[0], f[1])
            if closed and j == len(lines) - 1:
                lang, own, dropped = parse_info(f[2])
                if own and own != title:
                    self.warn("dropped-attribute", f"{tag.name}: code title {own!r} replaced by {title!r}")
                    dropped.append(own)
                if dropped:
                    self.drop(" ".join(dropped))
                return fence_lines(lang, title, [strip_cols(l, f[0]) for l in lines[1:j]], self.warn)
        self.warn("unknown-component", f"<{tag.name}> without a single code block")
        return div("component", {"name": tag.name, "filename": title}, self.convert(body))

    def details(self, tag: Tag, body: list[str]) -> list[str]:
        self.attrs_used(tag, {"open", "id"})
        text = "\n".join(body)
        title = None
        m = re.match(r"\s*<summary(\s[^>]*)?>(.*?)</summary>", text, re.S)
        if m:
            title = plain(self.inline(m.group(2).strip(), cell=True).replace(LINEBREAK, " "))
            text = text[m.end() :]
        else:
            self.warn("details-without-summary", text.strip()[:60])
        return div("accordion", {"title": title}, self.convert(self.split_body("\n" + text), "accordion"),
                   self.ident(tag))

    def card(self, tag: Tag, body: list[str]) -> list[str]:
        self.attrs_used(tag, {"title", "href", "img", "image", "description", "id"})
        href = self.text_attr(tag, "href")
        image = self.text_attr(tag, "img") or self.text_attr(tag, "image")
        lines = []
        if tag.attrs.get("description"):
            lines += [md_escape(str(tag.attrs["description"])), ""]
        lines += self.convert(body, "card")
        attrs = {"title": self.text_attr(tag, "title"), "href": absolute(href, self.base) if href else None,
                 "image": absolute(image, self.base) if image else None}
        return div("card", attrs, lines, self.ident(tag))

    def field(self, tag: Tag, body: list[str]) -> list[str]:
        kind = "param" if tag.name == "ParamField" else "response"
        attrs: dict[str, object] = {"kind": kind}
        used = {"type", "required", "default", "deprecated", "id"}
        for loc in ("name", "param", "path", "query", "body", "header", "cookie"):
            if loc in tag.attrs:
                attrs["name"] = self.text_attr(tag, loc)
                if loc not in ("name", "param"):
                    attrs["location"] = loc
                used.add(loc)
                break
        attrs["type"] = self.text_attr(tag, "type")
        if tag.attrs.get("required"):
            attrs["required"] = "true"
        if tag.attrs.get("deprecated"):
            attrs["deprecated"] = "true"
        attrs["default"] = self.text_attr(tag, "default")
        attrs = {"kind": attrs.pop("kind"), "name": attrs.pop("name", None), **attrs}
        self.attrs_used(tag, used)
        return div("field", attrs, self.convert(body, "field"), self.ident(tag))

    def heading_block(self, tag: Tag, body: list[str]) -> list[str]:
        """Home page banners: their attributes are visible text."""
        self.attrs_used(tag, {"eyebrow", "title", "subtitle", "label", "description"})
        lines: list[str] = []
        if tag.name == "HomeSectionHeader" and tag.attrs.get("label"):
            lines += [f"*{md_escape(str(tag.attrs['label']))}*", ""]
        if tag.attrs.get("eyebrow"):
            lines += [f"*{md_escape(str(tag.attrs['eyebrow']))}*", ""]
        if tag.attrs.get("title"):
            lines += [f"**{md_escape(str(tag.attrs['title']))}**", ""]
        for k in ("subtitle", "description"):
            if tag.attrs.get(k):
                lines += [md_escape(str(tag.attrs[k])), ""]
        if tag.name == "HomePartnerLinks" and tag.attrs.get("label"):
            lines += [md_escape(str(tag.attrs["label"])), ""]
        return lines + self.convert(body)

    def component(self, tag: Tag, body: list[str]) -> list[str]:
        attrs: dict[str, object] = {"name": tag.name}
        for k, v in tag.attrs.items():
            if k in DECORATIVE or not re.fullmatch(r"[A-Za-z_][\w-]*", k):
                self.dropped += [k, str(v)]
            else:
                attrs[k] = "true" if v is True else v
        lines = self.convert(body)
        detail = f"<{tag.name}>" + ("" if lines else " (empty)")
        self.warn("unknown-component", detail)
        return div("component", attrs, lines, None)

    def image(self, tag: Tag) -> str:
        self.attrs_used(tag, {"src", "alt", "title"})
        src = absolute(str(tag.attrs.get("src") or ""), self.base)
        if not src:
            self.warn("image-without-src", str(tag.attrs)[:60])
        alt = md_escape(str(tag.attrs.get("alt") or ""))
        title = tag.attrs.get("title")
        t = ' "' + str(title).replace('"', "&quot;") + '"' if title else ""
        return f"![{alt}](<{src}>{t})" if " " in src else f"![{alt}]({src}{t})"

    def media(self, tag: Tag, body: list[str]) -> str:
        srcs = [str(tag.attrs["src"])] if tag.attrs.get("src") else []
        text = "\n".join(body)
        for m in re.finditer(r"<source\b", text):
            t = parse_tag(text, m.start())
            if t and t.attrs.get("src"):
                srcs.append(str(t.attrs["src"]))
                self.dropped += [k for k in t.attrs] + [str(v) for k, v in t.attrs.items() if k != "src"]
        self.attrs_used(tag, {"src", "title", "aria-label", "alt"})
        srcs = [absolute(s, self.base) for s in srcs]
        label = tag.attrs.get("title") or tag.attrs.get("aria-label") or tag.attrs.get("alt")
        if not label and srcs:
            label = unquote(PurePosixPath(urlsplit(srcs[0]).path).name)
        word = "Audio" if tag.name == "audio" else "Video" if tag.name == "video" or (
            srcs and re.search(r"youtube|vimeo|loom|wistia", srcs[0])) else "Embedded content"
        if not srcs:
            self.warn("media-without-src", f"<{tag.name}>")
            return md_escape(f"{word}: {label or ''}")
        links = [f"[{md_escape(f'{word}: {label}')}]({srcs[0]})"]
        links += [f"[{md_escape(PurePosixPath(urlsplit(s).path).suffix.lstrip('.') or 'alternate')}]({s})"
                  for s in srcs[1:]]
        return " · ".join(links)

    def pre(self, tag: Tag, text: str) -> list[str]:
        self.attrs_used(tag, {"id"})
        m = re.fullmatch(r"\s*(<code[^>]*>)?(.*?)(</code>)?\s*", text, re.S)
        inner = m.group(2) if m else text
        lang = ""
        if m and m.group(1):
            lm = re.search(r'class="(?:language-)?([\w+-]+)', m.group(1))
            lang = lm.group(1) if lm else ""
        span = re.fullmatch(r"\s*(`+)(.*?)\1\s*(Copy)?\s*", inner, re.S)
        if span:  # Mintlify's flattened <pre>`code`Copy</pre>
            if span.group(3):
                self.drop("Copy")
                self.copy_labels += 1
            code = span.group(2)
            if code.startswith(" ") and code.endswith(" ") and code.strip():
                code = code[1:-1]
            code = html.unescape(code)  # HTML context: the backticks are an export artifact
            pretty = reindent_json(code)
            if pretty is not None:
                code, lang = pretty, lang or "json"
            content = code.split("\n")
        else:
            content = html.unescape(re.sub(r"<[^>]+>", "", inner)).split("\n")
            content = trim_blank(content)
        return fence_lines(lang, None, content, self.warn, self.ident(tag))

    def html_list(self, tag: Tag, text: str) -> list[str]:
        self.attrs_used(tag, set())
        items = self.html_items(text, "li")
        lines: list[str] = []
        for n, (attrs, inner) in enumerate(items, 1):
            marker = f"{n}." if tag.name == "ol" else "-"
            body = self.convert(self.split_body("\n" + inner)) or [""]
            pad = " " * (len(marker) + 1)
            lines.append(f"{marker} {body[0]}")
            lines += [pad + l if l else "" for l in body[1:]]
        return lines

    def html_items(self, text: str, name: str) -> list[tuple[dict, str]]:
        """Direct <name> children of an HTML fragment: (attrs, inner)."""
        items = []
        masked = mask_code(text)
        pos = 0
        pat = re.compile(r"<" + name + r"(?=[\s/>])")
        while (m := pat.search(masked, pos)):
            tag = parse_tag(text, m.start())
            if tag is None:
                pos = m.end()
                continue
            between = re.sub(r"<[^>]*>", "", text[pos : m.start()]).strip()
            if between:
                self.warn("stray-content", f"<{name}> sibling text {between[:40]!r}")
                self.dropped.append(between)
            close = self.find_close(text, tag)
            end = close[0] if close else len(text)
            items.append((tag.attrs, text[tag.end : end]))
            pos = close[1] if close else len(text)
        return items

    def table(self, tag: Tag, text: str) -> list[str]:
        self.attrs_used(tag, set())
        rows: list[tuple[list[str], bool]] = []
        caption = None
        cm = re.search(r"<caption[^>]*>(.*?)</caption>", text, re.S)
        if cm:
            caption = cm.group(1)
        for _, row in self.html_items(text, "tr"):
            cells, header = [], True
            for m in re.finditer(r"<(td|th)(?=[\s>])", row):
                t = parse_tag(row, m.start())
                if t is None:
                    continue
                close = self.find_close(row, t)
                inner = row[t.end : close[0]] if close else row[t.end :]
                header &= t.name == "th"
                for k in ("colspan", "rowspan"):
                    if str(t.attrs.get(k, "1")) != "1":
                        self.warn("table-span", f"{k}={t.attrs[k]}")
                cells.append(self.cell(inner))
            rows.append((cells, header))
        if not rows:
            self.warn("empty-table", "<table> without rows")
            return []
        width = max(len(c) for c, _ in rows)
        head = rows[0][0] if rows[0][1] else [""] * width
        body = rows[1:] if rows[0][1] else rows
        fmt = lambda cells: "| " + " | ".join(cells + [""] * (width - len(cells))) + " |"  # noqa: E731
        lines = [fmt(head), "|" + "---|" * width] + [fmt(c) for c, _ in body]
        if caption:
            lines += ["", self.inline(caption.strip())]
        return lines

    def cell(self, inner: str) -> str:
        """Markdown inside an HTML table cell as one pipe-table cell."""
        lines = self.split_body("\n" + inner)
        if any(open_fence(l) for l in lines):
            self.warn("table-cell-code", "code block in table cell made inline")
        paras, cur = [], []
        for l in lines + [""]:
            if l.strip():
                hard = re.search(r"(?<!\\)(\\\\)*\\$", l) or l.endswith("  ")
                text = l.strip()[:-1] if hard and l.rstrip().endswith("\\") else l.strip()
                cur.append(text + (f" {LINEBREAK}" if hard else ""))
            elif cur:
                paras.append(" ".join(cur))
                cur = []
        text = f" {LINEBREAK} ".join(self.inline(p, cell=True) for p in paras)
        return trim_breaks("|" + pipe_escape(text) + "|")[1:-1].strip()

    # -- inline -------------------------------------------------------------

    def inline(self, text: str, cell: bool = False) -> str:
        """Rewrite inline HTML/JSX in a paragraph, table row or heading."""
        out: list[str] = []
        i, n = 0, len(text)
        while i < n:
            ch = text[i]
            if ch == "\\" and i + 1 < n:
                out.append(text[i : i + 2])
                i += 2
                continue
            if ch == "`":
                e = code_span_end(text, i)
                if e < 0:
                    j = i
                    while j < n and text[j] == "`":
                        j += 1
                    out.append(text[i:j])
                    i = j
                else:
                    out.append(text[i:e])
                    i = e
                continue
            if ch == "<":
                r = self.inline_tag(text, i, cell)
                if r is not None:
                    rep, i = r
                    out.append(rep)
                    continue
                nxt = text[i + 1 : i + 2]
                out.append("\\<" if nxt and (nxt.isalpha() or nxt in "/!?") else "<")
                i += 1
                continue
            if ch == "{" and self.mdx:
                m = re.match(r"\{\s*(?:\"\s*\"|'\s*'|`\s*`)\s*\}", text[i:])
                if m:
                    out.append(" ")
                    i += m.end()
                    continue
                m = re.match(r"\{\s*/\*.*?\*/\s*\}", text[i:], re.S)
                if m:
                    self.drop(m.group(), "jsx-comment", m.group()[:60])
                    i += m.end()
                    continue
            if ch == "[" and text.startswith("[Permalink](#", i) and text.find(")", i) > 0:
                e = text.find(")", i)
                self.drop(text[i : e + 1])
                self.permalinks += 1
                i = e + 1
                continue
            if ch == "]" and text.startswith("](", i):
                r = self.link_dest(text, i + 2)
                if r is not None:
                    dest, j = r
                    out.append("](" + dest)
                    i = j
                    continue
            if ch == ":" and text.startswith(":::", i) and not text[text.rfind("\n", 0, i) + 1 : i].strip():
                out.append("\\:")  # would open or close a fenced div
                i += 1
                continue
            if ch == "[" and (i == 0 or text[i - 1] == "\n" or not text[text.rfind("\n", 0, i) + 1 : i].strip()):
                m = REFDEF.match(text, i)
                if m:  # reference definition: [label]: destination
                    out.append(m.group(1) + absolute(m.group(2), self.base))
                    i = m.end()
                    continue
            out.append(ch)
            i += 1
        return "".join(out)

    def link_dest(self, text: str, i: int) -> tuple[str, int] | None:
        """Absolutize the destination of an inline link starting at text[i]."""
        if text.startswith("<", i):
            e = text.find(">", i)
            if e < 0:
                return None
            return "<" + absolute(text[i + 1 : e], self.base) + ">", e + 1
        j, depth = i, 0
        while j < len(text) and not text[j].isspace():
            if text[j] == "\\":
                j += 2
                continue
            if text[j] == "(":
                depth += 1
            elif text[j] == ")":
                if depth == 0:
                    break
                depth -= 1
            j += 1
        dest = text[i:j]
        if not dest:
            return None
        new = absolute(dest, self.base)
        return new.replace(" ", "%20"), j

    def inline_tag(self, text: str, i: int, cell: bool) -> tuple[str, int] | None:
        m = AUTOLINK.match(text, i)
        if m:
            return m.group(), m.end()
        if text.startswith("<!--", i):
            e = text.find("-->", i)
            end = n = len(text) if e < 0 else e + 3
            self.drop(text[i:end], "html-comment", re.sub(r"\s+", " ", text[i:end])[:80])
            return "", n
        tag = parse_tag(text, i)
        if tag is None:
            return None
        name = tag.name
        lname = name.lower()
        if tag.closing:
            if name in HTML_TAGS or (name[:1].isupper() and not name.isupper() and name in BLOCK_TAGS | CARD_LINKS):
                self.drop(f"</{name}>", "stray-close", f"</{name}>")
                return "", tag.end
            return None
        if lname == "br":
            j = tag.end
            while j < len(text) and text[j] in " \t":
                j += 1
            if cell:
                return LINEBREAK, j
            if text.startswith("\n", j):
                j += 1
            rest = text[j:]
            if not rest.strip() or not text[:i].strip():
                return "", j  # a break at the start or end of a paragraph shows nothing
            # Keep the next line from starting a list, quote, heading, ...
            lead = re.match(r"[ \t]*", rest).end()
            follow = re.match(r"(?:[-+*>#|=]|\d+[.)]|:::|```|~~~)", rest[lead:])
            return "\\\n" + rest[:lead] + ("\\" if follow else ""), j + lead
        if lname in HTML_VOID or tag.selfclosing:
            if lname == "img" or name == "Image":
                return self.image(tag), tag.end
            if lname in ("hr", "wbr"):
                return "", tag.end
            if name in CARD_LINKS or name in BLOCK_TAGS:
                return None
            if name[:1].isupper() and not name.isupper():
                self.warn("unknown-inline", f"<{name} />")
                self.dropped += list(tag.attrs) + [str(v) for v in tag.attrs.values()]
                return "", tag.end
            if lname in HTML_VOID and tag.attrs:
                self.warn("dropped-element", f"<{name}>")
                self.dropped += list(tag.attrs) + [str(v) for v in tag.attrs.values()]
                return "", tag.end
            return None
        if not (name in HTML_TAGS or (name[:1].isupper() and not name.isupper())):
            return None
        close = self.find_close(text, tag)
        if close is None:
            return None
        inner = text[tag.end : close[0]]
        end = close[1]
        conv = lambda: self.inline(inner, cell)  # noqa: E731
        if lname == "sup":
            return "\\^" + conv(), end
        if lname == "sub":
            return "\\_" + conv(), end
        if lname in ("kbd", "code", "tt", "samp"):
            return code_span(html.unescape(plain_tags(inner))), end
        if lname in ("b", "strong"):
            return "**" + conv().strip() + "**", end
        if lname in ("i", "em", "cite", "var", "dfn"):
            return "*" + conv().strip() + "*", end
        if lname in ("s", "del", "strike"):
            return "~~" + conv().strip() + "~~", end
        if lname == "a":
            href = tag.attrs.get("href")
            if isinstance(href, str):
                return f"[{conv()}]({absolute(href, self.base)})", end
            return conv(), end
        if name == "Badge":
            return "\\[" + conv().strip() + "\\]", end
        if name in ("Eligible", "Tooltip") or lname in ("span", "u", "ins", "small", "font", "mark",
                                                         "abbr", "q", "label", "big", "nobr"):
            self.attrs_used(tag, {"tip", "title"} if name == "Tooltip" else set())
            tip = tag.attrs.get("tip") if name == "Tooltip" else None
            return conv() + (f" ({md_escape(str(tip))})" if tip else ""), end
        if lname in ("ul", "ol") and cell:
            items = self.html_items(inner, "li")
            parts = []
            for n, (_, li) in enumerate(items, 1):
                marker = f"{n}." if lname == "ol" else "•"
                parts.append(f"{marker} " + self.inline(re.sub(r"\s*\n\s*", " ", li.strip()), cell))
            return "".join(f"{LINEBREAK}{p} " for p in parts) + LINEBREAK, end
        if lname in ("p", "div") and cell:
            return f"{LINEBREAK}" + conv().strip() + f"{LINEBREAK}", end
        if lname in ("p", "div", "section", "center"):
            return conv(), end
        self.warn("unknown-inline", f"<{name}>")
        self.dropped += list(tag.attrs) + [str(v) for v in tag.attrs.values()]
        return conv(), end


def plain_tags(s: str) -> str:
    return re.sub(r"</?[A-Za-z][^>]*>", "", s)


def code_span(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    tick = "`" * (longest + 1)
    pad = " " if text.startswith("`") or text.endswith("`") else ""
    return f"{tick}{pad}{text}{pad}{tick}"


def trim_breaks(row: str) -> str:
    """Drop line breaks at the start or end of pipe-table cells."""
    br = re.escape(LINEBREAK)
    row = re.sub(rf"(?:\s*{br})+\s*(?=(?<!\\)\|)", " ", row)
    return re.sub(rf"((?<!\\)\|)\s*(?:{br}\s*)+", r"\1 ", row)


def pipe_escape(text: str) -> str:
    """Escape `|` that would split a pipe-table cell."""
    return re.sub(r"(?<!\\)\|", r"\\|", text)


def reindent_json(code: str) -> str | None:
    """Re-indent a JSON document flattened onto one line; None if not JSON."""
    if "\n" in code.strip():
        return None
    try:
        json.loads(code)
    except ValueError:
        return None
    tokens = re.findall(r'"(?:[^"\\]|\\.)*"|[{}\[\],:]|[^\s{}\[\],:"]+', code)
    out, depth, i = [], 0, 0
    while i < len(tokens):
        t = tokens[i]
        if t in ("{", "["):
            if i + 1 < len(tokens) and tokens[i + 1] in ("}", "]"):
                out.append(t + tokens[i + 1])
                i += 2
                continue
            depth += 1
            out.append(t + "\n" + "  " * depth)
        elif t in ("}", "]"):
            depth -= 1
            out.append("\n" + "  " * depth + t)
        elif t == ",":
            out.append(",\n" + "  " * depth)
        elif t == ":":
            out.append(": ")
        else:
            out.append(t)
        i += 1
    return "".join(out)


# --------------------------------------------------------------------------
# Page


def _normalize(text: str, page_url: str) -> tuple[NormalizedPage, Converter]:
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    meta: dict[str, str] = {}
    warnings: list[str] = []
    m = re.match(r"\A---[ \t]*\n(.*?\n)?---[ \t]*(\n|\Z)", text, re.S)
    mdx = bool(m)
    if m:
        try:
            value = parse_yaml((m.group(1) or "").split("\n"))
            meta = flatten(value) if isinstance(value, dict) else {}
            if not isinstance(value, dict):
                warnings.append("frontmatter: not a mapping")
        except (ValueError, json.JSONDecodeError) as e:
            warnings.append(f"frontmatter: {e}")
            meta = {"frontmatter": m.group(1) or ""}
        text = text[m.end() :]
    conv = Converter(page_url, mdx)
    conv.warnings = warnings
    b = BOILERPLATE.match(text)
    if b:
        conv.dropped.append(b.group())
        host = urlsplit(b.group(1)).netloc
        if host != urlsplit(page_url).netloc:
            conv.warn("boilerplate-variant", f"index at {b.group(1)}")
        text = text[b.end() :]
    elif "Documentation Index" in text[:500]:
        conv.warn("boilerplate-variant", "unrecognized Documentation Index block kept")
    body = conv.convert(text.split("\n"))
    if conv.permalinks:
        conv.warn("dropped-permalink", f"{conv.permalinks} [Permalink](#...) links")
    if conv.copy_labels:
        conv.warn("dropped-copy-label", f"{conv.copy_labels} 'Copy' button labels in <pre>")
    markdown = "\n".join(body).strip("\n") + "\n"
    return NormalizedPage(markdown, meta, conv.warnings), conv


# --------------------------------------------------------------------------
# Self-check

DIV_CLASSES = {"callout", "tabs", "tab", "codegroup", "steps", "step", "accordion",
               "accordiongroup", "cards", "card", "field", "frame", "component"}
WORD = re.compile(r"[^\W_]+(?:_+[^\W_]+)*")


def raw_fences(text: str, prose: list[str] | None = None) -> list[str]:
    """Contents of the fenced code blocks of a raw page, extracted
    independently of the converter (CommonMark indentation rules).
    Lines outside code are appended to `prose` if given."""
    blocks: list[str] = []
    fence = None  # (marker, indent, quoted, lines)
    for line in text.split("\n"):
        original = line
        quoted = bool(re.match(r"^\s*>", line))
        if fence is None or fence[2]:
            line = re.sub(r"^(\s*>)+ ?", "", line)
        if fence is None:
            line = re.sub(r"^[ \t]*(?:[-+*]|\d{1,9}[.)])[ \t]+(?=`{3}|~{3})", lambda m: " " * len(m.group()), line)
        m = re.match(r"^(\s*)(`{3,}|~{3,})(.*)$", line)
        if fence:
            if m and m.group(2)[0] == fence[0][0] and len(m.group(2)) >= len(fence[0]) \
                    and not m.group(3).strip() and indent_of(line) <= fence[1] + 3:
                blocks.append("\n".join(fence[3]))
                fence = None
            else:
                fence[3].append(strip_cols(line, fence[1]))
            continue
        if m and not (m.group(2)[0] == "`" and "`" in m.group(3)):
            fence = (m.group(2), indent_of(line), quoted, [])
        elif prose is not None:
            prose.append(original)
    if fence:
        blocks.append("\n".join(fence[3]))
    return blocks


def raw_structure(prose: list[str]) -> tuple[int, int]:
    """(headings, tables) in the non-code lines of a raw page."""
    text = mask_code("\n".join(prose))
    headings = len(re.findall(r"^[ \t>]*#{1,6}(?:[ \t]|$)", text, re.M))
    headings += len(re.findall(r"<h[1-6][\s>]", text))
    tables = len(re.findall(r"^[ \t>]*\|?[ \t]*:?-+:?[ \t]*(?:\|[ \t]*:?-+:?[ \t]*)+\|?[ \t]*$", text, re.M))
    tables += len(re.findall(r"<table[\s>]", text))
    return headings, tables


CONTAINERS = {"cards", "steps", "tabs", "codegroup", "accordiongroup"}
RAW_CLASS = {
    **{n: "callout" for n in CALLOUTS}, **{n: "card" for n in CARD_LINKS},
    "Tab": "tab", "HomeJourneyTab": "tab", "Step": "step", "HomeJourneyStep": "step",
    "Accordion": "accordion", "Expandable": "accordion", "details": "accordion",
    "Card": "card", "HomePlatformCard": "card", "Frame": "frame",
    "ParamField": "field", "ResponseField": "field",
}
NOT_DIVS = UNWRAP | INLINE_COMPONENTS | {
    "Tabs", "HomeJourney", "CodeGroup", "FileExplorer", "File", "Steps", "AccordionGroup",
    "CardGroup", "Columns", "HomePlatformCards", "HomeHero", "HomeSectionHeader",
    "HomePartnerLinks", "CodeGroupItem",
}


def raw_components(prose: list[str]) -> list[tuple[str, int]]:
    """(div class, depth) of each component in a raw page, in document order,
    as the converter should produce them (containers left out)."""
    text = "\n".join(prose)
    masked = mask_code(text)
    out: list[tuple[str, int]] = []
    stack: list[tuple[str, bool]] = []  # (tag name, counts as a level)
    skip = 0  # end of the last tag, whose attribute values may hold <placeholders>
    for m in re.finditer(r"<(/?)([A-Za-z][\w.]*)|^(?:[ \t]*>)+[ \t]?\[!(?:NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]",
                         masked, re.M | re.I):
        if m.start() < skip:
            continue
        if not m.group(2):
            out.append(("callout", sum(lvl for _, lvl in stack)))
            continue
        name = m.group(2)
        if name in HTML_TAGS - {"details"} or name in NOT_DIVS or not name[:1].isupper() and name != "details":
            continue
        tag = parse_tag(text, m.start())
        if tag is None:
            continue
        skip = tag.end
        if tag.closing:
            while stack:
                if stack.pop()[0] == name:
                    break
            continue
        if name == "CodeGroupItem":
            continue
        cls = RAW_CLASS.get(name, "component")
        out.append((cls, sum(lvl for _, lvl in stack)))
        if not tag.selfclosing:
            stack.append((name, True))
    return out


def ast_components(blocks: list) -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []

    def walk(node, depth: int) -> None:
        if isinstance(node, dict):
            if node.get("t") == "Div":
                classes = node["c"][0][1]
                cls = next((c for c in classes if c in DIV_CLASSES), "")
                if cls and cls not in CONTAINERS:
                    if not (cls == "tab" and depth_parent[-1] == "codegroup"):
                        out.append((cls, depth))
                    depth_parent.append(cls)
                    walk(node["c"][1], depth + 1)
                    depth_parent.pop()
                    return
                depth_parent.append(cls)
                walk(node["c"][1], depth)
                depth_parent.pop()
                return
            for v in node.values():
                walk(v, depth)
        elif isinstance(node, list):
            for v in node:
                walk(v, depth)

    depth_parent = [""]
    walk(blocks, 0)
    return out


def raw_words(text: str) -> Counter:
    """Words of a raw page outside markup: tag and attribute names removed."""
    text = re.sub(r"\A---[ \t]*\n.*?\n---[ \t]*\n", "", text, flags=re.S)
    text = re.sub(r"(?<!\\)</?[A-Za-z][\w.:-]*", " ", text)
    text = re.sub(r"[\w:-]+(?==[\"'{])", " ", text)
    text = re.sub(r"^[ \t>]*\[[^\]\n]+\]:", " ", text, flags=re.M)  # reference definitions
    text = re.sub(r"\]\[[^\]\n]*\]", "] ", text)  # reference labels
    text = re.sub(r"\[\^[^\]\n]+\]", " ", text)  # footnote labels
    text = re.sub(r"^[ \t>]*\d{1,9}[.)](?=[ \t]|$)", " ", text, flags=re.M)
    text = re.sub(r"\\([!-/:-@\[-`{-~])", r"\1", text)
    text = re.sub(r"&(?:#\d+|#[xX][0-9a-fA-F]+|[A-Za-z]\w*);", lambda m: html.unescape(m.group()), text)
    return Counter(w.lower() for w in WORD.findall(text))


def ast_walk(node, visit) -> None:
    if isinstance(node, dict):
        if "t" in node:
            visit(node)
        for v in node.values():
            ast_walk(v, visit)
    elif isinstance(node, list):
        for v in node:
            ast_walk(v, visit)


def ast_facts(ast: dict) -> dict:
    words: list[str] = []
    facts = {"raw": [], "code": [], "odd": [], "headers": 0, "tables": 0}

    def attr_words(attr) -> None:
        ident, classes, kvs = attr
        words.extend([ident, *classes])
        for k, v in kvs:
            words.append(v)

    def visit(n) -> None:
        t, c = n["t"], n.get("c")
        if t == "Str":
            words.append(c)
            if c.startswith(":::"):
                facts["odd"].append("stray ::: text")
        elif t in ("Code", "CodeBlock"):
            attr_words(c[0])
            words.append(c[1])
            if t == "CodeBlock":
                facts["code"].append(c[1])
        elif t in ("RawBlock", "RawInline"):
            facts["raw"].append(c[1][:80])
            words.append(c[1])
        elif t in ("Link", "Image"):
            attr_words(c[0])
            words.extend(c[2])
        elif t in ("Div", "Span", "Header", "Table"):
            attr = c[1] if t == "Header" else c[0]
            attr_words(attr)
            if t == "Header":
                facts["headers"] += 1
            if t == "Table":
                facts["tables"] += 1
            if t == "Div" and not (set(attr[1]) & DIV_CLASSES):
                facts["odd"].append(f"Div {attr[1]}")
            if t == "Span" and attr[1] != ["linebreak"]:
                facts["odd"].append(f"Span {attr[1]}")
        elif t == "Math":
            words.append(c[1])
            facts["odd"].append("Math")
        elif t in ("Superscript", "Subscript", "Cite", "SmallCaps"):
            facts["odd"].append(t)
        elif t == "OrderedList":
            style, delim = c[0][1]["t"], c[0][2]["t"]
            if style not in ("Decimal", "DefaultStyle") or delim == "TwoParens":
                facts["odd"].append(f"OrderedList {style}/{delim}")

    ast_walk(ast["blocks"], visit)
    facts["words"] = Counter(w.lower() for s in words for w in WORD.findall(s))
    return facts


def check_page(path: str, text: str, url: str) -> dict:
    page, conv = _normalize(text, url)
    r = subprocess.run(["pandoc", "--preserve-tabs", "-f", PANDOC_READER, "-t", "json"],
                       input=page.markdown, capture_output=True, text=True)
    if r.returncode:
        return {"path": path, "error": r.stderr.strip(), "warnings": page.warnings}
    facts = ast_facts(json.loads(r.stdout))
    prose: list[str] = []
    body = re.sub(r"\A---[ \t]*\n.*?\n---[ \t]*\n", "", text, flags=re.S)
    fences = raw_fences(BOILERPLATE.sub("", body), prose)
    headings, tables = raw_structure(prose)
    pres = len(re.findall(r"<pre[\s>]", mask_code(text)))
    expected = len(fences) + pres
    lost = Counter(fences) - Counter(facts["code"])
    dropped = Counter(w.lower() for s in conv.dropped for w in WORD.findall(s))
    missing = raw_words(text) - facts["words"] - dropped
    fm = re.match(r"\A---[ \t]*\n(.*?\n)?---[ \t]*(\n|\Z)", text, re.S)
    if fm:
        have = Counter(w.lower() for k, v in page.meta.items() for w in WORD.findall(f"{k} {v}"))
        for w, n in (Counter(w.lower() for w in WORD.findall(fm.group(1) or "")) - have).items():
            missing[f"meta:{w}"] = n
    structure = []
    want, got = raw_components(prose), ast_components(json.loads(r.stdout)["blocks"])
    if want != got:
        k = next((n for n, (a, b) in enumerate(zip(want, got)) if a != b), min(len(want), len(got)))
        structure.append(f"components raw {len(want)} / ast {len(got)}, first difference at #{k}: "
                         f"{want[k:k + 2]} vs {got[k:k + 2]}")
    if headings != facts["headers"]:
        structure.append(f"headings raw {headings} / ast {facts['headers']}")
    if tables != facts["tables"]:
        structure.append(f"tables raw {tables} / ast {facts['tables']}")
    return {
        "path": path,
        "raw": facts["raw"],
        "code": (expected, len(facts["code"])),
        "changed": [c[:60] for c in lost.elements()],
        "missing": dict(missing.most_common(8)),
        "odd": facts["odd"],
        "structure": structure,
        "warnings": page.warnings,
    }


def run_check(source_ids: list[str]) -> int:
    from .config import load_sources

    sources = load_sources()
    if source_ids:
        known = {s.id for s in sources}
        bad = [s for s in source_ids if s not in known]
        if bad:
            sys.exit(f"unknown source(s): {', '.join(bad)}")
        sources = [s for s in sources if s.id in source_ids]
    problems = 0
    for source in sources:
        manifest = json.loads((source.mirror / "manifest.json").read_text())
        jobs = []
        for p in manifest["pages"]:
            f = source.pages_dir / p["path"]
            url = p["url"][:-3] if p["url"].endswith(".md") else p["url"]
            jobs.append((p["path"], f.read_text(encoding="utf-8"), url))
        with ProcessPoolExecutor(os.cpu_count() or 4) as pool:
            results = list(pool.map(check_page, *zip(*jobs), chunksize=4))
        problems += report(source.id, results)
    return 1 if problems else 0


def report(source: str, results: list[dict]) -> int:
    errors = [r for r in results if "error" in r]
    raw = [r for r in results if r.get("raw")]
    code = [r for r in results if "code" in r and r["code"][0] != r["code"][1]]
    changed = [r for r in results if r.get("changed")]
    missing = [r for r in results if r.get("missing")]
    odd = [r for r in results if r.get("odd")]
    structure = [r for r in results if r.get("structure")]
    print(f"== {source}: {len(results)} pages")
    print(f"  pandoc errors: {len(errors)}")
    for r in errors:
        print(f"    {r['path']}: {r['error'][:200]}")
    print(f"  pages with raw HTML: {len(raw)}")
    for r in raw:
        print(f"    {r['path']}: {r['raw'][:3]}")
    print(f"  code block count mismatches: {len(code)}")
    for r in code:
        print(f"    {r['path']}: raw {r['code'][0]} / ast {r['code'][1]}")
    print(f"  pages with code content not byte-exact: {len(changed)}")
    for r in changed:
        print(f"    {r['path']}: {len(r['changed'])} blocks, e.g. {r['changed'][0]!r}")
    print(f"  pages with missing words: {len(missing)}")
    for r in missing:
        print(f"    {r['path']}: {r['missing']}")
    print(f"  heading/table count mismatches: {len(structure)}")
    for r in structure:
        print(f"    {r['path']}: {', '.join(r['structure'])}")
    print(f"  pages with unexpected constructs: {len(odd)}")
    for r in odd:
        print(f"    {r['path']}: {Counter(r['odd']).most_common(4)}")
    kinds: dict[str, Counter] = defaultdict(Counter)
    pages: dict[str, set] = defaultdict(set)
    for r in results:
        for w in r.get("warnings", []):
            kind, _, detail = w.partition(": ")
            kinds[kind][detail] += 1
            pages[kind].add(r["path"])
    total = sum(sum(c.values()) for c in kinds.values())
    print(f"  warnings: {total}")
    for kind, c in sorted(kinds.items(), key=lambda kv: -sum(kv[1].values())):
        ex = sorted(pages[kind])[:3]
        print(f"    {kind}: {sum(c.values())} on {len(pages[kind])} pages, e.g. {', '.join(ex)}")
        for detail, n in c.most_common(5):
            print(f"      {n}x {detail}")
    return len(errors) + len(raw) + len(code) + len(changed) + len(missing) + len(structure) + len(odd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m claude_info.normalize")
    parser.add_argument("--check", action="store_true", help="normalize and verify every mirrored page")
    parser.add_argument("sources", nargs="*", help="source ids (default: all)")
    parser.add_argument("--show", metavar="PATH", help="print the normalized Markdown of one mirrored page")
    args = parser.parse_args(argv)
    if args.show:
        from .config import MIRROR

        f = MIRROR / args.show
        source = args.show.split("/", 1)[0]
        manifest = json.loads((MIRROR / source / "manifest.json").read_text())
        rel = str(f.relative_to(MIRROR / source / "pages"))
        url = next(p["url"] for p in manifest["pages"] if p["path"] == rel)
        page = normalize(f.read_text(encoding="utf-8"), url.removesuffix(".md"))
        sys.stdout.write(page.markdown)
        for w in page.warnings:
            print(f"warning: {w}", file=sys.stderr)
        return 0
    if args.check:
        return run_check(args.sources)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
