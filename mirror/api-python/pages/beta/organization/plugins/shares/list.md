---
title: List Plugin Shares
url: https://platform.claude.com/docs/en/api/python/beta/organization/plugins/shares/list
---

# List Plugin Shares

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

## Parameters

- `plugin_id: str` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `100`.

  default: 20, minimum: 1, maximum: 100

- `organization_id: Optional[str]` (query parameter)

  For a `read:org_audit` or `read:compliance_org_data` key created for all of a parent organization's linked organizations: a child organization of that parent to read instead of the organization the key was created in, given as the organization's UUID or its `org_`-prefixed ID. A value that is neither returns a 400; an organization that is not a child of the key's parent, or where the Plugins API is not available, returns a 404. Any other key may pass only its own organization's ID here; another organization returns a 404.

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

## Returns

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

## Example

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

### Response (200)

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
