---
title: Delete External Key
url: https://platform.claude.com/docs/en/api/python/beta/organization/external_keys/delete
---

# Delete External Key

`beta.organization.external_keys.delete(external_key_id) -> ExternalKeyDeleteResponse`

**DELETE** `/v1/organizations/external_keys/{external_key_id}`

Delete an external key config.

The request is rejected if any workspace still references this config.

## Parameters

- `external_key_id: str` (path parameter)

  ID of the External Key.

  maxLength: 2048

## Returns

- `class ExternalKeyDeleteResponse`

  - `type: Literal["external_key_deleted"]`

    default: external_key_deleted

  - `id: str`

    ID of the deleted External Key.

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
external_key = client.beta.organization.external_keys.delete(
    "external_key_id",
)
print(external_key.id)
```

### Response (200)

```json
{
  "id": "ekey_01AbCdEfGhIjKlMnOpQrStUv",
  "type": "external_key_deleted"
}
```
