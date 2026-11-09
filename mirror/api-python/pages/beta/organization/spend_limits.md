---
title: Spend Limits
url: https://platform.claude.com/docs/en/api/python/beta/organization/spend_limits
---

# Spend Limits

## Set Spend Limit

`beta.organization.spend_limits.set(**kwargs) -> BetaSpendLimit`

**POST** `/v1/organizations/spend_limits`

Set a spend limit.

Upsert keyed on (scope, period): setting a limit that already exists
overwrites it in place. A Claude Enterprise organization sets `user`
limits. Its seat-tier, group, and organization-level defaults are configured
in claude.ai. A Claude Console organization sets `organization` and
`workspace` limits, which are monthly and always carry an amount. Setting those
limits is in an early access preview. To request access, contact your
Anthropic account team.

### Parameters

- `amount: Optional[str]`

  Limit amount as a non-negative integer decimal string in the minor unit of the organization's billing currency (cents for USD): "50000" is $500.00. `null` sets an explicit no-limit override for this scope and `period` only — each period resolves independently, so caps for other periods still apply.

- `scope: Scope`

  What the limit applies to. Claude Enterprise organizations set `user` limits. Claude Console organizations set `organization` and `workspace` limits. Any other combination returns 400. Setting `organization` and `workspace` limits through the API is in an early access preview. To request access, contact your Anthropic account team.

  - `class BetaSpendLimitUserScope`

    Scope selecting a single member of the organization.

    - `type: Literal["user"]`

      Scope type. Always `user` for this scope.

      default: user

    - `user_id: str`

      Tagged ID of the member the spend limit applies to.

  - `class BetaSpendLimitOrganizationScope`

    - `type: Literal["organization"]`

      default: organization

  - `class BetaSpendLimitWorkspaceScope`

    Scope selecting one workspace of a Claude Console organization.

    - `type: Literal["workspace"]`

      Scope type. Always `workspace` for this scope.

      default: workspace

    - `workspace_id: str`

      Tagged ID of the workspace the spend limit applies to.

- `period: Optional[BetaSpendLimitPeriod]`

  - `"daily"`

  - `"monthly"`

  - `"weekly"`

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  Optional header to specify the beta version(s) you want to use.

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

