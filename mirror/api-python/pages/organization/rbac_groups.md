---
title: RBAC Groups
url: https://platform.claude.com/docs/en/api/python/organization/rbac_groups
---

# RBAC Groups

## Create RBAC Group

`organization.rbac_groups.create(**kwargs) -> RBACGroup`

**POST** `/v1/organizations/rbac_groups`

Create an RBAC Group in the Claude Enterprise tenant. Groups created via the API have source type `"direct"`.

The RBAC Groups API is available to Claude Enterprise organizations only.

### Parameters

- `name: str`

  Name of the RBAC Group. Not uniqueness-enforced.

  minLength: 1, maxLength: 255

### Returns

- `class RBACGroup`

  - `type: Literal["rbac_group"]`

    Object type.

    For RBAC Groups, this is always `"rbac_group"`.

    default: rbac_group

  - `id: str`

    ID of the RBAC Group.

  - `created_at: datetime`

    RFC 3339 timestamp of when the RBAC Group was created.

    format: date-time

  - `name: str`

    Name of the RBAC Group. Not uniqueness-enforced.

  - `role_ids: Optional[List[str]]`

    RBAC Role IDs attached to this RBAC Group. Role attachment is managed in the admin settings and is read-only on this API. `null` means role data was temporarily unavailable — retry to distinguish from an empty list.

  - `source_type: Literal["direct", "scim"]`

    How the RBAC Group was created: `"direct"` for groups created directly (for example, in the organization's admin settings), `"scim"` for groups provisioned by the identity provider.

    - `"direct"`

    - `"scim"`

  - `updated_at: datetime`

    RFC 3339 timestamp of when the RBAC Group was last updated.

    format: date-time

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
rbac_group = client.organization.rbac_groups.create(
    name="Engineering",
)
print(rbac_group.id)
```

#### Response (200)

```json
{
  "id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "name": "Engineering",
  "role_ids": [
    "rbac_role_016J8xVtKpDq3Wy9ZmN2hR4s"
  ],
  "source_type": "direct",
  "type": "rbac_group",
  "updated_at": "2024-10-30T23:58:27.427722Z"
}
```

## List RBAC Groups

`organization.rbac_groups.list(**kwargs) -> SyncPageCursor[RBACGroup]`

**GET** `/v1/organizations/rbac_groups`

List RBAC Groups in the Claude Enterprise tenant.

The RBAC Groups API is available to Claude Enterprise organizations only.

### Parameters

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

### Returns

- `class RBACGroup`

  - `type: Literal["rbac_group"]`

    Object type.

    For RBAC Groups, this is always `"rbac_group"`.

    default: rbac_group

  - `id: str`

    ID of the RBAC Group.

  - `created_at: datetime`

    RFC 3339 timestamp of when the RBAC Group was created.

    format: date-time

  - `name: str`

    Name of the RBAC Group. Not uniqueness-enforced.

  - `role_ids: Optional[List[str]]`

    RBAC Role IDs attached to this RBAC Group. Role attachment is managed in the admin settings and is read-only on this API. `null` means role data was temporarily unavailable — retry to distinguish from an empty list.

  - `source_type: Literal["direct", "scim"]`

    How the RBAC Group was created: `"direct"` for groups created directly (for example, in the organization's admin settings), `"scim"` for groups provisioned by the identity provider.

    - `"direct"`

    - `"scim"`

  - `updated_at: datetime`

    RFC 3339 timestamp of when the RBAC Group was last updated.

    format: date-time

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.rbac_groups.list()
page = page.data[0]
print(page.id)
```

#### Response (200)

```json
{
  "data": [
    {
      "id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
      "created_at": "2024-10-30T23:58:27.427722Z",
      "name": "Engineering",
      "role_ids": [
        "rbac_role_016J8xVtKpDq3Wy9ZmN2hR4s"
      ],
      "source_type": "direct",
      "type": "rbac_group",
      "updated_at": "2024-10-30T23:58:27.427722Z"
    }
  ],
  "has_more": false,
  "next_page": "eyJjdXJzb3IiOiAicmJhY19ncm91cF8wMSJ9"
}
```

## Get RBAC Group

`organization.rbac_groups.retrieve(rbac_group_id) -> RBACGroup`

**GET** `/v1/organizations/rbac_groups/{rbac_group_id}`

Retrieve an RBAC Group by ID.

The RBAC Groups API is available to Claude Enterprise organizations only.

### Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

### Returns

- `class RBACGroup`

  - `type: Literal["rbac_group"]`

    Object type.

    For RBAC Groups, this is always `"rbac_group"`.

    default: rbac_group

  - `id: str`

    ID of the RBAC Group.

  - `created_at: datetime`

    RFC 3339 timestamp of when the RBAC Group was created.

    format: date-time

  - `name: str`

    Name of the RBAC Group. Not uniqueness-enforced.

  - `role_ids: Optional[List[str]]`

    RBAC Role IDs attached to this RBAC Group. Role attachment is managed in the admin settings and is read-only on this API. `null` means role data was temporarily unavailable — retry to distinguish from an empty list.

  - `source_type: Literal["direct", "scim"]`

    How the RBAC Group was created: `"direct"` for groups created directly (for example, in the organization's admin settings), `"scim"` for groups provisioned by the identity provider.

    - `"direct"`

    - `"scim"`

  - `updated_at: datetime`

    RFC 3339 timestamp of when the RBAC Group was last updated.

    format: date-time

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
rbac_group = client.organization.rbac_groups.retrieve(
    "rbac_group_id",
)
print(rbac_group.id)
```

#### Response (200)

```json
{
  "id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "name": "Engineering",
  "role_ids": [
    "rbac_role_016J8xVtKpDq3Wy9ZmN2hR4s"
  ],
  "source_type": "direct",
  "type": "rbac_group",
  "updated_at": "2024-10-30T23:58:27.427722Z"
}
```

## Update RBAC Group

`organization.rbac_groups.update(rbac_group_id, **kwargs) -> RBACGroup`

**POST** `/v1/organizations/rbac_groups/{rbac_group_id}`

Update an RBAC Group's name. Groups provisioned by an identity provider (source type `"scim"`) cannot be modified via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

### Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

- `name: Optional[str]`

  Name of the RBAC Group. Not uniqueness-enforced.

  minLength: 1, maxLength: 255

### Returns

- `class RBACGroup`

  - `type: Literal["rbac_group"]`

    Object type.

    For RBAC Groups, this is always `"rbac_group"`.

    default: rbac_group

  - `id: str`

    ID of the RBAC Group.

  - `created_at: datetime`

    RFC 3339 timestamp of when the RBAC Group was created.

    format: date-time

  - `name: str`

    Name of the RBAC Group. Not uniqueness-enforced.

  - `role_ids: Optional[List[str]]`

    RBAC Role IDs attached to this RBAC Group. Role attachment is managed in the admin settings and is read-only on this API. `null` means role data was temporarily unavailable — retry to distinguish from an empty list.

  - `source_type: Literal["direct", "scim"]`

    How the RBAC Group was created: `"direct"` for groups created directly (for example, in the organization's admin settings), `"scim"` for groups provisioned by the identity provider.

    - `"direct"`

    - `"scim"`

  - `updated_at: datetime`

    RFC 3339 timestamp of when the RBAC Group was last updated.

    format: date-time

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
rbac_group = client.organization.rbac_groups.update(
    rbac_group_id="rbac_group_id",
)
print(rbac_group.id)
```

#### Response (200)

```json
{
  "id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "name": "Engineering",
  "role_ids": [
    "rbac_role_016J8xVtKpDq3Wy9ZmN2hR4s"
  ],
  "source_type": "direct",
  "type": "rbac_group",
  "updated_at": "2024-10-30T23:58:27.427722Z"
}
```

## Delete RBAC Group

`organization.rbac_groups.delete(rbac_group_id) -> DeletedRBACGroup`

**DELETE** `/v1/organizations/rbac_groups/{rbac_group_id}`

Delete an RBAC Group. Groups provisioned by an identity provider (source type `"scim"`) cannot be deleted via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

### Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

### Returns

- `class DeletedRBACGroup`

  - `type: Literal["rbac_group_deleted"]`

    Deleted object type.

    For RBAC Groups, this is always `"rbac_group_deleted"`.

    default: rbac_group_deleted

  - `id: str`

    ID of the RBAC Group.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
deleted_rbac_group = client.organization.rbac_groups.delete(
    "rbac_group_id",
)
print(deleted_rbac_group.id)
```

#### Response (200)

```json
{
  "id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "type": "rbac_group_deleted"
}
```

## Domain types

### Deleted RBAC Group

- `class DeletedRBACGroup`

  - `type: Literal["rbac_group_deleted"]`

    Deleted object type.

    For RBAC Groups, this is always `"rbac_group_deleted"`.

    default: rbac_group_deleted

  - `id: str`

    ID of the RBAC Group.

### RBAC Group

- `class RBACGroup`

  - `type: Literal["rbac_group"]`

    Object type.

    For RBAC Groups, this is always `"rbac_group"`.

    default: rbac_group

  - `id: str`

    ID of the RBAC Group.

  - `created_at: datetime`

    RFC 3339 timestamp of when the RBAC Group was created.

    format: date-time

  - `name: str`

    Name of the RBAC Group. Not uniqueness-enforced.

  - `role_ids: Optional[List[str]]`

    RBAC Role IDs attached to this RBAC Group. Role attachment is managed in the admin settings and is read-only on this API. `null` means role data was temporarily unavailable — retry to distinguish from an empty list.

  - `source_type: Literal["direct", "scim"]`

    How the RBAC Group was created: `"direct"` for groups created directly (for example, in the organization's admin settings), `"scim"` for groups provisioned by the identity provider.

    - `"direct"`

    - `"scim"`

  - `updated_at: datetime`

    RFC 3339 timestamp of when the RBAC Group was last updated.

    format: date-time

## RBAC Groups › Members

### List RBAC Group Members

`organization.rbac_groups.members.list(rbac_group_id, **kwargs) -> SyncPageCursor[RBACGroupMember]`

**GET** `/v1/organizations/rbac_groups/{rbac_group_id}/members`

List members of an RBAC Group.

The RBAC Groups API is available to Claude Enterprise organizations only.

#### Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

#### Returns

- `class RBACGroupMember`

  - `type: Literal["rbac_group_member"]`

    Object type.

    For RBAC Group Members, this is always `"rbac_group_member"`.

    default: rbac_group_member

  - `created_at: datetime`

    RFC 3339 timestamp of when the User was added to the RBAC Group.

    format: date-time

  - `email: str`

    Email of the User.

  - `rbac_group_id: str`

    ID of the RBAC Group.

  - `user_id: str`

    ID of the User.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.rbac_groups.members.list(
    rbac_group_id="rbac_group_id",
)
page = page.data[0]
print(page.rbac_group_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "created_at": "2024-10-30T23:58:27.427722Z",
      "email": "user@emaildomain.com",
      "rbac_group_id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
      "type": "rbac_group_member",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    }
  ],
  "has_more": false,
  "next_page": "eyJjdXJzb3IiOiAicmJhY19ncm91cF8wMSJ9"
}
```

### Add RBAC Group Member

`organization.rbac_groups.members.add(rbac_group_id, **kwargs) -> RBACGroupMember`

**POST** `/v1/organizations/rbac_groups/{rbac_group_id}/members`

Add a User to an RBAC Group. Membership of groups provisioned by an identity provider (source type `"scim"`) cannot be modified via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

#### Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

- `user_id: str`

  ID of the User.

#### Returns

- `class RBACGroupMember`

  - `type: Literal["rbac_group_member"]`

    Object type.

    For RBAC Group Members, this is always `"rbac_group_member"`.

    default: rbac_group_member

  - `created_at: datetime`

    RFC 3339 timestamp of when the User was added to the RBAC Group.

    format: date-time

  - `email: str`

    Email of the User.

  - `rbac_group_id: str`

    ID of the RBAC Group.

  - `user_id: str`

    ID of the User.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
rbac_group_member = client.organization.rbac_groups.members.add(
    rbac_group_id="rbac_group_id",
    user_id="user_01WxYzAbCdEfGhJkMnPqRsTu",
)
print(rbac_group_member.rbac_group_id)
```

##### Response (200)

```json
{
  "created_at": "2024-10-30T23:58:27.427722Z",
  "email": "user@emaildomain.com",
  "rbac_group_id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "type": "rbac_group_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
}
```

### Remove RBAC Group Member

`organization.rbac_groups.members.remove(user_id, **kwargs) -> DeletedRBACGroupMember`

**DELETE** `/v1/organizations/rbac_groups/{rbac_group_id}/members/{user_id}`

Remove a User from an RBAC Group. Membership of groups provisioned by an identity provider (source type `"scim"`) cannot be modified via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

#### Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

- `user_id: str` (path parameter)

  ID of the User.

#### Returns

- `class DeletedRBACGroupMember`

  - `type: Literal["rbac_group_member_deleted"]`

    Deleted object type. For RBAC Group Members, this is always `"rbac_group_member_deleted"`.

    default: rbac_group_member_deleted

  - `rbac_group_id: str`

    ID of the RBAC Group.

  - `user_id: str`

    ID of the User.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
deleted_rbac_group_member = client.organization.rbac_groups.members.remove(
    user_id="user_id",
    rbac_group_id="rbac_group_id",
)
print(deleted_rbac_group_member.rbac_group_id)
```

##### Response (200)

```json
{
  "rbac_group_id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "type": "rbac_group_member_deleted",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
}
```
