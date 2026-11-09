"""The MCP schema as its canonical TypeScript source, one page per version.

The site's schema pages are TypeDoc HTML flattened by its Markdown export, so
the interfaces run together with their prose. The spec repository publishes
the real `schema.ts` for every version; it is mirrored here and turned into a
page per version with one section (heading, index entry, anchor) per
declaration, placed next to that version's other specification pages.

Layout (committed to git like the rest of the mirror):

    mirror/mcp-schema/<version>/schema.ts
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass

from . import http
from .config import MIRROR, STATE
from .fetch import atomic_write, load_json

SOURCE = "mcp"  # the source whose manual gets the schema pages
DIR = MIRROR / "mcp-schema"
RAW = "https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/{version}/schema.ts"
BLOB = "https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/{version}/schema.ts"
TITLE = "TypeScript schema"
DECL = re.compile(
    r"^export\s+(?:declare\s+)?(?:abstract\s+)?(interface|type|const|enum|class|function|namespace)\s+([A-Za-z_$][\w$]*)",
    re.M,
)


def versions() -> list[str]:
    """Specification versions present in the MCP mirror (e.g. 2025-06-18, draft)."""
    spec = MIRROR / SOURCE / "pages" / "specification"
    if not spec.exists():
        return []
    return sorted(d.name for d in spec.iterdir() if d.is_dir() and any(d.rglob("*.md")))


@dataclass
class SchemaReport:
    fetched: list[str]
    changed: list[str]
    removed: list[str]
    errors: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def sync(log=print) -> SchemaReport:
    """Fetch schema.ts for every mirrored spec version. A failed fetch keeps
    the last good copy; a version no longer mirrored is removed."""
    report = SchemaReport([], [], [], [])
    validators = load_json(STATE / "mcp-schema.validators.json", {})
    wanted = versions()
    for version in wanted:
        dest = DIR / version / "schema.ts"
        v = validators.get(version, {}) if dest.exists() else {}
        try:
            r = http.get(RAW.format(version=version), etag=v.get("etag"), last_modified=v.get("last_modified"))
        except Exception as e:
            report.errors.append(f"{version}: {e}" + ("; keeping last copy" if dest.exists() else ""))
            continue
        if r.status == 304:
            continue
        try:
            text = r.body.decode("utf-8")
        except UnicodeDecodeError as e:
            report.errors.append(f"{version}: not UTF-8 ({e})")
            continue
        if not DECL.search(text):
            report.errors.append(f"{version}: no TypeScript declarations in response; keeping last copy")
            continue
        validators[version] = {"etag": r.etag, "last_modified": r.last_modified}
        data = text.encode()
        if dest.exists() and dest.read_bytes() == data:
            continue
        (report.changed if dest.exists() else report.fetched).append(version)
        atomic_write(dest, data)
    for d in sorted(DIR.iterdir()) if DIR.exists() else []:
        if d.is_dir() and d.name not in wanted:
            for f in d.iterdir():
                f.unlink()
            d.rmdir()
            report.removed.append(d.name)
    STATE.mkdir(parents=True, exist_ok=True)
    atomic_write(STATE / "mcp-schema.validators.json", json.dumps(validators, indent=1, sort_keys=True).encode())
    log(f"mcp-schema: {len(wanted)} versions, +{len(report.fetched)} ~{len(report.changed)} "
        f"-{len(report.removed)}, {len(report.errors)} errors")
    for e in report.errors:
        log(f"  error: {e}")
    return report


# --- splitting the TypeScript source ---------------------------------------------

def split(ts: str) -> tuple[str, list[tuple[str, str]]]:
    """Split schema.ts into (preamble, [(name, code), ...]): each top-level
    declaration together with the comments directly above it. Every line ends
    up somewhere: comment blocks that belong to no declaration go to the
    preamble (before the first one) or to the following declaration. Braces
    inside comments and strings (JSDoc has {@link X}) don't count."""
    items: list[tuple[bool, list[str]]] = [(False, [])]
    depth, state, prev_blank = 0, "code", True
    for line in ts.splitlines():
        at_top = depth == 0 and state == "code"
        starts = at_top and re.match(r"(/\*|//|export\s)", line)
        has_decl, current = items[-1]
        if starts and current and (has_decl or prev_blank):
            items.append((False, []))
        if at_top and DECL.match(line):
            items[-1] = (True, items[-1][1])
        items[-1][1].append(line)
        depth, state = scan(line, depth, state)
        prev_blank = not line.strip()

    preamble: list[str] = []
    decls: list[tuple[str, str]] = []
    pending: list[str] = []
    for has_decl, lines in items:
        if not has_decl:
            (pending if decls or preamble_done(items, lines) else preamble).extend(lines)
            continue
        code = "\n".join(pending + lines).strip("\n")
        pending = []
        decls.append((DECL.search(code).group(2), code))
    if pending:
        if decls:
            name, code = decls[-1]
            decls[-1] = (name, code + "\n" + "\n".join(pending).rstrip("\n"))
        else:
            preamble += pending
    return "\n".join(preamble).strip("\n"), decls


def preamble_done(items, lines) -> bool:
    """A comment-only chunk directly before the first declaration (no blank
    line between) is that declaration's doc comment, not preamble."""
    idx = next(i for i, (_, l) in enumerate(items) if l is lines)
    nxt = items[idx + 1] if idx + 1 < len(items) else None
    return bool(nxt and nxt[0] and lines and lines[-1].strip())


def scan(line: str, depth: int, state: str) -> tuple[int, str]:
    """Track bracket depth across one line, skipping comments and strings."""
    i, n = 0, len(line)
    quote = ""
    while i < n:
        ch, nxt = line[i], line[i + 1 : i + 2]
        if state == "block":
            if ch == "*" and nxt == "/":
                state, i = "code", i + 2
                continue
            i += 1
            continue
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = ""
            i += 1
            continue
        if ch == "/" and nxt == "/":
            break
        if ch == "/" and nxt == "*":
            state, i = "block", i + 2
            continue
        if ch in "\"'`":
            quote = ch
        elif ch in "{[(":
            depth += 1
        elif ch in "}])":
            depth = max(0, depth - 1)
        i += 1
    return depth, state


def page_markdown(version: str, ts: str) -> str:
    """The generated page for one version: an introduction, then one section
    per declaration in source order."""
    preamble, decls = split(ts)
    digest = hashlib.sha256(ts.encode()).hexdigest()[:12]
    out = [
        f"# {TITLE}",
        "",
        f"The Model Context Protocol schema for version {version}, as its canonical TypeScript "
        f"source: [schema.ts]({BLOB.format(version=version)}) in the specification repository "
        f"({len(decls)} declarations, sha256 {digest}). Each declaration has its own section and "
        "index entry; the comments are the normative descriptions.",
        "",
    ]
    if preamble.strip():
        out += ["## Preamble", "", fence(preamble), ""]
    for name, code in decls:
        out += [f"### `{name}`", "", fence(code), ""]
    return "\n".join(out)


def fence(code: str) -> str:
    ticks = "```"
    while ticks in code:
        ticks += "`"
    return f"{ticks}typescript\n{code}\n{ticks}"


def pages() -> list[tuple[str, str, str]]:
    """(version, mirror path of schema.ts, generated markdown) for every
    mirrored schema file."""
    out = []
    for version in versions():
        f = DIR / version / "schema.ts"
        if f.exists():
            out.append((version, f"mcp-schema/{version}/schema.ts", page_markdown(version, f.read_text(encoding="utf-8"))))
    return out
