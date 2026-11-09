---
title: Get Spend Limit
url: https://platform.claude.com/docs/en/api/python/beta/organization/spend_limits/retrieve
---

# Get Spend Limit

`beta.organization.spend_limits.retrieve(spend_limit_id) -> BetaSpendLimit`

**GET** `/v1/organizations/spend_limits/{spend_limit_id}`

Retrieve a spend limit by ID.

## Parameters

- `spend_limit_id: str` (path parameter)

  ID of the Spend Limit.

## Returns

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

## Example

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

### Response (200)

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
