"""Tests for claude_info.normalize, built from snippets of the mirrored docs."""

from __future__ import annotations

import json
import shutil
import subprocess
from textwrap import dedent

import pytest

from claude_info.config import PANDOC_READER
from claude_info.normalize import (
    LINEBREAK,
    normalize,
    parse_info,
    raw_fences,
    reindent_json,
)

CC = "https://code.claude.com/docs/en/hooks"
PLATFORM = "https://platform.claude.com/docs/en/build-with-claude/fast-mode"
MCP = "https://modelcontextprotocol.io/specification/2026-07-28/schema"

needs_pandoc = pytest.mark.skipif(shutil.which("pandoc") is None, reason="pandoc not installed")


def md(text: str, url: str = PLATFORM) -> str:
    return normalize(dedent(text), url).markdown


def ast(markdown: str) -> list:
    r = subprocess.run(["pandoc", "--preserve-tabs", "-f", PANDOC_READER, "-t", "json"],
                       input=markdown, capture_output=True, text=True, check=True)
    return json.loads(r.stdout)["blocks"]


def nodes(blocks, kind: str) -> list:
    found = []

    def walk(n):
        if isinstance(n, dict):
            if n.get("t") == kind:
                found.append(n)
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    walk(blocks)
    return found


# -- page envelope ------------------------------------------------------------


def test_frontmatter_moves_to_meta():
    page = normalize(dedent("""\
        ---
        title: Fast mode
        url: https://platform.claude.com/docs/en/build-with-claude/fast-mode
        description: "Diagnose and fix: the most common thinking failures."
        featureMetadata:
          betaHeader: fast-mode-2026-02-01
          zdr:
            eligibility: eligible
          supportedModels:
            - claude-opus-5-5
            - claude-opus-5
          supportedPlatforms:
            Claude Models on Google Cloud (Anthropic managed): ga
        ---

        Fast mode text.
        """), PLATFORM)
    assert page.markdown == "Fast mode text.\n"
    assert page.meta["title"] == "Fast mode"
    assert page.meta["description"] == "Diagnose and fix: the most common thinking failures."
    assert page.meta["featureMetadata.zdr.eligibility"] == "eligible"
    assert page.meta["featureMetadata.supportedModels"] == "claude-opus-5-5\nclaude-opus-5"
    assert page.meta["featureMetadata.supportedPlatforms.Claude Models on Google Cloud (Anthropic managed)"] == "ga"
    assert page.warnings == []


def test_boilerplate_removed():
    page = normalize(dedent("""\
        > ## Documentation Index
        > Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
        > Use this file to discover all available pages before exploring further.

        # Hooks reference

        > Reference for Claude Code hook events.
        """), CC)
    assert page.markdown == "# Hooks reference\n\n> Reference for Claude Code hook events.\n"
    assert page.warnings == []


def test_boilerplate_variant_warns():
    page = normalize(dedent("""\
        > ## Documentation Index
        > Fetch the complete documentation index at: https://claude.com/docs/llms.txt
        > Use this file to discover all available pages before exploring further.

        # Work with Claude Tag
        """), "https://code.claude.com/docs/en/claude-tag")
    assert page.markdown == "# Work with Claude Tag\n"
    assert page.warnings == ["boilerplate-variant: index at https://claude.com/docs/llms.txt"]


def test_unrecognized_boilerplate_is_kept():
    page = normalize("> ## Documentation Index\n> Something else\n", CC)
    assert "Something else" in page.markdown
    assert page.warnings[0].startswith("boilerplate-variant:")


# -- code ---------------------------------------------------------------------


@pytest.mark.parametrize("info, expected", [
    ("bash cURL", ("bash", "cURL", [])),
    ("json settings.json theme={null}", ("json", "settings.json", ["theme={null}"])),
    ("text Output wrap", ("text", "Output", ["wrap"])),
    ('ts title="Full webhook.ts with reply tool" expandable theme={null}',
     ("ts", "Full webhook.ts with reply tool", ["expandable", "theme={null}"])),
    ("json {3,5,11} theme={null}", ("json", None, ["{3,5,11}", "theme={null}"])),
    ("text highlight={4, 5} theme={null}", ("text", None, ["highlight={4, 5}", "theme={null}"])),
    ("bash Bash and Zsh theme={null}", ("bash", "Bash and Zsh", ["theme={null}"])),
    ("python Python (Claude Platform on AWS)", ("python", "Python (Claude Platform on AWS)", [])),
    ("typescript TypeScript hidelines={1,-1} theme={null}", ("typescript", "TypeScript", ["hidelines={1,-1}", "theme={null}"])),
    ("", ("", None, [])),
])
def test_parse_info(info, expected):
    assert parse_info(info) == expected


