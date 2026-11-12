---
title: Get Activity Summaries
url: https://platform.claude.com/docs/en/api/python/beta/organization/analytics/summaries/list
---

# Get Activity Summaries

`beta.organization.analytics.summaries.list(**kwargs) -> SyncPageCursor[BetaAnalyticsSingleDayActivitySummary]`

**GET** `/v1/organizations/analytics/summaries`

Get organization-wide activity summaries for a date range.

Returns one entry per day from `starting_date` (inclusive) to `ending_date`
(exclusive) in `data`, the same `data` / `next_page` envelope as the other
analytics list endpoints; the series is currently returned in full, so
`next_page` is always null.
Data is typically available with a 1-day lag and may be revised by a few
percent over the following days: when `ending_date` is omitted it
defaults to the most recent available day + 1, so the last entry covers
the most recent available day. The series can be scoped to an RBAC group
via `filter[]=rbac_group_id:{id}`. Available to organizations on a Claude
Enterprise plan. Requires an API key with the `read:analytics` scope.

## Parameters

- `starting_date: Union[null, null]` (query parameter)

  UTC date in YYYY-MM-DD format. Start of the date range (inclusive). Data is typically available with a 1-day lag (varies by query; the error for a too-recent date names the latest available day) and may be revised by a few percent over the following days. No earlier than 2026-01-01.

  format: date

- `ending_date: Optional[Union[null, null, null]]` (query parameter)

  UTC date in YYYY-MM-DD format. End of the date range (exclusive). Data is typically available with a 1-day lag, so this can be at most today — which is also the default when omitted, making the last entry cover the most recent available day. Data may be revised by a few percent over the following days. The range may span at most 366 days.

  format: date

- `filter: Optional[Sequence[str]]` (query parameter)

  Filters as `dimension:value`. Only `rbac_group_id` is supported (e.g. `filter[]=rbac_group_id:{id}`); repeat the param to OR across groups. Scopes the whole day series to members of the matching group(s), re-aggregated from member-level activity — org-wide seat/invite fields and the adoption rates derived from them are null on scoped rows. `rbac_group_id` accepts the tagged id (`rbac_group_...`, as emitted in responses and by the spend-limits API) or a bare group UUID, and matches users who held the group at any point during each UTC day (time-of-usage attribution). At most 100 entries.

  maxItems: 100

