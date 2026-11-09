"""Tests for claude_info.diagrams, built from real diagrams in the mirror.

Each snippet below is copied verbatim from the page named above it, so the
tests do not depend on mirror/ being present.
"""

from __future__ import annotations

import random
import re

import pytest

from claude_info.diagrams import (
    Rendered,
    labels,
    mermaid_blocks,
    missing_labels,
    problems,
    render,
    tw,
    wrap,
)

# mcp/pages/specification/2024-11-05/basic/lifecycle.md:14
LIFECYCLE = """\
sequenceDiagram
    participant Client
    participant Server

    Note over Client,Server: Initialization Phase
    activate Client
    Client->>+Server: initialize request
    Server-->>Client: initialize response
    Client--)Server: initialized notification

    Note over Client,Server: Operation Phase
    rect rgb(200, 220, 250)
        note over Client,Server: Normal protocol operations
    end

    Note over Client,Server: Shutdown
    Client--)-Server: Disconnect
    deactivate Server
    Note over Client,Server: Connection closed
"""

# mcp/pages/extensions/skills/overview.md:298
SKILLS = """\
sequenceDiagram
    actor User
    participant Model
    participant Host
    participant Server

    opt Discover a catalog
        Host->>Server: skills/list
        Server-->>Host: Skill entries with frontmatter and manifests
        Host->>Model: Available skills and their origins
        Host->>User: Available skills and their origins
    end

    alt Model selects a skill
        Model->>Host: Load skill (server, URI)
    else User selects a skill
        User->>Host: Load skill (server, URI)
    end

    opt Host has only a URI
        Host->>Server: skills/get (URI)
        Server-->>Host: Skill entry or error
    end
    break Lookup failed
        Note over Host,Server: Stop loading (unknown skill: -32602)
    end
    Note over Host: Retain entry (server, URI)

    opt User approval required
        Host->>User: Request approval for this skill and manifest
        User-->>Host: Approve
    end

    Host->>Server: resources/read (SKILL.md URI)
    Server-->>Host: SKILL.md content
    Host->>Host: Verify byte size, digest, and frontmatter
    Host->>Model: Load verified instructions with server origin

    loop Supporting files requested while the skill is active
        Model->>Host: Read a supporting file
        Host->>Host: Resolve URI within the retained manifest
        Host->>Server: resources/read (file URI)
        Server-->>Host: File content
        Host->>Host: Verify byte size and digest
        Host->>Model: Verified content with server origin
    end
"""

# mcp/pages/specification/2025-03-26/basic/transports.md:211
TRANSPORTS = """\
sequenceDiagram
    participant Client
    participant Server

    note over Client, Server: initialization

    Client->>+Server: POST InitializeRequest
    Server->>-Client: InitializeResponse<br>Mcp-Session-Id: 1868a90c...

    Client->>+Server: POST InitializedNotification<br>Mcp-Session-Id: 1868a90c...
    Server->>-Client: 202 Accepted

    note over Client, Server: client requests
    Client->>+Server: POST ... request ...<br>Mcp-Session-Id: 1868a90c...

    alt single HTTP response
      Server->>Client: ... response ...
    else server opens SSE stream
      loop while connection remains open
          Server-)Client: ... SSE messages from server ...
      end
      Server-)Client: SSE event: ... response ...
    end
    deactivate Server

    note over Client, Server: client notifications/responses
    Client->>+Server: POST ... notification/response ...<br>Mcp-Session-Id: 1868a90c...
    Server->>-Client: 202 Accepted

    note over Client, Server: server requests
    Client->>+Server: GET<br>Mcp-Session-Id: 1868a90c...
    loop while connection remains open
        Server-)Client: ... SSE messages from server ...
    end
    deactivate Server
"""

