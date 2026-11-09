"""Tests for claude_info.texinfo: escaping, node names, wrapping, tables,
links, and real makeinfo runs over small generated documents."""

from __future__ import annotations

import json
import random
import shutil
import signal
import subprocess
from contextlib import contextmanager

import pytest

from claude_info import texinfo as tx
from claude_info.config import PANDOC_READER
from claude_info.texinfo import Target, dwidth, layout_records, layout_table, wrap

needs_makeinfo = pytest.mark.skipif(shutil.which("makeinfo") is None, reason="makeinfo not installed")
needs_pandoc = pytest.mark.skipif(shutil.which("pandoc") is None, reason="pandoc not installed")

PAGE = "https://docs.example.com/en/page"
OTHER = "https://docs.example.com/en/other"
HOOKS = "https://code.example.com/docs/en/hooks"


def resolver(url: str, page_url: str):
    """Fake LinkMap.resolve: two pages in this manual, one in another."""
    if url.startswith("#"):
        url = page_url + url
    base, _, frag = url.partition("#")
    if base == PAGE:
        if frag == "known":
            return Target("docs", "This page - Known")
        return Target("docs", "This page", here=True)
    if base == OTHER:
        return Target("docs", "Other page - Sec" if frag == "sec" else "Other page")
    if base == HOOKS:
        return Target("claude-code", "Hooks reference")
    return None


def writer(anchors=None, widths=None) -> tx.PageWriter:
    def diagram(source, width):
        if widths is not None:
            widths.append(width)
        return f"[diagram at {width}]"

    return tx.PageWriter(manual="docs", page_url=PAGE, page_title="This page",
                         anchors=anchors or {}, resolve=resolver, diagram=diagram)


def blocks_of(markdown: str) -> list:
    r = subprocess.run(["pandoc", "--preserve-tabs", "-f", PANDOC_READER, "-t", "json"],
                       input=markdown, capture_output=True, text=True, check=True)
    return json.loads(r.stdout)["blocks"]


def render(markdown: str, w: tx.PageWriter | None = None) -> str:
    return (w or writer()).blocks(blocks_of(markdown))


def S(s):  # Str
    return {"t": "Str", "c": s}


SP = {"t": "Space"}
LB_SPAN = {"t": "Span", "c": [["", ["linebreak"], []], []]}


def link(inls, url):
    return {"t": "Link", "c": [["", [], []], inls, [url, ""]]}


# -- makeinfo harness ----------------------------------------------------------


def run_makeinfo(tmp_path, body: str, extra_nodes: dict[str, str] | None = None):
    """Wrap a fragment into a small manual (Top + extra nodes), run makeinfo
    as the builder does, and return (returncode, stderr, info text)."""
    extra_nodes = {"This page": "", "Other page": "@anchor{Other page - Sec}\nSection.\n",
                   **(extra_nodes or {})}
    parts = ["\\input texinfo", "@setfilename t.info", "@documentencoding UTF-8",
             "@settitle T", "@frenchspacing on", "", "@node Top", "@top T", "", body, "", "@menu"]
    parts += [f"* {n}::" for n in extra_nodes] + ["@end menu", ""]
    for name, text in extra_nodes.items():
        parts += [f"@node {name}", f"@chapheading {tx.esc_text(name)}", text or "Text.", ""]
    parts += ["@bye", ""]
    texi = tmp_path / "t.texi"
    texi.write_text("\n".join(parts), encoding="utf-8")
    r = subprocess.run(["makeinfo", "--enable-encoding", "--fill-column=78", "--no-split",
                        "-o", str(tmp_path / "t.info"), str(texi)], capture_output=True, text=True)
    info = (tmp_path / "t.info").read_text(encoding="utf-8") if r.returncode == 0 else ""
    return r.returncode, r.stderr, info


def top_text(info: str) -> str:
    """The Top node's text with paragraphs re-joined on single spaces."""
    chunk = info.split("\x1f\n")[1]
    return " ".join(chunk.split("\n", 2)[2].split())


@contextmanager
def time_limit(seconds: float):
    def handler(signum, frame):
        raise TimeoutError(f"took longer than {seconds} s")

    old = signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


