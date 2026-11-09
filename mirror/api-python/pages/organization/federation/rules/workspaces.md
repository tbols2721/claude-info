---
title: Workspaces
url: https://platform.claude.com/docs/en/api/python/organization/federation/rules/workspaces
---

# Workspaces

## Add Federation Rule Workspace

`organization.federation.rules.workspaces.add(federation_rule_id, **kwargs) -> FederationRuleWorkspace`

**POST** `/v1/organizations/federation_rules/{federation_rule_id}/workspaces`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Enable a federation rule for a workspace.

Idempotent; re-enabling returns the existing enablement. The rule and
workspace must both belong to your organization. Membership of the
rule's target service account in this workspace is not checked at
enablement: token exchange into this workspace is rejected unless the
target is a member (it is implicitly a member of the default workspace).
Archived rules are rejected with 400. OAuth callers may only manage rules
whose `oauth_scope` is `workspace:developer` or `workspace:inference`;
other scopes require a Console session.

### Parameters

- `federation_rule_id: str` (path parameter)

  ID of the federation rule.

- `workspace_id: str`

  Tagged ID of the workspace to enable this rule for.

### Returns

- `class FederationRuleWorkspace`

  - `type: Literal["federation_rule_workspace"]`

    default: federation_rule_workspace

  - `created_at: datetime`

    When this workspace was enabled for the rule.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...` or `svac_...`) of the actor that enabled this workspace for the rule, if known.

  - `federation_rule_id: str`

    Tagged ID of the federation rule.

  - `workspace_id: str`

    Tagged ID of the workspace this rule is enabled for.

  - `workspace_name: Optional[str]`

    Workspace display name. Populated when listing; null in the enable response.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
federation_rule_workspace = client.organization.federation.rules.workspaces.add(
    federation_rule_id="federation_rule_id",
    workspace_id="workspace_id",
)
print(federation_rule_workspace.created_by_actor_id)
```

#### Response (200)

```json
{
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "federation_rule_id": "federation_rule_id",
  "type": "federation_rule_workspace",
  "workspace_id": "workspace_id",
  "workspace_name": "workspace_name"
}
```

## List Federation Rule Workspaces

`organization.federation.rules.workspaces.list(federation_rule_id, **kwargs) -> SyncPageCursor[FederationRuleWorkspace]`

**GET** `/v1/organizations/federation_rules/{federation_rule_id}/workspaces`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

List workspaces where this federation rule is enabled.

Returns all workspace enablements in a single response; the `limit` and
`page` parameters are accepted but have no effect, and `next_page` is
always `null`. Returns explicit per-workspace enablements only; for
rules with `applies_to_all_workspaces` or a legacy single
`workspace_id`, check those fields on the rule itself.

### Parameters

- `federation_rule_id: str` (path parameter)

  ID of the federation rule.

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

### Returns

- `class FederationRuleWorkspace`

  - `type: Literal["federation_rule_workspace"]`

    default: federation_rule_workspace

  - `created_at: datetime`

    When this workspace was enabled for the rule.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...` or `svac_...`) of the actor that enabled this workspace for the rule, if known.

  - `federation_rule_id: str`

    Tagged ID of the federation rule.

  - `workspace_id: str`

    Tagged ID of the workspace this rule is enabled for.

  - `workspace_name: Optional[str]`

    Workspace display name. Populated when listing; null in the enable response.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.federation.rules.workspaces.list(
    federation_rule_id="federation_rule_id",
)
page = page.data[0]
print(page.created_by_actor_id)
```

#### Response (200)

```json
{
  "data": [
    {
      "created_at": "2024-10-30T23:58:27.427722Z",
      "created_by_actor_id": "created_by_actor_id",
      "federation_rule_id": "federation_rule_id",
      "type": "federation_rule_workspace",
      "workspace_id": "workspace_id",
      "workspace_name": "workspace_name"
    }
  ],
  "next_page": "next_page"
}
```

## Remove Federation Rule Workspace

`organization.federation.rules.workspaces.remove(workspace_id, **kwargs) -> WorkspaceRemoveResponse`

**DELETE** `/v1/organizations/federation_rules/{federation_rule_id}/workspaces/{workspace_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Disable a federation rule for a workspace.

Idempotent; succeeds even if the enablement was already removed. OAuth
callers may only manage rules whose `oauth_scope` is
`workspace:developer` or `workspace:inference`; other scopes require a
Console session.

### Parameters

- `federation_rule_id: str` (path parameter)

  ID of the federation rule.

- `workspace_id: str` (path parameter)

  ID of the workspace to disable for.

### Returns

- `class WorkspaceRemoveResponse`

  - `type: Literal["federation_rule_workspace_deleted"]`

    default: federation_rule_workspace_deleted

  - `federation_rule_id: str`

    Tagged ID of the federation rule.

  - `workspace_id: str`

    Tagged ID of the workspace named in the delete request. Removal is idempotent.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace = client.organization.federation.rules.workspaces.remove(
    workspace_id="workspace_id",
    federation_rule_id="federation_rule_id",
)
print(workspace.federation_rule_id)
```

#### Response (200)

```json
{
  "federation_rule_id": "federation_rule_id",
  "type": "federation_rule_workspace_deleted",
  "workspace_id": "workspace_id"
}
```

## Domain types

### Workspace Remove Response

- `class WorkspaceRemoveResponse`

  - `type: Literal["federation_rule_workspace_deleted"]`

    default: federation_rule_workspace_deleted

  - `federation_rule_id: str`

    Tagged ID of the federation rule.

  - `workspace_id: str`

    Tagged ID of the workspace named in the delete request. Removal is idempotent.