# platform/pages/cli-sdks-libraries/middleware.md:35
MIDDLEWARE = """\
sequenceDiagram
    accTitle: How a request and its response pass through middleware
    accDescr: Your code sends the request to Middleware A. Middleware A calls next(request) to pass it to Middleware B, and Middleware B calls next(request) to pass it to the SDK core. The SDK core sends the HTTP request to the Claude API and receives the HTTP response. The response returns through Middleware B, then Middleware A, to your code.
    autonumber
    participant App as Your code
    participant M1 as Middleware A
    participant M2 as Middleware B
    participant Core as SDK core
    participant API as Claude API
    App->>M1: request
    M1->>M2: next(request)
    M2->>Core: next(request)
    Core->>API: HTTP request
    API-->>Core: HTTP response
    Core-->>M2: response
    M2-->>M1: response
    M1-->>App: response
"""

# mcp/pages/docs/2024-11-05/develop/build-client.md:1333
BUILD_CLIENT = """\
---
config:
    theme: neutral
---
sequenceDiagram
    actor User
    participant Client
    participant Claude
    participant MCP_Server as MCP Server
    participant Tools

    User->>Client: Send query
    Client<<->>MCP_Server: Get available tools
    Client->>Claude: Send query with tool descriptions
    Claude-->>Client: Decide tool execution
    Client->>MCP_Server: Request tool execution
    MCP_Server->>Tools: Execute chosen tools
    Tools-->>MCP_Server: Return results
    MCP_Server-->>Client: Send results
    Client->>Claude: Send tool results
    Claude-->>Client: Provide final response
    Client-->>User: Display response
"""

# mcp/pages/seps/990-enable-enterprise-idp-policy-controls-during-mcp-o.md:59
IDP = """\
sequenceDiagram
    participant UA as Browser
    participant C as MCP Client
    participant MAS as MCP Authorization Server
    participant MRS as MCP Resource Server
    participant IdP as Identity Provider

    rect rgb(255,255,225)
    C-->>UA: Redirect to IdP
    UA->>+IdP: Redirect to IdP
    Note over IdP: User Logs In
    IdP-->>-UA: IdP Authorization Code
    UA->>C: IdP Authorization Code
    C->>+IdP: Token Request with IdP Authorization Code
    IdP-->-C: ID Token
    end

    note over C: User is logged<br>in to MCP Client.<br>Client stores ID Token.

    C->+IdP: Exchange ID Token for ID-JAG
    note over IdP: Evaluate Policy
    IdP-->-C: Responds with ID-JAG
    C->+MAS: Token Request with ID-JAG
    note over MAS: Validate ID-JAG
    MAS-->-C: MCP Access Token

    loop
    C->>+MRS: Call MCP API with Access Token
    MRS-->>-C: MCP Response with Data
    end
"""

# mcp/pages/seps/1686-tasks.md:1035 (indented inside an MDX component upstream)
SUBTASKS = """\
sequenceDiagram
    participant C as Client
    participant S as Server

    Note over C,S: Server Responds with Subtask Requirements
    C->>S: tasks/get (taskId: "deploy-123")
    S->>C: status: working<br/>childTasks: [{<br/>  taskId: "build-456",<br/>  toolName: "run_build",<br/>  arguments: {...}<br/>}, {<br/>  taskId: "test-789",<br/>  toolName: "run_tests",<br/>  arguments: {...}<br/>}]
"""

