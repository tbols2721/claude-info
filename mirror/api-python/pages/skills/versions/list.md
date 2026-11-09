---
title: List Skill Versions
url: https://platform.claude.com/docs/en/api/python/skills/versions/list
---

# List Skill Versions

`skills.versions.list(skill_id, **kwargs) -> SyncPageCursor[SkillVersion]`

**GET** `/v1/skills/{skill_id}/versions`

List Skill Versions

## Parameters

- `skill_id: str` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `limit: Optional[int]` (query parameter)

  Number of results to return per page.

  Ranges from `1` to `1000`. Defaults to `20`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

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
page = client.skills.versions.list(
    skill_id="skill_id",
)
page = page.data[0]
print(page.id)
```

### Response (200)

```json
{
  "data": [
    {
      "id": "id",
      "created_at": "2024-10-30T23:58:27.427722Z",
      "description": "description",
      "name": "name",
      "skill_id": "skill_01JAbcdefghijklmnopqrstuvw",
      "type": "skill_version"
    }
  ],
  "next_page": "next_page"
}
```
