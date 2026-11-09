"""Tests for claude_info.build: URLs, titles, the node tree, names, links,
and a full build of a tiny mirrored site through pandoc and makeinfo."""

from __future__ import annotations

import json
import random
import shutil
from collections import Counter

import pytest

from claude_info import build
from claude_info import texinfo as tx
from claude_info.build import Group, PageDoc
from claude_info.config import Manual, Source

pytestmark = pytest.mark.usefixtures("isolated")

BASE = "https://docs.example.com/en/"
MAN = Manual("docs", "Docs", "The docs.", ("",))
SRC = Source(id="s", name="S", base=BASE, manuals=(MAN,))

needs_tools = pytest.mark.skipif(not (shutil.which("pandoc") and shutil.which("makeinfo")),
                                 reason="pandoc and makeinfo are required")


def doc(path, title, nav=("Guide",), order=0, blocks=None, manual=MAN, source=SRC, url=None, desc=""):
    return PageDoc(source=source, manual=manual, path=path,
                   url=url or build.canonical(source.base + path), title=title, description=desc,
                   nav=list(nav), order=order, ast={"blocks": blocks or []})


def H(level, ident, text):
    return {"t": "Header", "c": [level, [ident, [], []], [{"t": "Str", "c": text}]]}


def shape(node):
    """A compact view of a tree: titles of groups (with landing) and pages."""
    if isinstance(node, PageDoc):
        return node.title
    head = node.title + (f" [{node.landing.title}]" if node.landing else "")
    return {head: [shape(c) for c in node.children]}


# -- canonical / humanize ----------------------------------------------------------


@pytest.mark.parametrize("url, out", [
    ("https://docs.example.com/en/a", "https://docs.example.com/en/a"),
    ("https://docs.example.com/en/a.md", "https://docs.example.com/en/a"),
    ("https://docs.example.com/en/a/", "https://docs.example.com/en/a"),
    ("https://docs.example.com/en/a//", "https://docs.example.com/en/a"),
    ("http://WWW.Docs.Example.com/en/a", "https://docs.example.com/en/a"),
    ("https://docs.example.com/en/a?x=1#frag", "https://docs.example.com/en/a"),
    ("https://docs.example.com", "https://docs.example.com"),
    ("https://docs.example.com/", "https://docs.example.com"),
    ("https://docs.example.com/en/Case/Path", "https://docs.example.com/en/Case/Path"),
])
def test_canonical(url, out):
    assert build.canonical(url) == out


@pytest.mark.parametrize("segment, title", [
    ("tool-use", "Tool use"),
    ("claude-api", "Claude API"),
    ("claude-code", "Claude code"),
    ("agent-sdk", "Agent SDK"),
    ("github_actions", "GitHub actions"),
    ("mcp", "MCP"),
    ("macos-setup", "macOS setup"),
    ("2025-06-18", "2025-06-18"),
    ("v1.2", "v1.2"),
    ("3", "3"),
    ("already Titled", "Already Titled"),
    ("", ""),
    ("--", "--"),
])
def test_humanize(segment, title):
    assert build.humanize(segment) == title


# -- fuzzy_anchor ------------------------------------------------------------------------


def test_fuzzy_anchor_matches_renamed_heading():
    anchors = {"eliminate-permission-prompts-with-auto-mode": "A", "configure-hooks": "B"}
    assert build.fuzzy_anchor("eliminate-prompts-with-auto-mode", anchors) == "A"


@pytest.mark.parametrize("frag, anchors", [
    ("hooks", {"hooks": "A"}),  # one word: too ambiguous to guess
    ("configure-mcp-servers", {"install-plugins-quickly": "A"}),  # too different
    ("set-up-hooks", {"set-up-hooks-now": "A", "set-up-hooks-later": "B"}),  # a tie
    ("a-b", {}),
])
def test_fuzzy_anchor_refuses(frag, anchors):
    assert build.fuzzy_anchor(frag, anchors) is None


# -- LinkMap ---------------------------------------------------------------------------------

CODE = Source(id="code", name="Code", base="https://code.claude.com/docs/en/",
              manuals=(Manual("claude-code", "Claude Code", "", ("",)),))
PLAT = Source(id="platform", name="Platform", base="https://platform.claude.com/docs/en/",
              manuals=(Manual("claude-api", "API", "", ("api/",)), Manual("claude-platform", "P", "", ("",))))