# mcp/pages/specification/2026-07-28/client/elicitation.md:547
ELICITATION = """\
sequenceDiagram
    participant User
    participant UserAgent as User Agent (Browser)
    participant 3AS as 3rd Party AS
    participant 3RS as 3rd Party RS
    participant Client as MCP Client
    participant Server as MCP Server

    Client->>Server: tools/call
    Note over Server: Needs 3rd-party authorization for user
    Note over Server: Store state (bind the elicitation request to the user)
    Note over Server: generate requestState that encodes information about the original request and user.
    Server->>Client: InputRequiredResult<br/>(mode: "url", url: "https://mcp.example.com/connect?...", requestState)

    Client->>User: Present consent to open URL
    User->>Client: Provide consent
    Client->>UserAgent: Open URL
    Client->>Server: Accept response
    UserAgent->>Server: Load connect route

    Note over Server: Confirm: user is logged into MCP Server or MCP AS<br>Confirm: elicitation user matches session user
    Server->>UserAgent: Redirect to third-party authorization endpoint
    UserAgent->>3AS: Load authorize route
    Note over 3AS,User: User interaction (OAuth flow):<br>User consents to scoped MCP Server access
    3AS->>UserAgent: redirect to MCP Server's redirect_uri
    UserAgent->>Server: load redirect_uri page
    Note over Server: Confirm: redirect_uri belongs to MCP Server
    Server->>3AS: Exchange authorization code for  OAuth tokens
    3AS->>Server: Grants tokens
    Note over Server: Bind tokens to MCP user identity
    Client->>Server: tools/call (ElicitResults, requestState)
    Note over Server: Retrieve token bound to user identity
    Server->>3RS: Call 3rd-party API
"""

# mcp/pages/specification/2025-11-25/basic/authorization.md:151
NESTED_ALT = """\
sequenceDiagram
    participant C as Client
    participant M as MCP Server (Resource Server)
    participant A as Authorization Server

    Note over C: Attempt unauthenticated MCP request
    C->>M: MCP request without token
    M-->>C: HTTP 401 Unauthorized (may include WWW-Authenticate header)

    alt Header includes resource_metadata
        Note over C: Extract resource_metadata URL from header
        C->>M: GET resource_metadata URI
        M-->>C: Resource metadata with authorization server URL
    else No resource_metadata in header
        Note over C: Fallback to well-known URI probing
        Note over M: _Not applicable if the MCP server is at the root_
        C->>M: GET /.well-known/oauth-protected-resource/mcp
        alt Sub-path metadata found
            M-->>C: Resource metadata with authorization server URL
        else Sub-path not found
            C->>M: GET /.well-known/oauth-protected-resource
            alt Root metadata found
                M-->>C: Resource metadata with authorization server URL
            else Root metadata not found
                Note over C: Abort or use pre-configured values
            end
        end
    end

    Note over C: Validate RS metadata,<br />build AS metadata URL
    C->>A: GET Authorization server metadata endpoint
    Note over C,A: Try OAuth 2.0 and OpenID Connect<br/>discovery endpoints in priority order
    A-->>C: Authorization server metadata
"""

# mcp/pages/community/sep-guidelines.md:50
SEP_FLOW = """\
flowchart TD
    Idea["Idea"]
    AwaitingSponsor{"Awaiting Sponsor<br/>(up to 6 months)"}
    Draft["Draft"]
    Dormant["Dormant<br/>(no sponsor)"]
    Withdrawn["Withdrawn<br/>(by author)"]
    InReview["In-Review"]
    Decision{"Core Maintainers decide"}
    Accepted["Accepted"]
    Rejected["Rejected"]
    Final["Final"]

    Idea -->|"Submit PR with SEP file"| AwaitingSponsor
    AwaitingSponsor --> Draft
    AwaitingSponsor --> Dormant
    AwaitingSponsor --> Withdrawn
    Draft -->|"Sponsor reviews"| InReview
    InReview --> Decision
    Decision --> Accepted
    Decision --> Rejected
    Accepted -->|"Reference implementation +<br/>conformance test complete"| Final
"""

# mcp/pages/specification/2024-11-05/architecture/index.md:15
ARCHITECTURE = """\
graph LR
    subgraph "Application Host Process"
        H[Host]
        C1[Client 1]
        C2[Client 2]
        C3[Client 3]
        H --> C1
        H --> C2
        H --> C3
    end

    subgraph "Local machine"
        S1[Server 1<br>Files & Git]
        S2[Server 2<br>Database]
        R1[("Local<br>Resource A")]
        R2[("Local<br>Resource B")]

        C1 --> S1
        C2 --> S2
        S1 <--> R1
        S2 <--> R2
    end

    subgraph "Internet"
        S3[Server 3<br>External APIs]
        R3[("Remote<br>Resource C")]

        C3 --> S3
        S3 <--> R3
    end
"""

