---
title: Get File Metadata
url: https://platform.claude.com/docs/en/api/python/files/retrieve_metadata
---

# Get File Metadata

`files.retrieve_metadata(file_id, **kwargs) -> FileMetadata`

**GET** `/v1/files/{file_id}`

Get File Metadata

## Parameters

- `file_id: str` (path parameter)

  ID of the File.

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

## Returns

- `class FileMetadata`

  - `type: Literal["file"]`

    Object type.

    For files, this is always `"file"`.

  - `id: str`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `created_at: datetime`

    RFC 3339 datetime string representing when the file was created.

    format: date-time

  - `filename: str`

    Original filename of the uploaded file.

    minLength: 1, maxLength: 500

  - `mime_type: str`

    MIME type of the file.

    minLength: 1, maxLength: 255

  - `size_bytes: int`

    Size of the file in bytes.

    minimum: 0

  - `downloadable: Optional[bool]`

    Whether the file can be downloaded.

    default: false

  - `expires_at: Optional[datetime]`

    RFC 3339 datetime string representing when the file will expire and become unavailable for download. Null if the file does not expire. For files uploaded with `expires_in_seconds`, this is the upload time plus that value.

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
file_metadata = client.files.retrieve_metadata(
    file_id="file_id",
)
print(file_metadata.id)
```

### Response (200)

```json
{
  "id": "file_011CNha8iCJcU1wXNR6q4V8w",
  "created_at": "2025-04-15T18:37:24.100435Z",
  "filename": "document.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 102400,
  "type": "file",
  "downloadable": false,
  "expires_at": "2025-05-15T18:37:24.100435Z"
}
```
