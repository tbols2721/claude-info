---
title: Dreams
url: https://platform.claude.com/docs/en/api/cli/beta/dreams
---

# Dreams

## Create a Dream

`$ ant beta:dreams create`

**POST** `/v1/dreams`

Start an asynchronous job that uses past sessions to produce a reorganized version of a memory store and get back the dream to poll for the result.

By default the dream writes its result to a new memory store and doesn't change the input memory store. The response has `status` set to `pending` and an empty `outputs` array. Poll the dream until `status` is `completed`, `failed`, or `canceled`.

See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#create-a-dream) to learn more about creating dreams.

### Parameters

- `--input: array of BetaDreamInput`

  The memory store and sessions for the dream to read, as exactly one `memory_store` entry and exactly one `sessions` entry.

  - `beta_dream_memory_store_input: object`

    The memory store that a dream reads, given as an entry in `inputs`.

    With `output_behavior` set to `update_existing`, the dream writes its result into this memory store. Otherwise the dream doesn't change it.

    - `type: "memory_store"`

    - `memory_store_id: string`

      The ID of the memory store for the dream to read (`memstore_...`).

      The memory store must be in the same workspace as the dream and must not be archived.

      minLength: 1

  - `beta_dream_sessions_input: object`

    The sessions that a dream reads, given as an entry in `inputs`.

    - `type: "sessions"`

    - `session_ids: array of string`

      The IDs of the sessions whose transcripts the dream reads (`sesn_...`).

      Give 1 to 100 IDs, with no duplicates. Each session must be in the same workspace as the dream. Responses list the IDs in sorted order.

