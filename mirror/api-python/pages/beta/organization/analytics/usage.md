---
title: Usage
url: https://platform.claude.com/docs/en/api/python/beta/organization/analytics/usage
---

# Usage

## Get Token Usage By Dimension

`beta.organization.analytics.usage.list(**kwargs) -> SyncReportPageCursor[BetaAnalyticsUsageItem]`

**GET** `/v1/organizations/analytics/usage`

Get token usage across a date range, broken out by dimension.

Returns one row per combination of the requested `group_by[]`
dimensions (and time bucket, when `time_bucket_width` is set) that has
usage in the range, ranked by the `order_by` metric or ordered by time
bucket; every combination is returned across pages. With no `group_by[]`
and no `time_bucket_width`, a single row aggregates the whole range.
Includes all usage, whether or not it is attributable to a seat user.
Requires an API key with the `read:analytics` scope, or an Admin API key.

### Parameters

- `starting_at: Union[str, datetime]` (query parameter)

  Start of range, inclusive. RFC 3339 tz-aware. Must be within the last 365 days and no earlier than 2026-01-01T00:00:00Z.

  format: date-time

- `actor_ids: Optional[Sequence[str]]` (query parameter)

  Filter to usage attributed to specific identities, by tagged ID: a `user_...`, `svac_...` (service account), or `apikey_...` ID. An `apikey_` entry matches only usage attributed to the key itself, not usage on that key attributed to a user or service account (use `api_key_ids[]` for every request a key authenticated). Federated identities have no tagged ID; select them with `actor_types[]`. Use `group_by[]=actor` to break out per-identity values.

  maxItems: 100

- `actor_types: Optional[List[BetaAnalyticsActorType]]` (query parameter)

  Filter to usage attributed to specific kinds of identity. Use `group_by[]=actor_type` to break out per-kind values.

  maxItems: 100

  - `"api_actor"`

  - `"federated_actor"`

  - `"service_account_actor"`

  - `"user_actor"`

- `agent_ids: Optional[Sequence[str]]` (query parameter)

  Filter to usage incurred by sessions of specific Claude Managed Agents agents. Use `group_by[]=agent_id` to break out per-agent values. Claude Developer Platform organizations only.

  maxItems: 100

- `api_key_ids: Optional[Sequence[str]]` (query parameter)

  Filter to usage authenticated by specific API keys, by tagged API key ID (`apikey_...`), whichever identity the usage is attributed to. Include an empty entry (`api_key_ids[]=`) to also match usage that no API key authenticated. Use `group_by[]=api_key_id` to break out per-key values; usage without a key has a null `api_key_id`. Claude Developer Platform organizations only.

  maxItems: 100

- `claude_tag_categories: Optional[List[BetaAnalyticsClaudeTagCategory]]` (query parameter)

  Filter to Claude Tag (Claude in Slack) usage in specific spend categories. Usage with no category never matches. `dm` usage is reported under the user's product rather than `claude_tag`, so combining this filter with `products[]=claude_tag` excludes it. Use `group_by[]=claude_tag_category` to break out per-category values.

  maxItems: 100

  - `"dm"`

  - `"engaged"`

  - `"monitoring"`

  - `"proactive"`

  - `"scheduled"`

- `claude_tag_user_ids: Optional[Sequence[str]]` (query parameter)

  Filter to Claude Tag (Claude in Slack) usage attributed to specific Slack users, by Slack user ID (for example `U0123ABCDEF`), not claude.ai user ID. Usage that is not Claude Tag, and Claude Tag usage not attributed to a single user, never matches. Use `group_by[]=claude_tag_user_id` to break out per-user values.

  maxItems: 100

- `context_windows: Optional[List[BetaAnalyticsContextWindow]]` (query parameter)

  Filter to specific context-window pricing tiers. Use `group_by[]=context_window` to break out per-tier values.

  maxItems: 100

  - `"0-200k"`

  - `"200k-1M"`

- `deployment_ids: Optional[Sequence[str]]` (query parameter)

  Filter to usage incurred by Claude Managed Agents sessions that specific deployments started. Use `group_by[]=deployment_id` to break out per-deployment values. Claude Developer Platform organizations only.

  maxItems: 100

- `ending_at: Optional[Union[str, datetime, null]]` (query parameter)

  End of range, exclusive. Required when `time_bucket_width` is set. Without `time_bucket_width`, defaults to the earlier of now and `starting_at` + 31 days. The range may span at most 31 days.

  format: date-time

- `environment_ids: Optional[Sequence[str]]` (query parameter)

  Filter to usage incurred by Claude Managed Agents sessions that ran in specific environments. Use `group_by[]=environment_id` to break out per-environment values. Claude Developer Platform organizations only.

  maxItems: 100

- `exclude_deleted_users: Optional[bool]` (query parameter)

  If true, omit rows whose `actor` is a `user_actor` with `deleted: true`. Requires `group_by[]=actor`. Rows for other actor types, and rows whose `actor` is null, are always kept. A page may contain fewer than `limit` rows; use `has_more` and `next_page` to paginate as usual.

  default: false

- `group_by: Optional[List[BetaAnalyticsUsageGroupBy]]` (query parameter)

  Dimensions to break usage out by (at most 5): one row per combination of their values with usage in the range (and per time bucket, when `time_bucket_width` is set), every combination returned across pages rather than a capped top set. When omitted, a single row aggregates the whole range.

  maxItems: 100

  - `"actor"`

  - `"actor_type"`

  - `"agent_id"`

  - `"api_key_id"`

  - `"claude_tag_category"`

  - `"claude_tag_user_id"`

  - `"context_window"`

  - `"deployment_id"`

  - `"environment_id"`

  - `"inference_geo"`

  - `"model"`

  - `"product"`

  - `"rbac_group_id"`

  - `"service_tier"`

  - `"session_id"`

  - `"slack_channel_id"`

  - `"speed"`

  - `"user_profile_id"`

  - `"workspace_id"`