# mcp/pages/docs/2024-11-05/develop/clients/client-best-practices.md:254
CODE_MODE = """\
flowchart LR
    subgraph Host["MCP Host"]
        A[LLM] -->|writes code| B[Sandbox]
        B -->|function call| C[MCP Client]
        C -->|return value| B
        B -->|console output| A
    end
    C -->|tool call| D[MCP Server A]
    C -->|tool call| E[MCP Server B]
    D -->|result| C
    E -->|result| C
"""

# mcp/pages/docs/2024-11-05/learn/architecture.md:44
DEDICATED = """\
graph TB
    subgraph "MCP Host (AI Application)"
        Client1["MCP Client 1"]
        Client2["MCP Client 2"]
        Client3["MCP Client 3"]
        Client4["MCP Client 4"]
    end

    ServerA["MCP Server A - Local<br/>(e.g. Filesystem)"]
    ServerB["MCP Server B - Local<br/>(e.g. Database)"]
    ServerC["MCP Server C - Remote<br/>(e.g. Sentry)"]

    Client1 ---|"Dedicated<br/>connection"| ServerA
    Client2 ---|"Dedicated<br/>connection"| ServerB
    Client3 ---|"Dedicated<br/>connection"| ServerC
    Client4 ---|"Dedicated<br/>connection"| ServerC
"""

# platform/pages/about-claude/use-case-guides/ticket-routing.md:1431
TICKETS = """\
---
config:
  flowchart:
    nodeSpacing: 10
    rankSpacing: 60
    padding: 8
    wrappingWidth: 300
---
flowchart LR
  accTitle: Hierarchy of ticket classifiers
  accDescr: Classifier hierarchy routing tickets to Technical Issues, Billing Questions, or General Inquiries, each with a sub-classifier
  tickets[Support Tickets] --> technical[Technical Issues]
  tickets --> billing[Billing Questions]
  tickets --> general[General Inquiries]
  technical --> software[Software Installation]
  technical --> hardware[Hardware Troubleshooting]
  technical --> network[Network Connectivity]
  technical --> technicalMore[...]
  billing --> invoice[Invoice Clarification]
  billing --> payment[Payment Processing]
  billing --> refund[Refund Requests]
  general --> product[Product Information]
  general --> order[Order Status]
  general --> partnership[Partnership Opportunities]
  general --> generalMore[...]
"""

# mcp/pages/seps/1686-tasks.md:369
TASK_STATES = """\
stateDiagram-v2
    [*] --> submitted

    submitted --> working
    submitted --> terminal

    working --> input_required
    working --> terminal

    input_required --> working
    input_required --> terminal

    terminal --> [*]

    note right of terminal
        Terminal states:
        • completed
        • failed
        • cancelled
        • unknown
    end note
"""

# mcp/pages/seps/3398-release-cycle-updates.md:63
RELEASES = """\
---
config:
    gantt:
        displayMode: compact
        leftPadding: 140
---
gantt
    title Eight-month cycles, six months between releases
    dateFormat YYYY-MM-DD
    axisFormat %b
    tickInterval 1month
    todayMarker off

    section March release
    Planning      :march_plan, 2027-07-28, 2027-09-28
    CM review     :march_review, 2027-09-28, 2028-01-13
    Stabilization :march_stabilize, 2028-01-13, 2028-03-28

    section September release
    Planning      :september_plan, 2028-01-28, 2028-03-28
    CM review     :september_review, 2028-03-28, 2028-07-12
    Stabilization :september_stabilize, 2028-07-12, 2028-09-26

    section Releases
    March         :milestone, march_release, 2028-03-28, 0d
    September     :milestone, september_release, 2028-09-26, 0d
"""

