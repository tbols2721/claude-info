---
title: List Service Account Workspace Members
url: https://platform.claude.com/docs/en/api/python/organization/workspaces/service_accounts/list
---

# List Service Account Workspace Members

`organization.workspaces.service_accounts.list(workspace_id, **kwargs) -> SyncPageCursor[ServiceAccountWorkspaceMember]`

**GET** `/v1/organizations/workspaces/{workspace_id}/service_accounts`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

List the service accounts that are members of a workspace.

Each entry includes the service account's `workspace_role`. Use `limit`
and the `next_page` cursor to paginate. Archived workspaces return 400;
use `GET /service_accounts/{id}/workspaces` to audit memberships of an
archived workspace. The implicit default-workspace membership is not
included in this list. Memberships of archived service accounts are
omitted from the results.

## Parameters

- `workspace_id: str` (path parameter)

  ID of the workspace.

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

## Returns

- `class ServiceAccountWorkspaceMember`

  - `type: Literal["service_account_workspace_member"]`

    default: service_account_workspace_member

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: Optional[bool]`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: str`

    Tagged service account ID (`svac_...`).

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: WorkspaceRole`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.workspaces.service_accounts.list(
    workspace_id="workspace_id",
)
page = page.data[0]
print(page.created_by_actor_id)
```

### Response (200)

```json
{
  "data": [
    {
      "created_by_actor_id": "created_by_actor_id",
      "implicit": true,
      "service_account_id": "service_account_id",
      "type": "service_account_workspace_member",
      "workspace_id": "workspace_id",
      "workspace_role": "workspace_admin"
    }
  ],
  "next_page": "next_page"
}
```
