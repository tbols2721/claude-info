---
title: Create Workspace Member
url: https://platform.claude.com/docs/en/api/cli/organization/workspaces/members/add
---

# Create Workspace Member

`$ ant organization:workspaces:members add`

**POST** `/v1/organizations/workspaces/{workspace_id}/members`

Create Workspace Member

## Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

- `--user-id: string`

  ID of the User.

- `--workspace-role: NoBillingWorkspaceRole`

  Role of the new Workspace Member. Cannot be `workspace_billing`.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

## Returns

- `workspace_member: object`

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
ant organization:workspaces:members add \
  --workspace-id workspace_id \
  --user-id user_01WxYzAbCdEfGhJkMnPqRsTu \
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
