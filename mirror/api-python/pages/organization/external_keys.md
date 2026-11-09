---
title: External Keys
url: https://platform.claude.com/docs/en/api/python/organization/external_keys
---

# External Keys

## Create External Key

`organization.external_keys.create(**kwargs) -> ExternalKey`

**POST** `/v1/organizations/external_keys`

Create an external key config owned by the caller's organization.

### Parameters

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

  ID of a user profile to bind the key to. Omit this field for a key that isn't bound to a user profile. Such a key can be attached to a Workspace whatever its user profile. The binding cannot be changed later. A key bound to a user profile can only be attached to a Workspace that has the same user profile.

### Returns

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

### Example

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

#### Response (200)

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

## List External Keys

`organization.external_keys.list(**kwargs) -> SyncPageCursor[ExternalKey]`

**GET** `/v1/organizations/external_keys`

List external key configs in the caller's organization.

Results are ordered by creation time (newest first). Use the
`next_page` cursor from the response to fetch subsequent pages.

### Parameters

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

### Returns

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

### Example

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

#### Response (200)

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

## Get External Key

`organization.external_keys.retrieve(external_key_id) -> ExternalKey`

**GET** `/v1/organizations/external_keys/{external_key_id}`

Retrieve a single external key config in the caller's organization by ID.

### Parameters

- `external_key_id: str` (path parameter)

  ID of the External Key.

  maxLength: 2048

### Returns

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

### Example

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

#### Response (200)

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

## Update External Key

`organization.external_keys.update(external_key_id, **kwargs) -> ExternalKey`

**POST** `/v1/organizations/external_keys/{external_key_id}`

Partially update an external key config. Omitted fields are left unchanged.

`display_name` is always editable. `geo` and `provider_config` cannot
be changed once any workspace references this config, because previously
encrypted data requires the original key identity to decrypt.

### Parameters

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

### Returns

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

### Example

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

#### Response (200)

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

## Delete External Key

`organization.external_keys.delete(external_key_id) -> ExternalKeyDeleteResponse`

**DELETE** `/v1/organizations/external_keys/{external_key_id}`

Delete an external key config.

The request is rejected if any workspace still references this config.

### Parameters

- `external_key_id: str` (path parameter)

  ID of the External Key.

  maxLength: 2048

### Returns

- `class ExternalKeyDeleteResponse`

  - `type: Literal["external_key_deleted"]`

    default: external_key_deleted

  - `id: str`

    ID of the deleted External Key.

### Example

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

#### Response (200)

```json
{
  "id": "ekey_01AbCdEfGhIjKlMnOpQrStUv",
  "type": "external_key_deleted"
}
```

## Validate External Key

`organization.external_keys.validate(external_key_id) -> ExternalKeyValidateResponse`

**POST** `/v1/organizations/external_keys/{external_key_id}/validate`

Validate an external key config against the customer's KMS.

Anthropic performs an encrypt/decrypt roundtrip against the configured
KMS key and waits up to 30 seconds for the result. The response status is
`success` if the roundtrip succeeded, or `failure` with an error
message if it failed or timed out.

### Parameters

- `external_key_id: str` (path parameter)

  ID of the External Key.

  maxLength: 2048

### Returns

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

### Example

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

#### Response (200)

```json
{
  "error": "error",
  "status": "failure",
  "type": "external_key_validation"
}
```

## Domain types

### AWS External Key Config

- `class AWSExternalKeyConfig`

  - `type: Literal["aws"]`

  - `kms_arn: str`

    Full ARN of the AWS KMS key. On Claude Platform on AWS, alias ARNs are rejected, and your organization's own key must be a single-Region key in your organization's AWS account.

    maxLength: 2048

  - `region: Optional[str]`

    AWS region. Derived from `kms_arn` if omitted.

### Azure External Key Config

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

### Azure External Key Config Param

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

### External Key

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

### External Key Attached Attachment

- `class ExternalKeyAttachedAttachment`

  - `type: Literal["attached"]`

    default: attached

### External Key Unattached Attachment

- `class ExternalKeyUnattachedAttachment`

  - `type: Literal["unattached"]`

    default: unattached

### GCP External Key Config

- `class GCPExternalKeyConfig`

  - `type: Literal["gcp"]`

  - `key_name: str`

    Full resource name of the Cloud KMS key.

### External Key Delete Response

- `class ExternalKeyDeleteResponse`

  - `type: Literal["external_key_deleted"]`

    default: external_key_deleted

  - `id: str`

    ID of the deleted External Key.

### External Key Validate Response

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
