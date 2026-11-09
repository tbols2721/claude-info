---
title: Delete User Profile
url: https://platform.claude.com/docs/en/api/python/user_profiles/delete
---

# Delete User Profile

`user_profiles.delete(user_profile_id, **kwargs) -> DeletedUserProfile`

**DELETE** `/v1/user_profiles/{user_profile_id}`

Delete User Profile

## Parameters

- `user_profile_id: str` (path parameter)

  The ID of the user profile to delete (`uprof_...`).

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

## Returns

- `class DeletedUserProfile`

  - `type: Literal["user_profile_deleted"]`

    Object type. Always `user_profile_deleted`.

  - `id: str`

    Identifier of the deleted user profile, prefixed `uprof_`.

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
deleted_user_profile = client.user_profiles.delete(
    user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
)
print(deleted_user_profile.id)
```

### Response (200)

```json
{
  "id": "uprof_011CZkZCu8hGbp5mYRQgUmz9",
  "type": "user_profile_deleted"
}
```
