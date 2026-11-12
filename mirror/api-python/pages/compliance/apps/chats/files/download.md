---
title: Download file content
url: https://platform.claude.com/docs/en/api/python/compliance/apps/chats/files/download
---

# Download file content

**GET** `/v1/compliance/apps/chats/files/{claude_file_id}/content`

Downloads the binary content of a file referenced in chat messages.

## Path parameters

- `claude_file_id: string`

  The file ID (tagged ID, e.g., claude_file_abc123). Also use this endpoint for any id in `chat_messages[].generated_files[].id` that starts with `claude_file_`.

## Headers

- `"anthropic-version": string`

  The version of the Claude API to use. Send an available version on every request. Some other Compliance API endpoints return a 400 error for a request that omits this header, or sends a value that is not an available version. This endpoint treats such a request as version `2023-06-01`.

  See [API versions](https://platform.claude.com/docs/en/api/versioning?sdk_languages=http) for the available versions.

- `"x-api-key": optional string`

## Example

```bash
curl https://api.anthropic.com/v1/compliance/apps/chats/files/$CLAUDE_FILE_ID/content \
    -H 'anthropic-version: 2026-10-21' \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```