def linked_docs():
    docs = [
        doc("hooks.md", "Hooks reference", source=CODE, manual=CODE.manuals[0]),
        doc("api/messages.md", "Messages", source=PLAT, manual=PLAT.manuals[0]),
        doc("build-with-claude/caching.md", "Prompt caching", source=PLAT, manual=PLAT.manuals[1]),
        doc("guide/index.md", "Guide", source=PLAT, manual=PLAT.manuals[1]),
        doc("new-home.md", "New home", source=PLAT, manual=PLAT.manuals[1]),
    ]
    for d in docs:
        d.node = d.title
    docs[0].anchors = {"events": "Hooks reference - Events",
                       "eliminate-permission-prompts-with-auto-mode": "Hooks reference - Auto"}
    return docs


@pytest.fixture
def links(isolated):
    isolated.mirror.mkdir(parents=True, exist_ok=True)
    isolated.redirects.write_text(json.dumps({
        "https://platform.claude.com/docs/en/old-home": "https://platform.claude.com/docs/en/new-home.md",
        "https://code.claude.com/docs/en/legacy-hop": "https://docs.anthropic.com/en/api/messages",
        "https://platform.claude.com/docs/en/dead": None,
    }))
    docs = linked_docs()
    twin = docs[3]
    return build.LinkMap(docs, {"https://platform.claude.com/docs/en/guide-copy": twin})


HOOKS_URL = "https://code.claude.com/docs/en/hooks"


@pytest.mark.parametrize("url, node", [
    ("https://code.claude.com/docs/en/hooks", "Hooks reference"),
    ("https://code.claude.com/docs/en/hooks.md", "Hooks reference"),
    ("https://code.claude.com/docs/en/hooks/", "Hooks reference"),
    ("http://www.code.claude.com/docs/en/hooks?x=1", "Hooks reference"),
    ("https://docs.anthropic.com/en/docs/claude-code/hooks", "Hooks reference"),
    ("https://docs.anthropic.com/docs/claude-code/hooks", "Hooks reference"),
    ("https://docs.claude.com/en/docs/claude-code/hooks", "Hooks reference"),
    ("https://code.claude.com/docs/hooks", "Hooks reference"),
    ("https://docs.anthropic.com/en/api/messages", "Messages"),
    ("https://docs.anthropic.com/en/docs/build-with-claude/caching", "Prompt caching"),
    ("https://platform.claude.com/docs/api/messages", "Messages"),
    ("https://anthropic.com/docs/build-with-claude/caching", "Prompt caching"),
    ("https://www.anthropic.com/docs/build-with-claude/caching", "Prompt caching"),
    ("https://platform.claude.com/docs/en/guide", "Guide"),  # guide/index.md
    ("https://platform.claude.com/docs/en/guide/index", "Guide"),
    ("https://platform.claude.com/docs/en/guide-copy", "Guide"),  # folded duplicate
    ("https://platform.claude.com/docs/en/old-home", "New home"),  # recorded redirect
    ("https://code.claude.com/docs/en/legacy-hop", "Messages"),  # redirect to a legacy URL
])
def test_linkmap_resolves(links, url, node):
    t = links.resolve(url, "https://platform.claude.com/docs/en/elsewhere")
    assert t is not None and t.node == node and not t.here


def test_linkmap_cross_manual_target(links):
    t = links.resolve(HOOKS_URL, "https://platform.claude.com/docs/en/api/messages")
    assert t.manual == "claude-code"


def test_linkmap_fragments(links):
    page = "https://platform.claude.com/docs/en/api/messages"
    assert links.resolve(HOOKS_URL + "#events", page) == tx.Target("claude-code", "Hooks reference - Events")
    assert links.resolve(HOOKS_URL + "#eliminate-prompts-with-auto-mode", page).node == "Hooks reference - Auto"
    t = links.resolve(HOOKS_URL + "#no-such-heading", page)
    assert t == tx.Target("claude-code", "Hooks reference")
    assert links.fragment_misses == {("https://code.claude.com/docs/en/hooks", "no-such-heading"): 1}


def test_linkmap_same_page(links):
    assert links.resolve("#events", HOOKS_URL) == tx.Target("claude-code", "Hooks reference - Events")
    assert links.resolve("#gone", HOOKS_URL) == tx.Target("claude-code", "Hooks reference", here=True)
    assert links.resolve(HOOKS_URL, HOOKS_URL + "#x").here
    assert links.resolve(HOOKS_URL + ".md", HOOKS_URL).here


