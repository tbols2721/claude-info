---
title: Artifacts
url: https://platform.claude.com/docs/en/api/python/beta/organization/analytics/artifacts
---

# Artifacts

## Get Artifact Activity

`beta.organization.analytics.artifacts.list(**kwargs) -> SyncPageCursor[BetaAnalyticsArtifactActivity]`

**GET** `/v1/organizations/analytics/artifacts`

Get artifact-creation activity for a given day, broken out by MIME type.

Returns the full (`artifact_type`, `is_shared`) cube for the organization;
`next_page` is null except for grouped queries, which paginate. The cube
can be broken out per product, per member, or per RBAC group via
`group_by[]`, and scoped via `filter[]`. Requires an API key with the
`read:analytics` scope.

### Parameters

- `date: Union[null, null]` (query parameter)

  UTC date in YYYY-MM-DD format. The day to get artifact activity for. Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

- `filter: Optional[Sequence[str]]` (query parameter)

  Filters as `dimension:value`, e.g. `filter[]=rbac_group_id:{id}`. Repeat the param for OR within a dimension and across dimensions for AND. Supported dimensions on this endpoint: `artifact_type`, `is_shared`, `product`, `rbac_group_id`, `user_id`. Value forms: `artifact_type` is a canonical artifact MIME type (e.g. `text/markdown`) or `other`; `is_shared` is `true` or `false`; `product` is `chat_cowork_unified`, `chat`, `claude_code`, or `cowork` (the surfaces that create artifacts); `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in responses and by the spend-limits API) or a bare group UUID, and matches users who held the group at any point during each covered UTC day (time-of-usage attribution); `user_id` takes a tagged user id (`user_...`), as emitted in responses. An unsupported dimension returns 400. At most 100 entries. `chat_cowork_unified` is accepted as a `product` value only where Chat and Cowork unified is available.

  maxItems: 100

- `group_by: Optional[List[BetaAnalyticsArtifactGroupBy]]` (query parameter)

  Dimensions to break results out by: `product`, `user_id` and/or `rbac_group_id`. The ungrouped artifact-type cube is finite and returned in full; grouped queries multiply the cube and paginate via `next_page`. `product` takes the values `chat_cowork_unified`, `chat`, `claude_code`, or `cowork` (the surfaces that create artifacts). `rbac_group_id` attributes a user to every group they held at any point during the requested UTC day, so grouped rows are not an exclusive partition. At most 100 entries.

  maxItems: 100

  - `"product"`

  - `"rbac_group_id"`

  - `"user_id"`

- `limit: Optional[int]` (query parameter)

  Maximum rows to return (1-1000, default 100). The ungrouped artifact-type cube is finite and returned in full; `limit` is the page size only when `group_by[]` multiplies the cube.

  minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field. Only valid with `group_by[]` — the ungrouped cube is never paginated.

### Returns

- `class BetaAnalyticsArtifactActivity`

  Artifact-creation activity for one (`artifact_type`, `is_shared`) bucket
  on a given day.

  Artifacts form a small finite cube — the canonical MIME type (8 values incl.
  `other`) crossed with shared-vs-private — so the response is the full set of
  non-empty buckets, not a ranked/paginated list. Claude Code and Cowork
  artifacts report under `text/html` and are counted from 2026-08-17
  onward; earlier days contain claude.ai chat artifacts only. With
  `group_by[]=product` / `user_id` / `rbac_group_id` each row is further
  split by the flat group keys and counts are scoped to that cut.

  - `artifact_type: str`

    Canonical artifact MIME type (e.g. `text/markdown`, `application/vnd.ant.react`, `image/svg+xml`), or `other`. Claude Code and Cowork artifacts report as `text/html`.

  - `artifacts_created_count: int`

    Number of artifacts created in this bucket on the requested day

  - `distinct_user_count: int`

    Number of distinct users who created artifacts in this bucket on the requested day

  - `is_shared: bool`

    Whether the artifacts in this bucket have ever been shared (a Claude Code / Cowork artifact is shared once anyone beyond its creator may open it: named members, the whole organization, or anyone with the link).

  - `published_artifacts_created_count: int`

    Number of those artifacts that have been published (for Claude Code / Cowork artifacts: open to anyone with the link); never exceeds `artifacts_created_count`

  - `product: Optional[str]`

    Product that produced this row's activity: one of `chat`, `claude_code`, `cowork`, `office_agent`, or `chat_cowork_unified` (Chat and Cowork unified). These are the canonical Cost & Usage product names; an `office_agent` row's per-surface breakdown is in its `office_metrics`. On `/plugins` only `cowork`, `claude_code` and `chat_cowork_unified` occur (the only surfaces with plugin attribution); on `/artifacts` only `chat`, `claude_code`, `cowork` and `chat_cowork_unified` occur (the surfaces that create artifacts); `/apps/chat/projects` does not support the product dimension (a `product` entry in `group_by[]` or `filter[]` there is rejected). Present only when the request grouped by `product`.

  - `rbac_group_id: Optional[str]`

    Tagged RBAC group identifier (`rbac_group_...`), matching the spend-limits API spelling. Present only when the request grouped by `rbac_group_id`.

  - `rbac_group_name: Optional[str]`

    Resolved RBAC group display name, alongside `rbac_group_id` when name resolution is available. Null if the group has been deleted or its name could not be resolved; `rbac_group_id` remains the stable key.

  - `user_id: Optional[str]`

    Tagged user identifier (e.g. `user_...`). Present only when the request grouped by `user_id`.

### Example

```python
import os
from datetime import date
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.analytics.artifacts.list(
    date=date.fromisoformat("2019-12-27"),
)
page = page.data[0]
print(page.rbac_group_id)
```

#### Response (200)

```json
{
  "data": [
    {
      "artifact_type": "artifact_type",
      "artifacts_created_count": 0,
      "distinct_user_count": 0,
      "is_shared": true,
      "published_artifacts_created_count": 0,
      "product": "product",
      "rbac_group_id": "rbac_group_id",
      "rbac_group_name": "rbac_group_name",
      "user_id": "user_id"
    }
  ],
  "next_page": "next_page"
}
```
