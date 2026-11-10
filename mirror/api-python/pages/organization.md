---
title: Organization
url: https://platform.claude.com/docs/en/api/python/organization
---

# Organization

## Get Current Organization

`organization.retrieve() -> OrganizationInfo`

**GET** `/v1/organizations/me`

Retrieve information about the organization associated with the authenticated API key.

### Returns

- `class OrganizationInfo`

  - `type: Literal["organization"]`

    Object type.

    For Organizations, this is always `"organization"`.

    default: organization

  - `id: str`

    ID of the Organization.

    format: uuid

  - `name: str`

    Name of the Organization.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
organization_info = client.organization.retrieve()
print(organization_info.id)
```

#### Response (200)

```json
{
  "id": "12345678-1234-5678-1234-567812345678",
  "name": "Organization Name",
  "type": "organization"
}
```

## Domain types

### Concurrent Membership Change Error Details

- `class ConcurrentMembershipChangeErrorDetails`

  Another change to the organization's members is in progress. Retry the request once it completes.

  - `error_code: Literal["concurrent_membership_change"]`

### Org Member Limit Exceeded Error Details

- `class OrgMemberLimitExceededErrorDetails`

  The organization has reached the member limit that Anthropic set for it. Pending invites count toward the limit.

  - `error_code: Literal["org_member_limit_exceeded"]`

### Organization Info

- `class OrganizationInfo`

  - `type: Literal["organization"]`

    Object type.

    For Organizations, this is always `"organization"`.

    default: organization

  - `id: str`

    ID of the Organization.

    format: uuid

  - `name: str`

    Name of the Organization.

### Organization Role

- `type OrganizationRole = Literal["admin", "billing", "claude_code_user", 6 more]`

  - `"admin"`

  - `"billing"`

  - `"claude_code_user"`

  - `"developer"`

  - `"managed"`

  - `"membership_admin"`

  - `"owner"`

  - `"primary_owner"`

  - `"user"`

## Organization › API Keys

### List API Keys

`organization.api_keys.list(**kwargs) -> SyncPage[APIKey]`

**GET** `/v1/organizations/api_keys`

List API Keys

#### Parameters

- `after_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `created_by_user_id: Optional[str]` (query parameter)

  Filter by the ID of the User who created the object.

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `status: Optional[Literal["active", "archived", "expired", "inactive"]]` (query parameter)

  Filter by API key status.

  - `"active"`

  - `"archived"`

  - `"expired"`

  - `"inactive"`

- `workspace_id: Optional[str]` (query parameter)

  Filter by Workspace ID.

#### Returns

- `class APIKey`

  - `type: Literal["api_key"]`

    Object type.

    For API Keys, this is always `"api_key"`.

    default: api_key

  - `id: str`

    ID of the API key.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the API Key was created.

    format: date-time

  - `created_by: Optional[APIKeyCreatedBy]`

    The ID and type of the actor that created the API key, or `null` when the
    creator is not recorded (legacy, workload-identity-federated, or
    system-created keys).

    - `type: Literal["service_account", "user"]`

      Type of the actor that created the object.

      - `"service_account"`

      - `"user"`

    - `id: str`

      ID of the actor that created the object.

  - `expires_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the API Key expires, or `null` if it never expires.

    format: date-time

  - `name: str`

    Name of the API key.

  - `partial_key_hint: Optional[str]`

    Partially redacted hint for the API key.

  - `principal: Optional[Principal]`

    The principal the API key acts as (a User or a Service Account), or `null` if the API key is not bound to a principal.

    - `class APIKeyUserActor`

      - `type: Literal["user_actor"]`

        Principal type. Always `"user_actor"` for a User.

        default: user_actor

      - `user_id: str`

        ID of the User the API key acts as.

    - `class APIKeyServiceAccountActor`

      - `type: Literal["service_account_actor"]`

        Principal type. Always `"service_account_actor"` for a Service Account.

        default: service_account_actor

      - `service_account_id: str`

        ID of the Service Account the API key acts as.

  - `scope: Scope`

    Where the API key belongs: its Workspace (`{"type": "workspace", "workspace_id": "wrkspc_..."}`, with the Workspace's real ID even when it is the organization's default Workspace), or the organization (`{"type": "organization"}`) for a principal-bound API key that has no Workspace.

    - `class APIKeyOrganizationScope`

      - `type: Literal["organization"]`

        Scope type. Always `"organization"`: the API key has no Workspace. Only a principal-bound API key can have this scope.

        default: organization

    - `class APIKeyWorkspaceScope`

      - `type: Literal["workspace"]`

        Scope type. Always `"workspace"`: the API key belongs to one Workspace.

        default: workspace

      - `workspace_id: str`

        ID of the Workspace the API key belongs to, including when it is the organization's default Workspace.

  - `status: Literal["active", "archived", "expired", "inactive"]`

    Status of the API key.

    - `"active"`

    - `"archived"`

    - `"expired"`

    - `"inactive"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.api_keys.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

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

### Retrieve API Key (Admin API)

`organization.api_keys.retrieve(api_key_id) -> APIKey`

**GET** `/v1/organizations/api_keys/{api_key_id}`

Retrieve information about a single API key in your organization, looked up by its ID. This Admin API endpoint requires an Admin API key, is intended for programmatic key management, and never returns the key's secret value. To view or create your own API keys, go to [API keys](https://platform.claude.com/settings/keys) in the Claude Console.

#### Parameters

- `api_key_id: str` (path parameter)

  ID of the API key.

#### Returns

- `class APIKey`

  - `type: Literal["api_key"]`

    Object type.

    For API Keys, this is always `"api_key"`.

    default: api_key

  - `id: str`

    ID of the API key.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the API Key was created.

    format: date-time

  - `created_by: Optional[APIKeyCreatedBy]`

    The ID and type of the actor that created the API key, or `null` when the
    creator is not recorded (legacy, workload-identity-federated, or
    system-created keys).

    - `type: Literal["service_account", "user"]`

      Type of the actor that created the object.

      - `"service_account"`

      - `"user"`

    - `id: str`

      ID of the actor that created the object.

  - `expires_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the API Key expires, or `null` if it never expires.

    format: date-time

  - `name: str`

    Name of the API key.

  - `partial_key_hint: Optional[str]`

    Partially redacted hint for the API key.

  - `principal: Optional[Principal]`

    The principal the API key acts as (a User or a Service Account), or `null` if the API key is not bound to a principal.

    - `class APIKeyUserActor`

      - `type: Literal["user_actor"]`

        Principal type. Always `"user_actor"` for a User.

        default: user_actor

      - `user_id: str`

        ID of the User the API key acts as.

    - `class APIKeyServiceAccountActor`

      - `type: Literal["service_account_actor"]`

        Principal type. Always `"service_account_actor"` for a Service Account.

        default: service_account_actor

      - `service_account_id: str`

        ID of the Service Account the API key acts as.

  - `scope: Scope`

    Where the API key belongs: its Workspace (`{"type": "workspace", "workspace_id": "wrkspc_..."}`, with the Workspace's real ID even when it is the organization's default Workspace), or the organization (`{"type": "organization"}`) for a principal-bound API key that has no Workspace.

    - `class APIKeyOrganizationScope`

      - `type: Literal["organization"]`

        Scope type. Always `"organization"`: the API key has no Workspace. Only a principal-bound API key can have this scope.

        default: organization

    - `class APIKeyWorkspaceScope`

      - `type: Literal["workspace"]`

        Scope type. Always `"workspace"`: the API key belongs to one Workspace.

        default: workspace

      - `workspace_id: str`

        ID of the Workspace the API key belongs to, including when it is the organization's default Workspace.

  - `status: Literal["active", "archived", "expired", "inactive"]`

    Status of the API key.

    - `"active"`

    - `"archived"`

    - `"expired"`

    - `"inactive"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
api_key = client.organization.api_keys.retrieve(
    "api_key_id",
)
print(api_key.id)
```

##### Response (200)

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

### Update API Key

`organization.api_keys.update(api_key_id, **kwargs) -> APIKey`

**POST** `/v1/organizations/api_keys/{api_key_id}`

Update API Key

#### Parameters

- `api_key_id: str` (path parameter)

  ID of the API key.

- `name: Optional[str]`

  Name of the API key.

  minLength: 1, maxLength: 500

- `status: Optional[Literal["active", "archived", "inactive"]]`

  Status of the API key.

  - `"active"`

  - `"archived"`

  - `"inactive"`

#### Returns

- `class APIKey`

  - `type: Literal["api_key"]`

    Object type.

    For API Keys, this is always `"api_key"`.

    default: api_key

  - `id: str`

    ID of the API key.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the API Key was created.

    format: date-time

  - `created_by: Optional[APIKeyCreatedBy]`

    The ID and type of the actor that created the API key, or `null` when the
    creator is not recorded (legacy, workload-identity-federated, or
    system-created keys).

    - `type: Literal["service_account", "user"]`

      Type of the actor that created the object.

      - `"service_account"`

      - `"user"`

    - `id: str`

      ID of the actor that created the object.

  - `expires_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the API Key expires, or `null` if it never expires.

    format: date-time

  - `name: str`

    Name of the API key.

  - `partial_key_hint: Optional[str]`

    Partially redacted hint for the API key.

  - `principal: Optional[Principal]`

    The principal the API key acts as (a User or a Service Account), or `null` if the API key is not bound to a principal.

    - `class APIKeyUserActor`

      - `type: Literal["user_actor"]`

        Principal type. Always `"user_actor"` for a User.

        default: user_actor

      - `user_id: str`

        ID of the User the API key acts as.

    - `class APIKeyServiceAccountActor`

      - `type: Literal["service_account_actor"]`

        Principal type. Always `"service_account_actor"` for a Service Account.

        default: service_account_actor

      - `service_account_id: str`

        ID of the Service Account the API key acts as.

  - `scope: Scope`

    Where the API key belongs: its Workspace (`{"type": "workspace", "workspace_id": "wrkspc_..."}`, with the Workspace's real ID even when it is the organization's default Workspace), or the organization (`{"type": "organization"}`) for a principal-bound API key that has no Workspace.

    - `class APIKeyOrganizationScope`

      - `type: Literal["organization"]`

        Scope type. Always `"organization"`: the API key has no Workspace. Only a principal-bound API key can have this scope.

        default: organization

    - `class APIKeyWorkspaceScope`

      - `type: Literal["workspace"]`

        Scope type. Always `"workspace"`: the API key belongs to one Workspace.

        default: workspace

      - `workspace_id: str`

        ID of the Workspace the API key belongs to, including when it is the organization's default Workspace.

  - `status: Literal["active", "archived", "expired", "inactive"]`

    Status of the API key.

    - `"active"`

    - `"archived"`

    - `"expired"`

    - `"inactive"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
api_key = client.organization.api_keys.update(
    api_key_id="api_key_id",
)
print(api_key.id)
```

##### Response (200)

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

## Organization › External Keys

### Create External Key

`organization.external_keys.create(**kwargs) -> ExternalKey`

**POST** `/v1/organizations/external_keys`

Create an external key config owned by the caller's organization.

#### Parameters

- `provider_config: ProviderConfig`

  KMS provider identity and auth coordinates.

  - `class AWSExternalKeyConfig`

    - `type: Literal["aws"]`

    - `kms_arn: str`

      Full ARN of the AWS KMS key. On Claude Platform on AWS, alias ARNs are rejected, and your organization's own key must be a single-Region key in your organization's AWS account.

      maxLength: 2048

    - `region: Optional[str]`

      AWS region. Derived from `kms_arn` if omitted.

  - `class GCPExternalKeyConfig`

    - `type: Literal["gcp"]`

    - `key_name: str`

      Full resource name of the Cloud KMS key.

  - `class AzureExternalKeyConfigParam`

    Azure Key Vault provider configuration.

    - `type: Literal["azure"]`

    - `key_name: str`

      Name of the key within the vault.

    - `tenant_id: str`

      Azure AD tenant ID.

    - `vault_uri: str`

      Key Vault data-plane URI — `https://{vault-name}.vault.azure.net` or `https://{hsm-name}.managedhsm.azure.net`.

    - `client_id: Optional[str]`

      Azure AD application (client) ID. Omit to use Anthropic's multitenant app. Provide only if using a single-tenant app registration in the customer's directory.

- `display_name: Optional[str]`

  Human-friendly display name.

  minLength: 1, maxLength: 255

- `geo: Optional[Literal["us"]]`

  Data residency geo. Only `us` is supported.

- `user_profile_id: Optional[str]`

  ID of a user profile to bind the key to. A user profile represents one of your customers: bind a customer's key to that customer's user profile. A key bound to a user profile can only be attached to a Workspace that has the same user profile, and the binding cannot be changed later. Omit this field only for your organization's own key, because a key created without a user profile ID can be attached to any Workspace, including another customer's.

#### Returns

- `class ExternalKey`

  CMEK external key config belonging to the caller's organization.

  Configs are organization-scoped. Workspaces attach to a config; once any
  workspace references it, the provider fields become effectively immutable
  (existing encrypted data needs the config for decrypt).

  - `type: Literal["external_key"]`

    default: external_key

  - `id: str`

    Identifier of the external key config: a tagged ID prefixed `ekey_`, or, on Claude Platform on AWS, an AWS KMS key's ARN.

  - `attachment: Attachment`

    Whether any workspace uses this config to encrypt its data — counting live and archived workspaces (an archived workspace's data remains encrypted under the config), excluding deleted ones. Only an attached config is used by the encryption path; an `unattached` config is inert and can be deleted.

    - `class ExternalKeyAttachedAttachment`

      - `type: Literal["attached"]`

        default: attached

    - `class ExternalKeyUnattachedAttachment`

      - `type: Literal["unattached"]`

        default: unattached

  - `created_at: datetime`

    format: date-time

  - `display_name: Optional[str]`

    Human-friendly display name. Null if none was set.

  - `geo: str`

    Data residency geo. Selects the region this key is used in.

  - `provider_config: ProviderConfig`

    KMS provider identity and auth coordinates.

    - `class AWSExternalKeyConfig`

      - `type: Literal["aws"]`

      - `kms_arn: str`

        Full ARN of the AWS KMS key. On Claude Platform on AWS, alias ARNs are rejected, and your organization's own key must be a single-Region key in your organization's AWS account.

        maxLength: 2048

      - `region: Optional[str]`

        AWS region. Derived from `kms_arn` if omitted.

    - `class GCPExternalKeyConfig`

      - `type: Literal["gcp"]`

      - `key_name: str`

        Full resource name of the Cloud KMS key.

    - `class AzureExternalKeyConfig`

      - `type: Literal["azure"]`

      - `key_name: str`

        Name of the key within the vault.

      - `tenant_id: str`

        Azure AD tenant ID.

      - `vault_uri: str`

        Key Vault data-plane URI — `https://{vault-name}.vault.azure.net` or `https://{hsm-name}.managedhsm.azure.net`.

      - `client_id: Optional[str]`

        Azure AD application (client) ID. Omit to use Anthropic's multitenant app. Provide only if using a single-tenant app registration in the customer's directory.

  - `updated_at: datetime`

    format: date-time

  - `user_profile_id: Optional[str]`

    ID of the user profile the key is bound to, or null if the key is not bound to one. A key bound to a user profile can only be attached to a Workspace that has the same user profile. A key that isn't bound can be attached to a Workspace whatever its user profile.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
external_key = client.organization.external_keys.create(
    provider_config={
        "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
        "type": "aws",
    },
)
print(external_key.id)
```

##### Response (200)

```json
{
  "id": "ekey_01SDCCSbTxrXDpWc1phhtcfK",
  "attachment": {
    "type": "attached"
  },
  "created_at": "2024-10-30T23:58:27.427722Z",
  "display_name": "prod-us-key",
  "geo": "us",
  "provider_config": {
    "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
    "type": "aws",
    "region": "us-east-1",
    "role_arn": "arn:aws:iam::111122223333:role/anthropic-cmek"
  },
  "type": "external_key",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "user_profile_id": "uprof_01SDCCSbTxrXDpWc1phhtcfK"
}
```

### List External Keys

`organization.external_keys.list(**kwargs) -> SyncPageCursor[ExternalKey]`

**GET** `/v1/organizations/external_keys`

List external key configs in the caller's organization.

Results are ordered by creation time (newest first). Use the
`next_page` cursor from the response to fetch subsequent pages.

#### Parameters

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `class ExternalKey`

  CMEK external key config belonging to the caller's organization.

  Configs are organization-scoped. Workspaces attach to a config; once any
  workspace references it, the provider fields become effectively immutable
  (existing encrypted data needs the config for decrypt).

  - `type: Literal["external_key"]`

    default: external_key

  - `id: str`

    Identifier of the external key config: a tagged ID prefixed `ekey_`, or, on Claude Platform on AWS, an AWS KMS key's ARN.

  - `attachment: Attachment`

    Whether any workspace uses this config to encrypt its data — counting live and archived workspaces (an archived workspace's data remains encrypted under the config), excluding deleted ones. Only an attached config is used by the encryption path; an `unattached` config is inert and can be deleted.

    - `class ExternalKeyAttachedAttachment`

      - `type: Literal["attached"]`

        default: attached

    - `class ExternalKeyUnattachedAttachment`

      - `type: Literal["unattached"]`

        default: unattached

  - `created_at: datetime`

    format: date-time

  - `display_name: Optional[str]`

    Human-friendly display name. Null if none was set.

  - `geo: str`

    Data residency geo. Selects the region this key is used in.

  - `provider_config: ProviderConfig`

    KMS provider identity and auth coordinates.

    - `class AWSExternalKeyConfig`

      - `type: Literal["aws"]`

      - `kms_arn: str`

        Full ARN of the AWS KMS key. On Claude Platform on AWS, alias ARNs are rejected, and your organization's own key must be a single-Region key in your organization's AWS account.

        maxLength: 2048

      - `region: Optional[str]`

        AWS region. Derived from `kms_arn` if omitted.

    - `class GCPExternalKeyConfig`

      - `type: Literal["gcp"]`

      - `key_name: str`

        Full resource name of the Cloud KMS key.

    - `class AzureExternalKeyConfig`

      - `type: Literal["azure"]`

      - `key_name: str`

        Name of the key within the vault.

      - `tenant_id: str`

        Azure AD tenant ID.

      - `vault_uri: str`

        Key Vault data-plane URI — `https://{vault-name}.vault.azure.net` or `https://{hsm-name}.managedhsm.azure.net`.

      - `client_id: Optional[str]`

        Azure AD application (client) ID. Omit to use Anthropic's multitenant app. Provide only if using a single-tenant app registration in the customer's directory.

  - `updated_at: datetime`

    format: date-time

  - `user_profile_id: Optional[str]`

    ID of the user profile the key is bound to, or null if the key is not bound to one. A key bound to a user profile can only be attached to a Workspace that has the same user profile. A key that isn't bound can be attached to a Workspace whatever its user profile.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.external_keys.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "ekey_01SDCCSbTxrXDpWc1phhtcfK",
      "attachment": {
        "type": "attached"
      },
      "created_at": "2024-10-30T23:58:27.427722Z",
      "display_name": "prod-us-key",
      "geo": "us",
      "provider_config": {
        "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
        "type": "aws",
        "region": "us-east-1",
        "role_arn": "arn:aws:iam::111122223333:role/anthropic-cmek"
      },
      "type": "external_key",
      "updated_at": "2024-10-30T23:58:27.427722Z",
      "user_profile_id": "uprof_01SDCCSbTxrXDpWc1phhtcfK"
    }
  ],
  "next_page": "next_page"
}
```

### Get External Key

`organization.external_keys.retrieve(external_key_id) -> ExternalKey`

**GET** `/v1/organizations/external_keys/{external_key_id}`

Retrieve a single external key config in the caller's organization by ID.

#### Parameters

- `external_key_id: str` (path parameter)

  ID of the External Key.

  maxLength: 2048

#### Returns

- `class ExternalKey`

  CMEK external key config belonging to the caller's organization.

  Configs are organization-scoped. Workspaces attach to a config; once any
  workspace references it, the provider fields become effectively immutable
  (existing encrypted data needs the config for decrypt).

  - `type: Literal["external_key"]`

    default: external_key

  - `id: str`

    Identifier of the external key config: a tagged ID prefixed `ekey_`, or, on Claude Platform on AWS, an AWS KMS key's ARN.

  - `attachment: Attachment`

    Whether any workspace uses this config to encrypt its data — counting live and archived workspaces (an archived workspace's data remains encrypted under the config), excluding deleted ones. Only an attached config is used by the encryption path; an `unattached` config is inert and can be deleted.

    - `class ExternalKeyAttachedAttachment`

      - `type: Literal["attached"]`

        default: attached

    - `class ExternalKeyUnattachedAttachment`

      - `type: Literal["unattached"]`

        default: unattached

  - `created_at: datetime`

    format: date-time

  - `display_name: Optional[str]`

    Human-friendly display name. Null if none was set.

  - `geo: str`

    Data residency geo. Selects the region this key is used in.

  - `provider_config: ProviderConfig`

    KMS provider identity and auth coordinates.

    - `class AWSExternalKeyConfig`

      - `type: Literal["aws"]`

      - `kms_arn: str`

        Full ARN of the AWS KMS key. On Claude Platform on AWS, alias ARNs are rejected, and your organization's own key must be a single-Region key in your organization's AWS account.

        maxLength: 2048

      - `region: Optional[str]`

        AWS region. Derived from `kms_arn` if omitted.

    - `class GCPExternalKeyConfig`

      - `type: Literal["gcp"]`

      - `key_name: str`

        Full resource name of the Cloud KMS key.

    - `class AzureExternalKeyConfig`

      - `type: Literal["azure"]`

      - `key_name: str`

        Name of the key within the vault.

      - `tenant_id: str`

        Azure AD tenant ID.

      - `vault_uri: str`

        Key Vault data-plane URI — `https://{vault-name}.vault.azure.net` or `https://{hsm-name}.managedhsm.azure.net`.

      - `client_id: Optional[str]`

        Azure AD application (client) ID. Omit to use Anthropic's multitenant app. Provide only if using a single-tenant app registration in the customer's directory.

  - `updated_at: datetime`

    format: date-time

  - `user_profile_id: Optional[str]`

    ID of the user profile the key is bound to, or null if the key is not bound to one. A key bound to a user profile can only be attached to a Workspace that has the same user profile. A key that isn't bound can be attached to a Workspace whatever its user profile.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
external_key = client.organization.external_keys.retrieve(
    "external_key_id",
)
print(external_key.id)
```

##### Response (200)

```json
{
  "id": "ekey_01SDCCSbTxrXDpWc1phhtcfK",
  "attachment": {
    "type": "attached"
  },
  "created_at": "2024-10-30T23:58:27.427722Z",
  "display_name": "prod-us-key",
  "geo": "us",
  "provider_config": {
    "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
    "type": "aws",
    "region": "us-east-1",
    "role_arn": "arn:aws:iam::111122223333:role/anthropic-cmek"
  },
  "type": "external_key",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "user_profile_id": "uprof_01SDCCSbTxrXDpWc1phhtcfK"
}
```

### Update External Key

`organization.external_keys.update(external_key_id, **kwargs) -> ExternalKey`

**POST** `/v1/organizations/external_keys/{external_key_id}`

Partially update an external key config. Omitted fields are left unchanged.

`display_name` is always editable. `geo` and `provider_config` cannot
be changed once any workspace references this config, because previously
encrypted data requires the original key identity to decrypt.

#### Parameters

- `external_key_id: str` (path parameter)

  ID of the External Key.

  maxLength: 2048

- `display_name: Optional[str]`

  Human-friendly display name.

  minLength: 1, maxLength: 255

- `geo: Optional[Literal["us"]]`

  Data residency geo. Only `us` is supported.

- `provider_config: Optional[ProviderConfig]`

  KMS provider identity and auth coordinates.

  - `class AWSExternalKeyConfig`

    - `type: Literal["aws"]`

    - `kms_arn: str`

      Full ARN of the AWS KMS key. On Claude Platform on AWS, alias ARNs are rejected, and your organization's own key must be a single-Region key in your organization's AWS account.

      maxLength: 2048

    - `region: Optional[str]`

      AWS region. Derived from `kms_arn` if omitted.

  - `class GCPExternalKeyConfig`

    - `type: Literal["gcp"]`

    - `key_name: str`

      Full resource name of the Cloud KMS key.

  - `class AzureExternalKeyConfigParam`

    Azure Key Vault provider configuration.

    - `type: Literal["azure"]`

    - `key_name: str`

      Name of the key within the vault.

    - `tenant_id: str`

      Azure AD tenant ID.

    - `vault_uri: str`

      Key Vault data-plane URI — `https://{vault-name}.vault.azure.net` or `https://{hsm-name}.managedhsm.azure.net`.

    - `client_id: Optional[str]`

      Azure AD application (client) ID. Omit to use Anthropic's multitenant app. Provide only if using a single-tenant app registration in the customer's directory.

#### Returns

