"""Shared fixtures for the fetch/http/texinfo/build/verify/cli tests.

``isolated`` points every module-level path (mirror/, .state/, build/, the
Info directory, the repo root) at a temporary directory, so no test can touch
the real mirror, state, build output or ~/.local/share/info. The network
guard refuses any socket connection that is not to the loopback interface.
"""

from __future__ import annotations

import ipaddress
import socket
from pathlib import Path

import pytest

from claude_info import build, cli, config, fetch, install, verify, schemas


class Paths:
    def __init__(self, root: Path):
        self.root = root
        self.mirror = root / "mirror"
        self.state = root / ".state"
        self.build = root / "build"
        self.info = root / "info"
        self.redirects = self.mirror / "redirects.json"


@pytest.fixture
def isolated(tmp_path, monkeypatch) -> Paths:
    p = Paths(tmp_path / "repo")
    p.root.mkdir()
    monkeypatch.setattr(config, "ROOT", p.root)
    monkeypatch.setattr(config, "MIRROR", p.mirror)
    monkeypatch.setattr(config, "STATE", p.state)
    monkeypatch.setattr(config, "BUILD", p.build)
    monkeypatch.setattr(config, "INFO_DIR", p.info)
    monkeypatch.setattr(fetch, "STATE", p.state)
    monkeypatch.setattr(fetch, "MIRROR", p.mirror)
    monkeypatch.setattr(fetch, "REDIRECTS", p.redirects)
    monkeypatch.setattr(build, "BUILD", p.build)
    monkeypatch.setattr(build, "MIRROR", p.mirror)
    monkeypatch.setattr(build, "STATE", p.state)
    monkeypatch.setattr(build, "REDIRECTS", p.redirects)
    monkeypatch.setattr(verify, "BUILD", p.build)
    monkeypatch.setattr(cli, "ROOT", p.root)
    monkeypatch.setattr(cli, "STATE", p.state)
    monkeypatch.setattr(cli, "BUILD", p.build)
    monkeypatch.setattr(cli, "INFO_DIR", p.info)
    monkeypatch.setattr(install, "BUILD", p.build)
    monkeypatch.setattr(install, "INFO_DIR", p.info)
    monkeypatch.setattr(schemas, "MIRROR", p.mirror)
    monkeypatch.setattr(schemas, "DIR", p.mirror / "mcp-schema")
    monkeypatch.setattr(schemas, "STATE", p.state)

    def no_sources(*a, **k):
        raise AssertionError("test called load_sources() without stubbing it")

    for mod in (config, build, verify, cli):
        monkeypatch.setattr(mod, "load_sources", no_sources)
    return p


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    real = socket.socket.connect

    def guarded(self, address):
        if self.family in (socket.AF_INET, socket.AF_INET6):
            host = address[0]
            try:
                loopback = ipaddress.ip_address(host).is_loopback
            except ValueError:
                loopback = host == "localhost"
            if not loopback:
                raise AssertionError(f"test tried to reach the network: {address!r}")
        return real(self, address)

    monkeypatch.setattr(socket.socket, "connect", guarded)


# -- a tiny mirrored site for build/verify end-to-end tests ---------------------

CODE_BASE = "https://code.claude.com/docs/en/"
PLATFORM_BASE = "https://platform.claude.com/docs/en/"

SITE_PAGES = {
    "code": [
        # path, title, nav, body
        ("overview.md", "Claude Code", ["Getting started"],
         "# Claude Code\n\nClaude Code is an agentic coding tool. Start with the "
         "[hooks guide](https://code.claude.com/docs/en/hooks).\n"),
        ("hooks.md", "Hooks reference", ["Reference"],
         "# Hooks reference\n\nHooks run shell commands. See the "
         "[settings](https://docs.anthropic.com/en/docs/claude-code/settings) and the "
         "[Messages API](https://platform.claude.com/docs/en/api/messages#request).\n\n"
         "## Events {#events}\n\nEach event has a payload.\n\n"
         "| Event | When |\n|---|---|\n| PreToolUse | Before a tool runs |\n"
         "| Stop | When the turn ends |\n\n"
         "```mermaid\nsequenceDiagram\n    Alice->>Bob: Hello\n```\n\n"
         "Jump to [events](#events) or the [moved page](https://code.claude.com/docs/en/old-name).\n"),
        ("settings.md", "Settings", ["Reference"],
         "# Settings\n\nSettings live in `settings.json`, quokka.\n\nA quokka is a marsupial.\n"),
        ("whats-new.md", "What's new", ["Reference"], "# What's new\n\nRelease notes.\n"),
        # A sitemap-only copy of whats-new.md under a second URL.
        ("whats-new/index.md", "", ["Other pages"], "# What's new\n\nRelease notes.\n"),
    ],
    "platform": [
        ("intro.md", "Intro to Claude", ["Get started"],
         "# Intro to Claude\n\nClaude is a family of models. Read the "
         "[hooks reference](https://code.claude.com/docs/en/hooks#events).\n"),
        ("api/messages.md", "Messages", ["API"],
         "# Messages\n\nSend a message.\n\n## Request {#request}\n\nThe `model` parameter is required.\n"),
    ],
}


@pytest.fixture
def site(isolated, monkeypatch):
    """Two sources (three manuals) mirrored under the isolated root, with
    load_sources stubbed to return them."""
    import json

    from claude_info.config import Manual, Source

    code = Source(id="code", name="Claude Code", base=CODE_BASE,
                  index="https://code.claude.com/docs/llms.txt",
                  manuals=(Manual("claude-code", "Claude Code", "The coding tool.", ("",)),))
    platform = Source(id="platform", name="Claude Developer Platform", base=PLATFORM_BASE,
                      index="https://platform.claude.com/llms.txt",
                      manuals=(Manual("claude-api", "Claude API Reference", "Endpoints.", ("api/",)),
                               Manual("claude-platform", "Claude Developer Platform", "Guides.", ("",))))
    sources = [code, platform]
    for src in sources:
        pages = []
        for order, (path, title, nav, text) in enumerate(SITE_PAGES[src.id]):
            f = src.pages_dir / path
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(text, encoding="utf-8")
            pages.append({"path": path, "url": src.base + path, "title": title, "description": "",
                          "nav": nav, "order": order, "in_index": nav != ["Other pages"],
                          "in_sitemap": True, "linked": False, "sha256": ""})
        (src.mirror / "manifest.json").write_text(json.dumps({"source": src.id, "base": src.base,
                                                              "pages": pages}))
    isolated.redirects.write_text(json.dumps({
        "https://code.claude.com/docs/en/old-name": "https://code.claude.com/docs/en/settings",
    }))
    for mod in (config, build, verify, cli):
        monkeypatch.setattr(mod, "load_sources", lambda path=None: list(sources))
    return sources
