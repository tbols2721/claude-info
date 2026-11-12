---
title: Plugins
url: https://platform.claude.com/docs/en/api/python/beta/organization/plugins
---

# Plugins

## Create Plugin

`beta.organization.plugins.create(**kwargs) -> BetaPlugin`

**POST** `/v1/organizations/plugins`

Create an organization-owned Plugin and its first version by uploading the
version's files.

The upload is `multipart/form-data`: the version's files (`files`, each part sent
as `files[]`), with an optional `marketplace_id` and `release_notes`. The manifest's `name` becomes the
Plugin's `name`, and `display_name`, `description` and `manifest_version` come
from the manifest too.

`name` may contain lowercase letters (from any alphabet), digits, and hyphens, up
to 64 characters. Uppercase letters, spaces, underscores, and other punctuation are
rejected.

The `name` must be unique within the marketplace: a name already taken
returns a 409 with `error_code` `plugin_name_taken` and, when a Plugin holds it,
that Plugin's ID in `details.plugin_id`. A Plugin going into the organization's
library marketplace is also refused with a 409 when one of its skills has the name of
an organization skill that this API does not list: `error_code`
`skill_name_taken`, with that name in `details.skill_name`; rename the skill, or
remove the organization skill in claude.ai. A 503 with `error_code`
`registration_pending` means the Plugin and its version were stored (their IDs are
in `details`) but are not yet usable in claude.ai: do not retry the create (the
retry would return `plugin_name_taken`); create a version on the stored Plugin
instead, which completes it.

