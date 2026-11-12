---
title: Get Plugin Version
url: https://platform.claude.com/docs/en/api/python/beta/organization/plugins/versions/retrieve
---

# Get Plugin Version

`beta.organization.plugins.versions.retrieve(version, **kwargs) -> BetaPluginVersion`

**GET** `/v1/organizations/plugins/{plugin_id}/versions/{version}`

Retrieve one version of a Plugin by its ID, or the Plugin's newest version.

**Accepted credentials:** an Admin API key with the `read:plugins` or `read:org_audit` scope, or a Compliance Access Key with the `read:compliance_org_data` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

## Parameters

- `plugin_id: str` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `version: str` (path parameter)

  ID of the Plugin Version (prefixed `pluginver_`), or `latest` for the newest one.

- `organization_id: Optional[str]` (query parameter)

  For a `read:org_audit` or `read:compliance_org_data` key created for all of a parent organization's linked organizations: a child organization of that parent to read instead of the organization the key was created in, given as the organization's UUID or its `org_`-prefixed ID. A value that is neither returns a 400; an organization that is not a child of the key's parent, or where the Plugins API is not available, returns a 404. Any other key may pass only its own organization's ID here; another organization returns a 404. A key with no organization of its own must always pass `organization_id`.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

## Returns

- `class BetaPluginVersion`

  - `type: Literal["plugin_version"]`

    Always `plugin_version`.

    default: plugin_version

  - `id: str`

    The version's ID.

  - `components: Optional[List[BetaPluginComponent]]`

    What the version contains; null when not enumerated.

    - `type: Literal["agent", "cli", "command", 3 more]`

      The kind of component.

      - `"agent"`

      - `"cli"`

      - `"command"`

      - `"hook"`

      - `"mcp_server"`

      - `"skill"`

    - `description: Optional[str]`

      What the component declares about itself; always null for MCP servers, hooks, and CLIs.

    - `name: str`

      The component's name: a skill's, command's or agent's name, an MCP server's key in the manifest, the event a hook runs on, or a CLI's executable.

  - `content_scan: Optional[BetaPluginContentScan]`

    This version's content scan; null when it has not been scanned.

    - `assessment: Optional[Literal["fail", "pass", "unknown", "warn"]]`

      The scan's verdict; set only when `status` is `completed`. A `warn` can mean a `fail` that was allowed in claude.ai.

      - `"fail"`

      - `"pass"`

      - `"unknown"`

      - `"warn"`

    - `reason: Optional[str]`

      The primary mechanism behind a `warn` or `fail`, such as `credential-exposure` or `guardrail-tampering`; a mechanism this API does not yet name reads as `other`. Null on a `pass`, whenever `assessment` is null, and when no mechanism is reported for the verdict.

    - `status: Literal["completed", "errored", "processing"]`

      `processing` while a scan runs, `completed` when it ran to completion, `errored` when it could not run. Once a scan of the version has completed, `content_scan` describes the newest completed scan, even while a later scan runs. While the scan outcome cannot be read, `status` is `errored` instead.

      - `"completed"`

      - `"errored"`

      - `"processing"`

  - `created_at: datetime`

    RFC 3339.

    format: date-time

  - `created_by: Optional[CreatedBy]`

    Who uploaded this version; null when not recorded.

    - `class BetaPluginUserActor`

      - `type: Literal["user_actor"]`

        A member of the organization.

        default: user_actor

      - `email_address: Optional[str]`

        The member's email address; may be null, for example when they are no longer a member of the organization.

      - `user_id: str`

        The member's User ID.

    - `class BetaPluginAPIActor`

      - `type: Literal["api_actor"]`

        An Admin API key, in the same form the Compliance API activity feed uses for it.

        default: api_actor

      - `api_key_id: str`

        The key's ID.

  - `description: Optional[str]`

    The manifest's description; null when it declares none. The value can be longer than 500 characters, the limit on `description` in an uploaded manifest. A description that the manifest takes from a `SKILL.md` is cut to its first 500 characters. So if the manifest's description is the first 500 characters of exactly one distinct skill `description` in `components`, that skill `description` is returned instead.

  - `display_name: Optional[str]`

    The manifest's display name; null when it declares none.

  - `manifest_version: Optional[str]`

    The manifest's `version`, normalized for display: one leading `v` or `V` is dropped, and the result is returned only if it is 1 to 64 characters, starts with a digit, and uses only ASCII letters, digits, `.`, `+`, and `-`; otherwise `null`. For example, `"v1.4.0"` is returned as `"1.4.0"`, and `"latest"` as `null`. For a synchronized plugin, the `version` of its `marketplace.json` entry can take the place of the manifest's `version`. It is also `null` for a version stored before claude.ai began recording this field (August 2026).

  - `plugin_id: str`

    The Plugin's ID.

  - `reach: Optional[Literal["contained", "privileged", "remote"]]`

    How far the version reaches: `remote`, `privileged`, `contained`, or `null`, as defined on the Plugin's `reach`.

    - `"contained"`

    - `"privileged"`

    - `"remote"`

  - `release_notes: Optional[str]`

    As supplied with the upload; null when none were supplied.

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_plugin_version = client.beta.organization.plugins.versions.retrieve(
    version="version",
    plugin_id="plugin_id",
)
print(beta_plugin_version.id)
```

### Response (200)

```json
{
  "id": "pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
  "components": [
    {
      "description": "description",
      "name": "review-pr",
      "type": "skill"
    }
  ],
  "content_scan": {
    "assessment": "warn",
    "reason": "credential-exposure",
    "status": "completed"
  },
  "created_at": "2026-03-14T09:26:53.589793Z",
  "created_by": {
    "email_address": "user@example.com",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "description": "Reviews pull requests against your team's conventions.",
  "display_name": "Code Review Helper",
  "manifest_version": "1.2.0",
  "plugin_id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
  "reach": "contained",
  "release_notes": "Adds a review checklist for database migrations.",
  "type": "plugin_version"
}
```
