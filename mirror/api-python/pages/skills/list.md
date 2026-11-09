---
title: List Skills
url: https://platform.claude.com/docs/en/api/python/skills/list
---

# List Skills

`skills.list(**kwargs) -> SyncPageCursor[Skill]`

**GET** `/v1/skills`

List Skills

## Parameters

- `limit: Optional[int]` (query parameter)

  Number of results to return per page.

  Ranges from `1` to `1000`. Defaults to `20`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Pagination token for fetching a specific page of results.

  Pass the value from a previous response's `next_page` field to get the next page of results.

- `source: Optional[str]` (query parameter)

  Filter skills by source.

  If provided, only skills from the specified source will be returned:

  * `"custom"`: only return user-created skills
  * `"anthropic"`: only return Anthropic-created skills

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

## Returns

- `class Skill`

  - `type: Literal["skill"]`

    Object type.

    For Skills, this is always `"skill"`.

    default: skill

  - `id: str`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `created_at: datetime`

    ISO 8601 timestamp of when the skill was created.

    format: date-time

  - `display_name: str`

    Human-readable, single-line label for the Skill. Maximum 255 characters.
    Always set: derived from the SKILL.md frontmatter `name` when omitted at
    creation. Not unique.

  - `latest_version_id: str`

    ID of the newest Skill Version — what `latest` references resolve to. Always set: a Skill holds at least one version.

  - `source: SkillSource`

    Where the Skill comes from.

    Possible values:

    * `"custom"`: authored by the platform user; private to their workspace
    * `"anthropic"`: published by Anthropic; shared and read-only
    * `"anthropic_example"`: Anthropic-published sample Skill
    * `"plugin"`: resolved from an installed plugin

    - `type: Literal["custom", "anthropic", "anthropic_example", "plugin"]`

      Where the Skill comes from.

      Possible values:

      * `"custom"`: authored by the platform user; private to their workspace
      * `"anthropic"`: published by Anthropic; shared and read-only
      * `"anthropic_example"`: Anthropic-published sample Skill
      * `"plugin"`: resolved from an installed plugin

      - `"custom"`

      - `"anthropic"`

      - `"anthropic_example"`

      - `"plugin"`

  - `updated_at: datetime`

    ISO 8601 timestamp of when the skill was last updated.

    format: date-time

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.skills.list()
page = page.data[0]
print(page.id)
```

### Response (200)

```json
{
  "data": [
    {
      "id": "skill_01JAbcdefghijklmnopqrstuvw",
      "created_at": "2024-10-30T23:58:27.427722Z",
      "display_name": "display_name",
      "latest_version_id": "latest_version_id",
      "source": {
        "type": "custom"
      },
      "type": "skill",
      "updated_at": "2024-10-30T23:58:27.427722Z"
    }
  ],
  "next_page": "next_page"
}
```
