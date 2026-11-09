---
title: Rate Limits
url: https://platform.claude.com/docs/en/api/python/organization/rate_limits
---

# Rate Limits

## List Organization Rate Limits

`organization.rate_limits.list(**kwargs) -> SyncPageCursor[OrganizationRateLimit]`

**GET** `/v1/organizations/rate_limits`

List Messages API rate limits for your organization.

Each entry corresponds to one rate-limit group (either a model family
or an API-surface category such as the Message Batches API or the web
search tool) and contains the set of limiter values that apply to it.

When `limit` is omitted, every matching entry is returned in a single
page; when `limit` truncates the result, follow `next_page` to fetch
the remaining entries.

### Parameters

- `group_type: Optional[Literal["batch", "files", "model_group", 3 more]]` (query parameter)

  Filter by group type.

  - `"batch"`

  - `"files"`

  - `"model_group"`

  - `"skills"`

  - `"token_count"`

  - `"web_search"`

- `limit: Optional[int]` (query parameter)

  Maximum number of items to return per page. Ranges from `1` to `1000`.

  When omitted, every remaining entry is returned in a single page and `next_page` is `null`.

  minimum: 1, maximum: 1000

- `model: Optional[str]` (query parameter)

  Filter to the single entry containing this model. Accepts full model names and aliases. Returns 404 if the model is not found or has no rate limits for this organization.

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

### Returns

- `class OrganizationRateLimit`

  - `type: Literal["rate_limit"]`

    Object type. Always `rate_limit` for organization rate-limit entries.

    default: rate_limit

  - `id: str`

    Identifier of this rate-limit entry. It is stable within the organization and differs between organizations; the group's own identifier is `group.id`. Pass it as `rate_limit_id` to set a workspace's overrides for this group.

  - `group: Group`

    The rate-limit group this entry's limits apply to.

    - `class OrganizationRateLimitModelGroup`

      - `type: Literal["model_group"]`

        Always `model_group`: a family of models.

        default: model_group

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `display_name: str`

        Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

    - `class OrganizationRateLimitBatchGroup`

      - `type: Literal["batch"]`

        Always `batch`: the Message Batches API.

        default: batch

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitTokenCountGroup`

      - `type: Literal["token_count"]`

        Always `token_count`: the Token Count API.

        default: token_count

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitFilesGroup`

      - `type: Literal["files"]`

        Always `files`: the Files API.

        default: files

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitSkillsGroup`

      - `type: Literal["skills"]`

        Always `skills`: the Skills API.

        default: skills

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitWebSearchGroup`

      - `type: Literal["web_search"]`

        Always `web_search`: the Messages API web search tool.

        default: web_search

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

  - `limits: List[OrganizationRateLimitValue]`

    The limiter values that apply to this group.

    - `type: str`

      The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

    - `value: int`

      The configured limit value for this limiter type.

  - `models: Optional[List[str]]`

    Model names this entry's limits apply to, including aliases. `null` when `group.type` is not `"model_group"`. The list covers the models your organization has access to, so it can differ between organizations.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.rate_limits.list()
page = page.data[0]
print(page.id)
```

#### Response (200)

```json
{
  "data": [
    {
      "id": "id",
      "group": {
        "id": "id",
        "display_name": "display_name",
        "type": "model_group"
      },
      "limits": [
        {
          "type": "type",
          "value": 0
        }
      ],
      "models": [
        "string"
      ],
      "type": "rate_limit"
    }
  ],
  "next_page": "next_page"
}
```

## Domain types

### Organization Rate Limit

- `class OrganizationRateLimit`

  - `type: Literal["rate_limit"]`

    Object type. Always `rate_limit` for organization rate-limit entries.

    default: rate_limit

  - `id: str`

    Identifier of this rate-limit entry. It is stable within the organization and differs between organizations; the group's own identifier is `group.id`. Pass it as `rate_limit_id` to set a workspace's overrides for this group.

  - `group: Group`

    The rate-limit group this entry's limits apply to.

    - `class OrganizationRateLimitModelGroup`

      - `type: Literal["model_group"]`

        Always `model_group`: a family of models.

        default: model_group

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `display_name: str`

        Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

    - `class OrganizationRateLimitBatchGroup`

      - `type: Literal["batch"]`

        Always `batch`: the Message Batches API.

        default: batch

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitTokenCountGroup`

      - `type: Literal["token_count"]`

        Always `token_count`: the Token Count API.

        default: token_count

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitFilesGroup`

      - `type: Literal["files"]`

        Always `files`: the Files API.

        default: files

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitSkillsGroup`

      - `type: Literal["skills"]`

        Always `skills`: the Skills API.

        default: skills

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitWebSearchGroup`

      - `type: Literal["web_search"]`

        Always `web_search`: the Messages API web search tool.

        default: web_search

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

  - `limits: List[OrganizationRateLimitValue]`

    The limiter values that apply to this group.

    - `type: str`

      The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

    - `value: int`

      The configured limit value for this limiter type.

  - `models: Optional[List[str]]`

    Model names this entry's limits apply to, including aliases. `null` when `group.type` is not `"model_group"`. The list covers the models your organization has access to, so it can differ between organizations.

### Organization Rate Limit Batch Group

- `class OrganizationRateLimitBatchGroup`

  - `type: Literal["batch"]`

    Always `batch`: the Message Batches API.

    default: batch

  - `id: str`

    Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

### Organization Rate Limit Files Group

- `class OrganizationRateLimitFilesGroup`

  - `type: Literal["files"]`

    Always `files`: the Files API.

    default: files

  - `id: str`

    Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

### Organization Rate Limit Model Group

- `class OrganizationRateLimitModelGroup`

  - `type: Literal["model_group"]`

    Always `model_group`: a family of models.

    default: model_group

  - `id: str`

    Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

  - `display_name: str`

    Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

### Organization Rate Limit Skills Group

- `class OrganizationRateLimitSkillsGroup`

  - `type: Literal["skills"]`

    Always `skills`: the Skills API.

    default: skills

  - `id: str`

    Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

### Organization Rate Limit Token Count Group

- `class OrganizationRateLimitTokenCountGroup`

  - `type: Literal["token_count"]`

    Always `token_count`: the Token Count API.

    default: token_count

  - `id: str`

    Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

### Organization Rate Limit Value

- `class OrganizationRateLimitValue`

  - `type: str`

    The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

  - `value: int`

    The configured limit value for this limiter type.

### Organization Rate Limit Web Search Group

- `class OrganizationRateLimitWebSearchGroup`

  - `type: Literal["web_search"]`

    Always `web_search`: the Messages API web search tool.

    default: web_search

  - `id: str`

    Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.
