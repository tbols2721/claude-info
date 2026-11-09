"""claude-info command line."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone

from . import fetch, schemas
from .config import BUILD, INFO_DIR, ROOT, STATE, load_sources


def select_sources(names: list[str]):
    sources = load_sources()
    if not names:
        return sources
    known = {s.id: s for s in sources}
    unknown = [n for n in names if n not in known]
    if unknown:
        sys.exit(f"unknown source(s): {', '.join(unknown)}; known: {', '.join(known)}")
    return [known[n] for n in names]


def manual_names(sources) -> list[str]:
    return [m.name for s in sources for m in s.manuals]


def lock():
    """Hold an exclusive lock so a timer run and a manual run can't overlap."""
    STATE.mkdir(parents=True, exist_ok=True)
    f = open(STATE / "lock", "w")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        sys.exit("another claude-info run is in progress")
    return f


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=check)


# --- commands ---------------------------------------------------------------

def sync_all(sources) -> list:
    """Sync each source, resolve moved links, and pick up any pages that the
    redirects revealed (linked to, but in neither index nor sitemap). Each
    unlisted page is tried once per run, so a dead one can't cause loops."""
    reports = {s.id: fetch.sync_source(s) for s in sources}
    tried: set[tuple[str, str]] = set()
    for _round in range(5):  # unlisted pages can link to further unlisted pages
        redirects = fetch.sync_redirects(load_sources())
        pending = []
        for s in sources:
            manifest = fetch.load_json(s.mirror / "manifest.json", {}).get("pages", [])
            known = {p["path"] for p in manifest}
            new = {
                p for f in redirects.values() if f
                if (p := fetch.page_path(s, f)) and p not in known and (s.id, p) not in tried
            }
            if new:
                tried |= {(s.id, p) for p in new}
                pending.append(s)
        if not pending:
            break
        for s in pending:
            print(f"{s.id}: links point at unlisted pages; syncing again to fetch them")
            reports[s.id] = merge_reports(reports[s.id], fetch.sync_source(s))
    if any(s.id == schemas.SOURCE for s in sources):
        r = schemas.sync()
        reports["mcp-schema"] = fetch.SyncReport(
            "mcp-schema", pages=len(schemas.versions()), added=r.fetched,
            changed=r.changed, removed=r.removed, errors=r.errors)
    return list(reports.values())


def merge_reports(first: fetch.SyncReport, again: fetch.SyncReport) -> fetch.SyncReport:
    """Combine two syncs of one source in the same run into net changes:
    added then removed is nothing; removed then re-added is a change."""
    a1, a2 = set(first.added), set(again.added)
    r1, r2 = set(first.removed), set(again.removed)
    out = fetch.SyncReport(again.source, pages=again.pages, absent=again.absent)
    out.added = sorted((a1 - r2) | (a2 - r1))
    out.removed = sorted((r1 - a2) | (r2 - a1))
    out.changed = sorted((set(first.changed) | set(again.changed) | (r1 & a2))
                         - set(out.added) - set(out.removed))
    out.errors = list(dict.fromkeys(first.errors + again.errors))
    out.warnings = list(dict.fromkeys(first.warnings + again.warnings))
    return out


def cmd_sync(args) -> int:
    _l = lock()
    reports = sync_all(select_sources(args.sources))
    for r in reports:
        fetch.print_report(r)
    return 0 if all(r.ok for r in reports) else 1


def cmd_build(args) -> int:
    from .build import build

    _l = lock()
    results = build([s.id for s in select_sources(args.sources)])
    return 0 if all(results.values()) else 1


def cmd_install(args) -> int:
    from .install import install

    _l = lock()
    return 0 if install(manual_names(select_sources(args.sources))) else 1