- `inference_geos: Optional[List[BetaAnalyticsInferenceGeoFilter]]` (query parameter)

  Filter to specific inference regions. `not_available` matches rows where the region is unset. Use `group_by[]=inference_geo` to break out per-region values.

  maxItems: 100

  - `"global"`

  - `"not_available"`

  - `"us"`

- `limit: Optional[int]` (query parameter)

  Number of rows per page (1-1000, default 20). `cost_type`/`token_type` fan-out rows (cost endpoint only) do not count toward this limit, so `data` can exceed it.

  default: 20, minimum: 1, maximum: 1000

- `models: Optional[Sequence[str]]` (query parameter)

  Models to include. Defaults to all models. Use `group_by[]=model` to break out per-model values.

  maxItems: 100

- `order: Optional[BetaAnalyticsUsageCostSortOrder]` (query parameter)

  Sort direction of the `order_by` metric, or of the time buckets when `order_by` is `time` and `time_bucket_width` is set. Defaults to `desc`.

  - `"asc"`

  - `"desc"`

- `order_by: Optional[BetaAnalyticsUsageOrderBy]` (query parameter)

  Row order. A metric ranks rows by that metric in the `order` direction. `time` orders rows by time bucket in the `order` direction (newest first by default) and, within a bucket, by `total_tokens`, highest first. `time` takes effect only with `time_bucket_width`; without it, `time` is the same as `total_tokens`. Defaults to `total_tokens`.

  - `"output_tokens"`

  - `"requests"`

  - `"time"`

  - `"total_tokens"`

  - `"uncached_input_tokens"`

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field.

- `products: Optional[List[BetaAnalyticsUsageCostProductFilter]]` (query parameter)

  Product surfaces to include. Defaults to all products.

  maxItems: 100

  - `"chat"`

  - `"chat_cowork_unified"`

  - `"claude_code"`

  - `"claude_console"`

  - `"claude_design"`

  - `"claude_in_chrome"`

  - `"claude_tag"`

  - `"cowork"`

  - `"managed_agents_api"`

  - `"message_batches_api"`

  - `"messages_api"`

  - `"office_agent"`

- `rbac_group_ids: Optional[Sequence[str]]` (query parameter)

  Filter to usage attributed to specific RBAC groups. Accepts tagged RBAC group IDs (`rbac_group_...`) or bare group UUIDs. A row matches when the user belonged to any of the listed groups on the (UTC) day the usage occurred; usage with no group attribution never matches.

  maxItems: 100

- `service_tiers: Optional[List[BetaAnalyticsServiceTier]]` (query parameter)

  Filter to specific service tiers. Use `group_by[]=service_tier` to break out per-tier values. Claude Developer Platform organizations only; matches nothing for a Claude Enterprise organization.

  maxItems: 100

  - `"batch"`

  - `"flex"`

  - `"flex_discount"`

  - `"priority"`

  - `"priority_on_demand"`

  - `"standard"`

- `session_ids: Optional[Sequence[str]]` (query parameter)

  Filter to usage incurred by specific Claude Managed Agents sessions, by tagged session ID (`sesn_...`). Use `group_by[]=session_id` to break out per-session values. Claude Developer Platform organizations only.

  maxItems: 100

- `slack_channel_ids: Optional[Sequence[str]]` (query parameter)

  Filter to usage originating from specific Slack channels. Use `group_by[]=slack_channel_id` to break out per-channel values.

  maxItems: 100

- `speeds: Optional[List[BetaAnalyticsSpeed]]` (query parameter)

  Filter to fast or standard inference mode. Use `group_by[]=speed` to break out per-mode values.

  maxItems: 100

  - `"fast"`

  - `"standard"`

- `time_bucket_width: Optional[BetaAnalyticsTimeBucketWidth]` (query parameter)

  Time-bucket granularity. When set, rows are returned per time bucket (one per bucket and dimension combination with usage) and each row's `starting_at` and `ending_at` are that bucket's bounds; the time bucket counts toward `limit`. `ending_at` is required when `time_bucket_width` is set, and with `time_bucket_width="1m"` the range may span at most 24 hours. When omitted, each row aggregates the requested range with `starting_at` and `ending_at` each rounded down to the hour.

  - `"1d"`

  - `"1h"`

  - `"1m"`

- `user_profile_ids: Optional[Sequence[str]]` (query parameter)

  Filter to usage attributed to specific user profiles, by tagged user profile ID (`uprof_...`). Use `group_by[]=user_profile_id` to break out per-profile values. Claude Developer Platform organizations only.

  maxItems: 100

- `workspace_ids: Optional[Sequence[str]]` (query parameter)

  Filter to usage in specific workspaces, by tagged workspace ID (`wrkspc_...`). Use `group_by[]=workspace_id` to break out per-workspace values. Claude Developer Platform organizations only; matches nothing for a Claude Enterprise organization.

  maxItems: 100

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `analytics-usage-cost-2026-08-24` in this header.

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

### Returns