For a worked example, see [Create a plugin](https://platform.claude.com/docs/en/manage-claude/plugins-api?sdk_languages=python#create-a-plugin)
in the Plugins API guide.

**Accepted credentials:** an Admin API key with the `write:plugins` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

### Parameters

- `files: Sequence[FileTypes]`

  The version's files: one part per file, the part's filename being the file's path within the Plugin (for example `skills/review-pr/SKILL.md`), or a single `.zip` or `.plugin` archive holding them all. On the wire each part is named `files[]`, and a part named plain `files` is not read; with cURL, `-F 'files[]=@SKILL.md;filename=skills/review-pr/SKILL.md'`. The files must include the manifest, `.claude-plugin/plugin.json`.

- `marketplace_id: Optional[str]`

  ID of the organization-owned plugin marketplace to create the Plugin in (prefixed `marketplace_`). It must be a `manual` marketplace, one whose Plugins are uploaded rather than synchronized from a repository. When omitted, the Plugin is created in the organization's library marketplace, an organization-owned `manual` marketplace created on first use.

- `release_notes: Optional[str]`

  Release notes stored with the version and shown in its version history in claude.ai; up to 5,000 characters.

  maxLength: 5000

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

### Returns

- `class BetaPlugin`

  - `type: Literal["plugin"]`

    Always `plugin`.

    default: plugin

  - `id: str`

    The Plugin's ID.

  - `components: Optional[List[BetaPluginComponent]]`

    What the served version contains; null when not enumerated.

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

    The served version's content scan; null when it has not been scanned.

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

    Who created the Plugin; null when no creator is recorded.

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

    The served version's description.

  - `display_name: Optional[str]`

    The served version's display name.

  - `latest_version_id: str`

    The newest version.

  - `manifest_version: Optional[str]`

    The served version's manifest `version`, normalized for display, or `null` (the Plugin Version's `manifest_version` says how and when).

  - `marketplace_id: str`

    The ID of the plugin marketplace the Plugin lives in.

  - `name: str`

    Lowercase identifier, unique within its plugin marketplace. Fixed for an organization-owned Plugin's lifetime; a member-owned Plugin's changes when its owner renames it in claude.ai, while its `id` stays the same.

  - `organization_installation_preference: Optional[Literal["auto_install", "available", "not_available", "required"]]`

    Organization-owned Plugin: the organization-wide installation setting every member gets unless an RBAC Group they belong to holds its own — the Plugin's own setting, or its plugin marketplace's default. Null for a member-owned Plugin, which has shares instead. One of `required`, `auto_install`, `available`, `not_available`; a value this API does not yet name is returned as stored.

    - `"auto_install"`

    - `"available"`

    - `"not_available"`

    - `"required"`

  - `organization_installation_preference_inherited: Optional[bool]`

    Organization-owned Plugin: true while it has no organization-wide setting of its own and `organization_installation_preference` is its plugin marketplace's default. Null for a member-owned Plugin.

  - `owner: Owner`

    Who owns the Plugin: the organization, or the member whose personal plugin marketplace it lives in.

    - `class BetaPluginOwnerOrganization`

      - `type: Literal["organization"]`

        The Plugin lives in a plugin marketplace the organization owns.

        default: organization

    - `class BetaPluginOwnerUser`

      - `type: Literal["user"]`

        The Plugin lives in one member's personal plugin marketplace.

        default: user

      - `user_id: str`

        The member's User ID.

  - `reach: Optional[Literal["contained", "privileged", "remote"]]`

    How far the served version reaches, or `null` if it is not classified.

    `remote` means it declares an MCP server or a CLI, or something that counts as one. `privileged` means it is not `remote`, but declares a hook (of any type, even one that posts to a URL), monitor, language server, Claude Code workflow (any file in a `workflows/` folder at its root counts as one), or settings, or has a skill, command, or other Markdown file whose frontmatter pre-approves tools (`allowed-tools` with any value other than an empty one or one that names only `AskUserQuestion`, `TodoWrite`, and `ToolSearch`). Otherwise it is `contained`.

    If the frontmatter of a skill, command, or other Markdown file that could change the value could not be read, or was past a size limit, the version is `null` or `privileged` (or `remote`, if something else it declares makes it `remote`), not `contained`. The value is normally worked out when a version is stored, under the rules of that time, so an older version can be `null`, `contained` where the same files stored today would be `privileged`, `remote`, or `null`, or `privileged` where they would be `remote`.

    - `"contained"`

    - `"privileged"`

    - `"remote"`

  - `served_version_id: str`

    The version claude.ai serves to members.

  - `served_version_pinned: bool`

    True once the served version has been pinned, through Update Plugin or in claude.ai. While false, a new version normally becomes the served version when it is stored. While the newest version is not the served version, as when a version saved in claude.ai is waiting for its content scan, `served_version_id` differs from `latest_version_id`.

  - `updated_at: datetime`

    RFC 3339. Moves on a served-version change (including pinning an unpinned Plugin to the version it already serves) and, normally, on a new version. A version saved in claude.ai that waits for its content scan moves it when it becomes the served version, and not necessarily when it is stored. A change to the Plugin's installation settings or shares does not move it.

    format: date-time

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_plugin = client.beta.organization.plugins.create(
    files=[b"Example data"],
)
print(beta_plugin.id)
```

#### Response (200)

```json
{
  "id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
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
  "latest_version_id": "pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
  "manifest_version": "1.2.0",
  "marketplace_id": "marketplace_01HxQ3v9KpZ2mTn8RwLc4Ys7",
  "name": "code-review-helper",
  "organization_installation_preference": "available",
  "organization_installation_preference_inherited": true,
  "owner": {
    "type": "organization"
  },
  "reach": "contained",
  "served_version_id": "pluginver_01K9wPcHd4Rm2Tx8Vq6Ln3Sb",
  "served_version_pinned": true,
  "type": "plugin",
  "updated_at": "2026-03-14T09:26:53.589793Z"
}
```

## Get Plugin

`beta.organization.plugins.retrieve(plugin_id, **kwargs) -> BetaPlugin`

**GET** `/v1/organizations/plugins/{plugin_id}`

Retrieve a Plugin by ID.

**Accepted credentials:** an Admin API key with the `read:plugins` or `read:org_audit` scope, or a Compliance Access Key with the `read:compliance_org_data` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

### Parameters

- `plugin_id: str` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

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

### Returns

- `class BetaPlugin`

  - `type: Literal["plugin"]`

    Always `plugin`.

    default: plugin

  - `id: str`

    The Plugin's ID.

  - `components: Optional[List[BetaPluginComponent]]`

    What the served version contains; null when not enumerated.

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

    The served version's content scan; null when it has not been scanned.

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

    Who created the Plugin; null when no creator is recorded.

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

    The served version's description.

  - `display_name: Optional[str]`

    The served version's display name.

  - `latest_version_id: str`

    The newest version.

  - `manifest_version: Optional[str]`

    The served version's manifest `version`, normalized for display, or `null` (the Plugin Version's `manifest_version` says how and when).

  - `marketplace_id: str`

    The ID of the plugin marketplace the Plugin lives in.

  - `name: str`

    Lowercase identifier, unique within its plugin marketplace. Fixed for an organization-owned Plugin's lifetime; a member-owned Plugin's changes when its owner renames it in claude.ai, while its `id` stays the same.

  - `organization_installation_preference: Optional[Literal["auto_install", "available", "not_available", "required"]]`

    Organization-owned Plugin: the organization-wide installation setting every member gets unless an RBAC Group they belong to holds its own — the Plugin's own setting, or its plugin marketplace's default. Null for a member-owned Plugin, which has shares instead. One of `required`, `auto_install`, `available`, `not_available`; a value this API does not yet name is returned as stored.

    - `"auto_install"`

    - `"available"`

    - `"not_available"`

    - `"required"`

  - `organization_installation_preference_inherited: Optional[bool]`

    Organization-owned Plugin: true while it has no organization-wide setting of its own and `organization_installation_preference` is its plugin marketplace's default. Null for a member-owned Plugin.

  - `owner: Owner`

    Who owns the Plugin: the organization, or the member whose personal plugin marketplace it lives in.

    - `class BetaPluginOwnerOrganization`

      - `type: Literal["organization"]`

        The Plugin lives in a plugin marketplace the organization owns.

        default: organization

    - `class BetaPluginOwnerUser`

      - `type: Literal["user"]`

        The Plugin lives in one member's personal plugin marketplace.

        default: user

      - `user_id: str`

        The member's User ID.

  - `reach: Optional[Literal["contained", "privileged", "remote"]]`

    How far the served version reaches, or `null` if it is not classified.

    `remote` means it declares an MCP server or a CLI, or something that counts as one. `privileged` means it is not `remote`, but declares a hook (of any type, even one that posts to a URL), monitor, language server, Claude Code workflow (any file in a `workflows/` folder at its root counts as one), or settings, or has a skill, command, or other Markdown file whose frontmatter pre-approves tools (`allowed-tools` with any value other than an empty one or one that names only `AskUserQuestion`, `TodoWrite`, and `ToolSearch`). Otherwise it is `contained`.

    If the frontmatter of a skill, command, or other Markdown file that could change the value could not be read, or was past a size limit, the version is `null` or `privileged` (or `remote`, if something else it declares makes it `remote`), not `contained`. The value is normally worked out when a version is stored, under the rules of that time, so an older version can be `null`, `contained` where the same files stored today would be `privileged`, `remote`, or `null`, or `privileged` where they would be `remote`.

    - `"contained"`

    - `"privileged"`

    - `"remote"`

  - `served_version_id: str`

    The version claude.ai serves to members.

  - `served_version_pinned: bool`

    True once the served version has been pinned, through Update Plugin or in claude.ai. While false, a new version normally becomes the served version when it is stored. While the newest version is not the served version, as when a version saved in claude.ai is waiting for its content scan, `served_version_id` differs from `latest_version_id`.

  - `updated_at: datetime`

    RFC 3339. Moves on a served-version change (including pinning an unpinned Plugin to the version it already serves) and, normally, on a new version. A version saved in claude.ai that waits for its content scan moves it when it becomes the served version, and not necessarily when it is stored. A change to the Plugin's installation settings or shares does not move it.

    format: date-time

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_plugin = client.beta.organization.plugins.retrieve(
    plugin_id="plugin_id",
)
print(beta_plugin.id)
```

#### Response (200)

```json
{
  "id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
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
  "latest_version_id": "pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
  "manifest_version": "1.2.0",
  "marketplace_id": "marketplace_01HxQ3v9KpZ2mTn8RwLc4Ys7",
  "name": "code-review-helper",
  "organization_installation_preference": "available",
  "organization_installation_preference_inherited": true,
  "owner": {
    "type": "organization"
  },
  "reach": "contained",
  "served_version_id": "pluginver_01K9wPcHd4Rm2Tx8Vq6Ln3Sb",
  "served_version_pinned": true,
  "type": "plugin",
  "updated_at": "2026-03-14T09:26:53.589793Z"
}
```

## Update Plugin

`beta.organization.plugins.update(plugin_id, **kwargs) -> BetaPlugin`

**POST** `/v1/organizations/plugins/{plugin_id}`

Change which stored version of an organization-owned Plugin is served to members,
for example to roll back to an earlier one. This pins the served version: later
uploads are stored but no longer change what is served, and pinning cannot currently
be undone, here or in claude.ai.

Pass the version as `served_version_id`: an earlier one to roll back, a later one to
start serving a version that was stored without being served, or the one already
served to pin it without changing what is served. No new version is created.

