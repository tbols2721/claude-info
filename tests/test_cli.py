"""Tests for the pure parts of claude_info.cli: merging sync reports, Info
targets, the sync loop (with fetch stubbed), and committing/pushing mirror/
in a temporary git repository."""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from claude_info import cli, fetch
from claude_info.config import Manual, Source
from claude_info.fetch import SyncReport

pytestmark = pytest.mark.usefixtures("isolated")

needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")


# -- merge_reports ----------------------------------------------------------------


def test_merge_reports_net_changes():
    first = SyncReport("s", pages=10, added=["a.md", "b.md"], changed=["c.md", "d.md"],
                       removed=["e.md"], errors=["err1", "dup"], warnings=["w1"], absent=3)
    again = SyncReport("s", pages=12, added=["f.md"], changed=["a.md", "c.md", "g.md"],
                       removed=["d.md"], errors=["dup", "err2"], warnings=["w1", "w2"], absent=4)
    m = cli.merge_reports(first, again)
    assert m.source == "s" and m.pages == 12 and m.absent == 4
    assert m.added == ["a.md", "b.md", "f.md"]  # changed again after being added: still "added"
    assert m.changed == ["c.md", "g.md"]  # d.md was removed in the second sync
    assert m.removed == ["d.md", "e.md"]
    assert m.errors == ["err1", "dup", "err2"]  # deduplicated, order kept
    assert m.warnings == ["w1", "w2"]
    assert not m.ok


def test_merge_reports_ok_when_both_ok():
    m = cli.merge_reports(SyncReport("s", added=["a.md"]), SyncReport("s"))
    assert m.ok and m.added == ["a.md"]


def test_merge_reports_add_then_remove_is_no_change():
    m = cli.merge_reports(SyncReport("s", added=["x.md"]), SyncReport("s", removed=["x.md"]))
    assert "x.md" not in m.added and "x.md" not in m.removed


def test_merge_reports_remove_then_add_is_not_added():
    m = cli.merge_reports(SyncReport("s", removed=["x.md"]), SyncReport("s", added=["x.md"]))
    assert "x.md" not in m.added and "x.md" not in m.removed


# -- info_target ------------------------------------------------------------------------


@pytest.mark.parametrize("manual, node, target", [
    ("claude-code", "Hooks reference", "(claude-code)Hooks reference"),
    ("mcp", "Architecture overview (2025-06-18)", "(mcp)Architecture overview (2025-06-18)"),
    ("claude-api", "Top", "(claude-api)Top"),
])
def test_info_target(manual, node, target):
    assert cli.info_target(manual, node) == target


# -- sync_all with fetch stubbed --------------------------------------------------------------


def test_sync_all_refetches_pages_revealed_by_redirects_once(monkeypatch, isolated):
    src = Source(id="docs", name="Docs", base="https://d.example.com/en/",
                 manuals=(Manual("docs", "D", "", ("",)),))
    monkeypatch.setattr(cli, "load_sources", lambda path=None: [src])
    syncs: list[int] = []

    def fake_sync(source, log=print):
        syncs.append(1)
        src.mirror.mkdir(parents=True, exist_ok=True)
        (src.mirror / "manifest.json").write_text(json.dumps({"pages": [{"path": "a.md"}]}))
        return SyncReport(source.id, pages=1, added=["a.md"] if len(syncs) == 1 else ["late.md"])

    # The redirects keep pointing at a page the sync never manages to list:
    # it must be tried once, not forever.
    monkeypatch.setattr(fetch, "sync_source", fake_sync)
    monkeypatch.setattr(fetch, "sync_redirects",
                        lambda sources, log=print: {"https://d.example.com/en/old": "https://d.example.com/en/unlisted",
                                                    "https://d.example.com/en/dead": None})
    reports = cli.sync_all([src])
    assert len(syncs) == 2
    assert [r.added for r in reports] == [["a.md", "late.md"]]


# -- commit_mirror / push against a temporary repository ------------------------------------------


@pytest.fixture
def repo(isolated, tmp_path, monkeypatch):
    gitconfig = tmp_path / "gitconfig"
    gitconfig.write_text("[user]\n\tname = Test\n\temail = test@example.com\n"
                         "[commit]\n\tgpgsign = false\n[init]\n\tdefaultBranch = main\n")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(gitconfig))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    for var in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        monkeypatch.delenv(var, raising=False)
    root = isolated.root
    git(root, "init", "-q", "-b", "main")
    (root / "README").write_text("x\n")
    write(root, "mirror/docs/pages/keep.md", "keep\n")
    write(root, "mirror/docs/pages/change.md", "v1\n")
    write(root, "mirror/docs/pages/gone.md", "bye\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "initial")
    return root


def git(root, *args) -> str:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True).stdout


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def head_message(root) -> str:
    return git(root, "log", "-1", "--format=%B").strip()


@needs_git
def test_commit_mirror_message_lists_changes(repo, capsys):
    write(repo, "mirror/docs/pages/change.md", "v2\n")
    (repo / "mirror/docs/pages/gone.md").unlink()
    write(repo, "mirror/docs/pages/new/page.md", "hello\n")
    write(repo, "mirror/other/pages/b.md", "b\n")
    write(repo, "mirror/other/pages/a.md", "a\n")
    write(repo, "mirror/docs/manifest.json", "{}\n")
    assert cli.commit_mirror() is True
    msg = head_message(repo).splitlines()
    assert msg[0].startswith("Docs sync 20") and msg[1] == ""
    assert msg[2:] == [
        "docs: +1 ~1 -1",
        "  + new/page.md",
        "  - gone.md",
        "  ~ change.md",
        "other: +2 ~0 -0",
        "  + a.md",
        "  + b.md",
    ]
    assert git(repo, "status", "--porcelain") == ""
    assert "committed" in capsys.readouterr().out


