---
title: Rate Limits
url: https://platform.claude.com/docs/en/api/python/beta/organization/workspaces/rate_limits
---

# Rate Limits

## List Workspace Rate Limits

`beta.organization.workspaces.rate_limits.list(workspace_id, **kwargs) -> SyncPageCursor[BetaWorkspaceRateLimit]`

**GET** `/v1/organizations/workspaces/{workspace_id}/rate_limits`

List a workspace's rate limits.

By default, returns only the groups and limiter types that have a
workspace-level override. With `include_inherited=true`, returns every
group with organization-level limits the workspace can see, listing for
each the values it inherits from the organization as well as its own
overrides. Each value's `source` says which it is.

When `limit` is omitted, every matching entry is returned in a single
page; when `limit` truncates the result, follow `next_page` to fetch
the remaining entries.

### Parameters

- `workspace_id: str` (path parameter)

  The ID of the workspace.

- `group_type: Optional[Literal["batch", "files", "model_group", 3 more]]` (query parameter)

  Filter by group type.

  - `"batch"`

  - `"files"`

  - `"model_group"`

  - `"skills"`

  - `"token_count"`

  - `"web_search"`

- `include_inherited: Optional[bool]` (query parameter)

  Also list the limiter values the workspace inherits from the organization, including groups with no workspace-level override.

  default: false

- `limit: Optional[int]` (query parameter)

  Maximum number of items to return per page. Ranges from `1` to `1000`.

  When omitted, every remaining entry is returned in a single page and `next_page` is `null`.

  minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

### Returns

