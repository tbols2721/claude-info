---
title: Delete Workspace Member
url: https://platform.claude.com/docs/en/api/cli/beta/organization/workspaces/members/remove
---

# Delete Workspace Member

`$ ant beta:organization:workspaces:members remove`

**DELETE** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Delete Workspace Member

## Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

- `--user-id: string` (path parameter)

  ID of the User.

## Returns

- `BetaOrganizationWorkspaceMemberRemoveResponse: object`

  - `type: "workspace_member_deleted"`

    Deleted object type.

    For Workspace Members, this is always `"workspace_member_deleted"`.

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

## Example

```bash
ant beta:organization:workspaces:members remove \
  --workspace-id workspace_id \
  --user-id user_id
```

### Response (200)

```json
{
  "type": "workspace_member_deleted",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
}
```