- `class ExternalKey`

  CMEK external key config belonging to the caller's organization.

  Configs are organization-scoped. Workspaces attach to a config; once any
  workspace references it, the provider fields become effectively immutable
  (existing encrypted data needs the config for decrypt).

  - `type: Literal["external_key"]`

    default: external_key

  - `id: str`

    Identifier of the external key config: a tagged ID prefixed `ekey_`, or, on Claude Platform on AWS, an AWS KMS key's ARN.

  - `attachment: Attachment`

    Whether any workspace uses this config to encrypt its data — counting live and archived workspaces (an archived workspace's data remains encrypted under the config), excluding deleted ones. Only an attached config is used by the encryption path; an `unattached` config is inert and can be deleted.

    - `class ExternalKeyAttachedAttachment`

      - `type: Literal["attached"]`

        default: attached

    - `class ExternalKeyUnattachedAttachment`

      - `type: Literal["unattached"]`

        default: unattached

  - `created_at: datetime`

    format: date-time

  - `display_name: Optional[str]`

    Human-friendly display name. Null if none was set.

  - `geo: str`

    Data residency geo. Selects the region this key is used in.

  - `provider_config: ProviderConfig`

    KMS provider identity and auth coordinates.

    - `class AWSExternalKeyConfig`

      - `type: Literal["aws"]`

      - `kms_arn: str`

        Full ARN of the AWS KMS key. On Claude Platform on AWS, alias ARNs are rejected, and your organization's own key must be a single-Region key in your organization's AWS account.

        maxLength: 2048

      - `region: Optional[str]`

        AWS region. Derived from `kms_arn` if omitted.

    - `class GCPExternalKeyConfig`

      - `type: Literal["gcp"]`

      - `key_name: str`

        Full resource name of the Cloud KMS key.

    - `class AzureExternalKeyConfig`

      - `type: Literal["azure"]`

      - `key_name: str`

        Name of the key within the vault.

      - `tenant_id: str`

        Azure AD tenant ID.

      - `vault_uri: str`

        Key Vault data-plane URI — `https://{vault-name}.vault.azure.net` or `https://{hsm-name}.managedhsm.azure.net`.

      - `client_id: Optional[str]`

        Azure AD application (client) ID. Omit to use Anthropic's multitenant app. Provide only if using a single-tenant app registration in the customer's directory.

  - `updated_at: datetime`

    format: date-time

  - `user_profile_id: Optional[str]`

    ID of the user profile the key is bound to, or null if the key is not bound to one. A key bound to a user profile can only be attached to a Workspace that has the same user profile. A key that isn't bound can be attached to a Workspace whatever its user profile.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
external_key = client.organization.external_keys.update(
    external_key_id="external_key_id",
)
print(external_key.id)
```

##### Response (200)

```json
{
  "id": "ekey_01SDCCSbTxrXDpWc1phhtcfK",
  "attachment": {
    "type": "attached"
  },
  "created_at": "2024-10-30T23:58:27.427722Z",
  "display_name": "prod-us-key",
  "geo": "us",
  "provider_config": {
    "kms_arn": "arn:aws:kms:us-east-1:111122223333:key/abcd1234-5678-90ab-cdef-000011112222",
    "type": "aws",
    "region": "us-east-1",
    "role_arn": "arn:aws:iam::111122223333:role/anthropic-cmek"
  },
  "type": "external_key",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "user_profile_id": "uprof_01SDCCSbTxrXDpWc1phhtcfK"
}
```

### Delete External Key

`organization.external_keys.delete(external_key_id) -> ExternalKeyDeleteResponse`

**DELETE** `/v1/organizations/external_keys/{external_key_id}`

Delete an external key config.

The request is rejected if any workspace still references this config.

#### Parameters

- `external_key_id: str` (path parameter)

  ID of the External Key.

  maxLength: 2048

#### Returns

- `class ExternalKeyDeleteResponse`

  - `type: Literal["external_key_deleted"]`

    default: external_key_deleted

  - `id: str`

    ID of the deleted External Key.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
external_key = client.organization.external_keys.delete(
    "external_key_id",
)
print(external_key.id)
```

##### Response (200)

```json
{
  "id": "ekey_01AbCdEfGhIjKlMnOpQrStUv",
  "type": "external_key_deleted"
}
```

### Validate External Key

`organization.external_keys.validate(external_key_id) -> ExternalKeyValidateResponse`

**POST** `/v1/organizations/external_keys/{external_key_id}/validate`

Validate an external key config against the customer's KMS.

Anthropic performs an encrypt/decrypt roundtrip against the configured
KMS key and waits up to 30 seconds for the result. The response status is
`success` if the roundtrip succeeded, or `failure` with an error
message if it failed or timed out.

#### Parameters

- `external_key_id: str` (path parameter)

  ID of the External Key.

  maxLength: 2048

#### Returns

- `class ExternalKeyValidateResponse`

  Result of a validation roundtrip against the customer's KMS.

  HTTP 200 for both outcomes — the operation completed; `status` says
  whether the key works.

  - `type: Literal["external_key_validation"]`

    default: external_key_validation

  - `error: Optional[str]`

    Error message when status is `failure`. Null otherwise.

  - `status: Literal["failure", "success"]`

    `success` — encrypt/decrypt roundtrip succeeded. `failure` — the roundtrip failed or timed out; see `error`.

    - `"failure"`

    - `"success"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
response = client.organization.external_keys.validate(
    "external_key_id",
)
print(response.error)
```

##### Response (200)

```json
{
  "error": "error",
  "status": "failure",
  "type": "external_key_validation"
}
```

## Organization › Federation › Issuers

### Create Federation Issuer

`organization.federation.issuers.create(**kwargs) -> FederationIssuer`

**POST** `/v1/organizations/federation_issuers`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Register an OIDC issuer that Anthropic will trust for workload identity
federation in your organization.

The `jwks` field controls how the issuer's signing keys are obtained and
takes one of three shapes selected by `type`: `discovery` (resolve keys
through OIDC discovery), `explicit_url` (fetch keys from a fixed JWKS
URL), or `inline` (provide a static key set). When `jwks.type` is
`discovery` and no `discovery_base` is set, the issuer URL must be
publicly reachable over HTTPS so Anthropic can fetch the discovery
document; for `explicit_url` and `inline` modes the issuer URL is only
matched as the JWT's `iss` claim and is not fetched.

#### Parameters

- `issuer_url: str`

  The `iss` claim value to match against.

  minLength: 1

- `name: str`

  Slug identifier (lowercase, digits, hyphens). Unique within the organization; a duplicate name returns 409.

  minLength: 1, maxLength: 255

- `check_jti: Optional[bool]`

  Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Defaults to true. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

- `jwks: Optional[JWKS]`

  How signing keys are obtained. Defaults to OIDC discovery.

  - `class JWKSDiscovery`

    JWKS via the issuer's OIDC discovery document.

    - `type: Literal["discovery"]`

    - `ca_cert_pem: Optional[str]`

      Optional custom CA (PEM) for TLS verification of the JWKS fetch.

      maxLength: 8192

    - `discovery_base: Optional[str]`

      Set when the discovery URL differs from `issuer_url`.

  - `class JWKSExplicitURL`

    JWKS fetched from a fixed endpoint.

    - `type: Literal["explicit_url"]`

    - `url: str`

      JWKS endpoint.

      minLength: 1

    - `ca_cert_pem: Optional[str]`

      Optional custom CA (PEM) for TLS verification of the JWKS fetch.

      maxLength: 8192

  - `class JWKSInline`

    JWKS supplied directly; no network fetch.

    - `type: Literal["inline"]`

    - `keys: List[Dict[str, object]]`

      Inline JWK objects.

      minItems: 1

- `max_jwt_lifetime_seconds: Optional[int]`

  Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Defaults to 3600 (1h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  minimum: 1, maximum: 176400

#### Returns

- `class FederationIssuer`

  Registered external OIDC identity provider.

  Records an external IdP the organization trusts for the RFC 7523
  jwt-bearer grant. The `issuer_url` must match the JWT `iss` claim exactly.

  - `type: Literal["federation_issuer"]`

    default: federation_issuer

  - `id: str`

    Tagged ID of the federation issuer.

  - `archived_at: Optional[datetime]`

    If set, all rules referencing this issuer reject token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this issuer.

  - `check_jti: bool`

    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

  - `created_at: datetime`

    When this issuer was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this issuer.

  - `issuer_url: str`

    The `iss` claim value. Incoming JWTs must match exactly.

  - `jwks: JWKS`

    How signing keys are obtained for signature verification.

    - `class JWKSDiscovery`

      JWKS via the issuer's OIDC discovery document.

      - `type: Literal["discovery"]`

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

      - `discovery_base: Optional[str]`

        Set when the discovery URL differs from `issuer_url`.

    - `class JWKSExplicitURL`

      JWKS fetched from a fixed endpoint.

      - `type: Literal["explicit_url"]`

      - `url: str`

        JWKS endpoint.

        minLength: 1

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

    - `class JWKSInline`

      JWKS supplied directly; no network fetch.

      - `type: Literal["inline"]`

      - `keys: List[Dict[str, object]]`

        Inline JWK objects.

        minItems: 1

  - `jwks_polling_disabled_at: Optional[datetime]`

    If set, Anthropic's JWKS poller has paused polling for this issuer after repeated fetch failures. Re-enable by sending `jwks_polling_disabled: false` via the issuer update endpoint (POST) once the upstream JWKS endpoint is fixed. An OAuth caller cannot send this when the issuer backs a rule with any scope other than `workspace:developer` or `workspace:inference`; use a Console session.

    format: date-time

  - `max_jwt_lifetime_seconds: int`

    Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  - `name: str`

    Admin-chosen slug identifier.

  - `poll_status: Optional[FederationIssuerPollStatus]`

    Live state of Anthropic's JWKS polling for this issuer. Populated on both single-issuer retrieval and list responses, including archived issuers. Typically null for inline-key issuers (no polling), or when poll status is temporarily unavailable or polling has not started yet.

    - `consecutive_failures: int`

      Consecutive fetch failures since the last success.

    - `last_fetched_at: Optional[datetime]`

      When the last successful fetch completed.

      format: date-time

    - `next_poll_at: Optional[datetime]`

      When the next fetch is scheduled. Null if paused.

      format: date-time

  - `updated_at: datetime`

    When this issuer was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
federation_issuer = client.organization.federation.issuers.create(
    issuer_url="x",
    name="x",
)
print(federation_issuer.id)
```

##### Response (200)

```json
{
  "id": "fdis_01SDCCSbTxrXDpWc1phhtcfK",
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "check_jti": true,
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "issuer_url": "https://token.actions.githubusercontent.com",
  "jwks": {
    "type": "discovery",
    "ca_cert_pem": "ca_cert_pem",
    "discovery_base": "discovery_base"
  },
  "jwks_polling_disabled_at": "2019-12-27T18:11:19.117Z",
  "max_jwt_lifetime_seconds": 0,
  "name": "github-actions",
  "poll_status": {
    "consecutive_failures": 0,
    "last_fetched_at": "2019-12-27T18:11:19.117Z",
    "next_poll_at": "2019-12-27T18:11:19.117Z"
  },
  "type": "federation_issuer",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id"
}
```

### List Federation Issuers

`organization.federation.issuers.list(**kwargs) -> SyncPageCursor[FederationIssuer]`

**GET** `/v1/organizations/federation_issuers`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

List federation issuers in your organization.

Archived issuers are excluded unless `include_archived=true`.

#### Parameters

- `include_archived: Optional[bool]` (query parameter)

  Include archived resources. Defaults to false.

  default: false

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `class FederationIssuer`

  Registered external OIDC identity provider.

  Records an external IdP the organization trusts for the RFC 7523
  jwt-bearer grant. The `issuer_url` must match the JWT `iss` claim exactly.

  - `type: Literal["federation_issuer"]`

    default: federation_issuer

  - `id: str`

    Tagged ID of the federation issuer.

  - `archived_at: Optional[datetime]`

    If set, all rules referencing this issuer reject token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this issuer.

  - `check_jti: bool`

    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

  - `created_at: datetime`

    When this issuer was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this issuer.

  - `issuer_url: str`

    The `iss` claim value. Incoming JWTs must match exactly.

  - `jwks: JWKS`

    How signing keys are obtained for signature verification.

    - `class JWKSDiscovery`

      JWKS via the issuer's OIDC discovery document.

      - `type: Literal["discovery"]`

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

      - `discovery_base: Optional[str]`

        Set when the discovery URL differs from `issuer_url`.

    - `class JWKSExplicitURL`

      JWKS fetched from a fixed endpoint.

      - `type: Literal["explicit_url"]`

      - `url: str`

        JWKS endpoint.

        minLength: 1

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

    - `class JWKSInline`

      JWKS supplied directly; no network fetch.

      - `type: Literal["inline"]`

      - `keys: List[Dict[str, object]]`

        Inline JWK objects.

        minItems: 1

  - `jwks_polling_disabled_at: Optional[datetime]`

    If set, Anthropic's JWKS poller has paused polling for this issuer after repeated fetch failures. Re-enable by sending `jwks_polling_disabled: false` via the issuer update endpoint (POST) once the upstream JWKS endpoint is fixed. An OAuth caller cannot send this when the issuer backs a rule with any scope other than `workspace:developer` or `workspace:inference`; use a Console session.

    format: date-time

  - `max_jwt_lifetime_seconds: int`

    Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  - `name: str`

    Admin-chosen slug identifier.

  - `poll_status: Optional[FederationIssuerPollStatus]`

    Live state of Anthropic's JWKS polling for this issuer. Populated on both single-issuer retrieval and list responses, including archived issuers. Typically null for inline-key issuers (no polling), or when poll status is temporarily unavailable or polling has not started yet.

    - `consecutive_failures: int`

      Consecutive fetch failures since the last success.

    - `last_fetched_at: Optional[datetime]`

      When the last successful fetch completed.

      format: date-time

    - `next_poll_at: Optional[datetime]`

      When the next fetch is scheduled. Null if paused.

      format: date-time

  - `updated_at: datetime`

    When this issuer was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.federation.issuers.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "fdis_01SDCCSbTxrXDpWc1phhtcfK",
      "archived_at": "2019-12-27T18:11:19.117Z",
      "archived_by_actor_id": "archived_by_actor_id",
      "check_jti": true,
      "created_at": "2024-10-30T23:58:27.427722Z",
      "created_by_actor_id": "created_by_actor_id",
      "issuer_url": "https://token.actions.githubusercontent.com",
      "jwks": {
        "type": "discovery",
        "ca_cert_pem": "ca_cert_pem",
        "discovery_base": "discovery_base"
      },
      "jwks_polling_disabled_at": "2019-12-27T18:11:19.117Z",
      "max_jwt_lifetime_seconds": 0,
      "name": "github-actions",
      "poll_status": {
        "consecutive_failures": 0,
        "last_fetched_at": "2019-12-27T18:11:19.117Z",
        "next_poll_at": "2019-12-27T18:11:19.117Z"
      },
      "type": "federation_issuer",
      "updated_at": "2024-10-30T23:58:27.427722Z",
      "updated_by_actor_id": "updated_by_actor_id"
    }
  ],
  "next_page": "next_page"
}
```

### Get Federation Issuer

`organization.federation.issuers.retrieve(federation_issuer_id) -> FederationIssuer`

**GET** `/v1/organizations/federation_issuers/{federation_issuer_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Retrieve a federation issuer by its ID (`fdis_...`).

#### Parameters

- `federation_issuer_id: str` (path parameter)

  ID of the federation issuer.

#### Returns

- `class FederationIssuer`

  Registered external OIDC identity provider.

  Records an external IdP the organization trusts for the RFC 7523
  jwt-bearer grant. The `issuer_url` must match the JWT `iss` claim exactly.

  - `type: Literal["federation_issuer"]`

    default: federation_issuer

  - `id: str`

    Tagged ID of the federation issuer.

  - `archived_at: Optional[datetime]`

    If set, all rules referencing this issuer reject token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this issuer.

  - `check_jti: bool`

    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

  - `created_at: datetime`

    When this issuer was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this issuer.

  - `issuer_url: str`

    The `iss` claim value. Incoming JWTs must match exactly.

  - `jwks: JWKS`

    How signing keys are obtained for signature verification.

    - `class JWKSDiscovery`

      JWKS via the issuer's OIDC discovery document.

      - `type: Literal["discovery"]`

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

      - `discovery_base: Optional[str]`

        Set when the discovery URL differs from `issuer_url`.

    - `class JWKSExplicitURL`

      JWKS fetched from a fixed endpoint.

      - `type: Literal["explicit_url"]`

      - `url: str`

        JWKS endpoint.

        minLength: 1

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

    - `class JWKSInline`

      JWKS supplied directly; no network fetch.

      - `type: Literal["inline"]`

      - `keys: List[Dict[str, object]]`

        Inline JWK objects.

        minItems: 1

  - `jwks_polling_disabled_at: Optional[datetime]`

    If set, Anthropic's JWKS poller has paused polling for this issuer after repeated fetch failures. Re-enable by sending `jwks_polling_disabled: false` via the issuer update endpoint (POST) once the upstream JWKS endpoint is fixed. An OAuth caller cannot send this when the issuer backs a rule with any scope other than `workspace:developer` or `workspace:inference`; use a Console session.

    format: date-time

  - `max_jwt_lifetime_seconds: int`

    Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  - `name: str`

    Admin-chosen slug identifier.

  - `poll_status: Optional[FederationIssuerPollStatus]`

    Live state of Anthropic's JWKS polling for this issuer. Populated on both single-issuer retrieval and list responses, including archived issuers. Typically null for inline-key issuers (no polling), or when poll status is temporarily unavailable or polling has not started yet.

    - `consecutive_failures: int`

      Consecutive fetch failures since the last success.

    - `last_fetched_at: Optional[datetime]`

      When the last successful fetch completed.

      format: date-time

    - `next_poll_at: Optional[datetime]`

      When the next fetch is scheduled. Null if paused.

      format: date-time

  - `updated_at: datetime`

    When this issuer was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
federation_issuer = client.organization.federation.issuers.retrieve(
    "federation_issuer_id",
)
print(federation_issuer.id)
```

##### Response (200)

```json
{
  "id": "fdis_01SDCCSbTxrXDpWc1phhtcfK",
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "check_jti": true,
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "issuer_url": "https://token.actions.githubusercontent.com",
  "jwks": {
    "type": "discovery",
    "ca_cert_pem": "ca_cert_pem",
    "discovery_base": "discovery_base"
  },
  "jwks_polling_disabled_at": "2019-12-27T18:11:19.117Z",
  "max_jwt_lifetime_seconds": 0,
  "name": "github-actions",
  "poll_status": {
    "consecutive_failures": 0,
    "last_fetched_at": "2019-12-27T18:11:19.117Z",
    "next_poll_at": "2019-12-27T18:11:19.117Z"
  },
  "type": "federation_issuer",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id"
}
```

### Update Federation Issuer

`organization.federation.issuers.update(federation_issuer_id, **kwargs) -> FederationIssuer`

**POST** `/v1/organizations/federation_issuers/{federation_issuer_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Partially update a federation issuer.

Setting `jwks` replaces the full JWKS shape at once. Archived issuers
cannot be updated; this returns 400. Create a new issuer instead.

Updating an issuer that backs a rule with a scope outside
`workspace:developer` or `workspace:inference` requires a Console
session.

#### Parameters

- `federation_issuer_id: str` (path parameter)

  ID of the federation issuer to update.

- `check_jti: Optional[bool]`

  Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

- `issuer_url: Optional[str]`

  Replaces the `iss` claim value to match against. For discovery-mode issuers without a `discovery_base`, this is also the URL Anthropic fetches the OIDC discovery document and signing keys from, so changing it repoints the JWKS source. Changing the issuer URL to a well-known shared platform is rejected while any live rule under this issuer would not constrain tenant identity.

  minLength: 1

- `jwks: Optional[JWKS]`

  Replaces the entire JWKS configuration.

  - `class JWKSDiscovery`

    JWKS via the issuer's OIDC discovery document.

    - `type: Literal["discovery"]`

    - `ca_cert_pem: Optional[str]`

      Optional custom CA (PEM) for TLS verification of the JWKS fetch.

      maxLength: 8192

    - `discovery_base: Optional[str]`

      Set when the discovery URL differs from `issuer_url`.

  - `class JWKSExplicitURL`

    JWKS fetched from a fixed endpoint.

    - `type: Literal["explicit_url"]`

    - `url: str`

      JWKS endpoint.

      minLength: 1

    - `ca_cert_pem: Optional[str]`

      Optional custom CA (PEM) for TLS verification of the JWKS fetch.

      maxLength: 8192

  - `class JWKSInline`

    JWKS supplied directly; no network fetch.

    - `type: Literal["inline"]`

    - `keys: List[Dict[str, object]]`

      Inline JWK objects.

      minItems: 1

- `jwks_polling_disabled: Optional[bool]`

  Only `false` is accepted, to re-enable polling after the system pauses it. Polling is paused automatically; sending `true` is rejected.

- `max_jwt_lifetime_seconds: Optional[int]`

  Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  minimum: 1, maximum: 176400

- `name: Optional[str]`

  Replaces the slug identifier (lowercase, digits, hyphens). Unique within the organization; a duplicate name returns 409.

  minLength: 1, maxLength: 255

#### Returns

- `class FederationIssuer`

  Registered external OIDC identity provider.

  Records an external IdP the organization trusts for the RFC 7523
  jwt-bearer grant. The `issuer_url` must match the JWT `iss` claim exactly.

  - `type: Literal["federation_issuer"]`

    default: federation_issuer

  - `id: str`

    Tagged ID of the federation issuer.

  - `archived_at: Optional[datetime]`

    If set, all rules referencing this issuer reject token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this issuer.

  - `check_jti: bool`

    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

  - `created_at: datetime`

    When this issuer was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this issuer.

  - `issuer_url: str`

    The `iss` claim value. Incoming JWTs must match exactly.

  - `jwks: JWKS`

    How signing keys are obtained for signature verification.

    - `class JWKSDiscovery`

      JWKS via the issuer's OIDC discovery document.

      - `type: Literal["discovery"]`

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

      - `discovery_base: Optional[str]`

        Set when the discovery URL differs from `issuer_url`.

    - `class JWKSExplicitURL`

      JWKS fetched from a fixed endpoint.

      - `type: Literal["explicit_url"]`

      - `url: str`

        JWKS endpoint.

        minLength: 1

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

    - `class JWKSInline`

      JWKS supplied directly; no network fetch.

      - `type: Literal["inline"]`

      - `keys: List[Dict[str, object]]`

        Inline JWK objects.

        minItems: 1

  - `jwks_polling_disabled_at: Optional[datetime]`

    If set, Anthropic's JWKS poller has paused polling for this issuer after repeated fetch failures. Re-enable by sending `jwks_polling_disabled: false` via the issuer update endpoint (POST) once the upstream JWKS endpoint is fixed. An OAuth caller cannot send this when the issuer backs a rule with any scope other than `workspace:developer` or `workspace:inference`; use a Console session.

    format: date-time

  - `max_jwt_lifetime_seconds: int`

    Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  - `name: str`

    Admin-chosen slug identifier.

  - `poll_status: Optional[FederationIssuerPollStatus]`

    Live state of Anthropic's JWKS polling for this issuer. Populated on both single-issuer retrieval and list responses, including archived issuers. Typically null for inline-key issuers (no polling), or when poll status is temporarily unavailable or polling has not started yet.

    - `consecutive_failures: int`

      Consecutive fetch failures since the last success.

    - `last_fetched_at: Optional[datetime]`

      When the last successful fetch completed.

      format: date-time

    - `next_poll_at: Optional[datetime]`

      When the next fetch is scheduled. Null if paused.

      format: date-time

  - `updated_at: datetime`

    When this issuer was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
federation_issuer = client.organization.federation.issuers.update(
    federation_issuer_id="federation_issuer_id",
)
print(federation_issuer.id)
```

##### Response (200)

```json
{
  "id": "fdis_01SDCCSbTxrXDpWc1phhtcfK",
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "check_jti": true,
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "issuer_url": "https://token.actions.githubusercontent.com",
  "jwks": {
    "type": "discovery",
    "ca_cert_pem": "ca_cert_pem",
    "discovery_base": "discovery_base"
  },
  "jwks_polling_disabled_at": "2019-12-27T18:11:19.117Z",
  "max_jwt_lifetime_seconds": 0,
  "name": "github-actions",
  "poll_status": {
    "consecutive_failures": 0,
    "last_fetched_at": "2019-12-27T18:11:19.117Z",
    "next_poll_at": "2019-12-27T18:11:19.117Z"
  },
  "type": "federation_issuer",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id"
}
```

### Archive Federation Issuer

`organization.federation.issuers.archive(federation_issuer_id) -> FederationIssuer`

**POST** `/v1/organizations/federation_issuers/{federation_issuer_id}/archive`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Archive a federation issuer.

Idempotent; re-archiving returns the issuer with its original
`archived_at`. Rejected with 400 if any live (non-archived) federation
rule still references the issuer; archive those rules first (a rule's
issuer cannot be changed), or recreate them against another issuer.

#### Parameters

- `federation_issuer_id: str` (path parameter)

  ID of the federation issuer to archive.

#### Returns

- `class FederationIssuer`

  Registered external OIDC identity provider.

  Records an external IdP the organization trusts for the RFC 7523
  jwt-bearer grant. The `issuer_url` must match the JWT `iss` claim exactly.

  - `type: Literal["federation_issuer"]`

    default: federation_issuer

  - `id: str`

    Tagged ID of the federation issuer.

  - `archived_at: Optional[datetime]`

    If set, all rules referencing this issuer reject token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this issuer.

  - `check_jti: bool`

    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

  - `created_at: datetime`

    When this issuer was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this issuer.

  - `issuer_url: str`

    The `iss` claim value. Incoming JWTs must match exactly.

  - `jwks: JWKS`

    How signing keys are obtained for signature verification.

    - `class JWKSDiscovery`

      JWKS via the issuer's OIDC discovery document.

      - `type: Literal["discovery"]`

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

      - `discovery_base: Optional[str]`

        Set when the discovery URL differs from `issuer_url`.

    - `class JWKSExplicitURL`

      JWKS fetched from a fixed endpoint.

      - `type: Literal["explicit_url"]`

      - `url: str`

        JWKS endpoint.

        minLength: 1

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

    - `class JWKSInline`

      JWKS supplied directly; no network fetch.

      - `type: Literal["inline"]`

      - `keys: List[Dict[str, object]]`

        Inline JWK objects.

        minItems: 1

  - `jwks_polling_disabled_at: Optional[datetime]`

    If set, Anthropic's JWKS poller has paused polling for this issuer after repeated fetch failures. Re-enable by sending `jwks_polling_disabled: false` via the issuer update endpoint (POST) once the upstream JWKS endpoint is fixed. An OAuth caller cannot send this when the issuer backs a rule with any scope other than `workspace:developer` or `workspace:inference`; use a Console session.

    format: date-time

  - `max_jwt_lifetime_seconds: int`

    Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  - `name: str`

    Admin-chosen slug identifier.

  - `poll_status: Optional[FederationIssuerPollStatus]`

    Live state of Anthropic's JWKS polling for this issuer. Populated on both single-issuer retrieval and list responses, including archived issuers. Typically null for inline-key issuers (no polling), or when poll status is temporarily unavailable or polling has not started yet.

    - `consecutive_failures: int`

      Consecutive fetch failures since the last success.

    - `last_fetched_at: Optional[datetime]`

      When the last successful fetch completed.

      format: date-time

    - `next_poll_at: Optional[datetime]`

      When the next fetch is scheduled. Null if paused.

      format: date-time

  - `updated_at: datetime`

    When this issuer was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
federation_issuer = client.organization.federation.issuers.archive(
    "federation_issuer_id",
)
print(federation_issuer.id)
```

##### Response (200)

```json
{
  "id": "fdis_01SDCCSbTxrXDpWc1phhtcfK",
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "check_jti": true,
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "issuer_url": "https://token.actions.githubusercontent.com",
  "jwks": {
    "type": "discovery",
    "ca_cert_pem": "ca_cert_pem",
    "discovery_base": "discovery_base"
  },
  "jwks_polling_disabled_at": "2019-12-27T18:11:19.117Z",
  "max_jwt_lifetime_seconds": 0,
  "name": "github-actions",
  "poll_status": {
    "consecutive_failures": 0,
    "last_fetched_at": "2019-12-27T18:11:19.117Z",
    "next_poll_at": "2019-12-27T18:11:19.117Z"
  },
  "type": "federation_issuer",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id"
}
```

## Organization › Federation › Rules

### Create Federation Rule

`organization.federation.rules.create(**kwargs) -> FederationRule`

**POST** `/v1/organizations/federation_rules`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Create a federation rule owned by your organization.

The referenced issuer and the target service account must already exist
in the same organization; invalid references are rejected with a 400
error. The workspace reference is validated. Membership is not checked
at rule creation: token exchange resolves a single enabled workspace per
call and is rejected unless the target service account is a member of
that workspace (it is implicitly a member of the default workspace).
Rules on well-known shared issuers (GitHub Actions, GitLab, Buildkite,
Terraform Cloud, Google) must constrain tenant identity via an
identity-bearing claim, a tenant-pinning subject prefix (such as
`repo:YOUR_ORG/...`), or a CEL condition referencing one of those
identity claims (e.g. `claims.repository_owner`). OAuth callers may only
manage rules whose `oauth_scope` is `workspace:developer` or
`workspace:inference`; other scopes require a Console session.

#### Parameters

- `issuer_id: str`

  Tagged ID of the federation issuer.

- `match: FederationRuleMatchParam`

  Conditions the verified JWT must satisfy for this rule to apply. At least one of `subject_prefix` (other than a wildcard-only value like `*`), `claims`, or `condition` is required; `audience` alone is not sufficient.

  - `audience: Optional[str]`

    Exact match against the `aud` claim (any element if array). When omitted, the JWT's `aud` must still equal Anthropic's expected audience for the issuer; setting this field overrides that default.

    maxLength: 1024

  - `claims: Optional[Dict[str, str]]`

    Exact-match `{claim: value}` pairs against top-level claims. Only string-valued claims can be matched; use `condition` for non-string claims.

  - `condition: Optional[str]`

    CEL expression over claims for logic the structural fields can't express. Must evaluate to a boolean and may reference only the `claims` variable; a constant-true expression (such as `true`) is rejected with 400.

    maxLength: 4096

  - `subject_prefix: Optional[str]`

    Match the verified JWT `sub` claim. Exact match unless the value ends with `*`, in which case it is a prefix match. Example: `repo:my-org/my-repo:ref:refs/heads/main`.

    maxLength: 1024

- `name: str`

  Slug identifier (lowercase, digits, hyphens). Unique within the organization; a duplicate name returns 409.

  minLength: 1, maxLength: 255

- `oauth_scope: str`

  Space-separated OAuth scopes. OAuth callers may only set `workspace:developer` or `workspace:inference`; other scopes (such as `org:admin`) require a Console session.

  minLength: 1

- `target: ServiceAccountTargetParam`

  Identity that tokens minted via this rule act as. Currently always a `service_account` target.

  - `type: Literal["service_account"]`

  - `service_account_id: str`

    Tagged ID of the service account to mint tokens for.

  - `service_account_name: Optional[str]`

    Service account's display name at read time. Ignored on writes.

- `applies_to_all_workspaces: Optional[bool]`

  When true, enable this rule for every workspace in the org (including workspaces created later).

- `description: Optional[str]`

  Optional free-text description.

  maxLength: 2000

- `token_lifetime_seconds: Optional[int]`

  Lifetime in seconds for access tokens minted via this rule (60-86400). Defaults to 3600 (1h). Minted tokens are capped at `max(60, min(this value, 2 × remaining assertion validity))` seconds.

  minimum: 60, maximum: 86400

- `workspace_id: Optional[str]`

  Tagged ID of the workspace to enable this rule for. Required unless `applies_to_all_workspaces` is true. Additional workspaces can be added via the `/federation_rules/{federation_rule_id}/workspaces` sub-resource.

#### Returns

- `class FederationRule`

  Authorization rule binding an external OIDC identity to Anthropic.

  Evaluates the match conditions and mints an OAuth access token for the
  resolved target, scoped to a single workspace where the rule is enabled
  (chosen by the caller at exchange time when the rule is enabled for more
  than one). For rules enabled via `workspace_ids` or
  `applies_to_all_workspaces`, the target service account must be a member
  of that workspace (it is implicitly a member of the default workspace);
  rules carrying only the legacy `workspace_id` binding do not enforce
  this.

  - `type: Literal["federation_rule"]`

    default: federation_rule

  - `id: str`

    Tagged ID of the federation rule.

  - `applies_to_all_workspaces: bool`

    When true, this rule is enabled for every workspace in the org (including ones created after the rule). `workspace_ids` is ignored at exchange time.

  - `archived_at: Optional[datetime]`

    If set, this rule is archived and rejects token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this rule.

  - `created_at: datetime`

    When this rule was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this rule.

  - `description: Optional[str]`

    Optional free-text description.

  - `issuer_id: str`

    Tagged ID of the issuer whose tokens this rule accepts.

  - `issuer_name: Optional[str]`

    Issuer's display name at read time.

  - `match: FederationRuleMatch`

    Conditions the verified JWT must satisfy for this rule to apply. All populated matcher fields must pass.

    - `audience: Optional[str]`

      Exact match against the `aud` claim (any element if array). When omitted, the JWT's `aud` must still equal Anthropic's expected audience for the issuer; setting this field overrides that default.

      maxLength: 1024

    - `claims: Optional[Dict[str, str]]`

      Exact-match `{claim: value}` pairs against top-level claims. Only string-valued claims can be matched; use `condition` for non-string claims.

    - `condition: Optional[str]`

      CEL expression over claims for logic the structural fields can't express. Must evaluate to a boolean and may reference only the `claims` variable; a constant-true expression (such as `true`) is rejected with 400.

      maxLength: 4096

    - `subject_prefix: Optional[str]`

      Match the verified JWT `sub` claim. Exact match unless the value ends with `*`, in which case it is a prefix match. Example: `repo:my-org/my-repo:ref:refs/heads/main`.

      maxLength: 1024

  - `name: str`

    Admin-chosen slug identifier.

  - `oauth_scope: str`

    Space-separated OAuth scopes granted on the minted token.

  - `target: ServiceAccountTarget`

    What this rule targets. Check `type` before reading the other fields. Tokens minted via a rule whose target `type` is `service_account` act as that service account.

    - `type: Literal["service_account"]`

    - `service_account_id: str`

      Tagged ID of the service account to mint tokens for.

    - `service_account_name: Optional[str]`

      Service account's display name at read time. Ignored on writes.

  - `token_lifetime_seconds: int`

    Lifetime in seconds of access tokens minted via this rule. Minted tokens are capped at `max(60, min(this value, 2 × remaining assertion validity))` seconds.

  - `updated_at: datetime`

    When this rule was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this rule.

  - `workspace_ids: List[str]`

    Tagged IDs of the workspaces this rule is enabled for. May be empty for older rules that only carry the legacy `workspace_id` binding. Ignored at exchange time when `applies_to_all_workspaces` is true (the list may still be non-empty).

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
federation_rule = client.organization.federation.rules.create(
    issuer_id="issuer_id",
    match={},
    name="x",
    oauth_scope="x",
    target={
        "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
        "type": "service_account",
    },
)
print(federation_rule.id)
```

##### Response (200)

```json
{
  "id": "fdrl_01SDCCSbTxrXDpWc1phhtcfK",
  "applies_to_all_workspaces": true,
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "attributes": {
    "foo": "string"
  },
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "description": "description",
  "issuer_id": "issuer_id",
  "issuer_name": "issuer_name",
  "match": {
    "audience": "audience",
    "claims": {
      "foo": "string"
    },
    "condition": "condition",
    "subject_prefix": "subject_prefix"
  },
  "name": "prod-deploy-pipeline",
  "oauth_scope": "oauth_scope",
  "target": {
    "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
    "type": "service_account",
    "service_account_name": "service_account_name"
  },
  "token_lifetime_seconds": 0,
  "type": "federation_rule",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id",
  "workspace_id": "workspace_id",
  "workspace_ids": [
    "string"
  ]
}
```

### List Federation Rules

`organization.federation.rules.list(**kwargs) -> SyncPageCursor[FederationRule]`

**GET** `/v1/organizations/federation_rules`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

List federation rules in your organization.

Optionally filter by issuer with `issuer_id`. Archived rules are excluded
unless `include_archived=true`.

#### Parameters

- `include_archived: Optional[bool]` (query parameter)

  Include archived resources. Defaults to false.

  default: false

- `issuer_id: Optional[str]` (query parameter)

  Filter to rules referencing this federation issuer.

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `class FederationRule`

  Authorization rule binding an external OIDC identity to Anthropic.

  Evaluates the match conditions and mints an OAuth access token for the
  resolved target, scoped to a single workspace where the rule is enabled
  (chosen by the caller at exchange time when the rule is enabled for more
  than one). For rules enabled via `workspace_ids` or
  `applies_to_all_workspaces`, the target service account must be a member
  of that workspace (it is implicitly a member of the default workspace);
  rules carrying only the legacy `workspace_id` binding do not enforce
  this.

  - `type: Literal["federation_rule"]`

    default: federation_rule

  - `id: str`

    Tagged ID of the federation rule.

  - `applies_to_all_workspaces: bool`

    When true, this rule is enabled for every workspace in the org (including ones created after the rule). `workspace_ids` is ignored at exchange time.

  - `archived_at: Optional[datetime]`

    If set, this rule is archived and rejects token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this rule.

  - `created_at: datetime`

    When this rule was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this rule.

  - `description: Optional[str]`

    Optional free-text description.

  - `issuer_id: str`

    Tagged ID of the issuer whose tokens this rule accepts.

  - `issuer_name: Optional[str]`

    Issuer's display name at read time.

  - `match: FederationRuleMatch`

    Conditions the verified JWT must satisfy for this rule to apply. All populated matcher fields must pass.

    - `audience: Optional[str]`

      Exact match against the `aud` claim (any element if array). When omitted, the JWT's `aud` must still equal Anthropic's expected audience for the issuer; setting this field overrides that default.

      maxLength: 1024

    - `claims: Optional[Dict[str, str]]`

      Exact-match `{claim: value}` pairs against top-level claims. Only string-valued claims can be matched; use `condition` for non-string claims.

    - `condition: Optional[str]`

      CEL expression over claims for logic the structural fields can't express. Must evaluate to a boolean and may reference only the `claims` variable; a constant-true expression (such as `true`) is rejected with 400.

      maxLength: 4096

    - `subject_prefix: Optional[str]`

      Match the verified JWT `sub` claim. Exact match unless the value ends with `*`, in which case it is a prefix match. Example: `repo:my-org/my-repo:ref:refs/heads/main`.

      maxLength: 1024

  - `name: str`

    Admin-chosen slug identifier.

  - `oauth_scope: str`

    Space-separated OAuth scopes granted on the minted token.

  - `target: ServiceAccountTarget`

    What this rule targets. Check `type` before reading the other fields. Tokens minted via a rule whose target `type` is `service_account` act as that service account.

    - `type: Literal["service_account"]`

    - `service_account_id: str`

      Tagged ID of the service account to mint tokens for.

    - `service_account_name: Optional[str]`

      Service account's display name at read time. Ignored on writes.

  - `token_lifetime_seconds: int`

    Lifetime in seconds of access tokens minted via this rule. Minted tokens are capped at `max(60, min(this value, 2 × remaining assertion validity))` seconds.

  - `updated_at: datetime`

    When this rule was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this rule.

  - `workspace_ids: List[str]`

    Tagged IDs of the workspaces this rule is enabled for. May be empty for older rules that only carry the legacy `workspace_id` binding. Ignored at exchange time when `applies_to_all_workspaces` is true (the list may still be non-empty).

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.federation.rules.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "fdrl_01SDCCSbTxrXDpWc1phhtcfK",
      "applies_to_all_workspaces": true,
      "archived_at": "2019-12-27T18:11:19.117Z",
      "archived_by_actor_id": "archived_by_actor_id",
      "attributes": {
        "foo": "string"
      },
      "created_at": "2024-10-30T23:58:27.427722Z",
      "created_by_actor_id": "created_by_actor_id",
      "description": "description",
      "issuer_id": "issuer_id",
      "issuer_name": "issuer_name",
      "match": {
        "audience": "audience",
        "claims": {
          "foo": "string"
        },
        "condition": "condition",
        "subject_prefix": "subject_prefix"
      },
      "name": "prod-deploy-pipeline",
      "oauth_scope": "oauth_scope",
      "target": {
        "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
        "type": "service_account",
        "service_account_name": "service_account_name"
      },
      "token_lifetime_seconds": 0,
      "type": "federation_rule",
      "updated_at": "2024-10-30T23:58:27.427722Z",
      "updated_by_actor_id": "updated_by_actor_id",
      "workspace_id": "workspace_id",
      "workspace_ids": [
        "string"
      ]
    }
  ],
  "next_page": "next_page"
}
```

### Get Federation Rule

`organization.federation.rules.retrieve(federation_rule_id) -> FederationRule`

**GET** `/v1/organizations/federation_rules/{federation_rule_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Retrieve a federation rule by its ID (`fdrl_...`).

#### Parameters

- `federation_rule_id: str` (path parameter)

  ID of the federation rule.

#### Returns

- `class FederationRule`

  Authorization rule binding an external OIDC identity to Anthropic.

  Evaluates the match conditions and mints an OAuth access token for the
  resolved target, scoped to a single workspace where the rule is enabled
  (chosen by the caller at exchange time when the rule is enabled for more
  than one). For rules enabled via `workspace_ids` or
  `applies_to_all_workspaces`, the target service account must be a member
  of that workspace (it is implicitly a member of the default workspace);
  rules carrying only the legacy `workspace_id` binding do not enforce
  this.

  - `type: Literal["federation_rule"]`

    default: federation_rule

  - `id: str`

    Tagged ID of the federation rule.

  - `applies_to_all_workspaces: bool`

    When true, this rule is enabled for every workspace in the org (including ones created after the rule). `workspace_ids` is ignored at exchange time.

  - `archived_at: Optional[datetime]`

    If set, this rule is archived and rejects token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this rule.

  - `created_at: datetime`

    When this rule was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this rule.

  - `description: Optional[str]`

    Optional free-text description.

  - `issuer_id: str`

    Tagged ID of the issuer whose tokens this rule accepts.

  - `issuer_name: Optional[str]`

    Issuer's display name at read time.

  - `match: FederationRuleMatch`

    Conditions the verified JWT must satisfy for this rule to apply. All populated matcher fields must pass.

    - `audience: Optional[str]`

      Exact match against the `aud` claim (any element if array). When omitted, the JWT's `aud` must still equal Anthropic's expected audience for the issuer; setting this field overrides that default.

      maxLength: 1024

    - `claims: Optional[Dict[str, str]]`

      Exact-match `{claim: value}` pairs against top-level claims. Only string-valued claims can be matched; use `condition` for non-string claims.

    - `condition: Optional[str]`

      CEL expression over claims for logic the structural fields can't express. Must evaluate to a boolean and may reference only the `claims` variable; a constant-true expression (such as `true`) is rejected with 400.

      maxLength: 4096

    - `subject_prefix: Optional[str]`

      Match the verified JWT `sub` claim. Exact match unless the value ends with `*`, in which case it is a prefix match. Example: `repo:my-org/my-repo:ref:refs/heads/main`.

      maxLength: 1024

  - `name: str`

    Admin-chosen slug identifier.

  - `oauth_scope: str`

    Space-separated OAuth scopes granted on the minted token.

  - `target: ServiceAccountTarget`

    What this rule targets. Check `type` before reading the other fields. Tokens minted via a rule whose target `type` is `service_account` act as that service account.

    - `type: Literal["service_account"]`

    - `service_account_id: str`

      Tagged ID of the service account to mint tokens for.

    - `service_account_name: Optional[str]`

      Service account's display name at read time. Ignored on writes.

  - `token_lifetime_seconds: int`

    Lifetime in seconds of access tokens minted via this rule. Minted tokens are capped at `max(60, min(this value, 2 × remaining assertion validity))` seconds.

  - `updated_at: datetime`

    When this rule was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this rule.

  - `workspace_ids: List[str]`

    Tagged IDs of the workspaces this rule is enabled for. May be empty for older rules that only carry the legacy `workspace_id` binding. Ignored at exchange time when `applies_to_all_workspaces` is true (the list may still be non-empty).

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
federation_rule = client.organization.federation.rules.retrieve(
    "federation_rule_id",
)
print(federation_rule.id)
```

##### Response (200)

```json
{
  "id": "fdrl_01SDCCSbTxrXDpWc1phhtcfK",
  "applies_to_all_workspaces": true,
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "attributes": {
    "foo": "string"
  },
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "description": "description",
  "issuer_id": "issuer_id",
  "issuer_name": "issuer_name",
  "match": {
    "audience": "audience",
    "claims": {
      "foo": "string"
    },
    "condition": "condition",
    "subject_prefix": "subject_prefix"
  },
  "name": "prod-deploy-pipeline",
  "oauth_scope": "oauth_scope",
  "target": {
    "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
    "type": "service_account",
    "service_account_name": "service_account_name"
  },
  "token_lifetime_seconds": 0,
  "type": "federation_rule",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id",
  "workspace_id": "workspace_id",
  "workspace_ids": [
    "string"
  ]
}
```

### Update Federation Rule

`organization.federation.rules.update(federation_rule_id, **kwargs) -> FederationRule`

**POST** `/v1/organizations/federation_rules/{federation_rule_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Partially update a federation rule.

`issuer_id` is immutable. `match` and `target` are replaced as whole
objects when set. Referenced service accounts and workspaces must exist
in your organization; invalid references are rejected with a 400 error.
Archived rules cannot be updated; this returns 400. Create a new rule
instead. Rules on well-known shared issuers (GitHub Actions, GitLab,
Buildkite, Terraform Cloud, Google) must constrain tenant identity via
an identity-bearing claim, a tenant-pinning subject prefix (such as
`repo:YOUR_ORG/...`), or a CEL condition referencing one of those
identity claims (e.g. `claims.repository_owner`). On these issuers the
requirement is re-checked on every update; if an existing rule's stored
match does not yet constrain tenant identity, any update (even a rename
or description change) must also supply a conforming `match` in the same
request. OAuth callers may only manage rules whose `oauth_scope` is
`workspace:developer` or `workspace:inference`; other scopes require a
Console session.

#### Parameters

- `federation_rule_id: str` (path parameter)

  ID of the federation rule to update.

- `applies_to_all_workspaces: Optional[bool]`

  When true, enables this rule for every workspace in the org (including workspaces created later). Setting `false` is rejected with 400 if no workspace would remain enabled; a rule with only a legacy `workspace_id` binding continues to mint.

- `description: Optional[str]`

  Replaces the description. Omit to leave unchanged; send `null` to clear (the field is stored as an empty string).

  maxLength: 2000

- `match: Optional[FederationRuleMatchParam]`

  Replaces the entire match object. All populated matcher fields must pass.

  - `audience: Optional[str]`

    Exact match against the `aud` claim (any element if array). When omitted, the JWT's `aud` must still equal Anthropic's expected audience for the issuer; setting this field overrides that default.

    maxLength: 1024

  - `claims: Optional[Dict[str, str]]`

    Exact-match `{claim: value}` pairs against top-level claims. Only string-valued claims can be matched; use `condition` for non-string claims.

  - `condition: Optional[str]`

    CEL expression over claims for logic the structural fields can't express. Must evaluate to a boolean and may reference only the `claims` variable; a constant-true expression (such as `true`) is rejected with 400.

    maxLength: 4096

  - `subject_prefix: Optional[str]`

    Match the verified JWT `sub` claim. Exact match unless the value ends with `*`, in which case it is a prefix match. Example: `repo:my-org/my-repo:ref:refs/heads/main`.

    maxLength: 1024

- `name: Optional[str]`

  Replaces the slug identifier (lowercase, digits, hyphens). Unique within the organization; a duplicate name returns 409.

  minLength: 1, maxLength: 255

- `oauth_scope: Optional[str]`

  Replaces the space-separated OAuth scopes granted on minted tokens. OAuth callers may only set `workspace:developer` or `workspace:inference`; other scopes (such as `org:admin`) require a Console session.

  minLength: 1

- `target: Optional[ServiceAccountTargetParam]`

  Replaces the entire target object. Currently always a `service_account` target.

  - `type: Literal["service_account"]`

  - `service_account_id: str`

    Tagged ID of the service account to mint tokens for.

  - `service_account_name: Optional[str]`

    Service account's display name at read time. Ignored on writes.

- `token_lifetime_seconds: Optional[int]`

  Replaces the lifetime in seconds for access tokens minted via this rule (60-86400). Minted tokens are capped at `max(60, min(this value, 2 × remaining assertion validity))` seconds.

  minimum: 60, maximum: 86400

- `workspace_id: Optional[str]`

  Replaces the existing single workspace enablement (the previous one is removed). Rejected with 400 if the rule is enabled for more than one workspace; use the `/federation_rules/{federation_rule_id}/workspaces` sub-resource instead.

#### Returns

- `class FederationRule`

  Authorization rule binding an external OIDC identity to Anthropic.

  Evaluates the match conditions and mints an OAuth access token for the
  resolved target, scoped to a single workspace where the rule is enabled
  (chosen by the caller at exchange time when the rule is enabled for more
  than one). For rules enabled via `workspace_ids` or
  `applies_to_all_workspaces`, the target service account must be a member
  of that workspace (it is implicitly a member of the default workspace);
  rules carrying only the legacy `workspace_id` binding do not enforce
  this.

  - `type: Literal["federation_rule"]`

    default: federation_rule

  - `id: str`

    Tagged ID of the federation rule.

  - `applies_to_all_workspaces: bool`

    When true, this rule is enabled for every workspace in the org (including ones created after the rule). `workspace_ids` is ignored at exchange time.

  - `archived_at: Optional[datetime]`

    If set, this rule is archived and rejects token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this rule.

  - `created_at: datetime`

    When this rule was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this rule.

  - `description: Optional[str]`

    Optional free-text description.

  - `issuer_id: str`

    Tagged ID of the issuer whose tokens this rule accepts.

  - `issuer_name: Optional[str]`

    Issuer's display name at read time.

  - `match: FederationRuleMatch`

    Conditions the verified JWT must satisfy for this rule to apply. All populated matcher fields must pass.

    - `audience: Optional[str]`

      Exact match against the `aud` claim (any element if array). When omitted, the JWT's `aud` must still equal Anthropic's expected audience for the issuer; setting this field overrides that default.

      maxLength: 1024

    - `claims: Optional[Dict[str, str]]`

      Exact-match `{claim: value}` pairs against top-level claims. Only string-valued claims can be matched; use `condition` for non-string claims.

    - `condition: Optional[str]`

      CEL expression over claims for logic the structural fields can't express. Must evaluate to a boolean and may reference only the `claims` variable; a constant-true expression (such as `true`) is rejected with 400.

      maxLength: 4096

    - `subject_prefix: Optional[str]`

      Match the verified JWT `sub` claim. Exact match unless the value ends with `*`, in which case it is a prefix match. Example: `repo:my-org/my-repo:ref:refs/heads/main`.

      maxLength: 1024

  - `name: str`

    Admin-chosen slug identifier.

  - `oauth_scope: str`

    Space-separated OAuth scopes granted on the minted token.

  - `target: ServiceAccountTarget`

    What this rule targets. Check `type` before reading the other fields. Tokens minted via a rule whose target `type` is `service_account` act as that service account.

    - `type: Literal["service_account"]`

    - `service_account_id: str`

      Tagged ID of the service account to mint tokens for.

    - `service_account_name: Optional[str]`

      Service account's display name at read time. Ignored on writes.

  - `token_lifetime_seconds: int`

    Lifetime in seconds of access tokens minted via this rule. Minted tokens are capped at `max(60, min(this value, 2 × remaining assertion validity))` seconds.

  - `updated_at: datetime`

    When this rule was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this rule.

  - `workspace_ids: List[str]`

    Tagged IDs of the workspaces this rule is enabled for. May be empty for older rules that only carry the legacy `workspace_id` binding. Ignored at exchange time when `applies_to_all_workspaces` is true (the list may still be non-empty).

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
federation_rule = client.organization.federation.rules.update(
    federation_rule_id="federation_rule_id",
)
print(federation_rule.id)
```

##### Response (200)

```json
{
  "id": "fdrl_01SDCCSbTxrXDpWc1phhtcfK",
  "applies_to_all_workspaces": true,
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "attributes": {
    "foo": "string"
  },
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "description": "description",
  "issuer_id": "issuer_id",
  "issuer_name": "issuer_name",
  "match": {
    "audience": "audience",
    "claims": {
      "foo": "string"
    },
    "condition": "condition",
    "subject_prefix": "subject_prefix"
  },
  "name": "prod-deploy-pipeline",
  "oauth_scope": "oauth_scope",
  "target": {
    "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
    "type": "service_account",
    "service_account_name": "service_account_name"
  },
  "token_lifetime_seconds": 0,
  "type": "federation_rule",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id",
  "workspace_id": "workspace_id",
  "workspace_ids": [
    "string"
  ]
}
```

### Archive Federation Rule

`organization.federation.rules.archive(federation_rule_id) -> FederationRule`

**POST** `/v1/organizations/federation_rules/{federation_rule_id}/archive`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Archive a federation rule.

Token exchange through this rule stops immediately. Idempotent;
re-archiving returns the rule with its original `archived_at`. Archiving
clears the rule's workspace targeting (`workspace_id` and
`workspace_ids` are emptied). Tokens already minted before archive
remain valid until they expire. OAuth callers may only manage rules
whose `oauth_scope` is `workspace:developer` or `workspace:inference`;
other scopes require a Console session.

#### Parameters

- `federation_rule_id: str` (path parameter)

  ID of the federation rule to archive.

#### Returns

- `class FederationRule`

  Authorization rule binding an external OIDC identity to Anthropic.

  Evaluates the match conditions and mints an OAuth access token for the
  resolved target, scoped to a single workspace where the rule is enabled
  (chosen by the caller at exchange time when the rule is enabled for more
  than one). For rules enabled via `workspace_ids` or
  `applies_to_all_workspaces`, the target service account must be a member
  of that workspace (it is implicitly a member of the default workspace);
  rules carrying only the legacy `workspace_id` binding do not enforce
  this.

  - `type: Literal["federation_rule"]`

    default: federation_rule

  - `id: str`

    Tagged ID of the federation rule.

  - `applies_to_all_workspaces: bool`

    When true, this rule is enabled for every workspace in the org (including ones created after the rule). `workspace_ids` is ignored at exchange time.

  - `archived_at: Optional[datetime]`

    If set, this rule is archived and rejects token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this rule.

  - `created_at: datetime`

    When this rule was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this rule.

  - `description: Optional[str]`

    Optional free-text description.

  - `issuer_id: str`

    Tagged ID of the issuer whose tokens this rule accepts.

  - `issuer_name: Optional[str]`

    Issuer's display name at read time.

  - `match: FederationRuleMatch`

    Conditions the verified JWT must satisfy for this rule to apply. All populated matcher fields must pass.

    - `audience: Optional[str]`

      Exact match against the `aud` claim (any element if array). When omitted, the JWT's `aud` must still equal Anthropic's expected audience for the issuer; setting this field overrides that default.

      maxLength: 1024

    - `claims: Optional[Dict[str, str]]`

      Exact-match `{claim: value}` pairs against top-level claims. Only string-valued claims can be matched; use `condition` for non-string claims.

    - `condition: Optional[str]`

      CEL expression over claims for logic the structural fields can't express. Must evaluate to a boolean and may reference only the `claims` variable; a constant-true expression (such as `true`) is rejected with 400.

      maxLength: 4096

    - `subject_prefix: Optional[str]`

      Match the verified JWT `sub` claim. Exact match unless the value ends with `*`, in which case it is a prefix match. Example: `repo:my-org/my-repo:ref:refs/heads/main`.

      maxLength: 1024

  - `name: str`

    Admin-chosen slug identifier.

  - `oauth_scope: str`

    Space-separated OAuth scopes granted on the minted token.

  - `target: ServiceAccountTarget`

    What this rule targets. Check `type` before reading the other fields. Tokens minted via a rule whose target `type` is `service_account` act as that service account.

    - `type: Literal["service_account"]`

    - `service_account_id: str`

      Tagged ID of the service account to mint tokens for.

    - `service_account_name: Optional[str]`

      Service account's display name at read time. Ignored on writes.

  - `token_lifetime_seconds: int`

    Lifetime in seconds of access tokens minted via this rule. Minted tokens are capped at `max(60, min(this value, 2 × remaining assertion validity))` seconds.

  - `updated_at: datetime`

    When this rule was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this rule.

  - `workspace_ids: List[str]`

    Tagged IDs of the workspaces this rule is enabled for. May be empty for older rules that only carry the legacy `workspace_id` binding. Ignored at exchange time when `applies_to_all_workspaces` is true (the list may still be non-empty).

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
federation_rule = client.organization.federation.rules.archive(
    "federation_rule_id",
)
print(federation_rule.id)
```

##### Response (200)

```json
{
  "id": "fdrl_01SDCCSbTxrXDpWc1phhtcfK",
  "applies_to_all_workspaces": true,
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "attributes": {
    "foo": "string"
  },
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "description": "description",
  "issuer_id": "issuer_id",
  "issuer_name": "issuer_name",
  "match": {
    "audience": "audience",
    "claims": {
      "foo": "string"
    },
    "condition": "condition",
    "subject_prefix": "subject_prefix"
  },
  "name": "prod-deploy-pipeline",
  "oauth_scope": "oauth_scope",
  "target": {
    "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
    "type": "service_account",
    "service_account_name": "service_account_name"
  },
  "token_lifetime_seconds": 0,
  "type": "federation_rule",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id",
  "workspace_id": "workspace_id",
  "workspace_ids": [
    "string"
  ]
}
```

## Organization › Federation › Rules › Workspaces

### Add Federation Rule Workspace

`organization.federation.rules.workspaces.add(federation_rule_id, **kwargs) -> FederationRuleWorkspace`

**POST** `/v1/organizations/federation_rules/{federation_rule_id}/workspaces`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Enable a federation rule for a workspace.

Idempotent; re-enabling returns the existing enablement. The rule and
workspace must both belong to your organization. Membership of the
rule's target service account in this workspace is not checked at
enablement: token exchange into this workspace is rejected unless the
target is a member (it is implicitly a member of the default workspace).
Archived rules are rejected with 400. OAuth callers may only manage rules
whose `oauth_scope` is `workspace:developer` or `workspace:inference`;
other scopes require a Console session.

#### Parameters

- `federation_rule_id: str` (path parameter)

  ID of the federation rule.

- `workspace_id: str`

  Tagged ID of the workspace to enable this rule for.

#### Returns

- `class FederationRuleWorkspace`

  - `type: Literal["federation_rule_workspace"]`

    default: federation_rule_workspace

  - `created_at: datetime`

    When this workspace was enabled for the rule.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...` or `svac_...`) of the actor that enabled this workspace for the rule, if known.

  - `federation_rule_id: str`

    Tagged ID of the federation rule.

  - `workspace_id: str`

    Tagged ID of the workspace this rule is enabled for.

  - `workspace_name: Optional[str]`

    Workspace display name. Populated when listing; null in the enable response.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
federation_rule_workspace = client.organization.federation.rules.workspaces.add(
    federation_rule_id="federation_rule_id",
    workspace_id="workspace_id",
)
print(federation_rule_workspace.created_by_actor_id)
```

##### Response (200)

```json
{
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "federation_rule_id": "federation_rule_id",
  "type": "federation_rule_workspace",
  "workspace_id": "workspace_id",
  "workspace_name": "workspace_name"
}
```

### List Federation Rule Workspaces

`organization.federation.rules.workspaces.list(federation_rule_id, **kwargs) -> SyncPageCursor[FederationRuleWorkspace]`

**GET** `/v1/organizations/federation_rules/{federation_rule_id}/workspaces`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

List workspaces where this federation rule is enabled.

Returns all workspace enablements in a single response; the `limit` and
`page` parameters are accepted but have no effect, and `next_page` is
always `null`. Returns explicit per-workspace enablements only; for
rules with `applies_to_all_workspaces` or a legacy single
`workspace_id`, check those fields on the rule itself.

#### Parameters

- `federation_rule_id: str` (path parameter)

  ID of the federation rule.

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `class FederationRuleWorkspace`

  - `type: Literal["federation_rule_workspace"]`

    default: federation_rule_workspace

  - `created_at: datetime`

    When this workspace was enabled for the rule.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...` or `svac_...`) of the actor that enabled this workspace for the rule, if known.

  - `federation_rule_id: str`

    Tagged ID of the federation rule.

  - `workspace_id: str`

    Tagged ID of the workspace this rule is enabled for.

  - `workspace_name: Optional[str]`

    Workspace display name. Populated when listing; null in the enable response.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.federation.rules.workspaces.list(
    federation_rule_id="federation_rule_id",
)
page = page.data[0]
print(page.created_by_actor_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "created_at": "2024-10-30T23:58:27.427722Z",
      "created_by_actor_id": "created_by_actor_id",
      "federation_rule_id": "federation_rule_id",
      "type": "federation_rule_workspace",
      "workspace_id": "workspace_id",
      "workspace_name": "workspace_name"
    }
  ],
  "next_page": "next_page"
}
```

### Remove Federation Rule Workspace

`organization.federation.rules.workspaces.remove(workspace_id, **kwargs) -> WorkspaceRemoveResponse`

**DELETE** `/v1/organizations/federation_rules/{federation_rule_id}/workspaces/{workspace_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Disable a federation rule for a workspace.

Idempotent; succeeds even if the enablement was already removed. OAuth
callers may only manage rules whose `oauth_scope` is
`workspace:developer` or `workspace:inference`; other scopes require a
Console session.

#### Parameters

- `federation_rule_id: str` (path parameter)

  ID of the federation rule.

- `workspace_id: str` (path parameter)

  ID of the workspace to disable for.

#### Returns

- `class WorkspaceRemoveResponse`

  - `type: Literal["federation_rule_workspace_deleted"]`

    default: federation_rule_workspace_deleted

  - `federation_rule_id: str`

    Tagged ID of the federation rule.

  - `workspace_id: str`

    Tagged ID of the workspace named in the delete request. Removal is idempotent.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace = client.organization.federation.rules.workspaces.remove(
    workspace_id="workspace_id",
    federation_rule_id="federation_rule_id",
)
print(workspace.federation_rule_id)
```

##### Response (200)

```json
{
  "federation_rule_id": "federation_rule_id",
  "type": "federation_rule_workspace_deleted",
  "workspace_id": "workspace_id"
}
```

## Organization › Invites

### Create Invite

`organization.invites.create(**kwargs) -> OrganizationInvite`

**POST** `/v1/organizations/invites`

Invite a user to join the organization by email.

On plans that draw members from a finite pool of purchased seats, the invite automatically consumes a seat from the lowest tier with availability; there is no seat-tier parameter. When no seat is free the request fails with a 400 error rather than purchasing a seat.

#### Parameters

- `email: str`

  Email of the User.

  format: email

- `role: Literal["billing", "claude_code_user", "developer", 2 more]`

  Role for the invited User.

  The accepted values depend on the organization type. Console and API organizations accept `user`, `developer`, `billing`, and `claude_code_user`; `admin` cannot be assigned through the API. Claude Enterprise organizations accept `user` and `managed`; inviting with the `managed` role requires the `write:rbac_groups` scope in addition to `write:members`.

  - `"billing"`

  - `"claude_code_user"`

  - `"developer"`

  - `"managed"`

  - `"user"`

- `rbac_group_ids: Optional[Sequence[str]]`

  RBAC group IDs to assign to the User when the Invite is accepted. A non-empty array is accepted only for a Claude Enterprise organization with RBAC groups, and requires the key to carry the `write:rbac_groups` scope.

  maxItems: 100

#### Returns

- `class OrganizationInvite`

  - `type: Literal["invite"]`

    Object type.

    For Invites, this is always `"invite"`.

    default: invite

  - `id: str`

    ID of the Invite.

  - `accepted_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the Invite was accepted, or null.

    format: date-time

  - `email: str`

    Email of the User being invited.

  - `expires_at: datetime`

    RFC 3339 datetime string indicating when the Invite expires.

    format: date-time

  - `invited_at: datetime`

    RFC 3339 datetime string indicating when the Invite was created.

    format: date-time

  - `rbac_group_ids: List[str]`

    RBAC group IDs recorded on the Invite (Claude Enterprise organizations), to be assigned to the User when the Invite is accepted. `[]` when none.

  - `role: OrganizationRole`

    Organization role of the User.

    - `"admin"`

    - `"billing"`

    - `"claude_code_user"`

    - `"developer"`

    - `"managed"`

    - `"membership_admin"`

    - `"owner"`

    - `"primary_owner"`

    - `"user"`

  - `status: Literal["accepted", "deleted", "expired", "pending"]`

    Status of the Invite.

    - `"accepted"`

    - `"deleted"`

    - `"expired"`

    - `"pending"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
organization_invite = client.organization.invites.create(
    email="user@emaildomain.com",
    role="user",
)
print(organization_invite.id)
```

##### Response (200)

```json
{
  "id": "invite_015gWxCN9Hfg2QhZwTK7Mdeu",
  "accepted_at": "2019-12-27T18:11:19.117Z",
  "email": "user@emaildomain.com",
  "expires_at": "2024-11-20T23:58:27.427722Z",
  "invited_at": "2024-10-30T23:58:27.427722Z",
  "rbac_group_ids": [
    "string"
  ],
  "role": "admin",
  "status": "pending",
  "type": "invite"
}
```

### List Invites

`organization.invites.list(**kwargs) -> SyncPage[OrganizationInvite]`

**GET** `/v1/organizations/invites`

List the organization's invites.

#### Parameters

- `after_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `email: Optional[str]` (query parameter)

  Filter by the email address the Invite was sent to. Matches the same way as the Users list's `email` filter (normalized, case-insensitive).

  format: email

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `roles: Optional[Sequence[str]]` (query parameter)

  Filter to items whose `role` equals one of the supplied values. Repeatable; values are OR'ed together.

  Accepted values depend on the organization type: Console and API organizations accept `user`, `developer`, `billing`, `admin`, and `claude_code_user`; Claude Enterprise organizations accept `user`, `owner`, `primary_owner`, `membership_admin`, and `managed`.

- `statuses: Optional[List[Literal["accepted", "expired", "pending"]]]` (query parameter)

  Filter by Invite status. Repeatable; values are OR'ed together. Omit to return `pending`, `accepted`, and `expired` Invites alike.

  - `"accepted"`

  - `"expired"`

  - `"pending"`

#### Returns

- `class OrganizationInvite`

  - `type: Literal["invite"]`

    Object type.

    For Invites, this is always `"invite"`.

    default: invite

  - `id: str`

    ID of the Invite.

  - `accepted_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the Invite was accepted, or null.

    format: date-time

  - `email: str`

    Email of the User being invited.

  - `expires_at: datetime`

    RFC 3339 datetime string indicating when the Invite expires.

    format: date-time

  - `invited_at: datetime`

    RFC 3339 datetime string indicating when the Invite was created.

    format: date-time

  - `rbac_group_ids: List[str]`

    RBAC group IDs recorded on the Invite (Claude Enterprise organizations), to be assigned to the User when the Invite is accepted. `[]` when none.

  - `role: OrganizationRole`

    Organization role of the User.

    - `"admin"`

    - `"billing"`

    - `"claude_code_user"`

    - `"developer"`

    - `"managed"`

    - `"membership_admin"`

    - `"owner"`

    - `"primary_owner"`

    - `"user"`

  - `status: Literal["accepted", "deleted", "expired", "pending"]`

    Status of the Invite.

    - `"accepted"`

    - `"deleted"`

    - `"expired"`

    - `"pending"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.invites.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "invite_015gWxCN9Hfg2QhZwTK7Mdeu",
      "accepted_at": "2019-12-27T18:11:19.117Z",
      "email": "user@emaildomain.com",
      "expires_at": "2024-11-20T23:58:27.427722Z",
      "invited_at": "2024-10-30T23:58:27.427722Z",
      "rbac_group_ids": [
        "string"
      ],
      "role": "admin",
      "status": "pending",
      "type": "invite"
    }
  ],
  "first_id": "first_id",
  "has_more": true,
  "last_id": "last_id"
}
```

### Get Invite

`organization.invites.retrieve(invite_id) -> OrganizationInvite`

**GET** `/v1/organizations/invites/{invite_id}`

Retrieve an invite by ID.

#### Parameters

- `invite_id: str` (path parameter)

  ID of the Invite.

#### Returns

- `class OrganizationInvite`

  - `type: Literal["invite"]`

    Object type.

    For Invites, this is always `"invite"`.

    default: invite

  - `id: str`

    ID of the Invite.

  - `accepted_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the Invite was accepted, or null.

    format: date-time

  - `email: str`

    Email of the User being invited.

  - `expires_at: datetime`

    RFC 3339 datetime string indicating when the Invite expires.

    format: date-time

  - `invited_at: datetime`

    RFC 3339 datetime string indicating when the Invite was created.

    format: date-time

  - `rbac_group_ids: List[str]`

    RBAC group IDs recorded on the Invite (Claude Enterprise organizations), to be assigned to the User when the Invite is accepted. `[]` when none.

  - `role: OrganizationRole`

    Organization role of the User.

    - `"admin"`

    - `"billing"`

    - `"claude_code_user"`

    - `"developer"`

    - `"managed"`

    - `"membership_admin"`

    - `"owner"`

    - `"primary_owner"`

    - `"user"`

  - `status: Literal["accepted", "deleted", "expired", "pending"]`

    Status of the Invite.

    - `"accepted"`

    - `"deleted"`

    - `"expired"`

    - `"pending"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
organization_invite = client.organization.invites.retrieve(
    "invite_id",
)
print(organization_invite.id)
```

