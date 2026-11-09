---
title: Delete File
url: https://platform.claude.com/docs/en/api/python/files/delete
---

# Delete File

`files.delete(file_id, **kwargs) -> DeletedFile`

**DELETE** `/v1/files/{file_id}`

Delete File

## Parameters

- `file_id: str` (path parameter)

  ID of the File.

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

## Returns

- `class DeletedFile`

  - `type: Optional[Literal["file_deleted"]]`

    Deleted object type.

    For file deletion, this is always `"file_deleted"`.

    default: file_deleted

  - `id: str`

    ID of the deleted file.

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
deleted_file = client.files.delete(
    file_id="file_id",
)
print(deleted_file.id)
```

### Response (200)

```json
{
  "id": "file_011CNha8iCJcU1wXNR6q4V8w",
  "type": "file_deleted"
}
```