# -- escaping ------------------------------------------------------------------------


def test_esc_specials():
    assert tx.esc("a@b{c}d") == "a@@b@{c@}d"
    assert tx.esc("--") == "--"  # code and examples have no ligatures


@pytest.mark.parametrize("raw, escaped", [
    ("a -- b", "a -@asis{}- b"),
    ("a --- b", "a -@asis{}-@asis{}- b"),
    ("--flag", "-@asis{}-flag"),
    ("x - y", "x - y"),
    ("``q''", "@U{0060}@U{0060}q'@asis{}'"),
    ("it's", "it's"),
    ("`x`", "@U{0060}x@U{0060}"),
    ("a\tb", "a b"),
    ("@{}", "@@@{@}"),
])
def test_esc_text(raw, escaped):
    assert tx.esc_text(raw) == escaped


def test_esc_arg():
    assert tx.esc_arg("a, b") == "a@comma{} b"


@needs_makeinfo
def test_esc_text_survives_makeinfo_literally(tmp_path):
    raw = "a -- b --- c ``q'' `x' it's @home {braces} --verbose 'single'"
    rc, err, info = run_makeinfo(tmp_path, tx.para(tx.esc_text(raw)))
    assert rc == 0 and err == ""
    assert raw in top_text(info)


# -- node names ---------------------------------------------------------------------------


@pytest.mark.parametrize("title, name", [
    ("Hooks: reference", "Hooks - reference"),
    ("Hooks : reference", "Hooks - reference"),
    ("Tools, agents, and more", "Tools agents and more"),
    ("Claude 3.5 Sonnet", "Claude 3․5 Sonnet"),
    ("index.md", "index․md"),
    ("@mentions and {braces}", "mentions and braces"),
    ("a -- b --- c", "a - b - c"),
    ("``quoted''", "'quoted'"),
    ("  lots   of\tspace ", "lots of space"),
    ("(optional) setup", "optional) setup"),
    ("", "Untitled"),
    (" : ", "Untitled"),
    ("@{}", "Untitled"),
    ("Café", "Café"),
    ("- leading dash", "leading dash"),
])
def test_node_name(title, name):
    assert tx.node_name(title) == name


def test_node_name_has_no_delimiters():
    for title in ["a:b", "a,b", "a.b", "a@b", "a{b}", "x: y, z. w", "1.2.3: v, w"]:
        n = tx.node_name(title)
        assert not set(n) & set(":,.@{}"), (title, n)


NASTY_TITLES = [
    "Hooks: reference", "Models, pricing, and limits", "Claude 3.5 Sonnet", "v1.2.3",
    "Use @mentions", "Set {braces}", "a -- b", "``Quoted''", "What's new?", "(dir) trick",
    "Ends with a dot.", "Tab\there", "Émoji 🚀 and 漢字", "*Note this", "Star * in middle",
]


@needs_makeinfo
def test_node_names_are_legal_for_makeinfo(tmp_path):
    names = [tx.node_name(t) for t in NASTY_TITLES]
    assert len(set(names)) == len(names)
    refs = " ".join("@ref{" + tx.esc_arg(n) + ",,label}." for n in names)
    rc, err, info = run_makeinfo(tmp_path, tx.para(refs), {n: "" for n in names})
    assert rc == 0, err
    assert err == ""
    for n in names:
        assert f"Node: {n}," in info


def test_index_entry():
    assert tx.index_entry("Hooks: events\n  and  more") == "Hooks - events and more"
    assert tx.index_entry("a -- b") == "a -@asis{}- b"


# -- display width and wrapping ----------------------------------------------------------


@pytest.mark.parametrize("s, w", [
    ("abc", 3), ("", 0), ("漢字", 4), ("ｶﾀｶﾅ", 4), ("Ａ", 2),
    ("é", 1), ("naïve", 5), ("a​b", 2), ("a‍b", 2), ("👍", 2),
    ("‘’“”…─│", 7),
])
def test_dwidth(s, w):
    assert dwidth(s) == w


def test_wrap_basic():
    assert wrap("the quick brown fox jumps", 10) == ["the quick", "brown fox", "jumps"]
    assert wrap("", 10) == [""]
    assert wrap("   ", 10) == [""]
    assert wrap("exactly10!", 10) == ["exactly10!"]