def test_linkmap_unresolved(links):
    page = HOOKS_URL
    assert links.resolve("https://code.claude.com/docs/en/missing", page) is None
    assert links.resolve("https://code.claude.com/docs/en/missing#x", page) is None
    assert links.resolve("https://platform.claude.com/docs/en/dead", page) is None
    assert links.resolve("https://example.org/page", page) is None
    assert links.resolve("mailto:a@b.c", page) is None
    assert links.resolve("/docs/en/hooks", page) is None
    assert links.unresolved == {"https://code.claude.com/docs/en/missing": 2,
                                "https://platform.claude.com/docs/en/dead": 1}


def test_linkmap_page_without_node(isolated):
    d = doc("a.md", "A")
    assert build.LinkMap([d], {}).resolve(BASE + "a", BASE + "b") is None


def test_linkmap_survives_missing_or_corrupt_redirects(isolated):
    isolated.mirror.mkdir(parents=True, exist_ok=True)
    assert build.LinkMap([], {}).redirects == {}
    isolated.redirects.write_text("{nope")
    assert build.LinkMap([], {}).redirects == {}


# -- titles ------------------------------------------------------------------------------------


def test_choose_title_preference():
    d = doc("dir/some-page.md", "Index title", blocks=[H(1, "h", "Heading title")])
    assert build.choose_title(d, {"title": " Meta title "}) == "Meta title"
    assert build.choose_title(d, {}) == "Heading title"
    d.ast = {"blocks": [H(2, "h", "Not a title")]}
    assert build.choose_title(d, {}) == "Index title"
    d.title = ""
    assert build.choose_title(d, {}) == "Some page"


def test_title_header_and_body_blocks():
    para = {"t": "Para", "c": [{"t": "Str", "c": "x"}]}
    d = doc("a.md", "Hooks: reference", blocks=[H(1, "hooks-reference", "Hooks - reference"), para])
    assert build.title_header(d) is d.ast["blocks"][0]
    assert build.body_blocks(d) == [para]
    d2 = doc("b.md", "Other", blocks=[H(1, "x", "Different"), para])
    assert build.title_header(d2) is None and len(build.body_blocks(d2)) == 2


# -- the tree ------------------------------------------------------------------------------------


def test_build_tree_follows_nav_and_order():
    docs = [doc("c.md", "C", ["Reference"], 2), doc("a.md", "A", ["Start"], 0),
            doc("b.md", "B", ["Start", "Deep"], 1), doc("d.md", "D", ["Reference"], 3),
            doc("e.md", "E", ["Start", "Deep"], 4)]
    root = build.build_tree(MAN, docs)
    assert shape(root) == {"Docs": [{"Start": ["A", {"Deep": ["B", "E"]}]}, {"Reference": ["C", "D"]}]}


def test_collapse_wrapper_group_and_landing_and_single_pages():
    docs = [doc("a.md", "Docs", ["Wrapper"], 0),  # titled like the manual: root landing
            doc("b.md", "Tools", ["Wrapper", "Tools"], 1),  # titled like its group: landing
            doc("c.md", "Web search", ["Wrapper", "Tools"], 2),
            doc("d.md", "Lonely", ["Wrapper", "Solo"], 3),  # single-page group: just the page
            doc("e.md", "Inner", ["Wrapper", "Tools", "Tools"], 4)]  # same title as parent: flattened
    root = build.build_tree(MAN, docs)
    assert shape(root) == {"Docs": ["Docs", {"Tools [Tools]": ["Web search", "Inner"]}, "Lonely"]}
    assert root.landing is None  # the root landing is a regular first entry
    assert Counter(id(p) for p in build.tree_pages(root)) == Counter(id(d) for d in docs)


def test_root_landing_from_single_wrapper_group_is_kept():
    g = Group("Docs", children=[Group("Wrapper", children=[doc("b.md", "B"), doc("c.md", "C")],
                                      landing=doc("a.md", "Wrapper page"))])
    build.collapse(g)
    assert g.landing is not None and g.landing.title == "Wrapper page"
    docs = [doc("a.md", "Docs", ["Only"], 0), doc("b.md", "B", ["Only"], 1)]
    root = build.build_tree(MAN, docs)
    assert [p.title for p in build.tree_pages(root)] == ["Docs", "B"]
    assert root.children[0].title == "Docs"


