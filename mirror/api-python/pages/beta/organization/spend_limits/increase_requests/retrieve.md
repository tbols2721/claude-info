---
title: Get Spend Limit Increase Request
url: https://platform.claude.com/docs/en/api/python/beta/organization/spend_limits/increase_requests/retrieve
---

# Get Spend Limit Increase Request

`beta.organization.spend_limits.increase_requests.retrieve(spend_limit_increase_request_id) -> BetaSpendLimitIncreaseRequest`

**GET** `/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}`

Retrieve a spend limit increase request.

While `pending`, the response includes a live `spend_summary` for the
requester at the request's period.

## Parameters

- `spend_limit_increase_request_id: str` (path parameter)

  ID of the spend limit increase request.

## Returns

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

## Example

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

### Response (200)

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
