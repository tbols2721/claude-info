# Verification and limitations

The project checks conversion quality separately from upstream accuracy. A
successful conversion means that the supplied documentation was represented
correctly; it does not independently establish the accuracy or currency of the
upstream documentation.

## Automated checks

`uv run pytest` exercises fetching, retries, source discovery, redirects,
normalization, diagrams, Texinfo generation, build structure, CLI behavior, and
verification. Test fixtures use temporary directories and block network access
other than localhost. Tests do not read personal configuration or alter installed
manuals.

`uv run claude-info verify` compares each mirrored page with its Info node:

- Source words must appear with their expected multiplicity after markup and
  navigation chrome are removed. Shown component attributes still count.
- Every page must have a node reachable through native menus.
- Top-level Mermaid diagrams must be rendered.
- Mirrored MCP schema declarations must retain their text and individual sections.

The report appears in the terminal and under ignored `build/verify-report.tsv`.
Run `uv run python -m claude_info.normalize --check` to compare fenced code and
normalization across the mirror. Run
`uv run python -m claude_info.diagrams --check` to inspect diagram width and label
preservation; drawings are written to ignored `build/diagram-review.txt`.

## Limits

Word comparisons do not establish identical punctuation or indentation. The
normalizer's code checks provide separate coverage for code preservation.
External links and fragments can be stale upstream. Unresolved fragments link
to the page rather than an invented section, and unresolved links remain URLs.
Build reports under `build/` identify these cases.

Diagrams that cannot fit the terminal width become structured lists. Dynamic
widgets absent from an upstream Markdown export cannot be reconstructed by this
tool. The MCP site's flattened schema prose remains source text; separately
rendered TypeScript schema pages provide a more readable reference.

An update can install successfully built manuals even when verification reports
problems, but exits nonzero so the failure is visible. Inspect the last run and
its reports before treating an update as fully verified. Historical test totals
and mirror page counts are not guarantees about later upstream snapshots.

## Reference snapshot result

The public snapshot passed the offline test suite and full content verification
for all seven manuals. Verification found no missing source words, pages without
nodes, or unreachable nodes; all 259 counted diagrams and six MCP schema files
passed their checks. The HTTP API manual emits four makeinfo layout warnings
about an inline end command. Conversion reports also identify unsupported or
presentation-only upstream component attributes. These warnings are retained in
local build reports rather than described as a warning-free build.