When the organization has content scanning enabled, a version whose
`content_scan.status` is `processing` is refused with a 409 (`error_code`
`scan_pending`; retry once the scan finishes). A version whose `content_scan.status`
is `errored`, or whose `content_scan.assessment` is `fail` or `unknown`, is refused
with a 400 (`error_code` `scan_failed`); a `warn` is accepted. If the scan outcome
cannot be read at that moment, the request fails with a retryable 503 instead.
When the Plugin is in the organization's
library marketplace, a version other than the one served is also refused with a 409
when an organization skill that this API does not list has since taken the name of
one of its skills: `error_code` `skill_name_taken`, with that name in
`details.skill_name`. A member-owned Plugin cannot be updated here (403).

This endpoint does not write installation settings; they are written at
`/v1/organizations/plugins/{plugin_id}/installation_settings/{target}`.

**Accepted credentials:** an Admin API key with the `write:plugins` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

### Parameters

- `plugin_id: str` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `served_version_id: str`

  Serve this version of the Plugin (prefixed `pluginver_`) and pin the served version to it; `latest` is not accepted.

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

### Returns

- `class BetaPlugin`

  - `type: Literal["plugin"]`

    Always `plugin`.

    default: plugin

  - `id: str`

    The Plugin's ID.

  - `components: Optional[List[BetaPluginComponent]]`

    What the served version contains; null when not enumerated.

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

    The served version's content scan; null when it has not been scanned.

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

    Who created the Plugin; null when no creator is recorded.

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

    The served version's description.

  - `display_name: Optional[str]`

    The served version's display name.

  - `latest_version_id: str`

    The newest version.

  - `manifest_version: Optional[str]`

    The served version's manifest `version`, normalized for display, or `null` (the Plugin Version's `manifest_version` says how and when).

  - `marketplace_id: str`

    The ID of the plugin marketplace the Plugin lives in.

  - `name: str`

    Lowercase identifier, unique within its plugin marketplace. Fixed for an organization-owned Plugin's lifetime; a member-owned Plugin's changes when its owner renames it in claude.ai, while its `id` stays the same.

  - `organization_installation_preference: Optional[Literal["auto_install", "available", "not_available", "required"]]`

    Organization-owned Plugin: the organization-wide installation setting every member gets unless an RBAC Group they belong to holds its own — the Plugin's own setting, or its plugin marketplace's default. Null for a member-owned Plugin, which has shares instead. One of `required`, `auto_install`, `available`, `not_available`; a value this API does not yet name is returned as stored.

    - `"auto_install"`

    - `"available"`

    - `"not_available"`

    - `"required"`

  - `organization_installation_preference_inherited: Optional[bool]`

    Organization-owned Plugin: true while it has no organization-wide setting of its own and `organization_installation_preference` is its plugin marketplace's default. Null for a member-owned Plugin.

  - `owner: Owner`

    Who owns the Plugin: the organization, or the member whose personal plugin marketplace it lives in.

    - `class BetaPluginOwnerOrganization`

      - `type: Literal["organization"]`

        The Plugin lives in a plugin marketplace the organization owns.

        default: organization

    - `class BetaPluginOwnerUser`

      - `type: Literal["user"]`

        The Plugin lives in one member's personal plugin marketplace.

        default: user

      - `user_id: str`

        The member's User ID.

  - `reach: Optional[Literal["contained", "privileged", "remote"]]`

    How far the served version reaches, or `null` if it is not classified.

    `remote` means it declares an MCP server or a CLI, or something that counts as one. `privileged` means it is not `remote`, but declares a hook (of any type, even one that posts to a URL), monitor, language server, Claude Code workflow (any file in a `workflows/` folder at its root counts as one), or settings, or has a skill, command, or other Markdown file whose frontmatter pre-approves tools (`allowed-tools` with any value other than an empty one or one that names only `AskUserQuestion`, `TodoWrite`, and `ToolSearch`). Otherwise it is `contained`.

    If the frontmatter of a skill, command, or other Markdown file that could change the value could not be read, or was past a size limit, the version is `null` or `privileged` (or `remote`, if something else it declares makes it `remote`), not `contained`. The value is normally worked out when a version is stored, under the rules of that time, so an older version can be `null`, `contained` where the same files stored today would be `privileged`, `remote`, or `null`, or `privileged` where they would be `remote`.

    - `"contained"`

    - `"privileged"`

    - `"remote"`

  - `served_version_id: str`

    The version claude.ai serves to members.

  - `served_version_pinned: bool`

    True once the served version has been pinned, through Update Plugin or in claude.ai. While false, a new version normally becomes the served version when it is stored. While the newest version is not the served version, as when a version saved in claude.ai is waiting for its content scan, `served_version_id` differs from `latest_version_id`.

  - `updated_at: datetime`

    RFC 3339. Moves on a served-version change (including pinning an unpinned Plugin to the version it already serves) and, normally, on a new version. A version saved in claude.ai that waits for its content scan moves it when it becomes the served version, and not necessarily when it is stored. A change to the Plugin's installation settings or shares does not move it.

    format: date-time

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_plugin = client.beta.organization.plugins.update(
    plugin_id="plugin_id",
    served_version_id="pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
)
print(beta_plugin.id)
```

#### Response (200)

```json
{
  "id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
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
  "latest_version_id": "pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
  "manifest_version": "1.2.0",
  "marketplace_id": "marketplace_01HxQ3v9KpZ2mTn8RwLc4Ys7",
  "name": "code-review-helper",
  "organization_installation_preference": "available",
  "organization_installation_preference_inherited": true,
  "owner": {
    "type": "organization"
  },
  "reach": "contained",
  "served_version_id": "pluginver_01K9wPcHd4Rm2Tx8Vq6Ln3Sb",
  "served_version_pinned": true,
  "type": "plugin",
  "updated_at": "2026-03-14T09:26:53.589793Z"
}
```

## List Plugins

`beta.organization.plugins.list(**kwargs) -> SyncPageCursor[BetaPlugin]`

**GET** `/v1/organizations/plugins`

List the Plugins created under the organization, newest first: those in the
organization's own plugin marketplaces and those in members' personal plugin
marketplaces.

Plugins in members' personal marketplaces are listed with the same detail as the
organization's own, and their files can be downloaded through the version archive
endpoint, which records each such download on the Compliance API activity feed.

**Accepted credentials:** an Admin API key with the `read:plugins` or `read:org_audit` scope, or a Compliance Access Key with the `read:compliance_org_data` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

### Parameters

- `created_at_gt: Optional[Union[str, datetime, null]]` (query parameter)

  RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt].

  format: date-time

- `created_at_gte: Optional[Union[str, datetime, null]]` (query parameter)

  RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt].

  format: date-time

- `created_at_lt: Optional[Union[str, datetime, null]]` (query parameter)

  RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt].

  format: date-time

- `created_at_lte: Optional[Union[str, datetime, null]]` (query parameter)

  RFC 3339 timestamp bound; combine [gte], [gt], [lte], [lt].

  format: date-time

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `100`.

  default: 20, minimum: 1, maximum: 100

- `marketplace_id: Optional[str]` (query parameter)

  Only Plugins in this plugin marketplace (prefixed `marketplace_`).

- `organization_id: Optional[str]` (query parameter)

  For a `read:org_audit` or `read:compliance_org_data` key created for all of a parent organization's linked organizations: a child organization of that parent to read instead of the organization the key was created in, given as the organization's UUID or its `org_`-prefixed ID. A value that is neither returns a 400; an organization that is not a child of the key's parent, or where the Plugins API is not available, returns a 404. Any other key may pass only its own organization's ID here; another organization returns a 404. A key with no organization of its own must always pass `organization_id`.

- `owner_type: Optional[Literal["organization", "user"]]` (query parameter)

  `organization` for Plugins in the organization's plugin marketplaces, `user` for Plugins in members' personal plugin marketplaces.

  - `"organization"`

  - `"user"`

- `owner_user_id: Optional[str]` (query parameter)

  Only Plugins in this member's personal plugin marketplaces (prefixed `user_`); a removed member's ID is accepted.

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

  maxLength: 2048

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

### Returns

- `class BetaPlugin`

  - `type: Literal["plugin"]`

    Always `plugin`.

    default: plugin

  - `id: str`

    The Plugin's ID.

  - `components: Optional[List[BetaPluginComponent]]`

    What the served version contains; null when not enumerated.

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

    The served version's content scan; null when it has not been scanned.

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

    Who created the Plugin; null when no creator is recorded.

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

    The served version's description.

  - `display_name: Optional[str]`

    The served version's display name.

  - `latest_version_id: str`

    The newest version.

  - `manifest_version: Optional[str]`

    The served version's manifest `version`, normalized for display, or `null` (the Plugin Version's `manifest_version` says how and when).

  - `marketplace_id: str`

    The ID of the plugin marketplace the Plugin lives in.

  - `name: str`

    Lowercase identifier, unique within its plugin marketplace. Fixed for an organization-owned Plugin's lifetime; a member-owned Plugin's changes when its owner renames it in claude.ai, while its `id` stays the same.

  - `organization_installation_preference: Optional[Literal["auto_install", "available", "not_available", "required"]]`

    Organization-owned Plugin: the organization-wide installation setting every member gets unless an RBAC Group they belong to holds its own — the Plugin's own setting, or its plugin marketplace's default. Null for a member-owned Plugin, which has shares instead. One of `required`, `auto_install`, `available`, `not_available`; a value this API does not yet name is returned as stored.

    - `"auto_install"`

    - `"available"`

    - `"not_available"`

    - `"required"`

  - `organization_installation_preference_inherited: Optional[bool]`

    Organization-owned Plugin: true while it has no organization-wide setting of its own and `organization_installation_preference` is its plugin marketplace's default. Null for a member-owned Plugin.

  - `owner: Owner`

    Who owns the Plugin: the organization, or the member whose personal plugin marketplace it lives in.

    - `class BetaPluginOwnerOrganization`

      - `type: Literal["organization"]`

        The Plugin lives in a plugin marketplace the organization owns.

        default: organization

    - `class BetaPluginOwnerUser`

      - `type: Literal["user"]`

        The Plugin lives in one member's personal plugin marketplace.

        default: user

      - `user_id: str`

        The member's User ID.

  - `reach: Optional[Literal["contained", "privileged", "remote"]]`

    How far the served version reaches, or `null` if it is not classified.

    `remote` means it declares an MCP server or a CLI, or something that counts as one. `privileged` means it is not `remote`, but declares a hook (of any type, even one that posts to a URL), monitor, language server, Claude Code workflow (any file in a `workflows/` folder at its root counts as one), or settings, or has a skill, command, or other Markdown file whose frontmatter pre-approves tools (`allowed-tools` with any value other than an empty one or one that names only `AskUserQuestion`, `TodoWrite`, and `ToolSearch`). Otherwise it is `contained`.

    If the frontmatter of a skill, command, or other Markdown file that could change the value could not be read, or was past a size limit, the version is `null` or `privileged` (or `remote`, if something else it declares makes it `remote`), not `contained`. The value is normally worked out when a version is stored, under the rules of that time, so an older version can be `null`, `contained` where the same files stored today would be `privileged`, `remote`, or `null`, or `privileged` where they would be `remote`.

    - `"contained"`

    - `"privileged"`

    - `"remote"`

  - `served_version_id: str`

    The version claude.ai serves to members.

  - `served_version_pinned: bool`

    True once the served version has been pinned, through Update Plugin or in claude.ai. While false, a new version normally becomes the served version when it is stored. While the newest version is not the served version, as when a version saved in claude.ai is waiting for its content scan, `served_version_id` differs from `latest_version_id`.

  - `updated_at: datetime`

    RFC 3339. Moves on a served-version change (including pinning an unpinned Plugin to the version it already serves) and, normally, on a new version. A version saved in claude.ai that waits for its content scan moves it when it becomes the served version, and not necessarily when it is stored. A change to the Plugin's installation settings or shares does not move it.

    format: date-time

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.plugins.list()
page = page.data[0]
print(page.id)
```

