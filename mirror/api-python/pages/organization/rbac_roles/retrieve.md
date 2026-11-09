---
title: Get RBAC Role
url: https://platform.claude.com/docs/en/api/python/organization/rbac_roles/retrieve
---

# Get RBAC Role

`organization.rbac_roles.retrieve(rbac_role_id) -> RBACRole`

**GET** `/v1/organizations/rbac_roles/{rbac_role_id}`

Retrieve an RBAC Role by ID.

The RBAC Roles API is available to Claude Enterprise organizations only.

## Parameters

- `rbac_role_id: str` (path parameter)

  ID of the RBAC Role.

## Returns

- `class RBACRole`

  - `type: Literal["rbac_role"]`

    Object type.

    For RBAC Roles, this is always `"rbac_role"`.

    default: rbac_role

  - `id: str`

    ID of the RBAC Role.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the RBAC Role was created.

    format: date-time

  - `display_name: str`

    Name of the RBAC Role. For a role created by Anthropic, this name can differ from the label claude.ai shows, and Anthropic may change the name. To keep a lasting reference to a role, store its `id`.

  - `updated_at: datetime`

    RFC 3339 datetime string indicating when the RBAC Role was last updated.

    format: date-time

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
rbac_role = client.organization.rbac_roles.retrieve(
    "rbac_role_id",
)
print(rbac_role.id)
```

### Response (200)

```json
{
  "id": "rbac_role_016J8xVtKpDq3Wy9ZmN2hR4s",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "display_name": "Project Editor",
  "type": "rbac_role",
  "updated_at": "2024-10-30T23:58:27.427722Z"
}
```
