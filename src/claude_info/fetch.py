"""Discover every page of each source and mirror its Markdown locally.

Layout per source (all committed to git, so `git log -p mirror/` is a
changelog of the upstream docs):

    mirror/<id>/llms.txt        raw index as published
    mirror/<id>/sitemap.txt     sorted page URLs from sitemap.xml
    mirror/<id>/manifest.json   every page: path, url, title, nav, sha256
    mirror/<id>/pages/...       one .md file per page, exactly as served

HTTP validators (ETag / Last-Modified) live in .state/, outside git.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import http
from .config import MIRROR, STATE, Source

# A source whose page count drops below this fraction of the previous sync is
# treated as a broken upstream index: nothing is deleted.
SHRINK_GUARD = 0.8
# A mirrored page that starts returning 404 is kept until it has been missing
# on this many days in a row.
GONE_AFTER = 3
WORKERS = 8

HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
LINK = re.compile(
    r"^\s*[-*]\s+\[(?P<title>.*?)\]\((?P<url>https?://[^\s)]+)\)"
    r"(?:\s*(?::|\s-\s|\s—\s)\s*(?P<desc>.*?))?\s*$"
)


@dataclass
class Page:
    path: str
    url: str
    title: str = ""
    description: str = ""
    nav: list[str] = field(default_factory=list)
    order: int = 0
    in_index: bool = False
    in_sitemap: bool = False
    linked: bool = False  # found only through a redirected link
    sha256: str = ""


@dataclass
class SyncReport:
    source: str
    pages: int = 0
    added: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    absent: int = 0  # derived candidates with no page in this edition (expected)

    @property
    def ok(self) -> bool:
        return not self.errors


def page_path(source: Source, url: str) -> str | None:
    """Mirror-relative path of a page URL, or None if it is outside the source."""
    url = url.split("#", 1)[0].split("?", 1)[0]
    if not url.startswith(source.base):
        return None
    rel = url[len(source.base) :].strip("/")
    if not rel:
        rel = "index"
    last = rel.rsplit("/", 1)[-1]
    if "." in last and not last.endswith(".md") and re.search(r"\.[a-z0-9]{2,5}$", last):
        return None  # a file such as llms.txt or an image, not a page
    if not rel.endswith(".md"):
        rel += ".md"
    parts = rel.split("/")
    if any(p in ("", ".", "..") for p in parts):
        return None
    if any(rel.startswith(x) for x in source.exclude):
        return None
    return rel


def parse_index(source: Source, text: str) -> list[Page]:
    pages: dict[str, Page] = {}
    stack: list[tuple[int, str]] = []
    started = source.index_start is None
    for line in text.splitlines():
        if not started:
            started = line.strip() == source.index_start
            continue
        if m := HEADING.match(line):
            level, title = len(m.group(1)), m.group(2).strip()
            if level == 1 or title in source.index_drop:
                continue
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
            continue
        if m := LINK.match(line):
            path = page_path(source, m.group("url"))
            if path is None or path in pages:
                continue
            pages[path] = Page(
                path=path,
                url=source.base + path,
                title=m.group("title").strip(),
                description=(m.group("desc") or "").strip(),
                nav=[t for _, t in stack],
                order=len(pages),
                in_index=True,
            )
    return list(pages.values())


def parse_sitemap(source: Source, data: bytes, depth: int = 0) -> list[str]:
    """Page URLs under the source's base. A <sitemapindex> is followed into
    its child sitemaps; a child that fails raises, so the caller can tell a
    partial sitemap from a complete one."""
    root = ET.fromstring(data)
    locs = [el.text.strip() for el in root.iter() if el.tag.endswith("loc") and el.text]
    if root.tag.endswith("sitemapindex"):
        if depth >= 2:
            raise ET.ParseError("sitemap index nested too deeply")
        out: set[str] = set()
        for child in locs:
            out |= set(parse_sitemap(source, http.get(child).body, depth + 1))
        return sorted(out)
    return sorted({loc for loc in locs if loc.startswith(source.base)})


def looks_like_html(text: str) -> bool:
    head = text.lstrip()[:200].lower()
    return head.startswith("<!doctype html") or head.startswith("<html")


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.chmod(tmp, 0o644)  # mkstemp creates 0600
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def discover_derived(source: Source, report: SyncReport) -> list[Page] | None:
    """Pages of an edition that no index lists: one candidate per page of the
    parent source under derive_prefix, keeping the parent's navigation. Pages
    that only exist in this edition are found through links (sync_redirects)."""
    from .config import load_sources

    parent = next((s for s in load_sources() if s.id == source.derive_from), None)
    if parent is None:
        report.errors.append(f"derive_from: unknown source {source.derive_from!r}")
        return None
    manifest = load_json(parent.mirror / "manifest.json", {}).get("pages", [])
    if not manifest:
        report.errors.append(f"derive_from: {parent.id} has not been synced")
        return None
    pages: dict[str, Page] = {}
    for p in manifest:
        if not p["path"].startswith(source.derive_prefix):
            continue
        rel = p["path"][len(source.derive_prefix):]
        pages[rel] = Page(
            path=rel, url=source.base + rel, title=p["title"],
            description=p["description"], nav=list(p["nav"]), order=p["order"],
        )
    for path in linked_only(source, pages):
        pages[path] = Page(path=path, url=source.base + path, nav=["Other pages"],
                           order=len(pages) + 10_000, linked=True)
    return sorted(pages.values(), key=lambda p: p.order)


def discover(source: Source, report: SyncReport) -> list[Page] | None:
    if source.derive_from:
        return discover_derived(source, report)
    try:
        index = http.get(source.index)
    except http.FetchError as e:
        report.errors.append(f"index: {e}")
        return None
    index_text = index.body.decode("utf-8", errors="replace")
    pages = parse_index(source, index_text)
    if not pages:
        report.errors.append("index: no pages found (format changed?)")
        return None
    atomic_write(source.mirror / "llms.txt", index.body)

    by_path = {p.path: p for p in pages}
    locs: list[str] = []
    if source.sitemap:
        previous = load_json(source.mirror / "manifest.json", {}).get("pages", [])
        before = [source.base + p["path"] for p in previous if p.get("in_sitemap")]
        index_before = sum(1 for p in previous if p.get("in_index"))
        try:
            locs = parse_sitemap(source, http.get(source.sitemap).body)
            index_steady = len(pages) >= SHRINK_GUARD * index_before
            if before and index_steady and len(locs) < SHRINK_GUARD * len(before):
                # Parsed, but most pages vanished (e.g. URLs moved to another
                # host): as untrustworthy as a failed fetch.
                raise ET.ParseError(f"lists {len(locs)} pages under {source.base}, was {len(before)}")
            atomic_write(source.mirror / "sitemap.txt", ("\n".join(locs) + "\n").encode())
        except Exception as e:  # FetchError, ParseError, LookupError (bad encoding), ...
            # Without the sitemap, sitemap-only pages would look deleted.
            # Carry them over from the last sync instead.
            report.errors.append(f"sitemap: {e}; keeping the previous sitemap-only pages")
            locs = before
    extra = []
    for loc in locs:
        path = page_path(source, loc)
        if path is None:
            continue
        if path in by_path:
            by_path[path].in_sitemap = True
        else:
            extra.append(path)
    for path in sorted(set(extra)):
        by_path[path] = Page(
            path=path,
            url=source.base + path,
            nav=["Other pages"],
            order=len(by_path),
            in_sitemap=True,
        )
    for path in linked_only(source, by_path):
        by_path[path] = Page(
            path=path,
            url=source.base + path,
            nav=["Other pages"],
            order=len(by_path),
            linked=True,
        )
    return sorted(by_path.values(), key=lambda p: p.order)


def linked_only(source: Source, known: dict[str, Page]) -> list[str]:
    """Pages that other pages link to (via a redirect) but that neither the
    index nor the sitemap lists."""
    out = set()
    for final in load_json(REDIRECTS, {}).values():
        if final and (path := page_path(source, final)) and path not in known:
            out.add(path)
    return sorted(out)


def fetch_page(source: Source, page: Page, validators: dict) -> tuple[str, str | None]:
    """Fetch one page. Returns (status, message) where status is
    added / changed / same / error / gone. Never raises."""
    try:
        return _fetch_page(source, page, validators)
    except Exception as e:  # one bad page must not abort the whole sync
        return "error", f"{page.url}: {type(e).__name__}: {e}"


def _fetch_page(source: Source, page: Page, validators: dict) -> tuple[str, str | None]:
    dest = source.pages_dir / page.path
    v = validators.get(page.path, {}) if dest.exists() else {}
    try:
        r = http.get(page.url, etag=v.get("etag"), last_modified=v.get("last_modified"))
    except http.FetchError as e:
        if "HTTP 404" in str(e) or "HTTP 410" in str(e):
            return "gone", str(e)
        return "error", str(e)
    if r.status == 304:
        page.sha256 = hashlib.sha256(dest.read_bytes()).hexdigest()
        return "same", None
    try:
        text = r.body.decode("utf-8").lstrip("﻿")
    except UnicodeDecodeError as e:
        return "error", f"{page.url}: body is not valid UTF-8 ({e})"
    if not text.strip():
        return "error", f"{page.url}: empty body"
    if looks_like_html(text):
        return "error", f"{page.url}: got HTML instead of Markdown"
    data = text.encode("utf-8")
    page.sha256 = hashlib.sha256(data).hexdigest()
    validators[page.path] = {"etag": r.etag, "last_modified": r.last_modified}
    if dest.exists():
        if dest.read_bytes() == data:
            return "same", None
        atomic_write(dest, data)
        return "changed", None
    atomic_write(dest, data)
    return "added", None


def sync_source(source: Source, log=print) -> SyncReport:
    report = SyncReport(source.id)
    for tmp in source.mirror.rglob(".tmp-*") if source.mirror.exists() else []:
        tmp.unlink()  # left behind by an interrupted run
    pages = discover(source, report)
    if pages is None:
        return report

    manifest_path = source.mirror / "manifest.json"
    previous = load_json(manifest_path, {}).get("pages", [])
    validators = load_json(STATE / f"{source.id}.validators.json", {})
    misses = load_json(STATE / f"{source.id}.misses.json", {})

    log(f"{source.id}: {len(pages)} candidate pages "
        f"({sum(p.in_index for p in pages)} indexed, "
        f"{sum(p.in_sitemap and not p.in_index for p in pages)} sitemap-only, "
        f"{sum(p.linked for p in pages)} found through links)")

    with ThreadPoolExecutor(WORKERS) as pool:
        results = list(pool.map(lambda p: fetch_page(source, p, validators), pages))

    kept: list[Page] = []
    for page, (status, message) in zip(pages, results):
        dest = source.pages_dir / page.path
        if status == "gone":
            if dest.exists():
                # A page we have that now 404s: could be a hiccup upstream.
                # Keep it until it has been missing GONE_AFTER days in a row.
                # Counted once per day: a run may sync a source more than once.
                today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                miss = misses.get(page.path) or {"days": 0, "last": ""}
                if miss["last"] != today:
                    miss = {"days": miss["days"] + 1, "last": today}
                misses[page.path] = miss
                if miss["days"] < GONE_AFTER:
                    report.warnings.append(f"{message} (missing {miss['days']} of {GONE_AFTER} days); keeping last copy")
                    page.sha256 = hashlib.sha256(dest.read_bytes()).hexdigest()
                    kept.append(page)
                else:
                    report.warnings.append(f"{message}: missing {GONE_AFTER} days in a row; removing")
                continue
            # Listed but never served. A derived candidate that 404s is a page
            # this edition simply doesn't have; an indexed one is worth flagging.
            if source.derive_from and not page.linked:
                report.absent += 1
            else:
                (report.errors if page.in_index else report.warnings).append(message)
            continue
        misses.pop(page.path, None)
        if status == "error":
            report.errors.append(message)
            if dest.exists():  # keep the last good copy
                page.sha256 = hashlib.sha256(dest.read_bytes()).hexdigest()
                kept.append(page)
            continue
        if status == "added":
            report.added.append(page.path)
        elif status == "changed":
            report.changed.append(page.path)
        kept.append(page)

    live = {p.path for p in kept}
    on_disk = {
        str(f.relative_to(source.pages_dir))
        for f in source.pages_dir.rglob("*.md")
    } if source.pages_dir.exists() else set()
    stale = sorted(on_disk - live)
    shrunk = shrinkage(source, previous or [{"path": p} for p in on_disk], live)
    if shrunk:
        report.errors.append(
            f"{shrunk}; not deleting {len(stale)} pages (upstream index may be broken)"
        )
        old = {p["path"]: p for p in previous}
        for path in stale:
            page = Page(**old[path]) if path in old else Page(path=path, url=source.base + path, nav=["Other pages"], order=10**6)
            kept.append(page)
    else:
        for path in stale:
            (source.pages_dir / path).unlink()
            report.removed.append(path)
            misses.pop(path, None)
        for d in sorted(source.pages_dir.rglob("*"), reverse=True) if source.pages_dir.exists() else []:
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()

    for i, page in enumerate(sorted(kept, key=lambda p: p.order)):
        page.order = i
    report.pages = len(kept)
    manifest = {
        "source": source.id,
        "base": source.base,
        "pages": [asdict(p) for p in sorted(kept, key=lambda p: p.order)],
    }
    atomic_write(manifest_path, (json.dumps(manifest, indent=1, ensure_ascii=False) + "\n").encode())
    STATE.mkdir(parents=True, exist_ok=True)
    atomic_write(STATE / f"{source.id}.validators.json", json.dumps(validators, indent=1, sort_keys=True).encode())
    atomic_write(STATE / f"{source.id}.misses.json", json.dumps(misses, indent=1, sort_keys=True).encode())
    if report.ok:
        atomic_write(STATE / f"{source.id}.last-sync", datetime.now(timezone.utc).isoformat().encode())
    return report


def shrinkage(source: Source, previous: list[dict], live: set[str]) -> str | None:
    """Describe a suspicious drop in page count, overall or for any one
    manual, or None. Checked per manual so a small manual can't vanish inside
    a big source."""
    groups: dict[str, list[int]] = {}
    for p in previous:
        groups.setdefault(source.manual_for(p["path"]).name, [0, 0])[0] += 1
    for path in live:
        groups.setdefault(source.manual_for(path).name, [0, 0])[1] += 1
    if len(previous) and len(live) < SHRINK_GUARD * len(previous):
        return f"page count fell from {len(previous)} to {len(live)}"
    for name, (before, after) in sorted(groups.items()):
        if before >= 5 and after < SHRINK_GUARD * before:
            return f"manual {name} fell from {before} to {after} pages"
    return None


def print_report(report: SyncReport, out=sys.stdout) -> None:
    print(
        f"{report.source}: {report.pages} pages, +{len(report.added)} "
        f"~{len(report.changed)} -{len(report.removed)}, "
        f"{len(report.errors)} errors, {len(report.warnings)} warnings"
        + (f", {report.absent} parent pages not in this edition" if report.absent else ""),
        file=out,
    )
    for e in report.errors:
        print(f"  error: {e}", file=out)
    for w in report.warnings:
        print(f"  warning: {w}", file=out)


# --- redirects ----------------------------------------------------------------

REDIRECTS = MIRROR / "redirects.json"
RECHECK_DAYS = 7
LINKED = re.compile(r"https?://(?:www\.)?(?:%s)/[^\s)\"'<>\]`]*")


def canonical_url(url: str) -> str:
    url = url.split("#", 1)[0].split("?", 1)[0]
    url = re.sub(r"^http://", "https://", url).replace("://www.", "://")
    return re.sub(r"/+$", "", url).removesuffix(".md")


def sync_redirects(sources: list[Source], log=print) -> dict[str, str | None]:
    """Docs pages link to many moved pages (old docs.anthropic.com URLs,
    renamed sections). For every linked docs URL that is not a mirrored page,
    follow its redirects once and record where it ends up; None means it is
    not reachable. Results are kept in mirror/redirects.json and only new URLs
    are looked up, so this is cheap after the first run."""
    hosts = {"docs.anthropic.com", "docs.claude.com", "anthropic.com"}
    pages: set[str] = set()
    for s in sources:
        hosts.add(s.base.split("/")[2])
        manifest = load_json(s.mirror / "manifest.json", {}).get("pages", [])
        pages |= {canonical_url(p["url"]) for p in manifest}
    pattern = re.compile(LINKED.pattern % "|".join(re.escape(h) for h in sorted(hosts)))
    linked: set[str] = set()
    for s in sources:
        for f in s.pages_dir.rglob("*.md"):
            linked |= {canonical_url(u.rstrip(".,;:")) for u in pattern.findall(f.read_text(encoding="utf-8"))}
    known = load_json(REDIRECTS, {})
    checked = load_json(STATE / "redirects-checked.json", {})
    stale_before = (datetime.now(timezone.utc) - timedelta(days=RECHECK_DAYS)).isoformat()
    # New URLs, failed lookups (retried every run), and week-old answers.
    todo = sorted(
        u for u in linked - pages
        if u not in known or known[u] is None or checked.get(u, "") < stale_before
    )

    def follow(url: str) -> tuple[str, str | None]:
        try:
            r = http.get(url, attempts=3, timeout=30)
            return url, canonical_url(r.url)
        except Exception:
            return url, None

    if todo:
        log(f"redirects: checking {len(todo)} linked URLs that are not mirrored pages")
        now = datetime.now(timezone.utc).isoformat()
        with ThreadPoolExecutor(WORKERS) as pool:
            for url, final in pool.map(follow, todo):
                known[url] = final
                checked[url] = now
        STATE.mkdir(parents=True, exist_ok=True)
        atomic_write(STATE / "redirects-checked.json", json.dumps(checked, indent=1, sort_keys=True).encode())
    # Keep entries for URLs that are still linked, sorted for stable diffs.
    known = {u: known[u] for u in sorted(known) if u in linked}
    atomic_write(REDIRECTS, (json.dumps(known, indent=1) + "\n").encode())
    moved = sum(1 for u, f in known.items() if f and f != u)
    log(f"redirects: {len(known)} linked URLs outside the mirror, {moved} redirect elsewhere")
    return known