- `class BetaWorkspaceRateLimit`

  - `type: Literal["workspace_rate_limit"]`

    Object type. Always `workspace_rate_limit` for workspace rate-limit entries.

    default: workspace_rate_limit

  - `group: Group`

    The rate-limit group this entry's limits apply to.

    - `class BetaOrganizationRateLimitModelGroup`

      - `type: Literal["model_group"]`

        Always `model_group`: a family of models.

        default: model_group

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `display_name: str`

        Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

    - `class BetaOrganizationRateLimitBatchGroup`

      - `type: Literal["batch"]`

        Always `batch`: the Message Batches API.

        default: batch

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class BetaOrganizationRateLimitTokenCountGroup`

      - `type: Literal["token_count"]`

        Always `token_count`: the Token Count API.

        default: token_count

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class BetaOrganizationRateLimitFilesGroup`

      - `type: Literal["files"]`

        Always `files`: the Files API.

        default: files

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class BetaOrganizationRateLimitSkillsGroup`

      - `type: Literal["skills"]`

        Always `skills`: the Skills API.

        default: skills

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class BetaOrganizationRateLimitWebSearchGroup`

      - `type: Literal["web_search"]`

        Always `web_search`: the Messages API web search tool.

        default: web_search

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

  - `limits: List[BetaWorkspaceRateLimitValue]`

    The workspace's limiter values for this group. By default only the limiter types with a workspace-level override are listed. With `include_inherited` set to `true`, the limiter types the workspace inherits from the organization are listed too, each marked by `source`.

    - `type: str`

      The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

    - `org_limit: Optional[int]`

      The organization-level value for the same limiter type, for reference. `null` when the organization has no limit configured for this limiter type.

    - `source: Source`

      Where `value` comes from. `organization` values are listed only when `include_inherited` is `true`, and then `value` equals `org_limit`.

      - `class BetaWorkspaceRateLimitWorkspaceSource`

        - `type: Literal["workspace"]`

          Always `workspace`: a workspace-level override is stored.

          default: workspace

      - `class BetaWorkspaceRateLimitOrganizationSource`

        - `type: Literal["organization"]`

          Always `organization`: no workspace-level override is stored, so the organization's value applies.

          default: organization

    - `value: int`

      The workspace's value for this limiter type: the workspace-level override when `source.type` is `workspace`, otherwise the organization's value.

  - `models: Optional[List[str]]`

    Model names this entry's limits apply to, including aliases. `null` when `group.type` is not `"model_group"`. The list covers the models this workspace has access to, so it can differ between workspaces.

  - `rate_limit_id: str`

    The `id` of the organization's RateLimit entry this entry applies to.

  - `workspace_id: str`

    ID of the Workspace this entry applies to.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.workspaces.rate_limits.list(
    workspace_id="workspace_id",
)
page = page.data[0]
print(page.rate_limit_id)
```

#### Response (200)

```json
{
  "data": [
    {
      "group": {
        "id": "id",
        "display_name": "display_name",
        "type": "model_group"
      },
      "limits": [
        {
          "org_limit": 0,
          "source": {
            "type": "workspace"
          },
          "type": "type",
          "value": 0
        }
      ],
      "models": [
        "string"
      ],
      "rate_limit_id": "rate_limit_id",
      "type": "workspace_rate_limit",
      "workspace_id": "workspace_id"
    }
  ],
  "next_page": "next_page"
}
```

## Set Workspace Rate Limits

`beta.organization.workspaces.rate_limits.update(rate_limit_id, **kwargs) -> BetaWorkspaceRateLimit`

**POST** `/v1/organizations/workspaces/{workspace_id}/rate_limits/{rate_limit_id}`

Set or clear rate-limit overrides for one rate-limit group in a workspace.

Only the limiter types named in `limits` change: an integer `value` sets
that type's override and `null` clears it. Types not named keep their
current value. A value above the organization's own limit is stored, but
the organization limit still applies, so the lower of the two is
enforced.

Returns the targeted group's entry with this request applied, in the shape
`GET /v1/organizations/workspaces/{workspace_id}/rate_limits` returns.
Changes take effect within about an hour.

### Parameters

- `workspace_id: str` (path parameter)

  The ID of the workspace.

- `rate_limit_id: str` (path parameter)

  The `id` of the organization's rate-limit entry to set overrides for.

- `limits: Iterable[BetaWorkspaceRateLimitUpdateValueParam]`

  Limits to set or clear. Unspecified limit types are unchanged.

  minItems: 1, maxItems: 16

  - `type: BetaWorkspaceRateLimitType`

    Rate limiter type.

    - `"fast_itpmca"`

    - `"fast_otpm"`

    - `"input_tokens_per_minute"`

    - `"input_tokens_per_minute_cache_aware"`

    - `"output_tokens_per_minute"`

    - `"requests_per_minute"`

    - `"tokens_per_day"`

    - `"tokens_per_minute"`

    - `"tool_uses_per_second"`

  - `value: Optional[int]`

    New limit value. Set to null to clear the workspace override and fall back to the organization limit.

    minimum: 0, maximum: 9007199254740991

### Returns

- `class BetaWorkspaceRateLimit`

  - `type: Literal["workspace_rate_limit"]`

    Object type. Always `workspace_rate_limit` for workspace rate-limit entries.

    default: workspace_rate_limit

  - `group: Group`

    The rate-limit group this entry's limits apply to.

    - `class BetaOrganizationRateLimitModelGroup`

      - `type: Literal["model_group"]`

        Always `model_group`: a family of models.

        default: model_group

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `display_name: str`

        Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

    - `class BetaOrganizationRateLimitBatchGroup`

      - `type: Literal["batch"]`

        Always `batch`: the Message Batches API.

        default: batch

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class BetaOrganizationRateLimitTokenCountGroup`

      - `type: Literal["token_count"]`

        Always `token_count`: the Token Count API.

        default: token_count

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class BetaOrganizationRateLimitFilesGroup`

      - `type: Literal["files"]`

        Always `files`: the Files API.

        default: files

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class BetaOrganizationRateLimitSkillsGroup`

      - `type: Literal["skills"]`

        Always `skills`: the Skills API.

        default: skills

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class BetaOrganizationRateLimitWebSearchGroup`

      - `type: Literal["web_search"]`

        Always `web_search`: the Messages API web search tool.

        default: web_search

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

  - `limits: List[BetaWorkspaceRateLimitValue]`

    The workspace's limiter values for this group. By default only the limiter types with a workspace-level override are listed. With `include_inherited` set to `true`, the limiter types the workspace inherits from the organization are listed too, each marked by `source`.

    - `type: str`

      The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

    - `org_limit: Optional[int]`

      The organization-level value for the same limiter type, for reference. `null` when the organization has no limit configured for this limiter type.

    - `source: Source`

      Where `value` comes from. `organization` values are listed only when `include_inherited` is `true`, and then `value` equals `org_limit`.

      - `class BetaWorkspaceRateLimitWorkspaceSource`

        - `type: Literal["workspace"]`

          Always `workspace`: a workspace-level override is stored.

          default: workspace

      - `class BetaWorkspaceRateLimitOrganizationSource`

        - `type: Literal["organization"]`

          Always `organization`: no workspace-level override is stored, so the organization's value applies.

          default: organization

    - `value: int`

      The workspace's value for this limiter type: the workspace-level override when `source.type` is `workspace`, otherwise the organization's value.

  - `models: Optional[List[str]]`

    Model names this entry's limits apply to, including aliases. `null` when `group.type` is not `"model_group"`. The list covers the models this workspace has access to, so it can differ between workspaces.

  - `rate_limit_id: str`

    The `id` of the organization's RateLimit entry this entry applies to.

  - `workspace_id: str`

    ID of the Workspace this entry applies to.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_workspace_rate_limit = client.beta.organization.workspaces.rate_limits.update(
    rate_limit_id="rate_limit_id",
    workspace_id="workspace_id",
    limits=[
        {
            "type": "fast_itpmca",
            "value": 0,
        }
    ],
)
print(beta_workspace_rate_limit.rate_limit_id)
```

