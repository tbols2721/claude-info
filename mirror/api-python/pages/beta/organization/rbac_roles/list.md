---
title: List RBAC Roles
url: https://platform.claude.com/docs/en/api/python/beta/organization/rbac_roles/list
---

# List RBAC Roles

`beta.organization.rbac_roles.list(**kwargs) -> SyncPageCursor[BetaRBACRole]`

**GET** `/v1/organizations/rbac_roles`

List RBAC Roles in the organization.

The RBAC Roles API is available to Claude Enterprise organizations only.

## Parameters

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

## Returns

- `class BetaRBACRole`

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
page = client.beta.organization.rbac_roles.list()
page = page.data[0]
print(page.id)
```

### Response (200)

```json
{
  "data": [
    {
      "id": "rbac_role_016J8xVtKpDq3Wy9ZmN2hR4s",
      "created_at": "2024-10-30T23:58:27.427722Z",
      "display_name": "Project Editor",
      "type": "rbac_role",
      "updated_at": "2024-10-30T23:58:27.427722Z"
    }
  ],
  "has_more": true,
  "next_page": "eyJjdXJzb3IiOiAicmJhY19yb2xlXzAxIn0"
}
```
