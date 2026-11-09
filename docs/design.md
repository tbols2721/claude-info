# Design and data flow

`claude-info` mirrors configured public documentation and converts it into
linked GNU Info manuals. The mirror provides source text for offline builds
and local change inspection. Conversion adapts navigation and layout to a
terminal while retaining source URLs and checking text preservation.

## Pipeline

```text
llms.txt + sitemap.xml + discovered links
    -> mirror/<source>/pages/*.md
    -> normalized Markdown -> Pandoc JSON
    -> Texinfo, navigation, index, tables, and diagrams
    -> makeinfo -> build/info/*.info
    -> optional installation in the user's Info directory
```

| Module | Responsibility |
| --- | --- |
| `config.py`, `sources.toml` | Paths, sources, and manual grouping |
| `http.py` | Requests, retries, and conditional fetching |
| `fetch.py` | Discovery, mirroring, redirects, and deletion guards |
| `schemas.py` | MCP TypeScript schema snapshots and generated schema pages |
| `normalize.py` | MDX and HTML conversion to the writer's Markdown vocabulary |
| `diagrams.py` | Mermaid rendering as terminal text |
| `texinfo.py` | Pandoc AST to Texinfo and table layout |
| `build.py` | Node trees, names, links, indexes, and makeinfo invocation |
| `verify.py` | Content, node reachability, and diagram checks |
| `install.py`, `cli.py` | Installation, commands, and optional scheduling |

## Source discovery and fetching

Sources are configured in `sources.toml`. Discovery combines `llms.txt` and
sitemap entries, then examines links for pages absent from either index.
Redirects are recorded in `mirror/redirects.json`. Legacy documentation URLs
can therefore resolve to native references rather than remain stale web links.
API reference editions can derive their page lists from the HTTP reference
without requiring an independent sitemap.

Requests use conditional validators, retry selected transient failures, and
check response encoding and content. HTTP validators and missing-page state
live in ignored `.state/`. Successful source text is written atomically.
A failed page fetch reports an error and retains the last good copy.

An index failure skips that source. Sitemap failures retain previously known
sitemap-only pages. Repeated 404 handling distinguishes temporary absence from
removal. Deletion guards reject substantial shrinkage in a source or individual
manual. These guards reduce accidental loss; upstream indexes and responses
still require inspection when behavior changes.

## Conversion and navigation

The normalizer turns supported MDX components into fenced divisions, tables,
and other structures understood by the writer. Code preservation has a separate
corpus check. CommonMark options avoid interpreting literal prices, approximate
values, mentions, or emoji syntax as unrelated formatting.

The writer builds native menus, cross-references, page nodes, section anchors,
and index entries. Node names are adjusted for Texinfo delimiter restrictions.
Displayed headings retain their original labels. Duplicate anchors are emitted
once. Builds load source metadata across manuals so subset builds can still
resolve cross-manual references.

Link resolution considers exact pages, known legacy URL forms, redirects,
and section anchors. Unresolved fragments fall back to the correct page and
are reported under `build/`. External references remain URLs. A direct Info
node is opened with `info '(manual)Node name'`; menu/index topic lookup is a
different reader operation.

Tables use terminal-width layouts and can become labeled records when columns
would be too narrow. Mermaid sequence, flowchart, state, and Gantt diagrams
are rendered as text. Wide diagrams can become structured lists. This adapts
presentation without inventing diagram content.

MCP schemas are mirrored from the specification repository for the versions
represented in the source collection. Generated schema pages provide separate
sections and index entries for declarations, alongside the site's own pages.

## Update and installation behavior

`update` runs fetching, building, installation, verification, and a local commit
of changed `mirror/` files on `main`. It does not push by default. `--push` or
`CLAUDE_INFO_PUSH=1` enables publication; `--no-push` prevents it. The supplied
systemd user service explicitly disables pushing.

A lock prevents concurrent updates. A failed manual build is not installed,
so its previous installed version remains available. Verification can report
problems after successfully built manuals have been installed; the command
exits nonzero in that case. Read the [verification guide](verification.md)
before interpreting a successful installation as a complete quality result.

The optional user timer runs daily with a randomized delay and catches up
after downtime. It waits for documentation-site DNS before starting. Installing
manuals does not itself install or enable the timer.