- `limit: Optional[int]` (query parameter)

  Number of results per page (1-1000, default 100). The day series (at most 366 entries) is currently returned in full in a single page, so `limit` does not yet shorten it.

  minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page` field. `next_page` is currently always null, so there is never a cursor to send.

## Returns

- `class BetaAnalyticsSingleDayActivitySummary`

  Per-day entry in the /summaries response.

  - `assigned_seat_count: Optional[int]`

    Number of seats currently assigned to members. Null when the response is scoped to an RBAC group — seat assignment is org-wide and has no per-group analogue.

  - `cowork_daily_active_user_count: int`

    Number of users with Cowork activity on the requested day

  - `cowork_monthly_active_user_count: int`

    Number of users with Cowork activity in the 30-day rolling window

  - `cowork_weekly_active_user_count: int`

    Number of users with Cowork activity in the 7-day rolling window

  - `daily_active_user_count: int`

    Number of users with token consumption on the requested day

  - `daily_adoption_rate: Optional[float]`

    Percentage of assigned seats with activity on the requested day (`DAU / assigned_seat_count * 100`). Null when the response is scoped to an RBAC group.

  - `ending_at: datetime`

    End of the aggregation period (exclusive), UTC midnight in RFC 3339 format (e.g. `2026-01-16T00:00:00Z`).

    format: date-time

  - `monthly_active_user_count: int`

    Number of users with token consumption in the 30-day rolling window

  - `monthly_adoption_rate: Optional[float]`

    Percentage of assigned seats with activity in the 30-day rolling window (`MAU / assigned_seat_count * 100`). Null when the response is scoped to an RBAC group.

  - `pending_invite_count: Optional[int]`

    Number of pending invitations to join the organization. Null when the response is scoped to an RBAC group.

  - `starting_at: datetime`

    Start of the aggregation period (inclusive), UTC midnight in RFC 3339 format (e.g. `2026-01-15T00:00:00Z`).

    format: date-time

  - `weekly_active_user_count: int`

    Number of users with token consumption in the 7-day rolling window

  - `weekly_adoption_rate: Optional[float]`

    Percentage of assigned seats with activity in the 7-day rolling window (`WAU / assigned_seat_count * 100`). Null when the response is scoped to an RBAC group.

  - `chat_cowork_unified_daily_active_user_count: Optional[int]`

    Number of users with activity in Chat and Cowork unified on the requested day. Omitted from the response where Chat and Cowork unified is not available.

  - `chat_cowork_unified_monthly_active_user_count: Optional[int]`

    Number of users with activity in Chat and Cowork unified in the 28-day rolling window (30 days when the request filters by `rbac_group_id`). Omitted from the response where Chat and Cowork unified is not available.

  - `chat_cowork_unified_weekly_active_user_count: Optional[int]`

    Number of users with activity in Chat and Cowork unified in the 7-day rolling window. Omitted from the response where Chat and Cowork unified is not available.

  - `chat_daily_active_user_count: Optional[int]`

    Number of users with claude.ai (chat) activity on the requested day. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `chat_monthly_active_user_count: Optional[int]`

    Number of users with claude.ai (chat) activity in the 30-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `chat_weekly_active_user_count: Optional[int]`

    Number of users with claude.ai (chat) activity in the 7-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_code_daily_active_user_count: Optional[int]`

    Number of users with Claude Code activity on the requested day. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_code_monthly_active_user_count: Optional[int]`

    Number of users with Claude Code activity in the 30-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_code_weekly_active_user_count: Optional[int]`

    Number of users with Claude Code activity in the 7-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_design_daily_active_user_count: Optional[int]`

    Number of users with Claude Design activity on the requested day. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_design_monthly_active_user_count: Optional[int]`

    Number of users with Claude Design activity in the 30-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_design_weekly_active_user_count: Optional[int]`

    Number of users with Claude Design activity in the 7-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `claude_tag_daily_active_user_count: Optional[int]`

    Number of Slack users active in Claude Tag on the requested day. Counts distinct Slack users, including users who have not linked a Claude account, so it can exceed `daily_active_user_count` and `assigned_seat_count`. Null on a day with no measured value, when Claude Tag data cannot be read for the request, and when the response is scoped to an RBAC group, because an unlinked user belongs to no group. Omitted from the response on deployments that do not offer Claude Tag reporting.

  - `claude_tag_monthly_active_user_count: Optional[int]`

    Number of Slack users active in Claude Tag in the 28-day rolling window. Counts distinct Slack users, including users who have not linked a Claude account, so it can exceed `daily_active_user_count` and `assigned_seat_count`. Null on a day with no measured value, when Claude Tag data cannot be read for the request, and when the response is scoped to an RBAC group, because an unlinked user belongs to no group. Omitted from the response on deployments that do not offer Claude Tag reporting.

  - `claude_tag_weekly_active_user_count: Optional[int]`

    Number of Slack users active in Claude Tag in the 7-day rolling window. Counts distinct Slack users, including users who have not linked a Claude account, so it can exceed `daily_active_user_count` and `assigned_seat_count`. Null on a day with no measured value, when Claude Tag data cannot be read for the request, and when the response is scoped to an RBAC group, because an unlinked user belongs to no group. Omitted from the response on deployments that do not offer Claude Tag reporting.

  - `office_agent_daily_active_user_count: Optional[int]`

    Number of users with Claude in Office activity on the requested day. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `office_agent_monthly_active_user_count: Optional[int]`

    Number of users with Claude in Office activity in the 30-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `office_agent_weekly_active_user_count: Optional[int]`

    Number of users with Claude in Office activity in the 7-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `science_daily_active_user_count: Optional[int]`

    Number of users with Claude Science activity on the requested day. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `science_entitled_user_count: Optional[int]`

    Number of users with a Claude Science seat entitlement (per-seat RBAC) at the time of the daily snapshot. The funnel top; independent of the org-level Claude Science toggle. Null when the response is scoped to an RBAC group — entitlement is org-wide and has no per-group analogue. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `science_monthly_active_user_count: Optional[int]`

    Number of users with Claude Science activity in the 30-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

  - `science_weekly_active_user_count: Optional[int]`

    Number of users with Claude Science activity in the 7-day rolling window. Omitted from the response while the per-product breakdown is not enabled for this organization.

## Example

```python
import os
from datetime import date
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.analytics.summaries.list(
    starting_date=date.fromisoformat("2019-12-27"),
)
page = page.data[0]
print(page.assigned_seat_count)
```

### Response (200)

```json
{
  "data": [
    {
      "assigned_seat_count": 0,
      "cowork_daily_active_user_count": 0,
      "cowork_monthly_active_user_count": 0,
      "cowork_weekly_active_user_count": 0,
      "daily_active_user_count": 0,
      "daily_adoption_rate": 0,
      "ending_at": "2019-12-27T18:11:19.117Z",
      "monthly_active_user_count": 0,
      "monthly_adoption_rate": 0,
      "pending_invite_count": 0,
      "starting_at": "2019-12-27T18:11:19.117Z",
      "weekly_active_user_count": 0,
      "weekly_adoption_rate": 0,
      "chat_cowork_unified_daily_active_user_count": 0,
      "chat_cowork_unified_monthly_active_user_count": 0,
      "chat_cowork_unified_weekly_active_user_count": 0,
      "chat_daily_active_user_count": 0,
      "chat_monthly_active_user_count": 0,
      "chat_weekly_active_user_count": 0,
      "claude_code_daily_active_user_count": 0,
      "claude_code_monthly_active_user_count": 0,
      "claude_code_weekly_active_user_count": 0,
      "claude_design_daily_active_user_count": 0,
      "claude_design_monthly_active_user_count": 0,
      "claude_design_weekly_active_user_count": 0,
      "claude_tag_daily_active_user_count": 0,
      "claude_tag_monthly_active_user_count": 0,
      "claude_tag_weekly_active_user_count": 0,
      "office_agent_daily_active_user_count": 0,
      "office_agent_monthly_active_user_count": 0,
      "office_agent_weekly_active_user_count": 0,
      "science_daily_active_user_count": 0,
      "science_entitled_user_count": 0,
      "science_monthly_active_user_count": 0,
      "science_weekly_active_user_count": 0
    }
  ],
  "next_page": "next_page"
}
```
