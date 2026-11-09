---
title: Delete Service Account Workspace Member
url: https://platform.claude.com/docs/en/api/python/organization/workspaces/service_accounts/remove
---

# Delete Service Account Workspace Member

`organization.workspaces.service_accounts.remove(service_account_id, **kwargs) -> ServiceAccountRemoveResponse`

**DELETE** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Remove a service account from a workspace.

Removal is idempotent (returns 200 even if the membership was already
removed). A DELETE against the implicit default-workspace membership
returns 200 but is a no-op and the membership persists; deleting an
explicit default-workspace row reverts to the implicit `workspace_user`
membership. Archived workspaces return 400.

## Parameters

- `workspace_id: str` (path parameter)

  ID of the workspace.

- `service_account_id: str` (path parameter)

  ID of the service account.

## Returns

- `class ServiceAccountRemoveResponse`

  - `type: Literal["service_account_workspace_member_deleted"]`

    default: service_account_workspace_member_deleted

  - `service_account_id: str`

    Tagged service account ID (`svac_...`) named in the delete request. Removal is idempotent; see the endpoint description for the implicit-membership no-op.

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`) named in the delete request.

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account = client.organization.workspaces.service_accounts.remove(
    service_account_id="service_account_id",
    workspace_id="workspace_id",
)
print(service_account.service_account_id)
```

### Response (200)

```json
{
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member_deleted",
  "workspace_id": "workspace_id"
}
```