##### Response (200)

```json
{
  "id": "invite_015gWxCN9Hfg2QhZwTK7Mdeu",
  "accepted_at": "2019-12-27T18:11:19.117Z",
  "email": "user@emaildomain.com",
  "expires_at": "2024-11-20T23:58:27.427722Z",
  "invited_at": "2024-10-30T23:58:27.427722Z",
  "rbac_group_ids": [
    "string"
  ],
  "role": "admin",
  "status": "pending",
  "type": "invite"
}
```

### Delete Invite

`organization.invites.delete(invite_id) -> InviteDeleteResponse`

**DELETE** `/v1/organizations/invites/{invite_id}`

Delete a pending invite.

#### Parameters

- `invite_id: str` (path parameter)

  ID of the Invite.

#### Returns

- `class InviteDeleteResponse`

  - `type: Literal["invite_deleted"]`

    Deleted object type.

    For Invites, this is always `"invite_deleted"`.

    default: invite_deleted

  - `id: str`

    ID of the Invite.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
invite = client.organization.invites.delete(
    "invite_id",
)
print(invite.id)
```

##### Response (200)

```json
{
  "id": "invite_015gWxCN9Hfg2QhZwTK7Mdeu",
  "type": "invite_deleted"
}
```

## Organization › Service Accounts

### Create Service Account

`organization.service_accounts.create(**kwargs) -> ServiceAccount`

**POST** `/v1/organizations/service_accounts`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Create a service account.

A service account is a named workload identity that federation rules
target. `organization_role` is `developer` (default) or `admin`; a rule
may only be created or retargeted to grant `org:admin` scope when the
target's `organization_role` is `admin`. Creating an `admin`-role service
account requires an interactive credential (a user OAuth token or a
Console session) — a workload may only create `developer`-role service
accounts.

#### Parameters

- `name: str`

  Slug identifier (lowercase, digits, hyphens). Unique within the organization; a duplicate name returns 409.

  minLength: 1, maxLength: 255

- `description: Optional[str]`

  Optional free-text description.

  maxLength: 2000

- `organization_role: Optional[Literal["admin", "developer"]]`

  Org-level role. Defaults to `developer`.

  - `"admin"`

  - `"developer"`

#### Returns

- `class ServiceAccount`

  Named non-human identity within the caller's organization.

  A service account is a pure identity: name + org. Authorization lives on
  whatever references it (federation rules).

  - `type: Literal["service_account"]`

    default: service_account

  - `id: str`

    Tagged ID of the service account.

  - `archived_at: Optional[datetime]`

    If set, this service account is archived.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this service account.

  - `created_at: datetime`

    When this service account was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this service account.

  - `description: Optional[str]`

    Optional free-text description.

  - `name: str`

    Admin-chosen slug identifier.

  - `organization_role: Literal["admin", "developer"]`

    Org-level role. A federation rule may only be created or retargeted to grant `org:admin` scope when this is `admin`. A rule granting `org:admin` whose target is later demoted to `developer` is rejected at token exchange. Rules granting `org:admin` are managed in the Console.

    - `"admin"`

    - `"developer"`

  - `updated_at: datetime`

    When this service account was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this service account.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account = client.organization.service_accounts.create(
    name="ci-deploy-bot",
)
print(service_account.id)
```

##### Response (200)

```json
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
```

### List Service Accounts

`organization.service_accounts.list(**kwargs) -> SyncPageCursor[ServiceAccount]`

**GET** `/v1/organizations/service_accounts`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

List service accounts in the caller's organization.

Results are ordered by creation time, newest first. Use `limit` and the
`next_page` cursor to paginate; set `include_archived=true` to include
archived service accounts.

#### Parameters

- `include_archived: Optional[bool]` (query parameter)

  Include archived resources. Defaults to false.

  default: false

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `class ServiceAccount`

  Named non-human identity within the caller's organization.

  A service account is a pure identity: name + org. Authorization lives on
  whatever references it (federation rules).

  - `type: Literal["service_account"]`

    default: service_account

  - `id: str`

    Tagged ID of the service account.

  - `archived_at: Optional[datetime]`

    If set, this service account is archived.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this service account.

  - `created_at: datetime`

    When this service account was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this service account.

  - `description: Optional[str]`

    Optional free-text description.

  - `name: str`

    Admin-chosen slug identifier.

  - `organization_role: Literal["admin", "developer"]`

    Org-level role. A federation rule may only be created or retargeted to grant `org:admin` scope when this is `admin`. A rule granting `org:admin` whose target is later demoted to `developer` is rejected at token exchange. Rules granting `org:admin` are managed in the Console.

    - `"admin"`

    - `"developer"`

  - `updated_at: datetime`

    When this service account was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this service account.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.service_accounts.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

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

### Get Service Account

`organization.service_accounts.retrieve(service_account_id) -> ServiceAccount`

**GET** `/v1/organizations/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Retrieve a service account by its ID (`svac_...`).

#### Parameters

- `service_account_id: str` (path parameter)

  ID of the service account.

#### Returns

- `class ServiceAccount`

  Named non-human identity within the caller's organization.

  A service account is a pure identity: name + org. Authorization lives on
  whatever references it (federation rules).

  - `type: Literal["service_account"]`

    default: service_account

  - `id: str`

    Tagged ID of the service account.

  - `archived_at: Optional[datetime]`

    If set, this service account is archived.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this service account.

  - `created_at: datetime`

    When this service account was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this service account.

  - `description: Optional[str]`

    Optional free-text description.

  - `name: str`

    Admin-chosen slug identifier.

  - `organization_role: Literal["admin", "developer"]`

    Org-level role. A federation rule may only be created or retargeted to grant `org:admin` scope when this is `admin`. A rule granting `org:admin` whose target is later demoted to `developer` is rejected at token exchange. Rules granting `org:admin` are managed in the Console.

    - `"admin"`

    - `"developer"`

  - `updated_at: datetime`

    When this service account was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this service account.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account = client.organization.service_accounts.retrieve(
    "service_account_id",
)
print(service_account.id)
```

##### Response (200)

```json
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
```

### Update Service Account

`organization.service_accounts.update(service_account_id, **kwargs) -> ServiceAccount`

**POST** `/v1/organizations/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Update a service account.

Only `description` and `organization_role` are mutable; `name` cannot be
changed. Archived service accounts cannot be updated; this returns 400.
Setting `organization_role` to `admin` (even when unchanged) requires an
interactive credential (a user OAuth token or a Console session).

#### Parameters

- `service_account_id: str` (path parameter)

  ID of the service account to update.

- `description: Optional[str]`

  Replaces the description. Omit to leave unchanged; send `null` to clear (the field is stored as an empty string).

  maxLength: 2000

- `organization_role: Optional[Literal["admin", "developer"]]`

  Replaces the org-level role. Omit or send `null` to leave unchanged.

  - `"admin"`

  - `"developer"`

#### Returns

- `class ServiceAccount`

  Named non-human identity within the caller's organization.

  A service account is a pure identity: name + org. Authorization lives on
  whatever references it (federation rules).

  - `type: Literal["service_account"]`

    default: service_account

  - `id: str`

    Tagged ID of the service account.

  - `archived_at: Optional[datetime]`

    If set, this service account is archived.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this service account.

  - `created_at: datetime`

    When this service account was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this service account.

  - `description: Optional[str]`

    Optional free-text description.

  - `name: str`

    Admin-chosen slug identifier.

  - `organization_role: Literal["admin", "developer"]`

    Org-level role. A federation rule may only be created or retargeted to grant `org:admin` scope when this is `admin`. A rule granting `org:admin` whose target is later demoted to `developer` is rejected at token exchange. Rules granting `org:admin` are managed in the Console.

    - `"admin"`

    - `"developer"`

  - `updated_at: datetime`

    When this service account was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this service account.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account = client.organization.service_accounts.update(
    service_account_id="service_account_id",
)
print(service_account.id)
```

##### Response (200)

```json
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
```

### Archive Service Account

`organization.service_accounts.archive(service_account_id) -> ServiceAccount`

**POST** `/v1/organizations/service_accounts/{service_account_id}/archive`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Archive a service account.

Idempotent; re-archiving returns the service account with its original
`archived_at`. Rejected with 400 if any live (non-archived) federation
rule still targets this service account, same as issuer archival; archive
those rules first or change their target to another service account.

#### Parameters

- `service_account_id: str` (path parameter)

  ID of the service account to archive.

#### Returns

