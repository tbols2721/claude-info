"""Tests for claude_info.verify: which source words must survive, diagram
counting, Info node parsing, and end-to-end checks of a built mini site."""

from __future__ import annotations

import json
import re
import shutil
from textwrap import dedent

import pytest

from claude_info import build, verify
from claude_info.verify import count_diagrams, info_nodes, reachable, source_words

pytestmark = pytest.mark.usefixtures("isolated")

needs_tools = pytest.mark.skipif(not (shutil.which("pandoc") and shutil.which("makeinfo")),
                                 reason="pandoc and makeinfo are required")


def words(raw: str) -> dict[str, int]:
    return dict(source_words(raw))


# -- source_words -------------------------------------------------------------------


def test_plain_words_lowercased_and_counted():
    assert words("Hello hello, World_wide 42") == {"hello": 2, "world": 1, "wide": 1, "42": 1}


def test_frontmatter_and_index_boilerplate_ignored():
    raw = dedent("""\
        ---
        title: Front matter words
        ---
        > ## Documentation Index
        > Fetch the complete documentation index at: https://x.example/llms.txt
        > Use this file to discover all available pages before exploring further.

        # Body
        """)
    assert words(raw) == {"body": 1}


def test_mermaid_source_ignored_but_surrounding_text_kept():
    raw = "Before\n\n```mermaid\nsequenceDiagram\n  participant Alice\n```\n\nafter\n"
    assert words(raw) == {"before": 1, "after": 1}
    quoted = "> ~~~mermaid\n> graph TD\n> ~~~\nafter\n"
    assert words(quoted) == {"after": 1}


def test_permalink_and_copy_button_chrome_ignored():
    assert words("`schema` [Permalink](#field-x) value") == {"schema": 1, "value": 1}
    assert words("<pre>echo hi\n`Copy</pre>") == {"echo": 1, "hi": 1}


def test_link_targets_urls_and_reference_ids_ignored():
    raw = 'See [the docs][ref1] and [inline](https://example.com/path "Title words") or https://bare.example/x.\n\n[ref1]: https://example.com/x "Title"\n'
    assert words(raw) == {"see": 1, "the": 1, "docs": 1, "and": 1, "inline": 1, "or": 1}


def test_footnote_ids_ignored_but_footnote_text_kept():
    raw = "Claim[^ts-sdk-resume].\n\n[^ts-sdk-resume]: Footnote text.\n"
    assert words(raw) == {"claim": 1, "footnote": 1, "text": 1}


def test_only_complete_entities_decoded():
    assert words("Go's &params and &amp; &#39;quoted&#39; &#x41;BC &bogus") == {
        "go": 1, "s": 1, "params": 1, "and": 1, "quoted": 1, "abc": 1, "bogus": 1}
    # html.unescape would have turned "&para" into a pilcrow and lost "params".
    assert "params" in words("url?x=1&params=2")


def test_component_attributes_shown_to_the_reader_are_kept():
    raw = ('<Tab title="Python tab">body</Tab> <div title="hidden">x</div> '
           '<img alt="Alt words" src="a.png"/> <Card href="https://x" icon="star" title="Card title">c</Card> '
           '<ParamField path="model" type="string" required>doc</ParamField>')
    w = words(raw)
    for kept in ["python", "tab", "body", "alt", "words", "card", "title", "string", "doc"]:
        assert kept in w, kept
    for dropped in ["hidden", "star", "href", "icon", "src", "png", "required", "path"]:
        assert dropped not in w, dropped


def test_placeholders_jsx_and_heading_ids():
    assert words("Use <your-api-key> here") == {"use": 1, "your": 1, "api": 1, "key": 1, "here": 1}
    assert words("{/* jsx comment */} {'literal'} kept") == {"kept": 1}
    assert words("## Heading {#custom-id}") == {"heading": 1}


def test_fence_info_strings_ignored_but_code_kept():
    assert words('```python title="example.py"\nprint(1)\n```\n') == {"print": 1, "1": 1}
    assert words('- ~~~json filename\n  {"k": 2}\n  ~~~\n') == {"k": 1, "2": 1}


# -- count_diagrams -------------------------------------------------------------------


def test_count_diagrams_top_level_only():
    raw = dedent("""\
        ```mermaid
        graph TD; A-->B
        ```

        ````markdown
        How to write one:
        ```mermaid
        graph TD; quoted
        ```
        ````

        ~~~ mermaid
        graph TD; tilde
        ~~~

        > ```mermaid
        > graph TD; in a quote
        > ```

        ~~~text
        ```mermaid
        inside a tilde fence
        ```
        ~~~

        ```Mermaid
        sequenceDiagram
        ```
        """)
    assert count_diagrams(raw) == 4


def test_count_diagrams_other_languages_and_unclosed():
    assert count_diagrams("```python\nx\n```\n") == 0
    assert count_diagrams("```mermaid-js\nx\n```\n") == 0
    assert count_diagrams("```mermaid\nnever closed\n") == 1
    # A closing fence can't carry an info string, so the mermaid inside stays quoted.
    assert count_diagrams("````md\n```mermaid\n```\n````\n```mermaid\nreal\n```\n") == 1


