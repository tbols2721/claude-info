"""Tests for claude_info.fetch: discovery, mirroring and failure handling.

http.get is replaced by an in-memory fake web; every path (mirror/, .state/,
redirects.json) points into tmp_path through the ``isolated`` fixture.
"""

from __future__ import annotations

import hashlib
import http.client
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from claude_info import config, fetch
from claude_info import http as h
from claude_info.config import Manual, Source

pytestmark = pytest.mark.usefixtures("isolated")

BASE = "https://docs.example.com/en/"
INDEX = "https://docs.example.com/llms.txt"
SITEMAP = "https://docs.example.com/sitemap.xml"
ALL = Manual("docs", "Docs", "The docs.", ("",))


def make_source(**kw) -> Source:
    args = dict(id="docs", name="Docs", base=BASE, index=INDEX, sitemap=SITEMAP, manuals=(ALL,))
    args.update(kw)
    return Source(**args)


class Web:
    """Fake http.get. Routes map a URL to bytes (200, with an ETag derived
    from the body, answering 304 to a matching If-None-Match), an int status
    (404/410/5xx raise FetchError like the real client), an exception to
    raise, or a Response to return as is. Unknown URLs are 404."""

    def __init__(self):
        self.routes: dict[str, object] = {}
        self.calls: list[tuple[str, str | None]] = []

    @staticmethod
    def etag(body: bytes) -> str:
        return '"' + hashlib.sha256(body).hexdigest()[:12] + '"'

    def __call__(self, url, *, etag=None, last_modified=None, attempts=5, timeout=60):
        self.calls.append((url, etag))
        r = self.routes.get(url, 404)
        if isinstance(r, BaseException):
            raise r
        if isinstance(r, h.Response):
            return r
        if isinstance(r, int):
            if r in (404, 410, 403):
                raise h.FetchError(f"{url}: HTTP {r}")
            raise h.FetchError(f"{url}: failed after {attempts} attempts: HTTP Error {r}")
        tag = self.etag(r)
        if etag == tag:
            return h.Response(url, 304, b"", etag, last_modified, "")
        return h.Response(url, 200, r, tag, None, "text/markdown")

    def urls(self) -> list[str]:
        return [u for u, _ in self.calls]


@pytest.fixture
def web(monkeypatch) -> Web:
    w = Web()
    monkeypatch.setattr(h, "get", w)
    return w


class Clock:
    """Controls fetch's idea of now (for GONE_AFTER and redirect rechecks)."""

    def __init__(self, monkeypatch):
        self.now = datetime(2026, 10, 1, 12, 0, tzinfo=timezone.utc)
        clock = self

        class FakeDateTime(datetime):
            @classmethod
            def now(cls, tz=None):
                return clock.now

        monkeypatch.setattr(fetch, "datetime", FakeDateTime)

    def next_day(self, days: int = 1):
        self.now += timedelta(days=days)


@pytest.fixture
def clock(monkeypatch) -> Clock:
    return Clock(monkeypatch)


def llms(pages: dict[str, str], heading: str = "## Guides", preamble: str = "# Docs\n\n> The docs.\n") -> str:
    lines = [preamble, heading]
    lines += [f"- [{title}]({BASE}{path}.md): About {title.lower()}" for path, title in pages.items()]
    return "\n".join(lines) + "\n"