- `class ServiceAccount`

  Named non-human identity within the caller's organization.

  A service account is a pure identity: name + org. Authorization lives on
  whatever references it (federation rules).

  - `type: Literal["service_account"]`

    default: service_account

  - `id: str`

    Tagged ID of the service account.

  - `archived_at: Optional[datetime]`

    If set, this service account is archived.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this service account.

  - `created_at: datetime`

    When this service account was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this service account.

  - `description: Optional[str]`

    Optional free-text description.

  - `name: str`

    Admin-chosen slug identifier.

  - `organization_role: Literal["admin", "developer"]`

    Org-level role. A federation rule may only be created or retargeted to grant `org:admin` scope when this is `admin`. A rule granting `org:admin` whose target is later demoted to `developer` is rejected at token exchange. Rules granting `org:admin` are managed in the Console.

    - `"admin"`

    - `"developer"`

  - `updated_at: datetime`

    When this service account was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this service account.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account = client.organization.service_accounts.archive(
    "service_account_id",
)
print(service_account.id)
```

##### Response (200)

```json
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
```

## Organization › Service Accounts › Workspaces

### Add Workspace To Service Account

`organization.service_accounts.workspaces.add(service_account_id, **kwargs) -> ServiceAccountWorkspaceMember`

**POST** `/v1/organizations/service_accounts/{service_account_id}/workspaces`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Add a service account to a workspace with the given `workspace_role`.

Mirror of `POST /workspaces/{workspace_id}/service_accounts`, addressed
from the service-account side; both create the same membership. If the
service account is already an explicit member of the workspace, its
`workspace_role` is replaced with the value supplied here. Archived
workspaces return 400. Archived service accounts cannot be added and are
rejected.

#### Parameters

- `service_account_id: str` (path parameter)

  ID of the service account.

- `workspace_id: str`

  Tagged workspace ID to add the service account to.

- `workspace_role: NoBillingWorkspaceRole`

  Role to assign to the service account in this workspace.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `class ServiceAccountWorkspaceMember`

  - `type: Literal["service_account_workspace_member"]`

    default: service_account_workspace_member

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: Optional[bool]`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: str`

    Tagged service account ID (`svac_...`).

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: WorkspaceRole`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account_workspace_member = client.organization.service_accounts.workspaces.add(
    service_account_id="service_account_id",
    workspace_id="workspace_id",
    workspace_role="workspace_admin",
)
print(service_account_workspace_member.created_by_actor_id)
```

##### Response (200)

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

### List Workspaces For Service Account

`organization.service_accounts.workspaces.list(service_account_id, **kwargs) -> SyncPageCursor[ServiceAccountWorkspaceMember]`

**GET** `/v1/organizations/service_accounts/{service_account_id}/workspaces`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

List the workspaces a service account is a member of.

Each entry includes the service account's `workspace_role` in that
workspace. Use `limit` and the `next_page` cursor to paginate. When the
service account has no explicit default-workspace membership, the
implicit (`implicit: true`) membership is returned as the first entry on
the first page; with `limit=1` the first page may return up to 2 entries
(the implicit entry plus one explicit membership) so a pagination cursor
can be derived. Memberships are returned only while
the service account is active. Without a `page` cursor, an archived
service account returns an empty list. A `page` cursor that does not
match an active membership returns a 400 invalid-request error. A cursor
stops matching when the membership is removed, the workspace is deleted,
or the service account is archived. Restart pagination from the first
page to recover.

#### Parameters

- `service_account_id: str` (path parameter)

  ID of the service account.

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `class ServiceAccountWorkspaceMember`

  - `type: Literal["service_account_workspace_member"]`

    default: service_account_workspace_member

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: Optional[bool]`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: str`

    Tagged service account ID (`svac_...`).

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: WorkspaceRole`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.service_accounts.workspaces.list(
    service_account_id="service_account_id",
)
page = page.data[0]
print(page.created_by_actor_id)
```

##### Response (200)

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

### Remove Workspace From Service Account

`organization.service_accounts.workspaces.remove(workspace_id, **kwargs) -> WorkspaceRemoveResponse`

**DELETE** `/v1/organizations/service_accounts/{service_account_id}/workspaces/{workspace_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Remove a service account from a workspace.

Mirror of `DELETE /workspaces/{workspace_id}/service_accounts/{service_account_id}`,
addressed from the service-account side. Removal is idempotent (returns
200 even if the membership was already removed). A DELETE against the
implicit default-workspace membership returns 200 but is a no-op and the
membership persists; deleting an explicit default-workspace row reverts
to the implicit `workspace_user` membership. Archived workspaces return
400.

#### Parameters

- `service_account_id: str` (path parameter)

  ID of the service account.

- `workspace_id: str` (path parameter)

  ID of the workspace.

#### Returns

- `class WorkspaceRemoveResponse`

  - `type: Literal["service_account_workspace_member_deleted"]`

    default: service_account_workspace_member_deleted

  - `service_account_id: str`

    Tagged service account ID (`svac_...`) named in the delete request. Removal is idempotent; see the endpoint description for the implicit-membership no-op.

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`) named in the delete request.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace = client.organization.service_accounts.workspaces.remove(
    workspace_id="workspace_id",
    service_account_id="service_account_id",
)
print(workspace.service_account_id)
```

##### Response (200)

```json
{
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member_deleted",
  "workspace_id": "workspace_id"
}
```

## Organization › Users

### List Users

`organization.users.list(**kwargs) -> SyncPage[OrganizationUser]`

**GET** `/v1/organizations/users`

List the organization's members.

#### Parameters

- `after_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `email: Optional[str]` (query parameter)

  Filter by user email.

  format: email

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `roles: Optional[Sequence[str]]` (query parameter)

  Filter to items whose `role` equals one of the supplied values. Repeatable; values are OR'ed together.

  Accepted values depend on the organization type: Console and API organizations accept `user`, `developer`, `billing`, `admin`, and `claude_code_user`; Claude Enterprise organizations accept `user`, `owner`, `primary_owner`, `membership_admin`, and `managed`.

#### Returns

- `class OrganizationUser`

  - `type: Literal["user"]`

    Object type.

    For Users, this is always `"user"`.

    default: user

  - `id: str`

    ID of the User.

  - `added_at: datetime`

    RFC 3339 datetime string indicating when the User joined the Organization.

    format: date-time

  - `email: str`

    Email of the User.

  - `name: str`

    Name of the User.

  - `role: OrganizationRole`

    Organization role of the User.

    - `"admin"`

    - `"billing"`

    - `"claude_code_user"`

    - `"developer"`

    - `"managed"`

    - `"membership_admin"`

    - `"owner"`

    - `"primary_owner"`

    - `"user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.users.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
      "added_at": "2024-10-30T23:58:27.427722Z",
      "email": "user@emaildomain.com",
      "name": "Jane Doe",
      "role": "admin",
      "type": "user"
    }
  ],
  "first_id": "first_id",
  "has_more": true,
  "last_id": "last_id"
}
```

### Get User

`organization.users.retrieve(user_id) -> OrganizationUser`

**GET** `/v1/organizations/users/{user_id}`

Retrieve a member of the organization by user ID.

#### Parameters

- `user_id: str` (path parameter)

  ID of the User.

#### Returns

- `class OrganizationUser`

  - `type: Literal["user"]`

    Object type.

    For Users, this is always `"user"`.

    default: user

  - `id: str`

    ID of the User.

  - `added_at: datetime`

    RFC 3339 datetime string indicating when the User joined the Organization.

    format: date-time

  - `email: str`

    Email of the User.

  - `name: str`

    Name of the User.

  - `role: OrganizationRole`

    Organization role of the User.

    - `"admin"`

    - `"billing"`

    - `"claude_code_user"`

    - `"developer"`

    - `"managed"`

    - `"membership_admin"`

    - `"owner"`

    - `"primary_owner"`

    - `"user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
organization_user = client.organization.users.retrieve(
    "user_id",
)
print(organization_user.id)
```

##### Response (200)

```json
{
  "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "added_at": "2024-10-30T23:58:27.427722Z",
  "email": "user@emaildomain.com",
  "name": "Jane Doe",
  "role": "admin",
  "type": "user"
}
```

### Update User

`organization.users.update(user_id, **kwargs) -> OrganizationUser`

**POST** `/v1/organizations/users/{user_id}`

Update a member's organization role.

#### Parameters

- `user_id: str` (path parameter)

  ID of the User.

- `role: Literal["billing", "claude_code_user", "developer", 2 more]`

  New role for the User.

  The accepted values depend on the organization type. Console and API organizations accept `user`, `developer`, `billing`, and `claude_code_user`; `admin` cannot be assigned through the API. Claude Enterprise organizations accept `user` and `managed`; changing a User's role to `managed` requires the `write:rbac_groups` scope in addition to `write:members`.

  - `"billing"`

  - `"claude_code_user"`

  - `"developer"`

  - `"managed"`

  - `"user"`

#### Returns

- `class OrganizationUser`

  - `type: Literal["user"]`

    Object type.

    For Users, this is always `"user"`.

    default: user

  - `id: str`

    ID of the User.

  - `added_at: datetime`

    RFC 3339 datetime string indicating when the User joined the Organization.

    format: date-time

  - `email: str`

    Email of the User.

  - `name: str`

    Name of the User.

  - `role: OrganizationRole`

    Organization role of the User.

    - `"admin"`

    - `"billing"`

    - `"claude_code_user"`

    - `"developer"`

    - `"managed"`

    - `"membership_admin"`

    - `"owner"`

    - `"primary_owner"`

    - `"user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
organization_user = client.organization.users.update(
    user_id="user_id",
    role="user",
)
print(organization_user.id)
```

##### Response (200)

```json
{
  "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "added_at": "2024-10-30T23:58:27.427722Z",
  "email": "user@emaildomain.com",
  "name": "Jane Doe",
  "role": "admin",
  "type": "user"
}
```

### Remove User

`organization.users.remove(user_id) -> UserRemoveResponse`

**DELETE** `/v1/organizations/users/{user_id}`

Remove a member from the organization.

#### Parameters

- `user_id: str` (path parameter)

  ID of the User.

#### Returns

- `class UserRemoveResponse`

  - `type: Literal["user_deleted"]`

    Deleted object type.

    For Users, this is always `"user_deleted"`.

    default: user_deleted

  - `id: str`

    ID of the User.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
user = client.organization.users.remove(
    "user_id",
)
print(user.id)
```

##### Response (200)

```json
{
  "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "type": "user_deleted"
}
```

## Organization › Workspaces

### List Workspaces

`organization.workspaces.list(**kwargs) -> SyncPage[Workspace]`

**GET** `/v1/organizations/workspaces`

List Workspaces

#### Parameters

- `after_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `ids: Optional[Sequence[str]]` (query parameter)

  Only the Workspaces with these IDs, at most 100. `include_archived` and `include_default` still apply, and IDs of Workspaces the caller can't list are left out.

- `include_archived: Optional[bool]` (query parameter)

  Whether to include Workspaces that have been archived in the response

  default: false

- `include_default: Optional[bool]` (query parameter)

  Whether to include the organization's default Workspace in the response

  default: false

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

#### Returns

- `class Workspace`

  - `type: Literal["workspace"]`

    Object type.

    For Workspaces, this is always `"workspace"`.

    default: workspace

  - `id: str`

    ID of the Workspace.

  - `archived_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

    format: date-time

  - `compartment_id: str`

    Identifier for this Workspace's encryption compartment. When you configure an
    AWS KMS customer-managed encryption key (CMEK) that isn't bound to a user
    profile, reference this value in your KMS key-policy condition so the key is
    scoped to this compartment. On GCP and Azure, Anthropic enforces the compartment
    binding automatically; you do not need to reference this value in your key
    configuration. See the CMEK integration guide for the required key
    configuration; unless your organization is on Claude Platform on AWS, it
    includes a separate value used during key validation. On Claude Platform on AWS
    there is no separate validation value: your organization's own key is validated
    against this Workspace's own value when it is attached, so if its key policy
    uses the compartment condition, add this value to it before attaching the key.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the Workspace was created.

    format: date-time

  - `data_residency: DataResidency`

    Data residency configuration.

    - `allowed_inference_geos: Union[List[AllowedInferenceGeo], Literal["unrestricted"]]`

      Permitted inference geo values. 'unrestricted' means all geos are allowed.

      - `List[AllowedInferenceGeo]`

        - `"global"`

        - `"us"`

      - `"unrestricted"`

    - `default_inference_geo: Literal["global", "us"]`

      Default inference geo applied when requests omit the parameter.

      - `"global"`

      - `"us"`

    - `workspace_geo: Literal["us"]`

      Geographic region for workspace data storage. Immutable after creation.

  - `display_color: str`

    Hex color code representing the Workspace in the Anthropic Console.

  - `external_key_id: Optional[str]`

    ID of the customer-managed encryption key (CMEK) configuration to use for this
    Workspace. Setting this field requires CMEK to be enabled for your
    organization. When set, data stored for this Workspace is encrypted with the
    referenced key. Create key configurations with the External Keys API. On
    Claude Platform on AWS the value for an AWS KMS key is the key's ARN, and your
    organization's own key must be a single-Region key in the same AWS account and
    Region as the Workspace. On that platform the key is validated against this
    Workspace when it is attached, so a key-policy problem is reported as an error
    on this request. This field is write-once: once a key is attached to a Workspace
    it cannot be detached or replaced. To rotate key material, rotate the underlying
    key on your cloud KMS; the `external_key_id` stays the same.

  - `name: str`

    Name of the Workspace.

  - `tags: Dict[str, str]`

    User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

  - `user_profile_id: Optional[str]`

    ID of the user profile attached to the Workspace, or null if it has none. Every inference request through a Workspace that has a user profile must name that profile.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.workspaces.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      "archived_at": "2024-11-01T23:59:27.427722Z",
      "compartment_id": "f8a7b6c5-4d3e-4f1a-8b9c-0d1e2f3a4b5c",
      "created_at": "2024-10-30T23:58:27.427722Z",
      "data_residency": {
        "allowed_inference_geos": "unrestricted",
        "default_inference_geo": "global",
        "workspace_geo": "us"
      },
      "display_color": "#6C5BB9",
      "external_key_id": "ekey_01SDCCSbTxrXDpWc1phhtcfK",
      "name": "Workspace Name",
      "tags": {
        "env": "prod",
        "team": "platform"
      },
      "type": "workspace",
      "user_profile_id": "uprof_01SDCCSbTxrXDpWc1phhtcfK"
    }
  ],
  "first_id": "first_id",
  "has_more": true,
  "last_id": "last_id"
}
```

### Create Workspace

`organization.workspaces.create(**kwargs) -> Workspace`

**POST** `/v1/organizations/workspaces`

Create Workspace

#### Parameters

- `name: str`

  Name of the Workspace.

  minLength: 1, maxLength: 255

- `data_residency: Optional[DataResidencyCreateConfigParam]`

  Data residency configuration for the workspace. If omitted, defaults to `workspace_geo: "us"`, `allowed_inference_geos: "unrestricted"`, and `default_inference_geo: "global"`.

  - `allowed_inference_geos: Optional[Union[List[AllowedInferenceGeo], Literal["unrestricted"], null]]`

    Permitted inference geo values. Defaults to 'unrestricted' if omitted, which allows all geos. Use the string 'unrestricted' to allow all geos, or a list of specific geos.

    - `List[AllowedInferenceGeo]`

      - `"global"`

      - `"us"`

    - `"unrestricted"`

  - `default_inference_geo: Optional[Literal["global", "us"]]`

    Default inference geo applied when requests omit the parameter. Defaults to 'global' if omitted. Must be a member of `allowed_inference_geos` unless `allowed_inference_geos` is `"unrestricted"`.

    - `"global"`

    - `"us"`

  - `workspace_geo: Optional[Literal["us"]]`

    Geographic region for workspace data storage. Immutable after creation. Defaults to 'us' if omitted.

- `display_color: Optional[str]`

  Hex color code representing the Workspace in the Anthropic Console.

  maxLength: 7, pattern: ^#[0-9A-Fa-f]{6}$

- `external_key_id: Optional[str]`

  ID of the customer-managed encryption key (CMEK) configuration to use for this
  Workspace. Setting this field requires CMEK to be enabled for your
  organization. When set, data stored for this Workspace is encrypted with the
  referenced key. Create key configurations with the External Keys API. On
  Claude Platform on AWS the value for an AWS KMS key is the key's ARN, and your
  organization's own key must be a single-Region key in the same AWS account and
  Region as the Workspace. On that platform the key is validated against this
  Workspace when it is attached, so a key-policy problem is reported as an error
  on this request. This field is write-once: once a key is attached to a Workspace
  it cannot be detached or replaced. To rotate key material, rotate the underlying
  key on your cloud KMS; the `external_key_id` stays the same.

- `tags: Optional[Dict[str, str]]`

  User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

- `user_profile_id: Optional[str]`

  ID of a user profile to attach to the Workspace. Every inference request through the Workspace must then name this user profile; the API rejects a request that names none or a different one. The user profile can't be replaced or removed later; only deleting the user profile clears it.

#### Returns

- `class Workspace`

  - `type: Literal["workspace"]`

    Object type.

    For Workspaces, this is always `"workspace"`.

    default: workspace

  - `id: str`

    ID of the Workspace.

  - `archived_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

    format: date-time

  - `compartment_id: str`

    Identifier for this Workspace's encryption compartment. When you configure an
    AWS KMS customer-managed encryption key (CMEK) that isn't bound to a user
    profile, reference this value in your KMS key-policy condition so the key is
    scoped to this compartment. On GCP and Azure, Anthropic enforces the compartment
    binding automatically; you do not need to reference this value in your key
    configuration. See the CMEK integration guide for the required key
    configuration; unless your organization is on Claude Platform on AWS, it
    includes a separate value used during key validation. On Claude Platform on AWS
    there is no separate validation value: your organization's own key is validated
    against this Workspace's own value when it is attached, so if its key policy
    uses the compartment condition, add this value to it before attaching the key.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the Workspace was created.

    format: date-time

  - `data_residency: DataResidency`

    Data residency configuration.

    - `allowed_inference_geos: Union[List[AllowedInferenceGeo], Literal["unrestricted"]]`

      Permitted inference geo values. 'unrestricted' means all geos are allowed.

      - `List[AllowedInferenceGeo]`

        - `"global"`

        - `"us"`

      - `"unrestricted"`

    - `default_inference_geo: Literal["global", "us"]`

      Default inference geo applied when requests omit the parameter.

      - `"global"`

      - `"us"`

    - `workspace_geo: Literal["us"]`

      Geographic region for workspace data storage. Immutable after creation.

  - `display_color: str`

    Hex color code representing the Workspace in the Anthropic Console.

  - `external_key_id: Optional[str]`

    ID of the customer-managed encryption key (CMEK) configuration to use for this
    Workspace. Setting this field requires CMEK to be enabled for your
    organization. When set, data stored for this Workspace is encrypted with the
    referenced key. Create key configurations with the External Keys API. On
    Claude Platform on AWS the value for an AWS KMS key is the key's ARN, and your
    organization's own key must be a single-Region key in the same AWS account and
    Region as the Workspace. On that platform the key is validated against this
    Workspace when it is attached, so a key-policy problem is reported as an error
    on this request. This field is write-once: once a key is attached to a Workspace
    it cannot be detached or replaced. To rotate key material, rotate the underlying
    key on your cloud KMS; the `external_key_id` stays the same.

  - `name: str`

    Name of the Workspace.

  - `tags: Dict[str, str]`

    User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

  - `user_profile_id: Optional[str]`

    ID of the user profile attached to the Workspace, or null if it has none. Every inference request through a Workspace that has a user profile must name that profile.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace = client.organization.workspaces.create(
    name="x",
)
print(workspace.id)
```

##### Response (200)

```json
{
  "id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "archived_at": "2024-11-01T23:59:27.427722Z",
  "compartment_id": "f8a7b6c5-4d3e-4f1a-8b9c-0d1e2f3a4b5c",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "data_residency": {
    "allowed_inference_geos": "unrestricted",
    "default_inference_geo": "global",
    "workspace_geo": "us"
  },
  "display_color": "#6C5BB9",
  "external_key_id": "ekey_01SDCCSbTxrXDpWc1phhtcfK",
  "name": "Workspace Name",
  "tags": {
    "env": "prod",
    "team": "platform"
  },
  "type": "workspace",
  "user_profile_id": "uprof_01SDCCSbTxrXDpWc1phhtcfK"
}
```

### Get Workspace

`organization.workspaces.retrieve(workspace_id) -> Workspace`

**GET** `/v1/organizations/workspaces/{workspace_id}`

Get Workspace

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

#### Returns

- `class Workspace`

  - `type: Literal["workspace"]`

    Object type.

    For Workspaces, this is always `"workspace"`.

    default: workspace

  - `id: str`

    ID of the Workspace.

  - `archived_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

    format: date-time

  - `compartment_id: str`

    Identifier for this Workspace's encryption compartment. When you configure an
    AWS KMS customer-managed encryption key (CMEK) that isn't bound to a user
    profile, reference this value in your KMS key-policy condition so the key is
    scoped to this compartment. On GCP and Azure, Anthropic enforces the compartment
    binding automatically; you do not need to reference this value in your key
    configuration. See the CMEK integration guide for the required key
    configuration; unless your organization is on Claude Platform on AWS, it
    includes a separate value used during key validation. On Claude Platform on AWS
    there is no separate validation value: your organization's own key is validated
    against this Workspace's own value when it is attached, so if its key policy
    uses the compartment condition, add this value to it before attaching the key.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the Workspace was created.

    format: date-time

  - `data_residency: DataResidency`

    Data residency configuration.

    - `allowed_inference_geos: Union[List[AllowedInferenceGeo], Literal["unrestricted"]]`

      Permitted inference geo values. 'unrestricted' means all geos are allowed.

      - `List[AllowedInferenceGeo]`

        - `"global"`

        - `"us"`

      - `"unrestricted"`

    - `default_inference_geo: Literal["global", "us"]`

      Default inference geo applied when requests omit the parameter.

      - `"global"`

      - `"us"`

    - `workspace_geo: Literal["us"]`

      Geographic region for workspace data storage. Immutable after creation.

  - `display_color: str`

    Hex color code representing the Workspace in the Anthropic Console.

  - `external_key_id: Optional[str]`

    ID of the customer-managed encryption key (CMEK) configuration to use for this
    Workspace. Setting this field requires CMEK to be enabled for your
    organization. When set, data stored for this Workspace is encrypted with the
    referenced key. Create key configurations with the External Keys API. On
    Claude Platform on AWS the value for an AWS KMS key is the key's ARN, and your
    organization's own key must be a single-Region key in the same AWS account and
    Region as the Workspace. On that platform the key is validated against this
    Workspace when it is attached, so a key-policy problem is reported as an error
    on this request. This field is write-once: once a key is attached to a Workspace
    it cannot be detached or replaced. To rotate key material, rotate the underlying
    key on your cloud KMS; the `external_key_id` stays the same.

  - `name: str`

    Name of the Workspace.

  - `tags: Dict[str, str]`

    User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

  - `user_profile_id: Optional[str]`

    ID of the user profile attached to the Workspace, or null if it has none. Every inference request through a Workspace that has a user profile must name that profile.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace = client.organization.workspaces.retrieve(
    "workspace_id",
)
print(workspace.id)
```

##### Response (200)

```json
{
  "id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "archived_at": "2024-11-01T23:59:27.427722Z",
  "compartment_id": "f8a7b6c5-4d3e-4f1a-8b9c-0d1e2f3a4b5c",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "data_residency": {
    "allowed_inference_geos": "unrestricted",
    "default_inference_geo": "global",
    "workspace_geo": "us"
  },
  "display_color": "#6C5BB9",
  "external_key_id": "ekey_01SDCCSbTxrXDpWc1phhtcfK",
  "name": "Workspace Name",
  "tags": {
    "env": "prod",
    "team": "platform"
  },
  "type": "workspace",
  "user_profile_id": "uprof_01SDCCSbTxrXDpWc1phhtcfK"
}
```

### Update Workspace

`organization.workspaces.update(workspace_id, **kwargs) -> Workspace`

**POST** `/v1/organizations/workspaces/{workspace_id}`

Update Workspace

#### Parameters

- `workspace_id: str` (path parameter)

- `data_residency: Optional[DataResidencyUpdateConfigParam]`

  Data residency configuration for the workspace.

  - `allowed_inference_geos: Optional[Union[List[AllowedInferenceGeo], Literal["unrestricted"], null]]`

    Permitted inference geo values. Use 'unrestricted' to allow all geos, or a list of specific geos.

    - `List[AllowedInferenceGeo]`

      - `"global"`

      - `"us"`

    - `"unrestricted"`

  - `default_inference_geo: Optional[Literal["global", "us"]]`

    Default inference geo applied when requests omit the parameter. Must be a member of `allowed_inference_geos` unless `allowed_inference_geos` is `"unrestricted"`.

    - `"global"`

    - `"us"`

- `display_color: Optional[str]`

  Hex color code representing the Workspace in the Anthropic Console.

  maxLength: 7, pattern: ^#[0-9A-Fa-f]{6}$

- `external_key_id: Optional[str]`

  ID of the customer-managed encryption key (CMEK) configuration to use for this
  Workspace. Setting this field requires CMEK to be enabled for your
  organization. When set, data stored for this Workspace is encrypted with the
  referenced key. Create key configurations with the External Keys API. On
  Claude Platform on AWS the value for an AWS KMS key is the key's ARN, and your
  organization's own key must be a single-Region key in the same AWS account and
  Region as the Workspace. On that platform the key is validated against this
  Workspace when it is attached, so a key-policy problem is reported as an error
  on this request. This field is write-once: once a key is attached to a Workspace
  it cannot be detached or replaced. To rotate key material, rotate the underlying
  key on your cloud KMS; the `external_key_id` stays the same.

- `name: Optional[str]`

  Name of the Workspace.

  minLength: 1, maxLength: 255

- `tags: Optional[Dict[str, Optional[str]]]`

  User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

- `user_profile_id: Optional[str]`

  ID of a user profile to attach to the Workspace. Every inference request through the Workspace must then name this user profile; the API rejects a request that names none or a different one. Once set, it can't be replaced or removed (sending the same ID again changes nothing); only deleting the user profile clears it. The default Workspace can't have a user profile.

#### Returns

- `class Workspace`

  - `type: Literal["workspace"]`

    Object type.

    For Workspaces, this is always `"workspace"`.

    default: workspace

  - `id: str`

    ID of the Workspace.

  - `archived_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

    format: date-time

  - `compartment_id: str`

    Identifier for this Workspace's encryption compartment. When you configure an
    AWS KMS customer-managed encryption key (CMEK) that isn't bound to a user
    profile, reference this value in your KMS key-policy condition so the key is
    scoped to this compartment. On GCP and Azure, Anthropic enforces the compartment
    binding automatically; you do not need to reference this value in your key
    configuration. See the CMEK integration guide for the required key
    configuration; unless your organization is on Claude Platform on AWS, it
    includes a separate value used during key validation. On Claude Platform on AWS
    there is no separate validation value: your organization's own key is validated
    against this Workspace's own value when it is attached, so if its key policy
    uses the compartment condition, add this value to it before attaching the key.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the Workspace was created.

    format: date-time

  - `data_residency: DataResidency`

    Data residency configuration.

    - `allowed_inference_geos: Union[List[AllowedInferenceGeo], Literal["unrestricted"]]`

      Permitted inference geo values. 'unrestricted' means all geos are allowed.

      - `List[AllowedInferenceGeo]`

        - `"global"`

        - `"us"`

      - `"unrestricted"`

    - `default_inference_geo: Literal["global", "us"]`

      Default inference geo applied when requests omit the parameter.

      - `"global"`

      - `"us"`

    - `workspace_geo: Literal["us"]`

      Geographic region for workspace data storage. Immutable after creation.

  - `display_color: str`

    Hex color code representing the Workspace in the Anthropic Console.

  - `external_key_id: Optional[str]`

    ID of the customer-managed encryption key (CMEK) configuration to use for this
    Workspace. Setting this field requires CMEK to be enabled for your
    organization. When set, data stored for this Workspace is encrypted with the
    referenced key. Create key configurations with the External Keys API. On
    Claude Platform on AWS the value for an AWS KMS key is the key's ARN, and your
    organization's own key must be a single-Region key in the same AWS account and
    Region as the Workspace. On that platform the key is validated against this
    Workspace when it is attached, so a key-policy problem is reported as an error
    on this request. This field is write-once: once a key is attached to a Workspace
    it cannot be detached or replaced. To rotate key material, rotate the underlying
    key on your cloud KMS; the `external_key_id` stays the same.

  - `name: str`

    Name of the Workspace.

  - `tags: Dict[str, str]`

    User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

  - `user_profile_id: Optional[str]`

    ID of the user profile attached to the Workspace, or null if it has none. Every inference request through a Workspace that has a user profile must name that profile.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace = client.organization.workspaces.update(
    workspace_id="workspace_id",
)
print(workspace.id)
```

##### Response (200)

```json
{
  "id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "archived_at": "2024-11-01T23:59:27.427722Z",
  "compartment_id": "f8a7b6c5-4d3e-4f1a-8b9c-0d1e2f3a4b5c",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "data_residency": {
    "allowed_inference_geos": "unrestricted",
    "default_inference_geo": "global",
    "workspace_geo": "us"
  },
  "display_color": "#6C5BB9",
  "external_key_id": "ekey_01SDCCSbTxrXDpWc1phhtcfK",
  "name": "Workspace Name",
  "tags": {
    "env": "prod",
    "team": "platform"
  },
  "type": "workspace",
  "user_profile_id": "uprof_01SDCCSbTxrXDpWc1phhtcfK"
}
```

### Archive Workspace

`organization.workspaces.archive(workspace_id) -> Workspace`

**POST** `/v1/organizations/workspaces/{workspace_id}/archive`

Archive Workspace

#### Parameters

- `workspace_id: str` (path parameter)

#### Returns

- `class Workspace`

  - `type: Literal["workspace"]`

    Object type.

    For Workspaces, this is always `"workspace"`.

    default: workspace

  - `id: str`

    ID of the Workspace.

  - `archived_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

    format: date-time

  - `compartment_id: str`

    Identifier for this Workspace's encryption compartment. When you configure an
    AWS KMS customer-managed encryption key (CMEK) that isn't bound to a user
    profile, reference this value in your KMS key-policy condition so the key is
    scoped to this compartment. On GCP and Azure, Anthropic enforces the compartment
    binding automatically; you do not need to reference this value in your key
    configuration. See the CMEK integration guide for the required key
    configuration; unless your organization is on Claude Platform on AWS, it
    includes a separate value used during key validation. On Claude Platform on AWS
    there is no separate validation value: your organization's own key is validated
    against this Workspace's own value when it is attached, so if its key policy
    uses the compartment condition, add this value to it before attaching the key.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the Workspace was created.

    format: date-time

  - `data_residency: DataResidency`

    Data residency configuration.

    - `allowed_inference_geos: Union[List[AllowedInferenceGeo], Literal["unrestricted"]]`

      Permitted inference geo values. 'unrestricted' means all geos are allowed.

      - `List[AllowedInferenceGeo]`

        - `"global"`

        - `"us"`

      - `"unrestricted"`

    - `default_inference_geo: Literal["global", "us"]`

      Default inference geo applied when requests omit the parameter.

      - `"global"`

      - `"us"`

    - `workspace_geo: Literal["us"]`

      Geographic region for workspace data storage. Immutable after creation.

  - `display_color: str`

    Hex color code representing the Workspace in the Anthropic Console.

  - `external_key_id: Optional[str]`

    ID of the customer-managed encryption key (CMEK) configuration to use for this
    Workspace. Setting this field requires CMEK to be enabled for your
    organization. When set, data stored for this Workspace is encrypted with the
    referenced key. Create key configurations with the External Keys API. On
    Claude Platform on AWS the value for an AWS KMS key is the key's ARN, and your
    organization's own key must be a single-Region key in the same AWS account and
    Region as the Workspace. On that platform the key is validated against this
    Workspace when it is attached, so a key-policy problem is reported as an error
    on this request. This field is write-once: once a key is attached to a Workspace
    it cannot be detached or replaced. To rotate key material, rotate the underlying
    key on your cloud KMS; the `external_key_id` stays the same.

  - `name: str`

    Name of the Workspace.

  - `tags: Dict[str, str]`

    User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

  - `user_profile_id: Optional[str]`

    ID of the user profile attached to the Workspace, or null if it has none. Every inference request through a Workspace that has a user profile must name that profile.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace = client.organization.workspaces.archive(
    "workspace_id",
)
print(workspace.id)
```

##### Response (200)

```json
{
  "id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "archived_at": "2024-11-01T23:59:27.427722Z",
  "compartment_id": "f8a7b6c5-4d3e-4f1a-8b9c-0d1e2f3a4b5c",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "data_residency": {
    "allowed_inference_geos": "unrestricted",
    "default_inference_geo": "global",
    "workspace_geo": "us"
  },
  "display_color": "#6C5BB9",
  "external_key_id": "ekey_01SDCCSbTxrXDpWc1phhtcfK",
  "name": "Workspace Name",
  "tags": {
    "env": "prod",
    "team": "platform"
  },
  "type": "workspace",
  "user_profile_id": "uprof_01SDCCSbTxrXDpWc1phhtcfK"
}
```

## Organization › Workspaces › Rate Limits

### List Workspace Rate Limits

`organization.workspaces.rate_limits.list(workspace_id, **kwargs) -> SyncPageCursor[WorkspaceRateLimit]`

**GET** `/v1/organizations/workspaces/{workspace_id}/rate_limits`

List a workspace's rate limits.

By default, returns only the groups and limiter types that have a
workspace-level override. With `include_inherited=true`, returns every
group with organization-level limits the workspace can see, listing for
each the values it inherits from the organization as well as its own
overrides. Each value's `source` says which it is.

When `limit` is omitted, every matching entry is returned in a single
page; when `limit` truncates the result, follow `next_page` to fetch
the remaining entries.

#### Parameters

- `workspace_id: str` (path parameter)

  The ID of the workspace.

- `group_type: Optional[Literal["batch", "files", "model_group", 3 more]]` (query parameter)

  Filter by group type.

  - `"batch"`

  - `"files"`

  - `"model_group"`

  - `"skills"`

  - `"token_count"`

  - `"web_search"`

- `include_inherited: Optional[bool]` (query parameter)

  Also list the limiter values the workspace inherits from the organization, including groups with no workspace-level override.

  default: false

- `limit: Optional[int]` (query parameter)

  Maximum number of items to return per page. Ranges from `1` to `1000`.

  When omitted, every remaining entry is returned in a single page and `next_page` is `null`.

  minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `class WorkspaceRateLimit`

  - `type: Literal["workspace_rate_limit"]`

    Object type. Always `workspace_rate_limit` for workspace rate-limit entries.

    default: workspace_rate_limit

  - `group: Group`

    The rate-limit group this entry's limits apply to.

    - `class OrganizationRateLimitModelGroup`

      - `type: Literal["model_group"]`

        Always `model_group`: a family of models.

        default: model_group

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `display_name: str`

        Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

    - `class OrganizationRateLimitBatchGroup`

      - `type: Literal["batch"]`

        Always `batch`: the Message Batches API.

        default: batch

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitTokenCountGroup`

      - `type: Literal["token_count"]`

        Always `token_count`: the Token Count API.

        default: token_count

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitFilesGroup`

      - `type: Literal["files"]`

        Always `files`: the Files API.

        default: files

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitSkillsGroup`

      - `type: Literal["skills"]`

        Always `skills`: the Skills API.

        default: skills

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitWebSearchGroup`

      - `type: Literal["web_search"]`

        Always `web_search`: the Messages API web search tool.

        default: web_search

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

  - `limits: List[WorkspaceRateLimitValue]`

    The workspace's limiter values for this group. By default only the limiter types with a workspace-level override are listed. With `include_inherited` set to `true`, the limiter types the workspace inherits from the organization are listed too, each marked by `source`.

    - `type: str`

      The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

    - `org_limit: Optional[int]`

      The organization-level value for the same limiter type, for reference. `null` when the organization has no limit configured for this limiter type.

    - `source: Source`

      Where `value` comes from. `organization` values are listed only when `include_inherited` is `true`, and then `value` equals `org_limit`.

      - `class WorkspaceRateLimitWorkspaceSource`

        - `type: Literal["workspace"]`

          Always `workspace`: a workspace-level override is stored.

          default: workspace

      - `class WorkspaceRateLimitOrganizationSource`

        - `type: Literal["organization"]`

          Always `organization`: no workspace-level override is stored, so the organization's value applies.

          default: organization

    - `value: int`

      The workspace's value for this limiter type: the workspace-level override when `source.type` is `workspace`, otherwise the organization's value.

  - `models: Optional[List[str]]`

    Model names this entry's limits apply to, including aliases. `null` when `group.type` is not `"model_group"`. The list covers the models this workspace has access to, so it can differ between workspaces.

  - `rate_limit_id: str`

    The `id` of the organization's RateLimit entry this entry applies to.

  - `workspace_id: str`

    ID of the Workspace this entry applies to.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.workspaces.rate_limits.list(
    workspace_id="workspace_id",
)
page = page.data[0]
print(page.rate_limit_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "group": {
        "id": "id",
        "display_name": "display_name",
        "type": "model_group"
      },
      "limits": [
        {
          "org_limit": 0,
          "source": {
            "type": "workspace"
          },
          "type": "type",
          "value": 0
        }
      ],
      "models": [
        "string"
      ],
      "rate_limit_id": "rate_limit_id",
      "type": "workspace_rate_limit",
      "workspace_id": "workspace_id"
    }
  ],
  "next_page": "next_page"
}
```

