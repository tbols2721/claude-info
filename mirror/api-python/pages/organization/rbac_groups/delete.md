---
title: Delete RBAC Group
url: https://platform.claude.com/docs/en/api/python/organization/rbac_groups/delete
---

# Delete RBAC Group

`organization.rbac_groups.delete(rbac_group_id) -> DeletedRBACGroup`

**DELETE** `/v1/organizations/rbac_groups/{rbac_group_id}`

Delete an RBAC Group. Groups provisioned by an identity provider (source type `"scim"`) cannot be deleted via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

## Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

## Returns

- `class DeletedRBACGroup`

  - `type: Literal["rbac_group_deleted"]`

    Deleted object type.

    For RBAC Groups, this is always `"rbac_group_deleted"`.

    default: rbac_group_deleted

  - `id: str`

    ID of the RBAC Group.

## Example

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

### Response (200)

```json
{
  "id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "type": "rbac_group_deleted"
}
```
