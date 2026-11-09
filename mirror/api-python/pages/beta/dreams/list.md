---
title: List Dreams
url: https://platform.claude.com/docs/en/api/python/beta/dreams/list
---

# List Dreams

`beta.dreams.list(**kwargs) -> SyncPageCursor[BetaDream]`

**GET** `/v1/dreams`

List the dreams in the workspace, newest first.

Archived dreams are left out unless `include_archived` is `true`.

See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=python#list-dreams) for how to page through dreams.

## Parameters

- `created_at_gt: Optional[Union[str, datetime]]` (query parameter)

  Return only dreams created after this time (exclusive), in RFC 3339.

  format: date-time

- `created_at_lt: Optional[Union[str, datetime]]` (query parameter)

  Return only dreams created before this time (exclusive), in RFC 3339.

  format: date-time

- `include_archived: Optional[bool]` (query parameter)

  Whether to include archived dreams. Defaults to `false`.

- `limit: Optional[int]` (query parameter)

  The maximum number of dreams to return, from 1 to 100. Defaults to 20.

  format: int32

- `page: Optional[str]` (query parameter)

  The cursor for the page to return, taken from `next_page` in a previous response.

  Leave it out to get the first page.

- `statuses: Optional[List[BetaDreamStatus]]` (query parameter)

  Return only dreams that have one of these statuses.

  Repeat the parameter to give more than one status. Leave it out to return dreams of every status.

  - `"pending"`

    The dream is waiting to start and hasn't read its inputs yet.

    `outputs` is empty and every `usage` count is zero.

  - `"running"`

    The dream is reading its inputs and writing its result.

    `usage` updates while the dream has this status.

  - `"completed"`

    The dream finished and its output memory store holds the complete result.

  - `"failed"`

    The dream stopped with an error, which `error` describes.

    If `outputs` references a memory store, that memory store keeps what the dream wrote before it stopped.

  - `"canceled"`

    A cancel request stopped the dream before it reached `completed` or `failed`.

    If `outputs` references a memory store, that memory store keeps what the dream wrote. `usage` can keep changing after the cancel.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `dreaming-2026-04-21` in this header.

  - `str`

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

- `workspace_id: Optional[str]` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

## Returns

