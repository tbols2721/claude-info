---
title: Members
url: https://platform.claude.com/docs/en/api/cli/organization/workspaces/members
---

# Members

## List Workspace Members

`$ ant organization:workspaces:members list`

**GET** `/v1/organizations/workspaces/{workspace_id}/members`

List Workspace Members

### Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

- `--after-id: optional string` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `--before-id: optional string` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `--limit: optional number` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  minimum: 1, maximum: 1000

### Returns

- `ListResponse_WorkspaceMemberSchema_: object`

  - `data: array of WorkspaceMember`

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

  - `first_id: string`

    First ID in the `data` list. Can be used as the `before_id` for the previous page.

  - `has_more: boolean`

    Indicates if there are more results in the requested page direction.

  - `last_id: string`

    Last ID in the `data` list. Can be used as the `after_id` for the next page.

### Example

```bash
ant organization:workspaces:members list \
  --workspace-id workspace_id
```

#### Response (200)

```json
{
  "data": [
    {
      "type": "workspace_member",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
      "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      "workspace_role": "workspace_admin"
    }
  ],
  "first_id": "first_id",
  "has_more": true,
  "last_id": "last_id"
}
```

## Create Workspace Member

`$ ant organization:workspaces:members add`

**POST** `/v1/organizations/workspaces/{workspace_id}/members`

Create Workspace Member

### Parameters

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

### Returns

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

### Example

```bash
ant organization:workspaces:members add \
  --workspace-id workspace_id \
  --user-id user_01WxYzAbCdEfGhJkMnPqRsTu \
  --workspace-role workspace_admin
```

#### Response (200)

```json
{
  "type": "workspace_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "workspace_role": "workspace_admin"
}
```

## Get Workspace Member

`$ ant organization:workspaces:members retrieve`

**GET** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Get Workspace Member

### Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

- `--user-id: string` (path parameter)

  ID of the User.

### Returns

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

### Example

```bash
ant organization:workspaces:members retrieve \
  --workspace-id workspace_id \
  --user-id user_id
```

#### Response (200)

```json
{
  "type": "workspace_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "workspace_role": "workspace_admin"
}
```

## Update Workspace Member

`$ ant organization:workspaces:members update`

**POST** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Update Workspace Member

### Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

- `--user-id: string` (path parameter)

  ID of the User.

- `--workspace-role: WorkspaceRole`

  New workspace role for the User.

  - `"workspace_admin"`

  - `"workspace_billing"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

### Returns

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

### Example

```bash
ant organization:workspaces:members update \
  --workspace-id workspace_id \
  --user-id user_id \
  --workspace-role workspace_admin
```

#### Response (200)

```json
{
  "type": "workspace_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "workspace_role": "workspace_admin"
}
```

## Delete Workspace Member

`$ ant organization:workspaces:members remove`

**DELETE** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Delete Workspace Member

### Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

- `--user-id: string` (path parameter)

  ID of the User.

### Returns

- `OrganizationWorkspaceMemberRemoveResponse: object`

  - `type: "workspace_member_deleted"`

    Deleted object type.

    For Workspace Members, this is always `"workspace_member_deleted"`.

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

### Example

```bash
ant organization:workspaces:members remove \
  --workspace-id workspace_id \
  --user-id user_id
```

#### Response (200)

```json
{
  "type": "workspace_member_deleted",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
}
```