def test_split_flat_regroups_by_path():
    docs = [doc(f"api/top-{i}.md", f"Top {i}", ["API"], i) for i in range(5)]
    docs += [doc("api/messages/create.md", "Create a message", ["API"], 10),
             doc("api/messages/count.md", "Count tokens", ["API"], 11),
             doc("api/models.md", "Models", ["API"], 12),  # landing of api/models/
             doc("api/models/list.md", "List models", ["API"], 13),
             doc("api/models/get.md", "Get a model", ["API"], 14),
             doc("api/batches/index.md", "Batches", ["API"], 15),  # landing of api/batches/
             doc("api/batches/create.md", "Create a batch", ["API"], 16),
             doc("api/batches/cancel.md", "Cancel a batch", ["API"], 17),
             doc("api/files/upload.md", "Upload a file", ["API"], 18)]  # lone page: no group
    docs += [doc(f"api/more-{i}.md", f"More {i}", ["API"], 20 + i) for i in range(4)]
    assert len(docs) > build.MAX_MENU_PAGES
    root = build.build_tree(MAN, docs)
    tree = shape(root)["Docs"]
    titles = [t if isinstance(t, str) else next(iter(t)) for t in tree]
    assert titles == ["Top 0", "Top 1", "Top 2", "Top 3", "Top 4", "Messages", "Models [Models]",
                      "Batches [Batches]", "Upload a file", "More 0", "More 1", "More 2", "More 3"]
    groups = {next(iter(t)): t[next(iter(t))] for t in tree if isinstance(t, dict)}
    assert groups["Messages"] == ["Create a message", "Count tokens"]
    assert groups["Models [Models]"] == ["List models", "Get a model"]
    assert groups["Batches [Batches]"] == ["Create a batch", "Cancel a batch"]
    assert Counter(id(p) for p in build.tree_pages(root)) == Counter(id(d) for d in docs)


def test_regroup_by_path_with_nothing_to_group():
    docs = [doc(f"p{i}.md", f"P{i}") for i in range(3)]
    assert build.regroup_by_path(docs) == docs


def test_regroup_index_only_directory_keeps_the_page():
    children = [doc("a.md", "A"), doc("only/index.md", "Only index"), doc("b.md", "B")]
    out = build.regroup_by_path(children)
    pages = []
    for c in out:
        pages += [c] if isinstance(c, PageDoc) else list(build.tree_pages(c))
    assert sorted(p.title for p in pages) == ["A", "B", "Only index"]


def test_adopt_nav():
    docs = [doc("guides/basics.md", "Basics", ["Guides"], 0),
            doc("guides/advanced/intro.md", "Intro", ["Guides", "Advanced"], 5),
            doc("guides/advanced/deep.md", "Deep", ["Other pages"], 99),
            doc("guides/advanced/index.md", "Advanced index", ["Other pages"], 100),
            doc("unrelated/thing.md", "Thing", ["Other pages"], 101)]
    build.adopt_nav(docs)
    assert docs[2].nav == ["Guides", "Advanced"] and docs[2].order == 5.5
    assert docs[3].nav == ["Guides", "Advanced"]
    assert docs[4].nav == ["Other pages"]


def test_adopt_nav_copies_the_list():
    docs = [doc("a/b.md", "B", ["X"], 0), doc("a/c.md", "C", ["Other pages"], 1)]
    build.adopt_nav(docs)
    docs[1].nav.append("mutated")
    assert docs[0].nav == ["X"]


# -- names ---------------------------------------------------------------------------------------


def all_names(root: Group) -> list[str]:
    names = [g.node for g in build.walk(root) if g is not root]
    for p in build.tree_pages(root):
        names.append(p.node)
        names += [a for i, a in p.anchors.items() if a != p.node]
    # A group's landing shares the group's node name.
    landings = {id(g.landing) for g in build.walk(root) if g.landing}
    names = [g.node for g in build.walk(root) if g is not root]
    names += [p.node for p in build.tree_pages(root) if id(p) not in landings]
    for p in build.tree_pages(root):
        names += [a for a in p.anchors.values() if a != p.node]
    return names


def test_names_shallow_first_and_qualified():
    docs = [doc("a/overview.md", "Overview", ["Alpha"], 0), doc("a/x.md", "X", ["Alpha"], 1),
            doc("b/overview.md", "Overview", ["Beta"], 2), doc("b/y.md", "Y", ["Beta"], 3),
            doc("c/overview.md", "overview", ["Gamma"], 4), doc("c/z.md", "Z", ["Gamma"], 5)]
    root = build.build_tree(MAN, docs)
    build.assign_names(root)
    assert [d.node for d in docs] == ["Overview", "X", "Overview (Beta)", "Y", "overview (Gamma)", "Z"]