- `class BetaDream`

  An asynchronous job that reads a memory store and past sessions, then writes a reorganized version of that memory store.

  By default the dream writes its result to a new memory store and doesn't change the input memory store. With `output_behavior` set to `update_existing`, it writes its result into the input memory store instead.

  The Dreams API is in research preview: the request and response shapes are volatile and may change without the deprecation period that applies to generally-available endpoints.

  See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=python#how-it-works) for what a dream reads and produces.

  - `type: Literal["dream"]`

  - `id: str`

    The unique ID of the dream (`drm_...`).

  - `archived_at: Optional[datetime]`

    When the dream was archived, in RFC 3339, or `null` if it hasn't been archived.

    format: date-time

  - `created_at: datetime`

    When the dream was created, in RFC 3339.

    Lists of dreams are sorted by this time, newest first.

    format: date-time

  - `ended_at: Optional[datetime]`

    When the dream reached `completed`, `failed`, or `canceled`, in RFC 3339, or `null` if it is still `pending` or `running`.

    format: date-time

  - `error: Optional[BetaDreamError]`

    Why the dream failed, or `null` if `status` isn't `failed`.

    - `type: str`

      A code for why the dream failed, such as `timeout` or `internal_error`.

      The [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=python#errors) lists common error codes and when they occur.

    - `message: str`

      A human-readable explanation of why the dream failed.

  - `inputs: List[BetaDreamInput]`

    The sources that the dream reads, from the request that created it.

    - `class BetaDreamMemoryStoreInput`

      The memory store that a dream reads, given as an entry in `inputs`.

      With `output_behavior` set to `update_existing`, the dream writes its result into this memory store. Otherwise the dream doesn't change it.

      - `type: Literal["memory_store"]`

      - `memory_store_id: str`

        The ID of the memory store for the dream to read (`memstore_...`).

        The memory store must be in the same workspace as the dream and must not be archived.

        minLength: 1

    - `class BetaDreamSessionsInput`

      The sessions that a dream reads, given as an entry in `inputs`.

      - `type: Literal["sessions"]`

      - `session_ids: List[str]`

        The IDs of the sessions whose transcripts the dream reads (`sesn_...`).

        Give 1 to 100 IDs, with no duplicates. Each session must be in the same workspace as the dream. Responses list the IDs in sorted order.

  - `instructions: Optional[str]`

    The guidance given when the dream was created, or `null` if none was given.

  - `model: BetaDreamModelConfig`

    The model that runs a dream, from the request that created it.

    The dream uses this model for all of its work. The response always gives the model as an object, even if the request gave only a model ID.

    - `id: str`

      The ID of the model that runs the dream, as given in the request that created it.

      minLength: 1, maxLength: 256

    - `speed: Optional[Literal["standard", "fast"]]`

      How fast the model generates output for the dream. Always `standard`.

      - `"standard"`

      - `"fast"`

  - `output_behavior: BetaOutputBehavior`

    Where the dream writes its result, as set in the request that created the dream. If that request left out `output_behavior`, the dream used the `create_new` behavior.

    - `class BetaOutputBehaviorCreateNew`

      Write the result to a new memory store that starts as a copy of the input memory store. This is the default.

      The new memory store is in the same workspace as the dream. The dream doesn't change the input memory store.

      - `type: Literal["create_new"]`

    - `class BetaOutputBehaviorUpdateExisting`

      Write the result into the input memory store instead of a new memory store.

      The credential must be allowed to write memory stores, or the request returns a 403 error. While another `update_existing` dream on the same memory store hasn't fully stopped, the request returns a 409 error.

      - `type: Literal["update_existing"]`

      - `memory_store_id: str`

        The ID of the memory store for the dream to write its result to (`memstore_...`). It must be the memory store in the `memory_store` entry of `inputs`.

        minLength: 1

  - `outputs: List[BetaDreamOutput]`

    The memory store that holds the dream's result, as a one-item array, or an empty array until the dream records that memory store.

    The array is empty while the dream is `pending` and for a short time after it starts `running`. It can stay empty if the dream fails or is canceled before then. The memory store holds the complete result only once `status` is `completed`.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=python#use-the-output) for how to review and use the result.

    - `type: Literal["memory_store"]`

    - `memory_store_id: str`

      The ID of the memory store that the dream writes its result to (`memstore_...`).

      With `output_behavior` set to `create_new`, this is a new memory store. With `update_existing`, it is the input memory store.

  - `session_id: Optional[str]`

    The ID of the session that runs the dream (`sesn_...`), or `null` if that session hasn't started.

    Stream that session's events to follow what the dream reads and writes.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=python#watch-the-pipeline-run) for how to watch a running dream.

  - `status: BetaDreamStatus`

    Where a dream is in its lifecycle.

    `completed`, `failed`, and `canceled` are final: once a dream has one of these statuses, its status doesn't change again.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=python#lifecycle) for what each status means.

    - `"pending"`

      The dream is waiting to start and hasn't read its inputs yet.

      `outputs` is empty and every `usage` count is zero.

    - `"running"`

      The dream is reading its inputs and writing its result.

      `usage` updates while the dream has this status.

    - `"completed"`

      The dream finished and its output memory store holds the complete result.

    - `"failed"`

      The dream stopped with an error, which `error` describes.

      If `outputs` references a memory store, that memory store keeps what the dream wrote before it stopped.

    - `"canceled"`

      A cancel request stopped the dream before it reached `completed` or `failed`.

      If `outputs` references a memory store, that memory store keeps what the dream wrote. `usage` can keep changing after the cancel.

  - `usage: BetaDreamUsage`

    The dream's token counts, which stop changing once its `status` is `completed` or `failed`. After a cancel, they can keep changing.

    - `cache_creation_input_tokens: int`

      The dream's input tokens that were written to the prompt cache, for both the 5-minute and 1-hour cache durations.

      format: int32

    - `cache_read_input_tokens: int`

      The dream's input tokens that were read from the prompt cache.

      format: int32

    - `input_tokens: int`

      The dream's input tokens that weren't read from or written to the prompt cache.

      format: int32

    - `output_tokens: int`

      The tokens that the model generated for the dream.

      format: int32

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.dreams.list()
page = page.data[0]
print(page.id)
```

### Response (200)

```json
{
  "data": [
    {
      "id": "id",
      "archived_at": "2019-12-27T18:11:19.117Z",
      "created_at": "2019-12-27T18:11:19.117Z",
      "ended_at": "2019-12-27T18:11:19.117Z",
      "error": {
        "message": "message",
        "type": "type"
      },
      "inputs": [
        {
          "memory_store_id": "x",
          "type": "memory_store"
        }
      ],
      "instructions": "instructions",
      "model": {
        "id": "x",
        "speed": "standard"
      },
      "output_behavior": {
        "type": "create_new"
      },
      "outputs": [
        {
          "memory_store_id": "memory_store_id",
          "type": "memory_store"
        }
      ],
      "session_id": "session_id",
      "status": "pending",
      "type": "dream",
      "usage": {
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "input_tokens": 0,
        "output_tokens": 0
      }
    }
  ],
  "next_page": "next_page"
}
```
