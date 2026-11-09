---
title: Action URLs
url: https://platform.claude.com/docs/en/api/python/user_profiles/action_urls
---

# Action URLs

## Create Action URL

`user_profiles.action_urls.create(user_profile_id, **kwargs) -> UserProfileActionURL`

**POST** `/v1/user_profiles/{user_profile_id}/action_urls`

Create Action URL

### Parameters

- `user_profile_id: str` (path parameter)

  The ID of the user profile the action is for (`uprof_...`).

- `action: UserProfileEnrollEndUserActionParam`

  The action that the person who opens the URL takes.

  - `type: Literal["enroll_end_user"]`

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `class UserProfileActionURL`

  A URL to give to the person who takes the requested action.

  - `type: Literal["user_profile_action_url"]`

    Object type. Always `user_profile_action_url`.

  - `expires_at: datetime`

    When the URL stops working, in RFC 3339 format.

    format: date-time

  - `url: str`

    The URL to give to the person who takes the action. Anyone who holds it can open it until `expires_at`.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
user_profile_action_url = client.user_profiles.action_urls.create(
    user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
    action={"type": "enroll_end_user"},
)
print(user_profile_action_url.expires_at)
```

#### Response (200)

```json
{
  "expires_at": "2026-03-15T10:15:00Z",
  "type": "user_profile_action_url",
  "url": "https://platform.claude.com/user-profiles/enrollment/M3J0bGJxZ2ppMnptbnB1"
}
```

## Domain types

### User Profile Action URL

- `class UserProfileActionURL`

  A URL to give to the person who takes the requested action.

  - `type: Literal["user_profile_action_url"]`

    Object type. Always `user_profile_action_url`.

  - `expires_at: datetime`

    When the URL stops working, in RFC 3339 format.

    format: date-time

  - `url: str`

    The URL to give to the person who takes the action. Anyone who holds it can open it until `expires_at`.

### User Profile Enroll End User Action

- `class UserProfileEnrollEndUserActionParam`

  The end-user that the profile represents enrolls in a program.

  - `type: Literal["enroll_end_user"]`
