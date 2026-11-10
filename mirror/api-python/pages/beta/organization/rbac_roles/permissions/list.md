---
title: List RBAC Role Permissions
url: https://platform.claude.com/docs/en/api/python/beta/organization/rbac_roles/permissions/list
---

# List RBAC Role Permissions

`beta.organization.rbac_roles.permissions.list(rbac_role_id, **kwargs) -> SyncPageCursor[BetaRBACRolePermission]`

**GET** `/v1/organizations/rbac_roles/{rbac_role_id}/permissions`

List the permissions an RBAC Role grants.

The RBAC Roles API is available to Claude Enterprise organizations only.

## Parameters

- `rbac_role_id: str` (path parameter)

  ID of the RBAC Role.

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Optionally set to the `next_page` token from the previous response.

## Returns

- `class BetaRBACRolePermission`

  - `type: Literal["rbac_role_permission"]`

    Object type.

    For RBAC Role Permissions, this is always `"rbac_role_permission"`.

    default: rbac_role_permission

  - `action: str`

    Action the permission grants on the resource.

    The vocabulary follows the resource: an `organization` grant carries a
    product-feature entitlement (for example `chat`), an admin-panel
    permission entitlement (`permission_*`), or a blanket capability-access
    mode — `capability_access_all` grants every product-feature entitlement
    except `inference_hooks_inspection`, which a role holds only through its
    own row, and `capability_access_all_ga` grants the subset of those for
    stable features as it stands at permission-check time; neither mode grants
    model-access entitlements. A consumer enumerating a role's per-feature grants should
    treat a blanket row as granting every product-feature entitlement it
    covers, or it will under-report the role's effective access. A `connector_tool` grant carries
    a tool-access action (`use` or `always_allow`); a `connector_scope` grant
    carries the scope action `grant` (the role may receive the named OAuth
    scope when tokens are minted for the connector); `connector` and
    `all_connectors` grants carry a tool-access action, the scope action, or
    an authentication-method action (`interactive` or `managed`).

  - `resource: Resource`

    What the permission applies to.

    A tagged union: `type` names the kind of resource and determines which
    identifier fields are present.

    - `class BetaRBACOrganizationPermissionResource`

      - `type: Literal["organization"]`

        Kind of resource the permission applies to.

        default: organization

      - `organization_id: str`

        UUID of the organization the permission applies to.

    - `class BetaRBACConnectorToolPermissionResource`

      - `type: Literal["connector_tool"]`

        Kind of resource the permission applies to.

        default: connector_tool

      - `connector_id: str`

        ID of the connector the permission applies to.

      - `tool_name: str`

        Published name of the connector tool the permission applies to.

        When the published name contains characters outside `[a-zA-Z0-9_-]` (or
        collides with a reserved form), it is server-encoded into a stable
        `{prefix}_{32-hex}` form — a shortened readable prefix of the name plus
        a hash — from which the published name is not recoverable.

    - `class BetaRBACConnectorScopePermissionResource`

      - `type: Literal["connector_scope"]`

        Kind of resource the permission applies to.

        default: connector_scope

      - `connector_id: str`

        ID of the connector the permission applies to.

      - `scope: str`

        OAuth scope the permission names — the role may receive this scope when
        tokens are minted for the connector.

        Subject to the same encoding rule as `tool_name`: a scope containing
        characters outside `[a-zA-Z0-9_-]` (or colliding with a reserved form)
        appears server-encoded in a stable `{prefix}_{32-hex}` form. OAuth
        scopes routinely contain `:` and `/`, so most appear encoded.

    - `class BetaRBACConnectorPermissionResource`

      - `type: Literal["connector"]`

        Kind of resource the permission applies to.

        default: connector

      - `connector_id: str`

        ID of the connector the permission applies to.

    - `class BetaRBACAllConnectorsPermissionResource`

      - `type: Literal["all_connectors"]`

        Kind of resource the permission applies to.

        default: all_connectors

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.rbac_roles.permissions.list(
    rbac_role_id="rbac_role_id",
)
page = page.data[0]
print(page.action)
```

### Response (200)

```json
{
  "data": [
    {
      "action": "use",
      "resource": {
        "organization_id": "3c4f5e6d-7a8b-49c0-9d1e-2f3a4b5c6d7e",
        "type": "organization"
      },
      "type": "rbac_role_permission"
    }
  ],
  "has_more": true,
  "next_page": "eyJjdXJzb3IiOiAicmJhY19yb2xlXzAxIn0"
}
```