#### Response (200)

```json
{
  "data": [
    {
      "id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
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
      "latest_version_id": "pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
      "manifest_version": "1.2.0",
      "marketplace_id": "marketplace_01HxQ3v9KpZ2mTn8RwLc4Ys7",
      "name": "code-review-helper",
      "organization_installation_preference": "available",
      "organization_installation_preference_inherited": true,
      "owner": {
        "type": "organization"
      },
      "reach": "contained",
      "served_version_id": "pluginver_01K9wPcHd4Rm2Tx8Vq6Ln3Sb",
      "served_version_pinned": true,
      "type": "plugin",
      "updated_at": "2026-03-14T09:26:53.589793Z"
    }
  ],
  "next_page": "page_MjAyNi0wOS0xNlQxNDowNTowOVo"
}
```

## Delete Plugin

`beta.organization.plugins.delete(plugin_id, **kwargs) -> BetaDeletedPlugin`

**DELETE** `/v1/organizations/plugins/{plugin_id}`

Permanently delete a Plugin and every version it holds, exactly as when an
administrator deletes it in claude.ai. The Plugin may belong to the organization or
to a member, including a member who has since left the organization. Do not delete a
Plugin only because your pipeline did not create it: a member or an administrator
might have added it in claude.ai.

An organization-owned Plugin's installation settings go with it; a member-owned
Plugin's shares are withdrawn and its owner no longer has it.

