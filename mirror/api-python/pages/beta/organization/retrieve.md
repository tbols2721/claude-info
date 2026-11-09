---
title: Get Current Organization
url: https://platform.claude.com/docs/en/api/python/beta/organization/retrieve
---

# Get Current Organization

`beta.organization.retrieve() -> BetaOrganization`

**GET** `/v1/organizations/me`

Retrieve information about the organization associated with the authenticated API key.

## Returns

- `class BetaOrganization`

  - `type: Literal["organization"]`

    Object type.

    For Organizations, this is always `"organization"`.

    default: organization

  - `id: str`

    ID of the Organization.

    format: uuid

  - `name: str`

    Name of the Organization.

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_organization = client.beta.organization.retrieve()
print(beta_organization.id)
```

### Response (200)

```json
{
  "id": "12345678-1234-5678-1234-567812345678",
  "name": "Organization Name",
  "type": "organization"
}
```
