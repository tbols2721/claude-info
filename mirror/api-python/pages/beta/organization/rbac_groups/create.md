---
title: Create RBAC Group
url: https://platform.claude.com/docs/en/api/python/beta/organization/rbac_groups/create
---

# Create RBAC Group

`beta.organization.rbac_groups.create(**kwargs) -> BetaRBACGroup`

**POST** `/v1/organizations/rbac_groups`

Create an RBAC Group in the Claude Enterprise tenant. Groups created via the API have source type `"direct"`.

The RBAC Groups API is available to Claude Enterprise organizations only.

## Parameters

- `name: str`

  Name of the RBAC Group. Not uniqueness-enforced.

  minLength: 1, maxLength: 255

## Returns

- `class BetaRBACGroup`

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
beta_rbac_group = client.beta.organization.rbac_groups.create(
    name="Engineering",
)
print(beta_rbac_group.id)
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
