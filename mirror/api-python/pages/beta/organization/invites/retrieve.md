---
title: Get Invite
url: https://platform.claude.com/docs/en/api/python/beta/organization/invites/retrieve
---

# Get Invite

`beta.organization.invites.retrieve(invite_id) -> BetaOrganizationInvite`

**GET** `/v1/organizations/invites/{invite_id}`

Retrieve an invite by ID.

## Parameters

- `invite_id: str` (path parameter)

  ID of the Invite.

## Returns

- `class BetaOrganizationInvite`

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

  - `role: BetaOrganizationRole`

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

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_organization_invite = client.beta.organization.invites.retrieve(
    "invite_id",
)
print(beta_organization_invite.id)
```

### Response (200)

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