CORPUS = {
    "lifecycle": LIFECYCLE,
    "skills": SKILLS,
    "transports": TRANSPORTS,
    "middleware": MIDDLEWARE,
    "build_client": BUILD_CLIENT,
    "idp": IDP,
    "subtasks": SUBTASKS,
    "elicitation": ELICITATION,
    "nested_alt": NESTED_ALT,
    "sep_flow": SEP_FLOW,
    "architecture": ARCHITECTURE,
    "code_mode": CODE_MODE,
    "dedicated": DEDICATED,
    "tickets": TICKETS,
    "task_states": TASK_STATES,
    "releases": RELEASES,
}


def ok(source: str, width: int = 78) -> Rendered:
    """Render and assert every invariant, including that all labels survive."""
    r = render(source, width)
    assert problems(source, r, width) == []
    return r


# --- corpus snippets: method and invariants at several widths ---------------

EXPECTED = {
    "lifecycle": "sequence",
    "skills": "sequence",
    "transports": "sequence",
    "middleware": "sequence",
    "build_client": "sequence",
    "idp": "sequence-list",
    "subtasks": "sequence",
    "elicitation": "sequence-list",
    "nested_alt": "sequence",
    "sep_flow": "flowchart",
    "architecture": "flowchart",
    "code_mode": "flowchart",
    "dedicated": "flowchart",
    "tickets": "flowchart",
    "task_states": "state",
    "releases": "gantt",
}


@pytest.mark.parametrize("name", sorted(CORPUS))
def test_corpus_at_78(name):
    assert ok(CORPUS[name]).method == EXPECTED[name]


@pytest.mark.parametrize("width", [40, 50, 60, 70, 100, 160])
@pytest.mark.parametrize("name", sorted(CORPUS))
def test_corpus_other_widths(name, width):
    ok(CORPUS[name], width)


def test_deterministic():
    for src in CORPUS.values():
        assert render(src).text == render(src).text


# --- sequence diagrams --------------------------------------------------------


def test_sequence_activations_rect_and_async():
    text = ok(LIFECYCLE).text
    assert "┃" in text  # activation bars
    assert "┌┄" in text and "┆" in text  # rect: a dotted frame
    assert "─>┃" not in text and "╌>┃" in text  # async arrow head ends at the bar
    assert "╭" in text and "Initialization Phase" in text  # notes are rounded boxes


def test_sequence_blocks_and_actor():
    text = ok(SKILLS).text
    for title in ("opt [Discover a catalog]", "alt [Model selects a skill]",
                  "else [User selects a skill]", "break [Lookup failed]",
                  "loop [Supporting files requested while the skill is active]"):
        assert title in text
    assert "/|\\" in text  # the actor figure
    assert "├──┐" in text and "◄─┘" in text  # self message


def test_sequence_nested_frames():
    text = ok(TRANSPORTS).text
    lines = text.split("\n")
    loop = next(l for l in lines if "loop [while connection remains open]" in l)
    assert loop.startswith("│ ┌─")  # nested inside the alt frame


def test_sequence_autonumber_title_and_description():
    text = ok(MIDDLEWARE).text
    lines = text.split("\n")
    assert lines[0] == "How a request and its response pass through middleware"
    assert "1. request" in text and "8. response" in text
    assert "next(request) to pass it to the SDK core" in " ".join(text.split())


def test_sequence_front_matter_and_bidirectional():
    text = ok(BUILD_CLIENT).text
    assert "theme" not in text
    assert re.search("◄─+►", text)


def test_sequence_indented_lines_keep_their_shape():
    lines = ok(SUBTASKS).text.split("\n")
    col = {key: next(l.index(key) for l in lines if key in l)
           for key in ("childTasks", "taskId: \"build", "}, {")}
    assert col["taskId: \"build"] == col["childTasks"] + 2
    assert col["}, {"] == col["childTasks"]


def test_sequence_list_fallback():
    r = ok(ELICITATION)
    assert r.method == "sequence-list"
    text = r.text
    assert text.startswith("Participants:")
    assert "  • User Agent (Browser)" in text
    assert re.search(r"^ 1\. MCP Client ──► MCP Server: tools/call$", text, re.M)
    assert "Note over 3rd Party AS, User: User interaction (OAuth flow):" in text
    assert "15. MCP Server ──► 3rd Party RS: Call 3rd-party API" in text


