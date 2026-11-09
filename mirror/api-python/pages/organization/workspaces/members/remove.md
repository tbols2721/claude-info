---
title: Delete Workspace Member
url: https://platform.claude.com/docs/en/api/python/organization/workspaces/members/remove
---

# Delete Workspace Member

`organization.workspaces.members.remove(user_id, **kwargs) -> MemberRemoveResponse`

**DELETE** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Delete Workspace Member

## Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `user_id: str` (path parameter)

  ID of the User.

## Returns

- `class MemberRemoveResponse`

  - `type: Literal["workspace_member_deleted"]`

    Deleted object type.

    For Workspace Members, this is always `"workspace_member_deleted"`.

    default: workspace_member_deleted

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
member = client.organization.workspaces.members.remove(
    user_id="user_id",
    workspace_id="workspace_id",
)
print(member.user_id)
```

### Response (200)

```json
{
  "type": "workspace_member_deleted",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
}
```
