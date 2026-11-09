---
title: Add Federation Rule Workspace
url: https://platform.claude.com/docs/en/api/cli/organization/federation/rules/workspaces/add
---

# Add Federation Rule Workspace

`$ ant organization:federation:rules:workspaces add`

**POST** `/v1/organizations/federation_rules/{federation_rule_id}/workspaces`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

Enable a federation rule for a workspace.

Idempotent; re-enabling returns the existing enablement. The rule and
workspace must both belong to your organization. Membership of the
rule's target service account in this workspace is not checked at
enablement: token exchange into this workspace is rejected unless the
target is a member (it is implicitly a member of the default workspace).
Archived rules are rejected with 400. OAuth callers may only manage rules
whose `oauth_scope` is `workspace:developer` or `workspace:inference`;
other scopes require a Console session.

## Parameters

- `--federation-rule-id: string` (path parameter)

  ID of the federation rule.

- `--workspace-id: string`

  Tagged ID of the workspace to enable this rule for.

## Returns

- `federation_rule_workspace: object`

  - `type: "federation_rule_workspace"`

  - `created_at: string`

    When this workspace was enabled for the rule.

    format: date-time

  - `created_by_actor_id: string`

    Tagged ID (`user_...` or `svac_...`) of the actor that enabled this workspace for the rule, if known.

  - `federation_rule_id: string`

    Tagged ID of the federation rule.

  - `workspace_id: string`

    Tagged ID of the workspace this rule is enabled for.

  - `workspace_name: string`

    Workspace display name. Populated when listing; null in the enable response.

## Example

```bash
ant organization:federation:rules:workspaces add \
  --federation-rule-id federation_rule_id \
  --workspace-id workspace_id
```

### Response (200)

```json
{
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "federation_rule_id": "federation_rule_id",
  "type": "federation_rule_workspace",
  "workspace_id": "workspace_id",
  "workspace_name": "workspace_name"
}
```