def test_names_reserved_and_numbered():
    docs = [doc("index.md", "Index", ["Root"], 0), doc("top.md", "Top", ["Root"], 1),
            doc("about.md", "About this manual", ["Root"], 2),
            doc("dup1.md", "Dup", ["Root"], 3), doc("dup2.md", "dup", ["Root"], 4),
            doc("dup3.md", "DUP", ["Root"], 5)]
    root = build.build_tree(MAN, docs)
    build.assign_names(root)
    nodes = [d.node for d in docs]
    assert len({n.lower() for n in nodes}) == 6
    assert not {n.lower() for n in nodes} & build.Names.RESERVED
    assert nodes[3] == "Dup" and nodes[4] == "dup 2" and nodes[5] == "DUP 3"


def test_names_anchor_for_headers():
    blocks = [H(1, "title-id", "Hooks"), H(2, "events", "Events"), H(2, "events-2", "Events"),
              H(3, "colon", "Step: one")]
    docs = [doc("hooks.md", "Hooks", ["Ref"], 0, blocks=blocks), doc("x.md", "X", ["Ref"], 1)]
    root = build.build_tree(MAN, docs)
    build.assign_names(root)
    a = docs[0].anchors
    assert a["title-id"] == "Hooks"  # links to the dropped title header go to the node
    assert a["events"] == "Hooks - Events" and a["events-2"] == "Hooks - Events 2"
    assert a["colon"] == "Hooks - Step - one"


def test_names_property_unique_and_nothing_lost():
    rnd = random.Random(11)
    words = ["Overview", "overview", "Setup", "Index", "Top", "API: reference", "a.b", "Tools, more",
             "Hooks", "Quickstart", "FAQ", "Models", "Docs"]
    dirs = ["", "api/", "api/messages/", "guides/", "guides/advanced/", "tools/", "tools/web/"]
    for trial in range(40):
        docs = []
        for i in range(rnd.randint(1, 60)):
            nav = [rnd.choice(words) for _ in range(rnd.randint(0, 3))] or ["Other pages"]
            leaf = rnd.choice(["index", "overview", f"p{i}", rnd.choice(words).lower().replace(" ", "-")])
            path = f"{rnd.choice(dirs)}{leaf}-{i}.md" if rnd.random() < 0.7 else f"{rnd.choice(dirs)}{leaf}.md"
            blocks = [H(2, f"h{j}", rnd.choice(words)) for j in range(rnd.randint(0, 3))]
            docs.append(doc(path, rnd.choice(words), nav, i, blocks=blocks))
        root = build.build_tree(MAN, docs)
        build.assign_names(root)
        assert Counter(id(p) for p in build.tree_pages(root)) == Counter(id(d) for d in docs), trial
        names = all_names(root)
        lowered = [n.lower() for n in names]
        assert len(set(lowered)) == len(lowered), (trial, Counter(lowered).most_common(3))
        assert not set(lowered) & build.Names.RESERVED
        for n in names:
            assert not set(n) & set(":,.@{}"), n


# -- drop_duplicates -----------------------------------------------------------------------------


def write_pages(source, files: dict[str, bytes]):
    for path, data in files.items():
        f = source.pages_dir / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(data)


def test_drop_duplicates(isolated):
    other = Source(id="other", name="O", base="https://o.example.com/", manuals=(MAN,))
    write_pages(SRC, {"whats-new.md": b"same", "whats-new/index.md": b"same", "x.md": b"same",
                      "solo.md": b"unique", "a.md": b"twins", "b.md": b"twins"})
    write_pages(other, {"copy.md": b"same"})
    indexed = doc("whats-new.md", "What's new", ["Ref"])
    alias = doc("whats-new/index.md", "", ["Other pages"])
    indexed_twin = doc("x.md", "X", ["Ref"])  # identical but indexed: both stay
    solo = doc("solo.md", "Solo", ["Other pages"])
    a, b = doc("a.md", "A", ["Other pages"]), doc("b.md", "B", ["Other pages"])  # no indexed twin
    cross = doc("copy.md", "Copy", ["Other pages"], source=other)  # other source: stays
    kept, aliases = build.drop_duplicates([indexed, alias, indexed_twin, solo, a, b, cross])
    assert kept == [indexed, indexed_twin, solo, a, b, cross]
    assert aliases == {alias.url: indexed}
    assert build.ALIAS_PATHS == {"s/pages/whats-new/index.md": indexed}


# -- menus ---------------------------------------------------------------------------------------


