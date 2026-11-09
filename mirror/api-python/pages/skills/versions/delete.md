---
title: Delete Skill Version
url: https://platform.claude.com/docs/en/api/python/skills/versions/delete
---

# Delete Skill Version

`skills.versions.delete(version, **kwargs) -> DeletedSkillVersion`

**DELETE** `/v1/skills/{skill_id}/versions/{version}`

Delete Skill Version

## Parameters

- `skill_id: str` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `version: str` (path parameter)

  Identifies the skill version by its version ID.

  Requests carrying the `skills-2025-10-02` beta header address versions by their Unix epoch timestamp instead (e.g., "1759178010641129").

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

## Returns

- `class DeletedSkillVersion`

  - `type: Literal["skill_version_deleted"]`

    Deleted object type.

    For Skill Versions, this is always `"skill_version_deleted"`.

    default: skill_version_deleted

  - `id: str`

    Unique identifier for this Skill Version. The id addresses the version in
    paths and pins it in references.

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
deleted_skill_version = client.skills.versions.delete(
    version="version",
    skill_id="skill_id",
)
print(deleted_skill_version.id)
```

### Response (200)

```json
{
  "id": "id",
  "type": "skill_version_deleted"
}
```
