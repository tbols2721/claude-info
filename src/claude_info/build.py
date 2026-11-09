"""Assemble mirrored pages into Texinfo manuals and run makeinfo.

Pipeline per page: raw Markdown -> normalize -> pandoc JSON AST (cached) ->
PageWriter. Pages are arranged into a node tree that follows each site's
navigation; very flat sections are split by URL path so menus stay short.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from . import texinfo as tx
from .config import BUILD, FILL_COLUMN, MIRROR, PANDOC_READER, STATE, Manual, Source, load_sources

REDIRECTS = MIRROR / "redirects.json"

# Split a menu by URL directory when it lists more pages than this.
MAX_MENU_PAGES = 16
DIR_CATEGORY = "Claude and Anthropic"

ACRONYMS = {
    "claude": "Claude", "anthropic": "Anthropic", "aws": "AWS", "gcp": "GCP",
    "iam": "IAM", "ip": "IP", "ios": "iOS", "macos": "macOS", "github": "GitHub",
    "api": "API", "apis": "APIs", "sdk": "SDK", "sdks": "SDKs", "cli": "CLI",
    "mcp": "MCP", "ide": "IDE", "ides": "IDEs", "sso": "SSO", "oauth": "OAuth",
    "seps": "SEPs", "ui": "UI", "url": "URL", "json": "JSON", "http": "HTTP",
}


# --- pages -------------------------------------------------------------------

@dataclass
class PageDoc:
    source: Source
    manual: Manual
    path: str
    url: str  # canonical URL, no .md
    title: str
    description: str
    nav: list[str]
    order: int
    ast: dict | None = None
    warnings: list[str] = field(default_factory=list)
    node: str = ""
    anchors: dict[str, str] = field(default_factory=dict)
    # Generated pages (the MCP TypeScript schema) carry their own Markdown and
    # the mirror file they come from, instead of a file under pages/.
    markdown: str | None = None
    mirror_path: str = ""
    see_also: "PageDoc | None" = None

    @property
    def key(self) -> str:
        """Path relative to mirror/, as used in build/nodes.json and search."""
        return self.mirror_path or f"{self.source.id}/pages/{self.path}"


def canonical(url: str) -> str:
    parts = urlsplit(url)
    host = parts.netloc.lower().removeprefix("www.")
    path = re.sub(r"/+$", "", parts.path)
    path = path.removesuffix(".md")
    return f"https://{host}{path}"


def pandoc_version() -> str:
    out = subprocess.run(["pandoc", "--version"], capture_output=True, text=True, check=True)
    return out.stdout.splitlines()[0]


def to_ast(markdown: str, cache: Path, version: str) -> dict:
    key = hashlib.sha256(f"{version}\n{PANDOC_READER}\npreserve-tabs\n{markdown}".encode()).hexdigest()
    hit = cache / key[:2] / f"{key}.json"
    if hit.exists():
        return json.loads(hit.read_text())
    out = subprocess.run(
        # --preserve-tabs keeps code byte-exact (Go examples are tab-indented).
        ["pandoc", "--preserve-tabs", "-f", PANDOC_READER, "-t", "json"],
        input=markdown, capture_output=True, text=True, check=True,
    )
    hit.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=hit.parent, suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        f.write(out.stdout)
    os.replace(tmp, hit)
    return json.loads(out.stdout)


def load_pages(sources: list[Source], log=print) -> list[PageDoc]:
    from .normalize import normalize

    version = pandoc_version()
    cache = BUILD / "cache" / "ast"
    docs: list[PageDoc] = []
    for source in sources:
        manifest = json.loads((source.mirror / "manifest.json").read_text())
        for p in manifest["pages"]:
            docs.append(
                PageDoc(
                    source=source,
                    manual=source.manual_for(p["path"]),
                    path=p["path"],
                    url=canonical(p["url"]),
                    title=p["title"],
                    description=p["description"],
                    nav=p["nav"],
                    order=p["order"],
                )
            )

    docs += schema_pages(sources, docs)

    def prepare(doc: PageDoc) -> None:
        if doc.markdown is not None:
            raw = doc.markdown
        else:
            raw = (doc.source.pages_dir / doc.path).read_text(encoding="utf-8")
        page = normalize(raw, doc.url)
        doc.warnings += page.warnings
        try:
            doc.ast = to_ast(page.markdown, cache, version)
        except subprocess.CalledProcessError as e:
            doc.warnings.append(f"pandoc failed: {e.stderr.strip()[:200]}")
            doc.ast = {"blocks": [{"t": "Para", "c": [{"t": "Str", "c": "(This page could not be converted; see the online version.)"}]}]}
        doc.title = choose_title(doc, page.meta)
        # Frontmatter descriptions are written as descriptions; index link
        # suffixes are sometimes just section names.
        doc.description = page.meta.get("description", "").strip() or doc.description

    with ThreadPoolExecutor(os.cpu_count() or 4) as pool:
        list(pool.map(prepare, docs))
    docs, aliases = drop_duplicates(docs)
    log(f"loaded {len(docs)} pages ({len(aliases)} sitemap-only duplicates folded in)")
    return docs, aliases


def schema_pages(sources: list[Source], docs: list[PageDoc]) -> list[PageDoc]:
    """One generated page per MCP version with the TypeScript schema, filed
    under that version's specification pages, right after its schema page if
    the site has one (that page then links to it)."""
    from . import schemas

    source = next((s for s in sources if s.id == schemas.SOURCE), None)
    if source is None:
        return []
    out = []
    for version, mirror_path, markdown in schemas.pages():
        path = f"specification/{version}/typescript-schema.md"
        siblings = [d for d in docs if d.source is source and d.path.startswith(f"specification/{version}/")]
        site_page = next((d for d in siblings if d.path == f"specification/{version}/schema.md"), None)
        anchor = site_page or max(siblings, key=lambda d: d.order, default=None)
        doc = PageDoc(
            source=source,
            manual=source.manual_for(path),
            path=path,
            url=canonical(schemas.BLOB.format(version=version)),
            title=schemas.TITLE,
            description=f"Canonical schema.ts for MCP {version}, one section per type.",
            nav=list(anchor.nav) if anchor else [],
            order=(anchor.order + 0.5) if anchor else 10**6,
            markdown=markdown,
            mirror_path=mirror_path,
        )
        if site_page is not None:
            site_page.see_also = doc
        out.append(doc)
    return out


def drop_duplicates(docs: list[PageDoc]) -> tuple[list[PageDoc], dict[str, PageDoc]]:
    """A sitemap-only page that is byte-identical to an indexed page (e.g.
    whats-new/index.md and whats-new.md) is the same page under a second URL."""
    ALIAS_PATHS.clear()
    by_hash: dict[tuple[str, str], PageDoc] = {}
    digests = {}
    for d in docs:
        data = d.markdown.encode() if d.markdown is not None else (d.source.pages_dir / d.path).read_bytes()
        digests[id(d)] = hashlib.sha256(data).hexdigest()
        if d.nav != ["Other pages"]:
            by_hash.setdefault((d.source.id, digests[id(d)]), d)
    kept, aliases = [], {}
    for d in docs:
        twin = by_hash.get((d.source.id, digests[id(d)]))
        if d.nav == ["Other pages"] and twin is not None:
            aliases[d.url] = twin
            ALIAS_PATHS[d.key] = twin
        else:
            kept.append(d)
    return kept, aliases


# Mirror paths of folded duplicates -> the page they duplicate (for nodes.json).
ALIAS_PATHS: dict[str, PageDoc] = {}


def choose_title(doc: PageDoc, meta: dict) -> str:
    """Prefer the page's own title over the (often terse) index link text."""
    if meta.get("title"):
        return meta["title"].strip()
    for b in doc.ast["blocks"][:3]:
        if b["t"] == "Header" and b["c"][0] == 1:
            return tx.stringify(b["c"][2]).strip()
    if doc.title:
        return doc.title
    return humanize(doc.path.removesuffix(".md").rsplit("/", 1)[-1])


