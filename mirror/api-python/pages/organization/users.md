---
title: Users
url: https://platform.claude.com/docs/en/api/python/organization/users
---

# Users

## List Users

`organization.users.list(**kwargs) -> SyncPage[OrganizationUser]`

**GET** `/v1/organizations/users`

List the organization's members.

### Parameters

- `after_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `email: Optional[str]` (query parameter)

  Filter by user email.

  format: email

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `roles: Optional[Sequence[str]]` (query parameter)

  Filter to items whose `role` equals one of the supplied values. Repeatable; values are OR'ed together.

  Accepted values depend on the organization type: Console and API organizations accept `user`, `developer`, `billing`, `admin`, and `claude_code_user`; Claude Enterprise organizations accept `user`, `owner`, `primary_owner`, `membership_admin`, and `managed`.

### Returns

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

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.users.list()
page = page.data[0]
print(page.id)
```

#### Response (200)

```json
{
  "data": [
    {
      "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
      "added_at": "2024-10-30T23:58:27.427722Z",
      "email": "user@emaildomain.com",
      "name": "Jane Doe",
      "role": "admin",
      "type": "user"
    }
  ],
  "first_id": "first_id",
  "has_more": true,
  "last_id": "last_id"
}
```

## Get User

`organization.users.retrieve(user_id) -> OrganizationUser`

**GET** `/v1/organizations/users/{user_id}`

Retrieve a member of the organization by user ID.

### Parameters

- `user_id: str` (path parameter)

  ID of the User.

### Returns

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

### Example

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

#### Response (200)

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

## Update User

`organization.users.update(user_id, **kwargs) -> OrganizationUser`

**POST** `/v1/organizations/users/{user_id}`

Update a member's organization role.

### Parameters

- `user_id: str` (path parameter)

  ID of the User.

- `role: Literal["billing", "claude_code_user", "developer", 2 more]`

  New role for the User.

  The accepted values depend on the organization type. Console and API organizations accept `user`, `developer`, `billing`, and `claude_code_user`; `admin` cannot be assigned through the API. Claude Enterprise organizations accept `user` and `managed`; changing a User's role to `managed` requires the `write:rbac_groups` scope in addition to `write:members`.

  - `"billing"`

  - `"claude_code_user"`

  - `"developer"`

  - `"managed"`

  - `"user"`

### Returns

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

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
organization_user = client.organization.users.update(
    user_id="user_id",
    role="user",
)
print(organization_user.id)
```

#### Response (200)

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

## Remove User

`organization.users.remove(user_id) -> UserRemoveResponse`

**DELETE** `/v1/organizations/users/{user_id}`

Remove a member from the organization.

### Parameters

- `user_id: str` (path parameter)

  ID of the User.

### Returns

- `class UserRemoveResponse`

  - `type: Literal["user_deleted"]`

    Deleted object type.

    For Users, this is always `"user_deleted"`.

    default: user_deleted

  - `id: str`

    ID of the User.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
user = client.organization.users.remove(
    "user_id",
)
print(user.id)
```

#### Response (200)

```json
{
  "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "type": "user_deleted"
}
```

## Domain types

### Organization User

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

### User Remove Response

- `class UserRemoveResponse`

  - `type: Literal["user_deleted"]`

    Deleted object type.

    For Users, this is always `"user_deleted"`.

    default: user_deleted

  - `id: str`

    ID of the User.