def test_fence_attributes():
    out = md("""\
        ```json settings.json theme={null}
        {"a": 1}
        ```

        ```mermaid theme={null}
        flowchart LR
          A --> B
        ```

        ```
        plain
        ```
        """, CC)
    assert out == dedent("""\
        ```{.json title="settings.json"}
        {"a": 1}
        ```

        ```{.mermaid}
        flowchart LR
          A --> B
        ```

        ```
        plain
        ```
        """)


def test_nested_fences_keep_content():
    src = dedent("""\
        ````markdown theme={null}
        ## Environment
        ```!
        node --version
        ```
        ````
        """)
    out = md(src, CC)
    assert out.startswith("````{.markdown}\n## Environment\n```!\n")
    assert out.endswith("```\n````\n")


def test_code_in_components_is_byte_exact():
    # Go code inside a CodeGroup: two-space component indent plus tabs.
    src = (
        "<CodeGroup>\n"
        "  ```go Go\n"
        "  client := anthropic.NewClient(\n"
        "  \toption.WithAPIKey(\"sk-ant-api03-...\"),\n"
        "  )\n"
        "  ```\n"
        "\n"
        "  ```bash cURL\n"
        "  curl https://api.anthropic.com/v1/messages \\\n"
        "  \t--header \"x-api-key: $ANTHROPIC_API_KEY\"\n"
        "\n"
        "      indented four more\n"
        "  ```\n"
        "</CodeGroup>\n"
    )
    out = md(src)
    assert '```{.go title="Go"}\nclient := anthropic.NewClient(\n\toption.WithAPIKey' in out
    assert '\t--header "x-api-key: $ANTHROPIC_API_KEY"\n\n    indented four more\n```' in out
    assert out.startswith("::: {.codegroup}\n")


def test_fence_long_enough_for_content():
    out = md("~~~text\n```\ninner\n```\n~~~\n")
    assert out == "````{.text}\n```\ninner\n```\n````\n"


def test_title_with_backtick_uses_tildes():
    out = md('<File filename="a`b`.md">\n  ```markdown\n  x\n  ```\n</File>\n')
    assert "title=" in out and "x" in out


@needs_pandoc
def test_fence_on_list_marker_line():
    src = dedent("""\
        * Notes:
          * OpenAI: `x`
            * ```typescript theme={null}
              [
                { role: "user" },
              ];
              ```
          * Claude API: y
        """)
    out = md(src, MCP)
    blocks = ast(out)
    codes = nodes(blocks, "CodeBlock")
    assert [c["c"][1] for c in codes] == ['[\n  { role: "user" },\n];']
    assert raw_fences(src) == ['[\n  { role: "user" },\n];']


# -- callouts -----------------------------------------------------------------


def test_note_callout():
    out = md("""\
        <Note>
          Claude Platform on AWS: These credits apply only to the Claude API.
        </Note>
        """)
    assert out == dedent("""\
        ::: {.callout kind="note"}

        Claude Platform on AWS: These credits apply only to the Claude API.

        :::
        """)


def test_warning_with_id_and_title():
    out = md("""\
        <Warning id="workspace-scoped-access" title="Uploaded files are accessible to your entire workspace">
          Any API key in the workspace can read them.
        </Warning>
        """)
    assert out.startswith(
        '::: {#workspace-scoped-access .callout kind="warning" '
        'title="Uploaded files are accessible to your entire workspace"}')


def test_github_alert_becomes_callout():
    out = md("""\
        > [!TIP]
        >
        > For a quickstart guide, see [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide.md).
        """, CC)
    assert out == dedent("""\
        ::: {.callout kind="tip"}

        For a quickstart guide, see [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide.md).

        :::
        """)


def test_alert_with_code_inside():
    out = md("""\
        > [!NOTE]
        >
        > Run:
        >
        > ```bash theme={null}
        > claude --version
        > ```
        """, CC)
    assert '```{.bash}\nclaude --version\n```' in out


# -- containers ---------------------------------------------------------------


