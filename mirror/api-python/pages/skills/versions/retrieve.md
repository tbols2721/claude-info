---
title: Get Skill Version
url: https://platform.claude.com/docs/en/api/python/skills/versions/retrieve
---

# Get Skill Version

`skills.versions.retrieve(version, **kwargs) -> SkillVersion`

**GET** `/v1/skills/{skill_id}/versions/{version}`

Get Skill Version

## Parameters

- `skill_id: str` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `version: str` (path parameter)

  Identifies the skill version: a version ID, or the literal `latest` for the skill's most recent version.

  Requests carrying the `skills-2025-10-02` beta header address versions by their Unix epoch timestamp instead (e.g., "1759178010641129").

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

## Returns

- `class SkillVersion`

  - `type: Literal["skill_version"]`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

    default: skill_version

  - `id: str`

    Unique identifier for this Skill Version. The id addresses the version in
    paths and pins it in references.

  - `created_at: datetime`

    ISO 8601 timestamp of when the skill was created.

    format: date-time

  - `description: str`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `name: str`

    The Skill's immutable kebab-case slug, set at creation from the first
    upload's SKILL.md frontmatter `name` (or its enclosing directory). Every
    later upload must resolve to the same value. Also the top-level directory
    of the Skill's mounted files and the base name of a downloaded archive.

  - `skill_id: str`

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
skill_version = client.skills.versions.retrieve(
    version="version",
    skill_id="skill_id",
)
print(skill_version.id)
```

### Response (200)

```json
{
  "id": "id",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "description": "description",
  "name": "name",
  "skill_id": "skill_01JAbcdefghijklmnopqrstuvw",
  "type": "skill_version"
}
```
