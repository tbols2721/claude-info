---
title: Get Current Organization
url: https://platform.claude.com/docs/en/api/python/organization/retrieve
---

# Get Current Organization

`organization.retrieve() -> OrganizationInfo`

**GET** `/v1/organizations/me`

Retrieve information about the organization associated with the authenticated API key.

## Returns

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

## Example

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

### Response (200)

```json
{
  "id": "12345678-1234-5678-1234-567812345678",
  "name": "Organization Name",
  "type": "organization"
}
```