def test_tabs():
    out = md("""\
        <Tabs>
          <Tab title="Python">
            The MCP helpers are included in the `mcp` extra:

            ```bash
            pip install "anthropic[mcp]"
            ```
          </Tab>

          <Tab title="TypeScript">
            Install the SDK.
          </Tab>
        </Tabs>
        """)
    assert out == dedent("""\
        :::: {.tabs}

        ::: {.tab title="Python"}

        The MCP helpers are included in the `mcp` extra:

        ```{.bash}
        pip install "anthropic[mcp]"
        ```

        :::

        ::: {.tab title="TypeScript"}

        Install the SDK.

        :::

        ::::
        """)


def test_codegroup_item_text_becomes_tab():
    out = md("""\
        <CodeGroup exclude="shell:cURL, shell:CLI">
          <CodeGroupItem language="cURL">
            The refusal-fallback middleware is part of the Claude SDK, so a cURL request can’t use it.
          </CodeGroupItem>

          ```python Python
          from anthropic import Anthropic
          ```
        </CodeGroup>
        """)
    assert out == dedent("""\
        :::: {.codegroup}

        ::: {.tab title="cURL"}

        The refusal-fallback middleware is part of the Claude SDK, so a cURL request can’t use it.

        :::

        ```{.python title="Python"}
        from anthropic import Anthropic
        ```

        ::::
        """)


def test_steps_with_nested_frame():
    out = md("""\
        <Steps>
          <Step title="Add labels">
            Enter an **Alias** for the key, such as `anthropic-cmek`. Click **Next**.

            <Frame caption="An alias for the key.">
              ![AWS KMS Add labels step.](https://platform.claude.com/docs/images/cmek/aws-add-labels.png)
            </Frame>
          </Step>
        </Steps>
        """)
    assert out == dedent("""\
        ::::: {.steps}

        :::: {.step title="Add labels"}

        Enter an **Alias** for the key, such as `anthropic-cmek`. Click **Next**.

        ::: {.frame caption="An alias for the key."}

        ![AWS KMS Add labels step.](https://platform.claude.com/docs/images/cmek/aws-add-labels.png)

        :::

        ::::

        :::::
        """)


def test_accordion_group():
    out = md("""\
        <AccordionGroup>
          <Accordion title="Example: Creating an analytics dashboard" defaultOpen>
            **Less effective:**
          </Accordion>
        </AccordionGroup>
        """)
    assert out.startswith(":::: {.accordiongroup}\n\n::: {.accordion title=\"Example: Creating an analytics dashboard\"}\n")
    assert "**Less effective:**" in out


def test_details_summary():
    out = md("""\
        <details>
          <summary>See the same operation in V1</summary>

          ```typescript theme={null}
          import { query } from "@anthropic-ai/claude-agent-sdk";
          ```
        </details>
        """, CC)
    assert out == dedent("""\
        ::: {.accordion title="See the same operation in V1"}

        ```{.typescript}
        import { query } from "@anthropic-ai/claude-agent-sdk";
        ```

        :::
        """)


def test_expandable_and_fields():
    out = md("""\
        <ParamField path="user_id" type="string" required>
          The user.
        </ParamField>

        <ParamField body="limit" type="number" default="20">
          Page size.
        </ParamField>

        <ResponseField name="data" type="object[]">
          <Expandable title="properties">
            <ResponseField name="id" type="string" />
          </Expandable>
        </ResponseField>
        """)
    assert '::: {.field kind="param" name="user_id" location="path" type="string" required="true"}' in out
    assert '::: {.field kind="param" name="limit" location="body" type="number" default="20"}' in out
    assert '{.field kind="response" name="data" type="object[]"}' in out
    assert '{.accordion title="properties"}' in out
    assert '::: {.field kind="response" name="id" type="string"}\n\n:::' in out


def test_cards():
    out = md("""\
        <CardGroup cols={3}>
          <Card title="Quickstarts" icon="lightning" href="https://github.com/anthropics/anthropic-quickstarts">
            Deployable applications built with the API.
          </Card>

          <Card id="claude-haiku-5-5" title="Claude Haiku 5.5" icon="file" href="/docs/en/release-notes/system-prompts/claude-haiku-5-5" />
        </CardGroup>
        """)
    assert out == dedent("""\
        :::: {.cards}

        ::: {.card title="Quickstarts" href="https://github.com/anthropics/anthropic-quickstarts"}

        Deployable applications built with the API.

        :::

        ::: {#claude-haiku-5-5 .card title="Claude Haiku 5.5" href="https://platform.claude.com/docs/en/release-notes/system-prompts/claude-haiku-5-5"}

        :::

        ::::
        """)