### Set Workspace Rate Limits

`organization.workspaces.rate_limits.update(rate_limit_id, **kwargs) -> WorkspaceRateLimit`

**POST** `/v1/organizations/workspaces/{workspace_id}/rate_limits/{rate_limit_id}`

Set or clear rate-limit overrides for one rate-limit group in a workspace.

Only the limiter types named in `limits` change: an integer `value` sets
that type's override and `null` clears it. Types not named keep their
current value. A value above the organization's own limit is stored, but
the organization limit still applies, so the lower of the two is
enforced.

Returns the targeted group's entry with this request applied, in the shape
`GET /v1/organizations/workspaces/{workspace_id}/rate_limits` returns.
Changes take effect within about an hour.

#### Parameters

- `workspace_id: str` (path parameter)

  The ID of the workspace.

- `rate_limit_id: str` (path parameter)

  The `id` of the organization's rate-limit entry to set overrides for.

- `limits: Iterable[WorkspaceRateLimitUpdateValueParam]`

  Limits to set or clear. Unspecified limit types are unchanged.

  minItems: 1, maxItems: 16

  - `type: WorkspaceRateLimitType`

    Rate limiter type.

    - `"fast_itpmca"`

    - `"fast_otpm"`

    - `"input_tokens_per_minute"`

    - `"input_tokens_per_minute_cache_aware"`

    - `"output_tokens_per_minute"`

    - `"requests_per_minute"`

    - `"tokens_per_day"`

    - `"tokens_per_minute"`

    - `"tool_uses_per_second"`

  - `value: Optional[int]`

    New limit value. Set to null to clear the workspace override and fall back to the organization limit.

    minimum: 0, maximum: 9007199254740991

#### Returns

- `class WorkspaceRateLimit`

  - `type: Literal["workspace_rate_limit"]`

    Object type. Always `workspace_rate_limit` for workspace rate-limit entries.

    default: workspace_rate_limit

  - `group: Group`

    The rate-limit group this entry's limits apply to.

    - `class OrganizationRateLimitModelGroup`

      - `type: Literal["model_group"]`

        Always `model_group`: a family of models.

        default: model_group

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `display_name: str`

        Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

    - `class OrganizationRateLimitBatchGroup`

      - `type: Literal["batch"]`

        Always `batch`: the Message Batches API.

        default: batch

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitTokenCountGroup`

      - `type: Literal["token_count"]`

        Always `token_count`: the Token Count API.

        default: token_count

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitFilesGroup`

      - `type: Literal["files"]`

        Always `files`: the Files API.

        default: files

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitSkillsGroup`

      - `type: Literal["skills"]`

        Always `skills`: the Skills API.

        default: skills

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitWebSearchGroup`

      - `type: Literal["web_search"]`

        Always `web_search`: the Messages API web search tool.

        default: web_search

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

  - `limits: List[WorkspaceRateLimitValue]`

    The workspace's limiter values for this group. By default only the limiter types with a workspace-level override are listed. With `include_inherited` set to `true`, the limiter types the workspace inherits from the organization are listed too, each marked by `source`.

    - `type: str`

      The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

    - `org_limit: Optional[int]`

      The organization-level value for the same limiter type, for reference. `null` when the organization has no limit configured for this limiter type.

    - `source: Source`

      Where `value` comes from. `organization` values are listed only when `include_inherited` is `true`, and then `value` equals `org_limit`.

      - `class WorkspaceRateLimitWorkspaceSource`

        - `type: Literal["workspace"]`

          Always `workspace`: a workspace-level override is stored.

          default: workspace

      - `class WorkspaceRateLimitOrganizationSource`

        - `type: Literal["organization"]`

          Always `organization`: no workspace-level override is stored, so the organization's value applies.

          default: organization

    - `value: int`

      The workspace's value for this limiter type: the workspace-level override when `source.type` is `workspace`, otherwise the organization's value.

  - `models: Optional[List[str]]`

    Model names this entry's limits apply to, including aliases. `null` when `group.type` is not `"model_group"`. The list covers the models this workspace has access to, so it can differ between workspaces.

  - `rate_limit_id: str`

    The `id` of the organization's RateLimit entry this entry applies to.

  - `workspace_id: str`

    ID of the Workspace this entry applies to.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace_rate_limit = client.organization.workspaces.rate_limits.update(
    rate_limit_id="rate_limit_id",
    workspace_id="workspace_id",
    limits=[
        {
            "type": "fast_itpmca",
            "value": 0,
        }
    ],
)
print(workspace_rate_limit.rate_limit_id)
```

##### Response (200)

```json
{
  "group": {
    "id": "id",
    "display_name": "display_name",
    "type": "model_group"
  },
  "limits": [
    {
      "org_limit": 0,
      "source": {
        "type": "workspace"
      },
      "type": "type",
      "value": 0
    }
  ],
  "models": [
    "string"
  ],
  "rate_limit_id": "rate_limit_id",
  "type": "workspace_rate_limit",
  "workspace_id": "workspace_id"
}
```

## Organization › Workspaces › Members

### List Workspace Members

`organization.workspaces.members.list(workspace_id, **kwargs) -> SyncPage[WorkspaceMember]`

**GET** `/v1/organizations/workspaces/{workspace_id}/members`

List Workspace Members

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `after_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

#### Returns

- `class WorkspaceMember`

  - `type: Literal["workspace_member"]`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    default: workspace_member

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

  - `workspace_role: WorkspaceRole`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.workspaces.members.list(
    workspace_id="workspace_id",
)
page = page.data[0]
print(page.user_id)
```

##### Response (200)

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

### Create Workspace Member

`organization.workspaces.members.add(workspace_id, **kwargs) -> WorkspaceMember`

**POST** `/v1/organizations/workspaces/{workspace_id}/members`

Create Workspace Member

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `user_id: str`

  ID of the User.

- `workspace_role: NoBillingWorkspaceRole`

  Role of the new Workspace Member. Cannot be `workspace_billing`.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `class WorkspaceMember`

  - `type: Literal["workspace_member"]`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    default: workspace_member

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

  - `workspace_role: WorkspaceRole`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace_member = client.organization.workspaces.members.add(
    workspace_id="workspace_id",
    user_id="user_01WxYzAbCdEfGhJkMnPqRsTu",
    workspace_role="workspace_admin",
)
print(workspace_member.user_id)
```

##### Response (200)

```json
{
  "type": "workspace_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "workspace_role": "workspace_admin"
}
```

### Get Workspace Member

`organization.workspaces.members.retrieve(user_id, **kwargs) -> WorkspaceMember`

**GET** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Get Workspace Member

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `user_id: str` (path parameter)

  ID of the User.

#### Returns

- `class WorkspaceMember`

  - `type: Literal["workspace_member"]`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    default: workspace_member

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

  - `workspace_role: WorkspaceRole`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace_member = client.organization.workspaces.members.retrieve(
    user_id="user_id",
    workspace_id="workspace_id",
)
print(workspace_member.user_id)
```

##### Response (200)

```json
{
  "type": "workspace_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "workspace_role": "workspace_admin"
}
```

### Update Workspace Member

`organization.workspaces.members.update(user_id, **kwargs) -> WorkspaceMember`

**POST** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Update Workspace Member

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `user_id: str` (path parameter)

  ID of the User.

- `workspace_role: WorkspaceRole`

  New workspace role for the User.

  - `"workspace_admin"`

  - `"workspace_billing"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `class WorkspaceMember`

  - `type: Literal["workspace_member"]`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    default: workspace_member

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

  - `workspace_role: WorkspaceRole`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace_member = client.organization.workspaces.members.update(
    user_id="user_id",
    workspace_id="workspace_id",
    workspace_role="workspace_admin",
)
print(workspace_member.user_id)
```

##### Response (200)

```json
{
  "type": "workspace_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "workspace_role": "workspace_admin"
}
```

### Delete Workspace Member

`organization.workspaces.members.remove(user_id, **kwargs) -> MemberRemoveResponse`

**DELETE** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Delete Workspace Member

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `user_id: str` (path parameter)

  ID of the User.

#### Returns

- `class MemberRemoveResponse`

  - `type: Literal["workspace_member_deleted"]`

    Deleted object type.

    For Workspace Members, this is always `"workspace_member_deleted"`.

    default: workspace_member_deleted

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
member = client.organization.workspaces.members.remove(
    user_id="user_id",
    workspace_id="workspace_id",
)
print(member.user_id)
```

##### Response (200)

```json
{
  "type": "workspace_member_deleted",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
}
```

## Organization › Workspaces › Service Accounts

### List Service Account Workspace Members

`organization.workspaces.service_accounts.list(workspace_id, **kwargs) -> SyncPageCursor[ServiceAccountWorkspaceMember]`

**GET** `/v1/organizations/workspaces/{workspace_id}/service_accounts`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

List the service accounts that are members of a workspace.

Each entry includes the service account's `workspace_role`. Use `limit`
and the `next_page` cursor to paginate. Archived workspaces return 400;
use `GET /service_accounts/{id}/workspaces` to audit memberships of an
archived workspace. The implicit default-workspace membership is not
included in this list. Memberships of archived service accounts are
omitted from the results.

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the workspace.

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `class ServiceAccountWorkspaceMember`

  - `type: Literal["service_account_workspace_member"]`

    default: service_account_workspace_member

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: Optional[bool]`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: str`

    Tagged service account ID (`svac_...`).

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: WorkspaceRole`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.workspaces.service_accounts.list(
    workspace_id="workspace_id",
)
page = page.data[0]
print(page.created_by_actor_id)
```

##### Response (200)

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

### Create Service Account Workspace Member

`organization.workspaces.service_accounts.add(workspace_id, **kwargs) -> ServiceAccountWorkspaceMember`

**POST** `/v1/organizations/workspaces/{workspace_id}/service_accounts`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Add a service account to a workspace with the given `workspace_role`.

The role determines what the service account can do in the workspace and
which workspace-scoped permissions it can be granted when authenticating
through federation. Every service account is already an implicit
`workspace_user` member of the default workspace; adding it explicitly
assigns a chosen role. If the service account is already an explicit
member of the workspace, its `workspace_role` is replaced with the
value supplied here. Archived workspaces return 400. Archived service
accounts cannot be added and are rejected.

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the workspace.

- `service_account_id: str`

  Tagged service account ID to add.

- `workspace_role: NoBillingWorkspaceRole`

  Role to assign to the service account in this workspace.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `class ServiceAccountWorkspaceMember`

  - `type: Literal["service_account_workspace_member"]`

    default: service_account_workspace_member

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: Optional[bool]`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: str`

    Tagged service account ID (`svac_...`).

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: WorkspaceRole`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account_workspace_member = client.organization.workspaces.service_accounts.add(
    workspace_id="workspace_id",
    service_account_id="service_account_id",
    workspace_role="workspace_admin",
)
print(service_account_workspace_member.created_by_actor_id)
```

##### Response (200)

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

### Get Service Account Workspace Member

`organization.workspaces.service_accounts.retrieve(service_account_id, **kwargs) -> ServiceAccountWorkspaceMember`

**GET** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Retrieve a service account's membership in a workspace.

Returns the membership record, including the service account's
`workspace_role` in this workspace. Archived workspaces return 400. For
the default workspace, returns the implicit (`implicit: true`)
membership when no explicit membership exists; an explicitly added
membership is returned with its assigned role. An archived service
account returns 404.

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the workspace.

- `service_account_id: str` (path parameter)

  ID of the service account.

#### Returns

- `class ServiceAccountWorkspaceMember`

  - `type: Literal["service_account_workspace_member"]`

    default: service_account_workspace_member

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: Optional[bool]`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: str`

    Tagged service account ID (`svac_...`).

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: WorkspaceRole`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account_workspace_member = (
    client.organization.workspaces.service_accounts.retrieve(
        service_account_id="service_account_id",
        workspace_id="workspace_id",
    )
)
print(service_account_workspace_member.created_by_actor_id)
```

##### Response (200)

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

### Update Service Account Workspace Member

`organization.workspaces.service_accounts.update(service_account_id, **kwargs) -> ServiceAccountWorkspaceMember`

**POST** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Change a service account's role in a workspace.

The new `workspace_role` replaces the current one. Only explicit
memberships can be updated; to set a role on the implicit
default-workspace membership, add the service account explicitly with
`POST /workspaces/{workspace_id}/service_accounts`. Archived workspaces
return 400. Archived service accounts cannot be updated and are
rejected.

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the workspace.

- `service_account_id: str` (path parameter)

  ID of the service account.

- `workspace_role: NoBillingWorkspaceRole`

  New role for the service account in this workspace.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `class ServiceAccountWorkspaceMember`

  - `type: Literal["service_account_workspace_member"]`

    default: service_account_workspace_member

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: Optional[bool]`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: str`

    Tagged service account ID (`svac_...`).

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: WorkspaceRole`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account_workspace_member = (
    client.organization.workspaces.service_accounts.update(
        service_account_id="service_account_id",
        workspace_id="workspace_id",
        workspace_role="workspace_admin",
    )
)
print(service_account_workspace_member.created_by_actor_id)
```

##### Response (200)

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

### Delete Service Account Workspace Member

`organization.workspaces.service_accounts.remove(service_account_id, **kwargs) -> ServiceAccountRemoveResponse`

**DELETE** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Remove a service account from a workspace.

Removal is idempotent (returns 200 even if the membership was already
removed). A DELETE against the implicit default-workspace membership
returns 200 but is a no-op and the membership persists; deleting an
explicit default-workspace row reverts to the implicit `workspace_user`
membership. Archived workspaces return 400.

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the workspace.

- `service_account_id: str` (path parameter)

  ID of the service account.

#### Returns

- `class ServiceAccountRemoveResponse`

  - `type: Literal["service_account_workspace_member_deleted"]`

    default: service_account_workspace_member_deleted

  - `service_account_id: str`

    Tagged service account ID (`svac_...`) named in the delete request. Removal is idempotent; see the endpoint description for the implicit-membership no-op.

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`) named in the delete request.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account = client.organization.workspaces.service_accounts.remove(
    service_account_id="service_account_id",
    workspace_id="workspace_id",
)
print(service_account.service_account_id)
```

##### Response (200)

```json
{
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member_deleted",
  "workspace_id": "workspace_id"
}
```

## Organization › Rate Limits

### List Organization Rate Limits

`organization.rate_limits.list(**kwargs) -> SyncPageCursor[OrganizationRateLimit]`

**GET** `/v1/organizations/rate_limits`

List Messages API rate limits for your organization.

Each entry corresponds to one rate-limit group (either a model family
or an API-surface category such as the Message Batches API or the web
search tool) and contains the set of limiter values that apply to it.

When `limit` is omitted, every matching entry is returned in a single
page; when `limit` truncates the result, follow `next_page` to fetch
the remaining entries.

#### Parameters

- `group_type: Optional[Literal["batch", "files", "model_group", 3 more]]` (query parameter)

  Filter by group type.

  - `"batch"`

  - `"files"`

  - `"model_group"`

  - `"skills"`

  - `"token_count"`

  - `"web_search"`

- `limit: Optional[int]` (query parameter)

  Maximum number of items to return per page. Ranges from `1` to `1000`.

  When omitted, every remaining entry is returned in a single page and `next_page` is `null`.

  minimum: 1, maximum: 1000

- `model: Optional[str]` (query parameter)

  Filter to the single entry containing this model. Accepts full model names and aliases. Returns 404 if the model is not found or has no rate limits for this organization.

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `class OrganizationRateLimit`

  - `type: Literal["rate_limit"]`

    Object type. Always `rate_limit` for organization rate-limit entries.

    default: rate_limit

  - `id: str`

    Identifier of this rate-limit entry. It is stable within the organization and differs between organizations; the group's own identifier is `group.id`. Pass it as `rate_limit_id` to set a workspace's overrides for this group.

  - `group: Group`

    The rate-limit group this entry's limits apply to.

    - `class OrganizationRateLimitModelGroup`

      - `type: Literal["model_group"]`

        Always `model_group`: a family of models.

        default: model_group

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `display_name: str`

        Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

    - `class OrganizationRateLimitBatchGroup`

      - `type: Literal["batch"]`

        Always `batch`: the Message Batches API.

        default: batch

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitTokenCountGroup`

      - `type: Literal["token_count"]`

        Always `token_count`: the Token Count API.

        default: token_count

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitFilesGroup`

      - `type: Literal["files"]`

        Always `files`: the Files API.

        default: files

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitSkillsGroup`

      - `type: Literal["skills"]`

        Always `skills`: the Skills API.

        default: skills

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitWebSearchGroup`

      - `type: Literal["web_search"]`

        Always `web_search`: the Messages API web search tool.

        default: web_search

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

  - `limits: List[OrganizationRateLimitValue]`

    The limiter values that apply to this group.

    - `type: str`

      The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

    - `value: int`

      The configured limit value for this limiter type.

  - `models: Optional[List[str]]`

    Model names this entry's limits apply to, including aliases. `null` when `group.type` is not `"model_group"`. The list covers the models your organization has access to, so it can differ between organizations.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.rate_limits.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "id",
      "group": {
        "id": "id",
        "display_name": "display_name",
        "type": "model_group"
      },
      "limits": [
        {
          "type": "type",
          "value": 0
        }
      ],
      "models": [
        "string"
      ],
      "type": "rate_limit"
    }
  ],
  "next_page": "next_page"
}
```

## Organization › Compliance Settings

### Get Compliance Settings

`organization.compliance_settings.retrieve() -> OrganizationComplianceSettings`

**GET** `/v1/organizations/compliance_settings`

Retrieve your organization's Compliance Settings.

Compliance Settings is a singleton resource: there is exactly one per
organization, addressed without an identifier. The `state` field reflects
whether the Compliance API is enabled. An organization with a parent
organization reads the state inherited from the parent's configuration.

#### Returns

- `class OrganizationComplianceSettings`

  - `type: Literal["compliance_settings"]`

    default: compliance_settings

  - `state: ComplianceSettingsState`

    Whether the Compliance API is enabled for this organization.

    - `class ComplianceSettingsStateEnabled`

      - `type: Literal["enabled"]`

        default: enabled

    - `class ComplianceSettingsStateDisabled`

      - `type: Literal["disabled"]`

        default: disabled

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
organization_compliance_settings = client.organization.compliance_settings.retrieve()
print(organization_compliance_settings.state)
```

##### Response (200)

```json
{
  "state": {
    "type": "enabled"
  },
  "type": "compliance_settings"
}
```

### Update Compliance Settings

`organization.compliance_settings.update(**kwargs) -> OrganizationComplianceSettings`

**POST** `/v1/organizations/compliance_settings`

Update your organization's Compliance Settings.

Setting `state` to `enabled` turns on the Compliance API and begins
capturing organization activity events. Setting it to `disabled` turns
both off. Access Transparency events are an exception: they are still
captured while the Compliance API is disabled, and the Compliance API
activity feed returns them once it is enabled again. `state` reflects
whether the Compliance API is enabled.

A request that sets `state` to its current value succeeds and leaves the
resource unchanged. A `disabled` request stays in effect until a later
`enabled` request or the organization's next provisioning action that
enables Access Transparency: enabling Access Transparency also enables
the Compliance API, which serves its activity events, so such
provisioning (including re-runs) re-enables the Compliance API even
after a `disabled` request. Automated provisioning never disables
compliance settings.

#### Parameters

- `state: ComplianceSettingsStateParam`

  Desired state. Accepts the string shorthand "enabled" or "disabled" in place of the object form; the response always returns the canonical object form.

  - `class ComplianceSettingsStateEnabledParam`

    - `type: Literal["enabled"]`

  - `class ComplianceSettingsStateDisabledParam`

    - `type: Literal["disabled"]`

#### Returns

- `class OrganizationComplianceSettings`

  - `type: Literal["compliance_settings"]`

    default: compliance_settings

  - `state: ComplianceSettingsState`

    Whether the Compliance API is enabled for this organization.

    - `class ComplianceSettingsStateEnabled`

      - `type: Literal["enabled"]`

        default: enabled

    - `class ComplianceSettingsStateDisabled`

      - `type: Literal["disabled"]`

        default: disabled

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
organization_compliance_settings = client.organization.compliance_settings.update(
    state={"type": "enabled"},
)
print(organization_compliance_settings.state)
```

##### Response (200)

```json
{
  "state": {
    "type": "enabled"
  },
  "type": "compliance_settings"
}
```

## Organization › Analytics › Summaries

### Get Activity Summaries

`organization.analytics.summaries.list(**kwargs) -> SyncPageCursor[AnalyticsSingleDayActivitySummary]`

**GET** `/v1/organizations/analytics/summaries`

Get organization-wide activity summaries for a date range.

Returns one entry per day from `starting_date` (inclusive) to `ending_date`
(exclusive) in `data`, the same `data` / `next_page` envelope as the other
analytics list endpoints; the series is currently returned in full, so
`next_page` is always null.
Data is typically available with a 1-day lag and may be revised by a few
percent over the following days: when `ending_date` is omitted it
defaults to the most recent available day + 1, so the last entry covers
the most recent available day. The series can be scoped to an RBAC group
via `filter[]=rbac_group_id:{id}`. Available to organizations on a Claude
Enterprise plan. Requires an API key with the `read:analytics` scope.

#### Parameters

- `starting_date: Union[null, null]` (query parameter)

  UTC date in YYYY-MM-DD format. Start of the date range (inclusive). Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

- `ending_date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. End of the date range (exclusive). Data is typically available with a 1-day lag, so this can be at most today — which is also the default when omitted, making the last entry cover the most recent available day. Data may be revised by a few percent over the following days. The range may span at most 366 days.

  format: date

- `filter: Optional[Sequence[str]]` (query parameter)

  Filters as `dimension:value`. Only `rbac_group_id` is supported (e.g. `filter[]=rbac_group_id:{id}`); repeat the param to OR across groups. Scopes the whole day series to members of the matching group(s), re-aggregated from member-level activity — org-wide seat/invite fields and the adoption rates derived from them are null on scoped rows. `rbac_group_id` accepts the tagged id (`rbac_group_...`, as emitted in responses and by the spend-limits API) or a bare group UUID, and matches users who held the group at any point during each UTC day (time-of-usage attribution). At most 100 entries.

  maxItems: 100

- `limit: Optional[int]` (query parameter)

  Number of results per page (1-1000, default 100). The day series (at most 366 entries) is currently returned in full in a single page, so `limit` does not yet shorten it.

  minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field. `next_page` is currently always null, so there is never a cursor to send.

#### Returns

- `class AnalyticsSingleDayActivitySummary`

  Per-day entry in the /summaries response.

  - `assigned_seat_count: Optional[int]`

    Number of seats currently assigned to members. Null when the response is scoped to an RBAC group — seat assignment is org-wide and has no per-group analogue.

  - `cowork_daily_active_user_count: int`

    Number of users with Cowork activity on the requested day

  - `cowork_monthly_active_user_count: int`

    Number of users with Cowork activity in the 30-day rolling window

  - `cowork_weekly_active_user_count: int`

    Number of users with Cowork activity in the 7-day rolling window

  - `daily_active_user_count: int`

    Number of users with token consumption on the requested day

  - `daily_adoption_rate: Optional[float]`

    Percentage of assigned seats with activity on the requested day (`DAU / assigned_seat_count * 100`). Null when the response is scoped to an RBAC group.

  - `ending_at: datetime`

    End of the aggregation period (exclusive), UTC midnight in RFC 3339 format (e.g. `2026-01-16T00:00:00Z`).

    format: date-time

  - `monthly_active_user_count: int`

    Number of users with token consumption in the 30-day rolling window

  - `monthly_adoption_rate: Optional[float]`

    Percentage of assigned seats with activity in the 30-day rolling window (`MAU / assigned_seat_count * 100`). Null when the response is scoped to an RBAC group.

  - `pending_invite_count: Optional[int]`

    Number of pending invitations to join the organization. Null when the response is scoped to an RBAC group.

  - `starting_at: datetime`

    Start of the aggregation period (inclusive), UTC midnight in RFC 3339 format (e.g. `2026-01-15T00:00:00Z`).

    format: date-time

  - `weekly_active_user_count: int`

    Number of users with token consumption in the 7-day rolling window

  - `weekly_adoption_rate: Optional[float]`

    Percentage of assigned seats with activity in the 7-day rolling window (`WAU / assigned_seat_count * 100`). Null when the response is scoped to an RBAC group.

  - `chat_cowork_unified_daily_active_user_count: Optional[int]`

    Number of users with activity in Chat and Cowork unified on the requested day. Omitted from the response where Chat and Cowork unified is not available.

  - `chat_cowork_unified_monthly_active_user_count: Optional[int]`

    Number of users with activity in Chat and Cowork unified in the 28-day rolling window (30 days when the request filters by `rbac_group_id`). Omitted from the response where Chat and Cowork unified is not available.

  - `chat_cowork_unified_weekly_active_user_count: Optional[int]`

    Number of users with activity in Chat and Cowork unified in the 7-day rolling window. Omitted from the response where Chat and Cowork unified is not available.

  - `chat_daily_active_user_count: Optional[int]`

    Number of users with claude.ai (chat) activity on the requested day. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `chat_monthly_active_user_count: Optional[int]`

    Number of users with claude.ai (chat) activity in the 30-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `chat_weekly_active_user_count: Optional[int]`

    Number of users with claude.ai (chat) activity in the 7-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_code_daily_active_user_count: Optional[int]`

    Number of users with Claude Code activity on the requested day. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_code_monthly_active_user_count: Optional[int]`

    Number of users with Claude Code activity in the 30-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_code_weekly_active_user_count: Optional[int]`

    Number of users with Claude Code activity in the 7-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_design_daily_active_user_count: Optional[int]`

    Number of users with Claude Design activity on the requested day. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_design_monthly_active_user_count: Optional[int]`

    Number of users with Claude Design activity in the 30-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_design_weekly_active_user_count: Optional[int]`

    Number of users with Claude Design activity in the 7-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `office_agent_daily_active_user_count: Optional[int]`

    Number of users with Claude in Office activity on the requested day. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `office_agent_monthly_active_user_count: Optional[int]`

    Number of users with Claude in Office activity in the 30-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `office_agent_weekly_active_user_count: Optional[int]`

    Number of users with Claude in Office activity in the 7-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `science_daily_active_user_count: Optional[int]`

    Number of users with Claude Science activity on the requested day. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `science_entitled_user_count: Optional[int]`

    Number of users with a Claude Science seat entitlement (per-seat RBAC) at the time of the daily snapshot. The funnel top; independent of the org-level Claude Science toggle. Null when the response is scoped to an RBAC group — entitlement is org-wide and has no per-group analogue. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `science_monthly_active_user_count: Optional[int]`

    Number of users with Claude Science activity in the 30-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `science_weekly_active_user_count: Optional[int]`

    Number of users with Claude Science activity in the 7-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

#### Example

```python
import os
from datetime import date
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.analytics.summaries.list(
    starting_date=date.fromisoformat("2019-12-27"),
)
page = page.data[0]
print(page.assigned_seat_count)
```

##### Response (200)

```json
{
  "data": [
    {
      "assigned_seat_count": 0,
      "cowork_daily_active_user_count": 0,
      "cowork_monthly_active_user_count": 0,
      "cowork_weekly_active_user_count": 0,
      "daily_active_user_count": 0,
      "daily_adoption_rate": 0,
      "ending_at": "2019-12-27T18:11:19.117Z",
      "monthly_active_user_count": 0,
      "monthly_adoption_rate": 0,
      "pending_invite_count": 0,
      "starting_at": "2019-12-27T18:11:19.117Z",
      "weekly_active_user_count": 0,
      "weekly_adoption_rate": 0,
      "chat_cowork_unified_daily_active_user_count": 0,
      "chat_cowork_unified_monthly_active_user_count": 0,
      "chat_cowork_unified_weekly_active_user_count": 0,
      "chat_daily_active_user_count": 0,
      "chat_monthly_active_user_count": 0,
      "chat_weekly_active_user_count": 0,
      "claude_code_daily_active_user_count": 0,
      "claude_code_monthly_active_user_count": 0,
      "claude_code_weekly_active_user_count": 0,
      "claude_design_daily_active_user_count": 0,
      "claude_design_monthly_active_user_count": 0,
      "claude_design_weekly_active_user_count": 0,
      "office_agent_daily_active_user_count": 0,
      "office_agent_monthly_active_user_count": 0,
      "office_agent_weekly_active_user_count": 0,
      "science_daily_active_user_count": 0,
      "science_entitled_user_count": 0,
      "science_monthly_active_user_count": 0,
      "science_weekly_active_user_count": 0
    }
  ],
  "next_page": "next_page"
}
```

## Organization › Analytics › Users

### List User Activity

`organization.analytics.users.list(**kwargs) -> SyncPageCursor[AnalyticsUserActivity]`

**GET** `/v1/organizations/analytics/users`

Get per-user activity for a given day, with cursor-based pagination.

Returns activity metrics for each user in the organization, sorted by email
address. Use `group_by[]` for per-RBAC-group aggregates, or `filter[]` to
scope results to specific members, groups, or a chat project. Available
to organizations on a Claude Enterprise plan. Requires an API key with
the `read:analytics` scope.

#### Parameters

- `date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. The day to get user activity for. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

- `ending_date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. End of the date range (exclusive); only valid with `starting_date`. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day), so this can be at most today — which is also the default when omitted, resolved once when the first page is served and reused for the rest of the pagination sequence. At most 366 days after `starting_date`.

  format: date

- `filter: Optional[Sequence[str]]` (query parameter)

  Filters as `dimension:value`, e.g. `filter[]=rbac_group_id:{id}`. Repeat the param for OR within a dimension and across dimensions for AND. Supported dimensions on this endpoint: `project_id`, `rbac_group_id`, `user_id`. Value forms: `project_id` takes a tagged project id (`claude_proj_...`); `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in responses and by the spend-limits API) or a bare group UUID, and matches users who held the group at any point during each covered UTC day (time-of-usage attribution); `user_id` takes a tagged user id (`user_...`), as emitted in responses. An unsupported dimension returns 400. At most 100 entries. A `project_id` filter limits each member's row to their claude.ai chat activity in that project and cannot be combined with `group_by[]` or an `rbac_group_id` filter. On these rows, every count in `chat_cowork_unified_metrics.sessions` is 0, because sessions are not measured per project. On any day a member sent a chat message in Chat and Cowork unified, all of that member's project activity for the day is counted in `chat_cowork_unified_metrics.chat` instead of `chat_metrics`.

  maxItems: 100

- `group_by: Optional[List[AnalyticsUserGroupBy]]` (query parameter)

  Dimensions to break results out by (e.g. `group_by[]=rbac_group_id`). Supported on this endpoint: `rbac_group_id`. Rows are already per-member, so the one supported grouping aggregates them per RBAC group instead. Grouped rows carry the requested dimension values as additional fields and paginate like ungrouped responses via `next_page`; an unsupported dimension returns 400. `rbac_group_id` attributes a user to every group they held at any point during each covered UTC day, so grouped rows are not an exclusive partition and can sum above org-level totals. At most 100 entries.

  maxItems: 100

- `limit: Optional[int]` (query parameter)

  Number of results per page (1-1000, default 100).

  minimum: 1, maximum: 1000

- `order: Optional[AnalyticsOrder]` (query parameter)

  Sort direction: `asc` or `desc`. Defaults to `asc` for the endpoint's sort column and to `desc` when `order_by` names a metric (a top-N ranking). Applies to `order_by`, or to the endpoint's default sort field when `order_by` is omitted.

  - `"asc"`

  - `"desc"`

- `order_by: Optional[str]` (query parameter)

  Sort field. Restricted to the endpoint's sort column plus its rankable metrics (metrics default to descending; a few metrics rank in date-range mode only, per the endpoint's documented orderable set).

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field.

- `starting_date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. Start of a date range (inclusive). Enables rollup mode: one row per entity aggregated over the whole range — addable counters are summed across days, and a distinct count is never summed where summing could double-count (a field's range value is recomputed exactly over the window, approximate via HLL with typical error under 2%, null, or — for the creation-event counts, whose per-day values cannot overlap — a per-day sum that is itself exact; each field's own description says which). Use either `date` or `starting_date`, not both. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

#### Returns

