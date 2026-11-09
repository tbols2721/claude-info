---
title: Get Service Account
url: https://platform.claude.com/docs/en/api/python/organization/service_accounts/retrieve
---

# Get Service Account

`organization.service_accounts.retrieve(service_account_id) -> ServiceAccount`

**GET** `/v1/organizations/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Retrieve a service account by its ID (`svac_...`).

## Parameters

- `service_account_id: str` (path parameter)

  ID of the service account.

## Returns

- `class ServiceAccount`

  Named non-human identity within the caller's organization.

  A service account is a pure identity: name + org. Authorization lives on
  whatever references it (federation rules).

  - `type: Literal["service_account"]`

    default: service_account

  - `id: str`

    Tagged ID of the service account.

  - `archived_at: Optional[datetime]`

    If set, this service account is archived.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this service account.

  - `created_at: datetime`

    When this service account was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this service account.

  - `description: Optional[str]`

    Optional free-text description.

  - `name: str`

    Admin-chosen slug identifier.

  - `organization_role: Literal["admin", "developer"]`

    Org-level role. A federation rule may only be created or retargeted to grant `org:admin` scope when this is `admin`. A rule granting `org:admin` whose target is later demoted to `developer` is rejected at token exchange. Rules granting `org:admin` are managed in the Console.

    - `"admin"`

    - `"developer"`

  - `updated_at: datetime`

    When this service account was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this service account.

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account = client.organization.service_accounts.retrieve(
    "service_account_id",
)
print(service_account.id)
```

### Response (200)

```json
{
  "id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "description": "description",
  "name": "ci-deploy-bot",
  "organization_role": "admin",
  "type": "service_account",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id"
}
```