- `class BetaAnalyticsUsageItem`

  - `ending_at: datetime`

    End of the period this row covers (exclusive), as an RFC 3339 UTC timestamp: the end of the row's time bucket when a time-bucket width is set; otherwise the requested `ending_at` (or, when omitted, the earlier of now and `starting_at` plus 31 days) rounded down to the hour, because without a time bucket the report covers whole hours.

    format: date-time

  - `group: BetaAnalyticsUsageGroup`

    The dimension values this row's usage is broken out by.

    - `actor: Optional[BetaAnalyticsActor]`

      The identity the usage is attributed to: the user if one is attributed, else the service account, else the federated (cloud-platform) identity, else the API key. Populated only when `actor` is in `group_by[]`; null for usage with no attributable identity, and for users' and federated identities' usage when the reader is a member who can see only some workspaces. Distinct identities the server cannot render also read null, each as its own row.

      - `class BetaAnalyticsReportUserActor`

        - `type: Literal["user_actor"]`

          Actor type. Always `"user_actor"`.

        - `deleted: bool`

          True when the account has been deleted, or when the user is no longer a member of the organization or its associated organizations (for example, their membership was removed or they were deprovisioned via your identity provider). `email_address` stays populated for removed users and is null when the account has been deleted. `name` follows the rules described on that field. The `user_id` is still populated for reconciliation.

        - `email_address: Optional[str]`

          The user's current email address, including for users who are no longer members of the organization. Null when the account has been deleted and for system-minted service accounts.

        - `name: Optional[str]`

          The user's current full name. Null when the user has not set one. `"Deleted User"` when the account has been deleted, or when the user is no longer a member and the organization hides removed users' names.

        - `user_id: str`

          Tagged user ID.

      - `class BetaAnalyticsServiceAccountActor`

        - `type: Literal["service_account_actor"]`

        - `service_account_id: str`

          Tagged service account ID.

      - `class BetaAnalyticsFederatedActor`

        - `type: Literal["federated_actor"]`

        - `provider: BetaAnalyticsFederatedActorProvider`

          The trusted provider that asserted the caller's identity.

          - `class BetaAnalyticsFederatedActorAWSProvider`

            - `type: Literal["aws"]`

            - `account_id: str`

              The AWS account the organization is bound to.

            - `signed_principal: str`

              The AWS-signed ARN of the IAM principal that made the requests.

          - `class BetaAnalyticsFederatedActorAzureProvider`

            - `type: Literal["azure"]`

            - `subscription_id: str`

              The Azure subscription the organization is bound to.

          - `class BetaAnalyticsFederatedActorGCPProvider`

            - `type: Literal["gcp"]`

            - `project_number: str`

              The Google Cloud project the organization is bound to.

          - `class BetaAnalyticsFederatedActorOIDCProvider`

            - `type: Literal["oidc"]`

            - `issuer: Optional[str]`

              The federation issuer's URL.

        - `subject: Optional[str]`

          The provider's identifier for the caller: on `aws`, the IAM principal ARN (one role is one actor across its sessions); on `gcp`, the caller's IAM principal identifier as Google Cloud reports it, such as `serviceAccount:<email>`, `user:<email>`, or a `principal://...` URI.

      - `class BetaAnalyticsAPIActor`

        - `type: Literal["api_actor"]`

        - `api_key_id: str`

          Tagged API key ID.

    - `actor_type: Optional[BetaAnalyticsActorType]`

      Kind of identity the usage is attributed to; matches `actor.type` when `actor` is set. Populated only when `actor_type` is in `group_by[]`.

      - `"api_actor"`

      - `"federated_actor"`

      - `"service_account_actor"`

      - `"user_actor"`

    - `agent_id: Optional[str]`

      Claude Managed Agents agent whose session incurred the usage. Populated only when `agent_id` is in `group_by[]`; null for usage outside a managed session.

    - `api_key_id: Optional[str]`

      API key that authenticated the requests, as a tagged API key ID, whichever identity `actor` resolves to. Populated only when `api_key_id` is in `group_by[]`; null for usage not authenticated by an API key.

    - `claude_tag_category: Optional[BetaAnalyticsClaudeTagCategory]`

      Claude Tag (Claude in Slack) spend category: `engaged` (a person addressed Claude in a channel or thread), `proactive` (Claude responded without being addressed), `scheduled` (a scheduled routine ran), `monitoring` (Claude watching a channel it was asked to monitor), or `dm` (direct messages with Claude). Populated only when `claude_tag_category` is in `group_by[]`; null for usage that is not Claude Tag. Direct-message usage is billed to the individual user and is reported under that user's product, not under `claude_tag`. New categories may be added over time.

      - `"dm"`

      - `"engaged"`

      - `"monitoring"`

      - `"proactive"`

      - `"scheduled"`

    - `claude_tag_user_id: Optional[str]`

      Slack user ID (for example `U0123ABCDEF`) of the member the Claude Tag (Claude in Slack) usage is attributed to, not a claude.ai user ID. Populated only when `claude_tag_user_id` is in `group_by[]`; null for usage that is not Claude Tag and for Claude Tag usage that is not attributed to a single user (for example `monitoring`, and `proactive` usage Claude initiated), so per-user rows can sum to less than the Claude Tag total. Cannot be combined with `group_by[]=rbac_group_id` or the `rbac_group_ids[]` filter.

    - `context_window: Optional[BetaAnalyticsContextWindow]`

      Context-window pricing tier of the usage or cost. Null unless `context_window` is in `group_by[]`; it can also be null on grouped rows with no context-window tier, such as code execution.

      - `"0-200k"`

      - `"200k-1M"`

    - `deployment_id: Optional[str]`

      Deployment that started the Claude Managed Agents session. Populated only when `deployment_id` is in `group_by[]`; null for usage outside a managed session and for sessions no deployment started.

    - `environment_id: Optional[str]`

      Claude Managed Agents environment the session ran in. Populated only when `environment_id` is in `group_by[]`; null for usage outside a managed session.

    - `inference_geo: Optional[BetaAnalyticsUsageCostInferenceGeo]`

      Inference region of the usage or cost. Null unless `inference_geo` is in `group_by[]`; it can also be null on grouped rows where the region is not set (the rows that `inference_geos[]=not_available` matches).

      - `"global"`

      - `"us"`

    - `model: Optional[str]`

      Model that produced the usage or cost, as a model name in the form the `models[]` filter accepts (for example, `claude-opus-5-5`). Null unless `model` is in `group_by[]`; it can also be null on grouped rows whose usage or cost is not attributed to a specific model, such as code execution.

    - `product: Optional[str]`

      Product surface that produced the usage or cost. Null unless product is in `group_by[]`; it can also be null on grouped rows whose usage cannot be attributed to a known surface. Values include `chat`, `claude_code`, `cowork`, `office_agent`, `claude_in_chrome`, `claude_design`, `claude_tag`, and `chat_cowork_unified`. `claude_tag` is Claude Tag, the Claude product in Slack. `chat_cowork_unified` is Chat and Cowork unified, Cowork's features inside claude.ai chat: chat and Cowork usage by a member who has it turned on is reported under this value instead of `chat` or `cowork`. It is accepted as a filter only where Chat and Cowork unified is available. Some unattributed usage is reported as "other".

    - `rbac_group_id: Optional[str]`

      RBAC group (team) the usage is attributed to, in the public tagged `rbac_group_...` spelling — the same spelling the activity resources use for this key, so the same team has one id across resources and it round-trips as an `rbac_group_ids[]` filter value. Populated only when `rbac_group_id` is in `group_by[]`. Any-membership semantics: a user in several groups contributes their full usage to each of those groups' rows, so the named-group rows overlap and their sum can exceed the org total. A null value is the single unassigned row: users in no group on that (UTC) day. For the true org total, run the same query without `group_by[]`.

    - `service_tier: Optional[BetaAnalyticsServiceTier]`

      Service tier the usage was served at. Populated only when `service_tier` is in `group_by[]`; null for usage with no service tier (for example, code execution) and for Claude Enterprise usage.

      - `"batch"`

      - `"flex"`

      - `"flex_discount"`

      - `"priority"`

      - `"priority_on_demand"`

      - `"standard"`

    - `session_id: Optional[str]`

      Claude Managed Agents session that incurred the usage. Populated only when `session_id` is in `group_by[]`; null for usage outside a managed session.

    - `slack_channel_id: Optional[str]`

      Slack channel the usage originated from. Populated only when `slack_channel_id` is in `group_by[]`; null for usage outside Slack (and for rows recorded before channel attribution was enabled).

    - `speed: Optional[BetaAnalyticsSpeed]`

      Inference speed mode of the usage or cost: `fast` or `standard`. Null unless `speed` is in `group_by[]`.

      - `"fast"`

      - `"standard"`

    - `user_profile_id: Optional[str]`

      User profile the usage was attributed to, as a tagged `uprof_` ID. Populated only when `user_profile_id` is in `group_by[]`; null for usage that named no profile and for Claude Enterprise usage.

    - `workspace_id: Optional[str]`

      Workspace the usage occurred in, as a tagged workspace ID, including the organization's default workspace. Populated only when `workspace_id` is in `group_by[]`; null for Claude Enterprise usage.

  - `starting_at: datetime`

    Start of the period this row covers (inclusive), as an RFC 3339 UTC timestamp: the start of the row's time bucket when a time-bucket width is set, otherwise the requested `starting_at` rounded down to the hour.

    format: date-time

  - `usage: BetaAnalyticsUsageMetrics`

    Token usage for this row.

    - `cache_creation: BetaCacheCreation`

      The number of input tokens for cache creation.

      - `ephemeral_1h_input_tokens: int`

        The number of input tokens used to create the 1 hour cache entry.

        default: 0, minimum: 0

      - `ephemeral_5m_input_tokens: int`

        The number of input tokens used to create the 5 minute cache entry.

        default: 0, minimum: 0

    - `cache_read_input_tokens: int`

      The number of input tokens read from the cache.

    - `output_tokens: int`

      The number of output tokens generated.

    - `requests: Optional[int]`

      Number of API requests in this row's scope. For sandbox / code-execution events, this counts execution spans rather than HTTP requests (these rows surface with `product: null`).

    - `server_tool_use: BetaAnalyticsServerToolUse`

      Server-side tool usage metrics.

      - `web_search_requests: int`

        The number of web search requests made.

    - `total_tokens: int`

      Total token count across all token types. This is the value the default `order_by` (`total_tokens`) sorts on.

    - `uncached_input_tokens: int`

      The number of uncached input tokens processed.

