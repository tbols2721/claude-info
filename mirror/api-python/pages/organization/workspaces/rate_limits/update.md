---
title: Set Workspace Rate Limits
url: https://platform.claude.com/docs/en/api/python/organization/workspaces/rate_limits/update
---

# Set Workspace Rate Limits

`organization.workspaces.rate_limits.update(rate_limit_id, **kwargs) -> WorkspaceRateLimit`

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

## Parameters

- `workspace_id: str` (path parameter)

  The ID of the workspace.

- `rate_limit_id: str` (path parameter)

  The `id` of the organization's rate-limit entry to set overrides for.

- `limits: Iterable[WorkspaceRateLimitUpdateValueParam]`

  Limits to set or clear. Unspecified limit types are unchanged.

  minItems: 1, maxItems: 16

  - `type: WorkspaceRateLimitType`

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

## Returns

- `class WorkspaceRateLimit`

  - `type: Literal["workspace_rate_limit"]`

    Object type. Always `workspace_rate_limit` for workspace rate-limit entries.

    default: workspace_rate_limit

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

  - `limits: List[WorkspaceRateLimitValue]`

    The workspace's limiter values for this group. By default only the limiter types with a workspace-level override are listed. With `include_inherited` set to `true`, the limiter types the workspace inherits from the organization are listed too, each marked by `source`.

    - `type: str`

      The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

    - `org_limit: Optional[int]`

      The organization-level value for the same limiter type, for reference. `null` when the organization has no limit configured for this limiter type.

    - `source: Source`

      Where `value` comes from. `organization` values are listed only when `include_inherited` is `true`, and then `value` equals `org_limit`.

      - `class WorkspaceRateLimitWorkspaceSource`

        - `type: Literal["workspace"]`

          Always `workspace`: a workspace-level override is stored.

          default: workspace

      - `class WorkspaceRateLimitOrganizationSource`

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

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace_rate_limit = client.organization.workspaces.rate_limits.update(
    rate_limit_id="rate_limit_id",
    workspace_id="workspace_id",
    limits=[
        {
            "type": "fast_itpmca",
            "value": 0,
        }
    ],
)
print(workspace_rate_limit.rate_limit_id)
```

### Response (200)

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
