---
title: Versions
url: https://platform.claude.com/docs/en/api/cli/skills/versions
---

# Versions

## Create Skill Version

`$ ant skills:versions create`

**POST** `/v1/skills/{skill_id}/versions`

Create Skill Version

### Parameters

- `--skill-id: string` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `--file: array of file`

  Files to upload for the skill.

  All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

- `--workspace-id: optional string` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `skill_version: object`

  - `type: "skill_version"`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `id: string`

    Unique identifier for this Skill Version. The id addresses the version in
    paths and pins it in references.

  - `created_at: string`

    ISO 8601 timestamp of when the skill was created.

    format: date-time

  - `description: string`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `name: string`

    The Skill's immutable kebab-case slug, set at creation from the first
    upload's SKILL.md frontmatter `name` (or its enclosing directory). Every
    later upload must resolve to the same value. Also the top-level directory
    of the Skill's mounted files and the base name of a downloaded archive.

  - `skill_id: string`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

### Example

```bash
ant skills:versions create \
  --skill-id skill_id \
  --file 'Example data'
```

#### Response (200)

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

## List Skill Versions

`$ ant skills:versions list`

**GET** `/v1/skills/{skill_id}/versions`

List Skill Versions

### Parameters

- `--skill-id: string` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `--limit: optional number` (query parameter)

  Number of results to return per page.

  Ranges from `1` to `1000`. Defaults to `20`.

  minimum: 1, maximum: 1000

- `--page: optional string` (query parameter)

  Optionally set to the `next_page` token from the previous response.

- `--workspace-id: optional string` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `ListSkillVersionsResponse: object`

  - `data: array of SkillVersion`

    List of skills.

    - `type: "skill_version"`

      Object type.

      For Skill Versions, this is always `"skill_version"`.

    - `id: string`

      Unique identifier for this Skill Version. The id addresses the version in
      paths and pins it in references.

    - `created_at: string`

      ISO 8601 timestamp of when the skill was created.

      format: date-time

    - `description: string`

      Description of the skill version.

      This is extracted from the SKILL.md file in the skill upload.

    - `name: string`

      The Skill's immutable kebab-case slug, set at creation from the first
      upload's SKILL.md frontmatter `name` (or its enclosing directory). Every
      later upload must resolve to the same value. Also the top-level directory
      of the Skill's mounted files and the base name of a downloaded archive.

    - `skill_id: string`

      Unique identifier for the skill.

      The format and length of IDs may change over time.

  - `next_page: string`

    Token for fetching the next page of results.

    If `null`, there are no more results available. Pass this value to the `page` parameter in the next request to get the next page.

### Example

```bash
ant skills:versions list \
  --skill-id skill_id
```

#### Response (200)

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

## Get Skill Version

`$ ant skills:versions retrieve`

**GET** `/v1/skills/{skill_id}/versions/{version}`

Get Skill Version

### Parameters

- `--skill-id: string` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `--version: string` (path parameter)

  Identifies the skill version: a version ID, or the literal `latest` for the skill's most recent version.

  Requests carrying the `skills-2025-10-02` beta header address versions by their Unix epoch timestamp instead (e.g., "1759178010641129").

- `--workspace-id: optional string` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `skill_version: object`

  - `type: "skill_version"`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `id: string`

    Unique identifier for this Skill Version. The id addresses the version in
    paths and pins it in references.

  - `created_at: string`

    ISO 8601 timestamp of when the skill was created.

    format: date-time

  - `description: string`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `name: string`

    The Skill's immutable kebab-case slug, set at creation from the first
    upload's SKILL.md frontmatter `name` (or its enclosing directory). Every
    later upload must resolve to the same value. Also the top-level directory
    of the Skill's mounted files and the base name of a downloaded archive.

  - `skill_id: string`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

### Example

```bash
ant skills:versions retrieve \
  --skill-id skill_id \
  --version version
```

#### Response (200)

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

## Delete Skill Version

`$ ant skills:versions delete`

**DELETE** `/v1/skills/{skill_id}/versions/{version}`

Delete Skill Version

### Parameters

- `--skill-id: string` (path parameter)

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `--version: string` (path parameter)

  Identifies the skill version by its version ID.

  Requests carrying the `skills-2025-10-02` beta header address versions by their Unix epoch timestamp instead (e.g., "1759178010641129").

- `--workspace-id: optional string` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `deleted_skill_version: object`

  - `type: "skill_version_deleted"`

    Deleted object type.

    For Skill Versions, this is always `"skill_version_deleted"`.

  - `id: string`

    Unique identifier for this Skill Version. The id addresses the version in
    paths and pins it in references.

### Example

```bash
ant skills:versions delete \
  --skill-id skill_id \
  --version version
```

#### Response (200)

```json
{
  "id": "id",
  "type": "skill_version_deleted"
}
```

## Domain types

### Deleted Skill Version

- `deleted_skill_version: object`

  - `type: "skill_version_deleted"`

    Deleted object type.

    For Skill Versions, this is always `"skill_version_deleted"`.

  - `id: string`

    Unique identifier for this Skill Version. The id addresses the version in
    paths and pins it in references.

### Skill Version

- `skill_version: object`

  - `type: "skill_version"`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `id: string`

    Unique identifier for this Skill Version. The id addresses the version in
    paths and pins it in references.

  - `created_at: string`

    ISO 8601 timestamp of when the skill was created.

    format: date-time

  - `description: string`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `name: string`

    The Skill's immutable kebab-case slug, set at creation from the first
    upload's SKILL.md frontmatter `name` (or its enclosing directory). Every
    later upload must resolve to the same value. Also the top-level directory
    of the Skill's mounted files and the base name of a downloaded archive.

  - `skill_id: string`

    Unique identifier for the skill.

    The format and length of IDs may change over time.
