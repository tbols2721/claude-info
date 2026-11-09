---
title: List RBAC Groups
url: https://platform.claude.com/docs/en/api/python/organization/rbac_groups/list
---

# List RBAC Groups

`organization.rbac_groups.list(**kwargs) -> SyncPageCursor[RBACGroup]`

**GET** `/v1/organizations/rbac_groups`

List RBAC Groups in the Claude Enterprise tenant.

The RBAC Groups API is available to Claude Enterprise organizations only.

## Parameters

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

## Returns

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

## Example

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

### Response (200)

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