def test_menu_entry():
    assert build.menu_entry("Hooks", "") == "* Hooks::"
    e = build.menu_entry("Hooks", "Run   shell\ncommands -- fast")
    assert e == "* Hooks::".ljust(32) + "Run shell commands -@asis{}- fast"
    long = build.menu_entry("Hooks", "word " * 40)
    assert long.endswith("…") and tx.dwidth(long) <= 78
    assert build.menu_entry("N" * 60, "desc") == "* " + "N" * 60 + "::"


def test_sync_stamp(isolated):
    assert "(build date; no sync record)" in build.sync_stamp(SRC)
    isolated.state.mkdir(parents=True)
    (isolated.state / "s.last-sync").write_text("2026-10-01T03:04:05+00:00")
    assert build.sync_stamp(SRC) == "on 2026-10-01"


# -- full build ------------------------------------------------------------------------------------


@needs_tools
def test_build_end_to_end(site, isolated):
    logs = []
    results = build.build(log=logs.append)
    assert results == {"claude-code": True, "claude-platform": True, "claude-api": True}
    for name in results:
        assert (isolated.build / "info" / f"{name}.info").exists()
        assert (isolated.build / f"{name}.makeinfo.txt").read_text() == ""
        assert (isolated.build / f"{name}.warnings.txt").read_text() == ""
    nodes = json.loads((isolated.build / "nodes.json").read_text())
    assert nodes["code/pages/hooks.md"] == ["claude-code", "Hooks reference"]
    assert nodes["code/pages/whats-new/index.md"] == ["claude-code", "What's new"]  # folded twin
    assert nodes["_urls"]["https://code.claude.com/docs/en/whats-new/index"] == ["claude-code", "What's new"]
    assert nodes["platform/pages/api/messages.md"] == ["claude-api", "Messages"]
    info = (isolated.build / "info" / "claude-code.info").read_text()
    text = " ".join(info.split())
    assert "*note Messages API: (claude-api)Messages - Request" in text  # cross-manual
    assert "*note settings: Settings" in text  # legacy docs.anthropic.com URL
    assert "*note moved page: Settings" in text  # recorded redirect
    assert "*note events: Hooks reference - Events" in text  # same-page anchor
    assert "── Diagram" in info and "Alice" in info
    assert "Online: <https://code.claude.com/docs/en/hooks>" in text
    platform = " ".join((isolated.build / "info" / "claude-platform.info").read_text().split())
    assert "*note hooks reference: (claude-code)Hooks reference - Events" in platform
    assert (isolated.build / "unresolved-links.txt").read_text() == ""
    assert (isolated.build / "unresolved-fragments.txt").read_text() == ""
    # The AST cache lives under build/, and a second build reuses it.
    assert list((isolated.build / "cache" / "ast").rglob("*.json"))
    assert build.build(log=logs.append) == results


@needs_tools
def test_build_selected_source_still_links_everywhere(site, isolated):
    results = build.build(["platform"], log=lambda *a: None)
    assert results == {"claude-platform": True, "claude-api": True}
    assert not (isolated.build / "info" / "claude-code.info").exists()
    nodes = json.loads((isolated.build / "nodes.json").read_text())
    assert "code/pages/hooks.md" in nodes  # every source is loaded for links and the node map


@needs_tools
def test_build_failing_manual_is_reported_and_others_still_build(site, isolated, monkeypatch):
    real = build.page_body

    def broken(d, links):
        body, warnings = real(d, links)
        if d.path == "settings.md":
            body += "\n@xref{No such node anywhere}.\n"
        return body, warnings

    monkeypatch.setattr(build, "page_body", broken)
    logs = []
    results = build.build(log=logs.append)
    assert results == {"claude-code": False, "claude-platform": True, "claude-api": True}
    assert "No such node anywhere" in (isolated.build / "claude-code.makeinfo.txt").read_text()
    assert any("claude-code" in l and "FAILED" in l for l in logs)


@needs_tools
def test_build_unresolved_links_are_listed(site, isolated):
    (site[0].pages_dir / "settings.md").write_text(
        "# Settings\n\nSee [gone](https://code.claude.com/docs/en/nowhere) and "
        "[bad anchor](https://code.claude.com/docs/en/hooks#not-a-heading-here).\n")
    build.build(log=lambda *a: None)
    assert (isolated.build / "unresolved-links.txt").read_text() == "1\thttps://code.claude.com/docs/en/nowhere\n"
    assert (isolated.build / "unresolved-fragments.txt").read_text() == (
        "1\thttps://code.claude.com/docs/en/hooks#not-a-heading-here\n")
