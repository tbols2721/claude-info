---
title: Remove User
url: https://platform.claude.com/docs/en/api/cli/beta/organization/users/remove
---

# Remove User

`$ ant beta:organization:users remove`

**DELETE** `/v1/organizations/users/{user_id}`

Remove a member from the organization.

## Parameters

- `--user-id: string` (path parameter)

  ID of the User.

## Returns

- `BetaOrganizationUserRemoveResponse: object`

  - `type: "user_deleted"`

    Deleted object type.

    For Users, this is always `"user_deleted"`.

  - `id: string`

    ID of the User.

## Example

```bash
ant beta:organization:users remove \
  --user-id user_id
```

### Response (200)

```json
{
  "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "type": "user_deleted"
}
```
