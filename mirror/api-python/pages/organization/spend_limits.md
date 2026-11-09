---
title: Spend Limits
url: https://platform.claude.com/docs/en/api/python/organization/spend_limits
---

# Spend Limits

## Domain types

### Spend Limit

- `class SpendLimit`

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

  - `period: SpendLimitPeriod`

    Length of the window the limit resets over. `amount` caps spend within each period.

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `scope: Scope`

    What the limit applies to. A tagged union on `type`; each variant carries the identifier for its scope.

    - `class SpendLimitUserScope`

      Scope selecting a single member of the organization.

      - `type: Literal["user"]`

        Scope type. Always `user` for this scope.

        default: user

      - `user_id: str`

        Tagged ID of the member the spend limit applies to.

    - `class SpendLimitSeatTierScope`

      - `type: Literal["seat_tier"]`

        default: seat_tier

      - `seat_tier: str`

    - `class SpendLimitRBACGroupScope`

      - `type: Literal["rbac_group"]`

        default: rbac_group

      - `rbac_group_id: str`

    - `class SpendLimitOrganizationServiceScope`

      - `type: Literal["organization_service"]`

        default: organization_service

      - `service: str`

    - `class SpendLimitOrganizationScope`

      - `type: Literal["organization"]`

        default: organization

    - `class SpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

      - `type: Literal["workspace"]`

        Scope type. Always `workspace` for this scope.

        default: workspace

      - `workspace_id: str`

        Tagged ID of the workspace the spend limit applies to.

    - `class SpendLimitUsageTierScope`

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

### Spend Limit Organization Scope

- `class SpendLimitOrganizationScope`

  - `type: Literal["organization"]`

    default: organization

### Spend Limit Organization Service Scope

- `class SpendLimitOrganizationServiceScope`

  - `type: Literal["organization_service"]`

    default: organization_service

  - `service: str`

### Spend Limit Period

- `type SpendLimitPeriod = Literal["daily", "monthly", "weekly"]`

  - `"daily"`

  - `"monthly"`

  - `"weekly"`

### Spend Limit RBAC Group Scope

- `class SpendLimitRBACGroupScope`

  - `type: Literal["rbac_group"]`

    default: rbac_group

  - `rbac_group_id: str`

### Spend Limit Scoped API Key Actor

- `class SpendLimitScopedAPIKeyActor`

  A scoped Admin API key acting on behalf of the organization.

  - `type: Literal["scoped_api_key_actor"]`

    default: scoped_api_key_actor

  - `scoped_api_key_id: str`

### Spend Limit Seat Tier Scope

- `class SpendLimitSeatTierScope`

  - `type: Literal["seat_tier"]`

    default: seat_tier

  - `seat_tier: str`

### Spend Limit Usage Tier Scope

- `class SpendLimitUsageTierScope`

  Scope of the monthly spend cap Anthropic sets for a Claude Console
  organization from its usage tier, or a higher cap Anthropic granted the
  organization. Read-only; its `created_at` and `updated_at` are the
  organization's creation time, so `amount` can change while `updated_at` stays
  the same.

  - `type: Literal["usage_tier"]`

    Scope type. Always `usage_tier` for this scope.

    default: usage_tier

### Spend Limit User Actor

- `class SpendLimitUserActor`

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

### Spend Limit User Scope

- `class SpendLimitUserScope`

  Scope selecting a single member of the organization.

  - `type: Literal["user"]`

    Scope type. Always `user` for this scope.

    default: user

  - `user_id: str`

    Tagged ID of the member the spend limit applies to.

### Spend Limit Workspace Scope

- `class SpendLimitWorkspaceScope`

  Scope selecting one workspace of a Claude Console organization.

  - `type: Literal["workspace"]`

    Scope type. Always `workspace` for this scope.

    default: workspace

  - `workspace_id: str`

    Tagged ID of the workspace the spend limit applies to.

### Spend Summary

- `class SpendSummary`

  Per-member effective-limit report row (`GET /spend_limits/effective`).

  - `actor: Actor`

    - `class SpendLimitUserActor`

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

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `amount: Optional[str]`

    Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

  - `currency: str`

    ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

  - `period: SpendLimitPeriod`

    Period this row's effective limit and spend are reported for.

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `period_to_date_spend: str`

    The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

  - `scope: Scope`

    - `class SpendLimitUserScope`

      Scope selecting a single member of the organization.

      - `type: Literal["user"]`

        Scope type. Always `user` for this scope.

        default: user

      - `user_id: str`

        Tagged ID of the member the spend limit applies to.

    - `class SpendLimitSeatTierScope`

      - `type: Literal["seat_tier"]`

        default: seat_tier

      - `seat_tier: str`

    - `class SpendLimitRBACGroupScope`

      - `type: Literal["rbac_group"]`

        default: rbac_group

      - `rbac_group_id: str`

    - `class SpendLimitOrganizationServiceScope`

      - `type: Literal["organization_service"]`

        default: organization_service

      - `service: str`

    - `class SpendLimitOrganizationScope`

      - `type: Literal["organization"]`

        default: organization

    - `class SpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

      - `type: Literal["workspace"]`

        Scope type. Always `workspace` for this scope.

        default: workspace

      - `workspace_id: str`

        Tagged ID of the workspace the spend limit applies to.

    - `class SpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

      - `type: Literal["usage_tier"]`

        Scope type. Always `usage_tier` for this scope.

        default: usage_tier

  - `source: Source`

    - `class SpendLimitUserScope`

      Scope selecting a single member of the organization.

    - `class SpendLimitSeatTierScope`

    - `class SpendLimitRBACGroupScope`

    - `class SpendLimitOrganizationServiceScope`

    - `class SpendLimitOrganizationScope`

    - `class SpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

    - `class SpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

  - `spend_limit_id: str`

## Spend Limits › Effective

### List Effective Spend Limits

`organization.spend_limits.effective.list(**kwargs) -> SyncPageCursor[SpendSummary]`

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

- `period: Optional[List[SpendLimitPeriod]]` (query parameter)

  Restrict the report to these limit periods. Omit to return one row per period each member resolves a spend limit for.

  maxItems: 3

  - `"daily"`

  - `"monthly"`

  - `"weekly"`

- `user_ids: Optional[Sequence[str]]` (query parameter)

  Restrict the report to these members, by tagged user ID (`user_...`). At most 100 entries.

  maxItems: 100

#### Returns

- `class SpendSummary`

  Per-member effective-limit report row (`GET /spend_limits/effective`).

  - `actor: Actor`

    - `class SpendLimitUserActor`

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

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `amount: Optional[str]`

    Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

  - `currency: str`

    ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

  - `period: SpendLimitPeriod`

    Period this row's effective limit and spend are reported for.

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `period_to_date_spend: str`

    The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

  - `scope: Scope`

    - `class SpendLimitUserScope`

      Scope selecting a single member of the organization.

      - `type: Literal["user"]`

        Scope type. Always `user` for this scope.

        default: user

      - `user_id: str`

        Tagged ID of the member the spend limit applies to.

    - `class SpendLimitSeatTierScope`

      - `type: Literal["seat_tier"]`

        default: seat_tier

      - `seat_tier: str`

    - `class SpendLimitRBACGroupScope`

      - `type: Literal["rbac_group"]`

        default: rbac_group

      - `rbac_group_id: str`

    - `class SpendLimitOrganizationServiceScope`

      - `type: Literal["organization_service"]`

        default: organization_service

      - `service: str`

    - `class SpendLimitOrganizationScope`

      - `type: Literal["organization"]`

        default: organization

    - `class SpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

      - `type: Literal["workspace"]`

        Scope type. Always `workspace` for this scope.

        default: workspace

      - `workspace_id: str`

        Tagged ID of the workspace the spend limit applies to.

    - `class SpendLimitUsageTierScope`

      Scope of the monthly spend cap Anthropic sets for a Claude Console
      organization from its usage tier, or a higher cap Anthropic granted the
      organization. Read-only; its `created_at` and `updated_at` are the
      organization's creation time, so `amount` can change while `updated_at` stays
      the same.

      - `type: Literal["usage_tier"]`

        Scope type. Always `usage_tier` for this scope.

        default: usage_tier

  - `source: Source`

    - `class SpendLimitUserScope`

      Scope selecting a single member of the organization.

    - `class SpendLimitSeatTierScope`

    - `class SpendLimitRBACGroupScope`

    - `class SpendLimitOrganizationServiceScope`

    - `class SpendLimitOrganizationScope`

    - `class SpendLimitWorkspaceScope`

      Scope selecting one workspace of a Claude Console organization.

    - `class SpendLimitUsageTierScope`

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
page = client.organization.spend_limits.effective.list()
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