To take an organization-owned Plugin out of use reversibly, set its
organization-wide installation setting to `not_available` instead (and
remove or change any group settings, which override it for their members). Only a
Plugin in a `manual` marketplace can be deleted here; one synchronized from a
repository is removed by removing it from the repository (400).

**Accepted credentials:** an Admin API key with the `write:plugins` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

### Parameters

- `plugin_id: str` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

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

### Returns

- `class BetaDeletedPlugin`

  - `type: Literal["plugin_deleted"]`

    Always `plugin_deleted`.

    default: plugin_deleted

  - `id: str`

    The deleted Plugin's ID.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_deleted_plugin = client.beta.organization.plugins.delete(
    plugin_id="plugin_id",
)
print(beta_deleted_plugin.id)
```

#### Response (200)

```json
{
  "id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
  "type": "plugin_deleted"
}
```

## Domain types

### Beta Deleted Plugin

- `class BetaDeletedPlugin`

  - `type: Literal["plugin_deleted"]`

    Always `plugin_deleted`.

    default: plugin_deleted

  - `id: str`

    The deleted Plugin's ID.

### Beta Plugin

- `class BetaPlugin`

  - `type: Literal["plugin"]`

    Always `plugin`.

    default: plugin

  - `id: str`

    The Plugin's ID.

  - `components: Optional[List[BetaPluginComponent]]`

    What the served version contains; null when not enumerated.

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

    The served version's content scan; null when it has not been scanned.

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

    Who created the Plugin; null when no creator is recorded.

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

    The served version's description.

  - `display_name: Optional[str]`

    The served version's display name.

  - `latest_version_id: str`

    The newest version.

  - `manifest_version: Optional[str]`

    The served version's manifest `version`, normalized for display, or `null` (the Plugin Version's `manifest_version` says how and when).

  - `marketplace_id: str`

    The ID of the plugin marketplace the Plugin lives in.

  - `name: str`

    Lowercase identifier, unique within its plugin marketplace. Fixed for an organization-owned Plugin's lifetime; a member-owned Plugin's changes when its owner renames it in claude.ai, while its `id` stays the same.

  - `organization_installation_preference: Optional[Literal["auto_install", "available", "not_available", "required"]]`

    Organization-owned Plugin: the organization-wide installation setting every member gets unless an RBAC Group they belong to holds its own — the Plugin's own setting, or its plugin marketplace's default. Null for a member-owned Plugin, which has shares instead. One of `required`, `auto_install`, `available`, `not_available`; a value this API does not yet name is returned as stored.

    - `"auto_install"`

    - `"available"`

    - `"not_available"`

    - `"required"`

  - `organization_installation_preference_inherited: Optional[bool]`

    Organization-owned Plugin: true while it has no organization-wide setting of its own and `organization_installation_preference` is its plugin marketplace's default. Null for a member-owned Plugin.

  - `owner: Owner`

    Who owns the Plugin: the organization, or the member whose personal plugin marketplace it lives in.

    - `class BetaPluginOwnerOrganization`

      - `type: Literal["organization"]`

        The Plugin lives in a plugin marketplace the organization owns.

        default: organization

    - `class BetaPluginOwnerUser`

      - `type: Literal["user"]`

        The Plugin lives in one member's personal plugin marketplace.

        default: user

      - `user_id: str`

        The member's User ID.

  - `reach: Optional[Literal["contained", "privileged", "remote"]]`

    How far the served version reaches, or `null` if it is not classified.

    `remote` means it declares an MCP server or a CLI, or something that counts as one. `privileged` means it is not `remote`, but declares a hook (of any type, even one that posts to a URL), monitor, language server, Claude Code workflow (any file in a `workflows/` folder at its root counts as one), or settings, or has a skill, command, or other Markdown file whose frontmatter pre-approves tools (`allowed-tools` with any value other than an empty one or one that names only `AskUserQuestion`, `TodoWrite`, and `ToolSearch`). Otherwise it is `contained`.

    If the frontmatter of a skill, command, or other Markdown file that could change the value could not be read, or was past a size limit, the version is `null` or `privileged` (or `remote`, if something else it declares makes it `remote`), not `contained`. The value is normally worked out when a version is stored, under the rules of that time, so an older version can be `null`, `contained` where the same files stored today would be `privileged`, `remote`, or `null`, or `privileged` where they would be `remote`.

    - `"contained"`

    - `"privileged"`

    - `"remote"`

  - `served_version_id: str`

    The version claude.ai serves to members.

  - `served_version_pinned: bool`

    True once the served version has been pinned, through Update Plugin or in claude.ai. While false, a new version normally becomes the served version when it is stored. While the newest version is not the served version, as when a version saved in claude.ai is waiting for its content scan, `served_version_id` differs from `latest_version_id`.

  - `updated_at: datetime`

    RFC 3339. Moves on a served-version change (including pinning an unpinned Plugin to the version it already serves) and, normally, on a new version. A version saved in claude.ai that waits for its content scan moves it when it becomes the served version, and not necessarily when it is stored. A change to the Plugin's installation settings or shares does not move it.

    format: date-time

### Beta Plugin API Actor

- `class BetaPluginAPIActor`

  - `type: Literal["api_actor"]`

    An Admin API key, in the same form the Compliance API activity feed uses for it.

    default: api_actor

  - `api_key_id: str`

    The key's ID.

### Beta Plugin Component

- `class BetaPluginComponent`

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

### Beta Plugin Content Scan

- `class BetaPluginContentScan`

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

### Beta Plugin Name Taken Error Details

- `class BetaPluginNameTakenErrorDetails`

  The marketplace already holds this name. `plugin_id` is the Plugin that holds it, and can be absent.

  - `error_code: Literal["plugin_name_taken"]`

  - `plugin_id: Optional[str]`

### Beta Plugin Owner Organization

- `class BetaPluginOwnerOrganization`

  - `type: Literal["organization"]`

    The Plugin lives in a plugin marketplace the organization owns.

    default: organization

### Beta Plugin Owner User

- `class BetaPluginOwnerUser`

  - `type: Literal["user"]`

    The Plugin lives in one member's personal plugin marketplace.

    default: user

  - `user_id: str`

    The member's User ID.

### Beta Plugin Target Organization

- `class BetaPluginTargetOrganization`

  - `type: Literal["organization"]`

    Every member of the organization.

    default: organization

### Beta Plugin Target Organization Member

- `class BetaPluginTargetOrganizationMember`

  - `type: Literal["organization_member"]`

    One member of the organization.

    default: organization_member

  - `user_id: str`

    The member's User ID.

### Beta Plugin Target RBAC Group

- `class BetaPluginTargetRBACGroup`

  - `type: Literal["rbac_group"]`

    An RBAC Group.

    default: rbac_group

  - `rbac_group_id: str`

    The RBAC Group's ID.

### Beta Plugin User Actor

- `class BetaPluginUserActor`

  - `type: Literal["user_actor"]`

    A member of the organization.

    default: user_actor

  - `email_address: Optional[str]`

    The member's email address; may be null, for example when they are no longer a member of the organization.

  - `user_id: str`

    The member's User ID.

### Beta Registration Pending Error Details

- `class BetaRegistrationPendingErrorDetails`

  The Plugin version was stored but is not yet usable in claude.ai. `plugin_id` and `plugin_version_id` identify what was stored.

  - `error_code: Literal["registration_pending"]`

  - `plugin_id: str`

  - `plugin_version_id: str`

### Beta Scan Failed Error Details

- `class BetaScanFailedErrorDetails`

  The version in `plugin_version_id` did not pass its content scan, so it cannot be served.

  - `error_code: Literal["scan_failed"]`

  - `plugin_version_id: str`

### Beta Scan Pending Error Details

- `class BetaScanPendingErrorDetails`

  The content scan of the version in `plugin_version_id` is still running. Retry once the scan finishes.

  - `error_code: Literal["scan_pending"]`

  - `plugin_version_id: str`

### Beta Skill Name Taken Error Details

- `class BetaSkillNameTakenErrorDetails`

  One of the Plugin's skills has the name of an organization skill. `skill_name` is that name.

  - `error_code: Literal["skill_name_taken"]`

  - `skill_name: str`

## Plugins › Versions

### Create Plugin Version

`beta.organization.plugins.versions.create(plugin_id, **kwargs) -> BetaPluginVersion`

**POST** `/v1/organizations/plugins/{plugin_id}/versions`

Add a version to an organization-owned Plugin by uploading the new version's
files; it becomes the version served to members unless the Plugin's served version
has been pinned.

The upload is the same `multipart/form-data` as creating a Plugin: the version's
files (`files`, each part sent as `files[]`) and optional `release_notes`. The uploaded manifest's `name`
must equal the Plugin's `name`. Returns the stored version; read the Plugin back to
see which version it serves.

Only a Plugin in a `manual` marketplace takes uploads; a Plugin synchronized from
a repository gets its versions from the repository. When the Plugin is in the
organization's library marketplace, a version that adds a skill with the name of an
organization skill that this API does not list is refused with a 409: `error_code`
`skill_name_taken`, with that name in `details.skill_name`. A 503 with `error_code`
`registration_pending` means the version was stored but is not yet usable; a later
version create on the Plugin completes it.

For a worked example, see [Create a version](https://platform.claude.com/docs/en/manage-claude/plugins-api?sdk_languages=python#create-a-version)
in the Plugins API guide.

**Accepted credentials:** an Admin API key with the `write:plugins` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

#### Parameters

- `plugin_id: str` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `files: Sequence[FileTypes]`

  The version's files: one part per file, the part's filename being the file's path within the Plugin (for example `skills/review-pr/SKILL.md`), or a single `.zip` or `.plugin` archive holding them all. On the wire each part is named `files[]`, and a part named plain `files` is not read; with cURL, `-F 'files[]=@SKILL.md;filename=skills/review-pr/SKILL.md'`. The files must include the manifest, `.claude-plugin/plugin.json`.

- `release_notes: Optional[str]`

  Release notes stored with the version and shown in its version history in claude.ai; up to 5,000 characters.

  maxLength: 5000

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

#### Returns

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

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_plugin_version = client.beta.organization.plugins.versions.create(
    plugin_id="plugin_id",
    files=[b"Example data"],
)
print(beta_plugin_version.id)
```

