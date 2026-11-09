---
title: Update Workspace Member
url: https://platform.claude.com/docs/en/api/cli/beta/organization/workspaces/members/update
---

# Update Workspace Member

`$ ant beta:organization:workspaces:members update`

**POST** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Update Workspace Member

## Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

- `--user-id: string` (path parameter)

  ID of the User.

- `--workspace-role: BetaWorkspaceRole`

  New workspace role for the User.

  - `"workspace_admin"`

  - `"workspace_billing"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

## Returns

- `beta_workspace_member: object`

  - `type: "workspace_member"`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

  - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

## Example

```bash
ant beta:organization:workspaces:members update \
  --workspace-id workspace_id \
  --user-id user_id \
  --workspace-role workspace_admin
```

### Response (200)

```json
{
  "type": "workspace_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "workspace_role": "workspace_admin"
}
```