#### Response (200)

```json
{
  "group": {
    "id": "id",
    "display_name": "display_name",
    "type": "model_group"
  },
  "limits": [
    {
      "org_limit": 0,
      "source": {
        "type": "workspace"
      },
      "type": "type",
      "value": 0
    }
  ],
  "models": [
    "string"
  ],
  "rate_limit_id": "rate_limit_id",
  "type": "workspace_rate_limit",
  "workspace_id": "workspace_id"
}
```

## Domain types

### Beta Workspace Rate Limit

- `class BetaWorkspaceRateLimit`

  - `type: Literal["workspace_rate_limit"]`

    Object type. Always `workspace_rate_limit` for workspace rate-limit entries.

    default: workspace_rate_limit

  - `group: Group`

    The rate-limit group this entry's limits apply to.

    - `class BetaOrganizationRateLimitModelGroup`

      - `type: Literal["model_group"]`

        Always `model_group`: a family of models.

        default: model_group

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `display_name: str`

        Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

    - `class BetaOrganizationRateLimitBatchGroup`

      - `type: Literal["batch"]`

        Always `batch`: the Message Batches API.

        default: batch

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class BetaOrganizationRateLimitTokenCountGroup`

      - `type: Literal["token_count"]`

        Always `token_count`: the Token Count API.

        default: token_count

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class BetaOrganizationRateLimitFilesGroup`

      - `type: Literal["files"]`

        Always `files`: the Files API.

        default: files

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class BetaOrganizationRateLimitSkillsGroup`

      - `type: Literal["skills"]`

        Always `skills`: the Skills API.

        default: skills

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class BetaOrganizationRateLimitWebSearchGroup`

      - `type: Literal["web_search"]`

        Always `web_search`: the Messages API web search tool.

        default: web_search

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

  - `limits: List[BetaWorkspaceRateLimitValue]`

    The workspace's limiter values for this group. By default only the limiter types with a workspace-level override are listed. With `include_inherited` set to `true`, the limiter types the workspace inherits from the organization are listed too, each marked by `source`.

    - `type: str`

      The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

    - `org_limit: Optional[int]`

      The organization-level value for the same limiter type, for reference. `null` when the organization has no limit configured for this limiter type.

    - `source: Source`

      Where `value` comes from. `organization` values are listed only when `include_inherited` is `true`, and then `value` equals `org_limit`.

      - `class BetaWorkspaceRateLimitWorkspaceSource`

        - `type: Literal["workspace"]`

          Always `workspace`: a workspace-level override is stored.

          default: workspace

      - `class BetaWorkspaceRateLimitOrganizationSource`

        - `type: Literal["organization"]`

          Always `organization`: no workspace-level override is stored, so the organization's value applies.

          default: organization

    - `value: int`

      The workspace's value for this limiter type: the workspace-level override when `source.type` is `workspace`, otherwise the organization's value.

  - `models: Optional[List[str]]`

    Model names this entry's limits apply to, including aliases. `null` when `group.type` is not `"model_group"`. The list covers the models this workspace has access to, so it can differ between workspaces.

  - `rate_limit_id: str`

    The `id` of the organization's RateLimit entry this entry applies to.

  - `workspace_id: str`

    ID of the Workspace this entry applies to.

