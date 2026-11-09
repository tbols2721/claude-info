---
title: Get Workspace Member
url: https://platform.claude.com/docs/en/api/python/beta/organization/workspaces/members/retrieve
---

# Get Workspace Member

`beta.organization.workspaces.members.retrieve(user_id, **kwargs) -> BetaWorkspaceMember`

**GET** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Get Workspace Member

## Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `user_id: str` (path parameter)

  ID of the User.

## Returns

- `class BetaWorkspaceMember`

  - `type: Literal["workspace_member"]`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    default: workspace_member

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

  - `workspace_role: BetaWorkspaceRole`

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
beta_workspace_member = client.beta.organization.workspaces.members.retrieve(
    user_id="user_id",
    workspace_id="workspace_id",
)
print(beta_workspace_member.user_id)
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