def sitemap(*urls: str) -> bytes:
    body = "".join(f"<url><loc>{u}</loc></url>" for u in urls)
    return (f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>').encode()


def body(path: str, version: int = 1) -> bytes:
    return f"# {path}\n\nVersion {version} of {path}.\n".encode()


def publish(web: Web, pages: dict[str, str], *, version=None, sitemap_only=(), index_extra=""):
    """Serve an index listing ``pages`` and each page's Markdown."""
    web.routes[INDEX] = (llms(pages) + index_extra).encode()
    web.routes[SITEMAP] = sitemap(*[BASE + p for p in pages], *[BASE + p for p in sitemap_only])
    for p in [*pages, *sitemap_only]:
        web.routes[BASE + p + ".md"] = body(p, (version or {}).get(p, 1))


def numbered(n: int, prefix: str = "page") -> dict[str, str]:
    return {f"{prefix}{i:02d}": f"Page {i}" for i in range(n)}


def manifest(source: Source) -> dict:
    return json.loads((source.mirror / "manifest.json").read_text())


def manifest_paths(source: Source) -> list[str]:
    return [p["path"] for p in manifest(source)["pages"]]


def on_disk(source: Source) -> set[str]:
    return {str(f.relative_to(source.pages_dir)) for f in source.pages_dir.rglob("*.md")}


def quiet(*a, **k):
    pass


def sync(source: Source) -> fetch.SyncReport:
    return fetch.sync_source(source, log=quiet)


# -- page_path ----------------------------------------------------------------


@pytest.mark.parametrize("url, path", [
    (BASE, "index.md"),
    (BASE.rstrip("/"), None),  # not under the base (no trailing slash)
    (BASE + "hooks", "hooks.md"),
    (BASE + "hooks/", "hooks.md"),
    (BASE + "hooks.md", "hooks.md"),
    (BASE + "hooks#events", "hooks.md"),
    (BASE + "hooks?utm_source=x", "hooks.md"),
    (BASE + "agent-sdk/python", "agent-sdk/python.md"),
    (BASE + "models/claude-opus-4.1", "models/claude-opus-4.1.md"),  # a dot is not an extension
    ("https://other.example.com/en/hooks", None),
    ("http://docs.example.com/en/hooks", None),
    (BASE + "llms.txt", None),
    (BASE + "llms-full.txt", None),
    (BASE + "sitemap.xml", None),
    (BASE + "images/diagram.png", None),
    (BASE + "openapi.json", None),
    (BASE + "a/../secret", None),
    (BASE + "../escape", None),
    (BASE + "a/./b", None),
    (BASE + "a//b", None),
    (BASE + "api/python/messages", None),  # excluded below
    (BASE + "api/messages", "api/messages.md"),
])
def test_page_path(url, path):
    source = make_source(exclude=("api/python/",))
    assert fetch.page_path(source, url) == path


def test_page_path_never_escapes_pages_dir():
    source = make_source()
    for url in [BASE + "..", BASE + "../..", BASE + "x/../../y", BASE + "./x", BASE + "x/.."]:
        p = fetch.page_path(source, url)
        assert p is None or ".." not in Path(p).parts, url


# -- parse_index ----------------------------------------------------------------

INDEX_TEXT = f"""\
# Docs

> Summary line.

## Getting started

- [Overview]({BASE}overview.md): What it is
- [Quickstart]({BASE}quickstart.md) - Get going
- [Elsewhere](https://other.example.com/en/x.md): Not ours
- [Text file]({BASE}llms-full.txt): Not a page

### Install

- [Linux]({BASE}install/linux.md) — On Linux
- [Overview again]({BASE}overview.md): Duplicate link

## Reference

- [CLI]({BASE}cli.md)
* [Star bullet]({BASE}star.md): Also a list item
"""


def test_parse_index_nav_titles_descriptions_order():
    pages = fetch.parse_index(make_source(), INDEX_TEXT)
    got = [(p.path, p.title, p.description, p.nav, p.order) for p in pages]
    assert got == [
        ("overview.md", "Overview", "What it is", ["Getting started"], 0),
        ("quickstart.md", "Quickstart", "Get going", ["Getting started"], 1),
        ("install/linux.md", "Linux", "On Linux", ["Getting started", "Install"], 2),
        ("cli.md", "CLI", "", ["Reference"], 3),
        ("star.md", "Star bullet", "Also a list item", ["Reference"], 4),
    ]
    assert all(p.in_index and not p.in_sitemap for p in pages)
    assert all(p.url == BASE + p.path for p in pages)


def test_parse_index_duplicate_link_keeps_first():
    pages = fetch.parse_index(make_source(), INDEX_TEXT)
    overview = [p for p in pages if p.path == "overview.md"]
    assert len(overview) == 1 and overview[0].title == "Overview"


def test_parse_index_start_and_drop():
    text = f"""\
# Platform

## Deutsch

- [Einstieg]({BASE}de-only.md)

## English

### Build with Claude

- [Tool use]({BASE}tool-use.md)

#### Server tools

- [Web search]({BASE}web-search.md)

### API

- [Messages]({BASE}api/messages.md)
"""
    source = make_source(index_start="## English", index_drop=("English",))
    pages = fetch.parse_index(source, text)
    assert [(p.path, p.nav) for p in pages] == [
        ("tool-use.md", ["Build with Claude"]),
        ("web-search.md", ["Build with Claude", "Server tools"]),
        ("api/messages.md", ["API"]),
    ]


def test_parse_index_start_missing_finds_nothing():
    source = make_source(index_start="## English")
    assert fetch.parse_index(source, INDEX_TEXT) == []


def test_parse_index_heading_with_trailing_hashes():
    text = f"## Section ##\n- [A]({BASE}a.md)\n"
    assert fetch.parse_index(make_source(), text)[0].nav == ["Section"]


# -- parse_sitemap ----------------------------------------------------------------


def test_parse_sitemap_filters_to_base_and_sorts():
    data = sitemap(BASE + "b", BASE + "a", "https://other.example.com/x", BASE + "a")
    assert fetch.parse_sitemap(make_source(), data) == [BASE + "a", BASE + "b"]


def test_parse_sitemap_index_follows_children(web):
    web.routes["https://docs.example.com/sm-1.xml"] = sitemap(BASE + "one", BASE + "shared")
    web.routes["https://docs.example.com/sm-2.xml"] = sitemap(BASE + "two", BASE + "shared",
                                                               "https://other.example.com/z")
    index = (b'<?xml version="1.0"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
             b"<sitemap><loc> https://docs.example.com/sm-1.xml </loc></sitemap>"
             b"<sitemap><loc>https://docs.example.com/sm-2.xml</loc></sitemap></sitemapindex>")
    assert fetch.parse_sitemap(make_source(), index) == [BASE + "one", BASE + "shared", BASE + "two"]


def test_parse_sitemap_index_child_failure_raises(web):
    web.routes["https://docs.example.com/sm-1.xml"] = sitemap(BASE + "one")
    web.routes["https://docs.example.com/sm-2.xml"] = 503
    index = (b"<sitemapindex><sitemap><loc>https://docs.example.com/sm-1.xml</loc></sitemap>"
             b"<sitemap><loc>https://docs.example.com/sm-2.xml</loc></sitemap></sitemapindex>")
    with pytest.raises(h.FetchError):
        fetch.parse_sitemap(make_source(), index)


def test_parse_sitemap_index_nested_too_deep(web):
    loop = b"<sitemapindex><sitemap><loc>https://docs.example.com/loop.xml</loc></sitemap></sitemapindex>"
    web.routes["https://docs.example.com/loop.xml"] = loop
    with pytest.raises(fetch.ET.ParseError):
        fetch.parse_sitemap(make_source(), loop)


def test_parse_sitemap_garbage_raises_parse_error():
    with pytest.raises(fetch.ET.ParseError):
        fetch.parse_sitemap(make_source(), b"<html><body>Oops")


# -- small helpers ----------------------------------------------------------------


@pytest.mark.parametrize("text, html", [
    ("<!DOCTYPE html><html>", True),
    ("\n\n  <html lang=en>", True),
    ("<HTML>", True),
    ("# Title\n<html> in prose", False),
    ("<div>component</div>", False),
])
def test_looks_like_html(text, html):
    assert fetch.looks_like_html(text) is html


def test_atomic_write_leaves_no_temp_on_failure(tmp_path, monkeypatch):
    target = tmp_path / "d" / "f.txt"
    fetch.atomic_write(target, b"old")

    def boom(src, dst):
        raise OSError("disk full")

    monkeypatch.setattr(fetch.os, "replace", boom)
    with pytest.raises(OSError):
        fetch.atomic_write(target, b"new")
    assert target.read_bytes() == b"old"
    assert [p.name for p in target.parent.iterdir()] == ["f.txt"]


def test_load_json_defaults(tmp_path):
    assert fetch.load_json(tmp_path / "missing.json", {"d": 1}) == {"d": 1}
    (tmp_path / "bad.json").write_text("{not json")
    assert fetch.load_json(tmp_path / "bad.json", []) == []


def test_canonical_url():
    assert fetch.canonical_url("http://www.docs.example.com/en/a.md?x=1#y") == "https://docs.example.com/en/a"
    assert fetch.canonical_url("https://docs.example.com/en/a///") == "https://docs.example.com/en/a"


def test_print_report():
    import io

    r = fetch.SyncReport("docs", pages=3, added=["a.md"], errors=["boom"], warnings=["hmm"], absent=2)
    buf = io.StringIO()
    fetch.print_report(r, out=buf)
    out = buf.getvalue()
    assert "docs: 3 pages, +1 ~0 -0, 1 errors, 1 warnings, 2 parent pages not in this edition" in out
    assert "  error: boom" in out and "  warning: hmm" in out


# -- sync_source: the normal cycle ---------------------------------------------------


def test_first_sync_adds_everything(web):
    src = make_source()
    publish(web, {"a": "A", "b": "B"}, sitemap_only=("extra",))
    r = sync(src)
    assert r.ok, r.errors
    assert sorted(r.added) == ["a.md", "b.md", "extra.md"]
    assert r.pages == 3 and r.changed == [] and r.removed == []
    assert on_disk(src) == {"a.md", "b.md", "extra.md"}
    assert (src.pages_dir / "a.md").read_bytes() == body("a")
    m = manifest(src)
    assert m["source"] == "docs" and m["base"] == BASE
    pages = {p["path"]: p for p in m["pages"]}
    assert pages["a.md"]["in_index"] and pages["a.md"]["in_sitemap"]
    assert pages["extra.md"]["in_sitemap"] and not pages["extra.md"]["in_index"]
    assert pages["extra.md"]["nav"] == ["Other pages"]
    assert pages["a.md"]["sha256"] == hashlib.sha256(body("a")).hexdigest()
    assert [p["order"] for p in m["pages"]] == [0, 1, 2]
    assert (src.mirror / "llms.txt").read_bytes() == web.routes[INDEX]
    assert (src.mirror / "sitemap.txt").read_text().split() == [BASE + "a", BASE + "b", BASE + "extra"]
    assert (config.STATE / "docs.last-sync").exists()
    validators = json.loads((config.STATE / "docs.validators.json").read_text())
    assert validators["a.md"]["etag"] == Web.etag(body("a"))


def test_second_sync_added_changed_same_removed(web):
    src = make_source()
    pages = numbered(10)
    publish(web, pages)
    sync(src)
    del pages["page09"]
    pages["new"] = "New"
    publish(web, pages, version={"page01": 2})
    web.calls.clear()
    r = sync(src)
    assert r.ok, r.errors
    assert r.added == ["new.md"]
    assert r.changed == ["page01.md"]
    assert r.removed == ["page09.md"]
    assert "page09.md" not in on_disk(src)
    assert (src.pages_dir / "page01.md").read_bytes() == body("page01", 2)
    assert sorted(manifest_paths(src)) == sorted(p + ".md" for p in pages)
    # Unchanged pages were asked for conditionally.
    sent = dict(web.calls)
    assert sent[BASE + "page02.md"] == Web.etag(body("page02"))
    assert sent[BASE + "new.md"] is None


def test_304_keeps_file_and_hash(web):
    src = make_source()
    publish(web, {"a": "A"})
    sync(src)
    before = (src.pages_dir / "a.md").stat().st_mtime_ns
    r = sync(src)
    assert r.ok and r.added == r.changed == r.removed == []
    assert (src.pages_dir / "a.md").stat().st_mtime_ns == before
    assert manifest(src)["pages"][0]["sha256"] == hashlib.sha256(body("a")).hexdigest()


def test_validators_ignored_when_file_missing(web):
    """If someone deletes a mirrored file, a stored ETag must not turn the
    refetch into a 304 with nothing on disk."""
    src = make_source()
    publish(web, {"a": "A"})
    sync(src)
    (src.pages_dir / "a.md").unlink()
    web.calls.clear()
    r = sync(src)
    assert r.ok and r.added == ["a.md"]
    assert dict(web.calls)[BASE + "a.md"] is None


def test_bom_is_stripped(web):
    src = make_source()
    publish(web, {"a": "A"})
    web.routes[BASE + "a.md"] = "﻿# A\n".encode()
    sync(src)
    assert (src.pages_dir / "a.md").read_bytes() == b"# A\n"


def test_nested_dirs_removed_when_empty(web):
    src = make_source()
    pages = {**numbered(9), "deep/er/page": "Deep"}
    publish(web, pages)
    sync(src)
    del pages["deep/er/page"]
    publish(web, pages)
    r = sync(src)
    assert r.removed == ["deep/er/page.md"]
    assert not (src.pages_dir / "deep").exists()


def test_stray_temp_files_are_cleaned(web):
    src = make_source()
    publish(web, {"a": "A"})
    sync(src)
    (src.pages_dir / "sub").mkdir()
    for tmp in [src.mirror / ".tmp-abc", src.pages_dir / ".tmp-def", src.pages_dir / "sub" / ".tmp-x"]:
        tmp.write_text("half written")
    r = sync(src)
    assert r.ok
    assert list(src.mirror.rglob(".tmp-*")) == []


# -- sync_source: discovery failures ----------------------------------------------------


def test_index_failure_changes_nothing(web):
    src = make_source()
    publish(web, numbered(5))
    sync(src)
    snapshot = {p: (src.pages_dir / p).read_bytes() for p in on_disk(src)}
    old_manifest = manifest(src)
    web.routes[INDEX] = 503
    r = sync(src)
    assert not r.ok and r.errors[0].startswith("index:")
    assert {p: (src.pages_dir / p).read_bytes() for p in on_disk(src)} == snapshot
    assert manifest(src) == old_manifest


def test_index_without_links_is_an_error(web):
    src = make_source()
    publish(web, numbered(5))
    sync(src)
    web.routes[INDEX] = b"<!doctype html><html>maintenance</html>"
    r = sync(src)
    assert not r.ok and "no pages found" in r.errors[0]
    assert len(on_disk(src)) == 5


@pytest.mark.parametrize("failure", [503, b"<urlset><url><loc>broken", h.FetchError("boom")])
def test_sitemap_failure_keeps_sitemap_only_pages(web, failure):
    src = make_source()
    publish(web, numbered(3), sitemap_only=("hidden", "also-hidden"))
    sync(src)
    web.routes[SITEMAP] = failure
    r = sync(src)
    assert not r.ok
    assert any(e.startswith("sitemap:") and "keeping the previous sitemap-only pages" in e for e in r.errors)
    assert {"hidden.md", "also-hidden.md"} <= set(manifest_paths(src))
    assert {"hidden.md", "also-hidden.md"} <= on_disk(src)
    assert r.removed == []
    hidden = next(p for p in manifest(src)["pages"] if p["path"] == "hidden.md")
    assert hidden["in_sitemap"]
    # And again the next day: still kept.
    r = sync(src)
    assert {"hidden.md", "also-hidden.md"} <= on_disk(src)


def test_sitemap_failure_still_fetches_sitemap_only_pages(web):
    src = make_source()
    publish(web, numbered(3), sitemap_only=("hidden",))
    sync(src)
    web.routes[SITEMAP] = 500
    web.routes[BASE + "hidden.md"] = body("hidden", 2)
    r = sync(src)
    assert r.changed == ["hidden.md"]


def test_page_dropped_from_sitemap_is_removed(web):
    src = make_source()
    publish(web, numbered(9), sitemap_only=("hidden",))
    sync(src)
    publish(web, numbered(9))
    r = sync(src)
    assert r.ok and r.removed == ["hidden.md"]


def test_empty_sitemap_keeps_sitemap_only_pages(web):
    src = make_source()
    publish(web, numbered(9), sitemap_only=("hidden",))
    sync(src)
    web.routes[SITEMAP] = sitemap(*["https://www.docs.example.com/en/" + p for p in numbered(9)],
                                  "https://www.docs.example.com/en/hidden")
    sync(src)
    assert "hidden.md" in on_disk(src)


def test_sitemap_unknown_encoding_does_not_crash(web):
    src = make_source()
    publish(web, numbered(3))
    web.routes[SITEMAP] = b'<?xml version="1.0" encoding="x-bogus"?><urlset/>'
    r = sync(src)
    assert not r.ok


# -- sync_source: page failures ------------------------------------------------------------


@pytest.mark.parametrize("exc", [
    http.client.IncompleteRead(b"half", 100),
    RuntimeError("unexpected"),
    KeyError("weird"),
    h.FetchError("https://docs.example.com/en/page01.md: failed after 5 attempts: timed out"),
])
def test_fetch_exception_keeps_last_good_copy(web, exc):
    src = make_source()
    publish(web, numbered(5))
    sync(src)
    web.routes[BASE + "page01.md"] = exc
    r = sync(src)
    assert not r.ok
    assert len(r.errors) == 1 and "page01.md" in r.errors[0]
    assert (src.pages_dir / "page01.md").read_bytes() == body("page01")
    assert "page01.md" in manifest_paths(src)
    entry = next(p for p in manifest(src)["pages"] if p["path"] == "page01.md")
    assert entry["sha256"] == hashlib.sha256(body("page01")).hexdigest()
    assert r.removed == [] and r.pages == 5


def test_exception_type_named_in_error(web):
    src = make_source()
    publish(web, {"a": "A"})
    web.routes[BASE + "a.md"] = http.client.IncompleteRead(b"half", 100)
    r = sync(src)
    assert r.errors == [f"{BASE}a.md: IncompleteRead: IncompleteRead(4 bytes read, 100 more expected)"]


def test_new_page_failing_is_reported_not_added(web):
    src = make_source()
    publish(web, {"a": "A", "b": "B"})
    web.routes[BASE + "b.md"] = RuntimeError("boom")
    r = sync(src)
    assert r.added == ["a.md"] and len(r.errors) == 1
    assert manifest_paths(src) == ["a.md"]


def test_failed_sync_does_not_update_last_sync(web, clock):
    src = make_source()
    publish(web, {"a": "A"})
    sync(src)
    first = (config.STATE / "docs.last-sync").read_text()
    clock.next_day()
    web.routes[BASE + "a.md"] = 500
    sync(src)
    assert (config.STATE / "docs.last-sync").read_text() == first


@pytest.mark.parametrize("bad, why", [
    (b"<!DOCTYPE html><html><body>Not found</body></html>", "got HTML instead of Markdown"),
    (b"  \n<html><head></head></html>", "got HTML instead of Markdown"),
    (b"", "empty body"),
    (b"  \n\t\n", "empty body"),
    (b"\xef\xbb\xbf", "empty body"),
    (b"# Title\n\xff\xfe broken", "not valid UTF-8"),
])
def test_bad_bodies_rejected_and_last_copy_kept(web, bad, why):
    src = make_source()
    publish(web, numbered(5))
    sync(src)
    web.routes[BASE + "page02.md"] = bad
    r = sync(src)
    assert len(r.errors) == 1 and why in r.errors[0]
    assert (src.pages_dir / "page02.md").read_bytes() == body("page02")
    assert "page02.md" in manifest_paths(src)
    # The bad body's validators are not stored, so the next run refetches fully.
    validators = json.loads((config.STATE / "docs.validators.json").read_text())
    assert validators["page02.md"]["etag"] == Web.etag(body("page02"))


@pytest.mark.parametrize("bad", [b"<!doctype html><p>x", b"", b"\xff"])
def test_bad_body_for_new_page_is_not_written(web, bad):
    src = make_source()
    publish(web, {"a": "A"})
    web.routes[BASE + "a.md"] = bad
    r = sync(src)
    assert not r.ok and not (src.pages_dir / "a.md").exists()


# -- sync_source: pages that 404 -------------------------------------------------------


def test_gone_page_kept_until_missing_on_gone_after_days(web, clock):
    assert fetch.GONE_AFTER == 3
    src = make_source()
    publish(web, numbered(10))
    sync(src)
    web.routes[BASE + "page03.md"] = 404

    r = sync(src)  # day 1
    assert r.ok and r.removed == []
    assert "missing 1 of 3 days" in r.warnings[0]
    assert "page03.md" in on_disk(src) and "page03.md" in manifest_paths(src)

    r = sync(src)  # day 1 again: not counted twice
    assert "missing 1 of 3 days" in r.warnings[0] and r.removed == []
    misses = json.loads((config.STATE / "docs.misses.json").read_text())
    assert misses["page03.md"]["days"] == 1

    clock.next_day()
    r = sync(src)  # day 2
    assert "missing 2 of 3 days" in r.warnings[0] and r.removed == []

    clock.next_day()
    r = sync(src)  # day 3: removed
    assert r.removed == ["page03.md"]
    assert "missing 3 days in a row; removing" in r.warnings[0]
    assert "page03.md" not in on_disk(src) and "page03.md" not in manifest_paths(src)
    misses = json.loads((config.STATE / "docs.misses.json").read_text())
    assert "page03.md" not in misses


def test_gone_count_resets_when_page_returns(web, clock):
    src = make_source()
    publish(web, numbered(10))
    sync(src)
    web.routes[BASE + "page03.md"] = 410
    sync(src)
    clock.next_day()
    sync(src)
    clock.next_day()
    web.routes[BASE + "page03.md"] = body("page03")  # back
    r = sync(src)
    assert r.warnings == []
    clock.next_day()
    web.routes[BASE + "page03.md"] = 404
    r = sync(src)
    assert "missing 1 of 3 days" in r.warnings[0]
    assert "page03.md" in on_disk(src)


def test_never_served_indexed_page_is_an_error(web):
    src = make_source()
    publish(web, {"a": "A", "b": "B"})
    web.routes[BASE + "b.md"] = 404
    r = sync(src)
    assert not r.ok and any("HTTP 404" in e for e in r.errors)
    assert manifest_paths(src) == ["a.md"]


def test_never_served_sitemap_only_page_is_a_warning(web):
    src = make_source()
    publish(web, {"a": "A"}, sitemap_only=("ghost",))
    web.routes[BASE + "ghost.md"] = 404
    r = sync(src)
    assert r.ok and any("ghost.md" in w for w in r.warnings)


# -- sync_source: the shrink guard ---------------------------------------------------------


def test_shrink_guard_whole_source(web):
    src = make_source()
    pages = numbered(10)
    publish(web, pages)
    sync(src)
    publish(web, dict(list(pages.items())[:7]))  # 70% of the pages left
    r = sync(src)
    assert not r.ok
    assert any("page count fell from 10 to 7" in e and "not deleting 3 pages" in e for e in r.errors)
    assert len(on_disk(src)) == 10 and r.removed == []
    assert sorted(manifest_paths(src)) == sorted(p + ".md" for p in pages)
    # Kept pages keep their metadata from the last good manifest.
    entry = next(p for p in manifest(src)["pages"] if p["path"] == "page09.md")
    assert entry["title"] == "Page 9" and entry["nav"] == ["Guides"]


def test_shrink_guard_allows_small_drop(web):
    src = make_source()
    pages = numbered(10)
    publish(web, pages)
    sync(src)
    publish(web, dict(list(pages.items())[:8]))  # exactly 80%: allowed
    r = sync(src)
    assert r.ok and len(r.removed) == 2


def test_shrink_guard_single_manual(web):
    api = Manual("api", "API", "API reference.", ("api/",))
    src = make_source(manuals=(api, ALL))
    pages = {**numbered(40), **numbered(5, "api/endpoint")}
    publish(web, pages)
    sync(src)
    del pages["api/endpoint03"], pages["api/endpoint04"]  # 3 of 5: 43 of 45 overall
    publish(web, pages)
    r = sync(src)
    assert not r.ok
    assert any("manual api fell from 5 to 3 pages" in e for e in r.errors)
    assert {"api/endpoint03.md", "api/endpoint04.md"} <= on_disk(src)
    assert {"api/endpoint03.md", "api/endpoint04.md"} <= set(manifest_paths(src))


def test_shrink_guard_counts_disk_without_manifest(web):
    """No manifest (deleted, or first run with files present): the files on
    disk are the baseline."""
    src = make_source()
    pages = numbered(10)
    publish(web, pages)
    sync(src)
    (src.mirror / "manifest.json").unlink()
    publish(web, dict(list(pages.items())[:5]))
    r = sync(src)
    assert not r.ok and len(on_disk(src)) == 10
    assert len(manifest_paths(src)) == 10


def test_shrinkage_function():
    src = make_source()
    prev = [{"path": f"p{i}.md"} for i in range(10)]
    assert fetch.shrinkage(src, prev, {f"p{i}.md" for i in range(8)}) is None
    assert "fell from 10 to 7" in fetch.shrinkage(src, prev, {f"p{i}.md" for i in range(7)})
    assert fetch.shrinkage(src, [], set()) is None
    small = Manual("small", "S", "", ("s/",))
    src2 = make_source(manuals=(small, ALL))
    big = [{"path": f"p{i}.md"} for i in range(40)]
    prev2 = big + [{"path": f"s/{i}.md"} for i in range(4)]
    # Manuals under 5 pages are not guarded on their own.
    assert fetch.shrinkage(src2, prev2, {p["path"] for p in big}) is None
    prev3 = big + [{"path": f"s/{i}.md"} for i in range(5)]
    assert "manual small fell from 5 to 0" in fetch.shrinkage(src2, prev3, {p["path"] for p in big})


# -- derived editions --------------------------------------------------------------------


PARENT_BASE = "https://docs.example.com/en/"
PY_BASE = "https://docs.example.com/en/api/python/"


@pytest.fixture
def editions(web, monkeypatch):
    parent = make_source(id="platform", exclude=("api/python/",))
    child = Source(id="api-python", name="Python", base=PY_BASE, derive_from="platform",
                   derive_prefix="api/", manuals=(Manual("api-python", "Py", "d", ("",)),))
    monkeypatch.setattr(config, "load_sources", lambda path=None: [parent, child])
    publish(web, {"overview": "Overview", "api/messages": "Messages", "api/models": "Models",
                  "api/admin": "Admin"})
    assert sync(parent).ok
    return parent, child


def test_discover_derived_from_parent(editions, web):
    parent, child = editions
    web.routes[PY_BASE + "messages.md"] = b"# messages.create()\n"
    web.routes[PY_BASE + "models.md"] = b"# models.list()\n"
    # api/admin has no Python edition: 404, which is expected, not an error.
    r = sync(child)
    assert r.ok, r.errors
    assert sorted(r.added) == ["messages.md", "models.md"]
    assert r.absent == 1 and r.warnings == []
    m = {p["path"]: p for p in manifest(child)["pages"]}
    assert m["messages.md"]["title"] == "Messages" and m["messages.md"]["nav"] == ["Guides"]
    assert m["messages.md"]["url"] == PY_BASE + "messages.md"
    assert not m["messages.md"]["in_index"]


def test_derived_linked_only_page(editions, web, isolated):
    parent, child = editions
    isolated.redirects.write_text(json.dumps({
        "https://docs.example.com/en/api/python/beta-only": PY_BASE + "beta/files",
        "https://docs.example.com/en/old": None,
        "https://elsewhere.example.org/x": "https://elsewhere.example.org/y",
    }))
    web.routes[PY_BASE + "messages.md"] = b"# m\n"
    web.routes[PY_BASE + "beta/files.md"] = b"# files\n"
    r = sync(child)
    m = {p["path"]: p for p in manifest(child)["pages"]}
    assert "beta/files.md" in r.added
    assert m["beta/files.md"]["linked"] and m["beta/files.md"]["nav"] == ["Other pages"]


def test_derived_linked_page_that_404s_is_a_warning(editions, web, isolated):
    parent, child = editions
    isolated.redirects.write_text(json.dumps({"https://x": PY_BASE + "dead"}))
    r = sync(child)
    assert r.ok and any("dead.md" in w for w in r.warnings)


def test_derived_unknown_parent(web, monkeypatch):
    child = Source(id="kid", name="Kid", base=PY_BASE, derive_from="nope", manuals=(ALL,))
    monkeypatch.setattr(config, "load_sources", lambda path=None: [child])
    r = sync(child)
    assert r.errors == ["derive_from: unknown source 'nope'"]
    assert not child.mirror.exists() or not (child.mirror / "manifest.json").exists()


def test_derived_parent_not_synced(web, monkeypatch):
    parent = make_source(id="platform")
    child = Source(id="kid", name="Kid", base=PY_BASE, derive_from="platform", manuals=(ALL,))
    monkeypatch.setattr(config, "load_sources", lambda path=None: [parent, child])
    r = sync(child)
    assert r.errors == ["derive_from: platform has not been synced"]


# -- linked_only via redirects ---------------------------------------------------------------


def test_linked_only_pages_are_fetched(web, isolated):
    src = make_source()
    isolated.mirror.mkdir(parents=True, exist_ok=True)
    isolated.redirects.write_text(json.dumps({
        "https://docs.example.com/en/old-name": BASE + "secret-page",
        "https://docs.example.com/en/a-alias": BASE + "a",  # already listed
        "https://docs.example.com/en/dead": None,
    }))
    publish(web, {"a": "A"})
    web.routes[BASE + "secret-page.md"] = b"# Secret\n"
    r = sync(src)
    assert r.ok and sorted(r.added) == ["a.md", "secret-page.md"]
    m = {p["path"]: p for p in manifest(src)["pages"]}
    assert m["secret-page.md"]["linked"] and not m["secret-page.md"]["in_index"]
    assert not m["a.md"]["linked"]


def test_linked_only_ignores_corrupt_redirects(web, isolated):
    src = make_source()
    isolated.mirror.mkdir(parents=True, exist_ok=True)
    isolated.redirects.write_text("{oops")
    publish(web, {"a": "A"})
    assert sync(src).ok


# -- sync_redirects ---------------------------------------------------------------------------


@pytest.fixture
def linking_site(web, isolated, monkeypatch):
    src = make_source()
    publish(web, {"a": "A", "b": "B"})
    web.routes[BASE + "a.md"] = (
        "# A\n\nSee [moved](https://docs.example.com/en/moved), "
        "[legacy](https://docs.anthropic.com/en/docs/old-thing#frag), "
        "[broken](http://www.docs.example.com/en/broken.md).\n"
        "Also [b](https://docs.example.com/en/b) and [x](https://unrelated.example.org/en/z).\n"
        "Trailing punctuation: https://docs.example.com/en/punct.\n"
    ).encode()
    assert sync(src).ok
    final = {
        "https://docs.example.com/en/moved": BASE + "new-home",
        "https://docs.anthropic.com/en/docs/old-thing": "https://docs.example.com/en/thing/",
        "https://docs.example.com/en/punct": BASE + "punct",
    }
    calls: list[str] = []

    def get(url, **kw):
        calls.append(url)
        if url in final:
            return h.Response(final[url], 200, b"", None, None, "")
        raise h.FetchError(f"{url}: HTTP 404")

    monkeypatch.setattr(h, "get", get)
    return src, calls, final


def test_sync_redirects_records_final_urls(linking_site, isolated):
    src, calls, _ = linking_site
    known = fetch.sync_redirects([src], log=quiet)
    assert known == {
        "https://docs.anthropic.com/en/docs/old-thing": "https://docs.example.com/en/thing",
        "https://docs.example.com/en/broken": None,
        "https://docs.example.com/en/moved": "https://docs.example.com/en/new-home",
        "https://docs.example.com/en/punct": "https://docs.example.com/en/punct",
    }
    assert json.loads(isolated.redirects.read_text()) == known
    # Mirrored pages and other hosts are not looked up.
    assert "https://docs.example.com/en/b" not in calls
    assert not any("unrelated" in c for c in calls)


def test_sync_redirects_retries_failures_only(linking_site, clock):
    src, calls, final = linking_site
    fetch.sync_redirects([src], log=quiet)
    calls.clear()
    clock.next_day()
    final["https://docs.example.com/en/broken"] = BASE + "fixed"
    known = fetch.sync_redirects([src], log=quiet)
    assert calls == ["https://docs.example.com/en/broken"]
    assert known["https://docs.example.com/en/broken"] == "https://docs.example.com/en/fixed"


def test_sync_redirects_rechecks_week_old_answers(linking_site, clock):
    src, calls, final = linking_site
    fetch.sync_redirects([src], log=quiet)
    calls.clear()
    clock.next_day(fetch.RECHECK_DAYS + 1)
    final["https://docs.example.com/en/moved"] = BASE + "moved-again"
    known = fetch.sync_redirects([src], log=quiet)
    assert "https://docs.example.com/en/moved" in calls
    assert known["https://docs.example.com/en/moved"] == "https://docs.example.com/en/moved-again"


def test_sync_redirects_drops_urls_no_longer_linked(linking_site, web, isolated):
    src, calls, _ = linking_site
    fetch.sync_redirects([src], log=quiet)
    (src.pages_dir / "a.md").write_text("# A\n\nOnly [moved](https://docs.example.com/en/moved).\n")
    known = fetch.sync_redirects([src], log=quiet)
    assert list(known) == ["https://docs.example.com/en/moved"]


def test_sync_redirects_follow_exception_is_none(linking_site, monkeypatch):
    src, calls, _ = linking_site

    def explode(url, **kw):
        raise http.client.IncompleteRead(b"", 1)

    monkeypatch.setattr(h, "get", explode)
    known = fetch.sync_redirects([src], log=quiet)
    assert set(known.values()) == {None}
