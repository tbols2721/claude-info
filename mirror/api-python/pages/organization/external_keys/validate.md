---
title: Validate External Key
url: https://platform.claude.com/docs/en/api/python/organization/external_keys/validate
---

# Validate External Key

`organization.external_keys.validate(external_key_id) -> ExternalKeyValidateResponse`

**POST** `/v1/organizations/external_keys/{external_key_id}/validate`

Validate an external key config against the customer's KMS.

Anthropic performs an encrypt/decrypt roundtrip against the configured
KMS key and waits up to 30 seconds for the result. The response status is
`success` if the roundtrip succeeded, or `failure` with an error
message if it failed or timed out.

## Parameters

- `external_key_id: str` (path parameter)

  ID of the External Key.

  maxLength: 2048

## Returns

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

## Example

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

### Response (200)

```json
{
  "error": "error",
  "status": "failure",
  "type": "external_key_validation"
}
```