- `class BetaSpendLimit`

  A configured spend limit: a cap on metered spend for one scope and period.

  - `type: Literal["spend_limit"]`

    Object type. Always `spend_limit`.

    default: spend_limit

  - `id: str`

    Unique tagged ID of the spend limit (`spl_...`).

  - `amount: Optional[str]`

    Limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD): "50000" is $500.00. `null` means no numeric cap is configured at this scope — see the effective report for whether a limit applies.

  - `created_at: datetime`

    RFC 3339 datetime at which the spend limit was created.

    format: date-time

  - `currency: str`

    ISO 4217 code of the organization's billing currency; the unit for `amount`.

  - `is_enabled: bool`

    Read-only. `false` when extra usage is switched off for this organization (`organization` limit); `amount` is kept and applies again when it's switched back on. Always `true` for other limits.

  - `period: BetaSpendLimitPeriod`

    Length of the window the limit resets over. `amount` caps spend within each period.

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `scope: Scope`

    What the limit applies to. A tagged union on `type`; each variant carries the identifier for its scope.

    - `class BetaSpendLimitUserScope`

      Scope selecting a single member of the organization.

      - `type: Literal["user"]`

        Scope type. Always `user` for this scope.

        default: user

      - `user_id: str`

        Tagged ID of the member the spend limit applies to.

    - `class BetaSpendLimitSeatTierScope`

      - `type: Literal["seat_tier"]`

        default: seat_tier

      - `seat_tier: str`

    - `class BetaSpendLimitRBACGroupScope`

      - `type: Literal["rbac_group"]`

        default: rbac_group

      - `rbac_group_id: str`

    - `class BetaSpendLimitOrganizationServiceScope`

      - `type: Literal["organization_service"]`

        default: organization_service

      - `service: str`

    - `class BetaSpendLimitOrganizationScope`

      - `type: Literal["organization"]`

        default: organization

    - `class BetaSpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

      - `type: Literal["workspace"]`

        Scope type. Always `workspace` for this scope.

        default: workspace

      - `workspace_id: str`

        Tagged ID of the workspace the spend limit applies to.

    - `class BetaSpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

      - `type: Literal["usage_tier"]`

        Scope type. Always `usage_tier` for this scope.

        default: usage_tier

  - `updated_at: datetime`

    RFC 3339 datetime at which the spend limit was last modified.

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
beta_spend_limit = client.beta.organization.spend_limits.set(
    amount="50000",
    scope={
        "type": "user",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
    },
)
print(beta_spend_limit.id)
```

#### Response (200)

```json
{
  "id": "id",
  "amount": "50000",
  "created_at": "2019-12-27T18:11:19.117Z",
  "currency": "USD",
  "is_enabled": true,
  "period": "daily",
  "scope": {
    "type": "user",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "type": "spend_limit",
  "updated_at": "2019-12-27T18:11:19.117Z"
}
```

## Get Spend Limit

`beta.organization.spend_limits.retrieve(spend_limit_id) -> BetaSpendLimit`

**GET** `/v1/organizations/spend_limits/{spend_limit_id}`

Retrieve a spend limit by ID.

### Parameters

- `spend_limit_id: str` (path parameter)

  ID of the Spend Limit.

### Returns

- `class BetaSpendLimit`

  A configured spend limit: a cap on metered spend for one scope and period.

  - `type: Literal["spend_limit"]`

    Object type. Always `spend_limit`.

    default: spend_limit

  - `id: str`

    Unique tagged ID of the spend limit (`spl_...`).

  - `amount: Optional[str]`

    Limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD): "50000" is $500.00. `null` means no numeric cap is configured at this scope — see the effective report for whether a limit applies.

  - `created_at: datetime`

    RFC 3339 datetime at which the spend limit was created.

    format: date-time

  - `currency: str`

    ISO 4217 code of the organization's billing currency; the unit for `amount`.

  - `is_enabled: bool`

    Read-only. `false` when extra usage is switched off for this organization (`organization` limit); `amount` is kept and applies again when it's switched back on. Always `true` for other limits.

  - `period: BetaSpendLimitPeriod`

    Length of the window the limit resets over. `amount` caps spend within each period.

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `scope: Scope`

    What the limit applies to. A tagged union on `type`; each variant carries the identifier for its scope.

    - `class BetaSpendLimitUserScope`

      Scope selecting a single member of the organization.

      - `type: Literal["user"]`

        Scope type. Always `user` for this scope.

        default: user

      - `user_id: str`

        Tagged ID of the member the spend limit applies to.

    - `class BetaSpendLimitSeatTierScope`

      - `type: Literal["seat_tier"]`

        default: seat_tier

      - `seat_tier: str`

    - `class BetaSpendLimitRBACGroupScope`

      - `type: Literal["rbac_group"]`

        default: rbac_group

      - `rbac_group_id: str`

    - `class BetaSpendLimitOrganizationServiceScope`

      - `type: Literal["organization_service"]`

        default: organization_service

      - `service: str`

    - `class BetaSpendLimitOrganizationScope`

      - `type: Literal["organization"]`

        default: organization

    - `class BetaSpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

      - `type: Literal["workspace"]`

        Scope type. Always `workspace` for this scope.

        default: workspace

      - `workspace_id: str`

        Tagged ID of the workspace the spend limit applies to.

    - `class BetaSpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

      - `type: Literal["usage_tier"]`

        Scope type. Always `usage_tier` for this scope.

        default: usage_tier

  - `updated_at: datetime`

    RFC 3339 datetime at which the spend limit was last modified.

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
beta_spend_limit = client.beta.organization.spend_limits.retrieve(
    "spend_limit_id",
)
print(beta_spend_limit.id)
```

#### Response (200)

```json
{
  "id": "id",
  "amount": "50000",
  "created_at": "2019-12-27T18:11:19.117Z",
  "currency": "USD",
  "is_enabled": true,
  "period": "daily",
  "scope": {
    "type": "user",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "type": "spend_limit",
  "updated_at": "2019-12-27T18:11:19.117Z"
}
```

## Delete Spend Limit

`beta.organization.spend_limits.delete(spend_limit_id) -> SpendLimitDeleteResponse`

**DELETE** `/v1/organizations/spend_limits/{spend_limit_id}`

Delete a spend limit.

For a Claude Enterprise organization, this deletes a per-user override, and
the member falls back to any inherited spend limit at that period. Its
seat-tier, group, and organization-level rows cannot be deleted via this
endpoint. A Claude Console organization deletes its organization and
workspace limits, but not its `usage_tier` limit. Deleting organization and
workspace limits through the API is in an early access preview.

### Parameters

- `spend_limit_id: str` (path parameter)

  ID of the Spend Limit.

### Returns

- `class SpendLimitDeleteResponse`

  - `type: Literal["spend_limit_deleted"]`

    default: spend_limit_deleted

  - `id: str`

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
spend_limit = client.beta.organization.spend_limits.delete(
    "spend_limit_id",
)
print(spend_limit.id)
```

#### Response (200)

```json
{
  "id": "id",
  "type": "spend_limit_deleted"
}
```

## List Spend Limits

`beta.organization.spend_limits.list(**kwargs) -> SyncPageCursor[BetaSpendLimit]`

**GET** `/v1/organizations/spend_limits`

List the organization's spend limits.

A Claude Console organization's limits, including any read-only `usage_tier`
limit, come newest first. Listing them is in an early access preview. To
request access, contact your Anthropic account team. A Claude Enterprise
organization's limits are grouped by scope type, in the order `organization`,
`seat_tier`, `rbac_group`, `organization_service`, `user`; within a type they
come in a fixed order that is not creation order.

### Parameters

- `limit: Optional[int]` (query parameter)

  Maximum number of limits per page. Defaults to `20`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field.

- `scope_type: Optional[List[Literal["organization", "organization_service", "rbac_group", 4 more]]]` (query parameter)

  Return only limits with these scope types. Omit for all. A scope type that doesn't apply to the organization gets a 400 error.

  maxItems: 100

  - `"organization"`

  - `"organization_service"`

  - `"rbac_group"`

  - `"seat_tier"`

  - `"usage_tier"`

  - `"user"`

  - `"workspace"`

- `workspace_id: Optional[str]` (query parameter)

  Return only the limits whose `scope.workspace_id` is this workspace (`wrkspc_...`). Claude Console organizations only; other organizations get a 400 error.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  This endpoint is in beta: requests must send `spend-limit-reads-2026-09-26` in this header.

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

- `class BetaSpendLimit`

  A configured spend limit: a cap on metered spend for one scope and period.

  - `type: Literal["spend_limit"]`

    Object type. Always `spend_limit`.

    default: spend_limit

  - `id: str`

    Unique tagged ID of the spend limit (`spl_...`).

  - `amount: Optional[str]`

    Limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD): "50000" is $500.00. `null` means no numeric cap is configured at this scope — see the effective report for whether a limit applies.

  - `created_at: datetime`

    RFC 3339 datetime at which the spend limit was created.

    format: date-time

  - `currency: str`

    ISO 4217 code of the organization's billing currency; the unit for `amount`.

  - `is_enabled: bool`

    Read-only. `false` when extra usage is switched off for this organization (`organization` limit); `amount` is kept and applies again when it's switched back on. Always `true` for other limits.

  - `period: BetaSpendLimitPeriod`

    Length of the window the limit resets over. `amount` caps spend within each period.

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `scope: Scope`

    What the limit applies to. A tagged union on `type`; each variant carries the identifier for its scope.

    - `class BetaSpendLimitUserScope`

      Scope selecting a single member of the organization.

      - `type: Literal["user"]`

        Scope type. Always `user` for this scope.

        default: user

      - `user_id: str`

        Tagged ID of the member the spend limit applies to.

    - `class BetaSpendLimitSeatTierScope`

      - `type: Literal["seat_tier"]`

        default: seat_tier

      - `seat_tier: str`

    - `class BetaSpendLimitRBACGroupScope`

      - `type: Literal["rbac_group"]`

        default: rbac_group

      - `rbac_group_id: str`

    - `class BetaSpendLimitOrganizationServiceScope`

      - `type: Literal["organization_service"]`

        default: organization_service

      - `service: str`

    - `class BetaSpendLimitOrganizationScope`

      - `type: Literal["organization"]`

        default: organization

    - `class BetaSpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

      - `type: Literal["workspace"]`

        Scope type. Always `workspace` for this scope.

        default: workspace

      - `workspace_id: str`

        Tagged ID of the workspace the spend limit applies to.

    - `class BetaSpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

      - `type: Literal["usage_tier"]`

        Scope type. Always `usage_tier` for this scope.

        default: usage_tier

  - `updated_at: datetime`

    RFC 3339 datetime at which the spend limit was last modified.

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
page = client.beta.organization.spend_limits.list()
page = page.data[0]
print(page.id)
```

#### Response (200)

```json
{
  "data": [
    {
      "id": "id",
      "amount": "50000",
      "created_at": "2019-12-27T18:11:19.117Z",
      "currency": "USD",
      "is_enabled": true,
      "period": "daily",
      "scope": {
        "type": "user",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
      },
      "type": "spend_limit",
      "updated_at": "2019-12-27T18:11:19.117Z"
    }
  ],
  "next_page": "next_page"
}
```

## Domain types

### Beta Spend Limit

- `class BetaSpendLimit`

  A configured spend limit: a cap on metered spend for one scope and period.

  - `type: Literal["spend_limit"]`

    Object type. Always `spend_limit`.

    default: spend_limit

  - `id: str`

    Unique tagged ID of the spend limit (`spl_...`).

  - `amount: Optional[str]`

    Limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD): "50000" is $500.00. `null` means no numeric cap is configured at this scope — see the effective report for whether a limit applies.

  - `created_at: datetime`

    RFC 3339 datetime at which the spend limit was created.

    format: date-time

  - `currency: str`

    ISO 4217 code of the organization's billing currency; the unit for `amount`.

  - `is_enabled: bool`

    Read-only. `false` when extra usage is switched off for this organization (`organization` limit); `amount` is kept and applies again when it's switched back on. Always `true` for other limits.

  - `period: BetaSpendLimitPeriod`

    Length of the window the limit resets over. `amount` caps spend within each period.

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `scope: Scope`

    What the limit applies to. A tagged union on `type`; each variant carries the identifier for its scope.

    - `class BetaSpendLimitUserScope`

      Scope selecting a single member of the organization.

      - `type: Literal["user"]`

        Scope type. Always `user` for this scope.

        default: user

      - `user_id: str`

        Tagged ID of the member the spend limit applies to.

    - `class BetaSpendLimitSeatTierScope`

      - `type: Literal["seat_tier"]`

        default: seat_tier

      - `seat_tier: str`

    - `class BetaSpendLimitRBACGroupScope`

      - `type: Literal["rbac_group"]`

        default: rbac_group

      - `rbac_group_id: str`

    - `class BetaSpendLimitOrganizationServiceScope`

      - `type: Literal["organization_service"]`

        default: organization_service

      - `service: str`

    - `class BetaSpendLimitOrganizationScope`

      - `type: Literal["organization"]`

        default: organization

    - `class BetaSpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

      - `type: Literal["workspace"]`

        Scope type. Always `workspace` for this scope.

        default: workspace

      - `workspace_id: str`

        Tagged ID of the workspace the spend limit applies to.

    - `class BetaSpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

      - `type: Literal["usage_tier"]`

        Scope type. Always `usage_tier` for this scope.

        default: usage_tier

  - `updated_at: datetime`

    RFC 3339 datetime at which the spend limit was last modified.

    format: date-time

