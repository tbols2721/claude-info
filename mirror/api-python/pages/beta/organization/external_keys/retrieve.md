---
title: Get External Key
url: https://platform.claude.com/docs/en/api/python/beta/organization/external_keys/retrieve
---

# Get External Key

`beta.organization.external_keys.retrieve(external_key_id) -> BetaExternalKey`

**GET** `/v1/organizations/external_keys/{external_key_id}`

Retrieve a single external key config in the caller's organization by ID.

## Parameters

- `external_key_id: str` (path parameter)

  ID of the External Key.

  maxLength: 2048

## Returns

- `class BetaExternalKey`

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

    - `class BetaExternalKeyAttachedAttachment`

      - `type: Literal["attached"]`

        default: attached

    - `class BetaExternalKeyUnattachedAttachment`

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

    - `class BetaAWSExternalKeyConfig`

      - `type: Literal["aws"]`

      - `kms_arn: str`

        Full ARN of the AWS KMS key. On Claude Platform on AWS, alias ARNs are rejected, and your organization's own key must be a single-Region key in your organization's AWS account.

        maxLength: 2048

      - `region: Optional[str]`

        AWS region. Derived from `kms_arn` if omitted.

      - `role_arn: Optional[str]`

        **Deprecated**

        IAM role ARN. Deprecated; this field is ignored.

    - `class BetaGCPExternalKeyConfig`

      - `type: Literal["gcp"]`

      - `key_name: str`

        Full resource name of the Cloud KMS key.

    - `class BetaAzureExternalKeyConfig`

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

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_external_key = client.beta.organization.external_keys.retrieve(
    "external_key_id",
)
print(beta_external_key.id)
```

### Response (200)

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
