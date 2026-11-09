---
title: Remove Federation Rule Workspace
url: https://platform.claude.com/docs/en/api/cli/organization/federation/rules/workspaces/remove
---

# Remove Federation Rule Workspace

`$ ant organization:federation:rules:workspaces remove`

**DELETE** `/v1/organizations/federation_rules/{federation_rule_id}/workspaces/{workspace_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

Disable a federation rule for a workspace.

Idempotent; succeeds even if the enablement was already removed. OAuth
callers may only manage rules whose `oauth_scope` is
`workspace:developer` or `workspace:inference`; other scopes require a
Console session.

## Parameters

- `--federation-rule-id: string` (path parameter)

  ID of the federation rule.

- `--workspace-id: string` (path parameter)

  ID of the workspace to disable for.

## Returns

- `OrganizationFederationRuleWorkspaceRemoveResponse: object`

  - `type: "federation_rule_workspace_deleted"`

  - `federation_rule_id: string`

    Tagged ID of the federation rule.

  - `workspace_id: string`

    Tagged ID of the workspace named in the delete request. Removal is idempotent.

## Example

```bash
ant organization:federation:rules:workspaces remove \
  --federation-rule-id federation_rule_id \
  --workspace-id workspace_id
```

### Response (200)

```json
{
  "federation_rule_id": "federation_rule_id",
  "type": "federation_rule_workspace_deleted",
  "workspace_id": "workspace_id"
}
```