def humanize(segment: str) -> str:
    """Directory name -> title: "tool-use" -> "Tool use", "2025-06-18" kept."""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}|v?\d+(\.\d+)*", segment):
        return segment
    words = re.split(r"[-_\s]+", segment.strip())
    words = [ACRONYMS.get(w.lower(), w) for w in words if w]
    if not words:
        return segment
    first = words[0]
    if first == first.lower():
        words[0] = first[:1].upper() + first[1:]
    return " ".join(words)


# --- tree --------------------------------------------------------------------

@dataclass
class Group:
    title: str
    children: list = field(default_factory=list)  # Group | PageDoc
    landing: PageDoc | None = None
    node: str = ""
    label: str = ""  # the nav heading or directory it came from


def adopt_nav(docs: list[PageDoc]) -> None:
    """Pages found only in the sitemap have no navigation; file each one with
    the indexed page that shares the longest URL directory with it."""
    indexed = [d for d in docs if d.nav != ["Other pages"]]
    for d in docs:
        if d.nav != ["Other pages"]:
            continue
        parts = d.path.removesuffix(".md").removesuffix("/index").split("/")
        best, best_len = None, 0
        for o in indexed:
            n = len(os.path.commonprefix([parts, o.path.removesuffix(".md").split("/")[:-1]]))
            if n > best_len:
                best, best_len = o, n
        if best is not None:
            d.nav = list(best.nav)
            d.order = best.order + 0.5