# -- info parsing ----------------------------------------------------------------------


INFO = (
    "This is t.info, produced by makeinfo.\n\n"
    "\x1f\nFile: t.info,  Node: Top,  Next: A,  Up: (dir)\n\nT\n*\n\n* Menu:\n\n* A::\n* B::   desc\n"
    "\x1f\nFile: t.info,  Node: A,  Next: B,  Up: Top\n\nA text\n\n* Menu:\n\n* A1::\n"
    "\x1f\nFile: t.info,  Node: A1,  Up: A\n\ndeep\n"
    "\x1f\nFile: t.info,  Node: B,  Up: Top\n\nB text\n"
    "\x1f\nFile: t.info,  Node: Orphan,  Up: Top\n\nnobody links here\n"
    "\x1f\nTag Table:\n\x1f\nEnd Tag Table\n"
)


def test_info_nodes_and_reachable(tmp_path):
    f = tmp_path / "t.info"
    f.write_text(INFO)
    nodes = info_nodes(f)
    assert list(nodes) == ["Top", "A", "A1", "B", "Orphan"]
    assert "A text" in nodes["A"] and "deep" not in nodes["A"]
    assert reachable(nodes) == {"Top", "A", "A1", "B"}


# -- end to end ---------------------------------------------------------------------------


@pytest.fixture
def built(site, isolated):
    assert all(build.build(log=lambda *a: None).values())
    return site


def run_verify(source_ids=None):
    logs: list[str] = []
    ok = verify.verify(source_ids, log=logs.append)
    return ok, logs


def edit_info(isolated, manual, fn):
    f = isolated.build / "info" / f"{manual}.info"
    f.write_text(fn(f.read_text(encoding="utf-8")), encoding="utf-8")


@needs_tools
def test_verify_passes_on_a_clean_build(built, isolated):
    ok, logs = run_verify()
    assert ok, logs
    assert logs[0].startswith("code: 5 pages, 0 without a node, 0 unreachable, 0 with missing words")
    assert "diagrams 1/1 drawn: OK" in logs[0]
    assert (isolated.build / "verify-report.tsv").read_text() == "\n"


@needs_tools
def test_verify_reports_a_dropped_word(built, isolated):
    edit_info(isolated, "claude-code", lambda t: t.replace("quokka", "", 1))
    ok, logs = run_verify()
    assert not ok
    assert any(l == "     1 missing in settings.md: quokka" for l in logs), logs
    assert "PROBLEMS" in logs[0] and "1 with missing words (1 words)" in logs[0]
    assert (isolated.build / "verify-report.tsv").read_text() == "code\t1\tsettings.md\tquokka\n"


@needs_tools
def test_verify_counts_repeated_words(built, isolated):
    # "quokka" appears twice on the page; losing one occurrence is a loss.
    edit_info(isolated, "claude-code", lambda t: t.replace("A quokka is", "A is", 1))
    ok, logs = run_verify(["code"])
    assert not ok and "     1 missing in settings.md: quokka" in logs


@needs_tools
def test_verify_word_also_in_a_url_is_still_checked(built, isolated):
    # "settings" occurs 3 times in the source text and once more in the
    # node's "Online: <https://code.claude.com/docs/en/settings>" line.
    def drop_one(text):
        node = text.index("Node: Settings,")
        return text[:node] + text[node:].replace("Settings live", "live", 1)

    edit_info(isolated, "claude-code", drop_one)
    ok, logs = run_verify(["code"])
    assert not ok and any("missing in settings.md: settings" in l for l in logs)


@needs_tools
def test_verify_reports_a_page_without_a_node(built, isolated):
    nodes = json.loads((isolated.build / "nodes.json").read_text())
    del nodes["code/pages/settings.md"]
    del nodes["_urls"]["https://code.claude.com/docs/en/settings"]
    (isolated.build / "nodes.json").write_text(json.dumps(nodes))
    ok, logs = run_verify(["code"])
    assert not ok and "  no node: settings.md" in logs


@needs_tools
def test_verify_reports_a_node_missing_from_the_info_file(built, isolated):
    edit_info(isolated, "claude-code", lambda t: t.replace("Node: Settings,", "Node: Renamed,"))
    ok, logs = run_verify(["code"])
    assert not ok and "  no node: settings.md" in logs


@needs_tools
def test_verify_reports_an_unreachable_node(built, isolated):
    edit_info(isolated, "claude-code", lambda t: re.sub(r"^\* Settings::.*\n", "", t, flags=re.M))
    ok, logs = run_verify(["code"])
    assert not ok and "  unreachable: Settings" in logs


@needs_tools
def test_verify_reports_an_undrawn_diagram(built, isolated):
    edit_info(isolated, "claude-code", lambda t: t.replace("── Diagram", "── Missing"))
    ok, logs = run_verify(["code"])
    assert not ok
    assert "diagrams 0/1 drawn" in logs[0]


@needs_tools
def test_verify_only_selected_sources(built, isolated):
    edit_info(isolated, "claude-code", lambda t: t.replace("quokka", ""))
    ok, logs = run_verify(["platform"])
    assert ok and all(not l.startswith("code:") for l in logs)
