"""Tests for the MCP TypeScript schema pages (schemas.py)."""

import re

import pytest

from claude_info import fetch, http, schemas


def squash(s: str) -> str:
    return re.sub(r"\s+", "", s)


TS = '''/* licence */

import x from "y";

/* Section: JSON-RPC */

/**
 * A request. See {@link Foo} and } in a comment.
 */
export interface Req {
  method: string; // a {brace} in a line comment
  params?: { [key: string]: unknown };
  label: "a } in a string";
}

// a floating comment

/** The id. */
export type Id = string | number;
export const LATEST = "2025-06-18";
export enum Level { A = "a", B = "b" }
// trailing comment
'''


def test_split_is_lossless_and_names_every_declaration():
    pre, decls = schemas.split(TS)
    assert [n for n, _ in decls] == ["Req", "Id", "LATEST", "Level"]
    assert squash("\n".join([pre] + [c for _, c in decls])) == squash(TS)


def test_split_keeps_doc_comment_with_its_declaration():
    _, decls = dict_and(schemas.split(TS))
    assert decls["Req"].startswith("/* Section: JSON-RPC */") or decls["Req"].startswith("/**")
    assert "See {@link Foo}" in decls["Req"]
    assert decls["Req"].rstrip().endswith("}")


def test_braces_in_comments_and_strings_do_not_end_a_declaration():
    _, decls = dict_and(schemas.split(TS))
    assert 'label: "a } in a string";' in decls["Req"]
    assert "params?: { [key: string]: unknown };" in decls["Req"]


def test_floating_and_trailing_comments_are_kept():
    _, decls = dict_and(schemas.split(TS))
    assert "// a floating comment" in decls["Id"]
    assert "// trailing comment" in decls["Level"]


def test_preamble():
    pre, _ = schemas.split(TS)
    assert "licence" in pre and 'import x from "y";' in pre


def dict_and(result):
    pre, decls = result
    return pre, dict(decls)


def test_page_markdown_has_a_section_per_declaration_and_safe_fences():
    ts = TS + 'export type Fence = "```";\n'
    md = schemas.page_markdown("2025-06-18", ts)
    assert md.startswith("# TypeScript schema")
    for name in ["Req", "Id", "LATEST", "Level", "Fence"]:
        assert f"### `{name}`" in md
    # A ``` inside the code forces a longer fence.
    assert "````typescript" in md


class FakeResponse:
    def __init__(self, body, status=200):
        self.body, self.status, self.etag, self.last_modified, self.url = body, status, None, None, ""
        self.content_type = "text/plain"


@pytest.fixture
def mirror(tmp_path, monkeypatch):
    monkeypatch.setattr(schemas, "MIRROR", tmp_path)
    monkeypatch.setattr(schemas, "DIR", tmp_path / "mcp-schema")
    monkeypatch.setattr(schemas, "STATE", tmp_path / ".state")
    for v in ("2025-06-18", "draft"):
        p = tmp_path / "mcp" / "pages" / "specification" / v / "index.md"
        p.parent.mkdir(parents=True)
        p.write_text("x")
    return tmp_path


def test_sync_fetches_every_version(mirror, monkeypatch):
    monkeypatch.setattr(http, "get", lambda url, **kw: FakeResponse(TS.encode()))
    r = schemas.sync(log=lambda *a: None)
    assert r.ok and sorted(r.fetched) == ["2025-06-18", "draft"]
    assert (mirror / "mcp-schema" / "draft" / "schema.ts").read_text() == TS


def test_sync_failure_keeps_last_copy(mirror, monkeypatch):
    monkeypatch.setattr(http, "get", lambda url, **kw: FakeResponse(TS.encode()))
    schemas.sync(log=lambda *a: None)

    def boom(url, **kw):
        raise http.FetchError("HTTP 503")

    monkeypatch.setattr(http, "get", boom)
    r = schemas.sync(log=lambda *a: None)
    assert not r.ok and len(r.errors) == 2
    assert (mirror / "mcp-schema" / "draft" / "schema.ts").read_text() == TS


def test_sync_rejects_a_body_without_declarations(mirror, monkeypatch):
    monkeypatch.setattr(http, "get", lambda url, **kw: FakeResponse(TS.encode()))
    schemas.sync(log=lambda *a: None)
    monkeypatch.setattr(http, "get", lambda url, **kw: FakeResponse(b"<html>rate limited</html>"))
    r = schemas.sync(log=lambda *a: None)
    assert not r.ok
    assert (mirror / "mcp-schema" / "2025-06-18" / "schema.ts").read_text() == TS


def test_sync_removes_versions_no_longer_mirrored(mirror, monkeypatch):
    monkeypatch.setattr(http, "get", lambda url, **kw: FakeResponse(TS.encode()))
    schemas.sync(log=lambda *a: None)
    (mirror / "mcp" / "pages" / "specification" / "draft" / "index.md").unlink()
    (mirror / "mcp" / "pages" / "specification" / "draft").rmdir()
    r = schemas.sync(log=lambda *a: None)
    assert r.removed == ["draft"] and not (mirror / "mcp-schema" / "draft").exists()