### Beta Spend Limit Organization Scope

- `class BetaSpendLimitOrganizationScope`

  - `type: Literal["organization"]`

    default: organization

### Beta Spend Limit Organization Service Scope

- `class BetaSpendLimitOrganizationServiceScope`

  - `type: Literal["organization_service"]`

    default: organization_service

  - `service: str`

### Beta Spend Limit Period

- `type BetaSpendLimitPeriod = Literal["daily", "monthly", "weekly"]`

  - `"daily"`

  - `"monthly"`

  - `"weekly"`

### Beta Spend Limit RBAC Group Scope

- `class BetaSpendLimitRBACGroupScope`

  - `type: Literal["rbac_group"]`

    default: rbac_group

  - `rbac_group_id: str`

### Beta Spend Limit Scoped API Key Actor

- `class BetaSpendLimitScopedAPIKeyActor`

  A scoped Admin API key acting on behalf of the organization.

  - `type: Literal["scoped_api_key_actor"]`

    default: scoped_api_key_actor

  - `scoped_api_key_id: str`

### Beta Spend Limit Seat Tier Scope

- `class BetaSpendLimitSeatTierScope`

  - `type: Literal["seat_tier"]`

    default: seat_tier

  - `seat_tier: str`

### Beta Spend Limit Usage Tier Scope

- `class BetaSpendLimitUsageTierScope`

  Scope of the monthly spend cap Anthropic sets for a Claude Console
  organization from its usage tier, or a higher cap Anthropic granted the
  organization. Read-only; its `created_at` and `updated_at` are the
  organization's creation time, so `amount` can change while `updated_at` stays
  the same.

  - `type: Literal["usage_tier"]`

    Scope type. Always `usage_tier` for this scope.

    default: usage_tier

### Beta Spend Limit User Actor

- `class BetaSpendLimitUserActor`

  A user within the organization. `name` and `email_address` are
  null when the underlying account is unavailable or has been deleted;
  `deleted` is true only for deleted accounts.

  - `type: Literal["user_actor"]`

    Actor type. Always `user_actor`.

    default: user_actor

  - `deleted: bool`

    True only when the underlying account has been deleted.

    default: false

  - `email_address: Optional[str]`

    The user's email address. Null when the account is unavailable or has been deleted.

  - `name: Optional[str]`

    The user's current display name. Null when the account is unavailable, has been deleted, or has no name set.

  - `user_id: str`

    Tagged ID of the user.