##### Response (200)

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

### List Plugin Versions

`beta.organization.plugins.versions.list(plugin_id, **kwargs) -> SyncPageCursor[BetaPluginVersion]`

**GET** `/v1/organizations/plugins/{plugin_id}/versions`

List a Plugin's versions, newest first.

The first item of the first page is the version the Plugin's `latest_version_id`
refers to.

**Accepted credentials:** an Admin API key with the `read:plugins` or `read:org_audit` scope, or a Compliance Access Key with the `read:compliance_org_data` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

#### Parameters

- `plugin_id: str` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `organization_id: Optional[str]` (query parameter)

  For a `read:org_audit` or `read:compliance_org_data` key created for all of a parent organization's linked organizations: a child organization of that parent to read instead of the organization the key was created in, given as the organization's UUID or its `org_`-prefixed ID. A value that is neither returns a 400; an organization that is not a child of the key's parent, or where the Plugins API is not available, returns a 404. Any other key may pass only its own organization's ID here; another organization returns a 404. A key with no organization of its own must always pass `organization_id`.

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

  maxLength: 2048

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

#### Returns

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

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.plugins.versions.list(
    plugin_id="plugin_id",
)
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
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
  ],
  "next_page": "page_MjAyNi0wOS0xNlQxNDowNTowOVo"
}
```

### Get Plugin Version

`beta.organization.plugins.versions.retrieve(version, **kwargs) -> BetaPluginVersion`

**GET** `/v1/organizations/plugins/{plugin_id}/versions/{version}`

Retrieve one version of a Plugin by its ID, or the Plugin's newest version.

**Accepted credentials:** an Admin API key with the `read:plugins` or `read:org_audit` scope, or a Compliance Access Key with the `read:compliance_org_data` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

#### Parameters

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

#### Returns

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

#### Example

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

##### Response (200)

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

### Download Plugin Version Archive

`beta.organization.plugins.versions.download(version, **kwargs) -> BinaryResponseContent`

**GET** `/v1/organizations/plugins/{plugin_id}/versions/{version}/content`

Download one version's `.zip` archive, exactly as stored. Each download of a
Plugin from a member's personal plugin marketplace is recorded on the Compliance API
activity feed.

The response body is the archive (`Content-Type: application/zip`), sent as an
attachment whose filename is derived from the Plugin's name; name saved files from
the IDs in the request path, since that filename is not unique.

**Accepted credentials:** an Admin API key with the `read:plugins` or `read:org_audit` scope, or a Compliance Access Key with the `read:compliance_org_data` scope.

Every read scope above (`read:plugins`, `read:org_audit`, and
`read:compliance_org_data`) can download the files of plugins in members' personal
marketplaces, including files that claude.ai's admin settings do not show, and a
`read:org_audit` or `read:compliance_org_data` key created for all of your parent
organization's linked organizations can do this in any organization under it that has
access to this API, by passing `organization_id`. Each such download records a
`claude_plugin_archive_accessed` event on the Compliance API activity feed,
identifying the key, the plugin, the version, and the member. Downloads of
organization-owned plugins are not recorded.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

#### Parameters

- `plugin_id: str` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `version: str` (path parameter)

  ID of the Plugin Version (prefixed `pluginver_`). `latest` is not accepted here.

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

#### Returns

- `BinaryResponseContent`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
response = client.beta.organization.plugins.versions.download(
    version="version",
    plugin_id="plugin_id",
)
print(response)
content = response.read()
print(content)
```

