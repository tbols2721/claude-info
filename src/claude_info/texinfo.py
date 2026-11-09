"""Render the Pandoc JSON AST of a normalized page as a Texinfo fragment.

The input vocabulary (fenced divs such as ``.callout``, ``.tabs``, ``.steps``)
is produced by :mod:`claude_info.normalize`. Mermaid code blocks are drawn as
text by :mod:`claude_info.diagrams`. Tables are laid out here as box-drawn text
so they stay readable at the Info fill column.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Callable

from .config import FILL_COLUMN

# Indentation makeinfo applies to @example and @quotation bodies.
EXAMPLE_INDENT = 5
BLOCK_WIDTH = FILL_COLUMN - EXAMPLE_INDENT
# Extra indentation Info adds per nesting level (list item, quotation,
# indented block, definition); tables and diagrams inside get narrower.
INDENT_STEP = 5
MIN_BLOCK_WIDTH = 30

TRACKING = re.compile(r"utm_[a-z]+(=|$)", re.I)


def display_url(url: str) -> str:
    """The URL without tracking parameters, for showing to the reader."""
    base, sep, query = url.partition("?")
    if not sep:
        return url
    query, hash_, frag = query.partition("#")
    query = "&".join(p for p in query.split("&") if p and not TRACKING.match(p))
    return base + ("?" + query if query else "") + (hash_ + frag)

CALLOUT_LABELS = {
    "note": "Note",
    "tip": "Tip",
    "info": "Info",
    "warning": "Warning",
    "caution": "Caution",
    "danger": "Danger",
    "important": "Important",
    "check": "Check",
    "success": "Success",
    "error": "Error",
}

# A grid table whose wrapped rows get taller than this becomes records.
MAX_ROW_LINES = 8
MAX_MEAN_ROW_LINES = 4

# Code-block languages that are not worth labelling.
UNLABELLED = {"", "text", "plain", "plaintext", "txt", "none"}


# --- escaping ---------------------------------------------------------------

def esc(s: str) -> str:
    """Escape Texinfo's three special characters (for @code and @example)."""
    return s.replace("@", "@@").replace("{", "@{").replace("}", "@}")


def esc_text(s: str) -> str:
    """Escape running text, also defeating Texinfo's typographic ligatures
    (-- and --- become dashes, `` and '' become quotes, ` becomes ')."""
    s = esc(s)
    s = s.replace("`", "@U{0060}")
    s = re.sub(r"-(?=-)", "-@asis{}", s)
    s = re.sub(r"'(?=')", "'@asis{}", s)
    return s.replace("\t", " ")


def esc_arg(s: str) -> str:
    """Escape an argument of a multi-argument command such as @ref or @uref."""
    return s.replace(",", "@comma{}")


_NAME_SUBS = [
    (re.compile(r"\s*:\s*"), " - "),  # menus and xrefs use ':' as a delimiter
    (re.compile(r","), ""),  # ',' separates @node and @ref arguments
    (re.compile(r"\."), "․"),  # ONE DOT LEADER looks like '.', is safe
    (re.compile(r"[@{}]"), ""),
    (re.compile(r"-{2,}"), "-"),
    (re.compile(r"`"), "'"),
    (re.compile(r"'{2,}"), "'"),
    (re.compile(r"\s+"), " "),
]


def node_name(title: str) -> str:
    """Turn a title into a legal, readable Info node name."""
    s = unicodedata.normalize("NFC", title).strip()
    for pattern, repl in _NAME_SUBS:
        s = pattern.sub(repl, s)
    s = s.strip(" -").lstrip("(")
    return s or "Untitled"


def index_entry(text: str) -> str:
    text = re.sub(r"\s*:\s*", " - ", text.strip())
    return esc_text(re.sub(r"\s+", " ", text))


# --- display width and wrapping ---------------------------------------------

def dwidth(s: str) -> int:
    """Display columns of s in a terminal."""
    w = 0
    for ch in s:
        if unicodedata.combining(ch) or ch in "​‍️":
            continue
        w += 2 if unicodedata.east_asian_width(ch) in "WF" else 1
    return w