def build_tree(manual: Manual, docs: list[PageDoc]) -> Group:
    adopt_nav(docs)
    root = Group(manual.title)
    for doc in sorted(docs, key=lambda d: d.order):
        group = root
        for title in doc.nav:
            sub = next((c for c in group.children if isinstance(c, Group) and same(c.title, title)), None)
            if sub is None:
                sub = Group(title, label=title)
                group.children.append(sub)
            group = sub
        group.children.append(doc)
    split_flat(root, depth=0)
    collapse(root)
    if root.landing is not None:
        # The Top node has its own text; keep such a page as the first entry.
        root.children.insert(0, root.landing)
        root.landing = None
    return root


def split_flat(group: Group, depth: int) -> None:
    pages = [c for c in group.children if isinstance(c, PageDoc)]
    if len(pages) > MAX_MENU_PAGES and depth < 8:
        group.children = regroup_by_path(group.children)
    for c in group.children:
        if isinstance(c, Group):
            split_flat(c, depth + 1)


def regroup_by_path(children: list) -> list:
    """Group a flat run of pages by the first URL directory they don't share.
    Order is preserved: each new group sits where its first page was."""
    pages = [c for c in children if isinstance(c, PageDoc)]
    stems = {id(p): p.path.removesuffix(".md").split("/") for p in pages}
    level = len(os.path.commonprefix([stems[id(p)][:-1] for p in pages]))
    buckets: dict[str, list[PageDoc]] = {}
    for p in pages:
        parts = stems[id(p)]
        if len(parts) > level + 1:
            buckets.setdefault(parts[level], []).append(p)
    if not buckets:
        return children
    # A page named like a directory ("tool-use.md" beside "tool-use/...") or a
    # directory's index.md becomes that directory's landing page.
    landing: dict[str, PageDoc] = {}
    for p in pages:
        parts = stems[id(p)]
        if len(parts) == level + 1 and parts[level] in buckets:
            landing[parts[level]] = p
    for key, members in buckets.items():
        if key not in landing:
            idx = next((m for m in members if stems[id(m)][level + 1:] == ["index"]), None)
            if idx is not None:
                landing[key] = idx
                members.remove(idx)
    placed: dict[int, object] = {}
    for key, members in buckets.items():
        if len(members) == 1 and key not in landing:
            continue  # a lone page needs no group of its own
        g = Group(humanize(key), children=list(members), landing=landing.get(key), label=humanize(key))
        if g.landing is not None:
            g.title = g.landing.title
            placed[id(g.landing)] = g
        for m in members:
            placed[id(m)] = g
    out: list = []
    seen: set[int] = set()
    for c in children:
        item = placed.get(id(c), c)
        if id(item) not in seen:
            seen.add(id(item))
            out.append(item)
    return out


