---
title: Delete File
url: https://platform.claude.com/docs/en/api/cli/files/delete
---

# Delete File

`$ ant files delete`

**DELETE** `/v1/files/{file_id}`

Delete File

## Parameters

- `--file-id: string` (path parameter)

  ID of the File.

- `--workspace-id: optional string` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

## Returns

- `deleted_file: object`

  - `type: optional "file_deleted"`

    Deleted object type.

    For file deletion, this is always `"file_deleted"`.

  - `id: string`

    ID of the deleted file.

## Example

```bash
ant files delete \
  --file-id file_id
```

### Response (200)

```json
{
  "id": "file_011CNha8iCJcU1wXNR6q4V8w",
  "type": "file_deleted"
}
```
