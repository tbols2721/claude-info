---
title: List Service Accounts
url: https://platform.claude.com/docs/en/api/cli/organization/service_accounts/list
---

# List Service Accounts

`$ ant organization:service-accounts list`

**GET** `/v1/organizations/service_accounts`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

List service accounts in the caller's organization.

Results are ordered by creation time, newest first. Use `limit` and the
`next_page` cursor to paginate; set `include_archived=true` to include
archived service accounts.

## Parameters

- `--include-archived: optional boolean` (query parameter)

  Include archived resources. Defaults to false.

- `--limit: optional number` (query parameter)

  Number of results per page.

  minimum: 1, maximum: 100

- `--page: optional string` (query parameter)

  Opaque cursor from a previous response's `next_page`.

## Returns

- `ServiceAccountListResponse: object`

  - `data: array of ServiceAccount`

    - `type: "service_account"`

    - `id: string`

      Tagged ID of the service account.

    - `archived_at: string`

      If set, this service account is archived.

      format: date-time

    - `archived_by_actor_id: string`

      Tagged ID (`user_`/`svac_`) of the actor that archived this service account.

    - `created_at: string`

      When this service account was created.

      format: date-time

    - `created_by_actor_id: string`

      Tagged ID (`user_`/`svac_`) of the actor that created this service account.

    - `description: string`

      Optional free-text description.

    - `name: string`

      Admin-chosen slug identifier.

    - `organization_role: "admin" or "developer"`

      Org-level role. A federation rule may only be created or retargeted to grant `org:admin` scope when this is `admin`. A rule granting `org:admin` whose target is later demoted to `developer` is rejected at token exchange. Rules granting `org:admin` are managed in the Console.

      - `"admin"`

      - `"developer"`

    - `updated_at: string`

      When this service account was last updated.

      format: date-time

    - `updated_by_actor_id: string`

      Tagged ID (`user_`/`svac_`) of the actor that last updated this service account.

  - `next_page: string`

    Opaque cursor for the next page, or null if no more results.

## Example

```bash
ant organization:service-accounts list
```

### Response (200)

```json
{
  "data": [
    {
      "id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
      "archived_at": "2019-12-27T18:11:19.117Z",
      "archived_by_actor_id": "archived_by_actor_id",
      "created_at": "2024-10-30T23:58:27.427722Z",
      "created_by_actor_id": "created_by_actor_id",
      "description": "description",
      "name": "ci-deploy-bot",
      "organization_role": "admin",
      "type": "service_account",
      "updated_at": "2024-10-30T23:58:27.427722Z",
      "updated_by_actor_id": "updated_by_actor_id"
    }
  ],
  "next_page": "next_page"
}
```