### Beta Spend Limit User Scope

- `class BetaSpendLimitUserScope`

  Scope selecting a single member of the organization.

  - `type: Literal["user"]`

    Scope type. Always `user` for this scope.

    default: user

  - `user_id: str`

    Tagged ID of the member the spend limit applies to.

### Beta Spend Limit Workspace Scope

- `class BetaSpendLimitWorkspaceScope`

  Scope selecting one workspace of a Claude Console organization.

  - `type: Literal["workspace"]`

    Scope type. Always `workspace` for this scope.

    default: workspace

  - `workspace_id: str`

    Tagged ID of the workspace the spend limit applies to.

### Beta Spend Summary

- `class BetaSpendSummary`

  Per-member effective-limit report row (`GET /spend_limits/effective`).

  - `actor: Actor`

    - `class BetaSpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

      - `type: Literal["user_actor"]`

        Actor type. Always `user_actor`.

        default: user_actor

      - `deleted: bool`

        True only when the underlying account has been deleted.

        default: false

      - `email_address: Optional[str]`

        The user's email address. Null when the account is unavailable or has been deleted.

      - `name: Optional[str]`

        The user's current display name. Null when the account is unavailable, has been deleted, or has no name set.

      - `user_id: str`

        Tagged ID of the user.

    - `class BetaSpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `amount: Optional[str]`

    Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

  - `currency: str`

    ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

  - `period: BetaSpendLimitPeriod`

    Period this row's effective limit and spend are reported for.

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `period_to_date_spend: str`

    The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

  - `scope: Scope`

    - `class BetaSpendLimitUserScope`

      Scope selecting a single member of the organization.

      - `type: Literal["user"]`

        Scope type. Always `user` for this scope.

        default: user

      - `user_id: str`

        Tagged ID of the member the spend limit applies to.

    - `class BetaSpendLimitSeatTierScope`

      - `type: Literal["seat_tier"]`

        default: seat_tier

      - `seat_tier: str`

    - `class BetaSpendLimitRBACGroupScope`

      - `type: Literal["rbac_group"]`

        default: rbac_group

      - `rbac_group_id: str`

    - `class BetaSpendLimitOrganizationServiceScope`

      - `type: Literal["organization_service"]`

        default: organization_service

      - `service: str`

    - `class BetaSpendLimitOrganizationScope`

      - `type: Literal["organization"]`

        default: organization

    - `class BetaSpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

      - `type: Literal["workspace"]`

        Scope type. Always `workspace` for this scope.

        default: workspace

      - `workspace_id: str`

        Tagged ID of the workspace the spend limit applies to.

    - `class BetaSpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

      - `type: Literal["usage_tier"]`

        Scope type. Always `usage_tier` for this scope.

        default: usage_tier

  - `source: Source`

    - `class BetaSpendLimitUserScope`

      Scope selecting a single member of the organization.

    - `class BetaSpendLimitSeatTierScope`

    - `class BetaSpendLimitRBACGroupScope`

    - `class BetaSpendLimitOrganizationServiceScope`

    - `class BetaSpendLimitOrganizationScope`

    - `class BetaSpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

    - `class BetaSpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

  - `spend_limit_id: str`

### Spend Limit Delete Response

- `class SpendLimitDeleteResponse`

  - `type: Literal["spend_limit_deleted"]`

    default: spend_limit_deleted

  - `id: str`

## Spend Limits › Effective

### List Effective Spend Limits

`beta.organization.spend_limits.effective.list(**kwargs) -> SyncPageCursor[BetaSpendSummary]`

**GET** `/v1/organizations/spend_limits/effective`

List each member's effective spend limit and period-to-date spend.

Returns one row per (member, period) the member resolves a spend limit
for, with the `source` scope the spend limit was inherited from.
Paginates by member, so a member's periods never split across pages.
Supported for Claude Enterprise organizations only, not for Claude Console
organizations.

#### Parameters

- `limit: Optional[int]` (query parameter)

  Maximum number of members per page. A member's period rows never split across pages, so a page may carry more rows than this. Defaults to `20`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field.

- `period: Optional[List[BetaSpendLimitPeriod]]` (query parameter)

  Restrict the report to these limit periods. Omit to return one row per period each member resolves a spend limit for.

  maxItems: 3

  - `"daily"`

  - `"monthly"`

  - `"weekly"`

- `user_ids: Optional[Sequence[str]]` (query parameter)

  Restrict the report to these members, by tagged user ID (`user_...`). At most 100 entries.

  maxItems: 100

#### Returns

- `class BetaSpendSummary`

  Per-member effective-limit report row (`GET /spend_limits/effective`).

  - `actor: Actor`

    - `class BetaSpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

      - `type: Literal["user_actor"]`

        Actor type. Always `user_actor`.

        default: user_actor

      - `deleted: bool`

        True only when the underlying account has been deleted.

        default: false

      - `email_address: Optional[str]`

        The user's email address. Null when the account is unavailable or has been deleted.

      - `name: Optional[str]`

        The user's current display name. Null when the account is unavailable, has been deleted, or has no name set.

      - `user_id: str`

        Tagged ID of the user.

    - `class BetaSpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `amount: Optional[str]`

    Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

  - `currency: str`

    ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

  - `period: BetaSpendLimitPeriod`

    Period this row's effective limit and spend are reported for.

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `period_to_date_spend: str`

    The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

  - `scope: Scope`

    - `class BetaSpendLimitUserScope`

      Scope selecting a single member of the organization.

      - `type: Literal["user"]`

        Scope type. Always `user` for this scope.

        default: user

      - `user_id: str`

        Tagged ID of the member the spend limit applies to.

    - `class BetaSpendLimitSeatTierScope`

      - `type: Literal["seat_tier"]`

        default: seat_tier

      - `seat_tier: str`

    - `class BetaSpendLimitRBACGroupScope`

      - `type: Literal["rbac_group"]`

        default: rbac_group

      - `rbac_group_id: str`

    - `class BetaSpendLimitOrganizationServiceScope`

      - `type: Literal["organization_service"]`

        default: organization_service

      - `service: str`

    - `class BetaSpendLimitOrganizationScope`

      - `type: Literal["organization"]`

        default: organization

    - `class BetaSpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

      - `type: Literal["workspace"]`

        Scope type. Always `workspace` for this scope.

        default: workspace

      - `workspace_id: str`

        Tagged ID of the workspace the spend limit applies to.

    - `class BetaSpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

      - `type: Literal["usage_tier"]`

        Scope type. Always `usage_tier` for this scope.

        default: usage_tier

  - `source: Source`

    - `class BetaSpendLimitUserScope`

      Scope selecting a single member of the organization.

    - `class BetaSpendLimitSeatTierScope`

    - `class BetaSpendLimitRBACGroupScope`

    - `class BetaSpendLimitOrganizationServiceScope`

    - `class BetaSpendLimitOrganizationScope`

    - `class BetaSpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

    - `class BetaSpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

  - `spend_limit_id: str`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.spend_limits.effective.list()
