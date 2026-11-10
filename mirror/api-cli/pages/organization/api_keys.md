---
title: API Keys
url: https://platform.claude.com/docs/en/api/cli/organization/api_keys
---

# API Keys

## List API Keys

`$ ant organization:api-keys list`

**GET** `/v1/organizations/api_keys`

List API Keys

### Parameters

- `--after-id: optional string` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `--before-id: optional string` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `--created-by-user-id: optional string` (query parameter)

  Filter by the ID of the User who created the object.

- `--limit: optional number` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  minimum: 1, maximum: 1000

- `--status: optional "active" or "archived" or "expired" or "inactive"` (query parameter)

  Filter by API key status.

  - `"active"`

  - `"archived"`

  - `"expired"`

  - `"inactive"`

- `--workspace-id: optional string` (query parameter)

  Filter by Workspace ID.

### Returns

- `ListResponse_ApiKey_: object`

  - `data: array of APIKey`

    - `type: "api_key"`

      Object type.

      For API Keys, this is always `"api_key"`.

    - `id: string`

      ID of the API key.

    - `created_at: string`

      RFC 3339 datetime string indicating when the API Key was created.

      format: date-time

    - `created_by: object`

      The ID and type of the actor that created the API key, or `null` when the
      creator is not recorded (legacy, workload-identity-federated, or
      system-created keys).

      - `type: "service_account" or "user"`

        Type of the actor that created the object.

        - `"service_account"`

        - `"user"`

      - `id: string`

        ID of the actor that created the object.

    - `expires_at: string`

      RFC 3339 datetime string indicating when the API Key expires, or `null` if it never expires.

      format: date-time

    - `name: string`

      Name of the API key.

    - `partial_key_hint: string`

      Partially redacted hint for the API key.

    - `principal: APIKeyUserActor or APIKeyServiceAccountActor`

      The principal the API key acts as (a User or a Service Account), or `null` if the API key is not bound to a principal.

      - `api_key_user_actor: object`

        - `type: "user_actor"`

          Principal type. Always `"user_actor"` for a User.

        - `user_id: string`

          ID of the User the API key acts as.

      - `api_key_service_account_actor: object`

        - `type: "service_account_actor"`

          Principal type. Always `"service_account_actor"` for a Service Account.

        - `service_account_id: string`

          ID of the Service Account the API key acts as.

    - `scope: APIKeyOrganizationScope or APIKeyWorkspaceScope`

      Where the API key belongs: its Workspace (`{"type": "workspace", "workspace_id": "wrkspc_..."}`, with the Workspace's real ID even when it is the organization's default Workspace), or the organization (`{"type": "organization"}`) for a principal-bound API key that has no Workspace.

      - `api_key_organization_scope: object`

        - `type: "organization"`

          Scope type. Always `"organization"`: the API key has no Workspace. Only a principal-bound API key can have this scope.

      - `api_key_workspace_scope: object`

        - `type: "workspace"`

          Scope type. Always `"workspace"`: the API key belongs to one Workspace.

        - `workspace_id: string`

          ID of the Workspace the API key belongs to, including when it is the organization's default Workspace.

    - `status: "active" or "archived" or "expired" or "inactive"`

      Status of the API key.

      - `"active"`

      - `"archived"`

      - `"expired"`

      - `"inactive"`

  - `first_id: string`

    First ID in the `data` list. Can be used as the `before_id` for the previous page.

  - `has_more: boolean`

    Indicates if there are more results in the requested page direction.

  - `last_id: string`

    Last ID in the `data` list. Can be used as the `after_id` for the next page.

### Example

```bash
ant organization:api-keys list
```

#### Response (200)

```json
{
  "data": [
    {
      "id": "apikey_01Rj2N8SVvo6BePZj99NhmiT",
      "created_at": "2024-10-30T23:58:27.427722Z",
      "created_by": {
        "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
        "type": "user"
      },
      "expires_at": "2024-10-30T23:58:27.427722Z",
      "name": "Developer Key",
      "partial_key_hint": "sk-ant-api03-R2D...igAA",
      "principal": {
        "type": "user_actor",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
      },
      "scope": {
        "type": "workspace",
        "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
      },
      "status": "active",
      "type": "api_key"
    }
  ],
  "first_id": "first_id",
  "has_more": true,
  "last_id": "last_id"
}
```

## Retrieve API Key (Admin API)

`$ ant organization:api-keys retrieve`

**GET** `/v1/organizations/api_keys/{api_key_id}`

Retrieve information about a single API key in your organization, looked up by its ID. This Admin API endpoint requires an Admin API key, is intended for programmatic key management, and never returns the key's secret value. To view or create your own API keys, go to [API keys](https://platform.claude.com/settings/keys) in the Claude Console.

### Parameters

- `--api-key-id: string` (path parameter)

  ID of the API key.

### Returns