def test_link_components_become_grouped_cards():
    out = md("""\
        <HomeJourneyStep title="Get started">
          <HomeJourneyLink icon="play" href="https://platform.claude.com/docs/en/get-started">
            Quickstart
          </HomeJourneyLink>
          <HomeJourneyLink icon="lock" href="https://platform.claude.com/settings/keys">
            Get API key in Claude Console
          </HomeJourneyLink>
        </HomeJourneyStep>
        """, "https://platform.claude.com/docs/en/home")
    assert out == dedent("""\
        :::::: {.steps}

        ::::: {.step title="Get started"}

        :::: {.cards}

        ::: {.card title="Quickstart" href="https://platform.claude.com/docs/en/get-started"}

        :::

        ::: {.card title="Get API key in Claude Console" href="https://platform.claude.com/settings/keys"}

        :::

        ::::

        :::::

        ::::::
        """)


def test_home_banner_attributes_are_text():
    out = md("""\
        <HomeSectionHeader label="Platform" title="Choose how you build" description="Pick the developer surface that matches your approach." />
        """, "https://platform.claude.com/docs/en/home")
    assert out == "*Platform*\n\n**Choose how you build**\n\nPick the developer surface that matches your approach.\n"


def test_file_explorer_titles_code():
    out = md("""\
        <FileExplorer>
          <File filename="agents/reviewer.md">
            ```markdown
            ---
            name: Code reviewer
            ---
            ```
          </File>
        </FileExplorer>
        """)
    assert out == dedent("""\
        ::: {.codegroup}

        ```{.markdown title="agents/reviewer.md"}
        ---
        name: Code reviewer
        ---
        ```

        :::
        """)


def test_unknown_component_is_kept_with_warning():
    page = normalize('<MCPServersTable platform="mcpConnector" />\n\n<Shiny mode="x">\n  Some **text**.\n</Shiny>\n', PLATFORM)
    assert '::: {.component name="MCPServersTable" platform="mcpConnector"}' in page.markdown
    assert '::: {.component name="Shiny" mode="x"}\n\nSome **text**.\n\n:::' in page.markdown
    assert page.warnings == ["unknown-component: <MCPServersTable> (empty)", "unknown-component: <Shiny>"]


def test_component_in_list_item_stays_in_item():
    out = md("""\
        1. Open the console.
        2. <Note>
             Only admins can do this.
           </Note>
        3. Done.
        """)
    assert '2. ::: {.callout kind="note"}\n\n   Only admins can do this.\n\n   :::' in out
    assert "3. Done." in out


# -- media --------------------------------------------------------------------


def test_video_with_sources_in_frame():
    out = md("""\
        <Frame caption="The ant CLI in action.">
          <video aria-label="Screen recording of the ant CLI running in a terminal.">
            <source src="https://platform.claude.com/docs/videos/ant-cli-demo.webm" type="video/webm" />
            <source src="/docs/videos/ant-cli-demo.mp4" type="video/mp4" />
          </video>
        </Frame>
        """, "https://platform.claude.com/docs/en/cli-sdks-libraries/cli/quickstart")
    assert out == dedent("""\
        ::: {.frame caption="The ant CLI in action."}

        [Video: Screen recording of the ant CLI running in a terminal.](https://platform.claude.com/docs/videos/ant-cli-demo.webm) · [mp4](https://platform.claude.com/docs/videos/ant-cli-demo.mp4)

        :::
        """)


def test_self_closing_video_uses_file_name():
    out = md('<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/x/images/whats-new/design-skill.mp4?fit=max&auto=format" />\n', CC)
    assert out == "[Video: design-skill.mp4](https://mintcdn.com/claude-code/x/images/whats-new/design-skill.mp4?fit=max&auto=format)\n"


def test_img_tag_becomes_image():
    out = md('Logo: <img src="/images/logo.png" alt="The logo" width="20" /> here.\n', CC)
    assert out == "Logo: ![The logo](https://code.claude.com/images/logo.png) here.\n"


# -- tables -------------------------------------------------------------------


