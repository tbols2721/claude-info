---
title: Get User
url: https://platform.claude.com/docs/en/api/python/organization/users/retrieve
---

# Get User

`organization.users.retrieve(user_id) -> OrganizationUser`

**GET** `/v1/organizations/users/{user_id}`

Retrieve a member of the organization by user ID.

## Parameters

- `user_id: str` (path parameter)

  ID of the User.

## Returns

- `class OrganizationUser`

  - `type: Literal["user"]`

    Object type.

    For Users, this is always `"user"`.

    default: user

  - `id: str`

    ID of the User.

  - `added_at: datetime`

    RFC 3339 datetime string indicating when the User joined the Organization.

    format: date-time

  - `email: str`

    Email of the User.

  - `name: str`

    Name of the User.

  - `role: OrganizationRole`

    Organization role of the User.

    - `"admin"`

    - `"billing"`

    - `"claude_code_user"`

    - `"developer"`

    - `"managed"`

    - `"membership_admin"`

    - `"owner"`

    - `"primary_owner"`

    - `"user"`

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
organization_user = client.organization.users.retrieve(
    "user_id",
)
print(organization_user.id)
```

### Response (200)

```json
{
  "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "added_at": "2024-10-30T23:58:27.427722Z",
  "email": "user@emaildomain.com",
  "name": "Jane Doe",
  "role": "admin",
  "type": "user"
}
```
