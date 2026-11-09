# Source attribution and content terms

The original converter, tests, and project documentation use the
[MIT license](LICENSE). That license does not replace licenses or terms attached
to third-party documentation, schemas, examples, or fixtures.

| Content | Upstream source |
| --- | --- |
| Claude Code documentation | [Anthropic Claude Code](https://code.claude.com/docs/) |
| Claude platform and API reference editions | [Anthropic developer platform](https://platform.claude.com/docs/) |
| Model Context Protocol documentation and schemas | [MCP](https://modelcontextprotocol.io/) and its [source repository](https://github.com/modelcontextprotocol/modelcontextprotocol) |
| Agent Skills documentation | [Agent Skills](https://agentskills.io/) and its [source repository](https://github.com/agentskills/agentskills) |

Files under `mirror/` retain upstream text. The converter changes presentation
when building Info manuals: it adds native navigation and indexes, converts
markup, and renders tables and diagrams for a terminal. Each generated page
retains its source URL. `sources.toml` and mirror manifests record source
locations. This project does not claim authorship of upstream documentation.

Anthropic documentation remains subject to its applicable upstream terms;
it is not relicensed under this project's MIT license. Consult those terms
before redistributing a derived collection.

MCP's upstream license notice describes an Apache 2.0/MIT transition and
CC BY 4.0 for documentation outside the specifications. Agent Skills' repository
includes Apache 2.0 terms. Copies of these upstream notices are retained under
`LICENSES/`; source URLs and retrieval hashes are recorded in
`LICENSES/sources.json`. Consult the source and notices applicable to the
particular version when redistributing it. Existing inline notices are retained.

Names and trademarks identify the source projects. This independent converter
has no endorsement from Anthropic or the upstream standards projects.
