"""Check built manuals against the mirror so nothing is silently lost.

For every page: the words of the raw Markdown (minus markup, component tag
syntax and URLs) must all appear in the page's Info node. Also checked: every
mirrored page has a node, every node is reachable from Top through menus, and
every mermaid diagram was drawn.
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

from .config import BUILD, load_sources

WORD = re.compile(r"[^\W_]+", re.UNICODE)
URL = re.compile(r"https?://[^\s)\]>\"'`]+")
# Component and HTML tag syntax, but not placeholders such as <your-key>.
TAG = re.compile(
    r"</?(?:[A-Z][A-Za-z0-9.]*|a|abbr|b|br|code|dd|del|details|div|dl|dt|em|"
    r"figcaption|figure|h[1-6]|hr|i|iframe|img|kbd|li|ol|p|pre|s|small|source|"
    r"span|strong|sub|summary|sup|table|tbody|td|tfoot|th|thead|tr|u|ul|video|audio)"
    r"(?:\s(?:\"[^\"]*\"|'[^']*'|\{[^{}]*\}|[^<>\"'{}])*)?/?>",
)
FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
BOILERPLATE = re.compile(r"\A(?:>.*\n)*?> Use this file to discover[^\n]*\n", re.M)
FENCE_INFO = re.compile(r"^([\s>]*(?:(?:[-*+]|\d+[.)])[ \t]+)*)(`{3,}|~{3,})[^\n]*$", re.M)
# Footnote labels: "[^ts-sdk-resume]" in text and at the start of the note.
FOOTNOTE_ID = re.compile(r"\[\^[^\]\s]+\]")
JSX_EXPR = re.compile(r"\{/\*.*?\*/\}|\{\s*[\"'`][^\"'`]*[\"'`]\s*\}", re.S)
LINK_TARGET = re.compile(r"\]\([^)\s]*(?:\s+\"[^\"]*\")?\)")
HEADING_ID = re.compile(r"\{#[^}\s]+\}")
# Reference-style links: the [id] in "[text][id]" and "[id]: url" lines.
REF_USE = re.compile(r"\]\[[^\]\n]+\]")
REF_DEF = re.compile(r"^ {0,3}\[[^\]\n]+\]:\s*\S+.*$", re.M)
ATTRS = re.compile(r"\b[a-zA-Z]+=(?:\"[^\"]*\"|'[^']*'|\{[^}]*\})")
# Diagram source is checked label-by-label by `diagrams --check`; its syntax
# keywords (participant, sequenceDiagram, ...) rightly vanish once drawn.
MERMAID = re.compile(r"^([ \t>]*)(`{3,}|~{3,})[ \t]*mermaid[^\n]*\n.*?^\1\2[ \t]*$", re.M | re.S)
# Self-anchor buttons the site renders next to schema fields.
PERMALINK = re.compile(r"\[Permalink\]\(#[^)]*\)")
ENTITY = re.compile(r"&(?:#\d+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);")
# Copy-button labels at the end of exported <pre> blocks (dropped on purpose).
COPY_BUTTON = re.compile(r"`?Copy</pre>")


# Component attributes whose values are shown to the reader (tab titles,
# captions, card titles, parameter names and types).
SHOWN_ATTR = re.compile(r"\b(title|caption|description|name|type|default|label|alt)=(?:\"([^\"]*)\"|'([^']*)')")


def shown_attributes(m: re.Match) -> str:
    tag = m.group(0)
    if not re.match(r"</?[A-Z]", tag) and not tag.startswith(("<img", "<summary")):
        return " "
    return " " + " ".join(v2 or v3 for _, v2, v3 in SHOWN_ATTR.findall(tag)) + " "


def source_words(raw: str) -> Counter:
    text = FRONTMATTER.sub("", raw)
    text = BOILERPLATE.sub("", text, count=1)
    text = MERMAID.sub(" ", text)
    text = PERMALINK.sub(" ", text)
    text = COPY_BUTTON.sub("</pre>", text)
    text = FENCE_INFO.sub(r"\1\2", text)  # fence info strings are labels, not content
    text = JSX_EXPR.sub(" ", text)
    text = TAG.sub(shown_attributes, text)
    text = FOOTNOTE_ID.sub(" ", text)
    text = REF_DEF.sub(" ", text)
    text = REF_USE.sub("] ", text)
    text = LINK_TARGET.sub("] ", text)
    text = HEADING_ID.sub(" ", text)
    text = URL.sub(" ", text)
    # Only complete entities: html.unescape would also turn Go's "&params"
    # into "¶ms".
    text = ENTITY.sub(lambda m: html.unescape(m.group(0)), text)
    return Counter(w.lower() for w in WORD.findall(text))


def count_diagrams(raw: str) -> int:
    """Mermaid fences at top level, not ones quoted inside another fence
    (docs that show how to write a diagram)."""
    count, fence = 0, None
    for line in raw.splitlines():
        m = re.match(r"^[ \t>]*(`{3,}|~{3,})[ \t]*([^\s`]*)", line)
        if fence is None:
            if m:
                fence = m.group(1)
                count += m.group(2).lower() == "mermaid"
        elif m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2):
            fence = None
    return count


ADDED_URL = re.compile(r"\(\s*https?://[^\s)]+\s*\)")
ONLINE = re.compile(r"^Online: <[^>]*>\s*$", re.M)


def added_text_removed(node: str) -> str:
    """A node's text without what the writer adds around the page: the
    "File: … Node: … Up: …" header, the "Online: <url>" line, and the
    "(https://…)" Info shows after a link's label. A lost word must not be
    "found" in any of these. URLs shown as the link text itself stay."""
    body = node.split("\n", 1)[1] if "\n" in node else ""
    return ADDED_URL.sub(" ", ONLINE.sub(" ", body))


def info_nodes(path: Path) -> dict[str, str]:
    nodes = {}
    for chunk in path.read_text(encoding="utf-8").split("\x1f\n")[1:]:
        m = re.match(r"File: [^,]+,  Node: ([^,\n]+)", chunk)
        if m:
            nodes[m.group(1)] = chunk
    return nodes


def reachable(nodes: dict[str, str]) -> set[str]:
    seen, todo = set(), ["Top"]
    while todo:
        n = todo.pop()
        if n in seen or n not in nodes:
            continue
        seen.add(n)
        menu = nodes[n].split("* Menu:", 1)
        if len(menu) > 1:
            todo += re.findall(r"^\* ([^:\n]+)::", menu[1], re.M)
    return seen


def verify(source_ids: list[str] | None = None, log=print, show: int = 5) -> bool:
    node_map = json.loads((BUILD / "nodes.json").read_text())
    ok = True
    report_lines = []
    for source in load_sources():
        if source_ids and source.id not in source_ids:
            continue
        manifest = json.loads((source.mirror / "manifest.json").read_text())
        manual_nodes = {m.name: info_nodes(BUILD / "info" / f"{m.name}.info") for m in source.manuals}
        manual_reach = {name: reachable(n) for name, n in manual_nodes.items()}
        missing_pages, lossy, unreachable = [], [], []
        total_missing = 0
        diagrams_expected = diagrams_found = 0
        for p in manifest["pages"]:
            key = f"{source.id}/pages/{p['path']}"
            raw = (source.pages_dir / p["path"]).read_text(encoding="utf-8")
            if key not in node_map:
                url = p["url"].removesuffix(".md")
                if url not in node_map["_urls"]:
                    missing_pages.append(p["path"])
                continue  # folded into a duplicate page
            manual, node = node_map[key]
            text = manual_nodes[manual].get(node)
            if text is None:
                missing_pages.append(p["path"])
                continue
            if node not in manual_reach[manual]:
                unreachable.append(node)
            diagrams_expected += count_diagrams(raw)
            diagrams_found += len(re.findall(r"^ *── Diagram[ :]", text, re.M))
            # URLs are stripped from the source, so strip them here too; a
            # lost word must not be "found" inside a link such as Online:.
            have = Counter(w.lower() for w in WORD.findall(added_text_removed(text)))
            want = source_words(raw)
            lost = {w: n - have[w] for w, n in want.items() if have[w] < n}
            if lost:
                count = sum(lost.values())
                total_missing += count
                lossy.append((count, p["path"], sorted(lost, key=lambda w: -lost[w])[:12]))
        lossy.sort(reverse=True)
        status = "OK" if not (missing_pages or unreachable or lossy) else "PROBLEMS"
        log(f"{source.id}: {len(manifest['pages'])} pages, {len(missing_pages)} without a node, "
            f"{len(unreachable)} unreachable, {len(lossy)} with missing words ({total_missing} words), "
            f"diagrams {diagrams_found}/{diagrams_expected} drawn: {status}")
        for path in missing_pages[:show]:
            log(f"  no node: {path}")
        for node in unreachable[:show]:
            log(f"  unreachable: {node}")
        for count, path, words in lossy[:show]:
            log(f"  {count:>4} missing in {path}: {' '.join(words)}")
        for count, path, words in lossy:
            report_lines.append(f"{source.id}\t{count}\t{path}\t{' '.join(words)}")
        ok &= status == "OK" and diagrams_found >= diagrams_expected
    if not source_ids or "mcp" in source_ids:
        ok &= verify_schemas(node_map, log, report_lines, show)
    (BUILD / "verify-report.tsv").write_text("\n".join(report_lines) + "\n")
    return ok


def verify_schemas(node_map: dict, log, report_lines: list, show: int) -> bool:
    """Every word of each mirrored schema.ts must be in its generated page,
    and every declaration must have its own section."""
    from . import schemas

    problems = []
    files = sorted(schemas.DIR.glob("*/schema.ts")) if schemas.DIR.exists() else []
    nodes_cache: dict[str, dict] = {}
    for f in files:
        key = f"mcp-schema/{f.parent.name}/schema.ts"
        if key not in node_map:
            problems.append(f"no node: {key}")
            continue
        manual, node = node_map[key]
        nodes = nodes_cache.setdefault(manual, info_nodes(BUILD / "info" / f"{manual}.info"))
        text = nodes.get(node)
        if text is None:
            problems.append(f"no node: {key}")
            continue
        ts = f.read_text(encoding="utf-8")
        want = Counter(w.lower() for w in WORD.findall(URL.sub(" ", ts)))
        have = Counter(w.lower() for w in WORD.findall(added_text_removed(text)))
        lost = {w: n - have[w] for w, n in want.items() if have[w] < n}
        if lost:
            problems.append(f"{sum(lost.values())} missing in {key}: {' '.join(sorted(lost, key=lambda w: -lost[w])[:12])}")
            report_lines.append(f"mcp-schema\t{sum(lost.values())}\t{key}\t{' '.join(lost)}")
        _, decls = schemas.split(ts)
        missing = [n for n, _ in decls if not re.search(rf"^‘{re.escape(n)}’$", text, re.M)]
        if missing:
            problems.append(f"{key}: {len(missing)} declarations without a section: {' '.join(missing[:8])}")
    log(f"mcp-schema: {len(files)} schema.ts files, {len(problems)} problems: {'OK' if not problems else 'PROBLEMS'}")
    for p in problems[:show]:
        log(f"  {p}")
    return not problems