`organization.spend_limits.increase_requests.list(**kwargs) -> SyncPageCursor[SpendLimitIncreaseRequest]`

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

- `status: Optional[List[SpendLimitIncreaseRequestStatus]]` (query parameter)

  Filter by status. Omit to return all.

  - `"approved"`

  - `"denied"`

  - `"pending"`

#### Returns

- `class SpendLimitIncreaseRequest`

  - `type: Literal["spend_limit_increase_request"]`

    default: spend_limit_increase_request

  - `id: str`

  - `actor: SpendLimitIncreaseRequestActor`

    Who submitted the increase request.

    - `class SpendLimitUserActor`

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

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `created_at: datetime`

    format: date-time

  - `period: SpendLimitPeriod`

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `resolved_at: Optional[datetime]`

    format: date-time

  - `resolved_by: Optional[SpendLimitIncreaseRequestResolvedBy]`

    Who approved or denied the increase request.

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

  - `spend_summary: Optional[SpendSummary]`

    Per-member effective-limit report row (`GET /spend_limits/effective`).

    - `actor: Actor`

      - `class SpendLimitUserActor`

        A user within the organization. `name` and `email_address` are
        null when the underlying account is unavailable or has been deleted;
        `deleted` is true only for deleted accounts.

      - `class SpendLimitScopedAPIKeyActor`

        A scoped Admin API key acting on behalf of the organization.

    - `amount: Optional[str]`

      Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

    - `period: SpendLimitPeriod`

      Period this row's effective limit and spend are reported for.

    - `period_to_date_spend: str`

      The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

    - `scope: Scope`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

        - `type: Literal["user"]`

          Scope type. Always `user` for this scope.

          default: user

        - `user_id: str`

          Tagged ID of the member the spend limit applies to.

      - `class SpendLimitSeatTierScope`

        - `type: Literal["seat_tier"]`

          default: seat_tier

        - `seat_tier: str`

      - `class SpendLimitRBACGroupScope`

        - `type: Literal["rbac_group"]`

          default: rbac_group

        - `rbac_group_id: str`

      - `class SpendLimitOrganizationServiceScope`

        - `type: Literal["organization_service"]`

          default: organization_service

        - `service: str`

      - `class SpendLimitOrganizationScope`

        - `type: Literal["organization"]`

          default: organization

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

        - `type: Literal["workspace"]`

          Scope type. Always `workspace` for this scope.

          default: workspace

        - `workspace_id: str`

          Tagged ID of the workspace the spend limit applies to.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

        - `type: Literal["usage_tier"]`

          Scope type. Always `usage_tier` for this scope.

          default: usage_tier

    - `source: Source`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class SpendLimitSeatTierScope`

      - `class SpendLimitRBACGroupScope`

      - `class SpendLimitOrganizationServiceScope`

      - `class SpendLimitOrganizationScope`

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `spend_limit_id: str`

  - `status: SpendLimitIncreaseRequestStatus`

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
page = client.organization.spend_limits.increase_requests.list()
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

`organization.spend_limits.increase_requests.retrieve(spend_limit_increase_request_id) -> SpendLimitIncreaseRequest`

**GET** `/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}`

Retrieve a spend limit increase request.

While `pending`, the response includes a live `spend_summary` for the
requester at the request's period.

#### Parameters

- `spend_limit_increase_request_id: str` (path parameter)

  ID of the spend limit increase request.

#### Returns

- `class SpendLimitIncreaseRequest`

  - `type: Literal["spend_limit_increase_request"]`

    default: spend_limit_increase_request

  - `id: str`

  - `actor: SpendLimitIncreaseRequestActor`

    Who submitted the increase request.

    - `class SpendLimitUserActor`

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

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `created_at: datetime`

    format: date-time

  - `period: SpendLimitPeriod`

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `resolved_at: Optional[datetime]`

    format: date-time

  - `resolved_by: Optional[SpendLimitIncreaseRequestResolvedBy]`

    Who approved or denied the increase request.

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

  - `spend_summary: Optional[SpendSummary]`

    Per-member effective-limit report row (`GET /spend_limits/effective`).

    - `actor: Actor`

      - `class SpendLimitUserActor`

        A user within the organization. `name` and `email_address` are
        null when the underlying account is unavailable or has been deleted;
        `deleted` is true only for deleted accounts.

      - `class SpendLimitScopedAPIKeyActor`

        A scoped Admin API key acting on behalf of the organization.

    - `amount: Optional[str]`

      Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

    - `period: SpendLimitPeriod`

      Period this row's effective limit and spend are reported for.

    - `period_to_date_spend: str`

      The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

    - `scope: Scope`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

        - `type: Literal["user"]`

          Scope type. Always `user` for this scope.

          default: user

        - `user_id: str`

          Tagged ID of the member the spend limit applies to.

      - `class SpendLimitSeatTierScope`

        - `type: Literal["seat_tier"]`

          default: seat_tier

        - `seat_tier: str`

      - `class SpendLimitRBACGroupScope`

        - `type: Literal["rbac_group"]`

          default: rbac_group

        - `rbac_group_id: str`

      - `class SpendLimitOrganizationServiceScope`

        - `type: Literal["organization_service"]`

          default: organization_service

        - `service: str`

      - `class SpendLimitOrganizationScope`

        - `type: Literal["organization"]`

          default: organization

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

        - `type: Literal["workspace"]`

          Scope type. Always `workspace` for this scope.

          default: workspace

        - `workspace_id: str`

          Tagged ID of the workspace the spend limit applies to.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

        - `type: Literal["usage_tier"]`

          Scope type. Always `usage_tier` for this scope.

          default: usage_tier

    - `source: Source`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class SpendLimitSeatTierScope`

      - `class SpendLimitRBACGroupScope`

      - `class SpendLimitOrganizationServiceScope`

      - `class SpendLimitOrganizationScope`

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `spend_limit_id: str`

  - `status: SpendLimitIncreaseRequestStatus`

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
spend_limit_increase_request = (
    client.organization.spend_limits.increase_requests.retrieve(
        "spend_limit_increase_request_id",
    )
)
print(spend_limit_increase_request.id)
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

