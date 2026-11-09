---
title: Delete Invite
url: https://platform.claude.com/docs/en/api/python/organization/invites/delete
---

# Delete Invite

`organization.invites.delete(invite_id) -> InviteDeleteResponse`

**DELETE** `/v1/organizations/invites/{invite_id}`

Delete a pending invite.

## Parameters

- `invite_id: str` (path parameter)

  ID of the Invite.

## Returns

- `class InviteDeleteResponse`

  - `type: Literal["invite_deleted"]`

    Deleted object type.

    For Invites, this is always `"invite_deleted"`.

    default: invite_deleted

  - `id: str`

    ID of the Invite.

## Example

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

### Response (200)

```json
{
  "id": "invite_015gWxCN9Hfg2QhZwTK7Mdeu",
  "type": "invite_deleted"
}
```