def test_sequence_list_blocks_and_arrow_kinds():
    text = ok(IDP).text
    assert "┌─ (highlighted)" in text  # rect
    assert "┌─ loop" in text and "└─" in text
    assert "MCP Client ─── Identity Provider" in text  # -> : no arrowhead
    assert "Identity Provider ╌╌╌ MCP Client" in text  # --> : dotted, no head
    assert "MCP Client ╌╌► Browser" in text  # -->>
    assert re.search(r"^│ 11\. MCP Client ──► MCP Resource Server", text, re.M)


def test_sequence_narrow_falls_back_but_keeps_everything():
    r = ok(NESTED_ALT, 50)
    assert r.method == "sequence-list"
    assert "┌─ alt [Header includes resource_metadata]" in r.text
    assert "│ │ ├─ else [Root metadata not found]" in r.text


def test_sequence_constructs_not_in_corpus():
    src = """sequenceDiagram
    title: Odds and ends
    box Aqua Front end
    participant A as Alice
    participant B
    end
    participant C
    A->>B: hello
    B-xC: dropped
    C-)A: async
    create participant D
    A->>D: make
    destroy D
    par First
    A->>B: one
    and Second
    A->>C: two
    end
    critical Must
    B->>C: x
    option Fallback
    B->>A: y
    end
    Note left of A: left
    Note right of C: right
    A->>A: wrap: self note
    %% a comment
    """
    r = ok(src)
    assert r.method in ("sequence", "sequence-list")
    for want in ("Odds and ends", "Front end", "Alice", "dropped", "par [First]",
                 "and [Second]", "critical [Must]", "option [Fallback]"):
        assert want in r.text
    assert "a comment" not in r.text


def test_sequence_unknown_statement_shows_source():
    src = "sequenceDiagram\n    A->>B: hi\n    links A: {\"Dashboard\": \"https://x.example\"}\n"
    r = ok(src)
    assert r.method == "source"
    assert "https://x.example" in r.text


# --- flowcharts and state diagrams --------------------------------------------


def test_flowchart_shapes_and_edge_labels():
    text = ok(SEP_FLOW).text
    assert "╱──" in text  # decision shape
    assert "Submit PR with SEP file" in text
    assert "▼" in text


def test_flowchart_subgraphs_lr():
    text = ok(ARCHITECTURE).text
    for title in ("Application Host Process", "Local machine", "Internet"):
        assert f"┌─ {title} ─" in text
    assert "◄───►" in text  # <--> edges
    assert "├────────────┤" in text  # cylinder
    assert max(tw(l) for l in text.split("\n")) <= 78


def test_flowchart_cycles_are_drawn():
    text = ok(CODE_MODE).text
    assert "▲" in text  # back edges point up
    assert "┌─ MCP Host ─" in text


def test_flowchart_undirected_edges_and_direction_switch():
    r = ok(DEDICATED)
    assert r.method == "flowchart"
    assert "Dedicated" in r.text and "►" not in r.text and "▼" not in r.text


def test_flowchart_list_fallback():
    r = ok(SEP_FLOW, 44)
    assert r.method == "flowchart-list"
    assert r.text.startswith("Idea\n  └─")
    assert "Submit PR with SEP file" in r.text


def test_flowchart_syntax_variants():
    src = """graph LR;
    A[Start] -- label one --> B(Round)
    B -.-> C([Stadium]) & D[[Sub]]
    C ==> E[(Data)] --> F((Circle))
    D --o G{{Hex}}
    G --x H>Flag]
    H ~~~ I[/Lean/]
    I -. dotted label .-> J[\\Back\\]
    J == thick label ==> K@{ shape: cyl, label: "New syntax" }
    K:::warm --> L["`**Markdown** label`"]
    classDef warm fill:#f96
    style A fill:#fff
    click A "https://example.com" "tooltip"
    """
    r = ok(src)
    assert r.method in ("flowchart", "flowchart-list")
    for want in ("Start", "label one", "Stadium", "Sub", "Data", "Circle", "Hex",
                 "Flag", "Lean", "dotted label", "Back", "thick label", "New syntax",
                 "Markdown label"):
        assert want in " ".join(r.text.split())
    assert "**" not in r.text and "warm" not in r.text