- `class AnalyticsUserActivity`

  Per-user activity data for a given day.

  - `chat_metrics: AnalyticsChatMetrics`

    Claude.ai activity metrics for a single user on a given day.

    - `connectors_used_count: int`

      Number of MCP connector invocations.

    - `distinct_artifacts_created_count: int`

      Number of distinct artifacts created. Exact in date-range mode: a creation belongs to exactly one day, so the per-day counts never overlap and their sum over the window is the exact count of distinct creations in it.

    - `distinct_connectors_used_count: Optional[int]`

      Distinct claude.ai connectors this user used. Excludes calls whose connector could not be identified and all calls from organizations with zero data retention. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `distinct_conversation_count: Optional[int]`

      Number of distinct conversations the user participated in. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `distinct_files_uploaded_count: Optional[int]`

      Number of distinct files uploaded. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `distinct_projects_created_count: int`

      Number of distinct projects created. Exact in date-range mode: a creation belongs to exactly one day, so the per-day counts never overlap and their sum over the window is the exact count of distinct creations in it.

    - `distinct_projects_used_count: Optional[int]`

      Number of distinct projects used. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `distinct_shared_artifacts_viewed_count: Optional[int]`

      Number of distinct shared artifacts the user viewed. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `distinct_skills_used_count: Optional[int]`

      Number of distinct skills used. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `message_count: int`

      Number of messages sent

    - `shared_conversations_viewed_count: int`

      Number of times the user opened a shared conversation in a project

    - `thinking_message_count: int`

      Number of messages that used extended thinking

  - `claude_code_metrics: AnalyticsClaudeCodeMetrics`

    Claude Code activity metrics for a single user on a given day.

    - `core_metrics: AnalyticsCoreCodeMetrics`

      Core Claude Code activity metrics for a single user on a given day.

      - `artifacts_created_count: int`

        Number of artifacts created in Claude Code sessions: an artifact counts once, on the day a session first saves it. Counted from 2026-08-17; 0 on earlier days. Exact in date-range mode: a creation belongs to exactly one day, so the per-day counts never overlap and their sum over the window is the exact count of distinct creations in it.

      - `commit_count: int`

        Number of commits made via Claude Code

      - `distinct_session_count: Optional[int]`

        Number of distinct Claude Code sessions. On aggregated rows and in date-range mode: summed per-day distinct counts. A session essentially never spans a UTC day, so the sum is in practice the true distinct count.

      - `lines_of_code: AnalyticsLinesOfCode`

        Lines of code added and removed via Claude Code.

        - `added_count: int`

          Lines of code added

        - `removed_count: int`

          Lines of code removed

      - `pull_request_count: int`

        Number of pull requests created via Claude Code

    - `tool_actions: AnalyticsToolActions`

      Per-tool accepted/rejected counts for Claude Code file modification tools.

      - `edit_tool: AnalyticsToolActionCounts`

        Accepted/rejected counts for a single Claude Code tool type.

        - `accepted_count: int`

          Number of tool proposals accepted

        - `rejected_count: int`

          Number of tool proposals rejected

      - `multi_edit_tool: AnalyticsToolActionCounts`

        Accepted/rejected counts for a single Claude Code tool type.

      - `notebook_edit_tool: AnalyticsToolActionCounts`

        Accepted/rejected counts for a single Claude Code tool type.

      - `write_tool: AnalyticsToolActionCounts`

        Accepted/rejected counts for a single Claude Code tool type.

  - `cowork_metrics: AnalyticsCoworkMetrics`

    Cowork activity metrics for a single user on a given day.

    - `action_count: int`

      Number of tool actions completed in Cowork sessions

    - `artifacts_created_count: int`

      Number of artifacts created in Cowork sessions: an artifact counts once, on the day a session first saves it. Counted from 2026-08-17; 0 on earlier days. Exact in date-range mode: a creation belongs to exactly one day, so the per-day counts never overlap and their sum over the window is the exact count of distinct creations in it.

    - `connectors_used_count: int`

      Total number of connector invocations in Cowork sessions

    - `dispatch_turn_count: int`

      Number of Dispatch (background agent) turns completed

    - `distinct_connectors_used_count: Optional[int]`

      Number of distinct connectors used in Cowork sessions. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `distinct_plugins_used_count: Optional[int]`

      Number of distinct plugins used in Cowork sessions. Null while Cowork plugin-use metrics are not enabled for this organization. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `distinct_session_count: Optional[int]`

      Number of distinct Cowork sessions. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `distinct_skills_used_count: Optional[int]`

      Number of distinct skills used in Cowork sessions. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `edit_tool_count: Optional[int]`

      Number of successful Edit tool calls in Cowork sessions. Null while the file-edit metrics are not enabled for this organization.

    - `file_edit_count: Optional[int]`

      Number of successful file-edit tool calls (Edit, MultiEdit, Write, NotebookEdit) in Cowork sessions. Null, never 0, while the file-edit metrics are not enabled for this organization.

    - `message_count: int`

      Number of messages sent in Cowork sessions

    - `multi_edit_tool_count: Optional[int]`

      Number of successful MultiEdit tool calls in Cowork sessions. Null while the file-edit metrics are not enabled for this organization.

    - `notebook_edit_tool_count: Optional[int]`

      Number of successful NotebookEdit tool calls in Cowork sessions. Null while the file-edit metrics are not enabled for this organization.

    - `plugins_used_count: Optional[int]`

      Total number of plugin invocations in Cowork sessions. Null while Cowork plugin-use metrics are not enabled for this organization.

    - `sessions_with_file_edits_count: Optional[int]`

      Number of distinct Cowork sessions with at least one successful file-edit tool call. Null while the file-edit metrics are not enabled for this organization. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `skills_used_count: int`

      Total number of skill invocations in Cowork sessions

    - `write_tool_count: Optional[int]`

      Number of successful Write tool calls in Cowork sessions. Null while the file-edit metrics are not enabled for this organization.

  - `design_metrics: AnalyticsDesignMetrics`

    Claude Design activity metrics for a single user on a given day.

    - `distinct_projects_created_count: int`

      Number of distinct Claude Design projects created. Exact in date-range mode: a creation belongs to exactly one day, so the per-day counts never overlap and their sum over the window is the exact count of distinct creations in it.

    - `distinct_projects_used_count: Optional[int]`

      Number of distinct Claude Design projects the user worked in. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `distinct_session_count: Optional[int]`

      Number of distinct Claude Design sessions. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `message_count: int`

      Number of messages sent in Claude Design sessions

  - `distinct_user_count: Optional[int]`

    Number of distinct active users represented by this row. Only set for grouped rollups (`group_by[]`); null for per-user rows. In date-range mode, recomputed as an exact distinct count of the group's active members over the requested window, never a sum of per-day values.

  - `office_metrics: AnalyticsOfficeMetrics`

    Office Agent activity metrics for a single user on a given day, broken out by Office product.

    - `excel: AnalyticsOfficeProductMetrics`

      Office Agent activity metrics for a single user on a given day within one Office product.

      - `connectors_used_count: int`

        Number of MCP connector invocations

      - `distinct_connectors_used_count: Optional[int]`

        Number of distinct MCP connectors used. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `distinct_session_count: Optional[int]`

        Number of distinct Office Agent sessions. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `distinct_skills_used_count: Optional[int]`

        Number of distinct skills used. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `message_count: int`

        Number of messages sent

      - `skills_used_count: int`

        Number of skill invocations

    - `outlook: AnalyticsOfficeProductMetrics`

      Office Agent activity metrics for a single user on a given day within one Office product.

    - `powerpoint: AnalyticsOfficeProductMetrics`

      Office Agent activity metrics for a single user on a given day within one Office product.

    - `word: AnalyticsOfficeProductMetrics`

      Office Agent activity metrics for a single user on a given day within one Office product.

  - `science_metrics: AnalyticsScienceMetrics`

    Claude Science activity metrics for a single user on a given day.

    - `delegation_count: int`

      Number of delegations (handoffs to a specialized agent) in Claude Science sessions

    - `distinct_session_count: Optional[int]`

      Number of distinct Claude Science sessions. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `message_count: int`

      Number of messages sent in Claude Science sessions

    - `remote_compute_job_count: int`

      Number of remote compute jobs launched from Claude Science sessions

    - `skills_used_count: int`

      Total number of skill invocations in Claude Science sessions

  - `user: Optional[AnalyticsUser]`

    The user this row describes. Null on rows aggregated across users.

    - `type: Literal["user"]`

      Object type. Always `user`.

      default: user

    - `id: str`

      Tagged user identifier (e.g. `user_...`)

    - `email_address: str`

      Email address of the user

  - `web_search_count: int`

    Number of web searches performed

  - `chat_cowork_unified_metrics: Optional[AnalyticsChatCoworkUnifiedMetrics]`

    Activity recorded while the member had Chat and Cowork unified (Cowork's features inside claude.ai chat) turned on, split into `chat` (chat activity) and `sessions` (Cowork activity). Omitted from the response where Chat and Cowork unified is not available.

    - `chat: AnalyticsChatCoworkUnifiedChatMetrics`

      Chat activity recorded while members had Chat and Cowork unified turned
      on.

      - `connectors_used_count: int`

        Same measure as `chat_metrics.connectors_used_count`, for activity recorded while members had Chat and Cowork unified turned on.

      - `distinct_artifacts_created_count: int`

        Same measure as `chat_metrics.distinct_artifacts_created_count`, for activity recorded while members had Chat and Cowork unified turned on. Exact in date-range mode: a creation belongs to exactly one day, so the per-day counts never overlap and their sum over the window is the exact count of distinct creations in it.

      - `distinct_connectors_used_count: Optional[int]`

        Same measure as `chat_metrics.distinct_connectors_used_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `distinct_conversation_count: Optional[int]`

        Same measure as `chat_metrics.distinct_conversation_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `distinct_files_uploaded_count: Optional[int]`

        Same measure as `chat_metrics.distinct_files_uploaded_count`, for activity recorded while members had Chat and Cowork unified turned on. It counts uploaded files as well as files Claude created and images returned by Claude's tools, such as screenshots. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `distinct_projects_created_count: int`

        Same measure as `chat_metrics.distinct_projects_created_count`, for activity recorded while members had Chat and Cowork unified turned on. Exact in date-range mode: a creation belongs to exactly one day, so the per-day counts never overlap and their sum over the window is the exact count of distinct creations in it.

      - `distinct_projects_used_count: Optional[int]`

        Same measure as `chat_metrics.distinct_projects_used_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `distinct_shared_artifacts_viewed_count: Optional[int]`

        Always null: shared-artifact views are not currently measured.

      - `distinct_skills_used_count: Optional[int]`

        Same measure as `chat_metrics.distinct_skills_used_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `message_count: int`

        Same measure as `chat_metrics.message_count`, for activity recorded while members had Chat and Cowork unified turned on.

      - `shared_conversations_viewed_count: int`

        Same measure as `chat_metrics.shared_conversations_viewed_count`, for activity recorded while members had Chat and Cowork unified turned on.

      - `thinking_message_count: int`

        Same measure as `chat_metrics.thinking_message_count`, for activity recorded while members had Chat and Cowork unified turned on.

    - `sessions: AnalyticsChatCoworkUnifiedSessionsMetrics`

      Cowork session activity recorded while members had Chat and Cowork
      unified turned on.

      - `action_count: int`

        Same measure as `cowork_metrics.action_count`, for activity recorded while members had Chat and Cowork unified turned on.

      - `artifacts_created_count: int`

        Same measure as `cowork_metrics.artifacts_created_count`, for activity recorded while members had Chat and Cowork unified turned on. Exact in date-range mode: a creation belongs to exactly one day, so the per-day counts never overlap and their sum over the window is the exact count of distinct creations in it.

      - `connectors_used_count: int`

        Same measure as `cowork_metrics.connectors_used_count`, for activity recorded while members had Chat and Cowork unified turned on.

      - `dispatch_turn_count: int`

        Same measure as `cowork_metrics.dispatch_turn_count`, for activity recorded while members had Chat and Cowork unified turned on.

      - `distinct_connectors_used_count: Optional[int]`

        Same measure as `cowork_metrics.distinct_connectors_used_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `distinct_plugins_used_count: Optional[int]`

        Same measure as `cowork_metrics.distinct_plugins_used_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `distinct_session_count: Optional[int]`

        Same measure as `cowork_metrics.distinct_session_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `distinct_skills_used_count: Optional[int]`

        Same measure as `cowork_metrics.distinct_skills_used_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `edit_tool_count: Optional[int]`

        Same measure as `cowork_metrics.edit_tool_count`, for activity recorded while members had Chat and Cowork unified turned on.

      - `file_edit_count: Optional[int]`

        Same measure as `cowork_metrics.file_edit_count`, for activity recorded while members had Chat and Cowork unified turned on.

      - `message_count: int`

        Same measure as `cowork_metrics.message_count`, for activity recorded while members had Chat and Cowork unified turned on.

      - `multi_edit_tool_count: Optional[int]`

        Same measure as `cowork_metrics.multi_edit_tool_count`, for activity recorded while members had Chat and Cowork unified turned on. Claude no longer has a multi-edit tool, so expect 0 when not null; each edit is now a separate Edit tool call, counted in `edit_tool_count` and `file_edit_count`.

      - `notebook_edit_tool_count: Optional[int]`

        Same measure as `cowork_metrics.notebook_edit_tool_count`, for activity recorded while members had Chat and Cowork unified turned on.

      - `plugins_used_count: Optional[int]`

        Same measure as `cowork_metrics.plugins_used_count`, for activity recorded while members had Chat and Cowork unified turned on.

      - `sessions_with_file_edits_count: Optional[int]`

        Same measure as `cowork_metrics.sessions_with_file_edits_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

      - `skills_used_count: int`

        Same measure as `cowork_metrics.skills_used_count`, for activity recorded while members had Chat and Cowork unified turned on.

      - `write_tool_count: Optional[int]`

        Same measure as `cowork_metrics.write_tool_count`, for activity recorded while members had Chat and Cowork unified turned on.

  - `last_activity_date: Optional[date]`

    Most recent UTC day (YYYY-MM-DD) on which the user had any counted activity, within the requested window: equal to the requested `date` in single-day mode, and to the latest active day from `starting_date` (inclusive) to `ending_date` (exclusive) in date-range rollup mode — never a day earlier than the window start. On filtered requests (`filter[]`) only days matching the filter count: with `filter[]=rbac_group_id:{id}` it is the last day the user was active while a member of that group, consistent with the row's other metrics. On grouped (`group_by[]`) rows it is the latest day any member of the group was active (the requested `date` in single-day mode). Omitted from the response while last-activity reporting is not enabled for this organization.

    format: date

  - `rbac_group_id: Optional[str]`

    Tagged RBAC group identifier (`rbac_group_...`), matching the spend-limits API spelling. Present only when the request grouped by `rbac_group_id`.

  - `rbac_group_name: Optional[str]`

    Resolved RBAC group display name, alongside `rbac_group_id` when name resolution is available. Null if the group has been deleted or its name could not be resolved; `rbac_group_id` remains the stable key.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.analytics.users.list()
page = page.data[0]
print(page.rbac_group_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "chat_metrics": {
        "connectors_used_count": 0,
        "distinct_artifacts_created_count": 0,
        "distinct_connectors_used_count": 0,
        "distinct_conversation_count": 0,
        "distinct_files_uploaded_count": 0,
        "distinct_projects_created_count": 0,
        "distinct_projects_used_count": 0,
        "distinct_shared_artifacts_viewed_count": 0,
        "distinct_skills_used_count": 0,
        "message_count": 0,
        "shared_conversations_viewed_count": 0,
        "thinking_message_count": 0
      },
      "claude_code_metrics": {
        "core_metrics": {
          "artifacts_created_count": 0,
          "commit_count": 0,
          "distinct_session_count": 0,
          "lines_of_code": {
            "added_count": 0,
            "removed_count": 0
          },
          "pull_request_count": 0
        },
        "tool_actions": {
          "edit_tool": {
            "accepted_count": 0,
            "rejected_count": 0
          },
          "multi_edit_tool": {
            "accepted_count": 0,
            "rejected_count": 0
          },
          "notebook_edit_tool": {
            "accepted_count": 0,
            "rejected_count": 0
          },
          "write_tool": {
            "accepted_count": 0,
            "rejected_count": 0
          }
        }
      },
      "cowork_metrics": {
        "action_count": 0,
        "artifacts_created_count": 0,
        "connectors_used_count": 0,
        "dispatch_turn_count": 0,
        "distinct_connectors_used_count": 0,
        "distinct_plugins_used_count": 0,
        "distinct_session_count": 0,
        "distinct_skills_used_count": 0,
        "edit_tool_count": 0,
        "file_edit_count": 0,
        "message_count": 0,
        "multi_edit_tool_count": 0,
        "notebook_edit_tool_count": 0,
        "plugins_used_count": 0,
        "sessions_with_file_edits_count": 0,
        "skills_used_count": 0,
        "write_tool_count": 0
      },
      "design_metrics": {
        "distinct_projects_created_count": 0,
        "distinct_projects_used_count": 0,
        "distinct_session_count": 0,
        "message_count": 0
      },
      "distinct_user_count": 0,
      "office_metrics": {
        "excel": {
          "connectors_used_count": 0,
          "distinct_connectors_used_count": 0,
          "distinct_session_count": 0,
          "distinct_skills_used_count": 0,
          "message_count": 0,
          "skills_used_count": 0
        },
        "outlook": {
          "connectors_used_count": 0,
          "distinct_connectors_used_count": 0,
          "distinct_session_count": 0,
          "distinct_skills_used_count": 0,
          "message_count": 0,
          "skills_used_count": 0
        },
        "powerpoint": {
          "connectors_used_count": 0,
          "distinct_connectors_used_count": 0,
          "distinct_session_count": 0,
          "distinct_skills_used_count": 0,
          "message_count": 0,
          "skills_used_count": 0
        },
        "word": {
          "connectors_used_count": 0,
          "distinct_connectors_used_count": 0,
          "distinct_session_count": 0,
          "distinct_skills_used_count": 0,
          "message_count": 0,
          "skills_used_count": 0
        }
      },
      "science_metrics": {
        "delegation_count": 0,
        "distinct_session_count": 0,
        "message_count": 0,
        "remote_compute_job_count": 0,
        "skills_used_count": 0
      },
      "user": {
        "id": "id",
        "email_address": "email_address",
        "type": "user"
      },
      "web_search_count": 0,
      "chat_cowork_unified_metrics": {
        "chat": {
          "connectors_used_count": 0,
          "distinct_artifacts_created_count": 0,
          "distinct_connectors_used_count": 0,
          "distinct_conversation_count": 0,
          "distinct_files_uploaded_count": 0,
          "distinct_projects_created_count": 0,
          "distinct_projects_used_count": 0,
          "distinct_shared_artifacts_viewed_count": 0,
          "distinct_skills_used_count": 0,
          "message_count": 0,
          "shared_conversations_viewed_count": 0,
          "thinking_message_count": 0
        },
        "sessions": {
          "action_count": 0,
          "artifacts_created_count": 0,
          "connectors_used_count": 0,
          "dispatch_turn_count": 0,
          "distinct_connectors_used_count": 0,
          "distinct_plugins_used_count": 0,
          "distinct_session_count": 0,
          "distinct_skills_used_count": 0,
          "edit_tool_count": 0,
          "file_edit_count": 0,
          "message_count": 0,
          "multi_edit_tool_count": 0,
          "notebook_edit_tool_count": 0,
          "plugins_used_count": 0,
          "sessions_with_file_edits_count": 0,
          "skills_used_count": 0,
          "write_tool_count": 0
        }
      },
      "last_activity_date": "2019-12-27",
      "rbac_group_id": "rbac_group_id",
      "rbac_group_name": "rbac_group_name"
    }
  ],
  "next_page": "next_page"
}
```

## Organization › Analytics › Apps › Chat › Projects

### Get Chat Project Usage

`organization.analytics.apps.chat.projects.list(**kwargs) -> SyncPageCursor[AnalyticsProjectActivity]`

**GET** `/v1/organizations/analytics/apps/chat/projects`

Get per-project activity for a given day, with cursor-based pagination.

Returns activity metrics for each project in the organization, sorted by
project ID. Use `group_by[]` to break projects out per member or per RBAC
group, and `filter[]` to scope results; the parameter descriptions list the
supported dimensions. Available to organizations on a Claude Enterprise
plan. Requires an API key with the `read:analytics` scope.

#### Parameters

- `date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. The day to get project activity for. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

- `ending_date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. End of the date range (exclusive); only valid with `starting_date`. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day), so this can be at most today — which is also the default when omitted, resolved once when the first page is served and reused for the rest of the pagination sequence. At most 366 days after `starting_date`.

  format: date

- `filter: Optional[Sequence[str]]` (query parameter)

  Filters as `dimension:value`, e.g. `filter[]=rbac_group_id:{id}`. Repeat the param for OR within a dimension and across dimensions for AND. Supported dimensions on this endpoint: `project_id`, `rbac_group_id`, `user_id`. Value forms: `project_id` takes a tagged project id (`claude_proj_...`); `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in responses and by the spend-limits API) or a bare group UUID, and matches users who held the group at any point during each covered UTC day (time-of-usage attribution); `user_id` takes a tagged user id (`user_...`), as emitted in responses. An unsupported dimension returns 400. At most 100 entries.

  maxItems: 100

- `group_by: Optional[List[AnalyticsProjectGroupBy]]` (query parameter)

  Dimensions to break results out by (e.g. `group_by[]=user_id`). Supported on this endpoint: `rbac_group_id`, `user_id`. Grouped rows carry the requested dimension values as additional fields and paginate like ungrouped responses via `next_page`; an unsupported dimension returns 400. `rbac_group_id` attributes a user to every group they held at any point during each covered UTC day, so grouped rows are not an exclusive partition and can sum above org-level totals. At most 100 entries.

  maxItems: 100

  - `"rbac_group_id"`

  - `"user_id"`

- `limit: Optional[int]` (query parameter)

  Number of results per page (1-1000, default 100).

  minimum: 1, maximum: 1000

- `order: Optional[AnalyticsOrder]` (query parameter)

  Sort direction: `asc` or `desc`. Defaults to `asc` for the endpoint's sort column and to `desc` when `order_by` names a metric (a top-N ranking). Applies to `order_by`, or to the endpoint's default sort field when `order_by` is omitted.

  - `"asc"`

  - `"desc"`

- `order_by: Optional[str]` (query parameter)

  Sort field. Restricted to the endpoint's sort column plus its rankable metrics (metrics default to descending; a few metrics rank in date-range mode only, per the endpoint's documented orderable set).

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field.

- `starting_date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. Start of a date range (inclusive). Enables rollup mode: one row per entity aggregated over the whole range — addable counters are summed across days, and a distinct count is never summed where summing could double-count (a field's range value is recomputed exactly over the window, approximate via HLL with typical error under 2%, null, or — for the creation-event counts, whose per-day values cannot overlap — a per-day sum that is itself exact; each field's own description says which). Use either `date` or `starting_date`, not both. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

#### Returns

- `class AnalyticsProjectActivity`

  Per-project activity data for a given day.

  - `created_at: Optional[datetime]`

    Project creation timestamp in RFC 3339 format. Null if the project was deleted before attribution was recorded.

    format: date-time

  - `created_by: Optional[AnalyticsUser]`

    User who created the project. Null if the project was deleted before attribution was recorded, or if the creator's account no longer exists.

    - `type: Literal["user"]`

      Object type. Always `user`.

      default: user

    - `id: str`

      Tagged user identifier (e.g. `user_...`)

    - `email_address: str`

      Email address of the user

  - `distinct_conversation_count: Optional[int]`

    Number of distinct conversations in the project. Null on aggregated rows where a distinct count cannot be computed.

  - `distinct_user_count: int`

    Number of distinct users who used the project on the requested day, or, in date-range mode, over the requested window — recomputed as an exact distinct count over the window's per-member daily rows, never a sum of per-day values.

  - `message_count: int`

    Number of messages sent in the project on the requested day

  - `project_id: str`

    Tagged project identifier (e.g. `claude_proj_...`)

  - `project_name: str`

    Name of the project

  - `rbac_group_id: Optional[str]`

    Tagged RBAC group identifier (`rbac_group_...`), matching the spend-limits API spelling. Present only when the request grouped by `rbac_group_id`.

  - `rbac_group_name: Optional[str]`

    Resolved RBAC group display name, alongside `rbac_group_id` when name resolution is available. Null if the group has been deleted or its name could not be resolved; `rbac_group_id` remains the stable key.

  - `user_id: Optional[str]`

    Tagged user identifier (e.g. `user_...`). Present only when the request grouped by `user_id`.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.analytics.apps.chat.projects.list()
page = page.data[0]
print(page.project_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "created_at": "2019-12-27T18:11:19.117Z",
      "created_by": {
        "id": "id",
        "email_address": "email_address",
        "type": "user"
      },
      "distinct_conversation_count": 0,
      "distinct_user_count": 0,
      "message_count": 0,
      "project_id": "project_id",
      "project_name": "project_name",
      "rbac_group_id": "rbac_group_id",
      "rbac_group_name": "rbac_group_name",
      "user_id": "user_id"
    }
  ],
  "next_page": "next_page"
}
```

## Organization › Analytics › Connectors

### Get Connector Usage

`organization.analytics.connectors.list(**kwargs) -> SyncPageCursor[AnalyticsConnectorActivity]`

**GET** `/v1/organizations/analytics/connectors`

Get per-connector usage for a given day, with cursor-based pagination.

Returns connector usage metrics for the organization, sorted by connector
name. Connector names are normalized from their various sources — for
example, "Atlassian MCP server" and "mcp-atlassian" both appear as
"atlassian". Use `group_by[]` to break usage out per member, per RBAC
group, or per product surface, and `filter[]` to scope results; the
parameter descriptions list the supported dimensions. Available to
organizations on a Claude Enterprise plan. Requires an API key with the
`read:analytics` scope.

#### Parameters

- `date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. The day to get connector usage for. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

- `ending_date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. End of the date range (exclusive); only valid with `starting_date`. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day), so this can be at most today — which is also the default when omitted, resolved once when the first page is served and reused for the rest of the pagination sequence. At most 366 days after `starting_date`.

  format: date

- `filter: Optional[Sequence[str]]` (query parameter)

  Filters as `dimension:value`, e.g. `filter[]=rbac_group_id:{id}`. Repeat the param for OR within a dimension and across dimensions for AND. Supported dimensions on this endpoint: `connector_name`, `product`, `rbac_group_id`, `user_id`. Value forms: `connector_name` matches case-insensitively, a display name such as 'GitHub MCP' also matches its normalized stored form ('github'), and for rows whose `connector_name` is an opaque connector id the connector's display name (`connector_display_name`) also matches; `product` is one of `chat_cowork_unified`, `chat`, `claude_code`, `cowork`, or `office_agent`; `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in responses and by the spend-limits API) or a bare group UUID, and matches users who held the group at any point during each covered UTC day (time-of-usage attribution); `user_id` takes a tagged user id (`user_...`), as emitted in responses. An unsupported dimension returns 400. At most 100 entries. `chat_cowork_unified` is accepted as a `product` value only where Chat and Cowork unified is available.

  maxItems: 100

- `group_by: Optional[List[AnalyticsConnectorGroupBy]]` (query parameter)

  Dimensions to break results out by (e.g. `group_by[]=user_id`). Supported on this endpoint: `product`, `rbac_group_id`, `user_id`. Grouped rows carry the requested dimension values as additional fields and paginate like ungrouped responses via `next_page`; an unsupported dimension returns 400. `rbac_group_id` attributes a user to every group they held at any point during each covered UTC day, so grouped rows are not an exclusive partition and can sum above org-level totals. At most 100 entries.

  maxItems: 100

  - `"product"`

  - `"rbac_group_id"`

  - `"user_id"`

- `limit: Optional[int]` (query parameter)

  Number of results per page (1-1000, default 100).

  minimum: 1, maximum: 1000

- `order: Optional[AnalyticsOrder]` (query parameter)

  Sort direction: `asc` or `desc`. Defaults to `asc` for the endpoint's sort column and to `desc` when `order_by` names a metric (a top-N ranking). Applies to `order_by`, or to the endpoint's default sort field when `order_by` is omitted.

  - `"asc"`

  - `"desc"`

- `order_by: Optional[str]` (query parameter)

  Sort field. Restricted to the endpoint's sort column plus its rankable metrics (metrics default to descending; a few metrics rank in date-range mode only, per the endpoint's documented orderable set).

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field.

- `starting_date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. Start of a date range (inclusive). Enables rollup mode: one row per entity aggregated over the whole range — addable counters are summed across days, and a distinct count is never summed where summing could double-count (a field's range value is recomputed exactly over the window, approximate via HLL with typical error under 2%, null, or — for the creation-event counts, whose per-day values cannot overlap — a per-day sum that is itself exact; each field's own description says which). Use either `date` or `starting_date`, not both. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

#### Returns

- `class AnalyticsConnectorActivity`

  Per-connector activity data for a given day.

  - `chat_metrics: AnalyticsConnectorChatMetrics`

    Claude.ai activity metrics for a single connector on a given day.

    - `distinct_conversation_connector_used_count: Optional[int]`

      Number of distinct conversations in which the connector was used. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

  - `claude_code_metrics: AnalyticsConnectorClaudeCodeMetrics`

    Claude Code activity metrics for a single connector on a given day.

    - `distinct_session_connector_used_count: Optional[int]`

      Number of distinct Claude Code sessions in which the connector was used. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

  - `connector_display_name: Optional[str]`

    Human-readable display name for rows whose `connector_name` is an opaque connector id rather than a readable name, resolved at request time from the organization's connectors (including connectors that have since been removed). `connector_name` remains the row's stable key for sorting and pagination, and `filter[]=connector_name:{value}` also matches these rows by display name. Display names are not unique, and the same connector's claude.ai usage can appear under a separate row with a readable `connector_name`. Null when `connector_name` is already a readable name, when the id cannot be resolved to one of the organization's connectors, or when display-name resolution is not enabled for this organization.

  - `connector_name: str`

    Name of the connector. Some rows carry an opaque connector id here instead of a readable name; `connector_display_name` holds the resolved name for those rows.

  - `cowork_metrics: AnalyticsConnectorCoworkMetrics`

    Cowork activity metrics for a single connector on a given day.

    - `distinct_session_connector_used_count: Optional[int]`

      Number of distinct Cowork sessions in which the connector was used. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

  - `distinct_user_count: int`

    Number of distinct users who used the connector on the requested day, or, in date-range mode, over the requested window — recomputed as an exact distinct count over the window's per-member daily rows, never a sum of per-day values.

  - `individual_auth_distinct_user_count: Optional[int]`

    Number of distinct users whose use of this connector on the requested day ran on their own individual credential, connected through their own consent flow. Companion bucket to `managed_auth_distinct_user_count`, which carries the measurement, attribution, and null rules. Users whose requests used no stored credential count in neither bucket.

  - `managed_auth_distinct_user_count: Optional[int]`

    Number of distinct users whose use of this connector on the requested day ran on Enterprise Managed Auth (an organization-managed credential provisioned through the organization's identity provider), read from the token record each request used. Null, never 0, when managed-auth reporting is not enabled for the organization, the value cannot be attributed to the row, no credentialed requests and no managed-token mint events (a managed credential being provisioned for a user's use of the connector) were observed that day, or the day predates 2026-07-01, the first day the backing data exists (forward-only data, no backfill). When credentialed requests or mint events were observed and attributed, both managed-auth fields populate, reporting 0 for a bucket with no users; the two counts are independent, not a partition — a user whose requests that day used both kinds of credential counts in both. Mint events carry user but not surface attribution, so they count as observed auth activity on `user_id` and `rbac_group_id` cuts — attributed to the user the credential was provisioned for — but never on a cut that references `product` (group or filter). Date-range rollup mode (`starting_date`/`ending_date`) computes both fields exactly over the window — distinct users with at least one qualifying day — when the whole window starts on or after 2026-07-01, with the null-versus-0 and mint-event rules applying with the window in place of the day; a range starting earlier reports every managed-auth field as null, never a partial-window value.

  - `office_metrics: AnalyticsConnectorOfficeMetrics`

    Office Agent activity metrics for a single connector on a given day, broken out by Office product.

    - `excel: AnalyticsConnectorOfficeProductMetrics`

      Office Agent activity metrics for a single connector on a given day within one Office product.

      - `distinct_session_connector_used_count: Optional[int]`

        Number of distinct Office Agent sessions in which the connector was used. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `outlook: AnalyticsConnectorOfficeProductMetrics`

      Office Agent activity metrics for a single connector on a given day within one Office product.

    - `powerpoint: AnalyticsConnectorOfficeProductMetrics`

      Office Agent activity metrics for a single connector on a given day within one Office product.

    - `word: AnalyticsConnectorOfficeProductMetrics`

      Office Agent activity metrics for a single connector on a given day within one Office product.

  - `read_call_count: Optional[int]`

    Number of connector tool calls on the requested day whose trusted read-only annotation marked them read-only. Call count, not distinct users. Every call recorded on a classified surface lands in exactly one of `read_call_count`, `write_call_count`, or `unclassified_call_count`, so the three sum to the day's classified calls. Classification is forward-only per surface: claude.ai from 2026-06-01, Claude Code from 2026-05-30, Claude in Office from 2026-05-29, Cowork from 2026-06-02 (Cowork clients predating annotation forwarding land in `unclassified_call_count`). Null, never 0, when the value cannot be stated: the read/write split is not enabled for this organization, or the day predates 2026-05-29. For a date-range total, sum the per-day values, but treat a window that extends before 2026-05-29 as null rather than summing only its covered days — date-range rollup mode (`starting_date`/`ending_date`) applies both rules server-side.

  - `unclassified_call_count: Optional[int]`

    Number of connector tool calls on the requested day with no trusted read-only annotation — the annotation is optional in the MCP spec and is discarded when connector access controls are active, so unclassified calls are common. This field shows how much of the day's classified activity the read/write split actually covers. Call count, not distinct users. One of the three call-classification buckets; see `read_call_count` for the per-surface data-start dates, null conditions, and date-range guidance.

  - `write_call_count: Optional[int]`

    Number of connector tool calls on the requested day whose trusted read-only annotation marked them not read-only. Call count, not distinct users. One of the three call-classification buckets; see `read_call_count` for the per-surface data-start dates, null conditions, and date-range guidance.

  - `chat_cowork_unified_metrics: Optional[AnalyticsConnectorChatCoworkUnifiedMetrics]`

    Connector use recorded while members had Chat and Cowork unified (Cowork's features inside claude.ai chat) turned on, split into chat conversations and Cowork sessions. A count is null in date-range mode where it cannot be computed. Omitted from the response where Chat and Cowork unified is not available.

    - `chat: AnalyticsConnectorChatCoworkUnifiedChatMetrics`

      A connector's use in chat conversations recorded while members had
      Chat and Cowork unified turned on.

      - `distinct_conversation_connector_used_count: Optional[int]`

        Same measure as `chat_metrics.distinct_conversation_connector_used_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `sessions: AnalyticsConnectorChatCoworkUnifiedSessionsMetrics`

      A connector's use in Cowork sessions recorded while members had
      Chat and Cowork unified turned on.

      - `distinct_session_connector_used_count: Optional[int]`

        Same measure as `cowork_metrics.distinct_session_connector_used_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

  - `product: Optional[str]`

    Product that produced this row's activity: one of `chat`, `claude_code`, `cowork`, `office_agent`, or `chat_cowork_unified` (Chat and Cowork unified). These are the canonical Cost & Usage product names; an `office_agent` row's per-surface breakdown is in its `office_metrics`. On `/plugins` only `cowork`, `claude_code` and `chat_cowork_unified` occur (the only surfaces with plugin attribution); on `/artifacts` only `chat`, `claude_code`, `cowork` and `chat_cowork_unified` occur (the surfaces that create artifacts); `/apps/chat/projects` does not support the product dimension (a `product` entry in `group_by[]` or `filter[]` there is rejected). Present only when the request grouped by `product`.

  - `rbac_group_id: Optional[str]`

    Tagged RBAC group identifier (`rbac_group_...`), matching the spend-limits API spelling. Present only when the request grouped by `rbac_group_id`.

  - `rbac_group_name: Optional[str]`

    Resolved RBAC group display name, alongside `rbac_group_id` when name resolution is available. Null if the group has been deleted or its name could not be resolved; `rbac_group_id` remains the stable key.

  - `user_id: Optional[str]`

    Tagged user identifier (e.g. `user_...`). Present only when the request grouped by `user_id`.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.analytics.connectors.list()
page = page.data[0]
print(page.individual_auth_distinct_user_count)
```

