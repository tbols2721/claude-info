---
title: Update API Key
url: https://platform.claude.com/docs/en/api/python/beta/organization/api_keys/update
---

# Update API Key

`beta.organization.api_keys.update(api_key_id, **kwargs) -> BetaAPIKey`

**POST** `/v1/organizations/api_keys/{api_key_id}`

Update API Key

## Parameters

- `api_key_id: str` (path parameter)

  ID of the API key.

- `name: Optional[str]`

  Name of the API key.

  minLength: 1, maxLength: 500

- `status: Optional[Literal["active", "archived", "inactive"]]`

  Status of the API key.

  - `"active"`

  - `"archived"`

  - `"inactive"`

## Returns

- `class BetaAPIKey`

  - `type: Literal["api_key"]`

    Object type.

    For API Keys, this is always `"api_key"`.

    default: api_key

  - `id: str`

    ID of the API key.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the API Key was created.

    format: date-time

  - `created_by: Optional[BetaAPIKeyCreatedBy]`

    The ID and type of the actor that created the API key, or `null` when the
    creator is not recorded (legacy, workload-identity-federated, or
    system-created keys).

    - `type: Literal["service_account", "user"]`

      Type of the actor that created the object.

      - `"service_account"`

      - `"user"`

    - `id: str`

      ID of the actor that created the object.

  - `expires_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the API Key expires, or `null` if it never expires.

    format: date-time

  - `name: str`

    Name of the API key.

  - `partial_key_hint: Optional[str]`

    Partially redacted hint for the API key.

  - `principal: Optional[Principal]`

    The principal the API key acts as (a User or a Service Account), or `null` if the API key is not bound to a principal.

    - `class BetaAPIKeyUserActor`

      - `type: Literal["user_actor"]`

        Principal type. Always `"user_actor"` for a User.

        default: user_actor

      - `user_id: str`

        ID of the User the API key acts as.

    - `class BetaAPIKeyServiceAccountActor`

      - `type: Literal["service_account_actor"]`

        Principal type. Always `"service_account_actor"` for a Service Account.

        default: service_account_actor

      - `service_account_id: str`

        ID of the Service Account the API key acts as.

  - `scope: Scope`

    Where the API key belongs: its Workspace (`{"type": "workspace", "workspace_id": "wrkspc_..."}`, with the Workspace's real ID even when it is the organization's default Workspace), or the organization (`{"type": "organization"}`) for a principal-bound API key that has no Workspace.

    - `class BetaAPIKeyOrganizationScope`

      - `type: Literal["organization"]`

        Scope type. Always `"organization"`: the API key has no Workspace. Only a principal-bound API key can have this scope.

        default: organization

    - `class BetaAPIKeyWorkspaceScope`

      - `type: Literal["workspace"]`

        Scope type. Always `"workspace"`: the API key belongs to one Workspace.

        default: workspace

      - `workspace_id: str`

        ID of the Workspace the API key belongs to, including when it is the organization's default Workspace.

  - `status: Literal["active", "archived", "expired", "inactive"]`

    Status of the API key.

    - `"active"`

    - `"archived"`

    - `"expired"`

    - `"inactive"`

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_api_key = client.beta.organization.api_keys.update(
    api_key_id="api_key_id",
)
print(beta_api_key.id)
```

### Response (200)

```json
{
  "id": "apikey_01Rj2N8SVvo6BePZj99NhmiT",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by": {
    "id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
    "type": "user"
  },
  "expires_at": "2024-10-30T23:58:27.427722Z",
  "name": "Developer Key",
  "partial_key_hint": "sk-ant-api03-R2D...igAA",
  "principal": {
    "type": "user_actor",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
  },
  "scope": {
    "type": "workspace",
    "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  },
  "status": "active",
  "type": "api_key"
}
```