def test_flowchart_edges_to_subgraphs_and_self_loops_use_the_list():
    src = """flowchart TB
    subgraph one [First group]
      a1 --> a2
    end
    c1 --> one
    a2 --> a2
    """
    r = ok(src)
    assert r.method == "flowchart-list"
    assert "First group" in r.text and "c1" in r.text


def test_state_diagram():
    text = ok(TASK_STATES).text
    assert "●" in text and "◉" in text
    assert "╌╌╌" in text  # note connector
    assert "• unknown" in text


def test_state_composite_and_pseudostates():
    src = """stateDiagram-v2
    direction LR
    state "Waiting for input" as Wait
    [*] --> Wait
    Wait --> Busy : got input
    state Busy {
        [*] --> Parse
        Parse --> Run
        Run --> [*]
    }
    state choose <<choice>>
    Busy --> choose
    choose --> Done : ok
    choose --> Wait : retry
    Done: All finished
    note left of Done : final note
    """
    r = ok(src)
    assert r.method in ("state", "state-list")
    for want in ("Waiting for input", "got input", "Parse", "retry", "All finished",
                 "final note"):
        assert want in r.text


# --- Gantt charts ---------------------------------------------------------------


def test_gantt():
    r = ok(RELEASES)
    assert r.method == "gantt"
    assert "█" in r.text and "◆" in r.text
    assert "  Planning       2027-07-28 to 2027-09-28" in r.text
    assert "  March          2028-03-28 (milestone)" in r.text


def test_gantt_relative_dates_and_unknown_format():
    src = """gantt
    dateFormat YYYY-MM-DD
    section A
    First :a1, 2024-01-01, 30d
    Second :after a1, 2w
    Third :crit, 5d
    """
    r = ok(src)
    assert r.method == "gantt"
    assert "2024-01-31 to 2024-02-14" in r.text
    assert "(crit)" in r.text
    r = ok(src.replace("YYYY-MM-DD", "DD.MM.YYYY"))
    assert r.method == "gantt-list"
    assert "a1, 2024-01-01, 30d" in r.text


# --- robustness -------------------------------------------------------------------


@pytest.mark.parametrize("src", [
    "", "   ", "\n\n", "graph", "sequenceDiagram", "gantt", "stateDiagram-v2",
    "---\nconfig:\n", "not a diagram", "classDiagram\n  Animal <|-- Duck",
    "pie title Pets\n  \"Dogs\" : 386", "😀" * 60, "x" * 400, "\t\tgraph TD\n\tA-->B",
    "graph TD\n  A[unclosed --> B", "sequenceDiagram\n  end", "sequenceDiagram\n  A->>",
    "flowchart TD\n  A --> B\n  subgraph S\n  C\n", "stateDiagram\n state X {\n state X {",
])
@pytest.mark.parametrize("width", [1, 2, 10, 40, 78])
def test_never_raises_and_keeps_invariants(src, width):
    r = render(src, width)
    lines = r.text.split("\n")
    assert r.text.strip()
    assert "\t" not in r.text
    assert lines[0].strip() and lines[-1].strip()
    assert all(l == l.rstrip() and tw(l) <= max(2, width) for l in lines)


def test_unsupported_types_show_source_with_labels():
    src = "classDiagram\n    class Duck {\n        +swim()\n    }\n"
    r = ok(src)
    assert r.method == "source" and "+swim()" in r.text


def test_wide_and_odd_characters():
    src = """sequenceDiagram
    participant A as 東京サーバー
    participant B as Café
    A->>B: 日本語のメッセージ 😀 with\ttab and &amp; entity and #9829;
    B-->>A: x́ combining
    """
    r = ok(src, 40)
    assert "東京サーバー" in r.text and "&" in r.text and "♥" in r.text
    assert all(tw(l) <= 40 for l in r.text.split("\n"))