- `api_key: object`

  - `type: "api_key"`

    Object type.

    For API Keys, this is always `"api_key"`.

  - `id: string`

    ID of the API key.

  - `created_at: string`

    RFC 3339 datetime string indicating when the API Key was created.

    format: date-time

  - `created_by: object`

    The ID and type of the actor that created the API key, or `null` when the
    creator is not recorded (legacy, workload-identity-federated, or
    system-created keys).

    - `type: "service_account" or "user"`

      Type of the actor that created the object.

      - `"service_account"`

      - `"user"`

    - `id: string`

      ID of the actor that created the object.

  - `expires_at: string`

    RFC 3339 datetime string indicating when the API Key expires, or `null` if it never expires.

    format: date-time

  - `name: string`

    Name of the API key.

  - `partial_key_hint: string`

    Partially redacted hint for the API key.

  - `principal: APIKeyUserActor or APIKeyServiceAccountActor`

    The principal the API key acts as (a User or a Service Account), or `null` if the API key is not bound to a principal.

    - `api_key_user_actor: object`

      - `type: "user_actor"`

        Principal type. Always `"user_actor"` for a User.

      - `user_id: string`

        ID of the User the API key acts as.

    - `api_key_service_account_actor: object`

      - `type: "service_account_actor"`

        Principal type. Always `"service_account_actor"` for a Service Account.

      - `service_account_id: string`

        ID of the Service Account the API key acts as.

  - `scope: APIKeyOrganizationScope or APIKeyWorkspaceScope`

    Where the API key belongs: its Workspace (`{"type": "workspace", "workspace_id": "wrkspc_..."}`, with the Workspace's real ID even when it is the organization's default Workspace), or the organization (`{"type": "organization"}`) for a principal-bound API key that has no Workspace.

    - `api_key_organization_scope: object`

      - `type: "organization"`

        Scope type. Always `"organization"`: the API key has no Workspace. Only a principal-bound API key can have this scope.

    - `api_key_workspace_scope: object`

      - `type: "workspace"`

        Scope type. Always `"workspace"`: the API key belongs to one Workspace.

      - `workspace_id: string`

        ID of the Workspace the API key belongs to, including when it is the organization's default Workspace.

  - `status: "active" or "archived" or "expired" or "inactive"`

    Status of the API key.

    - `"active"`

    - `"archived"`

    - `"expired"`

    - `"inactive"`

### Example

```bash
ant organization:api-keys retrieve \
  --api-key-id api_key_id
```

#### Response (200)

```json
{
  "id": "apikey_01Rj2N8SVvo6BePZj99NhmiT",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by": {
    "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
    "type": "user"
  },
  "expires_at": "2024-10-30T23:58:27.427722Z",
  "name": "Developer Key",
  "partial_key_hint": "sk-ant-api03-R2D...igAA",
  "principal": {
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "scope": {
    "type": "workspace",
    "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  },
  "status": "active",
  "type": "api_key"
}
```

## Update API Key

`$ ant organization:api-keys update`

**POST** `/v1/organizations/api_keys/{api_key_id}`

Update API Key

### Parameters

- `--api-key-id: string` (path parameter)

  ID of the API key.

- `--name: optional string`

  Name of the API key.

  minLength: 1, maxLength: 500

- `--status: optional "active" or "archived" or "inactive"`

  Status of the API key.

  - `"active"`

  - `"archived"`

  - `"inactive"`

### Returns

- `api_key: object`

  - `type: "api_key"`

    Object type.

    For API Keys, this is always `"api_key"`.

  - `id: string`

    ID of the API key.

  - `created_at: string`

    RFC 3339 datetime string indicating when the API Key was created.

    format: date-time

  - `created_by: object`

    The ID and type of the actor that created the API key, or `null` when the
    creator is not recorded (legacy, workload-identity-federated, or
    system-created keys).

    - `type: "service_account" or "user"`

      Type of the actor that created the object.

      - `"service_account"`

      - `"user"`

    - `id: string`

      ID of the actor that created the object.

  - `expires_at: string`

    RFC 3339 datetime string indicating when the API Key expires, or `null` if it never expires.

    format: date-time

  - `name: string`

    Name of the API key.

  - `partial_key_hint: string`

    Partially redacted hint for the API key.

  - `principal: APIKeyUserActor or APIKeyServiceAccountActor`

    The principal the API key acts as (a User or a Service Account), or `null` if the API key is not bound to a principal.

    - `api_key_user_actor: object`

      - `type: "user_actor"`

        Principal type. Always `"user_actor"` for a User.

      - `user_id: string`

        ID of the User the API key acts as.

    - `api_key_service_account_actor: object`

      - `type: "service_account_actor"`

        Principal type. Always `"service_account_actor"` for a Service Account.

      - `service_account_id: string`

        ID of the Service Account the API key acts as.

  - `scope: APIKeyOrganizationScope or APIKeyWorkspaceScope`

    Where the API key belongs: its Workspace (`{"type": "workspace", "workspace_id": "wrkspc_..."}`, with the Workspace's real ID even when it is the organization's default Workspace), or the organization (`{"type": "organization"}`) for a principal-bound API key that has no Workspace.

    - `api_key_organization_scope: object`

      - `type: "organization"`

        Scope type. Always `"organization"`: the API key has no Workspace. Only a principal-bound API key can have this scope.

    - `api_key_workspace_scope: object`

      - `type: "workspace"`

        Scope type. Always `"workspace"`: the API key belongs to one Workspace.

      - `workspace_id: string`

        ID of the Workspace the API key belongs to, including when it is the organization's default Workspace.

  - `status: "active" or "archived" or "expired" or "inactive"`

    Status of the API key.

    - `"active"`

    - `"archived"`

    - `"expired"`

    - `"inactive"`

