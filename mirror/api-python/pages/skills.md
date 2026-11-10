---
title: Skills
url: https://platform.claude.com/docs/en/api/python/skills
---

# Skills

## Create Skill

`skills.create(**kwargs) -> Skill`

**POST** `/v1/skills`

Create Skill

### Parameters

- `files: Sequence[FileTypes]`

  Files to upload for the skill.

  All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

- `display_name: Optional[str]`

  Human-readable, single-line label for the Skill. Maximum 255 characters.
  Always set: derived from the SKILL.md frontmatter `name` when omitted at
  creation. Not unique.

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

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

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
skill = client.skills.create(
    files=[b"Example data"],
)
print(skill.id)
```

#### Response (200)

```json
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
```

## List Skills

`skills.list(**kwargs) -> SyncPageCursor[Skill]`

**GET** `/v1/skills`

List Skills

### Parameters

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

### Returns

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

### Example

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

#### Response (200)

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

## Get Skill

`skills.retrieve(skill_id, **kwargs) -> Skill`

**GET** `/v1/skills/{skill_id}`

Get Skill

### Parameters

- `skill_id: str` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

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

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
skill = client.skills.retrieve(
    skill_id="skill_id",
)
print(skill.id)
```

#### Response (200)

```json
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
```

## Delete Skill

`skills.delete(skill_id, **kwargs) -> DeletedSkill`

**DELETE** `/v1/skills/{skill_id}`

Delete Skill

### Parameters

- `skill_id: str` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `class DeletedSkill`

  - `type: Literal["skill_deleted"]`

    Deleted object type.

    For Skills, this is always `"skill_deleted"`.

    default: skill_deleted

  - `id: str`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

### Example

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

#### Response (200)

```json
{
  "id": "skill_01JAbcdefghijklmnopqrstuvw",
  "type": "skill_deleted"
}
```

## Domain types

### Deleted Skill

- `class DeletedSkill`

  - `type: Literal["skill_deleted"]`

    Deleted object type.

    For Skills, this is always `"skill_deleted"`.

    default: skill_deleted

  - `id: str`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

### Skill

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

### Skill Read Blocked Undecryptable Error Details

- `class SkillReadBlockedUndecryptableErrorDetails`

  A custom skill the request names is stored under an encryption key state the workspace cannot currently decrypt.

  - `error_code: Literal["skill_read_blocked_undecryptable"]`

### Skill Source

- `class SkillSource`

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

## Skills › Versions

### Create Skill Version

`skills.versions.create(skill_id, **kwargs) -> SkillVersion`

**POST** `/v1/skills/{skill_id}/versions`

Create Skill Version

#### Parameters

- `skill_id: str` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `files: Sequence[FileTypes]`

  Files to upload for the skill.

  All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

#### Returns

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

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
skill_version = client.skills.versions.create(
    skill_id="skill_id",
    files=[b"Example data"],
)
print(skill_version.id)
```

##### Response (200)

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

### List Skill Versions

`skills.versions.list(skill_id, **kwargs) -> SyncPageCursor[SkillVersion]`

**GET** `/v1/skills/{skill_id}/versions`

List Skill Versions

#### Parameters

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

#### Returns

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

#### Example

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

##### Response (200)

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

### Get Skill Version

`skills.versions.retrieve(version, **kwargs) -> SkillVersion`

**GET** `/v1/skills/{skill_id}/versions/{version}`

Get Skill Version

#### Parameters

- `skill_id: str` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `version: str` (path parameter)

  Identifies the skill version: a version ID, or the literal `latest` for the skill's most recent version.

  Requests carrying the `skills-2025-10-02` beta header address versions by their Unix epoch timestamp instead (e.g., "1759178010641129").

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

#### Returns

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

#### Example

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

##### Response (200)

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

### Delete Skill Version

`skills.versions.delete(version, **kwargs) -> DeletedSkillVersion`

**DELETE** `/v1/skills/{skill_id}/versions/{version}`

Delete Skill Version

#### Parameters

- `skill_id: str` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `version: str` (path parameter)

  Identifies the skill version by its version ID.

  Requests carrying the `skills-2025-10-02` beta header address versions by their Unix epoch timestamp instead (e.g., "1759178010641129").

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

#### Returns

- `class DeletedSkillVersion`

  - `type: Literal["skill_version_deleted"]`

    Deleted object type.

    For Skill Versions, this is always `"skill_version_deleted"`.

    default: skill_version_deleted

  - `id: str`

    Unique identifier for this Skill Version. The id addresses the version in
    paths and pins it in references.

#### Example

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

##### Response (200)

```json
{
  "id": "id",
  "type": "skill_version_deleted"
}
```