def test_mutated_corpus_never_breaks():
    rng = random.Random(1234)
    junk = ["\t", "\x00", "漢字", "<br>", ";", ":", "-->", "|", "[", "{", "\"", "end",
            "loop x", "else", "subgraph x", "A-->A", "state X {", "}", "activate A"]
    for _ in range(400):
        lines = rng.choice(list(CORPUS.values())).split("\n")
        for _ in range(rng.randint(1, 4)):
            i = rng.randrange(len(lines))
            op = rng.random()
            if op < 0.3:
                del lines[i]
            elif op < 0.6:
                lines.insert(i, rng.choice(junk))
            else:
                k = rng.randint(0, len(lines[i]))
                lines[i] = lines[i][:k] + rng.choice(junk) + lines[i][k:]
        width = rng.choice([20, 40, 78])
        r = render("\n".join(lines), width)
        out = r.text.split("\n")
        assert r.text.strip() and "\t" not in r.text
        assert all(l == l.rstrip() and tw(l) <= width for l in out)


# --- helpers ------------------------------------------------------------------------


def test_text_width():
    assert tw("abc") == 3
    assert tw("東京") == 4
    assert tw("é") == 1
    assert tw("─│►") == 3


def test_wrap():
    assert wrap("one two three", 7) == ["one two", "three"]
    assert wrap("GET /.well-known/oauth-authorization-server", 20) == [
        "GET", "/.well-known/oauth-", "authorization-server"]  # breaks after / and -
    for line in wrap("a" * 50, 7):
        assert tw(line) <= 7
    assert wrap("  indented text here", 10) == ["  indented", "  text", "  here"]


def test_label_extraction():
    src = """sequenceDiagram
    participant A as Alice<br/>Smith
    B->>A: hi there
    Note over A,B: a note
    loop every day
    A-->>B: ok
    end
    """
    assert labels(src) == ["Alice", "Smith", "hi there", "a note", "every day", "ok", "B"]
    assert labels(SEP_FLOW)[:3] == ["Idea", "Awaiting Sponsor", "(up to 6 months)"]


def test_missing_labels_is_not_fooled():
    r = render(SKILLS)
    assert missing_labels(SKILLS, r.text) == []
    damaged = r.text.replace("Lookup failed", "Lookup")
    assert missing_labels(SKILLS, damaged) == ["Lookup failed"]
    # wrapped across lines still counts as present
    assert missing_labels("graph TD\n  A[alpha beta gamma]", "alpha beta\ngamma") == []


def test_problems_reports_dropped_duplicates():
    src = "sequenceDiagram\n  A->>B: response\n  B->>A: response\n"
    r = render(src)
    assert problems(src, r, 78) == []
    once = r.text.replace("response", "reply", 1)
    assert any("response" in p for p in problems(src, Rendered(once, r.method), 78))


def test_mermaid_blocks():
    md = """Intro

```mermaid theme={null}
graph TD
  A-->B
```

  <Tabs>
  ```mermaid
  sequenceDiagram
    A->>B: x
  ```
  </Tabs>

````markdown
```mermaid
graph TD
  NotADiagram
```
````

~~~mermaid
graph LR
  C-->D
~~~
"""
    blocks = mermaid_blocks(md)
    assert [line for line, _ in blocks] == [3, 9, 22]
    assert blocks[1][1] == "sequenceDiagram\n  A->>B: x"
    assert all("NotADiagram" not in src for _, src in blocks)


def test_state_note_on_composite():
    # Found by fuzzing: notes may be attached to composite states.
    src = "stateDiagram-v2\n[*] --> A\nstate X {\n  A --> B\n}\nnote right of X\n  about X\nend note\n"
    r = ok(src)
    assert r.method == "state-list" and "Note (right): about X" in r.text
