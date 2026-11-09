---
title: Delete Spend Limit
url: https://platform.claude.com/docs/en/api/python/beta/organization/spend_limits/delete
---

# Delete Spend Limit

`beta.organization.spend_limits.delete(spend_limit_id) -> SpendLimitDeleteResponse`

**DELETE** `/v1/organizations/spend_limits/{spend_limit_id}`

Delete a spend limit.

For a Claude Enterprise organization, this deletes a per-user override, and
the member falls back to any inherited spend limit at that period. Its
seat-tier, group, and organization-level rows cannot be deleted via this
endpoint. A Claude Console organization deletes its organization and
workspace limits, but not its `usage_tier` limit. Deleting organization and
workspace limits through the API is in an early access preview.

## Parameters

- `spend_limit_id: str` (path parameter)

  ID of the Spend Limit.

## Returns

- `class SpendLimitDeleteResponse`

  - `type: Literal["spend_limit_deleted"]`

    default: spend_limit_deleted

  - `id: str`

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
spend_limit = client.beta.organization.spend_limits.delete(
    "spend_limit_id",
)
print(spend_limit.id)
```

### Response (200)

```json
{
  "id": "id",
  "type": "spend_limit_deleted"
}
```