def test_wrap_wide_chars_by_display_width():
    lines = wrap("漢字 漢字 漢字", 9)
    assert lines == ["漢字 漢字", "漢字"]
    assert all(dwidth(l) <= 9 for l in lines)


def test_wrap_hard_breaks_long_word_at_punctuation():
    lines = wrap("see https://example.com/some/long/path/to/page", 20)
    assert all(dwidth(l) <= 20 for l in lines)
    assert "".join(lines).replace(" ", "") == "seehttps://example.com/some/long/path/to/page"
    assert lines[1].endswith("/")  # broke after a slash, not mid-segment


def test_wrap_short_room_starts_new_line():
    # Only 3 columns left after "abcdef": the long word starts on a new line.
    lines = wrap("abcdef " + "x" * 30, 10)
    assert lines[0] == "abcdef"
    assert all(dwidth(l) <= 10 for l in lines)


def test_wrap_property_no_loss_no_overflow():
    rnd = random.Random(7)
    vocab = ["a", "to", "word", "configuration", "漢字", "https://x.example/a/b/c", "x" * 33,
             "snake_case_identifier", "naïve", "é"]
    for _ in range(500):
        text = " ".join(rnd.choice(vocab) for _ in range(rnd.randint(0, 15)))
        width = rnd.randint(2, 40)
        with time_limit(2):
            lines = wrap(text, width)
        assert all(dwidth(l) <= width for l in lines), (text, width, lines)
        assert "".join("".join(lines).split()) == "".join(text.split())


def test_wrap_terminates_for_wide_char_wider_than_width():
    with time_limit(1):
        lines = wrap("漢", 1)
    assert "".join(lines) == "漢"


@pytest.mark.parametrize("word, width, split", [
    ("foo.bar.baz.quux", 9, ("foo.bar.", "baz.quux")),
    ("abcdefghijkl", 5, ("abcde", "fghijkl")),
    ("a.bcdefghijkl", 9, ("a.bcdefgh", "ijkl")),  # punctuation too early: hard cut
    ("short", 10, ("short", "")),
    ("漢字漢字", 5, ("漢字", "漢字")),
    ("key=value&other=thing", 12, ("key=value&", "other=thing")),
])
def test_split_at_width(word, width, split):
    assert tx._split_at_width(word, width) == split


@pytest.mark.parametrize("align, out", [
    ("AlignDefault", "ab   "), ("AlignLeft", "ab   "), ("AlignRight", "   ab"), ("AlignCenter", " ab  "),
])
def test_pad(align, out):
    assert tx.pad("ab", 5, align) == out
    assert tx.pad("toolong", 3, align) == "toolong"


# -- tables -------------------------------------------------------------------------------


