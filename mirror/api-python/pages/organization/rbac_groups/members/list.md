---
title: List RBAC Group Members
url: https://platform.claude.com/docs/en/api/python/organization/rbac_groups/members/list
---

# List RBAC Group Members

`organization.rbac_groups.members.list(rbac_group_id, **kwargs) -> SyncPageCursor[RBACGroupMember]`

**GET** `/v1/organizations/rbac_groups/{rbac_group_id}/members`

List members of an RBAC Group.

The RBAC Groups API is available to Claude Enterprise organizations only.

## Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

## Returns

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

## Example

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

### Response (200)

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
