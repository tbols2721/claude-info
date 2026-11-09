---
title: Remove User
url: https://platform.claude.com/docs/en/api/python/beta/organization/users/remove
---

# Remove User

`beta.organization.users.remove(user_id) -> UserRemoveResponse`

**DELETE** `/v1/organizations/users/{user_id}`

Remove a member from the organization.

## Parameters

- `user_id: str` (path parameter)

  ID of the User.

## Returns

- `class UserRemoveResponse`

  - `type: Literal["user_deleted"]`

    Deleted object type.

    For Users, this is always `"user_deleted"`.

    default: user_deleted

  - `id: str`

    ID of the User.

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
user = client.beta.organization.users.remove(
    "user_id",
)
print(user.id)
```

### Response (200)

```json
{
  "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "type": "user_deleted"
}
```