def collapse(group: Group) -> None:
    """Tidy the navigation tree, top-down:

    - a group whose only child is a group absorbs that child's children
      (llms.txt wraps each tab in a redundant first-section heading);
    - a child group titled like its parent is flattened into it;
    - a page titled like its group becomes the group's landing page.
    """
    while (
        group.landing is None
        and len(group.children) == 1
        and isinstance(group.children[0], Group)
    ):
        only = group.children[0]
        group.children, group.landing = only.children, only.landing
    flat: list = []
    for c in group.children:
        if isinstance(c, Group) and c.landing is None and same(c.title, group.title):
            flat.extend(c.children)
        else:
            flat.append(c)
    # A group holding a single page is just that page.
    group.children = [
        c.children[0]
        if isinstance(c, Group) and c.landing is None and len(c.children) == 1
        and isinstance(c.children[0], PageDoc)
        else c
        for c in flat
    ]
    if group.landing is None:
        match = next((c for c in group.children if isinstance(c, PageDoc) and same(c.title, group.title)), None)
        if match is not None:
            group.landing = match
            group.children.remove(match)
    for c in group.children:
        if isinstance(c, Group):
            collapse(c)


def same(a: str, b: str) -> bool:
    return tx.node_name(a).lower() == tx.node_name(b).lower()


def walk(group: Group):
    yield group
    for c in group.children:
        if isinstance(c, Group):
            yield from walk(c)


def tree_pages(group: Group):
    if group.landing is not None:
        yield group.landing
    for c in group.children:
        if isinstance(c, Group):
            yield from tree_pages(c)
        else:
            yield c


# --- naming --------------------------------------------------------------------

class Names:
    """Allocates unique node and anchor names within one manual."""

    RESERVED = {"top", "index", "about this manual"}

    def __init__(self):
        self.used: set[str] = set()

    def free(self, name: str) -> bool:
        return name.lower() not in self.used and name.lower() not in self.RESERVED

    def take(self, title: str, contexts: list[str] = ()) -> str:
        """The plain title if free; else the title qualified by the nearest
        context (own label, parent, grandparent, ...) that makes it unique."""
        base = tx.node_name(title)
        candidates = [base] + [
            tx.node_name(f"{title} ({c})") for c in contexts if c and not same(c, title)
        ]
        for name in candidates:
            if self.free(name):
                self.used.add(name.lower())
                return name
        n = 2
        while not self.free(f"{candidates[-1]} {n}"):
            n += 1
        name = f"{candidates[-1]} {n}"
        self.used.add(name.lower())
        return name


def assign_names(root: Group) -> None:
    """Name nodes breadth-first, so shallower nodes keep the plain titles and
    deeper namesakes are qualified ("Reference (Plugins)", "Architecture
    overview (2025-06-18)")."""
    names = Names()
    queue: list[tuple[Group, list[str]]] = [(root, [])]
    while queue:
        group, ancestors = queue.pop(0)
        here = ancestors if group is root else [group.label or group.title, *ancestors]
        for c in group.children:
            if isinstance(c, Group):
                title = c.landing.title if c.landing else c.title
                c.node = names.take(title, [c.label, *here])
                if c.landing is not None:
                    c.landing.node = c.node
                queue.append((c, here))
            else:
                c.node = names.take(c.title, here)
    for doc in tree_pages(root):
        title = title_header(doc)
        if title is not None and title["c"][1][0]:
            doc.anchors[title["c"][1][0]] = doc.node
        for level, ident, text in tx.header_ids(body_blocks(doc)):
            if ident and ident not in doc.anchors:
                doc.anchors[ident] = names.take(f"{doc.node} - {text or ident}")


# --- links -----------------------------------------------------------------------