@needs_pandoc
def test_html_table_becomes_pipe_table():
    src = dedent("""\
        <table>
          <thead>
            <tr>
              <th>Feature</th>
              <th>Google Cloud's Agent Platform</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>[Web search](https://code.claude.com/docs/en/tools-reference.md#websearch-tool-behavior)</td>
              <td>See note <sup>[1](#fn1)</sup></td>
            </tr>
            <tr>
              <td>Billing</td>
              <td>**Teams:** per-seat\\
              **Enterprise:** [Contact Sales](https://claude.com/contact-sales) | PAYG</td>
            </tr>
          </tbody>
        </table>
        """)
    out = md(src, CC)
    assert out.startswith("| Feature | Google Cloud's Agent Platform |\n|---|---|\n")
    assert "| See note \\^[1](#fn1) |" in out
    assert f"per-seat {LINEBREAK} **Enterprise:**" in out
    assert "PAYG" in out and "\\| PAYG" in out
    blocks = ast(out)
    assert [b["t"] for b in blocks] == ["Table"]
    assert not nodes(blocks, "RawInline") and not nodes(blocks, "RawBlock")


@needs_pandoc
def test_br_in_pipe_table_cell():
    out = md("""\
        | Where           | Required role                                       |
        | --------------- | --------------------------------------------------- |
        | **Claude plan** | Max: the subscriber<br />Team: Primary Owner, Owner |
        """)
    assert f"Max: the subscriber{LINEBREAK}Team: Primary Owner" in out
    spans = nodes(ast(out), "Span")
    assert [s["c"][0][1] for s in spans] == [["linebreak"]]


def test_list_in_table_cell():
    out = md("| a | Wire-level differences: <ul> <li>`tasks/result` is removed.</li> <li>The `task` parameter is removed.</li></ul> |\n", MCP)
    assert out == (f"| a | Wire-level differences: {LINEBREAK}• `tasks/result` is removed. "
                   f"{LINEBREAK}• The `task` parameter is removed. |\n")


def test_br_in_paragraph_is_hard_break():
    assert md("Line one<br />Line two\n") == "Line one\\\nLine two\n"
    assert md("Line one<br />\n- not a list\n") == "Line one\\\n\\- not a list\n"
    assert md("Trailing<br />\n") == "Trailing\n"


# -- inline -------------------------------------------------------------------


def test_kbd_sup_badge_eligible():
    assert md("Press <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>.\n", MCP) == "Press `Cmd` + `Shift` + `P`.\n"
    assert md("Opus 4.1<sup>1</sup>\n") == "Opus 4.1\\^1\n"
    assert md("Attributes tagged with <Badge>Content</Badge> are only on spans.\n") == \
        "Attributes tagged with \\[Content\\] are only on spans.\n"
    assert md('| x | <Eligible>Yes</Eligible> | <Eligible status="no">No</Eligible> |\n') == "| x | Yes | No |\n"


def test_span_and_div_unwrapped():
    out = md('<div class="note">\n  Some <span style="color: red">red</span> text.\n</div>\n')
    assert out == "Some red text.\n"


def test_placeholders_survive_as_text():
    out = md("Replace <your-api-key> and <ORGANIZATION_UUID> in `curl -H <name>`; a List<T> works.\n")
    assert out == "Replace \\<your-api-key> and \\<ORGANIZATION_UUID> in `curl -H <name>`; a List\\<T> works.\n"
    # Already-escaped placeholders and autolinks are untouched.
    assert md("Use \\<name> or <https://example.com>.\n", CC) == "Use \\<name> or <https://example.com>.\n"


def test_jsx_expressions_and_comments_removed():
    page = normalize("---\ntitle: T\n---\nSee the{\" \"}<a href=\"/x\">docs</a>.{/* TODO: link */}\n", PLATFORM)
    assert page.markdown == "See the [docs](https://platform.claude.com/x).\n"
    assert page.warnings == ["jsx-comment: {/* TODO: link */}"]


def test_html_comment_removed_with_warning():
    page = normalize("Text.\n\n<!-- hidden note -->\n\nMore.\n", CC)
    assert page.markdown == "Text.\n\nMore.\n"
    assert page.warnings == ["html-comment: <!-- hidden note -->"]


def test_relative_links_made_absolute():
    out = md("[a](/docs/en/x) [b](./y.md#z) [c](../c) [d](#anchor) [e](https://example.com/e) ![i](img/p.png \"t\")\n",
             "https://code.claude.com/docs/en/agent-sdk/overview")
    assert out == ("[a](https://code.claude.com/docs/en/x) [b](https://code.claude.com/docs/en/agent-sdk/y.md#z) "
                   "[c](https://code.claude.com/docs/en/c) [d](#anchor) [e](https://example.com/e) "
                   "![i](https://code.claude.com/docs/en/agent-sdk/img/p.png \"t\")\n")