##### Response (200)

```json
{
  "data": [
    {
      "chat_metrics": {
        "distinct_conversation_connector_used_count": 0
      },
      "claude_code_metrics": {
        "distinct_session_connector_used_count": 0
      },
      "connector_display_name": "connector_display_name",
      "connector_name": "connector_name",
      "cowork_metrics": {
        "distinct_session_connector_used_count": 0
      },
      "distinct_user_count": 0,
      "individual_auth_distinct_user_count": 0,
      "managed_auth_distinct_user_count": 0,
      "office_metrics": {
        "excel": {
          "distinct_session_connector_used_count": 0
        },
        "outlook": {
          "distinct_session_connector_used_count": 0
        },
        "powerpoint": {
          "distinct_session_connector_used_count": 0
        },
        "word": {
          "distinct_session_connector_used_count": 0
        }
      },
      "read_call_count": 0,
      "unclassified_call_count": 0,
      "write_call_count": 0,
      "chat_cowork_unified_metrics": {
        "chat": {
          "distinct_conversation_connector_used_count": 0
        },
        "sessions": {
          "distinct_session_connector_used_count": 0
        }
      },
      "product": "product",
      "rbac_group_id": "rbac_group_id",
      "rbac_group_name": "rbac_group_name",
      "user_id": "user_id"
    }
  ],
  "next_page": "next_page"
}
```

## Organization › Analytics › Plugins

### Get Plugin Usage

`organization.analytics.plugins.list(**kwargs) -> SyncPageCursor[AnalyticsPluginActivity]`

**GET** `/v1/organizations/analytics/plugins`

Get per-plugin install + invocation usage for a given day, with pagination.

Returns plugin usage metrics for the organization across Cowork and Claude
Code, sorted by plugin name. The `plugin_name` value `third-party` is
an aggregate bucket, not a plugin: it collects plugin activity, from
either surface, for which the reporting client did not provide a plugin
name — so an organization's own plugins can contribute both to their own
named rows and to this bucket. Use `group_by[]` to break usage out per
member, per RBAC group, or per product surface (Cowork / Claude Code),
and `filter[]` to scope results; the parameter descriptions list the
supported dimensions. Requires an API key with the
`read:analytics` scope. `starting_date` / `ending_date` select
range-rollup mode like `/skills`.

#### Parameters

- `date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. The day to get plugin usage for. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

- `ending_date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. End of the date range (exclusive); only valid with `starting_date`. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day), so this can be at most today — which is also the default when omitted, resolved once when the first page is served and reused for the rest of the pagination sequence. At most 366 days after `starting_date`.

  format: date

- `filter: Optional[Sequence[str]]` (query parameter)

  Filters as `dimension:value`, e.g. `filter[]=rbac_group_id:{id}`. Repeat the param for OR within a dimension and across dimensions for AND. Supported dimensions on this endpoint: `plugin_name`, `product`, `rbac_group_id`, `user_id`. Value forms: `plugin_name` matches case-insensitively; `product` is `chat_cowork_unified`, `claude_code`, or `cowork` (the only surfaces with plugin attribution); `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in responses and by the spend-limits API) or a bare group UUID, and matches users who held the group at any point during each covered UTC day (time-of-usage attribution); `user_id` takes a tagged user id (`user_...`), as emitted in responses. An unsupported dimension returns 400. At most 100 entries. `chat_cowork_unified` is accepted as a `product` value only where Chat and Cowork unified is available.

  maxItems: 100

- `group_by: Optional[List[AnalyticsPluginGroupBy]]` (query parameter)

  Dimensions to break results out by (e.g. `group_by[]=user_id`). Supported on this endpoint: `product`, `rbac_group_id`, `user_id`. On this endpoint `product` takes the values `chat_cowork_unified`, `claude_code`, or `cowork` only (the surfaces with plugin attribution). Grouped rows carry the requested dimension values as additional fields and paginate like ungrouped responses via `next_page`; an unsupported dimension returns 400. `rbac_group_id` attributes a user to every group they held at any point during each covered UTC day, so grouped rows are not an exclusive partition and can sum above org-level totals. At most 100 entries.

  maxItems: 100

  - `"product"`

  - `"rbac_group_id"`

  - `"user_id"`

- `limit: Optional[int]` (query parameter)

  Number of results per page (1-1000, default 100).

  minimum: 1, maximum: 1000

- `order: Optional[AnalyticsOrder]` (query parameter)

  Sort direction: `asc` or `desc`. Defaults to `asc` for the endpoint's sort column and to `desc` when `order_by` names a metric (a top-N ranking). Applies to `order_by`, or to the endpoint's default sort field when `order_by` is omitted.

  - `"asc"`

  - `"desc"`

- `order_by: Optional[str]` (query parameter)

  Sort field. Restricted to the endpoint's sort column plus its rankable metrics (metrics default to descending; a few metrics rank in date-range mode only, per the endpoint's documented orderable set).

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field.

- `starting_date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. Start of a date range (inclusive). Enables rollup mode: one row per entity aggregated over the whole range — addable counters are summed across days, and a distinct count is never summed where summing could double-count (a field's range value is recomputed exactly over the window, approximate via HLL with typical error under 2%, null, or — for the creation-event counts, whose per-day values cannot overlap — a per-day sum that is itself exact; each field's own description says which). Use either `date` or `starting_date`, not both. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

#### Returns

- `class AnalyticsPluginActivity`

  Per-plugin install + invocation activity for a given day.

  With `group_by[]=user_id` / `rbac_group_id` / `product` (`cowork`,
  `claude_code` and `chat_cowork_unified` only on this endpoint) each row is
  one (plugin, user), (plugin, group), or (plugin, product) cut: the flat
  `user_id` / `rbac_group_id` / `product` keys carry the cut and the counts
  are scoped to it.

  - `claude_code_metrics: AnalyticsPluginClaudeCodeMetrics`

    Claude Code activity metrics for a single plugin on a given day.

    - `distinct_session_plugin_used_count: Optional[int]`

      Number of distinct Claude Code sessions in which the plugin was invoked. Null on aggregated rows where a distinct count cannot be computed.

  - `cowork_metrics: AnalyticsPluginCoworkMetrics`

    Cowork activity metrics for a single plugin on a given day.

    - `distinct_session_plugin_used_count: Optional[int]`

      Number of distinct Cowork sessions in which the plugin was invoked. Null on aggregated rows where a distinct count cannot be computed.

  - `distinct_user_count: int`

    Number of distinct users with recorded install or invocation activity for the plugin on the requested day (install-only users count), or, in date-range mode, over the requested window — recomputed as an exact distinct count over the window's per-member daily rows, never a sum of per-day values.

  - `install_count: Optional[int]`

    Number of distinct users who installed the plugin on the requested day, or, in date-range mode, over the requested window — recomputed as an exact distinct count over the window's per-member daily rows, never a sum of per-day values.

  - `invocation_count: int`

    Number of plugin invocations on the requested day

  - `plugin_id: Optional[str]`

    Stable plugin identifier when available (e.g. `serena@claude-plugins-official`). Null for third-party Claude Code plugins (redacted at the source) and Cowork slash commands that carry only a hashed id.

  - `plugin_name: str`

    Name of the plugin

  - `chat_cowork_unified_metrics: Optional[AnalyticsPluginChatCoworkUnifiedMetrics]`

    Plugin use recorded while members had Chat and Cowork unified (Cowork's features inside claude.ai chat) turned on. A count is null in date-range mode where it cannot be computed. Omitted from the response where Chat and Cowork unified is not available.

    - `distinct_session_plugin_used_count: Optional[int]`

      Same measure as `cowork_metrics.distinct_session_plugin_used_count`, for activity recorded while members had Chat and Cowork unified turned on. Null on aggregated rows where a distinct count cannot be computed.

  - `product: Optional[str]`

    Product that produced this row's activity: one of `chat`, `claude_code`, `cowork`, `office_agent`, or `chat_cowork_unified` (Chat and Cowork unified). These are the canonical Cost & Usage product names; an `office_agent` row's per-surface breakdown is in its `office_metrics`. On `/plugins` only `cowork`, `claude_code` and `chat_cowork_unified` occur (the only surfaces with plugin attribution); on `/artifacts` only `chat`, `claude_code`, `cowork` and `chat_cowork_unified` occur (the surfaces that create artifacts); `/apps/chat/projects` does not support the product dimension (a `product` entry in `group_by[]` or `filter[]` there is rejected). Present only when the request grouped by `product`.

  - `rbac_group_id: Optional[str]`

    Tagged RBAC group identifier (`rbac_group_...`), matching the spend-limits API spelling. Present only when the request grouped by `rbac_group_id`.

  - `rbac_group_name: Optional[str]`

    Resolved RBAC group display name, alongside `rbac_group_id` when name resolution is available. Null if the group has been deleted or its name could not be resolved; `rbac_group_id` remains the stable key.

  - `user_id: Optional[str]`

    Tagged user identifier (e.g. `user_...`). Present only when the request grouped by `user_id`.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.analytics.plugins.list()
page = page.data[0]
print(page.plugin_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "claude_code_metrics": {
        "distinct_session_plugin_used_count": 0
      },
      "cowork_metrics": {
        "distinct_session_plugin_used_count": 0
      },
      "distinct_user_count": 0,
      "install_count": 0,
      "invocation_count": 0,
      "plugin_id": "plugin_id",
      "plugin_name": "plugin_name",
      "chat_cowork_unified_metrics": {
        "distinct_session_plugin_used_count": 0
      },
      "product": "product",
      "rbac_group_id": "rbac_group_id",
      "rbac_group_name": "rbac_group_name",
      "user_id": "user_id"
    }
  ],
  "next_page": "next_page"
}
```

## Organization › Analytics › Skills

### Get Skill Usage

`organization.analytics.skills.list(**kwargs) -> SyncPageCursor[AnalyticsSkillActivity]`

**GET** `/v1/organizations/analytics/skills`

Get per-skill usage for a given day, with cursor-based pagination.

Returns skill usage metrics for the organization, sorted by skill name.
Use `group_by[]` to break usage out per member, per RBAC group, or per
product surface, and `filter[]` to scope results; the parameter
descriptions list the supported dimensions. Available to organizations
on a Claude Enterprise plan. Requires an API key with the
`read:analytics` scope.

#### Parameters

- `date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. The day to get skill usage for. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

- `ending_date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. End of the date range (exclusive); only valid with `starting_date`. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day), so this can be at most today — which is also the default when omitted, resolved once when the first page is served and reused for the rest of the pagination sequence. At most 366 days after `starting_date`.

  format: date

- `filter: Optional[Sequence[str]]` (query parameter)

  Filters as `dimension:value`, e.g. `filter[]=rbac_group_id:{id}`. Repeat the param for OR within a dimension and across dimensions for AND. Supported dimensions on this endpoint: `product`, `rbac_group_id`, `share_status`, `skill_name`, `user_id`. Value forms: `product` is one of `chat_cowork_unified`, `chat`, `claude_code`, `cowork`, or `office_agent`; `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in responses and by the spend-limits API) or a bare group UUID, and matches users who held the group at any point during each covered UTC day (time-of-usage attribution); `share_status` is one of `organization`, `private`, or `public`; `skill_name` matches case-insensitively; `user_id` takes a tagged user id (`user_...`), as emitted in responses. An unsupported dimension returns 400. At most 100 entries. `chat_cowork_unified` is accepted as a `product` value only where Chat and Cowork unified is available.

  maxItems: 100

- `group_by: Optional[List[AnalyticsSkillGroupBy]]` (query parameter)

  Dimensions to break results out by (e.g. `group_by[]=user_id`). Supported on this endpoint: `product`, `rbac_group_id`, `user_id`. Grouped rows carry the requested dimension values as additional fields and paginate like ungrouped responses via `next_page`; an unsupported dimension returns 400. `rbac_group_id` attributes a user to every group they held at any point during each covered UTC day, so grouped rows are not an exclusive partition and can sum above org-level totals. At most 100 entries.

  maxItems: 100

  - `"product"`

  - `"rbac_group_id"`

  - `"user_id"`

- `limit: Optional[int]` (query parameter)

  Number of results per page (1-1000, default 100).

  minimum: 1, maximum: 1000

- `order: Optional[AnalyticsOrder]` (query parameter)

  Sort direction: `asc` or `desc`. Defaults to `asc` for the endpoint's sort column and to `desc` when `order_by` names a metric (a top-N ranking). Applies to `order_by`, or to the endpoint's default sort field when `order_by` is omitted.

  - `"asc"`

  - `"desc"`

- `order_by: Optional[str]` (query parameter)

  Sort field. Restricted to the endpoint's sort column plus its rankable metrics (metrics default to descending; a few metrics rank in date-range mode only, per the endpoint's documented orderable set).

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field.

- `starting_date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. Start of a date range (inclusive). Enables rollup mode: one row per entity aggregated over the whole range — addable counters are summed across days, and a distinct count is never summed where summing could double-count (a field's range value is recomputed exactly over the window, approximate via HLL with typical error under 2%, null, or — for the creation-event counts, whose per-day values cannot overlap — a per-day sum that is itself exact; each field's own description says which). Use either `date` or `starting_date`, not both. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

#### Returns

- `class AnalyticsSkillActivity`

  Per-skill activity data for a given day.

  - `attributed_list_price: Optional[str]`

    List-price (rate-card) value of the member requests attributed to this skill, as a decimal string in the minor unit of `currency` (cents for USD), from Claude Code, Cowork, and Office Agent request-level attribution — the value of requests that involved the skill, not the skill's incremental cost. Unlike `estimated_overage_spend` this reflects usage value regardless of how it was funded — seat-covered usage counts — but it is undiscounted and does not tie to billed spend or the organization's spend reporting. claude.ai chat usage carries no request-level attribution and contributes nothing: the field is null on `chat` product rows and on `office_agent` product cuts dated before 2026-06-18 (the Office Agent attribution data-start), and on ungrouped rows it covers the Claude Code + Cowork + Office Agent share only (null when no attributable usage exists). Also null under the same conditions as `estimated_overage_spend` (spend reporting not enabled for this organization, `office_agent` product cuts before the 2026-06-18 data-start). "0" means attributable usage existed but none was attributed to this skill. Addable across days: date-range rollup mode returns the window's sum. On `group_by[]` and `filter[]` shapes both amounts can total below the ungrouped value for the same skill over the same date or range: spend attributed to a member–skill pair with no counted usage on that day is excluded from those cuts.

  - `chat_metrics: AnalyticsSkillChatMetrics`

    Claude.ai activity metrics for a single skill on a given day.

    - `distinct_conversation_skill_used_count: Optional[int]`

      Number of distinct conversations in which the skill was used. A skill counts as used only when it is explicitly activated — the model (or the user, via the skill's slash command) invokes it, reading its instructions into context as part of that activation. Skills that are merely installed or listed as available, or whose content reaches the context without an activation (preloaded, hook-injected, or read as a plain file), are not counted. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

  - `claude_code_metrics: AnalyticsSkillClaudeCodeMetrics`

    Claude Code activity metrics for a single skill on a given day.

    - `distinct_session_skill_used_count: Optional[int]`

      Number of distinct Claude Code sessions in which the skill was used. A skill counts as used only when it is explicitly activated — the model (or the user, via the skill's slash command) invokes it, reading its instructions into context as part of that activation. Skills that are merely installed or listed as available, or whose content reaches the context without an activation (preloaded, hook-injected, or read as a plain file), are not counted. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

  - `cowork_metrics: AnalyticsSkillCoworkMetrics`

    Cowork activity metrics for a single skill on a given day.

    - `distinct_session_skill_used_count: Optional[int]`

      Number of distinct Cowork sessions in which the skill was used. A skill counts as used only when it is explicitly activated — the model (or the user, via the skill's slash command) invokes it, reading its instructions into context as part of that activation. Skills that are merely installed or listed as available, or whose content reaches the context without an activation (preloaded, hook-injected, or read as a plain file), are not counted. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

  - `currency: Optional[str]`

    Currency for this row's monetary fields (`estimated_overage_spend` and `attributed_list_price`), as an uppercase ISO-4217 code. Always "USD" when either amount is populated; null whenever both amounts are null.

  - `distinct_user_count: int`

    Number of distinct users who used the skill on the requested day, or, in date-range mode, over the requested window — recomputed as an exact distinct count over the window's per-member daily rows, never a sum of per-day values. A skill counts as used only when it is explicitly activated — the model (or the user, via the skill's slash command) invokes it, reading its instructions into context as part of that activation. Skills that are merely installed or listed as available, or whose content reaches the context without an activation (preloaded, hook-injected, or read as a plain file), are not counted.

  - `enable_count: Optional[int]`

    Distinct accounts that enabled this skill on the requested day (claude.ai only — the skill analog of plugin `install_count`). The count is org-wide: null when enable reporting is not enabled for this organization, or when the request scopes to `user_id` / `rbac_group_id` / `product` via `group_by[]` or `filter[]` (an org-wide count would be misleading on per-cut rows). A distinct count, not an event count: summing across days double-counts members who enable the skill on more than one day, so it is also null in date-range rollup mode (`starting_date`/`ending_date`).

  - `estimated_overage_spend: Optional[str]`

    Estimated overage spend attributed to this skill, as a decimal string in the minor unit of `currency` (cents for USD; "1250" is $12.50, fractional cents possible) — an allocation of each member's daily post-discount, pre-credit metered overage spend (the same cost basis as the organization's spend reporting and the Cost & Usage API, so per-skill figures are directly comparable; spend with no skill attribution — including any member-day without skill invocations — is not represented, so skill rows sum to at most those totals) across the skills the member used. Overage only: usage covered by included seat allowances bills nothing and allocates $0 here — see `attributed_list_price` for the funding-independent usage-value companion. Claude Code, Cowork, and Office Agent spend use request-level skill attribution; claude.ai chat spend is approximated proportionally to skill-invoking messages. An estimate, not a billing number — and the cost of the requests/messages that involved the skill, not the skill's incremental cost (the same request would still have cost something without the skill active). "0" means no overage spend was attributed; null when spend reporting is not enabled for this organization, on `office_agent` product cuts dated before 2026-06-18 (the Office Agent attribution data-start). Addable across days: date-range rollup mode (`starting_date`/`ending_date`) returns the window's sum. With `group_by[]=user_id` each row carries the user's own attributed spend. On `group_by[]` and `filter[]` shapes both amounts can total below the ungrouped value for the same skill over the same date or range: spend attributed to a member–skill pair with no counted usage on that day is excluded from those cuts.

  - `invocation_count: Optional[int]`

    Total number of times this skill was invoked on the requested day (the skill analog of plugin `invocation_count`). Unlike `distinct_user_count` — which answers '\# of users' — this is the true '# of uses'. A skill counts as used only when it is explicitly activated — the model (or the user, via the skill's slash command) invokes it, reading its instructions into context as part of that activation. Skills that are merely installed or listed as available, or whose content reaches the context without an activation (preloaded, hook-injected, or read as a plain file), are not counted. Null when invocation reporting is not enabled for this organization. Sum across a date range for total uses in the window — date-range rollup mode (`starting_date`/`ending_date`) returns this sum directly.

  - `office_metrics: AnalyticsSkillOfficeMetrics`

    Office Agent activity metrics for a single skill on a given day, broken out by Office product.

    - `excel: AnalyticsSkillOfficeProductMetrics`

      Office Agent activity metrics for a single skill on a given day within one Office product.

      - `distinct_session_skill_used_count: Optional[int]`

        Number of distinct Office Agent sessions in which the skill was used. A skill counts as used only when it is explicitly activated — the model (or the user, via the skill's slash command) invokes it, reading its instructions into context as part of that activation. Skills that are merely installed or listed as available, or whose content reaches the context without an activation (preloaded, hook-injected, or read as a plain file), are not counted. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `outlook: AnalyticsSkillOfficeProductMetrics`

      Office Agent activity metrics for a single skill on a given day within one Office product.

    - `powerpoint: AnalyticsSkillOfficeProductMetrics`

      Office Agent activity metrics for a single skill on a given day within one Office product.

    - `word: AnalyticsSkillOfficeProductMetrics`

      Office Agent activity metrics for a single skill on a given day within one Office product.

  - `share_status: Optional[Literal["organization", "private", "public"]]`

    Skill share status (claude.ai only): one of `private`, `organization`, or `public`. Null for skills used only in Claude Code or Office (no per-skill share-status concept) and when share-status reporting is not yet available for the organization. Filterable via `filter[]=share_status:{value}`.

    - `"organization"`

    - `"private"`

    - `"public"`

  - `skill_display_name: Optional[str]`

    Human-readable display name for rows whose `skill_name` is an opaque skill id (user/organization skill types and plugin-delivered skills, whose user-defined names usage reports generally withhold). Organization-shared skills and skills delivered by the organization's own plugins (its plugin marketplaces and its library) resolve; plugin skill names are shown without their 'plugin:' prefix. The literal 'unknown' bucket row gets a fixed 'Unknown skill' label. For a member's own skill (private or personal-plugin) it is null, except when the skill's owner used it from Claude Code or Cowork in the requested period: then it shows the name that client reported at the time. Apart from that, the names of members' own skills are not disclosed to analytics-key holders. Also null for Anthropic-provided plugin skills (not resolved), for an organization skill or plugin whose name can no longer be found (for example, one since deleted), when `skill_name` is already a display name, or when display-name resolution is not enabled for this organization.

  - `skill_name: str`

    Name of the skill

  - `chat_cowork_unified_metrics: Optional[AnalyticsSkillChatCoworkUnifiedMetrics]`

    Skill use recorded while members had Chat and Cowork unified (Cowork's features inside claude.ai chat) turned on, split into chat conversations and Cowork sessions. A count is null in date-range mode where it cannot be computed. Omitted from the response where Chat and Cowork unified is not available.

    - `chat: AnalyticsSkillChatCoworkUnifiedChatMetrics`

      A skill's use in chat conversations recorded while members had
      Chat and Cowork unified turned on.

      - `distinct_conversation_skill_used_count: Optional[int]`

        Same measure as `chat_metrics.distinct_conversation_skill_used_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

    - `sessions: AnalyticsSkillChatCoworkUnifiedSessionsMetrics`

      A skill's use in Cowork sessions recorded while members had Chat
      and Cowork unified turned on.

      - `distinct_session_skill_used_count: Optional[int]`

        Same measure as `cowork_metrics.distinct_session_skill_used_count`, for activity recorded while members had Chat and Cowork unified turned on. Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows where a distinct count cannot be computed.

  - `product: Optional[str]`

    Product that produced this row's activity: one of `chat`, `claude_code`, `cowork`, `office_agent`, or `chat_cowork_unified` (Chat and Cowork unified). These are the canonical Cost & Usage product names; an `office_agent` row's per-surface breakdown is in its `office_metrics`. On `/plugins` only `cowork`, `claude_code` and `chat_cowork_unified` occur (the only surfaces with plugin attribution); on `/artifacts` only `chat`, `claude_code`, `cowork` and `chat_cowork_unified` occur (the surfaces that create artifacts); `/apps/chat/projects` does not support the product dimension (a `product` entry in `group_by[]` or `filter[]` there is rejected). Present only when the request grouped by `product`.

  - `rbac_group_id: Optional[str]`

    Tagged RBAC group identifier (`rbac_group_...`), matching the spend-limits API spelling. Present only when the request grouped by `rbac_group_id`.

  - `rbac_group_name: Optional[str]`

    Resolved RBAC group display name, alongside `rbac_group_id` when name resolution is available. Null if the group has been deleted or its name could not be resolved; `rbac_group_id` remains the stable key.

  - `user_id: Optional[str]`

    Tagged user identifier (e.g. `user_...`). Present only when the request grouped by `user_id`.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.analytics.skills.list()
page = page.data[0]
print(page.rbac_group_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "attributed_list_price": "attributed_list_price",
      "chat_metrics": {
        "distinct_conversation_skill_used_count": 0
      },
      "claude_code_metrics": {
        "distinct_session_skill_used_count": 0
      },
      "cowork_metrics": {
        "distinct_session_skill_used_count": 0
      },
      "currency": "currency",
      "distinct_user_count": 0,
      "enable_count": 0,
      "estimated_overage_spend": "estimated_overage_spend",
      "invocation_count": 0,
      "office_metrics": {
        "excel": {
          "distinct_session_skill_used_count": 0
        },
        "outlook": {
          "distinct_session_skill_used_count": 0
        },
        "powerpoint": {
          "distinct_session_skill_used_count": 0
        },
        "word": {
          "distinct_session_skill_used_count": 0
        }
      },
      "share_status": "organization",
      "skill_display_name": "skill_display_name",
      "skill_name": "skill_name",
      "chat_cowork_unified_metrics": {
        "chat": {
          "distinct_conversation_skill_used_count": 0
        },
        "sessions": {
          "distinct_session_skill_used_count": 0
        }
      },
      "product": "product",
      "rbac_group_id": "rbac_group_id",
      "rbac_group_name": "rbac_group_name",
      "user_id": "user_id"
    }
  ],
  "next_page": "next_page"
}
```

## Organization › Analytics › Artifacts

### Get Artifact Activity

`organization.analytics.artifacts.list(**kwargs) -> SyncPageCursor[AnalyticsArtifactActivity]`

**GET** `/v1/organizations/analytics/artifacts`

Get artifact-creation activity for a given day, broken out by MIME type.

Returns the full (`artifact_type`, `is_shared`) cube for the organization;
`next_page` is null except for grouped queries, which paginate. The cube
can be broken out per product, per member, or per RBAC group via
`group_by[]`, and scoped via `filter[]`. Requires an API key with the
`read:analytics` scope.

#### Parameters

- `date: Union[null, null]` (query parameter)

  UTC date in YYYY-MM-DD format. The day to get artifact activity for. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

- `filter: Optional[Sequence[str]]` (query parameter)

  Filters as `dimension:value`, e.g. `filter[]=rbac_group_id:{id}`. Repeat the param for OR within a dimension and across dimensions for AND. Supported dimensions on this endpoint: `artifact_type`, `is_shared`, `product`, `rbac_group_id`, `user_id`. Value forms: `artifact_type` is a canonical artifact MIME type (e.g. `text/markdown`) or `other`; `is_shared` is `true` or `false`; `product` is `chat_cowork_unified`, `chat`, `claude_code`, or `cowork` (the surfaces that create artifacts); `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in responses and by the spend-limits API) or a bare group UUID, and matches users who held the group at any point during each covered UTC day (time-of-usage attribution); `user_id` takes a tagged user id (`user_...`), as emitted in responses. An unsupported dimension returns 400. At most 100 entries. `chat_cowork_unified` is accepted as a `product` value only where Chat and Cowork unified is available.

  maxItems: 100

- `group_by: Optional[List[AnalyticsArtifactGroupBy]]` (query parameter)

  Dimensions to break results out by: `product`, `user_id` and/or `rbac_group_id`. The ungrouped artifact-type cube is finite and returned in full; grouped queries multiply the cube and paginate via `next_page`. `product` takes the values `chat_cowork_unified`, `chat`, `claude_code`, or `cowork` (the surfaces that create artifacts). `rbac_group_id` attributes a user to every group they held at any point during the requested UTC day, so grouped rows are not an exclusive partition. At most 100 entries.

  maxItems: 100

  - `"product"`

  - `"rbac_group_id"`

  - `"user_id"`

- `limit: Optional[int]` (query parameter)

  Maximum rows to return (1-1000, default 100). The ungrouped artifact-type cube is finite and returned in full; `limit` is the page size only when `group_by[]` multiplies the cube.

  minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field. Only valid with `group_by[]` — the ungrouped cube is never paginated.

#### Returns

- `class AnalyticsArtifactActivity`

  Artifact-creation activity for one (`artifact_type`, `is_shared`) bucket
  on a given day.

  Artifacts form a small finite cube — the canonical MIME type (8 values incl.
  `other`) crossed with shared-vs-private — so the response is the full set of
  non-empty buckets, not a ranked/paginated list. Claude Code and Cowork
  artifacts report under `text/html` and are counted from 2026-08-17
  onward; earlier days contain claude.ai chat artifacts only. With
  `group_by[]=product` / `user_id` / `rbac_group_id` each row is further
  split by the flat group keys and counts are scoped to that cut.

  - `artifact_type: str`

    Canonical artifact MIME type (e.g. `text/markdown`, `application/vnd.ant.react`, `image/svg+xml`), or `other`. Claude Code and Cowork artifacts report as `text/html`.

  - `artifacts_created_count: int`

    Number of artifacts created in this bucket on the requested day

  - `distinct_user_count: int`

    Number of distinct users who created artifacts in this bucket on the requested day

  - `is_shared: bool`

    Whether the artifacts in this bucket have ever been shared (a Claude Code / Cowork artifact is shared once anyone beyond its creator may open it: named members, the whole organization, or anyone with the link).

  - `published_artifacts_created_count: int`

    Number of those artifacts that have been published (for Claude Code / Cowork artifacts: open to anyone with the link); never exceeds `artifacts_created_count`

  - `product: Optional[str]`

    Product that produced this row's activity: one of `chat`, `claude_code`, `cowork`, `office_agent`, or `chat_cowork_unified` (Chat and Cowork unified). These are the canonical Cost & Usage product names; an `office_agent` row's per-surface breakdown is in its `office_metrics`. On `/plugins` only `cowork`, `claude_code` and `chat_cowork_unified` occur (the only surfaces with plugin attribution); on `/artifacts` only `chat`, `claude_code`, `cowork` and `chat_cowork_unified` occur (the surfaces that create artifacts); `/apps/chat/projects` does not support the product dimension (a `product` entry in `group_by[]` or `filter[]` there is rejected). Present only when the request grouped by `product`.

  - `rbac_group_id: Optional[str]`

    Tagged RBAC group identifier (`rbac_group_...`), matching the spend-limits API spelling. Present only when the request grouped by `rbac_group_id`.

  - `rbac_group_name: Optional[str]`

    Resolved RBAC group display name, alongside `rbac_group_id` when name resolution is available. Null if the group has been deleted or its name could not be resolved; `rbac_group_id` remains the stable key.

  - `user_id: Optional[str]`

    Tagged user identifier (e.g. `user_...`). Present only when the request grouped by `user_id`.

#### Example

```python
import os
from datetime import date
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.analytics.artifacts.list(
    date=date.fromisoformat("2019-12-27"),
)
page = page.data[0]
print(page.rbac_group_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "artifact_type": "artifact_type",
      "artifacts_created_count": 0,
      "distinct_user_count": 0,
      "is_shared": true,
      "published_artifacts_created_count": 0,
      "product": "product",
      "rbac_group_id": "rbac_group_id",
      "rbac_group_name": "rbac_group_name",
      "user_id": "user_id"
    }
  ],
  "next_page": "next_page"
}
```

## Organization › Spend Limits › Effective

### List Effective Spend Limits

`organization.spend_limits.effective.list(**kwargs) -> SyncPageCursor[SpendSummary]`

**GET** `/v1/organizations/spend_limits/effective`

List each member's effective spend limit and period-to-date spend.

Returns one row per (member, period) the member resolves a spend limit
for, with the `source` scope the spend limit was inherited from.
Paginates by member, so a member's periods never split across pages.
Supported for Claude Enterprise organizations only, not for Claude Console
organizations.

#### Parameters

- `limit: Optional[int]` (query parameter)

  Maximum number of members per page. A member's period rows never split across pages, so a page may carry more rows than this. Defaults to `20`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field.

- `period: Optional[List[SpendLimitPeriod]]` (query parameter)

  Restrict the report to these limit periods. Omit to return one row per period each member resolves a spend limit for.

  maxItems: 3

  - `"daily"`

  - `"monthly"`

  - `"weekly"`

- `user_ids: Optional[Sequence[str]]` (query parameter)

  Restrict the report to these members, by tagged user ID (`user_...`). At most 100 entries.

  maxItems: 100

#### Returns

- `class SpendSummary`

  Per-member effective-limit report row (`GET /spend_limits/effective`).

  - `actor: Actor`

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

      - `type: Literal["user_actor"]`

        Actor type. Always `user_actor`.

        default: user_actor

      - `deleted: bool`

        True only when the underlying account has been deleted.

        default: false

      - `email_address: Optional[str]`

        The user's email address. Null when the account is unavailable or has been deleted.

      - `name: Optional[str]`

        The user's current display name. Null when the account is unavailable, has been deleted, or has no name set.

      - `user_id: str`

        Tagged ID of the user.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `amount: Optional[str]`

    Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

  - `currency: str`

    ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

  - `period: SpendLimitPeriod`

    Period this row's effective limit and spend are reported for.

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `period_to_date_spend: str`

    The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

  - `scope: Scope`

    - `class SpendLimitUserScope`

      Scope selecting a single member of the organization.

      - `type: Literal["user"]`

        Scope type. Always `user` for this scope.

        default: user

      - `user_id: str`

        Tagged ID of the member the spend limit applies to.

    - `class SpendLimitSeatTierScope`

      - `type: Literal["seat_tier"]`

        default: seat_tier

      - `seat_tier: str`

    - `class SpendLimitRBACGroupScope`

      - `type: Literal["rbac_group"]`

        default: rbac_group

      - `rbac_group_id: str`

    - `class SpendLimitOrganizationServiceScope`

      - `type: Literal["organization_service"]`

        default: organization_service

      - `service: str`

    - `class SpendLimitOrganizationScope`

      - `type: Literal["organization"]`

        default: organization

    - `class SpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

      - `type: Literal["workspace"]`

        Scope type. Always `workspace` for this scope.

        default: workspace

      - `workspace_id: str`

        Tagged ID of the workspace the spend limit applies to.

    - `class SpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

      - `type: Literal["usage_tier"]`

        Scope type. Always `usage_tier` for this scope.

        default: usage_tier

  - `source: Source`

    - `class SpendLimitUserScope`

      Scope selecting a single member of the organization.

    - `class SpendLimitSeatTierScope`

    - `class SpendLimitRBACGroupScope`

    - `class SpendLimitOrganizationServiceScope`

    - `class SpendLimitOrganizationScope`

    - `class SpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

    - `class SpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

  - `spend_limit_id: str`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.spend_limits.effective.list()