def wrap(text: str, width: int) -> list[str]:
    """Word-wrap one paragraph to display width, hard-breaking long words."""
    width = max(width, 1)
    lines: list[str] = []
    line = ""
    for word in text.split():
        while dwidth(word) > width:
            room = width - dwidth(line) - (1 if line else 0)
            if room < 4 and line:
                lines.append(line)
                line, room = "", width
            head, word = _split_at_width(word, room)
            lines.append((line + " " + head).strip())
            line = ""
        if not line:
            line = word
        elif dwidth(line) + 1 + dwidth(word) <= width:
            line += " " + word
        else:
            lines.append(line)
            line = word
    if line or not lines:
        lines.append(line)
    return lines


BREAK_AFTER = set(":/._-,=&?")


def _split_at_width(word: str, width: int) -> tuple[str, str]:
    """Split a too-long word to fit width, preferably after punctuation so
    identifiers and URLs break at natural boundaries."""
    w, cut, best = 0, len(word), 0
    for i, ch in enumerate(word):
        w += dwidth(ch)
        if w > width:
            cut = i
            break
        if ch in BREAK_AFTER and i + 1 < len(word):
            best = i + 1
    else:
        return word, ""
    if best >= max(1, cut // 3):
        cut = best
    # Always make progress, even when one wide character exceeds the width.
    cut = max(cut, 1)
    return word[:cut], word[cut:]


def pad(s: str, width: int, align: str = "AlignDefault") -> str:
    gap = width - dwidth(s)
    if gap <= 0:
        return s
    if align == "AlignRight":
        return " " * gap + s
    if align == "AlignCenter":
        return " " * (gap // 2) + s + " " * (gap - gap // 2)
    return s + " " * gap


# --- link resolution ----------------------------------------------------------

@dataclass(frozen=True)
class Target:
    """Where a docs URL lives in the generated manuals."""

    manual: str
    node: str  # node or anchor name
    here: bool = False  # the page being written, without a known anchor


Resolver = Callable[[str, str], "Target | None"]  # (url, current page url)


# --- the writer ---------------------------------------------------------------

def glued(prev, link) -> bool:
    """A word running straight into a link that starts a new capitalised
    phrase: the export lost a space."""
    if not prev or prev["t"] != "Str" or not prev["c"][-1:].isalpha():
        return False
    first = next((i for i in link["c"][1] if i["t"] in ("Str", "Code")), None)
    text = first["c"] if first and first["t"] == "Str" else (first["c"][1] if first else "")
    return text[:1].isupper()


def attr_parts(attr) -> tuple[str, list[str], dict[str, str]]:
    ident, classes, kvs = attr
    return ident, classes, {k: v for k, v in kvs}


@dataclass
class PageWriter:
    """Renders one page. ``anchors`` maps the page's header identifiers to the
    anchor names chosen for them by the manual builder."""

    manual: str
    page_url: str
    page_title: str
    anchors: dict[str, str]
    resolve: Resolver
    diagram: Callable[[str, int], str]
    warnings: list[str] = field(default_factory=list)
    index_label: str = ""
    _heading_levels: dict[int, str] = field(default_factory=dict)
    _depth: int = 0
    _anchored: set = field(default_factory=set)

    def unplaced_anchors(self) -> list[str]:
        """Anchors this page owns that no element emitted (e.g. ids inside
        table cells). The builder puts them at the top of the node so links
        to them still land on the right page."""
        return [a for i, a in self.anchors.items() if i not in self._anchored]

    def width(self) -> int:
        """Room for a table or diagram at the current nesting depth."""
        return max(MIN_BLOCK_WIDTH, BLOCK_WIDTH - INDENT_STEP * self._depth)

    def nested(self, blocks: list) -> str:
        self._depth += 1
        try:
            return self.blocks(blocks)
        finally:
            self._depth -= 1

    # -- inlines --

    def inlines(self, inls: list) -> str:
        out, prev = [], None
        for el in inls:
            if el["t"] == "Link" and glued(prev, el):
                out.append(" ")  # "See[JSON-RPC Error](…)" in squashed exports
            out.append(self.inline(el))
            prev = el
        return "".join(out)

    def inline(self, el) -> str:
        t, c = el["t"], el.get("c")
        if t == "Str":
            return esc_text(c)
        if t in ("Space", "SoftBreak"):
            return " "
        if t == "LineBreak":
            return "@*\n"
        if t == "Emph" or t == "Underline":
            return "@emph{" + self.inlines(c) + "}"
        if t == "Strong":
            inner = self.inlines(c)
            # Info renders @strong as *text*, and "*Note" starts a cross-reference.
            if inner[:4].lower() == "note":
                inner = "\u200b" + inner
            return "@strong{" + inner + "}"
        if t == "Strikeout":
            return "~~" + self.inlines(c) + "~~"
        if t == "Superscript":
            return "^" + self.inlines(c)
        if t == "Subscript":
            return "_" + self.inlines(c)
        if t == "SmallCaps":
            return "@sc{" + self.inlines(c) + "}"
        if t == "Quoted":
            q = "‘’" if c[0]["t"] == "SingleQuote" else "“”"
            return q[0] + self.inlines(c[1]) + q[1]
        if t == "Cite":
            return self.inlines(c[1])
        if t == "Code":
            return "@code{" + esc(c[1]) + "}" if c[1] else ""
        if t == "Math":
            return esc_text(c[1])
        if t == "RawInline":
            return self.raw(c[0], c[1])
        if t == "Link":
            return self.link(c[1], c[2][0])
        if t == "Image":
            return self.image(c[1], c[2][0])
        if t == "Note":
            return "@footnote{" + self.blocks(c).strip() + "}"
        if t == "Span":
            if "linebreak" in c[0][1]:
                return "@*\n"
            return self.inlines(c[1])
        self.warnings.append(f"unknown inline {t}")
        return ""

    def raw(self, fmt: str, text: str) -> str:
        if fmt in ("html", "html5"):
            stripped = re.sub(r"<[^>]+>", "", text)
            if text.strip():
                self.warnings.append(f"raw html kept as text: {text[:60]!r}")
            return esc_text(stripped)
        if fmt == "texinfo":
            return text
        self.warnings.append(f"raw {fmt} dropped: {text[:60]!r}")
        return esc_text(text)

    def link(self, label_inls: list, url: str) -> str:
        """A link; spaces at the edges of the link text move outside it
        ("invalidating[ an incorrect selection](…)")."""
        space = ("Space", "SoftBreak", "LineBreak")
        lead = " " if label_inls and label_inls[0]["t"] in space else ""
        trail = " " if label_inls and label_inls[-1]["t"] in space else ""
        return lead + self._link(label_inls, url) + trail

    def _link(self, label_inls: list, url: str) -> str:
        label = self.inlines(label_inls).strip()
        plain = stringify(label_inls).strip()
        if url.startswith("mailto:"):
            addr = url[len("mailto:"):]
            same_text = not label or plain in (addr, url)
            return "@email{" + esc_arg(esc(addr)) + ("" if same_text else "," + esc_arg(label)) + "}"
        target = self.resolve(url, self.page_url)
        if target is not None and target.here:
            # A link to this very page with no known anchor: a cross-reference
            # would only lead back to the top of what you're reading. A bare
            # number is a footnote marker ("DRACO[21](#refs)"): keep it apart.
            if plain.strip().isdigit():
                return "^" + esc_text(plain.strip())
            return label or esc_text(plain)
        if target is not None:
            # ':' ends the label in "*note label: Node." so use a look-alike.
            label = (label or esc_text(target.node)).replace(":", "\u2236")
            manual = "" if target.manual == self.manual else target.manual
            args = [esc_arg(target.node), "", esc_arg(label)]
            if manual:
                args.append(manual)
            return "@ref{" + ",".join(args) + "}"
        if url.startswith("#"):
            # A fragment the builder could not place: keep the words.
            return label
        shown = display_url(url)
        if not label or plain in (url, shown) or plain == shown.removeprefix("https://").removeprefix("http://"):
            return "@url{" + esc_arg(esc(shown)) + "}"
        return "@uref{" + esc_arg(esc(shown)) + "," + esc_arg(label) + "}"

    def image(self, alt_inls: list, url: str) -> str:
        alt = stringify(alt_inls).strip() or url.rsplit("/", 1)[-1]
        return "@uref{" + esc_arg(esc(url)) + "," + esc_arg(esc_text(f"[Image: {alt}]")) + "}"

    # -- blocks --

    def blocks(self, blocks: list) -> str:
        out = []
        for b in blocks:
            s = self.block(b)
            if s.strip():
                out.append(s.rstrip("\n") + "\n")
        return "\n".join(out)

    def block(self, el) -> str:
        t, c = el["t"], el.get("c")
        if t in ("Para", "Plain"):
            text = self.inlines(c).strip()
            return para(text)
        if t == "LineBlock":
            return para("@*\n".join(self.inlines(line) for line in c))
        if t == "CodeBlock":
            return self.code_block(c[0], c[1])
        if t == "RawBlock":
            return para(self.raw(c[0], c[1]))
        if t == "BlockQuote":
            return "@quotation\n" + self.nested(c) + "@end quotation\n"
        if t == "BulletList":
            return self.list_env("@itemize @bullet", "@end itemize", c)
        if t == "OrderedList":
            (start, style, _delim), items = c
            arg = str(start)
            if style["t"] == "LowerAlpha":
                arg = chr(ord("a") + start - 1)
            elif style["t"] == "UpperAlpha":
                arg = chr(ord("A") + start - 1)
            return self.list_env(f"@enumerate {arg}", "@end enumerate", items)
        if t == "DefinitionList":
            out = ["@table @asis"]
            for term, defs in c:
                out.append("@item " + oneline(self.inlines(term)))
                for d in defs:
                    out.append(self.nested(d))
            out.append("@end table")
            return "\n".join(out) + "\n"
        if t == "Header":
            return self.header(c[0], c[1], c[2])
        if t == "HorizontalRule":
            return "@center " + "─" * 20 + "\n"
        if t == "Table":
            return self.table(c)
        if t == "Figure":
            body = self.blocks(c[2])
            caption = self.blocks(c[1][1]).strip()
            if caption:
                body += "\n@noindent\n@emph{" + oneline(caption) + "}\n"
            return body
        if t == "Div":
            return self.div(c[0], c[1])
        if t == "Null":
            return ""
        self.warnings.append(f"unknown block {t}")
        return ""

    def list_env(self, start: str, end: str, items: list) -> str:
        """A list; items that hold more than one block are separated by blank
        lines so multi-paragraph items don't run together."""
        bodies = [self.nested(item).strip() for item in items]
        loose = any("\n\n" in b for b in bodies)
        out = [start]
        for body in bodies:
            out.append(("\n" if loose and len(out) > 1 else "") + ("@item\n" + body if body else "@item"))
        out.append(end)
        return "\n".join(out) + "\n"

    def header(self, level: int, attr, inls) -> str:
        ident, _, _ = attr_parts(attr)
        text = oneline(self.inlines(inls))
        cmd = self._heading_levels.get(level, "@subsubheading")
        out = []
        if ident in self.anchors and ident not in self._anchored:
            # Pandoc keeps explicit duplicate ids; a second @anchor would
            # make makeinfo fail the whole manual.
            self._anchored.add(ident)
            out.append("@anchor{" + self.anchors[ident] + "}")
        plain = stringify(inls).strip()
        if plain:
            out.append("@cindex " + index_entry(f"{plain} ({self.index_label or self.page_title})"))
        out.append(f"{cmd} {text}")
        return "\n".join(out) + "\n"

    def set_heading_levels(self, levels: list[int]) -> None:
        """Map the page's heading levels, shallowest first, to Texinfo
        heading commands (the page title itself is a @chapheading)."""
        cmds = ["@heading", "@subheading", "@subsubheading"]
        for i, level in enumerate(sorted(set(levels))):
            self._heading_levels[level] = cmds[min(i, len(cmds) - 1)]

    def anchor(self, ident: str) -> str:
        """@anchor line for an element id that links point at, once."""
        if ident and ident in self.anchors and ident not in self._anchored:
            self._anchored.add(ident)
            return "@anchor{" + self.anchors[ident] + "}\n"
        return ""

    def code_block(self, attr, code: str) -> str:
        return self.anchor(attr[0]) + self._code_block(attr, code)

    def _code_block(self, attr, code: str) -> str:
        _, classes, kv = attr_parts(attr)
        lang = classes[0] if classes else ""
        title = kv.get("title", "")
        if lang == "mermaid":
            art = self.diagram(code, self.width())
            return example(art, label="Diagram" + (f": {title}" if title else ""))
        label = title or ("" if lang.lower() in UNLABELLED else lang)
        return example(code.expandtabs(4).rstrip("\n"), label=label)

    # -- divs --

    def div(self, attr, blocks: list) -> str:
        return self.anchor(attr[0]) + self._div(attr, blocks)

    def _div(self, attr, blocks: list) -> str:
        _, classes, kv = attr_parts(attr)
        kind = classes[0] if classes else ""
        if kind == "callout":
            label = CALLOUT_LABELS.get(kv.get("kind", "note"), kv.get("kind", "note").title())
            body = self.nested(blocks)
            if kv.get("title"):
                body = para("@strong{" + esc_text(kv["title"]) + "}") + "\n" + body
            return f"@quotation {label}\n" + body + "@end quotation\n"
        if kind in ("tabs", "codegroup", "accordiongroup"):
            return self.blocks(blocks)
        if kind in ("tab", "accordion"):
            return self.labelled("▸ " + kv.get("title", "").strip(), blocks)
        if kind == "steps":
            out, n = [], 0
            for b in blocks:
                if b["t"] == "Div" and "step" in b["c"][0][1]:
                    n += 1
                    title = attr_parts(b["c"][0])[2].get("title", "").strip()
                    out.append(self.anchor(b["c"][0][0])
                               + self.labelled(f"Step {n}. {title}".strip().rstrip("."), b["c"][1]))
                else:
                    out.append(self.block(b))
            return "\n".join(o for o in out if o.strip())
        if kind == "step":
            return self.labelled(kv.get("title", "Step"), blocks)
        if kind == "cards":
            items = []
            for b in blocks:
                if b["t"] == "Div" and "card" in b["c"][0][1]:
                    items.append(self.anchor(b["c"][0][0]) + self.card(b["c"][0], b["c"][1]))
                else:
                    items.append(self.blocks([b]).strip())
            items = [i for i in items if i]
            if not items:
                return ""
            return "@itemize @bullet\n" + "\n".join("@item\n" + i for i in items) + "\n@end itemize\n"
        if kind == "card":
            return "@itemize @bullet\n@item\n" + self.card(attr, blocks) + "\n@end itemize\n"
        if kind == "field":
            return self.field(kv, blocks)
        if kind == "frame":
            body = self.blocks(blocks)
            if kv.get("caption"):
                body += "\n@noindent\n@emph{" + esc_text(kv["caption"]) + "}\n"
            return body
        if kind == "component":
            return self.labelled(kv.get("name", "Component"), blocks)
        return self.blocks(blocks)

    def labelled(self, label: str, blocks: list) -> str:
        head = "@noindent\n@strong{" + esc_text(label.strip()) + "}\n" if label.strip() else ""
        body = self.nested(blocks)
        if not body.strip():
            return head
        return head + "\n@indentedblock\n" + body + "@end indentedblock\n"

    def card(self, attr, blocks: list) -> str:
        _, _, kv = attr_parts(attr)
        title, href = kv.get("title", "").strip(), kv.get("href", "").strip()
        title_inls = [{"t": "Str", "c": title}] if title else []
        if href:
            head = self.link(title_inls, href)
        else:
            head = "@strong{" + esc_text(title) + "}" if title else ""
        body = self.blocks(blocks).strip()
        return "\n\n".join(p for p in (head, body) if p)

    def field(self, kv: dict, blocks: list) -> str:
        bits = [v for k in ("type", "location") if (v := kv.get(k))]
        if kv.get("required") == "true":
            bits.append("required")
        if kv.get("default"):
            bits.append("default: " + kv["default"])
        head = "@code{" + esc(kv.get("name", "")) + "}"
        if bits:
            head += " (" + esc_text(", ".join(bits)) + ")"
        body = self.nested(blocks)
        out = "@noindent\n" + head + "\n"
        if body.strip():
            out += "\n@indentedblock\n" + body + "@end indentedblock\n"
        return out

    # -- tables --

    def table(self, c) -> str:
        _attr, caption, colspecs, head, bodies, foot = c
        aligns = [spec[0]["t"] for spec in colspecs]
        refs: list[tuple[str, str]] = []
        cells = TableCells(self, refs)
        head_rows = [cells.row(r) for r in head[1]]
        body_rows = []
        for body in bodies:
            body_rows += [cells.row(r) for r in body[2]] + [cells.row(r) for r in body[3]]
        body_rows += [cells.row(r) for r in foot[1]]
        ncols = max([len(aligns)] + [len(r) for r in head_rows + body_rows])
        aligns += ["AlignDefault"] * (ncols - len(aligns))
        for r in head_rows + body_rows:
            r += [""] * (ncols - len(r))
        art = layout_table(head_rows, body_rows, aligns, self.width())
        out = example(art)
        cap = self.blocks(caption[1]).strip()
        if cap:
            out = "@noindent\n@emph{" + oneline(cap) + "}\n\n" + out
        if refs:
            lines = [f"[{n}] {text}" for n, (_, text) in enumerate(refs, 1)]
            out += "\n@noindent\n" + "@*\n".join(lines) + "\n"
        return out


class TableCells:
    """Flattens table cells to plain text, collecting links as numbered refs."""

    def __init__(self, writer: PageWriter, refs: list):
        self.w = writer
        self.refs = refs

    def row(self, row) -> list[str]:
        out = []
        for cell in row[1]:
            _attr, _align, _rowspan, colspan, blocks = cell
            out.append(self.blocks(blocks))
            out += [""] * (colspan - 1)
        return out

    def blocks(self, blocks: list) -> str:
        parts = []
        for b in blocks:
            t, c = b["t"], b.get("c")
            if t in ("Para", "Plain"):
                parts.append(self.inlines(c))
            elif t == "BulletList":
                parts += ["• " + self.blocks(item) for item in c]
            elif t == "OrderedList":
                parts += [f"{i}. " + self.blocks(item) for i, item in enumerate(c[1], c[0][0])]
            elif t == "CodeBlock":
                parts.append(c[1])
            elif t == "LineBlock":
                parts.append("\n".join(self.inlines(line) for line in c))
            elif t in ("Div", "BlockQuote"):
                parts.append(self.blocks(c[1] if t == "Div" else c))
            elif t == "Header":
                parts.append(self.inlines(c[2]))
            else:
                parts.append(stringify_blocks([b]))
        return "\n".join(p for p in parts if p.strip())

    def inlines(self, inls: list) -> str:
        out = []
        for el in inls:
            t, c = el["t"], el.get("c")
            if t == "Str":
                out.append(c)
            elif t in ("Space", "SoftBreak"):
                out.append(" ")
            elif t == "LineBreak":
                out.append("\n")
            elif t == "Code":
                out.append("‘" + c[1] + "’")
            elif t in ("Emph", "Strong", "Underline", "SmallCaps", "Strikeout",
                       "Superscript", "Subscript"):
                inner = self.inlines(c)
                out.append({"Superscript": "^", "Subscript": "_"}.get(t, "") + inner)
            elif t == "Quoted":
                out.append("“" + self.inlines(c[1]) + "”")
            elif t == "Span" and "linebreak" in c[0][1]:
                out.append("\n")
            elif t in ("Span", "Cite"):
                out.append(self.inlines(c[1]))
            elif t == "Link":
                text = self.inlines(c[1]).strip()
                url = c[2][0]
                target = self.w.resolve(url, self.w.page_url)
                footnote = text.isdigit()
                if (url.startswith("#") and target is None) or (target is not None and target.here):
                    out.append("^" + text if footnote else text)  # stays on this page
                    continue
                self.refs.append((url, self.w.link(c[1], url)))
                n = len(self.refs)
                # "Chartography[13](…)" must not read as "Chartography13[3]".
                out.append(f"^{text}[{n}]" if footnote else f"{text}[{n}]")
            elif t == "Image":
                alt = stringify(c[1]).strip() or c[2][0].rsplit("/", 1)[-1]
                self.refs.append((c[2][0], self.w.image(c[1], c[2][0])))
                out.append(f"[Image: {alt}][{len(self.refs)}]")
            elif t == "Math":
                out.append(c[1])
            elif t == "RawInline":
                out.append(re.sub(r"<[^>]+>", "", c[1]))
            elif t == "Note":
                out.append(" (" + stringify_blocks(c) + ")")
        return "".join(out)


def layout_table(head: list[list[str]], body: list[list[str]], aligns: list[str], width: int) -> str:
    """Draw a table with box characters, wrapping cells to fit ``width``.
    Tables too wide even when wrapped become one record per row."""
    ncols = len(aligns)
    rows = head + body
    if ncols == 0 or not rows:
        return ""
    natural = [max((max((dwidth(l) for l in r[i].split("\n")), default=0) for r in rows), default=0) for i in range(ncols)]
    natural = [max(n, 1) for n in natural]
    longest_word = [
        max((dwidth(w) for r in rows for w in r[i].split()), default=1) for i in range(ncols)
    ]
    frame = 3 * ncols + 1
    avail = width - frame
    if sum(natural) <= avail:
        widths = natural
    else:
        # Never break inside a word in a grid; records have room for long ones.
        minw = [min(natural[i], max(6, longest_word[i])) for i in range(ncols)]
        if sum(minw) > avail:
            return layout_records(head, body, width)
        widths = minw[:]
        spare = avail - sum(minw)
        want = [natural[i] - minw[i] for i in range(ncols)]
        total = sum(want)
        if total:
            for i in range(ncols):
                widths[i] += spare * want[i] // total
        # Hand out rounding leftovers to the columns that still want more.
        leftover = avail - sum(widths)
        for i in sorted(range(ncols), key=lambda i: want[i] - (widths[i] - minw[i]), reverse=True):
            if leftover <= 0:
                break
            if widths[i] < natural[i]:
                widths[i] += 1
                leftover -= 1

    def wrapped(row: list[str]) -> list[list[str]]:
        cols = []
        for i, text in enumerate(row):
            lines = []
            for para_ in text.split("\n"):
                lines += wrap(para_, widths[i]) if para_.strip() else [""]
            cols.append(lines)
        return cols

    def render_row(row: list[str]) -> list[str]:
        cols = wrapped(row)
        height = max(len(c) for c in cols)
        out = []
        for k in range(height):
            cells = [pad(cols[i][k] if k < len(cols[i]) else "", widths[i], aligns[i]) for i in range(ncols)]
            out.append("│ " + " │ ".join(cells) + " │")
        return out

    def rule(left: str, mid: str, right: str, fill: str = "─") -> str:
        return left + mid.join(fill * (w + 2) for w in widths) + right

    body_wrapped = [render_row(r) for r in body]
    heights = [len(r) for r in body_wrapped]
    if heights and (max(heights) > MAX_ROW_LINES or sum(heights) / len(heights) > MAX_MEAN_ROW_LINES):
        # Columns this narrow read badly; one labelled block per row reads well.
        return layout_records(head, body, width)
    multiline = any(h > 1 for h in heights)
    lines = [rule("┌", "┬", "┐")]
    for r in head:
        lines += render_row(r)
    if head:
        lines.append(rule("├", "┼", "┤", "─"))
    for i, r in enumerate(body_wrapped):
        if i and multiline:
            lines.append(rule("├", "┼", "┤", "╌"))
        lines += r
    lines.append(rule("└", "┴", "┘"))
    return "\n".join(l.rstrip() for l in lines)


def layout_records(head: list[list[str]], body: list[list[str]], width: int) -> str:
    """One block per row: 'Header: value' lines with hanging indents."""
    names = head[-1] if head else [f"Column {i + 1}" for i in range(len(body[0]) if body else 0)]
    names = [n.replace("\n", " ").strip() or f"Column {i + 1}" for i, n in enumerate(names)]
    label_w = min(max(dwidth(n) for n in names) + 2, width // 3)
    sep = "─" * width
    out = [sep]
    for row in body:
        for name, value in zip(names, row):
            label = name + ":"
            first = True
            paras = value.split("\n") if value.strip() else [""]
            room = width - label_w - 1
            if max((dwidth(w) for w in value.split()), default=0) > room:
                # A long hash or URL: give the value whole lines below its label.
                out += wrap(label, width)
                for p in paras:
                    out += ["  " + l for l in (wrap(p, width - 2) if p.strip() else [""])]
                continue
            for p in paras:
                for line in wrap(p, room) if p.strip() else [""]:
                    if first:
                        if dwidth(label) > label_w:
                            out += wrap(label, width)
                            out.append(" " * (label_w + 1) + line)
                        else:
                            out.append(pad(label, label_w) + " " + line)
                        first = False
                    else:
                        out.append(" " * (label_w + 1) + line)
        out.append(sep)
    return "\n".join(l.rstrip() for l in out)


# --- helpers ----------------------------------------------------------------

def para(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    # A paragraph must not contain blank lines; Texinfo would split it.
    text = re.sub(r"\n\s*\n", "\n", text)
    return text + "\n"


def oneline(text: str) -> str:
    return re.sub(r"\s*(@\*)?\s*\n\s*", " ", text).strip()


def example(text: str, label: str = "") -> str:
    out = ["@example"]
    if label:
        rule = "── " + label + " "
        rule += "─" * max(3, min(BLOCK_WIDTH, 40) - dwidth(rule))
        out.append(esc(rule))
    out.append(esc(text.rstrip("\n")) if text.strip() else "")
    out.append("@end example")
    return "\n".join(out) + "\n"


def stringify(inls: list) -> str:
    out = []
    for el in inls:
        t, c = el["t"], el.get("c")
        if t == "Str":
            out.append(c)
        elif t in ("Space", "SoftBreak", "LineBreak"):
            out.append(" ")
        elif t in ("Code", "Math", "RawInline"):
            out.append(c[1])
        elif t in ("Emph", "Strong", "Underline", "SmallCaps", "Strikeout", "Superscript", "Subscript"):
            out.append(stringify(c))
        elif t in ("Quoted", "Cite", "Span", "Link", "Image"):
            out.append(stringify(c[1]))
        elif t == "Note":
            out.append(stringify_blocks(c))
    return "".join(out)


def stringify_blocks(blocks: list) -> str:
    out = []
    for b in blocks:
        t, c = b["t"], b.get("c")
        if t in ("Para", "Plain"):
            out.append(stringify(c))
        elif t == "Header":
            out.append(stringify(c[2]))
        elif t == "CodeBlock":
            out.append(c[1])
        elif t in ("BulletList",):
            out += [stringify_blocks(i) for i in c]
        elif t == "OrderedList":
            out += [stringify_blocks(i) for i in c[1]]
        elif t in ("BlockQuote",):
            out.append(stringify_blocks(c))
        elif t == "Div":
            out.append(stringify_blocks(c[1]))
        elif t == "LineBlock":
            out += [stringify(line) for line in c]
        elif t == "DefinitionList":
            for term, defs in c:
                out.append(stringify(term))
                out += [stringify_blocks(d) for d in defs]
        elif t == "Table":
            for body in c[4]:
                for row in body[3]:
                    out += [stringify_blocks(cell[4]) for cell in row[1]]
        elif t == "Figure":
            out.append(stringify_blocks(c[2]))
    return " ".join(o for o in out if o)


def header_ids(blocks: list) -> list[tuple[int, str, str]]:
    """All headers in document order as (level, identifier, plain text),
    including those nested inside divs."""
    found = []

    def walk(bs):
        for b in bs:
            t, c = b["t"], b.get("c")
            if t == "Header":
                found.append((c[0], c[1][0], stringify(c[2]).strip()))
            elif t == "Div":
                if c[0][0]:
                    found.append((0, c[0][0], attr_parts(c[0])[2].get("title", "")))
                walk(c[1])
            elif t == "CodeBlock" and c[0][0]:
                found.append((0, c[0][0], attr_parts(c[0])[2].get("title", "")))
            elif t == "BlockQuote":
                walk(c)
            elif t in ("BulletList",):
                for item in c:
                    walk(item)
            elif t == "OrderedList":
                for item in c[1]:
                    walk(item)

    walk(blocks)
    return found
