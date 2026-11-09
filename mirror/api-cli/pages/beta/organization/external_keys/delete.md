---
title: Delete External Key
url: https://platform.claude.com/docs/en/api/cli/beta/organization/external_keys/delete
---

# Delete External Key

`$ ant beta:organization:external-keys delete`

**DELETE** `/v1/organizations/external_keys/{external_key_id}`

Delete an external key config.

The request is rejected if any workspace still references this config.

## Parameters

- `--external-key-id: string` (path parameter)

  ID of the External Key.

  maxLength: 2048

## Returns

- `BetaOrganizationExternalKeyDeleteResponse: object`

  - `type: "external_key_deleted"`

  - `id: string`

    ID of the deleted External Key.

## Example

```bash
ant beta:organization:external-keys delete \
  --external-key-id external_key_id
```

### Response (200)

```json
{
  "id": "ekey_01AbCdEfGhIjKlMnOpQrStUv",
  "type": "external_key_deleted"
}
```