@needs_git
def test_commit_mirror_only_commits_mirror(repo):
    write(repo, "README", "changed outside mirror\n")
    git(repo, "add", "README")  # even when staged
    write(repo, "src.py", "untracked\n")
    write(repo, "mirror/docs/pages/change.md", "v2\n")
    assert cli.commit_mirror() is True
    files = git(repo, "show", "--name-only", "--format=", "HEAD").split()
    assert files == ["mirror/docs/pages/change.md"]
    status = git(repo, "status", "--porcelain")
    assert "M  README" in status and "?? src.py" in status


@needs_git
def test_commit_mirror_nothing_to_commit(repo, capsys):
    before = git(repo, "rev-parse", "HEAD")
    assert cli.commit_mirror() is False
    assert git(repo, "rev-parse", "HEAD") == before
    assert "docs unchanged" in capsys.readouterr().out


@needs_git
def test_commit_mirror_non_page_files_only(repo):
    write(repo, "mirror/redirects.json", "{}\n")
    write(repo, "mirror/docs/llms.txt", "# index\n")
    assert cli.commit_mirror() is True
    assert head_message(repo).splitlines()[2:] == ["Index, sitemap or redirect files changed; no pages changed."]


@needs_git
def test_commit_mirror_includes_leftovers_from_an_interrupted_run(repo):
    write(repo, "mirror/docs/pages/change.md", "v2\n")
    git(repo, "add", "mirror")  # staged by a run that died before committing
    write(repo, "mirror/docs/pages/later.md", "new\n")
    assert cli.commit_mirror() is True
    msg = head_message(repo)
    assert "  ~ change.md" in msg and "  + later.md" in msg


@needs_git
def test_commit_mirror_ignores_temp_files(repo):
    (repo / ".gitignore").write_text(".tmp-*\n")
    write(repo, "mirror/docs/pages/.tmp-abc123", "half\n")
    assert cli.commit_mirror() is False


@needs_git
def test_commit_mirror_not_on_main(repo, capsys):
    git(repo, "checkout", "-q", "-b", "feature")
    write(repo, "mirror/docs/pages/change.md", "v2\n")
    assert cli.commit_mirror() is False
    assert "not main; not committing" in capsys.readouterr().out
    assert git(repo, "log", "-1", "--format=%s").strip() == "initial"


@needs_git
def test_commit_mirror_detached_head(repo, capsys):
    git(repo, "checkout", "-q", "--detach")
    write(repo, "mirror/docs/pages/change.md", "v2\n")
    assert cli.commit_mirror() is False
    assert "(detached)" in capsys.readouterr().out


@needs_git
def test_commit_mirror_not_a_repository(isolated, tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    write(isolated.root, "mirror/docs/pages/a.md", "a\n")
    assert cli.commit_mirror() is False
    assert "not a git repository" in capsys.readouterr().out


@needs_git
def test_push_without_remote(repo, capsys):
    assert cli.push() is True
    assert "no git remote" in capsys.readouterr().out


@needs_git
def test_push_to_local_remote(repo, tmp_path):
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    git(repo, "remote", "add", "origin", str(remote))
    git(repo, "push", "-q", "-u", "origin", "main")
    assert cli.push() is True  # nothing ahead
    write(repo, "mirror/docs/pages/change.md", "v2\n")
    cli.commit_mirror()
    assert cli.push() is True
    assert git(remote, "rev-parse", "main") == git(repo, "rev-parse", "HEAD")


@needs_git
def test_push_failure_returns_false(repo, tmp_path, capsys):
    git(repo, "remote", "add", "origin", str(tmp_path / "missing.git"))
    assert cli.push() is False
    assert "push failed" in capsys.readouterr().out


@pytest.mark.parametrize("environment,flags,expected", [
    (None, [], False),
    ("0", [], False),
    ("1", [], True),
    (None, ["--push"], True),
    ("0", ["--push"], True),
    ("1", ["--no-push"], False),
])
def test_update_push_requires_opt_in(monkeypatch, environment, flags, expected):
    """A normal local update must not publish; explicit choices are honored."""
    from types import SimpleNamespace
    from claude_info import build, install, verify

    if environment is None:
        monkeypatch.delenv("CLAUDE_INFO_PUSH", raising=False)
    else:
        monkeypatch.setenv("CLAUDE_INFO_PUSH", environment)
    monkeypatch.setattr(cli, "select_sources", lambda names: [SimpleNamespace(id="docs")])
    monkeypatch.setattr(cli, "sync_all", lambda sources: [SyncReport("docs")])
    monkeypatch.setattr(build, "build", lambda sources: {"docs": True})
    monkeypatch.setattr(install, "install", lambda manuals: True)
    monkeypatch.setattr(verify, "verify", lambda sources: True)
    commits, pushes = [], []
    monkeypatch.setattr(cli, "commit_mirror", lambda: commits.append(True))
    monkeypatch.setattr(cli, "push", lambda: pushes.append(True) or True)
    assert cli.main(["update", *flags]) == 0
    assert commits == [True]
    assert bool(pushes) is expected