def test_reference_definition_made_absolute():
    out = md("See [x][1].\n\n[1]: /docs/en/x\n", CC)
    assert out == "See [x][1].\n\n[1]: https://code.claude.com/docs/en/x\n"


def test_div_fence_text_is_escaped():
    assert md("::: not a div\n") == "\\::: not a div\n"


# -- exported MCP schema pages --------------------------------------------------


def test_flattened_schema_example():
    src = ('}Text provided to or from an LLM.  <details> <summary>Example: Text content'
           '[Permalink](#textcontent-example-text-content)</summary><pre id="textcontent-example-text-content">'
           '`{  "type": "text",  "text": "Tool result text"} `Copy</pre> </details> type: "text"'
           '[Permalink](#textcontent-type)  text: string\n')
    page = normalize(src, MCP)
    assert page.markdown == dedent("""\
        }Text provided to or from an LLM.
        ::: {.accordion title="Example: Text content"}

        ```{#textcontent-example-text-content .json}
        {
          "type": "text",
          "text": "Tool result text"
        }
        ```

        :::
        type: "text"  text: string
        """)
    assert page.warnings == ["dropped-permalink: 2 [Permalink](#...) links",
                             "dropped-copy-label: 1 'Copy' button labels in <pre>"]


@needs_pandoc
def test_code_and_divs_keep_lists_tight():
    out = md("""\
        1. Run:
           ```bash
           claude --version
           ```
        2. Then:
           <Note>
             Restart.
           </Note>
        3. Done.
        """)
    lists = nodes(ast(out), "OrderedList")
    items = lists[0]["c"][1]
    assert [[b["t"] for b in item] for item in items] == [["Plain", "CodeBlock"], ["Plain", "Div"], ["Plain"]]


def test_reindent_json_keeps_literals():
    assert reindent_json('{"a": [1e5, 0.70], "b": {}, "c": "x,  y"}') == \
        '{\n  "a": [\n    1e5,\n    0.70\n  ],\n  "b": {},\n  "c": "x,  y"\n}'
    assert reindent_json("not json") is None


# -- end to end ---------------------------------------------------------------


@needs_pandoc
def test_platform_page_parses_cleanly():
    src = dedent("""\
        ---
        title: API credits
        url: https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers
        ---

        <Note>
          Credits apply only to the Claude API in the [Claude Console](/settings).
        </Note>

        <Steps>
          <Step title="Open billing settings">
            On claude.ai, go to **Settings > Billing**.

            1. Pick a plan
            2. Confirm:

               ```bash cURL
               curl https://api.anthropic.com/v1/messages <your-api-key>
               ```
          </Step>
        </Steps>

        Use <kbd>Esc</kbd> to cancel a `<name>` lookup.
        """)
    out = normalize(src, "https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers").markdown
    blocks = ast(out)
    assert not nodes(blocks, "RawInline") and not nodes(blocks, "RawBlock")
    divs = [d["c"][0][1] for d in nodes(blocks, "Div")]
    assert divs == [["callout"], ["steps"], ["step"]]
    codes = nodes(blocks, "CodeBlock")
    assert [c["c"][1] for c in codes] == ["curl https://api.anthropic.com/v1/messages <your-api-key>"]
    assert codes[0]["c"][0][1:] == [["bash"], [["title", "cURL"]]]
    assert nodes(nodes(blocks, "OrderedList"), "CodeBlock"), "code block stays inside the list item"


def test_html_pre_keeps_whitespace():
    src = '<pre><code class="language-python">def f(x):\n    return x &lt; 1\n</code></pre>\n'
    assert md(src, CC) == "```{.python}\ndef f(x):\n    return x < 1\n```\n"


def test_file_without_single_code_block_is_component():
    page = normalize('<File filename="notes.txt">\n  Plain text.\n</File>\n', PLATFORM)
    assert page.markdown == '::: {.component name="File" filename="notes.txt"}\n\nPlain text.\n\n:::\n'
    assert page.warnings == ["unknown-component: <File> without a single code block"]


def test_unterminated_permalink_is_text():
    assert md("See [Permalink](#x and more\n", MCP) == "See [Permalink](#x and more\n"