def cmd_update(args) -> int:
    """sync -> build -> install -> verify -> commit mirror/; push only when requested.

    A manual that fails to build is not installed (the previous copy stays).
    Verify problems don't block installing, since fresh docs beat stale ones,
    but they make the run exit non-zero so the timer shows as failed."""
    from .build import build
    from .install import install
    from .verify import verify

    _l = lock()
    sources = select_sources(args.sources)
    reports = sync_all(sources)
    for r in reports:
        fetch.print_report(r)
    results = build([s.id for s in sources])
    built = [name for name, ok in results.items() if ok]
    installed = install(built) if built else False
    verified = verify([s.id for s in sources]) if built else False
    commit_mirror()
    pushed = True
    if not args.no_push and (args.push or os.environ.get("CLAUDE_INFO_PUSH", "0") == "1"):
        pushed = push()  # also retries commits a previous failed push left behind
    checks = {
        "sync": all(r.ok for r in reports),
        "build": bool(results) and all(results.values()),
        "install": installed,
        "verify": verified,
        "push": pushed,
    }
    failed = [k for k, ok in checks.items() if not ok]
    print("update finished" + (f" with problems in: {', '.join(failed)}" if failed else ""))
    return 1 if failed else 0


def current_branch() -> str:
    return git("symbolic-ref", "--quiet", "--short", "HEAD", check=False).stdout.strip()


def commit_mirror() -> bool:
    """Commit everything under mirror/ as one docs-sync commit, described from
    the staged diff itself (so changes from an earlier, interrupted run are
    listed too). Only on the main branch."""
    if git("rev-parse", "--git-dir", check=False).returncode != 0:
        print("not a git repository; skipping commit")
        return False
    if current_branch() != "main":
        print(f"on branch {current_branch() or '(detached)'}, not main; not committing docs")
        return False
    git("add", "--all", "--", "mirror")
    if git("diff", "--cached", "--quiet", "--", "mirror", check=False).returncode == 0:
        print("docs unchanged; nothing to commit")
        return False
    status = git("diff", "--cached", "--name-status", "--no-renames", "--", "mirror").stdout
    per_source: dict[str, list[str]] = {}
    for line in status.splitlines():
        code, path = line.split("\t", 1)
        parts = path.split("/", 3)  # mirror/<source>/pages/<page>
        if len(parts) == 4 and parts[2] == "pages":
            sign = {"A": "+", "D": "-"}.get(code[0], "~")
            per_source.setdefault(parts[1], []).append(f"  {sign} {parts[3]}")
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [f"Docs sync {day}", ""]
    for source, changes in sorted(per_source.items()):
        counts = {sign: sum(c.startswith(f"  {sign}") for c in changes) for sign in "+~-"}
        lines.append(f"{source}: +{counts['+']} ~{counts['~']} -{counts['-']}")
        lines += sorted(changes, key=lambda c: (c[2], c))
    if not per_source:
        lines.append("Index, sitemap or redirect files changed; no pages changed.")
    git("commit", "--quiet", "-m", "\n".join(lines), "--", "mirror")
    print(git("log", "-1", "--format=committed %h %s").stdout.strip())
    return True


def push() -> bool:
    if not git("remote", check=False).stdout.strip():
        print("no git remote; skipping push")
        return True
    if current_branch() != "main":
        return True
    ahead = git("rev-list", "--count", "@{upstream}..HEAD", check=False)
    if ahead.returncode == 0 and ahead.stdout.strip() == "0":
        return True  # nothing to push
    r = git("push", "--quiet", check=False)
    print("pushed" if r.returncode == 0 else f"push failed: {r.stderr.strip()}")
    return r.returncode == 0


def cmd_changes(args) -> int:
    """What changed upstream, from the mirror's git history."""
    paths = [f"mirror/{s.id}/pages" for s in select_sources(args.sources)]
    cmd = ["log", f"--since={args.since}", "--format=%n%C(yellow)%ad%C(reset)  %s",
           "--date=short", "--name-status", "--color=always"]
    if args.diff:
        cmd = ["log", f"--since={args.since}", "-p", "--word-diff=color", "--date=short",
               "--format=%n%C(yellow)%ad%C(reset)  %s", "--color=always"]
    out = git(*cmd, "--", *paths, check=False).stdout
    if not out.strip():
        print(f"no documentation changes since {args.since}")
        return 0
    return page(out)