def grid_cells(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if line.startswith("│"):
            rows.append([c.strip() for c in line.strip("│").split("│")])
    return rows


def test_layout_table_simple_grid():
    out = layout_table([["Name", "Type"]], [["model", "string"], ["max_tokens", "integer"]],
                       ["AlignDefault", "AlignRight"], 73)
    assert out.splitlines() == [
        "┌────────────┬─────────┐",
        "│ Name       │    Type │",
        "├────────────┼─────────┤",
        "│ model      │  string │",
        "│ max_tokens │ integer │",
        "└────────────┴─────────┘",
    ]


def test_layout_table_empty():
    assert layout_table([], [], [], 73) == ""
    assert layout_table([], [], ["AlignDefault"], 73) == ""


def test_layout_table_wraps_without_breaking_words():
    long = "This parameter controls how many tokens the model may generate before stopping"
    out = layout_table([["Param", "Description"]], [["max_tokens", long], ["temperature", "Randomness"]],
                       ["AlignDefault"] * 2, 40)
    assert out.startswith("┌")
    assert all(dwidth(l) <= 40 for l in out.splitlines())
    words = set(long.split()) | {"max_tokens", "temperature", "Randomness", "Param", "Description"}
    for row in grid_cells(out):
        for cell in row:
            assert set(cell.split()) <= words, cell
    assert "╌" in out  # multi-line rows are separated


def test_layout_table_property_never_exceeds_width_and_no_midword_in_grids():
    rnd = random.Random(3)
    vocab = ["a", "bb", "ccc", "word", "longerword", "x" * 15, "漢字漢字", "y" * 40,
             "https://example.com/a/b/c/d/e/f/g/h", "naïve"]
    short_heads = ["Name", "Type", "Default", "Notes", "A", "漢字"]
    for _ in range(1500):
        ncols = rnd.randint(1, 7)
        head = [[rnd.choice(short_heads) for _ in range(ncols)]] if rnd.random() < 0.8 else []
        body = [[" ".join(rnd.choice(vocab) for _ in range(rnd.randint(0, 8))) for _ in range(ncols)]
                for _ in range(rnd.randint(1, 5))]
        width = rnd.choice([30, 40, 58, 73])
        out = layout_table(head, body, ["AlignDefault"] * ncols, width)
        for line in out.splitlines():
            assert dwidth(line) <= width, (width, head, body, line)
        if out.startswith("┌"):
            words = {w for r in head + body for c in r for w in c.split()}
            for row in grid_cells(out):
                for cell in row:
                    assert set(cell.split()) <= words, (cell, body)


def test_layout_table_too_many_columns_becomes_records():
    head = [[f"Column{i}" for i in range(8)]]
    body = [[f"value{i}{j}" for i in range(8)] for j in range(2)]
    out = layout_table(head, body, ["AlignDefault"] * 8, 40)
    assert not out.startswith("┌")
    assert "Column0:" in out and "value01" in out
    assert out.splitlines()[0] == "─" * 40
    assert all(dwidth(l) <= 40 for l in out.splitlines())


def test_layout_table_long_words_force_records():
    out = layout_table([["a", "b", "c"]], [["x" * 20, "y" * 20, "z" * 20]], ["AlignDefault"] * 3, 50)
    assert not out.startswith("┌")
    assert "x" * 20 in out and "z" * 20 in out  # whole, not broken


def test_layout_table_tall_rows_become_records():
    para = " ".join(["lorem"] * 60)
    out = layout_table([["Key", "Description"]], [["k", para]], ["AlignDefault"] * 2, 30)
    assert not out.startswith("┌")
    assert out.count("lorem") == 60


def test_layout_table_mean_row_height_limit():
    para = " ".join(["word"] * 25)  # ~5 lines at this width, under the max of 8
    out = layout_table([["K", "V"]], [["k", para]] * 3, ["AlignDefault"] * 2, 30)
    assert not out.startswith("┌")


def test_layout_table_multiline_cells():
    out = layout_table([["K", "V"]], [["k", "line one\nline two"]], ["AlignDefault"] * 2, 73)
    rows = grid_cells(out)
    assert rows[1:] == [["k", "line one"], ["", "line two"]]


def test_layout_records_layout():
    out = layout_records([["Name", "Description"]], [["model", "Which model to use"]], 40)
    assert out.splitlines() == [
        "─" * 40,
        "Name:         model",
        "Description:  Which model to use",
        "─" * 40,
    ]


def test_layout_records_without_head():
    out = layout_records([], [["a", "b"]], 40)
    assert "Column 1:  a" in out and "Column 2:  b" in out


def test_layout_records_long_value_gets_own_lines():
    url = "https://example.com/" + "segment/" * 6
    out = layout_records([["Name", "Link"]], [["n", url + " trailing words"]], 40)
    lines = out.splitlines()
    i = lines.index("Link:")
    assert lines[i + 1].startswith("  https://")
    assert all(dwidth(l) <= 40 for l in lines)
    assert "".join(l.strip() for l in lines[i + 1:-1]).replace(" ", "") == (url + "trailingwords")


def test_layout_records_empty_value_and_multiline():
    out = layout_records([["A", "B"]], [["", "one\ntwo"]], 40)
    assert "A:" in out.splitlines()
    assert any(l.endswith("one") for l in out.splitlines())
    assert any(l.strip() == "two" for l in out.splitlines())


def test_layout_records_long_header_fits_width():
    head = [["A column header that is much longer than thirty columns", "B"]]
    out = layout_records(head, [["v", "w"]], 30)
    assert all(dwidth(l) <= 30 for l in out.splitlines())


# -- display_url ---------------------------------------------------------------------------------


@pytest.mark.parametrize("url, shown", [
    ("https://x.com/p", "https://x.com/p"),
    ("https://x.com/p?utm_source=a", "https://x.com/p"),
    ("https://x.com/p?utm_source=a&utm_medium=b&UTM_Campaign=c", "https://x.com/p"),
    ("https://x.com/p?id=7&utm_source=a", "https://x.com/p?id=7"),
    ("https://x.com/p?utm_source=a&id=7#frag", "https://x.com/p?id=7#frag"),
    ("https://x.com/p?id=7&page=2", "https://x.com/p?id=7&page=2"),
    ("https://x.com/p#utm_source=a", "https://x.com/p#utm_source=a"),
    ("https://x.com/p?q=1#a?utm_x=1", "https://x.com/p?q=1#a?utm_x=1"),
])
def test_display_url(url, shown):
    assert tx.display_url(url) == shown


def test_display_url_only_whole_utm_parameters():
    assert tx.display_url("https://x.com/p?a=1&notutm_x=2&b=3") == "https://x.com/p?a=1&notutm_x=2&b=3"


# -- links ------------------------------------------------------------------------------------------


@needs_pandoc
def test_cross_manual_ref():
    out = render(f"See [the hooks]({HOOKS}).")
    assert out == "See @ref{Hooks reference,,the hooks,claude-code}.\n"


@needs_pandoc
def test_same_manual_ref_and_anchor():
    assert render(f"[Other]({OTHER}) and [sec]({OTHER}#sec)") == (
        "@ref{Other page,,Other} and @ref{Other page - Sec,,sec}\n")


@needs_pandoc
def test_same_page_link_without_anchor_is_plain_text():
    assert render("Read [this page](#nowhere) and [also this](https://docs.example.com/en/page).") == (
        "Read this page and also this.\n")


@needs_pandoc
def test_same_page_link_with_known_anchor_is_a_ref():
    assert render("Go to [known](#known).") == "Go to @ref{This page - Known,,known}.\n"


@needs_pandoc
def test_numeric_same_page_link_is_a_footnote_marker():
    assert render("DRACO[21](#refs) is cited.") == "DRACO^21 is cited.\n"


@needs_pandoc
def test_spaces_at_link_edges_move_outside():
    out = render(f"invalidating[ an incorrect selection]({OTHER}) now")
    assert out == "invalidating @ref{Other page,,an incorrect selection} now\n"
    out = render(f"word[trailing ]({OTHER})next")
    assert out == "word@ref{Other page,,trailing} next\n"


@needs_pandoc
def test_glued_link_gets_a_space():
    assert render(f"See[JSON-RPC Error]({OTHER})") == "See @ref{Other page,,JSON-RPC Error}\n"
    # Lower-case continuation and non-letters are left alone.
    assert render(f"see[more]({OTHER})") == "see@ref{Other page,,more}\n"
    assert render(f"(see)[Link]({OTHER})") == "(see)@ref{Other page,,Link}\n"


@needs_pandoc
def test_colon_and_comma_in_labels():
    out = render(f"[Step 1: install, then run]({OTHER})")
    assert out == "@ref{Other page,,Step 1∶ install@comma{} then run}\n"


@needs_pandoc
def test_external_links():
    assert render("[site](https://example.org/a?utm_source=x&id=1)") == (
        "@uref{https://example.org/a?id=1,site}\n")
    assert render("<https://example.org/a>") == "@url{https://example.org/a}\n"
    assert render("[https://example.org/a](https://example.org/a?utm_medium=y)") == (
        "@url{https://example.org/a}\n")
    assert render("[example.org/a](https://example.org/a)") == "@url{https://example.org/a}\n"
    assert render("[a, b](https://example.org/x,y)") == "@uref{https://example.org/x@comma{}y,a@comma{} b}\n"


@needs_pandoc
def test_mailto_and_unresolved_fragment():
    assert render("[mail us](mailto:a@example.com)") == "@email{a@@example.com,mail us}\n"
    w = tx.PageWriter("docs", "https://unknown.example.com/p", "P", {}, resolver, lambda s, w: "")
    assert w.inlines([link([S("words")], "#missing")]) == "words"


@needs_pandoc
def test_mailto_autolink_shows_address_once():
    assert render("<mailto:a@example.com>") == "@email{a@@example.com}\n"


def test_strong_note_cannot_start_a_cross_reference():
    w = writer()
    out = w.inline({"t": "Strong", "c": [S("Note:"), SP, S("careful")]})
    assert out == "@strong{​Note: careful}"
    assert w.inline({"t": "Strong", "c": [S("Important")]}) == "@strong{Important}"


@needs_makeinfo
@needs_pandoc
def test_links_through_makeinfo(tmp_path):
    md = (f"See [the hooks]({HOOKS}), [Other]({OTHER}), [sec]({OTHER}#sec), "
          f"See[Glued]({OTHER}), [Step 1: go]({OTHER}), DRACO[21](#refs), "
          f"[site](https://example.org/a?utm_source=x), and [this page](#x).")
    rc, err, info = run_makeinfo(tmp_path, render(md))
    assert rc == 0 and err == ""
    text = top_text(info)
    assert "*note the hooks: (claude-code)Hooks reference" in text
    assert "*note Other: Other page" in text
    assert "*note sec: Other page - Sec" in text
    assert "See *note Glued: Other page" in text
    assert "*note Step 1∶ go: Other page" in text
    assert "DRACO^21" in text
    assert "site (https://example.org/a)" in text
    assert "and this page." in text


# -- line breaks, tables in pages, nesting, anchors ------------------------------------------


def test_linebreak_span_in_paragraph():
    w = writer()
    out = w.blocks([{"t": "Para", "c": [S("one"), LB_SPAN, S("two")]}])
    assert out == "one@*\ntwo\n"
    assert w.inline({"t": "Span", "c": [["", ["other"], []], [S("kept")]]}) == "kept"


@needs_pandoc
def test_linebreak_span_in_table_cell():
    out = render("| a | b |\n|---|---|\n| x[]{.linebreak}y | z |\n")
    rows = grid_cells(out)
    assert rows[1] == ["x", "z"] and rows[2] == ["y", ""]


@needs_pandoc
def test_table_links_are_numbered_refs():
    md = (f"| Name | Ref |\n|---|---|\n| hooks | [Hooks]({HOOKS}) |\n"
          f"| cite | Chartography[13](https://example.org/r) |\n| here | [top](#nowhere) |\n")
    out = render(md)
    assert "Hooks[1]" in out and "Chartography^13[2]" in out
    assert "│ here  │ top" in out
    assert "[1] @ref{Hooks reference,,Hooks,claude-code}" in out
    assert "[2] @uref{https://example.org/r,13}" in out


@needs_pandoc
def test_table_footnote_same_page():
    out = render("| a |\n|---|\n| DRACO[21](#refs) |\n")
    assert "DRACO^21" in out and "[1]" not in out


@needs_pandoc
@pytest.mark.parametrize("md, width", [
    ("```mermaid\ngraph TD; A-->B\n```\n", 73),
    ("> ```mermaid\n> graph TD; A-->B\n> ```\n", 68),
    ("- item\n\n  > ```mermaid\n  > graph TD; A-->B\n  > ```\n", 63),
])
def test_nesting_reduces_diagram_width(md, width):
    widths: list[int] = []
    render(md, writer(widths=widths))
    assert widths == [width]


def test_nesting_has_a_minimum_width():
    widths: list[int] = []
    block = {"t": "CodeBlock", "c": [["", ["mermaid"], []], "graph TD; A-->B"]}
    for _ in range(12):
        block = {"t": "BlockQuote", "c": [block]}
    writer(widths=widths).blocks([block])
    assert widths == [tx.MIN_BLOCK_WIDTH]


@needs_pandoc
def test_nesting_reduces_table_width():
    row = "| " + " | ".join(["word " * 3] * 6) + " |\n"
    md = "| " + " | ".join(f"h{i}" for i in range(6)) + " |\n|" + "---|" * 6 + "\n" + row
    flat = render(md)
    nested = render("> " + md.replace("\n", "\n> "))
    assert max(dwidth(l) for l in flat.splitlines() if "│" in l) <= tx.BLOCK_WIDTH
    widest = max((dwidth(l) for l in nested.splitlines() if "│" in l or "─" in l), default=0)
    assert widest <= tx.BLOCK_WIDTH - tx.INDENT_STEP


@needs_pandoc
def test_duplicate_header_ids_emit_one_anchor():
    w = writer(anchors={"dup": "This page - Dup", "other": "This page - Other"})
    out = render("## Dup {#dup}\n\ntext\n\n## Dup again {#dup}\n\n## Other {#other}\n", w)
    assert out.count("@anchor{This page - Dup}") == 1
    assert out.count("@anchor{This page - Other}") == 1
    assert w.unplaced_anchors() == []


def test_unplaced_anchors_reported():
    w = writer(anchors={"in-cell": "This page - In cell", "head": "This page - Head"})
    w.blocks([{"t": "Header", "c": [2, ["head", [], []], [S("Head")]]}])
    assert w.unplaced_anchors() == ["This page - In cell"]


def test_div_and_code_anchor_once():
    w = writer(anchors={"x": "This page - X"})
    out = w.blocks([
        {"t": "Div", "c": [["x", ["callout"], [["kind", "tip"]]], [{"t": "Para", "c": [S("hi")]}]]},
        {"t": "CodeBlock", "c": [["x", ["python"], []], "print(1)"]},
    ])
    assert out.count("@anchor{This page - X}") == 1
    assert "@quotation Tip" in out and "── python ─" in out


@needs_makeinfo
@needs_pandoc
def test_page_through_makeinfo(tmp_path):
    md = """\
## Setup {#setup}

Install with `npm i -g pkg@latest` -- then run it.

## Setup {#setup}

| Option | Meaning |
|---|---|
| `--verbose` | Print more[]{.linebreak}and more |

> **Note:** keep the `{braces}` and @signs.

1. First
2. Second

```bash
echo "@{}" --flag
```
"""
    w = writer(anchors={"setup": "This page - Setup"})
    w.set_heading_levels([2])
    body = render(md, w)
    rc, err, info = run_makeinfo(tmp_path, body)
    assert rc == 0, err
    assert err == ""
    text = top_text(info)
    assert "Install with ‘npm i -g pkg@latest’ -- then run it." in text
    assert "│ ‘--verbose’ │ Print more │" in info
    assert "│             │ and more   │" in info
    assert "keep the ‘{braces}’ and @signs." in text
    assert 'echo "@{}" --flag' in info
    assert info.count("Setup") >= 2


def test_example_label_rule():
    out = tx.example("code", label="Python")
    assert out.startswith("@example\n── Python ─")
    assert out.endswith("code\n@end example\n")
    assert tx.example("{x}") == "@example\n@{x@}\n@end example\n"


def test_para_and_oneline():
    assert tx.para("  a\n\n\nb  ") == "a\nb\n"
    assert tx.para("   ") == ""
    assert tx.oneline("a @*\nb\n  c") == "a b c"


def test_header_ids_walks_containers():
    blocks = [
        {"t": "Header", "c": [2, ["top", [], []], [S("Top")]]},
        {"t": "Div", "c": [["d", ["tab"], [["title", "Tab A"]]], [
            {"t": "Header", "c": [3, ["inner", [], []], [S("Inner")]]}]]},
        {"t": "BulletList", "c": [[{"t": "CodeBlock", "c": [["c", [], [["title", "T"]]], "x"]}]]},
        {"t": "BlockQuote", "c": [{"t": "Header", "c": [4, ["q", [], []], [S("Q")]]}]},
    ]
    assert tx.header_ids(blocks) == [(2, "top", "Top"), (0, "d", "Tab A"), (3, "inner", "Inner"),
                                     (0, "c", "T"), (4, "q", "Q")]


def test_set_heading_levels():
    w = writer()
    w.set_heading_levels([3, 2, 5, 4, 3])
    assert w._heading_levels == {2: "@heading", 3: "@subheading", 4: "@subsubheading", 5: "@subsubheading"}