class LinkMap:
    """Maps docs URLs (current and legacy forms) to manual nodes."""

    def __init__(self, docs: list[PageDoc], aliases: dict[str, PageDoc]):
        self.pages: dict[str, PageDoc] = dict(aliases)
        for d in docs:
            self.pages[d.url] = d
            if d.url.endswith("/index"):
                self.pages.setdefault(d.url.removesuffix("/index"), d)
        # Where moved URLs end up, as recorded by sync (mirror/redirects.json).
        try:
            recorded = json.loads(REDIRECTS.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            recorded = {}
        self.redirects = {canonical(k): canonical(v) for k, v in recorded.items() if v}
        self.unresolved: dict[str, int] = {}
        self.fragment_misses: dict[tuple[str, str], int] = {}

    def aliases(self, url: str) -> list[str]:
        out = [url]
        p = urlsplit(url)
        host, path = p.netloc, p.path
        if host in ("docs.anthropic.com", "docs.claude.com"):
            m = re.match(r"^/(?:en/)?(docs/)?(.*)$", path)
            rest = m.group(2) if m else path.lstrip("/")
            if rest.startswith("claude-code/"):
                out.append("https://code.claude.com/docs/en/" + rest.removeprefix("claude-code/"))
            out.append("https://platform.claude.com/docs/en/" + rest)
            if rest.startswith("en/"):
                out.append("https://platform.claude.com/docs/" + rest)
        elif host == "platform.claude.com" and path.startswith("/docs/") and not path.startswith("/docs/en/"):
            out.append("https://platform.claude.com/docs/en/" + path.removeprefix("/docs/"))
        elif host == "code.claude.com" and path.startswith("/docs/") and not path.startswith("/docs/en/"):
            out.append("https://code.claude.com/docs/en/" + path.removeprefix("/docs/"))
        elif host == "anthropic.com" and path.startswith("/docs"):
            out.append("https://platform.claude.com/docs/en" + path.removeprefix("/docs"))
        return out

    def resolve(self, url: str, page_url: str) -> tx.Target | None:
        if url.startswith("#"):
            url = page_url + url
        if not url.startswith(("http://", "https://")):
            return None
        base, _, frag = url.partition("#")
        doc = self.find(canonical(base))
        if doc is None or not doc.node:
            host = urlsplit(base).netloc.removeprefix("www.")
            if host in DOC_HOSTS:
                self.unresolved[canonical(base)] = self.unresolved.get(canonical(base), 0) + 1
            return None
        here = doc.url == canonical(page_url.partition("#")[0])
        if frag:
            anchor = doc.anchors.get(frag) or fuzzy_anchor(frag, doc.anchors)
            if anchor:
                return tx.Target(doc.manual.name, anchor)
            key = (doc.url, frag)
            self.fragment_misses[key] = self.fragment_misses.get(key, 0) + 1
        return tx.Target(doc.manual.name, doc.node, here=here)

    def find(self, url: str) -> PageDoc | None:
        """The page for a URL: directly, through a legacy-URL rewrite, or
        through a redirect recorded at sync time."""
        for candidate in self.aliases(url):
            if (doc := self.pages.get(candidate)) is not None:
                return doc
        for candidate in self.aliases(url):
            if (final := self.redirects.get(candidate)) is not None:
                for again in self.aliases(final):
                    if (doc := self.pages.get(again)) is not None:
                        return doc
        return None


def fuzzy_anchor(frag: str, anchors: dict[str, str]) -> str | None:
    """Match a stale fragment to a renamed heading, e.g.
    #eliminate-prompts-with-auto-mode -> "Eliminate permission prompts with
    auto mode". Only a clear best match (most words in common) is accepted."""
    want = set(re.split(r"[-_]+", frag.lower())) - {""}
    if len(want) < 2:
        return None
    scored = []
    for ident, anchor in anchors.items():
        have = set(re.split(r"[-_]+", ident.lower())) - {""}
        if have:
            scored.append((len(want & have) / len(want | have), anchor))
    scored.sort(reverse=True)
    if scored and scored[0][0] >= 0.6 and (len(scored) == 1 or scored[1][0] < scored[0][0]):
        return scored[0][1]
    return None


DOC_HOSTS = {
    "code.claude.com", "platform.claude.com", "docs.anthropic.com",
    "docs.claude.com", "modelcontextprotocol.io", "agentskills.io",
}


# --- diagrams --------------------------------------------------------------------

def draw_diagram(source: str, width: int) -> str:
    try:
        from .diagrams import render
    except ImportError:
        return "Mermaid diagram (renderer unavailable):\n\n" + source.rstrip()
    return render(source, max_width=width).text


# --- writing ---------------------------------------------------------------------

def menu_entry(node: str, description: str) -> str:
    entry = f"* {node}::"
    desc = re.sub(r"\s+", " ", description or "").strip()
    if not desc:
        return entry
    col = max(len(entry) + 2, 32)
    room = FILL_COLUMN - col
    if room < 20:
        return entry
    if tx.dwidth(desc) > room:
        cut = desc[: room - 1]
        cut = cut.rsplit(" ", 1)[0] if " " in cut else cut
        desc = cut.rstrip(" ,;:.") + "…"
    return entry.ljust(col) + tx.esc_text(desc)


def menu(group: Group) -> str:
    lines = ["@menu"]
    for c in group.children:
        if isinstance(c, Group):
            desc = c.landing.description if c.landing else ""
            lines.append(menu_entry(c.node, desc))
        else:
            lines.append(menu_entry(c.node, c.description))
    lines.append("@end menu")
    return "\n".join(lines) + "\n"


def title_header(doc: PageDoc) -> dict | None:
    """The leading H1 that repeats the page title, if any. The node heading
    already prints the title, so this header is dropped and links to it go to
    the node."""
    blocks = doc.ast["blocks"]
    if blocks and blocks[0]["t"] == "Header" and blocks[0]["c"][0] == 1:
        if tx.node_name(tx.stringify(blocks[0]["c"][2])).lower() == tx.node_name(doc.title).lower():
            return blocks[0]
    return None


def body_blocks(doc: PageDoc) -> list:
    blocks = doc.ast["blocks"]
    return blocks[1:] if title_header(doc) is not None else list(blocks)


def page_body(doc: PageDoc, links: LinkMap) -> tuple[str, list[str]]:
    blocks = body_blocks(doc)
    writer = tx.PageWriter(
        manual=doc.manual.name,
        page_url=doc.url,
        page_title=doc.title,
        anchors=doc.anchors,
        resolve=links.resolve,
        diagram=draw_diagram,
        # The node name, not the title: it tells namesakes apart
        # ("TypeScript schema (2025-06-18)").
        index_label=doc.node or doc.title,
    )
    writer.set_heading_levels([lvl for lvl, _, _ in tx.header_ids(blocks) if lvl])
    out = []
    lead_text = tx.stringify_blocks(blocks[:3])
    if doc.description and norm_ws(doc.description)[:60] not in norm_ws(lead_text):
        out.append(tx.para(tx.esc_text(doc.description)))
    if doc.see_also is not None and doc.see_also.node:
        out.append("@quotation Note\nThis page is the site's rendering of the schema. The "
                   "canonical TypeScript source, one section per type, is in @ref{"
                   + tx.esc_arg(doc.see_also.node) + "}.\n@end quotation\n")
    out.append(writer.blocks(blocks))
    out.append("@noindent\nOnline: @url{" + tx.esc_arg(tx.esc(doc.url)) + "}\n")
    loose = [a for a in writer.unplaced_anchors() if a != doc.node]
    if loose:
        out.insert(0, "".join("@anchor{" + a + "}\n" for a in loose))
    return "\n".join(o for o in out if o.strip()), writer.warnings


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def write_manual(manual: Manual, root: Group, links: LinkMap, sources: list[Source], stamp: str) -> tuple[str, list[str]]:
    warnings: list[str] = []
    pages = list(tree_pages(root))
    src = next(s for s in sources if manual in s.manuals)
    out = [
        "\\input texinfo",
        f"@setfilename {manual.name}.info",
        "@documentencoding UTF-8",
        "@documentlanguage en",
        f"@settitle {tx.esc_text(manual.title)}",
        "@frenchspacing on",
        "@paragraphindent 0",
        "@firstparagraphindent none",
        f"@dircategory {DIR_CATEGORY}",
        "@direntry",
        f"* {manual.title}: ({manual.name}).".ljust(32) + " " + tx.esc_text(manual.description),
        "@end direntry",
        "",
        "@node Top",
        f"@top {tx.esc_text(manual.title)}",
        "",
        tx.para(tx.esc_text(manual.description)),
        "@noindent",
        f"{len(pages)} pages from @url{{{tx.esc(src.base)}}}, mirrored {stamp}.",
        "",
        menu_top(root),
    ]

    def emit_group(g: Group):
        out.append(f"@node {g.node}")
        if g.landing is not None:
            out.append(f"@chapheading {tx.esc_text(g.landing.title)}")
            out.append("@cindex " + tx.index_entry(g.landing.title))
            body, w = page_body(g.landing, links)
            warnings.extend(f"{g.landing.path}: {x}" for x in w + g.landing.warnings)
            out.append(body)
        else:
            out.append(f"@chapheading {tx.esc_text(g.title)}")
            out.append("@cindex " + tx.index_entry(g.title))
        out.append("")
        out.append(menu(g))
        for c in g.children:
            if isinstance(c, Group):
                emit_group(c)
            else:
                emit_page(c)

    def emit_page(doc: PageDoc):
        out.append(f"@node {doc.node}")
        out.append(f"@chapheading {tx.esc_text(doc.title)}")
        out.append("@cindex " + tx.index_entry(doc.title))
        body, w = page_body(doc, links)
        warnings.extend(f"{doc.path}: {x}" for x in w + doc.warnings)
        out.append(body)
        out.append("")

    for c in root.children:
        if isinstance(c, Group):
            emit_group(c)
        else:
            emit_page(c)

    out += [
        "@node About this manual",
        "@chapheading About this manual",
        about_text(manual, src, len(pages), stamp),
        "@node Index",
        "@chapheading Index",
        "@printindex cp",
        "",
        "@bye",
        "",
    ]
    return "\n".join(out), warnings


def menu_top(root: Group) -> str:
    m = menu(root).splitlines()
    extra = [menu_entry("About this manual", "How this manual was made and how to read it."),
             menu_entry("Index", "Every page and section title.")]
    return "\n".join(m[:-1] + ["", *extra, m[-1]]) + "\n"


ABOUT = """This manual was generated by @command{claude-info} from the
Markdown that SOURCE publishes for every documentation page
(@url{INDEX}). It contains COUNT pages, mirrored STAMP.
Each page ends with a link to its online version.

Diagrams were redrawn as text. Tables are drawn with box characters; links
inside a table are listed underneath it, numbered as in the cells.

@heading Reading Info

@multitable @columnfractions .22 .78
@item @kbd{SPC} / @kbd{DEL} @tab Scroll forward / back, continuing into the next node
@item @kbd{n} / @kbd{p} / @kbd{u} @tab Next, previous, up node
@item @kbd{l} @tab Go back to the previous node visited
@item @kbd{m} @tab Choose a menu item (TAB completes)
@item @kbd{TAB} / @kbd{RET} @tab Move to the next link / follow it
@item @kbd{i} @tab Look up a topic in the index; @kbd{,} for the next match
@item @kbd{s} @tab Search the whole manual for a regular expression
@item @kbd{g} @tab Go to a node by name (TAB completes)
@item @kbd{d} @tab The directory of all manuals
@item @kbd{q} @tab Quit
@end multitable

@noindent
From the shell: @samp{info MANUAL}, @samp{info MANUAL "Node name"},
or @samp{info --apropos=WORD} to search every manual's index.
"""


def about_text(manual: Manual, src: Source, count: int, stamp: str) -> str:
    return (
        ABOUT.replace("SOURCE", tx.esc_text(src.name))
        .replace("INDEX", tx.esc(src.index or src.base))
        .replace("COUNT", str(count))
        .replace("STAMP", stamp)
        .replace("MANUAL", manual.name)
    )


def run_makeinfo(texi: Path, outdir: Path) -> tuple[int, str]:
    r = subprocess.run(
        ["makeinfo", "--enable-encoding", f"--fill-column={FILL_COLUMN}",
         "--no-split", "-o", str(outdir / (texi.stem + ".info")), str(texi)],
        capture_output=True, text=True,
    )
    return r.returncode, r.stderr


def build(source_ids: list[str] | None = None, log=print) -> dict[str, bool]:
    """Build the manuals of the given sources (default: all). Every source is
    loaded either way, so links into other manuals and build/nodes.json stay
    complete. Returns {manual: succeeded}."""
    sources = load_sources()
    selected = {s.id for s in sources if not source_ids or s.id in source_ids}
    docs, aliases = load_pages(sources, log=log)
    by_manual: dict[str, list[PageDoc]] = {}
    manuals: dict[str, Manual] = {}
    for d in docs:
        by_manual.setdefault(d.manual.name, []).append(d)
        manuals[d.manual.name] = d.manual
    trees = {name: build_tree(manuals[name], pages) for name, pages in by_manual.items()}
    for root in trees.values():
        assign_names(root)
    links = LinkMap(docs, aliases)

    outdir = BUILD / "info"
    texidir = BUILD / "texi"
    outdir.mkdir(parents=True, exist_ok=True)
    texidir.mkdir(parents=True, exist_ok=True)
    results: dict[str, bool] = {}
    for name, root in trees.items():
        source = next(s for s in sources if manuals[name] in s.manuals)
        if source.id not in selected:
            continue
        text, warnings = write_manual(manuals[name], root, links, sources, sync_stamp(source))
        texi = texidir / f"{name}.texi"
        texi.write_text(text, encoding="utf-8")
        code, stderr = run_makeinfo(texi, outdir)
        (BUILD / f"{name}.warnings.txt").write_text("\n".join(warnings) + ("\n" if warnings else ""))
        (BUILD / f"{name}.makeinfo.txt").write_text(stderr)
        n_mi = len([l for l in stderr.splitlines() if l.strip()])
        log(f"{name}: {len(list(tree_pages(root)))} pages, {len(warnings)} conversion warnings, "
            f"{n_mi} makeinfo messages{'' if code == 0 else ' (FAILED, see build/' + name + '.makeinfo.txt)'}")
        results[name] = code == 0
    write_node_map(docs, aliases)
    unresolved = sorted(links.unresolved.items(), key=lambda kv: -kv[1])
    (BUILD / "unresolved-links.txt").write_text("".join(f"{n}\t{u}\n" for u, n in unresolved))
    misses = sorted(links.fragment_misses.items(), key=lambda kv: -kv[1])
    (BUILD / "unresolved-fragments.txt").write_text("".join(f"{n}\t{u}#{f}\n" for (u, f), n in misses))
    log(f"{len(unresolved)} docs URLs matched no page (build/unresolved-links.txt); "
        f"{len(misses)} #fragments matched no heading and link to the page top "
        f"(build/unresolved-fragments.txt)")
    return results


def sync_stamp(source: Source) -> str:
    """Date of the last successful sync of a source, for the Top node."""
    try:
        return "on " + (STATE / f"{source.id}.last-sync").read_text()[:10]
    except FileNotFoundError:
        return "on " + datetime.now(timezone.utc).strftime("%Y-%m-%d") + " (build date; no sync record)"


def write_node_map(docs: list[PageDoc], aliases: dict[str, PageDoc]) -> None:
    """build/nodes.json: mirror path and URL -> (manual, node), for search/open."""
    data: dict = {}
    urls: dict = {}
    for d in docs:
        data[d.key] = [d.manual.name, d.node]
        urls[d.url] = [d.manual.name, d.node]
    for url, d in aliases.items():
        urls[url] = [d.manual.name, d.node]
    for path, d in ALIAS_PATHS.items():
        data[path] = [d.manual.name, d.node]
    data["_urls"] = urls
    (BUILD / "nodes.json").write_text(json.dumps(data, indent=0, ensure_ascii=False))
