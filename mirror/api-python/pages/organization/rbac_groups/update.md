---
title: Update RBAC Group
url: https://platform.claude.com/docs/en/api/python/organization/rbac_groups/update
---

# Update RBAC Group

`organization.rbac_groups.update(rbac_group_id, **kwargs) -> RBACGroup`

**POST** `/v1/organizations/rbac_groups/{rbac_group_id}`

Update an RBAC Group's name. Groups provisioned by an identity provider (source type `"scim"`) cannot be modified via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

## Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

- `name: Optional[str]`

  Name of the RBAC Group. Not uniqueness-enforced.

  minLength: 1, maxLength: 255

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
rbac_group = client.organization.rbac_groups.update(
    rbac_group_id="rbac_group_id",
)
print(rbac_group.id)
```

### Response (200)

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