def cmd_search(args) -> int:
    """ripgrep the Markdown mirror and say where each hit lives in Info."""
    nodes = load_nodes()
    if shutil.which("rg") is None:
        sys.exit("ripgrep (rg) is required for search")
    sources = select_sources(args.sources)
    cmd = ["rg", "--json", "-s" if args.case_sensitive else "-i", "-e", args.pattern, "--"]
    cmd += [str(s.pages_dir) for s in sources]
    if any(s.id == schemas.SOURCE for s in sources) and schemas.DIR.exists():
        cmd.append(str(schemas.DIR))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 2:
        sys.exit(f"rg: {r.stderr.strip()}")
    hits: dict[str, list[tuple[int, str]]] = {}
    for line in r.stdout.splitlines():
        ev = json.loads(line)
        if ev["type"] == "match":
            d = ev["data"]
            hits.setdefault(d["path"]["text"], []).append(
                (d["line_number"], d["lines"].get("text", "").strip()))
    if not hits:
        print("no matches")
        return 1
    out = []
    bold, plain = ("\033[1m", "\033[0m") if sys.stdout.isatty() else ("", "")
    for path, matches in sorted(hits.items(), key=lambda kv: -len(kv[1])):
        rel = os.path.relpath(path, ROOT / "mirror")
        manual, node = nodes.get(rel, ("?", "?"))
        out.append(f"{bold}{node}{plain}  ({len(matches)})  info {shlex.quote(info_target(manual, node))}")
        for n, text in matches[: args.max_per_page]:
            out.append(f"    {n:>5}: {text[:150]}")
    return page("\n".join(out) + "\n")


def cmd_open(args) -> int:
    """Open a docs URL (or a mirror path, or a page title) in info."""
    nodes = load_nodes()
    from .build import canonical

    key = args.target
    hit = None
    if key.startswith(("http://", "https://")):
        urls = nodes.get("_urls", {})
        base = canonical(key.split("#", 1)[0])
        hit = urls.get(base) or urls.get(base.removesuffix("/index"))
    if hit is None:
        hit = nodes.get(key) or nodes.get(key.removeprefix("mirror/"))
    if hit is None:
        lowered = key.lower()
        hit = next((v for k, v in nodes.items() if k != "_urls" and v[1].lower() == lowered), None)
    if hit is None:
        sys.exit(f"no page found for {key!r}")
    os.execvp("info", ["info", info_target(*hit)])


def info_target(manual: str, node: str) -> str:
    """'(manual)node' is the only form info resolves as a node name; a bare
    'info manual node' is matched against menu items and the index."""
    return f"({manual}){node}"


def load_nodes() -> dict:
    try:
        return json.loads((BUILD / "nodes.json").read_text())
    except FileNotFoundError:
        sys.exit("run 'claude-info build' first")


def cmd_verify(args) -> int:
    from .verify import verify

    return 0 if verify([s.id for s in select_sources(args.sources)]) else 1


def cmd_timer(args) -> int:
    """Install or remove the daily systemd user timer."""
    unit_dir = os.path.expanduser("~/.config/systemd/user")
    names = ["claude-info-update.service", "claude-info-update.timer"]
    if args.action == "remove":
        subprocess.run(["systemctl", "--user", "disable", "--now", names[1]], check=False)
        for n in names:
            p = os.path.join(unit_dir, n)
            if os.path.exists(p):
                os.unlink(p)
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
        print("timer removed")
        return 0
    os.makedirs(unit_dir, exist_ok=True)
    uv = shutil.which("uv") or "uv"
    for n in names:
        text = (ROOT / "systemd" / n).read_text()
        text = text.replace("@ROOT@", str(ROOT)).replace("@UV@", uv)
        with open(os.path.join(unit_dir, n), "w") as f:
            f.write(text)
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "--user", "enable", "--now", names[1]], check=True)
    subprocess.run(["systemctl", "--user", "list-timers", names[1], "--no-pager"], check=False)
    return 0