### Example

```python
import os
from datetime import datetime
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.analytics.usage.list(
    starting_at=datetime.fromisoformat("2026-09-01T00:00:00"),
)
page = page.data[0]
print(page.ending_at)
```

#### Response (200)

```json
{
  "data": [
    {
      "ending_at": "2026-10-01T00:00:00Z",
      "group": {
        "actor": {
          "deleted": false,
          "email_address": "user@emaildomain.com",
          "name": "Jane Doe",
          "type": "user_actor",
          "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
        },
        "actor_type": "user_actor",
        "agent_id": "agent_01VHd3EAGJ6PLkP9LM7DDu3f",
        "api_key_id": "apikey_01Rj2N8SVvo6BePZj99NhmiT",
        "claude_tag_category": "dm",
        "claude_tag_user_id": "U0123ABCDEF",
        "context_window": "0-200k",
        "deployment_id": "depl_01JFC6ihzZHtAuyHsaENdJhY",
        "environment_id": "env_017oTjuGedHtjhJauVC5xGJD",
        "inference_geo": "global",
        "model": "claude-opus-5-5",
        "product": "chat",
        "rbac_group_id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
        "service_tier": "standard",
        "session_id": "sesn_0187kPDyNCwibNNvfaPEApCJ",
        "slack_channel_id": "C0123ABCDEF",
        "speed": "fast",
        "user_profile_id": "uprof_01M33NeYUQK2WV9PpYcsPHLi",
        "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
      },
      "starting_at": "2026-09-01T00:00:00Z",
      "usage": {
        "cache_creation": {
          "ephemeral_1h_input_tokens": 0,
          "ephemeral_5m_input_tokens": 0
        },
        "cache_read_input_tokens": 3200000,
        "output_tokens": 891000,
        "requests": 128,
        "server_tool_use": {
          "web_search_requests": 10
        },
        "total_tokens": 5375500,
        "uncached_input_tokens": 1284500
      }
    }
  ],
  "data_refreshed_at": "2026-10-01T04:02:11Z",
  "has_more": true,
  "next_page": "next_page"
}
```

