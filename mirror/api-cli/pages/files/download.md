---
title: Download File
url: https://platform.claude.com/docs/en/api/cli/files/download
---

# Download File

`$ ant files download`

**GET** `/v1/files/{file_id}/content`

Download File

## Parameters

- `--file-id: string` (path parameter)

  ID of the File.

- `--workspace-id: optional string` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

## Returns

- `unnamed_schema_0: file path`

## Example

```bash
ant files download \
  --file-id file_id
```
