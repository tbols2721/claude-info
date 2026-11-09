---
title: Remove Federation Rule Workspace
url: https://platform.claude.com/docs/en/api/python/organization/federation/rules/workspaces/remove
---

# Remove Federation Rule Workspace

`organization.federation.rules.workspaces.remove(workspace_id, **kwargs) -> WorkspaceRemoveResponse`

**DELETE** `/v1/organizations/federation_rules/{federation_rule_id}/workspaces/{workspace_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Disable a federation rule for a workspace.

Idempotent; succeeds even if the enablement was already removed. OAuth
callers may only manage rules whose `oauth_scope` is
`workspace:developer` or `workspace:inference`; other scopes require a
Console session.

## Parameters

- `federation_rule_id: str` (path parameter)

  ID of the federation rule.

- `workspace_id: str` (path parameter)

  ID of the workspace to disable for.

## Returns

- `class WorkspaceRemoveResponse`

  - `type: Literal["federation_rule_workspace_deleted"]`

    default: federation_rule_workspace_deleted

  - `federation_rule_id: str`

    Tagged ID of the federation rule.

  - `workspace_id: str`

    Tagged ID of the workspace named in the delete request. Removal is idempotent.

## Example

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

### Response (200)

```json
{
  "federation_rule_id": "federation_rule_id",
  "type": "federation_rule_workspace_deleted",
  "workspace_id": "workspace_id"
}
```