## Plugins › Installation Settings

### List Plugin Installation Settings

`beta.organization.plugins.installation_settings.list(plugin_id, **kwargs) -> SyncPageCursor[BetaPluginInstallationSetting]`

**GET** `/v1/organizations/plugins/{plugin_id}/installation_settings`

List an organization-owned Plugin's installation settings, which say which
members it is for, most recently created first.

The list holds the Plugin's own organization-wide setting (absent while the Plugin
inherits its marketplace's default) and each RBAC Group's own setting. A
member-owned Plugin has shares instead, so this path returns 404 for one.

**Accepted credentials:** an Admin API key with the `read:plugins` or `read:org_audit` scope, or a Compliance Access Key with the `read:compliance_org_data` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

#### Parameters

- `plugin_id: str` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `100`.

  default: 20, minimum: 1, maximum: 100

- `organization_id: Optional[str]` (query parameter)

  For a `read:org_audit` or `read:compliance_org_data` key created for all of a parent organization's linked organizations: a child organization of that parent to read instead of the organization the key was created in, given as the organization's UUID or its `org_`-prefixed ID. A value that is neither returns a 400; an organization that is not a child of the key's parent, or where the Plugins API is not available, returns a 404. Any other key may pass only its own organization's ID here; another organization returns a 404. A key with no organization of its own must always pass `organization_id`.

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

  maxLength: 2048

- `target_type: Optional[Literal["organization", "rbac_group"]]` (query parameter)

  Only settings for this kind of target: `organization` (the organization-wide setting) or `rbac_group` (an RBAC Group's).

  - `"organization"`

  - `"rbac_group"`

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

#### Returns

- `class BetaPluginInstallationSetting`

  The installation setting an organization-owned Plugin holds for one
  target. It has no ID of its own: it is addressed by the Plugin's ID and the
  target.

  - `type: Literal["plugin_installation_setting"]`

    Always `plugin_installation_setting`.

    default: plugin_installation_setting

  - `created_at: datetime`

    When the target was first given a setting for this Plugin.

    format: date-time

  - `installation_preference: Literal["auto_install", "available", "not_available", "required"]`

    The setting the target holds for this Plugin. One of `required`, `auto_install`, `available`, `not_available`; a value this API does not yet name is returned as stored.

    - `"auto_install"`

    - `"available"`

    - `"not_available"`

    - `"required"`

  - `plugin_id: str`

    The Plugin's ID.

  - `target: Target`

    Whose setting this is: `organization` (the Plugin's own organization-wide setting) or `rbac_group` (one RBAC Group's own setting); `organization_member` does not occur here.

    - `class BetaPluginTargetOrganization`

      - `type: Literal["organization"]`

        Every member of the organization.

        default: organization

    - `class BetaPluginTargetRBACGroup`

      - `type: Literal["rbac_group"]`

        An RBAC Group.

        default: rbac_group

      - `rbac_group_id: str`

        The RBAC Group's ID.

    - `class BetaPluginTargetOrganizationMember`

      - `type: Literal["organization_member"]`

        One member of the organization.

        default: organization_member

      - `user_id: str`

        The member's User ID.

  - `updated_at: datetime`

    When its setting last changed.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.plugins.installation_settings.list(
    plugin_id="plugin_id",
)
page = page.data[0]
print(page.plugin_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "created_at": "2026-03-14T09:26:53.589793Z",
      "installation_preference": "required",
      "plugin_id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
      "target": {
        "type": "organization"
      },
      "type": "plugin_installation_setting",
      "updated_at": "2026-03-14T09:26:53.589793Z"
    }
  ],
  "next_page": "page_MjAyNi0wOS0xNlQxNDowNTowOVo"
}
```

### Set Plugin Installation Setting

`beta.organization.plugins.installation_settings.set(target, **kwargs) -> BetaPluginInstallationSetting`

**POST** `/v1/organizations/plugins/{plugin_id}/installation_settings/{target}`

Set or change an organization-owned Plugin's installation setting for the whole
organization or for one RBAC Group.

Writing the value a target already holds of its own changes nothing.

A member-owned Plugin has shares instead of installation settings, so this path
returns 404 for one.

Send a Plugin's installation-setting writes one at a time. If several writes for the
same Plugin arrive at the same time, the server handles them one after another and
can answer some of them with `503` instead of applying them. That `503` carries
`x-should-retry: true`, and the write is safe to repeat: wait a second or two, then
send it again.

**Accepted credentials:** an Admin API key with the `write:plugins` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

#### Parameters

- `plugin_id: str` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `target: str` (path parameter)

  The target whose setting is written: the literal `organization` for the Plugin's organization-wide setting, or an RBAC Group's ID (prefixed `rbac_group_`) for that group's own setting. Writing the `organization` target stops the Plugin from inheriting its marketplace's default, even when the value written equals that default.

- `installation_preference: Literal["auto_install", "available", "not_available", "required"]`

  The installation setting the target is to hold for this Plugin: one of `required`, `auto_install`, `available`, `not_available`.

  - `"auto_install"`

  - `"available"`

  - `"not_available"`

  - `"required"`

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

#### Returns

- `class BetaPluginInstallationSetting`

  The installation setting an organization-owned Plugin holds for one
  target. It has no ID of its own: it is addressed by the Plugin's ID and the
  target.

  - `type: Literal["plugin_installation_setting"]`

    Always `plugin_installation_setting`.

    default: plugin_installation_setting

  - `created_at: datetime`

    When the target was first given a setting for this Plugin.

    format: date-time

  - `installation_preference: Literal["auto_install", "available", "not_available", "required"]`

    The setting the target holds for this Plugin. One of `required`, `auto_install`, `available`, `not_available`; a value this API does not yet name is returned as stored.

    - `"auto_install"`

    - `"available"`

    - `"not_available"`

    - `"required"`

  - `plugin_id: str`

    The Plugin's ID.

  - `target: Target`

    Whose setting this is: `organization` (the Plugin's own organization-wide setting) or `rbac_group` (one RBAC Group's own setting); `organization_member` does not occur here.

    - `class BetaPluginTargetOrganization`

      - `type: Literal["organization"]`

        Every member of the organization.

        default: organization

    - `class BetaPluginTargetRBACGroup`

      - `type: Literal["rbac_group"]`

        An RBAC Group.

        default: rbac_group

      - `rbac_group_id: str`

        The RBAC Group's ID.

    - `class BetaPluginTargetOrganizationMember`

      - `type: Literal["organization_member"]`

        One member of the organization.

        default: organization_member

      - `user_id: str`

        The member's User ID.

  - `updated_at: datetime`

    When its setting last changed.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_plugin_installation_setting = (
    client.beta.organization.plugins.installation_settings.set(
        target="target",
        plugin_id="plugin_id",
        installation_preference="required",
    )
)
print(beta_plugin_installation_setting.plugin_id)
```