## Domain types

### Beta Analytics Usage Group

- `class BetaAnalyticsUsageGroup`

  The dimension values one usage row is broken out by; each is null
  unless its dimension is in `group_by[]`.

  - `actor: Optional[BetaAnalyticsActor]`

    The identity the usage is attributed to: the user if one is attributed, else the service account, else the federated (cloud-platform) identity, else the API key. Populated only when `actor` is in `group_by[]`; null for usage with no attributable identity, and for users' and federated identities' usage when the reader is a member who can see only some workspaces. Distinct identities the server cannot render also read null, each as its own row.

    - `class BetaAnalyticsReportUserActor`

      - `type: Literal["user_actor"]`

        Actor type. Always `"user_actor"`.

      - `deleted: bool`

        True when the account has been deleted, or when the user is no longer a member of the organization or its associated organizations (for example, their membership was removed or they were deprovisioned via your identity provider). `email_address` stays populated for removed users and is null when the account has been deleted. `name` follows the rules described on that field. The `user_id` is still populated for reconciliation.

      - `email_address: Optional[str]`

        The user's current email address, including for users who are no longer members of the organization. Null when the account has been deleted and for system-minted service accounts.

      - `name: Optional[str]`

        The user's current full name. Null when the user has not set one. `"Deleted User"` when the account has been deleted, or when the user is no longer a member and the organization hides removed users' names.

      - `user_id: str`

        Tagged user ID.

    - `class BetaAnalyticsServiceAccountActor`

      - `type: Literal["service_account_actor"]`

      - `service_account_id: str`

        Tagged service account ID.

    - `class BetaAnalyticsFederatedActor`

      - `type: Literal["federated_actor"]`

      - `provider: BetaAnalyticsFederatedActorProvider`

        The trusted provider that asserted the caller's identity.

        - `class BetaAnalyticsFederatedActorAWSProvider`

          - `type: Literal["aws"]`

          - `account_id: str`

            The AWS account the organization is bound to.

          - `signed_principal: str`

            The AWS-signed ARN of the IAM principal that made the requests.

        - `class BetaAnalyticsFederatedActorAzureProvider`

          - `type: Literal["azure"]`

          - `subscription_id: str`

            The Azure subscription the organization is bound to.

        - `class BetaAnalyticsFederatedActorGCPProvider`

          - `type: Literal["gcp"]`

          - `project_number: str`

            The Google Cloud project the organization is bound to.

        - `class BetaAnalyticsFederatedActorOIDCProvider`

          - `type: Literal["oidc"]`

          - `issuer: Optional[str]`

            The federation issuer's URL.

      - `subject: Optional[str]`

        The provider's identifier for the caller: on `aws`, the IAM principal ARN (one role is one actor across its sessions); on `gcp`, the caller's IAM principal identifier as Google Cloud reports it, such as `serviceAccount:<email>`, `user:<email>`, or a `principal://...` URI.

    - `class BetaAnalyticsAPIActor`

      - `type: Literal["api_actor"]`

      - `api_key_id: str`

        Tagged API key ID.

  - `actor_type: Optional[BetaAnalyticsActorType]`

    Kind of identity the usage is attributed to; matches `actor.type` when `actor` is set. Populated only when `actor_type` is in `group_by[]`.

    - `"api_actor"`

    - `"federated_actor"`

    - `"service_account_actor"`

    - `"user_actor"`

  - `agent_id: Optional[str]`

    Claude Managed Agents agent whose session incurred the usage. Populated only when `agent_id` is in `group_by[]`; null for usage outside a managed session.

  - `api_key_id: Optional[str]`

    API key that authenticated the requests, as a tagged API key ID, whichever identity `actor` resolves to. Populated only when `api_key_id` is in `group_by[]`; null for usage not authenticated by an API key.

  - `claude_tag_category: Optional[BetaAnalyticsClaudeTagCategory]`

    Claude Tag (Claude in Slack) spend category: `engaged` (a person addressed Claude in a channel or thread), `proactive` (Claude responded without being addressed), `scheduled` (a scheduled routine ran), `monitoring` (Claude watching a channel it was asked to monitor), or `dm` (direct messages with Claude). Populated only when `claude_tag_category` is in `group_by[]`; null for usage that is not Claude Tag. Direct-message usage is billed to the individual user and is reported under that user's product, not under `claude_tag`. New categories may be added over time.

    - `"dm"`

    - `"engaged"`

    - `"monitoring"`

    - `"proactive"`

    - `"scheduled"`

  - `claude_tag_user_id: Optional[str]`

    Slack user ID (for example `U0123ABCDEF`) of the member the Claude Tag (Claude in Slack) usage is attributed to, not a claude.ai user ID. Populated only when `claude_tag_user_id` is in `group_by[]`; null for usage that is not Claude Tag and for Claude Tag usage that is not attributed to a single user (for example `monitoring`, and `proactive` usage Claude initiated), so per-user rows can sum to less than the Claude Tag total. Cannot be combined with `group_by[]=rbac_group_id` or the `rbac_group_ids[]` filter.

  - `context_window: Optional[BetaAnalyticsContextWindow]`

    Context-window pricing tier of the usage or cost. Null unless `context_window` is in `group_by[]`; it can also be null on grouped rows with no context-window tier, such as code execution.

    - `"0-200k"`

    - `"200k-1M"`

  - `deployment_id: Optional[str]`

    Deployment that started the Claude Managed Agents session. Populated only when `deployment_id` is in `group_by[]`; null for usage outside a managed session and for sessions no deployment started.

  - `environment_id: Optional[str]`

    Claude Managed Agents environment the session ran in. Populated only when `environment_id` is in `group_by[]`; null for usage outside a managed session.

  - `inference_geo: Optional[BetaAnalyticsUsageCostInferenceGeo]`

    Inference region of the usage or cost. Null unless `inference_geo` is in `group_by[]`; it can also be null on grouped rows where the region is not set (the rows that `inference_geos[]=not_available` matches).

    - `"global"`

    - `"us"`

  - `model: Optional[str]`

    Model that produced the usage or cost, as a model name in the form the `models[]` filter accepts (for example, `claude-opus-5-5`). Null unless `model` is in `group_by[]`; it can also be null on grouped rows whose usage or cost is not attributed to a specific model, such as code execution.

  - `product: Optional[str]`

    Product surface that produced the usage or cost. Null unless product is in `group_by[]`; it can also be null on grouped rows whose usage cannot be attributed to a known surface. Values include `chat`, `claude_code`, `cowork`, `office_agent`, `claude_in_chrome`, `claude_design`, `claude_tag`, and `chat_cowork_unified`. `claude_tag` is Claude Tag, the Claude product in Slack. `chat_cowork_unified` is Chat and Cowork unified, Cowork's features inside claude.ai chat: chat and Cowork usage by a member who has it turned on is reported under this value instead of `chat` or `cowork`. It is accepted as a filter only where Chat and Cowork unified is available. Some unattributed usage is reported as "other".

  - `rbac_group_id: Optional[str]`

    RBAC group (team) the usage is attributed to, in the public tagged `rbac_group_...` spelling — the same spelling the activity resources use for this key, so the same team has one id across resources and it round-trips as an `rbac_group_ids[]` filter value. Populated only when `rbac_group_id` is in `group_by[]`. Any-membership semantics: a user in several groups contributes their full usage to each of those groups' rows, so the named-group rows overlap and their sum can exceed the org total. A null value is the single unassigned row: users in no group on that (UTC) day. For the true org total, run the same query without `group_by[]`.

  - `service_tier: Optional[BetaAnalyticsServiceTier]`

    Service tier the usage was served at. Populated only when `service_tier` is in `group_by[]`; null for usage with no service tier (for example, code execution) and for Claude Enterprise usage.

    - `"batch"`

    - `"flex"`

    - `"flex_discount"`

    - `"priority"`

    - `"priority_on_demand"`

    - `"standard"`

  - `session_id: Optional[str]`

    Claude Managed Agents session that incurred the usage. Populated only when `session_id` is in `group_by[]`; null for usage outside a managed session.

  - `slack_channel_id: Optional[str]`

    Slack channel the usage originated from. Populated only when `slack_channel_id` is in `group_by[]`; null for usage outside Slack (and for rows recorded before channel attribution was enabled).

  - `speed: Optional[BetaAnalyticsSpeed]`

    Inference speed mode of the usage or cost: `fast` or `standard`. Null unless `speed` is in `group_by[]`.

    - `"fast"`

    - `"standard"`

  - `user_profile_id: Optional[str]`

    User profile the usage was attributed to, as a tagged `uprof_` ID. Populated only when `user_profile_id` is in `group_by[]`; null for usage that named no profile and for Claude Enterprise usage.

  - `workspace_id: Optional[str]`

    Workspace the usage occurred in, as a tagged workspace ID, including the organization's default workspace. Populated only when `workspace_id` is in `group_by[]`; null for Claude Enterprise usage.

