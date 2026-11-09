# claude-info

Build searchable GNU Info manuals from the Claude Code, Claude API, Model
Context Protocol, and Agent Skills documentation. Read them in a terminal,
follow native cross-references, search their indexes, and inspect upstream
changes in a local Markdown mirror.

This is an independent documentation converter. It is not an official Anthropic,
MCP, or Agent Skills distribution. Source attribution and content terms are
listed in [NOTICE.md](NOTICE.md).

| Manual | Content |
| --- | --- |
| `claude-code` | Claude Code CLI, IDEs, plugins, hooks, and Agent SDK |
| `claude-platform` | Claude API guides, models, tools, and agents |
| `claude-api` | HTTP API reference |
| `claude-api-python` | Python SDK API reference |
| `claude-api-cli` | `ant` CLI API reference |
| `mcp` | MCP documentation, specification versions, and TypeScript schemas |
| `agent-skills` | Agent Skills open standard |

## Requirements and installation

Use Linux or a compatible Unix environment with Python 3.12+,
[uv](https://docs.astral.sh/uv/), Pandoc 3.1+, GNU Texinfo 7, Git, and ripgrep.
The optional scheduler requires a systemd user session. On Debian or Ubuntu,
the documentation tools can be installed with:

```sh
sudo apt install git pandoc texinfo info install-info ripgrep
```

Clone the repository and build the included source snapshot:

```sh
git clone https://github.com/tbols2721/claude-info.git
cd claude-info
uv run claude-info --help
uv run claude-info build
uv run claude-info verify
uv run claude-info install
```

The first `uv run` can download Python dependencies. Building uses the checked-in
mirror and does not contact an AI API. Manuals are installed under
`~/.local/share/info` by default. Select another destination with
`CLAUDE_INFO_INSTALL_DIR`. Neither the build nor user installation requires sudo.

If the reader or shell completion does not discover your user Info directory,
add it while retaining system defaults:

```sh
export INFOPATH="$HOME/.local/share/info:${INFOPATH-}"
```

Run commands from the checkout with `uv run`. To use the CLI elsewhere, pass
`uv run --project /path/to/claude-info claude-info` with your checkout path.

## Read and search

```sh
info claude-code
info '(claude-code)Hooks reference'
info --apropos='prompt caching'
uv run claude-info search 'cache_control'
uv run claude-info search 'cache_control' platform -n 5
uv run claude-info open https://code.claude.com/docs/en/hooks
uv run claude-info open 'Hooks reference'
```

Use `'(manual)Node name'` to open a specific node. The alternative
`info manual topic` searches menus and indexes and can select another topic
with the same name.

| GNU Info key | Action |
| --- | --- |
| `Space` / `Backspace` | Read forward / backward |
| `n` / `p` / `u` | Next / previous / parent node |
| `m` | Select a menu item; Tab completes |
| `Tab`, `Return` | Select and follow a link |
| `l` | Return to the previous location |
| `i`, then `,` | Search the index, then visit the next match |
| `s` | Search manual text |
| `g` | Open a named node |
| `d` / `q` | Open the manual directory / quit |

Menus follow upstream navigation. Code remains labeled; tables and diagrams
are adapted to terminal width. Wide diagrams use structured text. Each page
retains its online source URL.

## Update the local mirror

A sync fetches public documentation; it does not require API keys. Inspect
`git status` and configure a suitable Git author identity before using the
combined update command, which creates local mirror commits on `main`.

```sh
uv run claude-info sync
uv run claude-info build
uv run claude-info verify
uv run claude-info install
# Or run the combined pipeline, including a local mirror commit:
uv run claude-info update
```

Commands accept source IDs: `claude-code`, `platform`, `api-python`, `api-cli`,
`mcp`, and `agent-skills`. For example, use `uv run claude-info sync mcp`.
Fetching needs network access. Build, verification, and reading can use the
existing snapshot offline once their dependencies are available.

Updates do not push by default. To publish from your own fork, configure its
remote, review your Git author identity, and explicitly enable pushing:

```sh
uv run claude-info update --push
```

`CLAUDE_INFO_PUSH=1` also enables it; `--no-push` overrides that setting.
This project's upstream remote is not a destination for another user's local
updates. Read [PRIVACY.md](PRIVACY.md) before publishing a mirror or report.

## Optional daily timer

```sh
uv run claude-info timer install
uv run claude-info status
journalctl --user -u claude-info-update
uv run claude-info timer remove
```

The user timer runs daily with a randomized delay and catches up after downtime.
Its installed service explicitly disables pushes. It records local mirror
commits using the checkout's Git identity. No timer is installed by the normal
build or manual installation commands.

## Failures and maintenance

Failed downloads retain the last good page. Repeated 404s and substantial source
shrinkage have deletion guards. A failed build leaves the previously installed
manual intact. Verification problems produce a nonzero update result, although
successfully built manuals may still be installed. Inspect `build/` reports and
local service logs before treating an update as complete.

The source configuration is in `sources.toml`. The
[design guide](docs/design.md) describes discovery, cross-references, conversion,
and diagrams. The [verification guide](docs/verification.md) describes checks
and known limitations. HTTP validators and update state stay under ignored
`.state/`; generated manuals and diagnostic reports stay under ignored `build/`.

```sh
uv run pytest
uv run python -m claude_info.normalize --check
uv run python -m claude_info.diagrams --check
uv run claude-info changes --since '2 weeks ago'
```

To remove the user installation, remove the timer, delete the installed manuals
named above, and remove their entries with `install-info --delete`. Keep unrelated
manuals and the shared Info directory. Removing the checkout alone does not
remove installed manuals or scheduled user units.