page = page.data[0]
print(page.spend_limit_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "actor": {
        "deleted": true,
        "email_address": "email_address",
        "name": "name",
        "type": "user_actor",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
      },
      "amount": "50000",
      "currency": "USD",
      "period": "daily",
      "period_to_date_spend": "12050.5",
      "scope": {
        "type": "user",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
      },
      "source": {
        "type": "user",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
      },
      "spend_limit_id": "spend_limit_id"
    }
  ],
  "next_page": "next_page"
}
```

## Spend Limits › Increase Requests

### List Spend Limit Increase Requests

`beta.organization.spend_limits.increase_requests.list(**kwargs) -> SyncPageCursor[BetaSpendLimitIncreaseRequest]`

**GET** `/v1/organizations/spend_limit_increase_requests`

List spend limit increase requests, most recent first.

Pending requests include a live `spend_summary` for the requester.
Requests whose requester is no longer a member are excluded.

#### Parameters

- `actor_ids: Optional[Sequence[str]]` (query parameter)

  Filter by requester, as `user_...` tagged IDs.

- `limit: Optional[int]` (query parameter)

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

- `status: Optional[List[BetaSpendLimitIncreaseRequestStatus]]` (query parameter)

  Filter by status. Omit to return all.

  - `"approved"`

  - `"denied"`

  - `"pending"`

#### Returns

- `class BetaSpendLimitIncreaseRequest`

  - `type: Literal["spend_limit_increase_request"]`

    default: spend_limit_increase_request

  - `id: str`

  - `actor: BetaSpendLimitIncreaseRequestActor`

    Who submitted the increase request.

    - `class BetaSpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

      - `type: Literal["user_actor"]`

        Actor type. Always `user_actor`.

        default: user_actor

      - `deleted: bool`

        True only when the underlying account has been deleted.

        default: false

      - `email_address: Optional[str]`

        The user's email address. Null when the account is unavailable or has been deleted.

      - `name: Optional[str]`

        The user's current display name. Null when the account is unavailable, has been deleted, or has no name set.

      - `user_id: str`

        Tagged ID of the user.

    - `class BetaSpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `created_at: datetime`

    format: date-time

  - `period: BetaSpendLimitPeriod`

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `resolved_at: Optional[datetime]`

    format: date-time

  - `resolved_by: Optional[BetaSpendLimitIncreaseRequestResolvedBy]`

    Who approved or denied the increase request.

    - `class BetaSpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

    - `class BetaSpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

  - `spend_summary: Optional[BetaSpendSummary]`

    Per-member effective-limit report row (`GET /spend_limits/effective`).

    - `actor: Actor`

      - `class BetaSpendLimitUserActor`

        A user within the organization. `name` and `email_address` are
        null when the underlying account is unavailable or has been deleted;
        `deleted` is true only for deleted accounts.

      - `class BetaSpendLimitScopedAPIKeyActor`

        A scoped Admin API key acting on behalf of the organization.

    - `amount: Optional[str]`

      Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

    - `period: BetaSpendLimitPeriod`

      Period this row's effective limit and spend are reported for.

    - `period_to_date_spend: str`

      The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

    - `scope: Scope`

      - `class BetaSpendLimitUserScope`

        Scope selecting a single member of the organization.

        - `type: Literal["user"]`

          Scope type. Always `user` for this scope.

          default: user

        - `user_id: str`

          Tagged ID of the member the spend limit applies to.

      - `class BetaSpendLimitSeatTierScope`

        - `type: Literal["seat_tier"]`

          default: seat_tier

        - `seat_tier: str`

      - `class BetaSpendLimitRBACGroupScope`

        - `type: Literal["rbac_group"]`

          default: rbac_group

        - `rbac_group_id: str`

      - `class BetaSpendLimitOrganizationServiceScope`

        - `type: Literal["organization_service"]`

          default: organization_service

        - `service: str`

      - `class BetaSpendLimitOrganizationScope`

        - `type: Literal["organization"]`

          default: organization

      - `class BetaSpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

        - `type: Literal["workspace"]`

          Scope type. Always `workspace` for this scope.

          default: workspace

        - `workspace_id: str`

          Tagged ID of the workspace the spend limit applies to.

      - `class BetaSpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

        - `type: Literal["usage_tier"]`

          Scope type. Always `usage_tier` for this scope.

          default: usage_tier

    - `source: Source`

      - `class BetaSpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class BetaSpendLimitSeatTierScope`

      - `class BetaSpendLimitRBACGroupScope`

      - `class BetaSpendLimitOrganizationServiceScope`

      - `class BetaSpendLimitOrganizationScope`

      - `class BetaSpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class BetaSpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `spend_limit_id: str`

  - `status: BetaSpendLimitIncreaseRequestStatus`

    - `"approved"`

    - `"denied"`

    - `"pending"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.spend_limits.increase_requests.list()
page = page.data[0]
print(page.id)
```