def cmd_status(args) -> int:
    print(f"repo:      {ROOT}")
    print(f"info dir:  {INFO_DIR}")
    for s in load_sources():
        m = s.mirror / "manifest.json"
        n = len(json.loads(m.read_text())["pages"]) if m.exists() else 0
        last = STATE / f"{s.id}.last-sync"
        when = last.read_text()[:16].replace("T", " ") if last.exists() else "never"
        print(f"{s.id:<18} {n:>4} pages mirrored, last good sync {when}")
    for name in manual_names(load_sources()):
        p = INFO_DIR / f"{name}.info"
        when = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M") if p.exists() else "not installed"
        print(f"{name:<18} {when}")
    last = git("log", "-1", "--format=%ad %s", "--date=format:%Y-%m-%d %H:%M", "--", "mirror", check=False).stdout.strip()
    print(f"last docs commit: {last or 'none'}")
    t = subprocess.run(["systemctl", "--user", "list-timers", "claude-info-update.timer", "--no-pager", "--no-legend"],
                       capture_output=True, text=True)
    print(f"timer:     {t.stdout.strip() or 'not installed'}")
    return 0


def page(text: str) -> int:
    if sys.stdout.isatty():
        p = subprocess.Popen(["less", "-RFX"], stdin=subprocess.PIPE, text=True)
        try:
            p.communicate(text)
        except BrokenPipeError:
            pass
    else:
        sys.stdout.write(text)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="claude-info",
        description="Mirror the Claude, Anthropic, MCP and Agent Skills docs as GNU Info manuals.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name, func, help_, sources=True):
        p = sub.add_parser(name, help=help_, description=help_)
        if sources:
            p.add_argument("sources", nargs="*", help="source ids (default: all)")
        p.set_defaults(func=func)
        return p

    add("sync", cmd_sync, "fetch changed pages into mirror/")
    add("build", cmd_build, "convert mirror/ into Info manuals under build/")
    add("install", cmd_install, f"install built manuals into {INFO_DIR}")
    p = add("update", cmd_update, "sync, build, install, and commit mirror/ changes locally")
    network = p.add_mutually_exclusive_group()
    network.add_argument("--push", action="store_true", help="also push commits to the configured remote")
    network.add_argument("--no-push", action="store_true", help="keep commits local even when CLAUDE_INFO_PUSH=1")
    p = add("changes", cmd_changes, "show which pages changed upstream")
    p.add_argument("--since", default="2 weeks ago", help="git date, e.g. '3 days ago' or 2026-10-01")
    p.add_argument("--diff", action="store_true", help="show the changes as word diffs")
    p = sub.add_parser("search", help="search all pages; print where each hit lives in Info")
    p.add_argument("pattern", help="ripgrep regular expression (case-insensitive by default)")
    p.add_argument("sources", nargs="*", help="source ids (default: all)")
    p.add_argument("-s", "--case-sensitive", action="store_true")
    p.add_argument("-n", "--max-per-page", type=int, default=3)
    p.set_defaults(func=cmd_search)
    p = sub.add_parser("open", help="open a docs URL, mirror path, or page title in info")
    p.add_argument("target")
    p.set_defaults(func=cmd_open)
    add("verify", cmd_verify, "check the built manuals against the mirror for lost content")
    p = sub.add_parser("timer", help="install or remove the daily update timer")
    p.add_argument("action", choices=["install", "remove"])
    p.set_defaults(func=cmd_timer)
    add("status", cmd_status, "show what is mirrored, installed and scheduled", sources=False)

    args = parser.parse_args(argv)
    return args.func(args)
