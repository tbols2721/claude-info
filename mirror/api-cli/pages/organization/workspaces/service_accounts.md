---
title: Service Accounts
url: https://platform.claude.com/docs/en/api/cli/organization/workspaces/service_accounts
---

# Service Accounts

## List Service Account Workspace Members

`$ ant organization:workspaces:service-accounts list`

**GET** `/v1/organizations/workspaces/{workspace_id}/service_accounts`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

List the service accounts that are members of a workspace.

Each entry includes the service account's `workspace_role`. Use `limit`
and the `next_page` cursor to paginate. Archived workspaces return 400;
use `GET /service_accounts/{id}/workspaces` to audit memberships of an
archived workspace. The implicit default-workspace membership is not
included in this list. Memberships of archived service accounts are
omitted from the results.

### Parameters

- `--workspace-id: string` (path parameter)

  ID of the workspace.

- `--limit: optional number` (query parameter)

  Number of results per page.

  minimum: 1, maximum: 100

- `--page: optional string` (query parameter)

  Opaque cursor from a previous response's `next_page`.

### Returns

- `ServiceAccountWorkspaceMemberListResponse: object`

  - `data: array of ServiceAccountWorkspaceMember`

    - `type: "service_account_workspace_member"`

    - `created_by_actor_id: string`

      Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

    - `implicit: boolean`

      True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

    - `service_account_id: string`

      Tagged service account ID (`svac_...`).

    - `workspace_id: string`

      Tagged workspace ID (`wrkspc_...`).

    - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

      Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

      - `"workspace_admin"`

      - `"workspace_billing"`

      - `"workspace_developer"`

      - `"workspace_restricted_developer"`

      - `"workspace_user"`

  - `next_page: string`

    Opaque cursor for the next page, or null if no more results.

### Example

```bash
ant organization:workspaces:service-accounts list \
  --workspace-id workspace_id
```

#### Response (200)

```json
{
  "data": [
    {
      "created_by_actor_id": "created_by_actor_id",
      "implicit": true,
      "service_account_id": "service_account_id",
      "type": "service_account_workspace_member",
      "workspace_id": "workspace_id",
      "workspace_role": "workspace_admin"
    }
  ],
  "next_page": "next_page"
}
```

## Create Service Account Workspace Member

`$ ant organization:workspaces:service-accounts add`

**POST** `/v1/organizations/workspaces/{workspace_id}/service_accounts`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

Add a service account to a workspace with the given `workspace_role`.

The role determines what the service account can do in the workspace and
which workspace-scoped permissions it can be granted when authenticating
through federation. Every service account is already an implicit
`workspace_user` member of the default workspace; adding it explicitly
assigns a chosen role. If the service account is already an explicit
member of the workspace, its `workspace_role` is replaced with the
value supplied here. Archived workspaces return 400. Archived service
accounts cannot be added and are rejected.

### Parameters

- `--workspace-id: string` (path parameter)

  ID of the workspace.

- `--service-account-id: string`

  Tagged service account ID to add.

- `--workspace-role: NoBillingWorkspaceRole`

  Role to assign to the service account in this workspace.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

### Returns

- `service_account_workspace_member: object`

  - `type: "service_account_workspace_member"`

  - `created_by_actor_id: string`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: boolean`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: string`

    Tagged service account ID (`svac_...`).

  - `workspace_id: string`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

### Example

```bash
ant organization:workspaces:service-accounts add \
  --workspace-id workspace_id \
  --service-account-id service_account_id \
  --workspace-role workspace_admin
```

#### Response (200)

```json
{
  "created_by_actor_id": "created_by_actor_id",
  "implicit": true,
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member",
  "workspace_id": "workspace_id",
  "workspace_role": "workspace_admin"
}
```

## Get Service Account Workspace Member

`$ ant organization:workspaces:service-accounts retrieve`

**GET** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

Retrieve a service account's membership in a workspace.

Returns the membership record, including the service account's
`workspace_role` in this workspace. Archived workspaces return 400. For
the default workspace, returns the implicit (`implicit: true`)
membership when no explicit membership exists; an explicitly added
membership is returned with its assigned role. An archived service
account returns 404.

### Parameters

- `--workspace-id: string` (path parameter)

  ID of the workspace.

- `--service-account-id: string` (path parameter)

  ID of the service account.

### Returns

- `service_account_workspace_member: object`

  - `type: "service_account_workspace_member"`

  - `created_by_actor_id: string`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: boolean`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: string`

    Tagged service account ID (`svac_...`).

  - `workspace_id: string`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

### Example

```bash
ant organization:workspaces:service-accounts retrieve \
  --workspace-id workspace_id \
  --service-account-id service_account_id
```

#### Response (200)

```json
{
  "created_by_actor_id": "created_by_actor_id",
  "implicit": true,
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member",
  "workspace_id": "workspace_id",
  "workspace_role": "workspace_admin"
}
```

## Update Service Account Workspace Member

`$ ant organization:workspaces:service-accounts update`

**POST** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

Change a service account's role in a workspace.

The new `workspace_role` replaces the current one. Only explicit
memberships can be updated; to set a role on the implicit
default-workspace membership, add the service account explicitly with
`POST /workspaces/{workspace_id}/service_accounts`. Archived workspaces
return 400. Archived service accounts cannot be updated and are
rejected.

### Parameters

- `--workspace-id: string` (path parameter)

  ID of the workspace.

- `--service-account-id: string` (path parameter)

  ID of the service account.

- `--workspace-role: NoBillingWorkspaceRole`

  New role for the service account in this workspace.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

### Returns

- `service_account_workspace_member: object`

  - `type: "service_account_workspace_member"`

  - `created_by_actor_id: string`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: boolean`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: string`

    Tagged service account ID (`svac_...`).

  - `workspace_id: string`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

### Example

```bash
ant organization:workspaces:service-accounts update \
  --workspace-id workspace_id \
  --service-account-id service_account_id \
  --workspace-role workspace_admin
```

#### Response (200)

```json
{
  "created_by_actor_id": "created_by_actor_id",
  "implicit": true,
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member",
  "workspace_id": "workspace_id",
  "workspace_role": "workspace_admin"
}
```

## Delete Service Account Workspace Member

`$ ant organization:workspaces:service-accounts remove`

**DELETE** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

Remove a service account from a workspace.

Removal is idempotent (returns 200 even if the membership was already
removed). A DELETE against the implicit default-workspace membership
returns 200 but is a no-op and the membership persists; deleting an
explicit default-workspace row reverts to the implicit `workspace_user`
membership. Archived workspaces return 400.

### Parameters

- `--workspace-id: string` (path parameter)

  ID of the workspace.

- `--service-account-id: string` (path parameter)

  ID of the service account.

### Returns

- `OrganizationWorkspaceServiceAccountRemoveResponse: object`

  - `type: "service_account_workspace_member_deleted"`

  - `service_account_id: string`

    Tagged service account ID (`svac_...`) named in the delete request. Removal is idempotent; see the endpoint description for the implicit-membership no-op.

  - `workspace_id: string`

    Tagged workspace ID (`wrkspc_...`) named in the delete request.

### Example

```bash
ant organization:workspaces:service-accounts remove \
  --workspace-id workspace_id \
  --service-account-id service_account_id
```

#### Response (200)

```json
{
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member_deleted",
  "workspace_id": "workspace_id"
}
```