### Example

```bash
ant organization:api-keys update \
  --api-key-id api_key_id
```

#### Response (200)

```json
{
  "id": "apikey_01Rj2N8SVvo6BePZj99NhmiT",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by": {
    "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
    "type": "user"
  },
  "expires_at": "2024-10-30T23:58:27.427722Z",
  "name": "Developer Key",
  "partial_key_hint": "sk-ant-api03-R2D...igAA",
  "principal": {
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "scope": {
    "type": "workspace",
    "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  },
  "status": "active",
  "type": "api_key"
}
```

## Domain types

### API Key

- `api_key: object`

  - `type: "api_key"`

    Object type.

    For API Keys, this is always `"api_key"`.

  - `id: string`

    ID of the API key.

  - `created_at: string`

    RFC 3339 datetime string indicating when the API Key was created.

    format: date-time

  - `created_by: object`

    The ID and type of the actor that created the API key, or `null` when the
    creator is not recorded (legacy, workload-identity-federated, or
    system-created keys).

    - `type: "service_account" or "user"`

      Type of the actor that created the object.

      - `"service_account"`

      - `"user"`

    - `id: string`

      ID of the actor that created the object.

  - `expires_at: string`

    RFC 3339 datetime string indicating when the API Key expires, or `null` if it never expires.

    format: date-time

  - `name: string`

    Name of the API key.

  - `partial_key_hint: string`

    Partially redacted hint for the API key.

  - `principal: APIKeyUserActor or APIKeyServiceAccountActor`

    The principal the API key acts as (a User or a Service Account), or `null` if the API key is not bound to a principal.

    - `api_key_user_actor: object`

      - `type: "user_actor"`

        Principal type. Always `"user_actor"` for a User.

      - `user_id: string`

        ID of the User the API key acts as.

    - `api_key_service_account_actor: object`

      - `type: "service_account_actor"`

        Principal type. Always `"service_account_actor"` for a Service Account.

      - `service_account_id: string`

        ID of the Service Account the API key acts as.

  - `scope: APIKeyOrganizationScope or APIKeyWorkspaceScope`

    Where the API key belongs: its Workspace (`{"type": "workspace", "workspace_id": "wrkspc_..."}`, with the Workspace's real ID even when it is the organization's default Workspace), or the organization (`{"type": "organization"}`) for a principal-bound API key that has no Workspace.

    - `api_key_organization_scope: object`

      - `type: "organization"`

        Scope type. Always `"organization"`: the API key has no Workspace. Only a principal-bound API key can have this scope.

    - `api_key_workspace_scope: object`

      - `type: "workspace"`

        Scope type. Always `"workspace"`: the API key belongs to one Workspace.

      - `workspace_id: string`

        ID of the Workspace the API key belongs to, including when it is the organization's default Workspace.

  - `status: "active" or "archived" or "expired" or "inactive"`

    Status of the API key.

    - `"active"`

    - `"archived"`

    - `"expired"`

    - `"inactive"`

### API Key Created By

- `api_key_created_by: object`

  - `type: "service_account" or "user"`

    Type of the actor that created the object.

    - `"service_account"`

    - `"user"`

  - `id: string`

    ID of the actor that created the object.

### API Key Organization Scope

- `api_key_organization_scope: object`

  - `type: "organization"`

    Scope type. Always `"organization"`: the API key has no Workspace. Only a principal-bound API key can have this scope.

### API Key Service Account Actor

- `api_key_service_account_actor: object`

  - `type: "service_account_actor"`

    Principal type. Always `"service_account_actor"` for a Service Account.

  - `service_account_id: string`

    ID of the Service Account the API key acts as.

### API Key User Actor

- `api_key_user_actor: object`

  - `type: "user_actor"`

    Principal type. Always `"user_actor"` for a User.

  - `user_id: string`

    ID of the User the API key acts as.

### API Key Workspace Scope

- `api_key_workspace_scope: object`

  - `type: "workspace"`

    Scope type. Always `"workspace"`: the API key belongs to one Workspace.

  - `workspace_id: string`

    ID of the Workspace the API key belongs to, including when it is the organization's default Workspace.

### Org API Key Limit Exceeded Error Details

- `org_api_key_limit_exceeded_error_details: object`

  The organization has reached its limit of active API keys.

  - `error_code: "org_api_key_limit_exceeded"`

### Workspace API Key Limit Exceeded Error Details

- `workspace_api_key_limit_exceeded_error_details: object`

  The workspace has reached its limit of active API keys.

  - `error_code: "workspace_api_key_limit_exceeded"`