### Beta Analytics Usage Group By

- `type BetaAnalyticsUsageGroupBy = Literal["actor", "actor_type", "agent_id", 16 more]`

  - `"actor"`

  - `"actor_type"`

  - `"agent_id"`

  - `"api_key_id"`

  - `"claude_tag_category"`

  - `"claude_tag_user_id"`

  - `"context_window"`

  - `"deployment_id"`

  - `"environment_id"`

  - `"inference_geo"`

  - `"model"`

  - `"product"`

  - `"rbac_group_id"`

  - `"service_tier"`

  - `"session_id"`

  - `"slack_channel_id"`

  - `"speed"`

  - `"user_profile_id"`

  - `"workspace_id"`

### Beta Analytics Usage Item

- `class BetaAnalyticsUsageItem`

  - `ending_at: datetime`

    End of the period this row covers (exclusive), as an RFC 3339 UTC timestamp: the end of the row's time bucket when a time-bucket width is set; otherwise the requested `ending_at` (or, when omitted, the earlier of now and `starting_at` plus 31 days) rounded down to the hour, because without a time bucket the report covers whole hours.

    format: date-time

  - `group: BetaAnalyticsUsageGroup`

    The dimension values this row's usage is broken out by.

    - `actor: Optional[BetaAnalyticsActor]`

      The identity the usage is attributed to: the user if one is attributed, else the service account, else the federated (cloud-platform) identity, else the API key. Populated only when `actor` is in `group_by[]`; null for usage with no attributable identity, and for users' and federated identities' usage when the reader is a member who can see only some workspaces. Distinct identities the server cannot render also read null, each as its own row.

      - `class BetaAnalyticsReportUserActor`

        - `type: Literal["user_actor"]`

          Actor type. Always `"user_actor"`.

        - `deleted: bool`

          True when the account has been deleted, or when the user is no longer a member of the organization or its associated organizations (for example, their membership was removed or they were deprovisioned via your identity provider). `email_address` stays populated for removed users and is null when the account has been deleted. `name` follows the rules described on that field. The `user_id` is still populated for reconciliation.

        - `email_address: Optional[str]`

          The user's current email address, including for users who are no longer members of the organization. Null when the account has been deleted and for system-minted service accounts.

        - `name: Optional[str]`

          The user's current full name. Null when the user has not set one. `"Deleted User"` when the account has been deleted, or when the user is no longer a member and the organization hides removed users' names.

        - `user_id: str`

          Tagged user ID.

      - `class BetaAnalyticsServiceAccountActor`

        - `type: Literal["service_account_actor"]`

        - `service_account_id: str`

          Tagged service account ID.

      - `class BetaAnalyticsFederatedActor`

        - `type: Literal["federated_actor"]`

        - `provider: BetaAnalyticsFederatedActorProvider`

          The trusted provider that asserted the caller's identity.

          - `class BetaAnalyticsFederatedActorAWSProvider`

            - `type: Literal["aws"]`

            - `account_id: str`

              The AWS account the organization is bound to.

            - `signed_principal: str`

              The AWS-signed ARN of the IAM principal that made the requests.

          - `class BetaAnalyticsFederatedActorAzureProvider`

            - `type: Literal["azure"]`

            - `subscription_id: str`

              The Azure subscription the organization is bound to.

          - `class BetaAnalyticsFederatedActorGCPProvider`

            - `type: Literal["gcp"]`

            - `project_number: str`

              The Google Cloud project the organization is bound to.

          - `class BetaAnalyticsFederatedActorOIDCProvider`

            - `type: Literal["oidc"]`

            - `issuer: Optional[str]`

              The federation issuer's URL.

        - `subject: Optional[str]`

          The provider's identifier for the caller: on `aws`, the IAM principal ARN (one role is one actor across its sessions); on `gcp`, the caller's IAM principal identifier as Google Cloud reports it, such as `serviceAccount:<email>`, `user:<email>`, or a `principal://...` URI.

      - `class BetaAnalyticsAPIActor`

        - `type: Literal["api_actor"]`

        - `api_key_id: str`

          Tagged API key ID.

    - `actor_type: Optional[BetaAnalyticsActorType]`

      Kind of identity the usage is attributed to; matches `actor.type` when `actor` is set. Populated only when `actor_type` is in `group_by[]`.

      - `"api_actor"`

      - `"federated_actor"`

      - `"service_account_actor"`

      - `"user_actor"`

    - `agent_id: Optional[str]`

      Claude Managed Agents agent whose session incurred the usage. Populated only when `agent_id` is in `group_by[]`; null for usage outside a managed session.

    - `api_key_id: Optional[str]`

      API key that authenticated the requests, as a tagged API key ID, whichever identity `actor` resolves to. Populated only when `api_key_id` is in `group_by[]`; null for usage not authenticated by an API key.

    - `claude_tag_category: Optional[BetaAnalyticsClaudeTagCategory]`

      Claude Tag (Claude in Slack) spend category: `engaged` (a person addressed Claude in a channel or thread), `proactive` (Claude responded without being addressed), `scheduled` (a scheduled routine ran), `monitoring` (Claude watching a channel it was asked to monitor), or `dm` (direct messages with Claude). Populated only when `claude_tag_category` is in `group_by[]`; null for usage that is not Claude Tag. Direct-message usage is billed to the individual user and is reported under that user's product, not under `claude_tag`. New categories may be added over time.

      - `"dm"`

      - `"engaged"`

      - `"monitoring"`

      - `"proactive"`

      - `"scheduled"`

    - `claude_tag_user_id: Optional[str]`

      Slack user ID (for example `U0123ABCDEF`) of the member the Claude Tag (Claude in Slack) usage is attributed to, not a claude.ai user ID. Populated only when `claude_tag_user_id` is in `group_by[]`; null for usage that is not Claude Tag and for Claude Tag usage that is not attributed to a single user (for example `monitoring`, and `proactive` usage Claude initiated), so per-user rows can sum to less than the Claude Tag total. Cannot be combined with `group_by[]=rbac_group_id` or the `rbac_group_ids[]` filter.

    - `context_window: Optional[BetaAnalyticsContextWindow]`

      Context-window pricing tier of the usage or cost. Null unless `context_window` is in `group_by[]`; it can also be null on grouped rows with no context-window tier, such as code execution.

      - `"0-200k"`

      - `"200k-1M"`

    - `deployment_id: Optional[str]`

      Deployment that started the Claude Managed Agents session. Populated only when `deployment_id` is in `group_by[]`; null for usage outside a managed session and for sessions no deployment started.

    - `environment_id: Optional[str]`

      Claude Managed Agents environment the session ran in. Populated only when `environment_id` is in `group_by[]`; null for usage outside a managed session.

    - `inference_geo: Optional[BetaAnalyticsUsageCostInferenceGeo]`

      Inference region of the usage or cost. Null unless `inference_geo` is in `group_by[]`; it can also be null on grouped rows where the region is not set (the rows that `inference_geos[]=not_available` matches).

      - `"global"`

      - `"us"`

    - `model: Optional[str]`

      Model that produced the usage or cost, as a model name in the form the `models[]` filter accepts (for example, `claude-opus-5-5`). Null unless `model` is in `group_by[]`; it can also be null on grouped rows whose usage or cost is not attributed to a specific model, such as code execution.

    - `product: Optional[str]`

      Product surface that produced the usage or cost. Null unless product is in `group_by[]`; it can also be null on grouped rows whose usage cannot be attributed to a known surface. Values include `chat`, `claude_code`, `cowork`, `office_agent`, `claude_in_chrome`, `claude_design`, `claude_tag`, and `chat_cowork_unified`. `claude_tag` is Claude Tag, the Claude product in Slack. `chat_cowork_unified` is Chat and Cowork unified, Cowork's features inside claude.ai chat: chat and Cowork usage by a member who has it turned on is reported under this value instead of `chat` or `cowork`. It is accepted as a filter only where Chat and Cowork unified is available. Some unattributed usage is reported as "other".

    - `rbac_group_id: Optional[str]`

      RBAC group (team) the usage is attributed to, in the public tagged `rbac_group_...` spelling — the same spelling the activity resources use for this key, so the same team has one id across resources and it round-trips as an `rbac_group_ids[]` filter value. Populated only when `rbac_group_id` is in `group_by[]`. Any-membership semantics: a user in several groups contributes their full usage to each of those groups' rows, so the named-group rows overlap and their sum can exceed the org total. A null value is the single unassigned row: users in no group on that (UTC) day. For the true org total, run the same query without `group_by[]`.

    - `service_tier: Optional[BetaAnalyticsServiceTier]`

      Service tier the usage was served at. Populated only when `service_tier` is in `group_by[]`; null for usage with no service tier (for example, code execution) and for Claude Enterprise usage.

      - `"batch"`

      - `"flex"`

      - `"flex_discount"`

      - `"priority"`

      - `"priority_on_demand"`

      - `"standard"`

    - `session_id: Optional[str]`

      Claude Managed Agents session that incurred the usage. Populated only when `session_id` is in `group_by[]`; null for usage outside a managed session.

    - `slack_channel_id: Optional[str]`

      Slack channel the usage originated from. Populated only when `slack_channel_id` is in `group_by[]`; null for usage outside Slack (and for rows recorded before channel attribution was enabled).

    - `speed: Optional[BetaAnalyticsSpeed]`

      Inference speed mode of the usage or cost: `fast` or `standard`. Null unless `speed` is in `group_by[]`.

      - `"fast"`

      - `"standard"`

    - `user_profile_id: Optional[str]`

      User profile the usage was attributed to, as a tagged `uprof_` ID. Populated only when `user_profile_id` is in `group_by[]`; null for usage that named no profile and for Claude Enterprise usage.

    - `workspace_id: Optional[str]`

      Workspace the usage occurred in, as a tagged workspace ID, including the organization's default workspace. Populated only when `workspace_id` is in `group_by[]`; null for Claude Enterprise usage.

  - `starting_at: datetime`

    Start of the period this row covers (inclusive), as an RFC 3339 UTC timestamp: the start of the row's time bucket when a time-bucket width is set, otherwise the requested `starting_at` rounded down to the hour.

    format: date-time

  - `usage: BetaAnalyticsUsageMetrics`

    Token usage for this row.

    - `cache_creation: BetaCacheCreation`

      The number of input tokens for cache creation.

      - `ephemeral_1h_input_tokens: int`

        The number of input tokens used to create the 1 hour cache entry.

        default: 0, minimum: 0

      - `ephemeral_5m_input_tokens: int`

        The number of input tokens used to create the 5 minute cache entry.

        default: 0, minimum: 0

    - `cache_read_input_tokens: int`

      The number of input tokens read from the cache.

    - `output_tokens: int`

      The number of output tokens generated.

    - `requests: Optional[int]`

      Number of API requests in this row's scope. For sandbox / code-execution events, this counts execution spans rather than HTTP requests (these rows surface with `product: null`).

    - `server_tool_use: BetaAnalyticsServerToolUse`

      Server-side tool usage metrics.

      - `web_search_requests: int`

        The number of web search requests made.

    - `total_tokens: int`

      Total token count across all token types. This is the value the default `order_by` (`total_tokens`) sorts on.

    - `uncached_input_tokens: int`

      The number of uncached input tokens processed.