### Beta Workspace Rate Limit Organization Source

- `class BetaWorkspaceRateLimitOrganizationSource`

  - `type: Literal["organization"]`

    Always `organization`: no workspace-level override is stored, so the organization's value applies.

    default: organization

### Beta Workspace Rate Limit Type

- `type BetaWorkspaceRateLimitType = Literal["fast_itpmca", "fast_otpm", "input_tokens_per_minute", 6 more]`

  Rate limiter type.

  - `"fast_itpmca"`

  - `"fast_otpm"`

  - `"input_tokens_per_minute"`

  - `"input_tokens_per_minute_cache_aware"`

  - `"output_tokens_per_minute"`

  - `"requests_per_minute"`

  - `"tokens_per_day"`

  - `"tokens_per_minute"`

  - `"tool_uses_per_second"`

### Beta Workspace Rate Limit Update Value

- `class BetaWorkspaceRateLimitUpdateValueParam`

  - `type: BetaWorkspaceRateLimitType`

    Rate limiter type.

    - `"fast_itpmca"`

    - `"fast_otpm"`

    - `"input_tokens_per_minute"`

    - `"input_tokens_per_minute_cache_aware"`

    - `"output_tokens_per_minute"`

    - `"requests_per_minute"`

    - `"tokens_per_day"`

    - `"tokens_per_minute"`

    - `"tool_uses_per_second"`

  - `value: Optional[int]`

    New limit value. Set to null to clear the workspace override and fall back to the organization limit.

    minimum: 0, maximum: 9007199254740991

### Beta Workspace Rate Limit Value

- `class BetaWorkspaceRateLimitValue`

  - `type: str`

    The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

  - `org_limit: Optional[int]`

    The organization-level value for the same limiter type, for reference. `null` when the organization has no limit configured for this limiter type.

  - `source: Source`

    Where `value` comes from. `organization` values are listed only when `include_inherited` is `true`, and then `value` equals `org_limit`.

    - `class BetaWorkspaceRateLimitWorkspaceSource`

      - `type: Literal["workspace"]`

        Always `workspace`: a workspace-level override is stored.

        default: workspace

    - `class BetaWorkspaceRateLimitOrganizationSource`

      - `type: Literal["organization"]`

        Always `organization`: no workspace-level override is stored, so the organization's value applies.

        default: organization

  - `value: int`

    The workspace's value for this limiter type: the workspace-level override when `source.type` is `workspace`, otherwise the organization's value.

### Beta Workspace Rate Limit Workspace Source

- `class BetaWorkspaceRateLimitWorkspaceSource`

  - `type: Literal["workspace"]`

    Always `workspace`: a workspace-level override is stored.

    default: workspace