##### Response (200)

```json
{
  "created_at": "2026-03-14T09:26:53.589793Z",
  "installation_preference": "required",
  "plugin_id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
  "target": {
    "type": "organization"
  },
  "type": "plugin_installation_setting",
  "updated_at": "2026-03-14T09:26:53.589793Z"
}
```

### Remove Plugin Installation Setting

`beta.organization.plugins.installation_settings.remove(target, **kwargs) -> BetaDeletedPluginInstallationSetting`

**DELETE** `/v1/organizations/plugins/{plugin_id}/installation_settings/{target}`

Remove an organization-owned Plugin's own installation setting for the whole
organization or for one RBAC Group.

Removing the `organization` target returns the Plugin to its marketplace's default
installation setting and leaves the groups' settings in place. Removing a group's
setting makes the group's members fall back to the Plugin's organization-wide setting
or to the settings of their other groups.

A target that holds no setting of its own returns 404 (a Plugin that already inherits
its marketplace's default holds no `organization` setting), and so does a member-owned
Plugin.

A removal counts as one of the Plugin's installation-setting writes: send all of those
writes one at a time. If several arrive for the same Plugin at the same time, the server
handles them one after another and can answer some of them with `503` and
`x-should-retry: true` instead of applying them; wait a second or two and send the
removal again. A `404` on the repeat means the setting is already gone.

**Accepted credentials:** an Admin API key with the `write:plugins` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

#### Parameters

- `plugin_id: str` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `target: str` (path parameter)

  The target whose own setting is removed: the literal `organization` for the Plugin's organization-wide setting, or an RBAC Group's ID (prefixed `rbac_group_`) for that group's own setting. Removing the `organization` setting returns the Plugin to its marketplace's default.

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

#### Returns

- `class BetaDeletedPluginInstallationSetting`

  Confirmation that one target's installation setting was removed, naming
  the Plugin and the target in place of an ID.

  - `type: Literal["plugin_installation_setting_deleted"]`

    Always `plugin_installation_setting_deleted`.

    default: plugin_installation_setting_deleted

  - `plugin_id: str`

    The Plugin's ID.

  - `target: Target`

    Whose setting was removed.

    - `class BetaPluginTargetOrganization`

      - `type: Literal["organization"]`

        Every member of the organization.

        default: organization

    - `class BetaPluginTargetRBACGroup`

      - `type: Literal["rbac_group"]`

        An RBAC Group.

        default: rbac_group

      - `rbac_group_id: str`

        The RBAC Group's ID.

    - `class BetaPluginTargetOrganizationMember`

      - `type: Literal["organization_member"]`

        One member of the organization.

        default: organization_member

      - `user_id: str`

        The member's User ID.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_deleted_plugin_installation_setting = (
    client.beta.organization.plugins.installation_settings.remove(
        target="target",
        plugin_id="plugin_id",
    )
)
print(beta_deleted_plugin_installation_setting.plugin_id)
```

##### Response (200)

```json
{
  "plugin_id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
  "target": {
    "rbac_group_id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
    "type": "rbac_group"
  },
  "type": "plugin_installation_setting_deleted"
}
```

## Plugins › Shares

### List Plugin Shares

`beta.organization.plugins.shares.list(plugin_id, **kwargs) -> SyncPageCursor[BetaPluginShare]`

**GET** `/v1/organizations/plugins/{plugin_id}/shares`

List the shares the owner of a member-owned Plugin has given — to every member of
the organization, to an RBAC Group, or to one member — most recently granted first.

Shares are read-only in this API: members give and withdraw them in claude.ai, and
who gave a share is recorded on the Compliance API activity feed rather than on the
share. An organization-owned Plugin has installation settings instead, so this path
returns 404 for one.

**Accepted credentials:** an Admin API key with the `read:plugins` or `read:org_audit` scope, or a Compliance Access Key with the `read:compliance_org_data` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

#### Parameters

- `plugin_id: str` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `100`.

  default: 20, minimum: 1, maximum: 100

- `organization_id: Optional[str]` (query parameter)

  For a `read:org_audit` or `read:compliance_org_data` key created for all of a parent organization's linked organizations: a child organization of that parent to read instead of the organization the key was created in, given as the organization's UUID or its `org_`-prefixed ID. A value that is neither returns a 400; an organization that is not a child of the key's parent, or where the Plugins API is not available, returns a 404. Any other key may pass only its own organization's ID here; another organization returns a 404. A key with no organization of its own must always pass `organization_id`.

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

  maxLength: 2048

- `target_type: Optional[Literal["organization", "organization_member", "rbac_group"]]` (query parameter)

  Only shares with this kind of target: `organization` (every member), `rbac_group` (one RBAC Group), or `organization_member` (one member).

  - `"organization"`

  - `"organization_member"`

  - `"rbac_group"`

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

#### Returns

- `class BetaPluginShare`

  One share the owner of a member-owned Plugin has given. Shares are
  read-only in this API and have no ID of their own; who gave a share is
  recorded on the Compliance API activity feed, not here.

  - `type: Literal["plugin_share"]`

    Always `plugin_share`.

    default: plugin_share

  - `granted_at: datetime`

    When the share was given; a share whose role is later changed in claude.ai is re-granted and carries the time of that change.

    format: date-time

  - `plugin_id: str`

    The Plugin's ID.

  - `target: Target`

    Who the Plugin is shared with: `organization` (every member), `rbac_group` (one RBAC Group), or `organization_member` (one member).

    - `class BetaPluginTargetOrganization`

      - `type: Literal["organization"]`

        Every member of the organization.

        default: organization

    - `class BetaPluginTargetRBACGroup`

      - `type: Literal["rbac_group"]`

        An RBAC Group.

        default: rbac_group

      - `rbac_group_id: str`

        The RBAC Group's ID.

    - `class BetaPluginTargetOrganizationMember`

      - `type: Literal["organization_member"]`

        One member of the organization.

        default: organization_member

      - `user_id: str`

        The member's User ID.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.plugins.shares.list(
    plugin_id="plugin_id",
)
page = page.data[0]
print(page.plugin_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "granted_at": "2026-03-14T09:26:53.589793Z",
      "plugin_id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
      "target": {
        "type": "organization"
      },
      "type": "plugin_share"
    }
  ],
  "next_page": "page_MjAyNi0wOS0xNlQxNDowNTowOVo"
}
```