##### Response (200)

```json
{
  "data": [
    {
      "id": "id",
      "actor": {
        "deleted": true,
        "email_address": "email_address",
        "name": "name",
        "type": "user_actor",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
      },
      "created_at": "2019-12-27T18:11:19.117Z",
      "period": "daily",
      "resolved_at": "2019-12-27T18:11:19.117Z",
      "resolved_by": {
        "deleted": true,
        "email_address": "email_address",
        "name": "name",
        "type": "user_actor",
        "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
      },
      "spend_summary": {
        "actor": {
          "deleted": true,
          "email_address": "email_address",
          "name": "name",
          "type": "user_actor",
          "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
        },
        "amount": "50000",
        "currency": "USD",
        "period": "daily",
        "period_to_date_spend": "12050.5",
        "scope": {
          "type": "user",
          "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
        },
        "source": {
          "type": "user",
          "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
        },
        "spend_limit_id": "spend_limit_id"
      },
      "status": "approved",
      "type": "spend_limit_increase_request"
    }
  ],
  "next_page": "next_page"
}
```

### Get Spend Limit Increase Request

`beta.organization.spend_limits.increase_requests.retrieve(spend_limit_increase_request_id) -> BetaSpendLimitIncreaseRequest`

**GET** `/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}`

Retrieve a spend limit increase request.

While `pending`, the response includes a live `spend_summary` for the
requester at the request's period.

#### Parameters

- `spend_limit_increase_request_id: str` (path parameter)

  ID of the spend limit increase request.

#### Returns

