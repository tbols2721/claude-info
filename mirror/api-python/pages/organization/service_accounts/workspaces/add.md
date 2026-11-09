---
title: Add Workspace To Service Account
url: https://platform.claude.com/docs/en/api/python/organization/service_accounts/workspaces/add
---

# Add Workspace To Service Account

`organization.service_accounts.workspaces.add(service_account_id, **kwargs) -> ServiceAccountWorkspaceMember`

**POST** `/v1/organizations/service_accounts/{service_account_id}/workspaces`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Add a service account to a workspace with the given `workspace_role`.

Mirror of `POST /workspaces/{workspace_id}/service_accounts`, addressed
from the service-account side; both create the same membership. If the
service account is already an explicit member of the workspace, its
`workspace_role` is replaced with the value supplied here. Archived
workspaces return 400. Archived service accounts cannot be added and are
rejected.

## Parameters

- `service_account_id: str` (path parameter)

  ID of the service account.

- `workspace_id: str`

  Tagged workspace ID to add the service account to.

- `workspace_role: NoBillingWorkspaceRole`

  Role to assign to the service account in this workspace.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

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
service_account_workspace_member = client.organization.service_accounts.workspaces.add(
    service_account_id="service_account_id",
    workspace_id="workspace_id",
    workspace_role="workspace_admin",
)
print(service_account_workspace_member.created_by_actor_id)
```

### Response (200)

```json
{
  "created_by_actor_id": "created_by_actor_id",
  "implicit": true,
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member",
  "workspace_id": "workspace_id",
  "workspace_role": "workspace_admin"
}
```
