---
title: Create Workspace Member
url: https://platform.claude.com/docs/en/api/python/organization/workspaces/members/add
---

# Create Workspace Member

`organization.workspaces.members.add(workspace_id, **kwargs) -> WorkspaceMember`

**POST** `/v1/organizations/workspaces/{workspace_id}/members`

Create Workspace Member

## Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `user_id: str`

  ID of the User.

- `workspace_role: NoBillingWorkspaceRole`

  Role of the new Workspace Member. Cannot be `workspace_billing`.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

## Returns

- `class WorkspaceMember`

  - `type: Literal["workspace_member"]`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    default: workspace_member

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

  - `workspace_role: WorkspaceRole`

    Role of the Workspace Member.

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
workspace_member = client.organization.workspaces.members.add(
    workspace_id="workspace_id",
    user_id="user_01WxYzAbCdEfGhJkMnPqRsTu",
    workspace_role="workspace_admin",
)
print(workspace_member.user_id)
```

### Response (200)

```json
{
  "type": "workspace_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "workspace_role": "workspace_admin"
}
```
