---
title: Download File
url: https://platform.claude.com/docs/en/api/python/files/download
---

# Download File

`files.download(file_id, **kwargs) -> BinaryResponseContent`

**GET** `/v1/files/{file_id}/content`

Download File

## Parameters

- `file_id: str` (path parameter)

  ID of the File.

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

## Returns

- `BinaryResponseContent`

## Example

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
