---
title: Files
url: https://platform.claude.com/docs/en/api/python/files
---

# Files

## Upload File

`files.upload(**kwargs) -> FileMetadata`

**POST** `/v1/files`

Upload File

### Parameters

- `file: FileTypes`

  The file to upload. Only the final path component of the part's `filename` is kept; an absent or empty `filename` is replaced with `unnamed` plus the extension for the file's stored `mime_type`, when known.

  format: binary

- `expires_in_seconds: Optional[int]`

  Seconds from upload until the file expires and its bytes become permanently unavailable. Must be between 3600 (one hour) and 7776000 (ninety days).

  minimum: 3600, maximum: 7776000

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

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

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
file_metadata = client.files.upload(
    file=b"Example data",
)
print(file_metadata.id)
```

#### Response (200)

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

## List Files

`files.list(**kwargs) -> SyncPageCursor[FileMetadata]`

**GET** `/v1/files`

List Files

### Parameters

- `ids: Optional[Sequence[str]]` (query parameter)

  Restrict the result set to Files whose `id` is in this list. At most 100 entries (after de-duplication). Mutually exclusive with `page` and `limit`. When supplied, the response is always a single page (`next_page` is null). IDs that do not resolve to a visible File — including deleted Files — are silently omitted.

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque page cursor returned in a prior list response's `next_page`. Prefixed `page_`.

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

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

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.files.list()
page = page.data[0]
print(page.id)
```

#### Response (200)

```json
{
  "data": [
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
  ],
  "next_page": "next_page"
}
```

## Download File

`files.download(file_id, **kwargs) -> BinaryResponseContent`

**GET** `/v1/files/{file_id}/content`

Download File

### Parameters

- `file_id: str` (path parameter)

  ID of the File.

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `BinaryResponseContent`

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
response = client.files.download(
    file_id="file_id",
)
print(response)
content = response.read()
print(content)
```

## Get File Metadata

`files.retrieve_metadata(file_id, **kwargs) -> FileMetadata`

**GET** `/v1/files/{file_id}`

Get File Metadata

### Parameters

- `file_id: str` (path parameter)

  ID of the File.

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

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

### Example

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

#### Response (200)

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

## Delete File

`files.delete(file_id, **kwargs) -> DeletedFile`

**DELETE** `/v1/files/{file_id}`

Delete File

### Parameters

- `file_id: str` (path parameter)

  ID of the File.

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `class DeletedFile`

  - `type: Optional[Literal["file_deleted"]]`

    Deleted object type.

    For file deletion, this is always `"file_deleted"`.

    default: file_deleted

  - `id: str`

    ID of the deleted file.

### Example

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

#### Response (200)

```json
{
  "id": "file_011CNha8iCJcU1wXNR6q4V8w",
  "type": "file_deleted"
}
```

## Domain types

### Deleted File

- `class DeletedFile`

  - `type: Optional[Literal["file_deleted"]]`

    Deleted object type.

    For file deletion, this is always `"file_deleted"`.

    default: file_deleted

  - `id: str`

    ID of the deleted file.

### File Metadata

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