- `class BetaSpendLimitIncreaseRequest`

  - `type: Literal["spend_limit_increase_request"]`

    default: spend_limit_increase_request

  - `id: str`

  - `actor: BetaSpendLimitIncreaseRequestActor`

    Who submitted the increase request.

    - `class BetaSpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

      - `type: Literal["user_actor"]`

        Actor type. Always `user_actor`.

        default: user_actor

      - `deleted: bool`

        True only when the underlying account has been deleted.

        default: false

      - `email_address: Optional[str]`

        The user's email address. Null when the account is unavailable or has been deleted.

      - `name: Optional[str]`

        The user's current display name. Null when the account is unavailable, has been deleted, or has no name set.

      - `user_id: str`

        Tagged ID of the user.

    - `class BetaSpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `created_at: datetime`

    format: date-time

  - `period: BetaSpendLimitPeriod`

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `resolved_at: Optional[datetime]`

    format: date-time

  - `resolved_by: Optional[BetaSpendLimitIncreaseRequestResolvedBy]`

    Who approved or denied the increase request.

    - `class BetaSpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

    - `class BetaSpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

  - `spend_summary: Optional[BetaSpendSummary]`

    Per-member effective-limit report row (`GET /spend_limits/effective`).

    - `actor: Actor`

      - `class BetaSpendLimitUserActor`

        A user within the organization. `name` and `email_address` are
        null when the underlying account is unavailable or has been deleted;
        `deleted` is true only for deleted accounts.

      - `class BetaSpendLimitScopedAPIKeyActor`

        A scoped Admin API key acting on behalf of the organization.

    - `amount: Optional[str]`

      Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

    - `period: BetaSpendLimitPeriod`

      Period this row's effective limit and spend are reported for.

    - `period_to_date_spend: str`

      The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

    - `scope: Scope`

      - `class BetaSpendLimitUserScope`

        Scope selecting a single member of the organization.

        - `type: Literal["user"]`

          Scope type. Always `user` for this scope.

          default: user

        - `user_id: str`

          Tagged ID of the member the spend limit applies to.

      - `class BetaSpendLimitSeatTierScope`

        - `type: Literal["seat_tier"]`

          default: seat_tier

        - `seat_tier: str`

      - `class BetaSpendLimitRBACGroupScope`

        - `type: Literal["rbac_group"]`

          default: rbac_group

        - `rbac_group_id: str`

      - `class BetaSpendLimitOrganizationServiceScope`

        - `type: Literal["organization_service"]`

          default: organization_service

        - `service: str`

      - `class BetaSpendLimitOrganizationScope`

        - `type: Literal["organization"]`

          default: organization

      - `class BetaSpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

        - `type: Literal["workspace"]`

          Scope type. Always `workspace` for this scope.

          default: workspace

        - `workspace_id: str`

          Tagged ID of the workspace the spend limit applies to.

      - `class BetaSpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

        - `type: Literal["usage_tier"]`

          Scope type. Always `usage_tier` for this scope.

          default: usage_tier

    - `source: Source`

      - `class BetaSpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class BetaSpendLimitSeatTierScope`

      - `class BetaSpendLimitRBACGroupScope`

      - `class BetaSpendLimitOrganizationServiceScope`

      - `class BetaSpendLimitOrganizationScope`

      - `class BetaSpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class BetaSpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `spend_limit_id: str`

  - `status: BetaSpendLimitIncreaseRequestStatus`

    - `"approved"`

    - `"denied"`

    - `"pending"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_spend_limit_increase_request = (
    client.beta.organization.spend_limits.increase_requests.retrieve(
        "spend_limit_increase_request_id",
    )
)
print(beta_spend_limit_increase_request.id)
```

##### Response (200)

```json
{
  "id": "id",
  "actor": {
    "deleted": true,
    "email_address": "email_address",
    "name": "name",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "created_at": "2019-12-27T18:11:19.117Z",
  "period": "daily",
  "resolved_at": "2019-12-27T18:11:19.117Z",
  "resolved_by": {
    "deleted": true,
    "email_address": "email_address",
    "name": "name",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "spend_summary": {
    "actor": {
      "deleted": true,
      "email_address": "email_address",
      "name": "name",
      "type": "user_actor",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "amount": "50000",
    "currency": "USD",
    "period": "daily",
    "period_to_date_spend": "12050.5",
    "scope": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "source": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "spend_limit_id": "spend_limit_id"
  },
  "status": "approved",
  "type": "spend_limit_increase_request"
}
```

### Approve Spend Limit Increase Request

`beta.organization.spend_limits.increase_requests.approve(spend_limit_increase_request_id, **kwargs) -> IncreaseRequestApproveResponse`

**POST** `/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}/approve`

Approve a pending spend limit increase request.

Writes a per-user spend limit at `amount` for the requester and
transitions the request to `approved`. `period` defaults to the period
the member was blocked on. Anthropic emails the requester unless
`suppress_notification` is set.

#### Parameters

- `spend_limit_increase_request_id: str` (path parameter)

  ID of the spend limit increase request.

- `amount: str`

  New per-user spend limit as a non-negative integer decimal string (minor units).

- `period: Optional[BetaSpendLimitPeriod]`

  - `"daily"`

  - `"monthly"`

  - `"weekly"`

- `suppress_notification: Optional[bool]`

#### Returns

- `class IncreaseRequestApproveResponse`

  - `type: Literal["spend_limit_increase_request"]`

    default: spend_limit_increase_request

  - `id: str`

  - `actor: BetaSpendLimitIncreaseRequestActor`

    Who submitted the increase request.

    - `class BetaSpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

      - `type: Literal["user_actor"]`

        Actor type. Always `user_actor`.

        default: user_actor

      - `deleted: bool`

        True only when the underlying account has been deleted.

        default: false

      - `email_address: Optional[str]`

        The user's email address. Null when the account is unavailable or has been deleted.

      - `name: Optional[str]`

        The user's current display name. Null when the account is unavailable, has been deleted, or has no name set.

      - `user_id: str`

        Tagged ID of the user.

    - `class BetaSpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `created_at: datetime`

    format: date-time

  - `period: BetaSpendLimitPeriod`

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `resolved_at: Optional[datetime]`

    format: date-time

  - `resolved_by: Optional[BetaSpendLimitIncreaseRequestResolvedBy]`

    Who approved or denied the increase request.

    - `class BetaSpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

    - `class BetaSpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

  - `spend_limit: Optional[BetaSpendLimit]`

    A configured spend limit: a cap on metered spend for one scope and period.

    - `type: Literal["spend_limit"]`

      Object type. Always `spend_limit`.

      default: spend_limit

    - `id: str`

      Unique tagged ID of the spend limit (`spl_...`).

    - `amount: Optional[str]`

      Limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD): "50000" is $500.00. `null` means no numeric cap is configured at this scope — see the effective report for whether a limit applies.

    - `created_at: datetime`

      RFC 3339 datetime at which the spend limit was created.

      format: date-time

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount`.

    - `is_enabled: bool`

      Read-only. `false` when extra usage is switched off for this organization (`organization` limit); `amount` is kept and applies again when it's switched back on. Always `true` for other limits.

    - `period: BetaSpendLimitPeriod`

      Length of the window the limit resets over. `amount` caps spend within each period.

    - `scope: Scope`

      What the limit applies to. A tagged union on `type`; each variant carries the identifier for its scope.

      - `class BetaSpendLimitUserScope`

        Scope selecting a single member of the organization.

        - `type: Literal["user"]`

          Scope type. Always `user` for this scope.

          default: user

        - `user_id: str`

          Tagged ID of the member the spend limit applies to.

      - `class BetaSpendLimitSeatTierScope`

        - `type: Literal["seat_tier"]`

          default: seat_tier

        - `seat_tier: str`

      - `class BetaSpendLimitRBACGroupScope`

        - `type: Literal["rbac_group"]`

          default: rbac_group

        - `rbac_group_id: str`

      - `class BetaSpendLimitOrganizationServiceScope`

        - `type: Literal["organization_service"]`

          default: organization_service

        - `service: str`

      - `class BetaSpendLimitOrganizationScope`

        - `type: Literal["organization"]`

          default: organization

      - `class BetaSpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

        - `type: Literal["workspace"]`

          Scope type. Always `workspace` for this scope.

          default: workspace

        - `workspace_id: str`

          Tagged ID of the workspace the spend limit applies to.

      - `class BetaSpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

        - `type: Literal["usage_tier"]`

          Scope type. Always `usage_tier` for this scope.

          default: usage_tier

    - `updated_at: datetime`

      RFC 3339 datetime at which the spend limit was last modified.

      format: date-time

  - `spend_summary: Optional[BetaSpendSummary]`

    Per-member effective-limit report row (`GET /spend_limits/effective`).

    - `actor: Actor`

      - `class BetaSpendLimitUserActor`

        A user within the organization. `name` and `email_address` are
        null when the underlying account is unavailable or has been deleted;
        `deleted` is true only for deleted accounts.

      - `class BetaSpendLimitScopedAPIKeyActor`

        A scoped Admin API key acting on behalf of the organization.

    - `amount: Optional[str]`

      Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

    - `period: BetaSpendLimitPeriod`

      Period this row's effective limit and spend are reported for.

    - `period_to_date_spend: str`

      The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

    - `scope: Scope`

      - `class BetaSpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class BetaSpendLimitSeatTierScope`

      - `class BetaSpendLimitRBACGroupScope`

      - `class BetaSpendLimitOrganizationServiceScope`

      - `class BetaSpendLimitOrganizationScope`

      - `class BetaSpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class BetaSpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `source: Source`

      - `class BetaSpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class BetaSpendLimitSeatTierScope`

      - `class BetaSpendLimitRBACGroupScope`

      - `class BetaSpendLimitOrganizationServiceScope`

      - `class BetaSpendLimitOrganizationScope`

      - `class BetaSpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class BetaSpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `spend_limit_id: str`

  - `status: BetaSpendLimitIncreaseRequestStatus`

    - `"approved"`

    - `"denied"`

    - `"pending"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
response = client.beta.organization.spend_limits.increase_requests.approve(
    spend_limit_increase_request_id="spend_limit_increase_request_id",
    amount="50000",
)
print(response.id)
```

##### Response (200)

```json
{
  "id": "id",
  "actor": {
    "deleted": true,
    "email_address": "email_address",
    "name": "name",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "created_at": "2019-12-27T18:11:19.117Z",
  "period": "daily",
  "resolved_at": "2019-12-27T18:11:19.117Z",
  "resolved_by": {
    "deleted": true,
    "email_address": "email_address",
    "name": "name",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "spend_limit": {
    "id": "id",
    "amount": "50000",
    "created_at": "2019-12-27T18:11:19.117Z",
    "currency": "USD",
    "is_enabled": true,
    "period": "daily",
    "scope": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "type": "spend_limit",
    "updated_at": "2019-12-27T18:11:19.117Z"
  },
  "spend_summary": {
    "actor": {
      "deleted": true,
      "email_address": "email_address",
      "name": "name",
      "type": "user_actor",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "amount": "50000",
    "currency": "USD",
    "period": "daily",
    "period_to_date_spend": "12050.5",
    "scope": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "source": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "spend_limit_id": "spend_limit_id"
  },
  "status": "approved",
  "type": "spend_limit_increase_request"
}
```

### Deny Spend Limit Increase Request

`beta.organization.spend_limits.increase_requests.deny(spend_limit_increase_request_id, **kwargs) -> BetaSpendLimitIncreaseRequest`

**POST** `/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}/deny`

Deny a pending spend limit increase request.

Idempotent on `denied`; denying an already-`approved` request returns
400. Anthropic emails the requester unless `suppress_notification` is set.

#### Parameters

- `spend_limit_increase_request_id: str` (path parameter)

  ID of the spend limit increase request.

- `suppress_notification: Optional[bool]`

#### Returns

- `class BetaSpendLimitIncreaseRequest`

  - `type: Literal["spend_limit_increase_request"]`

    default: spend_limit_increase_request

  - `id: str`

  - `actor: BetaSpendLimitIncreaseRequestActor`

    Who submitted the increase request.

    - `class BetaSpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

      - `type: Literal["user_actor"]`

        Actor type. Always `user_actor`.

        default: user_actor

      - `deleted: bool`

        True only when the underlying account has been deleted.

        default: false

      - `email_address: Optional[str]`

        The user's email address. Null when the account is unavailable or has been deleted.

      - `name: Optional[str]`

        The user's current display name. Null when the account is unavailable, has been deleted, or has no name set.

      - `user_id: str`

        Tagged ID of the user.

    - `class BetaSpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `created_at: datetime`

    format: date-time

  - `period: BetaSpendLimitPeriod`

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `resolved_at: Optional[datetime]`

    format: date-time

  - `resolved_by: Optional[BetaSpendLimitIncreaseRequestResolvedBy]`

    Who approved or denied the increase request.

    - `class BetaSpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

    - `class BetaSpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

  - `spend_summary: Optional[BetaSpendSummary]`

    Per-member effective-limit report row (`GET /spend_limits/effective`).

    - `actor: Actor`

      - `class BetaSpendLimitUserActor`

        A user within the organization. `name` and `email_address` are
        null when the underlying account is unavailable or has been deleted;
        `deleted` is true only for deleted accounts.

      - `class BetaSpendLimitScopedAPIKeyActor`

        A scoped Admin API key acting on behalf of the organization.

    - `amount: Optional[str]`

      Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

    - `period: BetaSpendLimitPeriod`

      Period this row's effective limit and spend are reported for.

    - `period_to_date_spend: str`

      The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

    - `scope: Scope`

      - `class BetaSpendLimitUserScope`

        Scope selecting a single member of the organization.

        - `type: Literal["user"]`

          Scope type. Always `user` for this scope.

          default: user

        - `user_id: str`

          Tagged ID of the member the spend limit applies to.

      - `class BetaSpendLimitSeatTierScope`

        - `type: Literal["seat_tier"]`

          default: seat_tier

        - `seat_tier: str`

      - `class BetaSpendLimitRBACGroupScope`

        - `type: Literal["rbac_group"]`

          default: rbac_group

        - `rbac_group_id: str`

      - `class BetaSpendLimitOrganizationServiceScope`

        - `type: Literal["organization_service"]`

          default: organization_service

        - `service: str`

      - `class BetaSpendLimitOrganizationScope`

        - `type: Literal["organization"]`

          default: organization

      - `class BetaSpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

        - `type: Literal["workspace"]`

          Scope type. Always `workspace` for this scope.

          default: workspace

        - `workspace_id: str`

          Tagged ID of the workspace the spend limit applies to.

      - `class BetaSpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

        - `type: Literal["usage_tier"]`

          Scope type. Always `usage_tier` for this scope.

          default: usage_tier

    - `source: Source`

      - `class BetaSpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class BetaSpendLimitSeatTierScope`

      - `class BetaSpendLimitRBACGroupScope`

      - `class BetaSpendLimitOrganizationServiceScope`

      - `class BetaSpendLimitOrganizationScope`

      - `class BetaSpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class BetaSpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `spend_limit_id: str`

  - `status: BetaSpendLimitIncreaseRequestStatus`

    - `"approved"`

    - `"denied"`

    - `"pending"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_spend_limit_increase_request = (
    client.beta.organization.spend_limits.increase_requests.deny(
        spend_limit_increase_request_id="spend_limit_increase_request_id",
    )
)
print(beta_spend_limit_increase_request.id)
```

##### Response (200)

```json
{
  "id": "id",
  "actor": {
    "deleted": true,
    "email_address": "email_address",
    "name": "name",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "created_at": "2019-12-27T18:11:19.117Z",
  "period": "daily",
  "resolved_at": "2019-12-27T18:11:19.117Z",
  "resolved_by": {
    "deleted": true,
    "email_address": "email_address",
    "name": "name",
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "spend_summary": {
    "actor": {
      "deleted": true,
      "email_address": "email_address",
      "name": "name",
      "type": "user_actor",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "amount": "50000",
    "currency": "USD",
    "period": "daily",
    "period_to_date_spend": "12050.5",
    "scope": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "source": {
      "type": "user",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
    },
    "spend_limit_id": "spend_limit_id"
  },
  "status": "approved",
  "type": "spend_limit_increase_request"
}
```