### Beta Analytics Usage Metrics

- `class BetaAnalyticsUsageMetrics`

  The token usage of one row.

  - `cache_creation: BetaCacheCreation`

    The number of input tokens for cache creation.

    - `ephemeral_1h_input_tokens: int`

      The number of input tokens used to create the 1 hour cache entry.

      default: 0, minimum: 0

    - `ephemeral_5m_input_tokens: int`

      The number of input tokens used to create the 5 minute cache entry.

      default: 0, minimum: 0

  - `cache_read_input_tokens: int`

    The number of input tokens read from the cache.

  - `output_tokens: int`

    The number of output tokens generated.

  - `requests: Optional[int]`

    Number of API requests in this row's scope. For sandbox / code-execution events, this counts execution spans rather than HTTP requests (these rows surface with `product: null`).

  - `server_tool_use: BetaAnalyticsServerToolUse`

    Server-side tool usage metrics.

    - `web_search_requests: int`

      The number of web search requests made.

  - `total_tokens: int`

    Total token count across all token types. This is the value the default `order_by` (`total_tokens`) sorts on.

  - `uncached_input_tokens: int`

    The number of uncached input tokens processed.

### Beta Analytics Usage Order By

- `type BetaAnalyticsUsageOrderBy = Literal["output_tokens", "requests", "time", 2 more]`

  - `"output_tokens"`

  - `"requests"`

  - `"time"`

  - `"total_tokens"`

  - `"uncached_input_tokens"`