page = page.data[0]
print(page.spend_limit_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "actor": {
        "deleted": true,
        "email_address": "email_address",
        "name": "name",
        "type": "user_actor",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
      },
      "amount": "50000",
      "currency": "USD",
      "period": "daily",
      "period_to_date_spend": "12050.5",
      "scope": {
        "type": "user",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
      },
      "source": {
        "type": "user",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
      },
      "spend_limit_id": "spend_limit_id"
    }
  ],
  "next_page": "next_page"
}
```

## Organization › Spend Limits › Increase Requests

### List Spend Limit Increase Requests

`organization.spend_limits.increase_requests.list(**kwargs) -> SyncPageCursor[SpendLimitIncreaseRequest]`

**GET** `/v1/organizations/spend_limit_increase_requests`

List spend limit increase requests, most recent first.

Pending requests include a live `spend_summary` for the requester.
Requests whose requester is no longer a member are excluded.

#### Parameters

- `actor_ids: Optional[Sequence[str]]` (query parameter)

  Filter by requester, as `user_...` tagged IDs.

- `limit: Optional[int]` (query parameter)

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

- `status: Optional[List[SpendLimitIncreaseRequestStatus]]` (query parameter)

  Filter by status. Omit to return all.

  - `"approved"`

  - `"denied"`

  - `"pending"`

#### Returns

- `class SpendLimitIncreaseRequest`

  - `type: Literal["spend_limit_increase_request"]`

    default: spend_limit_increase_request

  - `id: str`

  - `actor: SpendLimitIncreaseRequestActor`

    Who submitted the increase request.

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

      - `type: Literal["user_actor"]`

        Actor type. Always `user_actor`.

        default: user_actor

      - `deleted: bool`

        True only when the underlying account has been deleted.

        default: false

      - `email_address: Optional[str]`

        The user's email address. Null when the account is unavailable or has been deleted.

      - `name: Optional[str]`

        The user's current display name. Null when the account is unavailable, has been deleted, or has no name set.

      - `user_id: str`

        Tagged ID of the user.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `created_at: datetime`

    format: date-time

  - `period: SpendLimitPeriod`

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `resolved_at: Optional[datetime]`

    format: date-time

  - `resolved_by: Optional[SpendLimitIncreaseRequestResolvedBy]`

    Who approved or denied the increase request.

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

  - `spend_summary: Optional[SpendSummary]`

    Per-member effective-limit report row (`GET /spend_limits/effective`).

    - `actor: Actor`

      - `class SpendLimitUserActor`

        A user within the organization. `name` and `email_address` are
        null when the underlying account is unavailable or has been deleted;
        `deleted` is true only for deleted accounts.

      - `class SpendLimitScopedAPIKeyActor`

        A scoped Admin API key acting on behalf of the organization.

    - `amount: Optional[str]`

      Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

    - `period: SpendLimitPeriod`

      Period this row's effective limit and spend are reported for.

    - `period_to_date_spend: str`

      The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

    - `scope: Scope`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

        - `type: Literal["user"]`

          Scope type. Always `user` for this scope.

          default: user

        - `user_id: str`

          Tagged ID of the member the spend limit applies to.

      - `class SpendLimitSeatTierScope`

        - `type: Literal["seat_tier"]`

          default: seat_tier

        - `seat_tier: str`

      - `class SpendLimitRBACGroupScope`

        - `type: Literal["rbac_group"]`

          default: rbac_group

        - `rbac_group_id: str`

      - `class SpendLimitOrganizationServiceScope`

        - `type: Literal["organization_service"]`

          default: organization_service

        - `service: str`

      - `class SpendLimitOrganizationScope`

        - `type: Literal["organization"]`

          default: organization

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

        - `type: Literal["workspace"]`

          Scope type. Always `workspace` for this scope.

          default: workspace

        - `workspace_id: str`

          Tagged ID of the workspace the spend limit applies to.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

        - `type: Literal["usage_tier"]`

          Scope type. Always `usage_tier` for this scope.

          default: usage_tier

    - `source: Source`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class SpendLimitSeatTierScope`

      - `class SpendLimitRBACGroupScope`

      - `class SpendLimitOrganizationServiceScope`

      - `class SpendLimitOrganizationScope`

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `spend_limit_id: str`

  - `status: SpendLimitIncreaseRequestStatus`

    - `"approved"`

    - `"denied"`

    - `"pending"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.spend_limits.increase_requests.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "id",
      "actor": {
        "deleted": true,
        "email_address": "email_address",
        "name": "name",
        "type": "user_actor",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
      },
      "created_at": "2019-12-27T18:11:19.117Z",
      "period": "daily",
      "resolved_at": "2019-12-27T18:11:19.117Z",
      "resolved_by": {
        "deleted": true,
        "email_address": "email_address",
        "name": "name",
        "type": "user_actor",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
      },
      "spend_summary": {
        "actor": {
          "deleted": true,
          "email_address": "email_address",
          "name": "name",
          "type": "user_actor",
          "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
        },
        "amount": "50000",
        "currency": "USD",
        "period": "daily",
        "period_to_date_spend": "12050.5",
        "scope": {
          "type": "user",
          "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
        },
        "source": {
          "type": "user",
          "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
        },
        "spend_limit_id": "spend_limit_id"
      },
      "status": "approved",
      "type": "spend_limit_increase_request"
    }
  ],
  "next_page": "next_page"
}
```

### Get Spend Limit Increase Request

`organization.spend_limits.increase_requests.retrieve(spend_limit_increase_request_id) -> SpendLimitIncreaseRequest`

**GET** `/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}`

Retrieve a spend limit increase request.

While `pending`, the response includes a live `spend_summary` for the
requester at the request's period.

#### Parameters

- `spend_limit_increase_request_id: str` (path parameter)

  ID of the spend limit increase request.

#### Returns

- `class SpendLimitIncreaseRequest`

  - `type: Literal["spend_limit_increase_request"]`

    default: spend_limit_increase_request

  - `id: str`

  - `actor: SpendLimitIncreaseRequestActor`

    Who submitted the increase request.

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

      - `type: Literal["user_actor"]`

        Actor type. Always `user_actor`.

        default: user_actor

      - `deleted: bool`

        True only when the underlying account has been deleted.

        default: false

      - `email_address: Optional[str]`

        The user's email address. Null when the account is unavailable or has been deleted.

      - `name: Optional[str]`

        The user's current display name. Null when the account is unavailable, has been deleted, or has no name set.

      - `user_id: str`

        Tagged ID of the user.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `created_at: datetime`

    format: date-time

  - `period: SpendLimitPeriod`

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `resolved_at: Optional[datetime]`

    format: date-time

  - `resolved_by: Optional[SpendLimitIncreaseRequestResolvedBy]`

    Who approved or denied the increase request.

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

  - `spend_summary: Optional[SpendSummary]`

    Per-member effective-limit report row (`GET /spend_limits/effective`).

    - `actor: Actor`

      - `class SpendLimitUserActor`

        A user within the organization. `name` and `email_address` are
        null when the underlying account is unavailable or has been deleted;
        `deleted` is true only for deleted accounts.

      - `class SpendLimitScopedAPIKeyActor`

        A scoped Admin API key acting on behalf of the organization.

    - `amount: Optional[str]`

      Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

    - `period: SpendLimitPeriod`

      Period this row's effective limit and spend are reported for.

    - `period_to_date_spend: str`

      The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

    - `scope: Scope`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

        - `type: Literal["user"]`

          Scope type. Always `user` for this scope.

          default: user

        - `user_id: str`

          Tagged ID of the member the spend limit applies to.

      - `class SpendLimitSeatTierScope`

        - `type: Literal["seat_tier"]`

          default: seat_tier

        - `seat_tier: str`

      - `class SpendLimitRBACGroupScope`

        - `type: Literal["rbac_group"]`

          default: rbac_group

        - `rbac_group_id: str`

      - `class SpendLimitOrganizationServiceScope`

        - `type: Literal["organization_service"]`

          default: organization_service

        - `service: str`

      - `class SpendLimitOrganizationScope`

        - `type: Literal["organization"]`

          default: organization

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

        - `type: Literal["workspace"]`

          Scope type. Always `workspace` for this scope.

          default: workspace

        - `workspace_id: str`

          Tagged ID of the workspace the spend limit applies to.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

        - `type: Literal["usage_tier"]`

          Scope type. Always `usage_tier` for this scope.

          default: usage_tier

    - `source: Source`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class SpendLimitSeatTierScope`

      - `class SpendLimitRBACGroupScope`

      - `class SpendLimitOrganizationServiceScope`

      - `class SpendLimitOrganizationScope`

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `spend_limit_id: str`

  - `status: SpendLimitIncreaseRequestStatus`

    - `"approved"`

    - `"denied"`

    - `"pending"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
spend_limit_increase_request = (
    client.organization.spend_limits.increase_requests.retrieve(
        "spend_limit_increase_request_id",
    )
)
print(spend_limit_increase_request.id)
```

##### Response (200)

```json
{
  "id": "id",
  "actor": {
    "deleted": true,
    "email_address": "email_address",
    "name": "name",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "created_at": "2019-12-27T18:11:19.117Z",
  "period": "daily",
  "resolved_at": "2019-12-27T18:11:19.117Z",
  "resolved_by": {
    "deleted": true,
    "email_address": "email_address",
    "name": "name",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "spend_summary": {
    "actor": {
      "deleted": true,
      "email_address": "email_address",
      "name": "name",
      "type": "user_actor",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "amount": "50000",
    "currency": "USD",
    "period": "daily",
    "period_to_date_spend": "12050.5",
    "scope": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "source": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "spend_limit_id": "spend_limit_id"
  },
  "status": "approved",
  "type": "spend_limit_increase_request"
}
```

### Approve Spend Limit Increase Request

`organization.spend_limits.increase_requests.approve(spend_limit_increase_request_id, **kwargs) -> IncreaseRequestApproveResponse`

**POST** `/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}/approve`

Approve a pending spend limit increase request.

Writes a per-user spend limit at `amount` for the requester and
transitions the request to `approved`. `period` defaults to the period
the member was blocked on. Anthropic emails the requester unless
`suppress_notification` is set.

#### Parameters

- `spend_limit_increase_request_id: str` (path parameter)

  ID of the spend limit increase request.

- `amount: str`

  New per-user spend limit as a non-negative integer decimal string (minor units).

- `period: Optional[SpendLimitPeriod]`

  - `"daily"`

  - `"monthly"`

  - `"weekly"`

- `suppress_notification: Optional[bool]`

#### Returns

- `class IncreaseRequestApproveResponse`

  - `type: Literal["spend_limit_increase_request"]`

    default: spend_limit_increase_request

  - `id: str`

  - `actor: SpendLimitIncreaseRequestActor`

    Who submitted the increase request.

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

      - `type: Literal["user_actor"]`

        Actor type. Always `user_actor`.

        default: user_actor

      - `deleted: bool`

        True only when the underlying account has been deleted.

        default: false

      - `email_address: Optional[str]`

        The user's email address. Null when the account is unavailable or has been deleted.

      - `name: Optional[str]`

        The user's current display name. Null when the account is unavailable, has been deleted, or has no name set.

      - `user_id: str`

        Tagged ID of the user.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `created_at: datetime`

    format: date-time

  - `period: SpendLimitPeriod`

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `resolved_at: Optional[datetime]`

    format: date-time

  - `resolved_by: Optional[SpendLimitIncreaseRequestResolvedBy]`

    Who approved or denied the increase request.

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

  - `spend_limit: Optional[SpendLimit]`

    A configured spend limit: a cap on metered spend for one scope and period.

    - `type: Literal["spend_limit"]`

      Object type. Always `spend_limit`.

      default: spend_limit

    - `id: str`

      Unique tagged ID of the spend limit (`spl_...`).

    - `amount: Optional[str]`

      Limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD): "50000" is $500.00. `null` means no numeric cap is configured at this scope — see the effective report for whether a limit applies.

    - `created_at: datetime`

      RFC 3339 datetime at which the spend limit was created.

      format: date-time

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount`.

    - `is_enabled: bool`

      Read-only. `false` when extra usage is switched off for this organization (`organization` limit); `amount` is kept and applies again when it's switched back on. Always `true` for other limits.

    - `period: SpendLimitPeriod`

      Length of the window the limit resets over. `amount` caps spend within each period.

    - `scope: Scope`

      What the limit applies to. A tagged union on `type`; each variant carries the identifier for its scope.

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

        - `type: Literal["user"]`

          Scope type. Always `user` for this scope.

          default: user

        - `user_id: str`

          Tagged ID of the member the spend limit applies to.

      - `class SpendLimitSeatTierScope`

        - `type: Literal["seat_tier"]`

          default: seat_tier

        - `seat_tier: str`

      - `class SpendLimitRBACGroupScope`

        - `type: Literal["rbac_group"]`

          default: rbac_group

        - `rbac_group_id: str`

      - `class SpendLimitOrganizationServiceScope`

        - `type: Literal["organization_service"]`

          default: organization_service

        - `service: str`

      - `class SpendLimitOrganizationScope`

        - `type: Literal["organization"]`

          default: organization

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

        - `type: Literal["workspace"]`

          Scope type. Always `workspace` for this scope.

          default: workspace

        - `workspace_id: str`

          Tagged ID of the workspace the spend limit applies to.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

        - `type: Literal["usage_tier"]`

          Scope type. Always `usage_tier` for this scope.

          default: usage_tier

    - `updated_at: datetime`

      RFC 3339 datetime at which the spend limit was last modified.

      format: date-time

  - `spend_summary: Optional[SpendSummary]`

    Per-member effective-limit report row (`GET /spend_limits/effective`).

    - `actor: Actor`

      - `class SpendLimitUserActor`

        A user within the organization. `name` and `email_address` are
        null when the underlying account is unavailable or has been deleted;
        `deleted` is true only for deleted accounts.

      - `class SpendLimitScopedAPIKeyActor`

        A scoped Admin API key acting on behalf of the organization.

    - `amount: Optional[str]`

      Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

    - `period: SpendLimitPeriod`

      Period this row's effective limit and spend are reported for.

    - `period_to_date_spend: str`

      The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

    - `scope: Scope`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class SpendLimitSeatTierScope`

      - `class SpendLimitRBACGroupScope`

      - `class SpendLimitOrganizationServiceScope`

      - `class SpendLimitOrganizationScope`

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `source: Source`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class SpendLimitSeatTierScope`

      - `class SpendLimitRBACGroupScope`

      - `class SpendLimitOrganizationServiceScope`

      - `class SpendLimitOrganizationScope`

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `spend_limit_id: str`

  - `status: SpendLimitIncreaseRequestStatus`

    - `"approved"`

    - `"denied"`

    - `"pending"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
response = client.organization.spend_limits.increase_requests.approve(
    spend_limit_increase_request_id="spend_limit_increase_request_id",
    amount="50000",
)
print(response.id)
```

##### Response (200)

```json
{
  "id": "id",
  "actor": {
    "deleted": true,
    "email_address": "email_address",
    "name": "name",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "created_at": "2019-12-27T18:11:19.117Z",
  "period": "daily",
  "resolved_at": "2019-12-27T18:11:19.117Z",
  "resolved_by": {
    "deleted": true,
    "email_address": "email_address",
    "name": "name",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "spend_limit": {
    "id": "id",
    "amount": "50000",
    "created_at": "2019-12-27T18:11:19.117Z",
    "currency": "USD",
    "is_enabled": true,
    "period": "daily",
    "scope": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "type": "spend_limit",
    "updated_at": "2019-12-27T18:11:19.117Z"
  },
  "spend_summary": {
    "actor": {
      "deleted": true,
      "email_address": "email_address",
      "name": "name",
      "type": "user_actor",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "amount": "50000",
    "currency": "USD",
    "period": "daily",
    "period_to_date_spend": "12050.5",
    "scope": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "source": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "spend_limit_id": "spend_limit_id"
  },
  "status": "approved",
  "type": "spend_limit_increase_request"
}
```

### Deny Spend Limit Increase Request

`organization.spend_limits.increase_requests.deny(spend_limit_increase_request_id, **kwargs) -> SpendLimitIncreaseRequest`

**POST** `/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}/deny`

Deny a pending spend limit increase request.

Idempotent on `denied`; denying an already-`approved` request returns
400. Anthropic emails the requester unless `suppress_notification` is set.

#### Parameters

- `spend_limit_increase_request_id: str` (path parameter)

  ID of the spend limit increase request.

- `suppress_notification: Optional[bool]`

#### Returns

- `class SpendLimitIncreaseRequest`

  - `type: Literal["spend_limit_increase_request"]`

    default: spend_limit_increase_request

  - `id: str`

  - `actor: SpendLimitIncreaseRequestActor`

    Who submitted the increase request.

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

      - `type: Literal["user_actor"]`

        Actor type. Always `user_actor`.

        default: user_actor

      - `deleted: bool`

        True only when the underlying account has been deleted.

        default: false

      - `email_address: Optional[str]`

        The user's email address. Null when the account is unavailable or has been deleted.

      - `name: Optional[str]`

        The user's current display name. Null when the account is unavailable, has been deleted, or has no name set.

      - `user_id: str`

        Tagged ID of the user.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `created_at: datetime`

    format: date-time

  - `period: SpendLimitPeriod`

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `resolved_at: Optional[datetime]`

    format: date-time

  - `resolved_by: Optional[SpendLimitIncreaseRequestResolvedBy]`

    Who approved or denied the increase request.

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

  - `spend_summary: Optional[SpendSummary]`

    Per-member effective-limit report row (`GET /spend_limits/effective`).

    - `actor: Actor`

      - `class SpendLimitUserActor`

        A user within the organization. `name` and `email_address` are
        null when the underlying account is unavailable or has been deleted;
        `deleted` is true only for deleted accounts.

      - `class SpendLimitScopedAPIKeyActor`

        A scoped Admin API key acting on behalf of the organization.

    - `amount: Optional[str]`

      Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

    - `period: SpendLimitPeriod`

      Period this row's effective limit and spend are reported for.

    - `period_to_date_spend: str`

      The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

    - `scope: Scope`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

        - `type: Literal["user"]`

          Scope type. Always `user` for this scope.

          default: user

        - `user_id: str`

          Tagged ID of the member the spend limit applies to.

      - `class SpendLimitSeatTierScope`

        - `type: Literal["seat_tier"]`

          default: seat_tier

        - `seat_tier: str`

      - `class SpendLimitRBACGroupScope`

        - `type: Literal["rbac_group"]`

          default: rbac_group

        - `rbac_group_id: str`

      - `class SpendLimitOrganizationServiceScope`

        - `type: Literal["organization_service"]`

          default: organization_service

        - `service: str`

      - `class SpendLimitOrganizationScope`

        - `type: Literal["organization"]`

          default: organization

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

        - `type: Literal["workspace"]`

          Scope type. Always `workspace` for this scope.

          default: workspace

        - `workspace_id: str`

          Tagged ID of the workspace the spend limit applies to.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

        - `type: Literal["usage_tier"]`

          Scope type. Always `usage_tier` for this scope.

          default: usage_tier

    - `source: Source`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class SpendLimitSeatTierScope`

      - `class SpendLimitRBACGroupScope`

      - `class SpendLimitOrganizationServiceScope`

      - `class SpendLimitOrganizationScope`

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `spend_limit_id: str`

  - `status: SpendLimitIncreaseRequestStatus`

    - `"approved"`

    - `"denied"`

    - `"pending"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
spend_limit_increase_request = client.organization.spend_limits.increase_requests.deny(
    spend_limit_increase_request_id="spend_limit_increase_request_id",
)
print(spend_limit_increase_request.id)
```

##### Response (200)

```json
{
  "id": "id",
  "actor": {
    "deleted": true,
    "email_address": "email_address",
    "name": "name",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "created_at": "2019-12-27T18:11:19.117Z",
  "period": "daily",
  "resolved_at": "2019-12-27T18:11:19.117Z",
  "resolved_by": {
    "deleted": true,
    "email_address": "email_address",
    "name": "name",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "spend_summary": {
    "actor": {
      "deleted": true,
      "email_address": "email_address",
      "name": "name",
      "type": "user_actor",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "amount": "50000",
    "currency": "USD",
    "period": "daily",
    "period_to_date_spend": "12050.5",
    "scope": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "source": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "spend_limit_id": "spend_limit_id"
  },
  "status": "approved",
  "type": "spend_limit_increase_request"
}
```

## Organization › RBAC Groups

### Create RBAC Group

`organization.rbac_groups.create(**kwargs) -> RBACGroup`

**POST** `/v1/organizations/rbac_groups`

Create an RBAC Group in the Claude Enterprise tenant. Groups created via the API have source type `"direct"`.

The RBAC Groups API is available to Claude Enterprise organizations only.

#### Parameters

- `name: str`

  Name of the RBAC Group. Not uniqueness-enforced.

  minLength: 1, maxLength: 255

#### Returns

- `class RBACGroup`

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

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
rbac_group = client.organization.rbac_groups.create(
    name="Engineering",
)
print(rbac_group.id)
```

##### Response (200)

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

### List RBAC Groups

`organization.rbac_groups.list(**kwargs) -> SyncPageCursor[RBACGroup]`

**GET** `/v1/organizations/rbac_groups`

List RBAC Groups in the Claude Enterprise tenant.

The RBAC Groups API is available to Claude Enterprise organizations only.

#### Parameters

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

#### Returns

- `class RBACGroup`

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

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.rbac_groups.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
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
  ],
  "has_more": false,
  "next_page": "eyJjdXJzb3IiOiAicmJhY19ncm91cF8wMSJ9"
}
```

### Get RBAC Group

`organization.rbac_groups.retrieve(rbac_group_id) -> RBACGroup`

**GET** `/v1/organizations/rbac_groups/{rbac_group_id}`

Retrieve an RBAC Group by ID.

The RBAC Groups API is available to Claude Enterprise organizations only.

#### Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

#### Returns

- `class RBACGroup`

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

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
rbac_group = client.organization.rbac_groups.retrieve(
    "rbac_group_id",
)
print(rbac_group.id)
```

##### Response (200)

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

### Update RBAC Group

`organization.rbac_groups.update(rbac_group_id, **kwargs) -> RBACGroup`

**POST** `/v1/organizations/rbac_groups/{rbac_group_id}`

Update an RBAC Group's name. Groups provisioned by an identity provider (source type `"scim"`) cannot be modified via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

#### Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

- `name: Optional[str]`

  Name of the RBAC Group. Not uniqueness-enforced.

  minLength: 1, maxLength: 255

#### Returns

- `class RBACGroup`

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

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
rbac_group = client.organization.rbac_groups.update(
    rbac_group_id="rbac_group_id",
)
print(rbac_group.id)
```

##### Response (200)

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

### Delete RBAC Group

`organization.rbac_groups.delete(rbac_group_id) -> DeletedRBACGroup`

**DELETE** `/v1/organizations/rbac_groups/{rbac_group_id}`

Delete an RBAC Group. Groups provisioned by an identity provider (source type `"scim"`) cannot be deleted via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

#### Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

#### Returns

- `class DeletedRBACGroup`

  - `type: Literal["rbac_group_deleted"]`

    Deleted object type.

    For RBAC Groups, this is always `"rbac_group_deleted"`.

    default: rbac_group_deleted

  - `id: str`

    ID of the RBAC Group.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
deleted_rbac_group = client.organization.rbac_groups.delete(
    "rbac_group_id",
)
print(deleted_rbac_group.id)
```

##### Response (200)

```json
{
  "id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "type": "rbac_group_deleted"
}
```

## Organization › RBAC Groups › Members

### List RBAC Group Members

`organization.rbac_groups.members.list(rbac_group_id, **kwargs) -> SyncPageCursor[RBACGroupMember]`

**GET** `/v1/organizations/rbac_groups/{rbac_group_id}/members`

List members of an RBAC Group.

The RBAC Groups API is available to Claude Enterprise organizations only.

#### Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

#### Returns

- `class RBACGroupMember`

  - `type: Literal["rbac_group_member"]`

    Object type.

    For RBAC Group Members, this is always `"rbac_group_member"`.

    default: rbac_group_member

  - `created_at: datetime`

    RFC 3339 timestamp of when the User was added to the RBAC Group.

    format: date-time

  - `email: str`

    Email of the User.

  - `rbac_group_id: str`

    ID of the RBAC Group.

  - `user_id: str`

    ID of the User.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.rbac_groups.members.list(
    rbac_group_id="rbac_group_id",
)
page = page.data[0]
print(page.rbac_group_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "created_at": "2024-10-30T23:58:27.427722Z",
      "email": "user@emaildomain.com",
      "rbac_group_id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
      "type": "rbac_group_member",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    }
  ],
  "has_more": false,
  "next_page": "eyJjdXJzb3IiOiAicmJhY19ncm91cF8wMSJ9"
}
```

### Add RBAC Group Member

`organization.rbac_groups.members.add(rbac_group_id, **kwargs) -> RBACGroupMember`

**POST** `/v1/organizations/rbac_groups/{rbac_group_id}/members`

Add a User to an RBAC Group. Membership of groups provisioned by an identity provider (source type `"scim"`) cannot be modified via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

#### Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

- `user_id: str`

  ID of the User.

#### Returns

- `class RBACGroupMember`

  - `type: Literal["rbac_group_member"]`

    Object type.

    For RBAC Group Members, this is always `"rbac_group_member"`.

    default: rbac_group_member

  - `created_at: datetime`

    RFC 3339 timestamp of when the User was added to the RBAC Group.

    format: date-time

  - `email: str`

    Email of the User.

  - `rbac_group_id: str`

    ID of the RBAC Group.

  - `user_id: str`

    ID of the User.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
rbac_group_member = client.organization.rbac_groups.members.add(
    rbac_group_id="rbac_group_id",
    user_id="user_01WxYzAbCdEfGhJkMnPqRsTu",
)
print(rbac_group_member.rbac_group_id)
```

##### Response (200)

```json
{
  "created_at": "2024-10-30T23:58:27.427722Z",
  "email": "user@emaildomain.com",
  "rbac_group_id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "type": "rbac_group_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
}
```

### Remove RBAC Group Member

`organization.rbac_groups.members.remove(user_id, **kwargs) -> DeletedRBACGroupMember`

**DELETE** `/v1/organizations/rbac_groups/{rbac_group_id}/members/{user_id}`

Remove a User from an RBAC Group. Membership of groups provisioned by an identity provider (source type `"scim"`) cannot be modified via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

#### Parameters

- `rbac_group_id: str` (path parameter)

  ID of the RBAC Group.

- `user_id: str` (path parameter)

  ID of the User.

#### Returns

- `class DeletedRBACGroupMember`

  - `type: Literal["rbac_group_member_deleted"]`

    Deleted object type. For RBAC Group Members, this is always `"rbac_group_member_deleted"`.

    default: rbac_group_member_deleted

  - `rbac_group_id: str`

    ID of the RBAC Group.

  - `user_id: str`

    ID of the User.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
deleted_rbac_group_member = client.organization.rbac_groups.members.remove(
    user_id="user_id",
    rbac_group_id="rbac_group_id",
)
print(deleted_rbac_group_member.rbac_group_id)
```

##### Response (200)

```json
{
  "rbac_group_id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "type": "rbac_group_member_deleted",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
}
```

## Organization › RBAC Roles

### List RBAC Roles

`organization.rbac_roles.list(**kwargs) -> SyncPageCursor[RBACRole]`

**GET** `/v1/organizations/rbac_roles`

List RBAC Roles in the organization.

The RBAC Roles API is available to Claude Enterprise organizations only.

#### Parameters

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

#### Returns

- `class RBACRole`

  - `type: Literal["rbac_role"]`

    Object type.

    For RBAC Roles, this is always `"rbac_role"`.

    default: rbac_role

  - `id: str`

    ID of the RBAC Role.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the RBAC Role was created.

    format: date-time

  - `display_name: str`

    Name of the RBAC Role. For a role created by Anthropic, this is Anthropic's name for the access that the role grants. Anthropic may change this name, so to keep a lasting reference to a role, store its `id`.

  - `updated_at: datetime`

    RFC 3339 datetime string indicating when the RBAC Role was last updated.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.rbac_roles.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "rbac_role_016J8xVtKpDq3Wy9ZmN2hR4s",
      "created_at": "2024-10-30T23:58:27.427722Z",
      "display_name": "Project Editor",
      "type": "rbac_role",
      "updated_at": "2024-10-30T23:58:27.427722Z"
    }
  ],
  "has_more": true,
  "next_page": "eyJjdXJzb3IiOiAicmJhY19yb2xlXzAxIn0"
}
```

### Get RBAC Role

`organization.rbac_roles.retrieve(rbac_role_id) -> RBACRole`

**GET** `/v1/organizations/rbac_roles/{rbac_role_id}`

Retrieve an RBAC Role by ID.

The RBAC Roles API is available to Claude Enterprise organizations only.

#### Parameters

- `rbac_role_id: str` (path parameter)

  ID of the RBAC Role.

#### Returns

- `class RBACRole`

  - `type: Literal["rbac_role"]`

    Object type.

    For RBAC Roles, this is always `"rbac_role"`.

    default: rbac_role

  - `id: str`

    ID of the RBAC Role.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the RBAC Role was created.

    format: date-time

  - `display_name: str`

    Name of the RBAC Role. For a role created by Anthropic, this is Anthropic's name for the access that the role grants. Anthropic may change this name, so to keep a lasting reference to a role, store its `id`.

  - `updated_at: datetime`

    RFC 3339 datetime string indicating when the RBAC Role was last updated.

    format: date-time

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
rbac_role = client.organization.rbac_roles.retrieve(
    "rbac_role_id",
)
print(rbac_role.id)
```

##### Response (200)

```json
{
  "id": "rbac_role_016J8xVtKpDq3Wy9ZmN2hR4s",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "display_name": "Project Editor",
  "type": "rbac_role",
  "updated_at": "2024-10-30T23:58:27.427722Z"
}
```

## Organization › RBAC Roles › Permissions

### List RBAC Role Permissions

`organization.rbac_roles.permissions.list(rbac_role_id, **kwargs) -> SyncPageCursor[RBACRolePermission]`

**GET** `/v1/organizations/rbac_roles/{rbac_role_id}/permissions`

List the permissions an RBAC Role grants.

The RBAC Roles API is available to Claude Enterprise organizations only.

#### Parameters

- `rbac_role_id: str` (path parameter)

  ID of the RBAC Role.

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

#### Returns

- `class RBACRolePermission`

  - `type: Literal["rbac_role_permission"]`

    Object type.

    For RBAC Role Permissions, this is always `"rbac_role_permission"`.

    default: rbac_role_permission

  - `action: str`

    Action the permission grants on the resource.

    The vocabulary follows the resource: an `organization` grant carries a
    product-feature entitlement (for example `chat`), an admin-panel
    permission entitlement (`permission_*`), or a blanket capability-access
    mode — `capability_access_all` grants every product-feature entitlement
    except `inference_hooks_inspection`, which a role holds only through its
    own row, and `capability_access_all_ga` grants the subset of those for
    stable features as it stands at permission-check time; neither mode grants
    model-access entitlements. A consumer enumerating a role's per-feature grants should
    treat a blanket row as granting every product-feature entitlement it
    covers, or it will under-report the role's effective access. A `connector_tool` grant carries
    a tool-access action (`use` or `always_allow`); a `connector_scope` grant
    carries the scope action `grant` (the role may receive the named OAuth
    scope when tokens are minted for the connector); `connector` and
    `all_connectors` grants carry a tool-access action, the scope action, or
    an authentication-method action (`interactive` or `managed`).

  - `resource: Resource`

    What the permission applies to.

    A tagged union: `type` names the kind of resource and determines which
    identifier fields are present.

    - `class RBACOrganizationPermissionResource`

      - `type: Literal["organization"]`

        Kind of resource the permission applies to.

        default: organization

      - `organization_id: str`

        UUID of the organization the permission applies to.

    - `class RBACConnectorToolPermissionResource`

      - `type: Literal["connector_tool"]`

        Kind of resource the permission applies to.

        default: connector_tool

      - `connector_id: str`

        ID of the connector the permission applies to.

      - `tool_name: str`

        Published name of the connector tool the permission applies to.

        When the published name contains characters outside `[a-zA-Z0-9_-]` (or
        collides with a reserved form), it is server-encoded into a stable
        `{prefix}_{32-hex}` form — a shortened readable prefix of the name plus
        a hash — from which the published name is not recoverable.

    - `class RBACConnectorScopePermissionResource`

      - `type: Literal["connector_scope"]`

        Kind of resource the permission applies to.

        default: connector_scope

      - `connector_id: str`

        ID of the connector the permission applies to.

      - `scope: str`

        OAuth scope the permission names — the role may receive this scope when
        tokens are minted for the connector.

        Subject to the same encoding rule as `tool_name`: a scope containing
        characters outside `[a-zA-Z0-9_-]` (or colliding with a reserved form)
        appears server-encoded in a stable `{prefix}_{32-hex}` form. OAuth
        scopes routinely contain `:` and `/`, so most appear encoded.

    - `class RBACConnectorPermissionResource`

      - `type: Literal["connector"]`

        Kind of resource the permission applies to.

        default: connector

      - `connector_id: str`

        ID of the connector the permission applies to.

    - `class RBACAllConnectorsPermissionResource`

      - `type: Literal["all_connectors"]`

        Kind of resource the permission applies to.

        default: all_connectors

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.rbac_roles.permissions.list(
    rbac_role_id="rbac_role_id",
)
page = page.data[0]
print(page.action)
```

##### Response (200)

```json
{
  "data": [
    {
      "action": "use",
      "resource": {
        "organization_id": "3c4f5e6d-7a8b-49c0-9d1e-2f3a4b5c6d7e",
        "type": "organization"
      },
      "type": "rbac_role_permission"
    }
  ],
  "has_more": true,
  "next_page": "eyJjdXJzb3IiOiAicmJhY19yb2xlXzAxIn0"
}
```