`organization.spend_limits.increase_requests.approve(spend_limit_increase_request_id, **kwargs) -> IncreaseRequestApproveResponse`

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

- `period: Optional[SpendLimitPeriod]`

  - `"daily"`

  - `"monthly"`

  - `"weekly"`

- `suppress_notification: Optional[bool]`

#### Returns

- `class IncreaseRequestApproveResponse`

  - `type: Literal["spend_limit_increase_request"]`

    default: spend_limit_increase_request

  - `id: str`

  - `actor: SpendLimitIncreaseRequestActor`

    Who submitted the increase request.

    - `class SpendLimitUserActor`

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

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `created_at: datetime`

    format: date-time

  - `period: SpendLimitPeriod`

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `resolved_at: Optional[datetime]`

    format: date-time

  - `resolved_by: Optional[SpendLimitIncreaseRequestResolvedBy]`

    Who approved or denied the increase request.

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

  - `spend_limit: Optional[SpendLimit]`

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

    - `period: SpendLimitPeriod`

      Length of the window the limit resets over. `amount` caps spend within each period.

    - `scope: Scope`

      What the limit applies to. A tagged union on `type`; each variant carries the identifier for its scope.

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

        - `type: Literal["user"]`

          Scope type. Always `user` for this scope.

          default: user

        - `user_id: str`

          Tagged ID of the member the spend limit applies to.

      - `class SpendLimitSeatTierScope`

        - `type: Literal["seat_tier"]`

          default: seat_tier

        - `seat_tier: str`

      - `class SpendLimitRBACGroupScope`

        - `type: Literal["rbac_group"]`

          default: rbac_group

        - `rbac_group_id: str`

      - `class SpendLimitOrganizationServiceScope`

        - `type: Literal["organization_service"]`

          default: organization_service

        - `service: str`

      - `class SpendLimitOrganizationScope`

        - `type: Literal["organization"]`

          default: organization

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

        - `type: Literal["workspace"]`

          Scope type. Always `workspace` for this scope.

          default: workspace

        - `workspace_id: str`

          Tagged ID of the workspace the spend limit applies to.

      - `class SpendLimitUsageTierScope`

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

  - `spend_summary: Optional[SpendSummary]`

    Per-member effective-limit report row (`GET /spend_limits/effective`).

    - `actor: Actor`

      - `class SpendLimitUserActor`

        A user within the organization. `name` and `email_address` are
        null when the underlying account is unavailable or has been deleted;
        `deleted` is true only for deleted accounts.

      - `class SpendLimitScopedAPIKeyActor`

        A scoped Admin API key acting on behalf of the organization.

    - `amount: Optional[str]`

      Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

    - `period: SpendLimitPeriod`

      Period this row's effective limit and spend are reported for.

    - `period_to_date_spend: str`

      The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

    - `scope: Scope`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class SpendLimitSeatTierScope`

      - `class SpendLimitRBACGroupScope`

      - `class SpendLimitOrganizationServiceScope`

      - `class SpendLimitOrganizationScope`

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `source: Source`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class SpendLimitSeatTierScope`

      - `class SpendLimitRBACGroupScope`

      - `class SpendLimitOrganizationServiceScope`

      - `class SpendLimitOrganizationScope`

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `spend_limit_id: str`

  - `status: SpendLimitIncreaseRequestStatus`

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
response = client.organization.spend_limits.increase_requests.approve(
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

`organization.spend_limits.increase_requests.deny(spend_limit_increase_request_id, **kwargs) -> SpendLimitIncreaseRequest`

**POST** `/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}/deny`

Deny a pending spend limit increase request.

Idempotent on `denied`; denying an already-`approved` request returns
400. Anthropic emails the requester unless `suppress_notification` is set.

#### Parameters

- `spend_limit_increase_request_id: str` (path parameter)

  ID of the spend limit increase request.

- `suppress_notification: Optional[bool]`

#### Returns

- `class SpendLimitIncreaseRequest`

  - `type: Literal["spend_limit_increase_request"]`

    default: spend_limit_increase_request

  - `id: str`

  - `actor: SpendLimitIncreaseRequestActor`

    Who submitted the increase request.

    - `class SpendLimitUserActor`

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

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

      - `type: Literal["scoped_api_key_actor"]`

        default: scoped_api_key_actor

      - `scoped_api_key_id: str`

  - `created_at: datetime`

    format: date-time

  - `period: SpendLimitPeriod`

    - `"daily"`

    - `"monthly"`

    - `"weekly"`

  - `resolved_at: Optional[datetime]`

    format: date-time

  - `resolved_by: Optional[SpendLimitIncreaseRequestResolvedBy]`

    Who approved or denied the increase request.

    - `class SpendLimitUserActor`

      A user within the organization. `name` and `email_address` are
      null when the underlying account is unavailable or has been deleted;
      `deleted` is true only for deleted accounts.

    - `class SpendLimitScopedAPIKeyActor`

      A scoped Admin API key acting on behalf of the organization.

  - `spend_summary: Optional[SpendSummary]`

    Per-member effective-limit report row (`GET /spend_limits/effective`).

    - `actor: Actor`

      - `class SpendLimitUserActor`

        A user within the organization. `name` and `email_address` are
        null when the underlying account is unavailable or has been deleted;
        `deleted` is true only for deleted accounts.

      - `class SpendLimitScopedAPIKeyActor`

        A scoped Admin API key acting on behalf of the organization.

    - `amount: Optional[str]`

      Effective limit amount as a non-negative integer decimal string in the minor unit of `currency` (cents for USD). `null` means no limit applies for this row's `period` — each period resolves independently, so another period may still cap this member.

    - `currency: str`

      ISO 4217 code of the organization's billing currency; the unit for `amount` and `period_to_date_spend`.

    - `period: SpendLimitPeriod`

      Period this row's effective limit and spend are reported for.

    - `period_to_date_spend: str`

      The member's spend so far in the current period, as a non-negative decimal string in the minor unit of `currency` (cents for USD). May carry fractional minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not rounded to whole cents. Reads as `"0"` when the spend reading is temporarily unavailable.

    - `scope: Scope`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

        - `type: Literal["user"]`

          Scope type. Always `user` for this scope.

          default: user

        - `user_id: str`

          Tagged ID of the member the spend limit applies to.

      - `class SpendLimitSeatTierScope`

        - `type: Literal["seat_tier"]`

          default: seat_tier

        - `seat_tier: str`

      - `class SpendLimitRBACGroupScope`

        - `type: Literal["rbac_group"]`

          default: rbac_group

        - `rbac_group_id: str`

      - `class SpendLimitOrganizationServiceScope`

        - `type: Literal["organization_service"]`

          default: organization_service

        - `service: str`

      - `class SpendLimitOrganizationScope`

        - `type: Literal["organization"]`

          default: organization

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

        - `type: Literal["workspace"]`

          Scope type. Always `workspace` for this scope.

          default: workspace

        - `workspace_id: str`

          Tagged ID of the workspace the spend limit applies to.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

        - `type: Literal["usage_tier"]`

          Scope type. Always `usage_tier` for this scope.

          default: usage_tier

    - `source: Source`

      - `class SpendLimitUserScope`

        Scope selecting a single member of the organization.

      - `class SpendLimitSeatTierScope`

      - `class SpendLimitRBACGroupScope`

      - `class SpendLimitOrganizationServiceScope`

      - `class SpendLimitOrganizationScope`

      - `class SpendLimitWorkspaceScope`

        Scope selecting one workspace of a Claude Console organization.

      - `class SpendLimitUsageTierScope`

        Scope of the monthly spend cap Anthropic sets for a Claude Console
        organization from its usage tier, or a higher cap Anthropic granted the
        organization. Read-only; its `created_at` and `updated_at` are the
        organization's creation time, so `amount` can change while `updated_at` stays
        the same.

    - `spend_limit_id: str`

  - `status: SpendLimitIncreaseRequestStatus`

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
spend_limit_increase_request = client.organization.spend_limits.increase_requests.deny(
    spend_limit_increase_request_id="spend_limit_increase_request_id",
)
print(spend_limit_increase_request.id)
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
