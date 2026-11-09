---
title: List Service Account Workspace Members
url: https://platform.claude.com/docs/en/api/cli/organization/workspaces/service_accounts/list
---

# List Service Account Workspace Members

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

## Parameters

- `--workspace-id: string` (path parameter)

  ID of the workspace.

- `--limit: optional number` (query parameter)

  Number of results per page.

  minimum: 1, maximum: 100

- `--page: optional string` (query parameter)

  Opaque cursor from a previous response's `next_page`.

## Returns

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

## Example

```bash
ant organization:workspaces:service-accounts list \
  --workspace-id workspace_id
```

### Response (200)

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
