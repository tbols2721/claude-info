---
title: List Federation Rule Workspaces
url: https://platform.claude.com/docs/en/api/python/organization/federation/rules/workspaces/list
---

# List Federation Rule Workspaces

`organization.federation.rules.workspaces.list(federation_rule_id, **kwargs) -> SyncPageCursor[FederationRuleWorkspace]`

**GET** `/v1/organizations/federation_rules/{federation_rule_id}/workspaces`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

List workspaces where this federation rule is enabled.

Returns all workspace enablements in a single response; the `limit` and
`page` parameters are accepted but have no effect, and `next_page` is
always `null`. Returns explicit per-workspace enablements only; for
rules with `applies_to_all_workspaces` or a legacy single
`workspace_id`, check those fields on the rule itself.

## Parameters

- `federation_rule_id: str` (path parameter)

  ID of the federation rule.

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

## Returns

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

## Example

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

### Response (200)

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
