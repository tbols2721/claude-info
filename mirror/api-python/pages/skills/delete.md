---
title: Delete Skill
url: https://platform.claude.com/docs/en/api/python/skills/delete
---

# Delete Skill

`skills.delete(skill_id, **kwargs) -> DeletedSkill`

**DELETE** `/v1/skills/{skill_id}`

Delete Skill

## Parameters

- `skill_id: str` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

## Returns

- `class DeletedSkill`

  - `type: Literal["skill_deleted"]`

    Deleted object type.

    For Skills, this is always `"skill_deleted"`.

    default: skill_deleted

  - `id: str`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
deleted_skill = client.skills.delete(
    skill_id="skill_id",
)
print(deleted_skill.id)
```

### Response (200)

```json
{
  "id": "skill_01JAbcdefghijklmnopqrstuvw",
  "type": "skill_deleted"
}
```