- `--model: string or BetaDreamModelConfigParam`

  The model that runs a dream, given as a model ID or as an object with `id` and `speed`.

  In the object form, `speed` can only be `standard`.

  The [Availability section of the Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#feature-availability) lists the supported models.

  - `union_member_0: string`

  - `beta_dream_model_config_param: object`

    The object form of `model` in a request to create a dream.

    - `id: string`

      The ID of the model to run the dream with.

      The ID can be 1 to 256 characters long.

      The [Availability section of the Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#feature-availability) lists the supported models.

      minLength: 1, maxLength: 256

    - `speed: optional "standard" or "fast"`

      How fast the model generates output for the dream. Defaults to `standard`.

      Dreams accept only `standard`.

      - `"standard"`

      - `"fast"`

- `--instructions: optional string`

  Guidance that steers how the dream reads the sessions and organizes the output memory store, from 1 to 4,096 characters.

  See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#steer-with-instructions) for what kinds of instructions work well.

  minLength: 1, maxLength: 4096

- `--output-behavior: optional BetaOutputBehavior`

  Which memory store a dream writes its result to. Defaults to `create_new` when left out of a create request.

  - `beta_output_behavior_create_new: object`

    Write the result to a new memory store that starts as a copy of the input memory store. This is the default.

    The new memory store is in the same workspace as the dream. The dream doesn't change the input memory store.

    - `type: "create_new"`

  - `beta_output_behavior_update_existing: object`

    Write the result into the input memory store instead of a new memory store.

    The credential must be allowed to write memory stores, or the request returns a 403 error. While another `update_existing` dream on the same memory store hasn't fully stopped, the request returns a 409 error.

    - `type: "update_existing"`

    - `memory_store_id: string`

      The ID of the memory store for the dream to write its result to (`memstore_...`). It must be the memory store in the `memory_store` entry of `inputs`.

      minLength: 1

- `--beta: optional array of AnthropicBeta` (header parameter)

  This endpoint is in beta: requests must send `dreaming-2026-04-21` in this header.

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

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

- `--workspace-id: optional string` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `beta_dream: object`

  An asynchronous job that reads a memory store and past sessions, then writes a reorganized version of that memory store.

  By default the dream writes its result to a new memory store and doesn't change the input memory store. With `output_behavior` set to `update_existing`, it writes its result into the input memory store instead.

  The Dreams API is in research preview: the request and response shapes are volatile and may change without the deprecation period that applies to stable endpoints.

  See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#how-it-works) for what a dream reads and produces.

  - `type: "dream"`

  - `id: string`

    The unique ID of the dream (`drm_...`).

  - `archived_at: string`

    When the dream was archived, in RFC 3339, or `null` if it hasn't been archived.

    format: date-time

  - `created_at: string`

    When the dream was created, in RFC 3339.

    Lists of dreams are sorted by this time, newest first.

    format: date-time

  - `ended_at: string`

    When the dream reached `completed`, `failed`, or `canceled`, in RFC 3339, or `null` if it is still `pending` or `running`.

    format: date-time

  - `error: object`

    Why the dream failed, or `null` if `status` isn't `failed`.

    - `type: string`

      A code for why the dream failed, such as `timeout` or `internal_error`.

      The [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#errors) lists common error codes and when they occur.

    - `message: string`

      A human-readable explanation of why the dream failed.

  - `inputs: array of BetaDreamInput`

    The sources that the dream reads, from the request that created it.

    - `beta_dream_memory_store_input: object`

      The memory store that a dream reads, given as an entry in `inputs`.

      With `output_behavior` set to `update_existing`, the dream writes its result into this memory store. Otherwise the dream doesn't change it.

      - `type: "memory_store"`

      - `memory_store_id: string`

        The ID of the memory store for the dream to read (`memstore_...`).

        The memory store must be in the same workspace as the dream and must not be archived.

        minLength: 1

    - `beta_dream_sessions_input: object`

      The sessions that a dream reads, given as an entry in `inputs`.

      - `type: "sessions"`

      - `session_ids: array of string`

        The IDs of the sessions whose transcripts the dream reads (`sesn_...`).

        Give 1 to 100 IDs, with no duplicates. Each session must be in the same workspace as the dream. Responses list the IDs in sorted order.

  - `instructions: string`

    The guidance given when the dream was created, or `null` if none was given.

  - `model: object`

    The model that runs a dream, from the request that created it.

    The dream uses this model for all of its work. The response always gives the model as an object, even if the request gave only a model ID.

    - `id: string`

      The ID of the model that runs the dream, as given in the request that created it.

      minLength: 1, maxLength: 256

    - `speed: optional "standard" or "fast"`

      How fast the model generates output for the dream. Always `standard`.

      - `"standard"`

      - `"fast"`

  - `output_behavior: BetaOutputBehaviorCreateNew or BetaOutputBehaviorUpdateExisting`

    Where the dream writes its result, as set in the request that created the dream. If that request left out `output_behavior`, the dream used the `create_new` behavior.

    - `beta_output_behavior_create_new: object`

      Write the result to a new memory store that starts as a copy of the input memory store. This is the default.

      The new memory store is in the same workspace as the dream. The dream doesn't change the input memory store.

      - `type: "create_new"`

    - `beta_output_behavior_update_existing: object`

      Write the result into the input memory store instead of a new memory store.

      The credential must be allowed to write memory stores, or the request returns a 403 error. While another `update_existing` dream on the same memory store hasn't fully stopped, the request returns a 409 error.

      - `type: "update_existing"`

      - `memory_store_id: string`

        The ID of the memory store for the dream to write its result to (`memstore_...`). It must be the memory store in the `memory_store` entry of `inputs`.

        minLength: 1

  - `outputs: array of BetaDreamOutput`

    The memory store that holds the dream's result, as a one-item array, or an empty array until the dream records that memory store.

    The array is empty while the dream is `pending` and for a short time after it starts `running`. It can stay empty if the dream fails or is canceled before then. The memory store holds the complete result only once `status` is `completed`.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#use-the-output) for how to review and use the result.

    - `type: "memory_store"`

    - `memory_store_id: string`

      The ID of the memory store that the dream writes its result to (`memstore_...`).

      With `output_behavior` set to `create_new`, this is a new memory store. With `update_existing`, it is the input memory store.

  - `session_id: string`

    The ID of the session that runs the dream (`sesn_...`), or `null` if that session hasn't started.

    Stream that session's events to follow what the dream reads and writes.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#watch-the-pipeline-run) for how to watch a running dream.

  - `status: "pending" or "running" or "completed" or 2 more`

    Where a dream is in its lifecycle.

    `completed`, `failed`, and `canceled` are final: once a dream has one of these statuses, its status doesn't change again.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#lifecycle) for what each status means.

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

  - `usage: object`

    The dream's token counts, which stop changing once its `status` is `completed` or `failed`. After a cancel, they can keep changing.

    - `cache_creation_input_tokens: number`

      The dream's input tokens that were written to the prompt cache, for both the 5-minute and 1-hour cache durations.

      format: int32

    - `cache_read_input_tokens: number`

      The dream's input tokens that were read from the prompt cache.

      format: int32

    - `input_tokens: number`

      The dream's input tokens that weren't read from or written to the prompt cache.

      format: int32

    - `output_tokens: number`

      The tokens that the model generated for the dream.

      format: int32

### Example

```bash
ant beta:dreams create \
  --input '{memory_store_id: x, type: memory_store}' \
  --model string
```

#### Response (200)

```json
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
```

## List Dreams

`$ ant beta:dreams list`

**GET** `/v1/dreams`

List the dreams in the workspace, newest first.

Archived dreams are left out unless `include_archived` is `true`.

See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#list-dreams) for how to page through dreams.

### Parameters

- `--created-at-gt: optional string` (query parameter)

  Return only dreams created after this time (exclusive), in RFC 3339.

  format: date-time

- `--created-at-lt: optional string` (query parameter)

  Return only dreams created before this time (exclusive), in RFC 3339.

  format: date-time

- `--include-archived: optional boolean` (query parameter)

  Whether to include archived dreams. Defaults to `false`.

- `--limit: optional number` (query parameter)

  The maximum number of dreams to return, from 1 to 100. Defaults to 20.

  format: int32

- `--page: optional string` (query parameter)

  The cursor for the page to return, taken from `next_page` in a previous response.

  Leave it out to get the first page.

- `--status: optional array of BetaDreamStatus` (query parameter)

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

- `--beta: optional array of AnthropicBeta` (header parameter)

  This endpoint is in beta: requests must send `dreaming-2026-04-21` in this header.

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

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

- `--workspace-id: optional string` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `BetaListDreamsResponse: object`

  A page of dreams, newest first.

  - `data: array of BetaDream`

    The dreams on this page, newest first.

    - `type: "dream"`

    - `id: string`

      The unique ID of the dream (`drm_...`).

    - `archived_at: string`

      When the dream was archived, in RFC 3339, or `null` if it hasn't been archived.

      format: date-time

    - `created_at: string`

      When the dream was created, in RFC 3339.

      Lists of dreams are sorted by this time, newest first.

      format: date-time

    - `ended_at: string`

      When the dream reached `completed`, `failed`, or `canceled`, in RFC 3339, or `null` if it is still `pending` or `running`.

      format: date-time

    - `error: object`

      Why the dream failed, or `null` if `status` isn't `failed`.

      - `type: string`

        A code for why the dream failed, such as `timeout` or `internal_error`.

        The [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#errors) lists common error codes and when they occur.

      - `message: string`

        A human-readable explanation of why the dream failed.

    - `inputs: array of BetaDreamInput`

      The sources that the dream reads, from the request that created it.

      - `beta_dream_memory_store_input: object`

        The memory store that a dream reads, given as an entry in `inputs`.

        With `output_behavior` set to `update_existing`, the dream writes its result into this memory store. Otherwise the dream doesn't change it.

        - `type: "memory_store"`

        - `memory_store_id: string`

          The ID of the memory store for the dream to read (`memstore_...`).

          The memory store must be in the same workspace as the dream and must not be archived.

          minLength: 1

      - `beta_dream_sessions_input: object`

        The sessions that a dream reads, given as an entry in `inputs`.

        - `type: "sessions"`

        - `session_ids: array of string`

          The IDs of the sessions whose transcripts the dream reads (`sesn_...`).

          Give 1 to 100 IDs, with no duplicates. Each session must be in the same workspace as the dream. Responses list the IDs in sorted order.

    - `instructions: string`

      The guidance given when the dream was created, or `null` if none was given.

    - `model: object`

      The model that runs a dream, from the request that created it.

      The dream uses this model for all of its work. The response always gives the model as an object, even if the request gave only a model ID.

      - `id: string`

        The ID of the model that runs the dream, as given in the request that created it.

        minLength: 1, maxLength: 256

      - `speed: optional "standard" or "fast"`

        How fast the model generates output for the dream. Always `standard`.

        - `"standard"`

        - `"fast"`

    - `output_behavior: BetaOutputBehaviorCreateNew or BetaOutputBehaviorUpdateExisting`

      Where the dream writes its result, as set in the request that created the dream. If that request left out `output_behavior`, the dream used the `create_new` behavior.

      - `beta_output_behavior_create_new: object`

        Write the result to a new memory store that starts as a copy of the input memory store. This is the default.

        The new memory store is in the same workspace as the dream. The dream doesn't change the input memory store.

        - `type: "create_new"`

      - `beta_output_behavior_update_existing: object`

        Write the result into the input memory store instead of a new memory store.

        The credential must be allowed to write memory stores, or the request returns a 403 error. While another `update_existing` dream on the same memory store hasn't fully stopped, the request returns a 409 error.

        - `type: "update_existing"`

        - `memory_store_id: string`

          The ID of the memory store for the dream to write its result to (`memstore_...`). It must be the memory store in the `memory_store` entry of `inputs`.

          minLength: 1

    - `outputs: array of BetaDreamOutput`

      The memory store that holds the dream's result, as a one-item array, or an empty array until the dream records that memory store.

      The array is empty while the dream is `pending` and for a short time after it starts `running`. It can stay empty if the dream fails or is canceled before then. The memory store holds the complete result only once `status` is `completed`.

      See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#use-the-output) for how to review and use the result.

      - `type: "memory_store"`

      - `memory_store_id: string`

        The ID of the memory store that the dream writes its result to (`memstore_...`).

        With `output_behavior` set to `create_new`, this is a new memory store. With `update_existing`, it is the input memory store.

    - `session_id: string`

      The ID of the session that runs the dream (`sesn_...`), or `null` if that session hasn't started.

      Stream that session's events to follow what the dream reads and writes.

      See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#watch-the-pipeline-run) for how to watch a running dream.

    - `status: "pending" or "running" or "completed" or 2 more`

      Where a dream is in its lifecycle.

      `completed`, `failed`, and `canceled` are final: once a dream has one of these statuses, its status doesn't change again.

      See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#lifecycle) for what each status means.

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

    - `usage: object`

      The dream's token counts, which stop changing once its `status` is `completed` or `failed`. After a cancel, they can keep changing.

      - `cache_creation_input_tokens: number`

        The dream's input tokens that were written to the prompt cache, for both the 5-minute and 1-hour cache durations.

        format: int32

      - `cache_read_input_tokens: number`

        The dream's input tokens that were read from the prompt cache.

        format: int32

      - `input_tokens: number`

        The dream's input tokens that weren't read from or written to the prompt cache.

        format: int32

      - `output_tokens: number`

        The tokens that the model generated for the dream.

        format: int32

  - `next_page: string`

    The cursor for the next page, or `null` if this is the last page.

    Pass it as `page` to get the next page.

### Example

```bash
ant beta:dreams list
```

#### Response (200)

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

## Get a Dream

`$ ant beta:dreams retrieve`

**GET** `/v1/dreams/{dream_id}`

Get a dream by ID to check its status, output memory store, and token usage.

Archived dreams are returned too.

See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#track-progress) for how to poll a dream and what each status means.

### Parameters

- `--dream-id: string` (path parameter)

  The ID of the dream to get (`drm_...`).

- `--beta: optional array of AnthropicBeta` (header parameter)

  This endpoint is in beta: requests must send `dreaming-2026-04-21` in this header.

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

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

- `--workspace-id: optional string` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `beta_dream: object`

  An asynchronous job that reads a memory store and past sessions, then writes a reorganized version of that memory store.

  By default the dream writes its result to a new memory store and doesn't change the input memory store. With `output_behavior` set to `update_existing`, it writes its result into the input memory store instead.

  The Dreams API is in research preview: the request and response shapes are volatile and may change without the deprecation period that applies to stable endpoints.

  See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#how-it-works) for what a dream reads and produces.

  - `type: "dream"`

  - `id: string`

    The unique ID of the dream (`drm_...`).

  - `archived_at: string`

    When the dream was archived, in RFC 3339, or `null` if it hasn't been archived.

    format: date-time

  - `created_at: string`

    When the dream was created, in RFC 3339.

    Lists of dreams are sorted by this time, newest first.

    format: date-time

  - `ended_at: string`

    When the dream reached `completed`, `failed`, or `canceled`, in RFC 3339, or `null` if it is still `pending` or `running`.

    format: date-time

  - `error: object`

    Why the dream failed, or `null` if `status` isn't `failed`.

    - `type: string`

      A code for why the dream failed, such as `timeout` or `internal_error`.

      The [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#errors) lists common error codes and when they occur.

    - `message: string`

      A human-readable explanation of why the dream failed.

  - `inputs: array of BetaDreamInput`

    The sources that the dream reads, from the request that created it.

    - `beta_dream_memory_store_input: object`

      The memory store that a dream reads, given as an entry in `inputs`.

      With `output_behavior` set to `update_existing`, the dream writes its result into this memory store. Otherwise the dream doesn't change it.

      - `type: "memory_store"`

      - `memory_store_id: string`

        The ID of the memory store for the dream to read (`memstore_...`).

        The memory store must be in the same workspace as the dream and must not be archived.

        minLength: 1

    - `beta_dream_sessions_input: object`

      The sessions that a dream reads, given as an entry in `inputs`.

      - `type: "sessions"`

      - `session_ids: array of string`

        The IDs of the sessions whose transcripts the dream reads (`sesn_...`).

        Give 1 to 100 IDs, with no duplicates. Each session must be in the same workspace as the dream. Responses list the IDs in sorted order.

  - `instructions: string`

    The guidance given when the dream was created, or `null` if none was given.

  - `model: object`

    The model that runs a dream, from the request that created it.

    The dream uses this model for all of its work. The response always gives the model as an object, even if the request gave only a model ID.

    - `id: string`

      The ID of the model that runs the dream, as given in the request that created it.

      minLength: 1, maxLength: 256

    - `speed: optional "standard" or "fast"`

      How fast the model generates output for the dream. Always `standard`.

      - `"standard"`

      - `"fast"`

  - `output_behavior: BetaOutputBehaviorCreateNew or BetaOutputBehaviorUpdateExisting`

    Where the dream writes its result, as set in the request that created the dream. If that request left out `output_behavior`, the dream used the `create_new` behavior.

    - `beta_output_behavior_create_new: object`

      Write the result to a new memory store that starts as a copy of the input memory store. This is the default.

      The new memory store is in the same workspace as the dream. The dream doesn't change the input memory store.

      - `type: "create_new"`

    - `beta_output_behavior_update_existing: object`

      Write the result into the input memory store instead of a new memory store.

      The credential must be allowed to write memory stores, or the request returns a 403 error. While another `update_existing` dream on the same memory store hasn't fully stopped, the request returns a 409 error.

      - `type: "update_existing"`

      - `memory_store_id: string`

        The ID of the memory store for the dream to write its result to (`memstore_...`). It must be the memory store in the `memory_store` entry of `inputs`.

        minLength: 1

  - `outputs: array of BetaDreamOutput`

    The memory store that holds the dream's result, as a one-item array, or an empty array until the dream records that memory store.

    The array is empty while the dream is `pending` and for a short time after it starts `running`. It can stay empty if the dream fails or is canceled before then. The memory store holds the complete result only once `status` is `completed`.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#use-the-output) for how to review and use the result.

    - `type: "memory_store"`

    - `memory_store_id: string`

      The ID of the memory store that the dream writes its result to (`memstore_...`).

      With `output_behavior` set to `create_new`, this is a new memory store. With `update_existing`, it is the input memory store.

  - `session_id: string`

    The ID of the session that runs the dream (`sesn_...`), or `null` if that session hasn't started.

    Stream that session's events to follow what the dream reads and writes.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#watch-the-pipeline-run) for how to watch a running dream.

  - `status: "pending" or "running" or "completed" or 2 more`

    Where a dream is in its lifecycle.

    `completed`, `failed`, and `canceled` are final: once a dream has one of these statuses, its status doesn't change again.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#lifecycle) for what each status means.

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

  - `usage: object`

    The dream's token counts, which stop changing once its `status` is `completed` or `failed`. After a cancel, they can keep changing.

    - `cache_creation_input_tokens: number`

      The dream's input tokens that were written to the prompt cache, for both the 5-minute and 1-hour cache durations.

      format: int32

    - `cache_read_input_tokens: number`

      The dream's input tokens that were read from the prompt cache.

      format: int32

    - `input_tokens: number`

      The dream's input tokens that weren't read from or written to the prompt cache.

      format: int32

    - `output_tokens: number`

      The tokens that the model generated for the dream.

      format: int32

### Example

```bash
ant beta:dreams retrieve \
  --dream-id dream_id
```

#### Response (200)

```json
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
```

## Cancel a Dream

`$ ant beta:dreams cancel`

**POST** `/v1/dreams/{dream_id}/cancel`

Stop a `pending` or `running` dream.

The response shows `status` as `canceled`, unless the dream reached `completed` or `failed` first. `usage` can keep changing after the response. Canceling a `canceled` dream returns it unchanged. Canceling a `completed` or `failed` dream returns a 400 error.

See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#cancel-a-dream) to learn more about canceling dreams.

### Parameters

- `--dream-id: string` (path parameter)

  The ID of the dream to cancel (`drm_...`).

- `--beta: optional array of AnthropicBeta` (header parameter)

  This endpoint is in beta: requests must send `dreaming-2026-04-21` in this header.

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

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

- `--workspace-id: optional string` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `beta_dream: object`

  An asynchronous job that reads a memory store and past sessions, then writes a reorganized version of that memory store.

  By default the dream writes its result to a new memory store and doesn't change the input memory store. With `output_behavior` set to `update_existing`, it writes its result into the input memory store instead.

  The Dreams API is in research preview: the request and response shapes are volatile and may change without the deprecation period that applies to stable endpoints.

  See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#how-it-works) for what a dream reads and produces.

  - `type: "dream"`

  - `id: string`

    The unique ID of the dream (`drm_...`).

  - `archived_at: string`

    When the dream was archived, in RFC 3339, or `null` if it hasn't been archived.

    format: date-time

  - `created_at: string`

    When the dream was created, in RFC 3339.

    Lists of dreams are sorted by this time, newest first.

    format: date-time

  - `ended_at: string`

    When the dream reached `completed`, `failed`, or `canceled`, in RFC 3339, or `null` if it is still `pending` or `running`.

    format: date-time

  - `error: object`

    Why the dream failed, or `null` if `status` isn't `failed`.

    - `type: string`

      A code for why the dream failed, such as `timeout` or `internal_error`.

      The [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#errors) lists common error codes and when they occur.

    - `message: string`

      A human-readable explanation of why the dream failed.

  - `inputs: array of BetaDreamInput`

    The sources that the dream reads, from the request that created it.

    - `beta_dream_memory_store_input: object`

      The memory store that a dream reads, given as an entry in `inputs`.

      With `output_behavior` set to `update_existing`, the dream writes its result into this memory store. Otherwise the dream doesn't change it.

      - `type: "memory_store"`

      - `memory_store_id: string`

        The ID of the memory store for the dream to read (`memstore_...`).

        The memory store must be in the same workspace as the dream and must not be archived.

        minLength: 1

    - `beta_dream_sessions_input: object`

      The sessions that a dream reads, given as an entry in `inputs`.

      - `type: "sessions"`

      - `session_ids: array of string`

        The IDs of the sessions whose transcripts the dream reads (`sesn_...`).

        Give 1 to 100 IDs, with no duplicates. Each session must be in the same workspace as the dream. Responses list the IDs in sorted order.

  - `instructions: string`

    The guidance given when the dream was created, or `null` if none was given.

  - `model: object`

    The model that runs a dream, from the request that created it.

    The dream uses this model for all of its work. The response always gives the model as an object, even if the request gave only a model ID.

    - `id: string`

      The ID of the model that runs the dream, as given in the request that created it.

      minLength: 1, maxLength: 256

    - `speed: optional "standard" or "fast"`

      How fast the model generates output for the dream. Always `standard`.

      - `"standard"`

      - `"fast"`

  - `output_behavior: BetaOutputBehaviorCreateNew or BetaOutputBehaviorUpdateExisting`

    Where the dream writes its result, as set in the request that created the dream. If that request left out `output_behavior`, the dream used the `create_new` behavior.

    - `beta_output_behavior_create_new: object`

      Write the result to a new memory store that starts as a copy of the input memory store. This is the default.

      The new memory store is in the same workspace as the dream. The dream doesn't change the input memory store.

      - `type: "create_new"`

    - `beta_output_behavior_update_existing: object`

      Write the result into the input memory store instead of a new memory store.

      The credential must be allowed to write memory stores, or the request returns a 403 error. While another `update_existing` dream on the same memory store hasn't fully stopped, the request returns a 409 error.

      - `type: "update_existing"`

      - `memory_store_id: string`

        The ID of the memory store for the dream to write its result to (`memstore_...`). It must be the memory store in the `memory_store` entry of `inputs`.

        minLength: 1

  - `outputs: array of BetaDreamOutput`

    The memory store that holds the dream's result, as a one-item array, or an empty array until the dream records that memory store.

    The array is empty while the dream is `pending` and for a short time after it starts `running`. It can stay empty if the dream fails or is canceled before then. The memory store holds the complete result only once `status` is `completed`.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#use-the-output) for how to review and use the result.

    - `type: "memory_store"`

    - `memory_store_id: string`

      The ID of the memory store that the dream writes its result to (`memstore_...`).

      With `output_behavior` set to `create_new`, this is a new memory store. With `update_existing`, it is the input memory store.

  - `session_id: string`

    The ID of the session that runs the dream (`sesn_...`), or `null` if that session hasn't started.

    Stream that session's events to follow what the dream reads and writes.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#watch-the-pipeline-run) for how to watch a running dream.

  - `status: "pending" or "running" or "completed" or 2 more`

    Where a dream is in its lifecycle.

    `completed`, `failed`, and `canceled` are final: once a dream has one of these statuses, its status doesn't change again.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#lifecycle) for what each status means.

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

  - `usage: object`

    The dream's token counts, which stop changing once its `status` is `completed` or `failed`. After a cancel, they can keep changing.

    - `cache_creation_input_tokens: number`

      The dream's input tokens that were written to the prompt cache, for both the 5-minute and 1-hour cache durations.

      format: int32

    - `cache_read_input_tokens: number`

      The dream's input tokens that were read from the prompt cache.

      format: int32

    - `input_tokens: number`

      The dream's input tokens that weren't read from or written to the prompt cache.

      format: int32

    - `output_tokens: number`

      The tokens that the model generated for the dream.

      format: int32

### Example

```bash
ant beta:dreams cancel \
  --dream-id dream_id
```

#### Response (200)

```json
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
```

## Archive a Dream

`$ ant beta:dreams archive`

**POST** `/v1/dreams/{dream_id}/archive`

Hide a `completed`, `failed`, or `canceled` dream from the default list of dreams.

Archiving a `pending` or `running` dream returns a 400 error, so cancel it first. Archiving an archived dream returns it unchanged. An archived dream can still be fetched by ID. Archiving can't be undone.

See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#archive-a-dream) to learn more about archiving dreams.

### Parameters

- `--dream-id: string` (path parameter)

  The ID of the dream to archive (`drm_...`).

- `--beta: optional array of AnthropicBeta` (header parameter)

  This endpoint is in beta: requests must send `dreaming-2026-04-21` in this header.

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

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

- `--workspace-id: optional string` (header parameter)

  Optional header to select the Workspace for this request. The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

  Only needed for credentials that can act on more than one Workspace. A credential that belongs to a specific Workspace may omit it; if sent, it must match that Workspace.

### Returns

- `beta_dream: object`

  An asynchronous job that reads a memory store and past sessions, then writes a reorganized version of that memory store.

  By default the dream writes its result to a new memory store and doesn't change the input memory store. With `output_behavior` set to `update_existing`, it writes its result into the input memory store instead.

  The Dreams API is in research preview: the request and response shapes are volatile and may change without the deprecation period that applies to stable endpoints.

  See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#how-it-works) for what a dream reads and produces.

  - `type: "dream"`

  - `id: string`

    The unique ID of the dream (`drm_...`).

  - `archived_at: string`

    When the dream was archived, in RFC 3339, or `null` if it hasn't been archived.

    format: date-time

  - `created_at: string`

    When the dream was created, in RFC 3339.

    Lists of dreams are sorted by this time, newest first.

    format: date-time

  - `ended_at: string`

    When the dream reached `completed`, `failed`, or `canceled`, in RFC 3339, or `null` if it is still `pending` or `running`.

    format: date-time

  - `error: object`

    Why the dream failed, or `null` if `status` isn't `failed`.

    - `type: string`

      A code for why the dream failed, such as `timeout` or `internal_error`.

      The [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#errors) lists common error codes and when they occur.

    - `message: string`

      A human-readable explanation of why the dream failed.

  - `inputs: array of BetaDreamInput`

    The sources that the dream reads, from the request that created it.

    - `beta_dream_memory_store_input: object`

      The memory store that a dream reads, given as an entry in `inputs`.

      With `output_behavior` set to `update_existing`, the dream writes its result into this memory store. Otherwise the dream doesn't change it.

      - `type: "memory_store"`

      - `memory_store_id: string`

        The ID of the memory store for the dream to read (`memstore_...`).

        The memory store must be in the same workspace as the dream and must not be archived.

        minLength: 1

    - `beta_dream_sessions_input: object`

      The sessions that a dream reads, given as an entry in `inputs`.

      - `type: "sessions"`

      - `session_ids: array of string`

        The IDs of the sessions whose transcripts the dream reads (`sesn_...`).

        Give 1 to 100 IDs, with no duplicates. Each session must be in the same workspace as the dream. Responses list the IDs in sorted order.

  - `instructions: string`

    The guidance given when the dream was created, or `null` if none was given.

  - `model: object`

    The model that runs a dream, from the request that created it.

    The dream uses this model for all of its work. The response always gives the model as an object, even if the request gave only a model ID.

    - `id: string`

      The ID of the model that runs the dream, as given in the request that created it.

      minLength: 1, maxLength: 256

    - `speed: optional "standard" or "fast"`

      How fast the model generates output for the dream. Always `standard`.

      - `"standard"`

      - `"fast"`

  - `output_behavior: BetaOutputBehaviorCreateNew or BetaOutputBehaviorUpdateExisting`

    Where the dream writes its result, as set in the request that created the dream. If that request left out `output_behavior`, the dream used the `create_new` behavior.

    - `beta_output_behavior_create_new: object`

      Write the result to a new memory store that starts as a copy of the input memory store. This is the default.

      The new memory store is in the same workspace as the dream. The dream doesn't change the input memory store.

      - `type: "create_new"`

    - `beta_output_behavior_update_existing: object`

      Write the result into the input memory store instead of a new memory store.

      The credential must be allowed to write memory stores, or the request returns a 403 error. While another `update_existing` dream on the same memory store hasn't fully stopped, the request returns a 409 error.

      - `type: "update_existing"`

      - `memory_store_id: string`

        The ID of the memory store for the dream to write its result to (`memstore_...`). It must be the memory store in the `memory_store` entry of `inputs`.

        minLength: 1

  - `outputs: array of BetaDreamOutput`

    The memory store that holds the dream's result, as a one-item array, or an empty array until the dream records that memory store.

    The array is empty while the dream is `pending` and for a short time after it starts `running`. It can stay empty if the dream fails or is canceled before then. The memory store holds the complete result only once `status` is `completed`.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#use-the-output) for how to review and use the result.

    - `type: "memory_store"`

    - `memory_store_id: string`

      The ID of the memory store that the dream writes its result to (`memstore_...`).

      With `output_behavior` set to `create_new`, this is a new memory store. With `update_existing`, it is the input memory store.

  - `session_id: string`

    The ID of the session that runs the dream (`sesn_...`), or `null` if that session hasn't started.

    Stream that session's events to follow what the dream reads and writes.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#watch-the-pipeline-run) for how to watch a running dream.

  - `status: "pending" or "running" or "completed" or 2 more`

    Where a dream is in its lifecycle.

    `completed`, `failed`, and `canceled` are final: once a dream has one of these statuses, its status doesn't change again.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#lifecycle) for what each status means.

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

  - `usage: object`

    The dream's token counts, which stop changing once its `status` is `completed` or `failed`. After a cancel, they can keep changing.

    - `cache_creation_input_tokens: number`

      The dream's input tokens that were written to the prompt cache, for both the 5-minute and 1-hour cache durations.

      format: int32

    - `cache_read_input_tokens: number`

      The dream's input tokens that were read from the prompt cache.

      format: int32

    - `input_tokens: number`

      The dream's input tokens that weren't read from or written to the prompt cache.

      format: int32

    - `output_tokens: number`

      The tokens that the model generated for the dream.

      format: int32

### Example

```bash
ant beta:dreams archive \
  --dream-id dream_id
```

#### Response (200)

```json
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
```

## Domain types

### Beta Dream

- `beta_dream: object`

  An asynchronous job that reads a memory store and past sessions, then writes a reorganized version of that memory store.

  By default the dream writes its result to a new memory store and doesn't change the input memory store. With `output_behavior` set to `update_existing`, it writes its result into the input memory store instead.

  The Dreams API is in research preview: the request and response shapes are volatile and may change without the deprecation period that applies to stable endpoints.

  See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#how-it-works) for what a dream reads and produces.

  - `type: "dream"`

  - `id: string`

    The unique ID of the dream (`drm_...`).

  - `archived_at: string`

    When the dream was archived, in RFC 3339, or `null` if it hasn't been archived.

    format: date-time

  - `created_at: string`

    When the dream was created, in RFC 3339.

    Lists of dreams are sorted by this time, newest first.

    format: date-time

  - `ended_at: string`

    When the dream reached `completed`, `failed`, or `canceled`, in RFC 3339, or `null` if it is still `pending` or `running`.

    format: date-time

  - `error: object`

    Why the dream failed, or `null` if `status` isn't `failed`.

    - `type: string`

      A code for why the dream failed, such as `timeout` or `internal_error`.

      The [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#errors) lists common error codes and when they occur.

    - `message: string`

      A human-readable explanation of why the dream failed.

  - `inputs: array of BetaDreamInput`

    The sources that the dream reads, from the request that created it.

    - `beta_dream_memory_store_input: object`

      The memory store that a dream reads, given as an entry in `inputs`.

      With `output_behavior` set to `update_existing`, the dream writes its result into this memory store. Otherwise the dream doesn't change it.

      - `type: "memory_store"`

      - `memory_store_id: string`

        The ID of the memory store for the dream to read (`memstore_...`).

        The memory store must be in the same workspace as the dream and must not be archived.

        minLength: 1

    - `beta_dream_sessions_input: object`

      The sessions that a dream reads, given as an entry in `inputs`.

      - `type: "sessions"`

      - `session_ids: array of string`

        The IDs of the sessions whose transcripts the dream reads (`sesn_...`).

        Give 1 to 100 IDs, with no duplicates. Each session must be in the same workspace as the dream. Responses list the IDs in sorted order.

  - `instructions: string`

    The guidance given when the dream was created, or `null` if none was given.

  - `model: object`

    The model that runs a dream, from the request that created it.

    The dream uses this model for all of its work. The response always gives the model as an object, even if the request gave only a model ID.

    - `id: string`

      The ID of the model that runs the dream, as given in the request that created it.

      minLength: 1, maxLength: 256

    - `speed: optional "standard" or "fast"`

      How fast the model generates output for the dream. Always `standard`.

      - `"standard"`

      - `"fast"`

  - `output_behavior: BetaOutputBehaviorCreateNew or BetaOutputBehaviorUpdateExisting`

    Where the dream writes its result, as set in the request that created the dream. If that request left out `output_behavior`, the dream used the `create_new` behavior.

    - `beta_output_behavior_create_new: object`

      Write the result to a new memory store that starts as a copy of the input memory store. This is the default.

      The new memory store is in the same workspace as the dream. The dream doesn't change the input memory store.

      - `type: "create_new"`

    - `beta_output_behavior_update_existing: object`

      Write the result into the input memory store instead of a new memory store.

      The credential must be allowed to write memory stores, or the request returns a 403 error. While another `update_existing` dream on the same memory store hasn't fully stopped, the request returns a 409 error.

      - `type: "update_existing"`

      - `memory_store_id: string`

        The ID of the memory store for the dream to write its result to (`memstore_...`). It must be the memory store in the `memory_store` entry of `inputs`.

        minLength: 1

  - `outputs: array of BetaDreamOutput`

    The memory store that holds the dream's result, as a one-item array, or an empty array until the dream records that memory store.

    The array is empty while the dream is `pending` and for a short time after it starts `running`. It can stay empty if the dream fails or is canceled before then. The memory store holds the complete result only once `status` is `completed`.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#use-the-output) for how to review and use the result.

    - `type: "memory_store"`

    - `memory_store_id: string`

      The ID of the memory store that the dream writes its result to (`memstore_...`).

      With `output_behavior` set to `create_new`, this is a new memory store. With `update_existing`, it is the input memory store.

  - `session_id: string`

    The ID of the session that runs the dream (`sesn_...`), or `null` if that session hasn't started.

    Stream that session's events to follow what the dream reads and writes.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#watch-the-pipeline-run) for how to watch a running dream.

  - `status: "pending" or "running" or "completed" or 2 more`

    Where a dream is in its lifecycle.

    `completed`, `failed`, and `canceled` are final: once a dream has one of these statuses, its status doesn't change again.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#lifecycle) for what each status means.

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

  - `usage: object`

    The dream's token counts, which stop changing once its `status` is `completed` or `failed`. After a cancel, they can keep changing.

    - `cache_creation_input_tokens: number`

      The dream's input tokens that were written to the prompt cache, for both the 5-minute and 1-hour cache durations.

      format: int32

    - `cache_read_input_tokens: number`

      The dream's input tokens that were read from the prompt cache.

      format: int32

    - `input_tokens: number`

      The dream's input tokens that weren't read from or written to the prompt cache.

      format: int32

    - `output_tokens: number`

      The tokens that the model generated for the dream.

      format: int32

### Beta Dream Error

- `beta_dream_error: object`

  Failure detail for a Dream whose `status` is `failed`.

  - `type: string`

    A code for why the dream failed, such as `timeout` or `internal_error`.

    The [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#errors) lists common error codes and when they occur.

  - `message: string`

    A human-readable explanation of why the dream failed.

### Beta Dream Input

- `beta_dream_input: BetaDreamMemoryStoreInput or BetaDreamSessionsInput`

  A source that a dream reads, such as a memory store or a set of sessions.

  - `beta_dream_memory_store_input: object`

    The memory store that a dream reads, given as an entry in `inputs`.

    With `output_behavior` set to `update_existing`, the dream writes its result into this memory store. Otherwise the dream doesn't change it.

    - `type: "memory_store"`

    - `memory_store_id: string`

      The ID of the memory store for the dream to read (`memstore_...`).

      The memory store must be in the same workspace as the dream and must not be archived.

      minLength: 1

  - `beta_dream_sessions_input: object`

    The sessions that a dream reads, given as an entry in `inputs`.

    - `type: "sessions"`

    - `session_ids: array of string`

      The IDs of the sessions whose transcripts the dream reads (`sesn_...`).

      Give 1 to 100 IDs, with no duplicates. Each session must be in the same workspace as the dream. Responses list the IDs in sorted order.

### Beta Dream Memory Store Input

- `beta_dream_memory_store_input: object`

  The memory store that a dream reads, given as an entry in `inputs`.

  With `output_behavior` set to `update_existing`, the dream writes its result into this memory store. Otherwise the dream doesn't change it.

  - `type: "memory_store"`

  - `memory_store_id: string`

    The ID of the memory store for the dream to read (`memstore_...`).

    The memory store must be in the same workspace as the dream and must not be archived.

    minLength: 1

### Beta Dream Memory Store Output

- `beta_dream_memory_store_output: object`

  The memory store that holds a dream's result, as an entry in `outputs`.

  - `type: "memory_store"`

  - `memory_store_id: string`

    The ID of the memory store that the dream writes its result to (`memstore_...`).

    With `output_behavior` set to `create_new`, this is a new memory store. With `update_existing`, it is the input memory store.

### Beta Dream Model Config

- `beta_dream_model_config: object`

  The model that runs a dream, from the request that created it.

  The dream uses this model for all of its work. The response always gives the model as an object, even if the request gave only a model ID.

  - `id: string`

    The ID of the model that runs the dream, as given in the request that created it.

    minLength: 1, maxLength: 256

  - `speed: optional "standard" or "fast"`

    How fast the model generates output for the dream. Always `standard`.

    - `"standard"`

    - `"fast"`

### Beta Dream Model Config Param

- `beta_dream_model_config_param: object`

  The object form of `model` in a request to create a dream.

  - `id: string`

    The ID of the model to run the dream with.

    The ID can be 1 to 256 characters long.

    The [Availability section of the Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#feature-availability) lists the supported models.

    minLength: 1, maxLength: 256

  - `speed: optional "standard" or "fast"`

    How fast the model generates output for the dream. Defaults to `standard`.

    Dreams accept only `standard`.

    - `"standard"`

    - `"fast"`

### Beta Dream Output

- `beta_dream_output: object`

  An entry in a dream's `outputs` that references the memory store holding its result.

  - `type: "memory_store"`

  - `memory_store_id: string`

    The ID of the memory store that the dream writes its result to (`memstore_...`).

    With `output_behavior` set to `create_new`, this is a new memory store. With `update_existing`, it is the input memory store.

### Beta Dream Sessions Input

- `beta_dream_sessions_input: object`

  The sessions that a dream reads, given as an entry in `inputs`.

  - `type: "sessions"`

  - `session_ids: array of string`

    The IDs of the sessions whose transcripts the dream reads (`sesn_...`).

    Give 1 to 100 IDs, with no duplicates. Each session must be in the same workspace as the dream. Responses list the IDs in sorted order.

### Beta Dream Status

- `beta_dream_status: "pending" or "running" or "completed" or 2 more`

  Where a dream is in its lifecycle.

  `completed`, `failed`, and `canceled` are final: once a dream has one of these statuses, its status doesn't change again.

  See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#lifecycle) for what each status means.

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

### Beta Dream Usage

- `beta_dream_usage: object`

  The tokens that a dream has used so far.

  The counts are zero while the dream is `pending` and update while it is `running`. They can keep changing after a cancel.

  See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams?sdk_languages=cli#billing) for how dreams are billed. See the [prompt caching guide](https://platform.claude.com/docs/en/build-with-claude/prompt-caching?sdk_languages=cli#tracking-cache-performance) for how the input token counts add up.

  - `cache_creation_input_tokens: number`

    The dream's input tokens that were written to the prompt cache, for both the 5-minute and 1-hour cache durations.

    format: int32

  - `cache_read_input_tokens: number`

    The dream's input tokens that were read from the prompt cache.

    format: int32

  - `input_tokens: number`

    The dream's input tokens that weren't read from or written to the prompt cache.

    format: int32

  - `output_tokens: number`

    The tokens that the model generated for the dream.

    format: int32

### Beta Dreaming Error

- `beta_dreaming_error: BetaInvalidRequestError or BetaAuthenticationError or BetaBillingError or 7 more`

  - `beta_invalid_request_error: object`

    - `type: "invalid_request_error"`

      The broad category of the error.

    - `message: string`

      A human-readable explanation of the error. Its wording can change, so don't match on it.

  - `beta_authentication_error: object`

    - `type: "authentication_error"`

      The broad category of the error.

    - `message: string`

      A human-readable explanation of the error. Its wording can change, so don't match on it.

  - `beta_billing_error: object`

    - `type: "billing_error"`

      The broad category of the error.

    - `message: string`

      A human-readable explanation of the error. Its wording can change, so don't match on it.

  - `beta_permission_error: object`

    - `type: "permission_error"`

      The broad category of the error.

    - `message: string`

      A human-readable explanation of the error. Its wording can change, so don't match on it.

  - `beta_not_found_error: object`

    - `type: "not_found_error"`

      The broad category of the error.

    - `message: string`

      A human-readable explanation of the error. Its wording can change, so don't match on it.

  - `beta_rate_limit_error: object`

    - `type: "rate_limit_error"`

      The broad category of the error.

    - `message: string`

      A human-readable explanation of the error. Its wording can change, so don't match on it.

  - `beta_gateway_timeout_error: object`

    - `type: "timeout_error"`

      The broad category of the error.

    - `message: string`

      A human-readable explanation of the error. Its wording can change, so don't match on it.

  - `beta_api_error: object`

    - `type: "api_error"`

      The broad category of the error.

    - `message: string`

      A human-readable explanation of the error. Its wording can change, so don't match on it.

  - `beta_overloaded_error: object`

    - `type: "overloaded_error"`

      The broad category of the error.

    - `message: string`

      A human-readable explanation of the error. Its wording can change, so don't match on it.

  - `beta_target_store_held_error: object`

    Returned with status 409 when a request to create a dream sets `output_behavior` to `update_existing` and another dream that writes into the same memory store hasn't fully stopped.

    The other dream is `pending` or `running`, or it has just stopped and is still finishing its last writes. `message` gives the ID of the other dream when the server can identify it. If that dream has already reached `completed`, `failed`, or `canceled`, retry after a short wait. Otherwise, wait for the other dream to end or cancel it, then retry. The response sets the `x-should-retry` header to `false`.

    - `type: "conflict_error"`

    - `message: optional string`

### Beta Output Behavior

- `beta_output_behavior: BetaOutputBehaviorCreateNew or BetaOutputBehaviorUpdateExisting`

  Which memory store a dream writes its result to. Defaults to `create_new` when left out of a create request.

  - `beta_output_behavior_create_new: object`

    Write the result to a new memory store that starts as a copy of the input memory store. This is the default.

    The new memory store is in the same workspace as the dream. The dream doesn't change the input memory store.

    - `type: "create_new"`

  - `beta_output_behavior_update_existing: object`

    Write the result into the input memory store instead of a new memory store.

    The credential must be allowed to write memory stores, or the request returns a 403 error. While another `update_existing` dream on the same memory store hasn't fully stopped, the request returns a 409 error.

    - `type: "update_existing"`

    - `memory_store_id: string`

      The ID of the memory store for the dream to write its result to (`memstore_...`). It must be the memory store in the `memory_store` entry of `inputs`.

      minLength: 1

### Beta Output Behavior Create New

- `beta_output_behavior_create_new: object`

  Write the result to a new memory store that starts as a copy of the input memory store. This is the default.

  The new memory store is in the same workspace as the dream. The dream doesn't change the input memory store.

  - `type: "create_new"`

### Beta Output Behavior Update Existing

- `beta_output_behavior_update_existing: object`

  Write the result into the input memory store instead of a new memory store.

  The credential must be allowed to write memory stores, or the request returns a 403 error. While another `update_existing` dream on the same memory store hasn't fully stopped, the request returns a 409 error.

  - `type: "update_existing"`

  - `memory_store_id: string`

    The ID of the memory store for the dream to write its result to (`memstore_...`). It must be the memory store in the `memory_store` entry of `inputs`.

    minLength: 1

### Beta Target Store Held Error

- `beta_target_store_held_error: object`

  Returned with status 409 when a request to create a dream sets `output_behavior` to `update_existing` and another dream that writes into the same memory store hasn't fully stopped.

  The other dream is `pending` or `running`, or it has just stopped and is still finishing its last writes. `message` gives the ID of the other dream when the server can identify it. If that dream has already reached `completed`, `failed`, or `canceled`, retry after a short wait. Otherwise, wait for the other dream to end or cancel it, then retry. The response sets the `x-should-retry` header to `false`.

  - `type: "conflict_error"`

  - `message: optional string`
