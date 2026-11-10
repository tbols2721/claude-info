---
title: Installation Settings
url: https://platform.claude.com/docs/en/api/cli/beta/organization/plugins/installation_settings
---

# Installation Settings

## List Plugin Installation Settings

`$ ant beta:organization:plugins:installation-settings list`

**GET** `/v1/organizations/plugins/{plugin_id}/installation_settings`

List an organization-owned Plugin's installation settings, which say which
members it is for, most recently created first.

The list holds the Plugin's own organization-wide setting (absent while the Plugin
inherits its marketplace's default) and each RBAC Group's own setting. A
member-owned Plugin has shares instead, so this path returns 404 for one.

**Accepted credentials:** an Admin API key with the `read:plugins` or `read:org_audit` scope, or a Compliance Access Key with the `read:compliance_org_data` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

### Parameters

- `--plugin-id: string` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `--limit: optional number` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `100`.

  minimum: 1, maximum: 100

- `--organization-id: optional string` (query parameter)

  For a `read:org_audit` or `read:compliance_org_data` key created for all of a parent organization's linked organizations: a child organization of that parent to read instead of the organization the key was created in, given as the organization's UUID or its `org_`-prefixed ID. A value that is neither returns a 400; an organization that is not a child of the key's parent, or where the Plugins API is not available, returns a 404. Any other key may pass only its own organization's ID here; another organization returns a 404.

- `--page: optional string` (query parameter)

  Optionally set to the `next_page` token from the previous response.

  maxLength: 2048

- `--target-type: optional "organization" or "rbac_group"` (query parameter)

  Only settings for this kind of target: `organization` (the organization-wide setting) or `rbac_group` (an RBAC Group's).

  - `"organization"`

  - `"rbac_group"`

- `--beta: optional array of AnthropicBeta` (header parameter)

  This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this header.

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

### Returns

- `BetaPluginInstallationSettingList: object`

  - `data: array of BetaPluginInstallationSetting`

    - `type: "plugin_installation_setting"`

      Always `plugin_installation_setting`.

    - `created_at: string`

      When the target was first given a setting for this Plugin.

      format: date-time

    - `installation_preference: "auto_install" or "available" or "not_available" or "required"`

      The setting the target holds for this Plugin. One of `required`, `auto_install`, `available`, `not_available`; a value this API does not yet name is returned as stored.

      - `"auto_install"`

      - `"available"`

      - `"not_available"`

      - `"required"`

    - `plugin_id: string`

      The Plugin's ID.

    - `target: BetaPluginTargetOrganization or BetaPluginTargetRBACGroup or BetaPluginTargetOrganizationMember`

      Whose setting this is: `organization` (the Plugin's own organization-wide setting) or `rbac_group` (one RBAC Group's own setting); `organization_member` does not occur here.

      - `beta_plugin_target_organization: object`

        - `type: "organization"`

          Every member of the organization.

      - `beta_plugin_target_rbac_group: object`

        - `type: "rbac_group"`

          An RBAC Group.

        - `rbac_group_id: string`

          The RBAC Group's ID.

      - `beta_plugin_target_organization_member: object`

        - `type: "organization_member"`

          One member of the organization.

        - `user_id: string`

          The member's User ID.

    - `updated_at: string`

      When its setting last changed.

      format: date-time

  - `next_page: string`

    Token to provide in as `page` in the subsequent request to retrieve the next page of data.

### Example

```bash
ant beta:organization:plugins:installation-settings list \
  --plugin-id plugin_id
```

#### Response (200)

```json
{
  "data": [
    {
      "created_at": "2026-03-14T09:26:53.589793Z",
      "installation_preference": "required",
      "plugin_id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
      "target": {
        "type": "organization"
      },
      "type": "plugin_installation_setting",
      "updated_at": "2026-03-14T09:26:53.589793Z"
    }
  ],
  "next_page": "page_MjAyNi0wOS0xNlQxNDowNTowOVo"
}
```

## Set Plugin Installation Setting

`$ ant beta:organization:plugins:installation-settings set`

**POST** `/v1/organizations/plugins/{plugin_id}/installation_settings/{target}`

Set or change an organization-owned Plugin's installation setting for the whole
organization or for one RBAC Group.

Writing the value a target already holds of its own changes nothing.

A member-owned Plugin has shares instead of installation settings, so this path
returns 404 for one.

Send a Plugin's installation-setting writes one at a time. If several writes for the
same Plugin arrive at the same time, the server handles them one after another and
can answer some of them with `503` instead of applying them. That `503` carries
`x-should-retry: true`, and the write is safe to repeat: wait a second or two, then
send it again.

**Accepted credentials:** an Admin API key with the `write:plugins` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

### Parameters

- `--plugin-id: string` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `--target: string` (path parameter)

  The target whose setting is written: the literal `organization` for the Plugin's organization-wide setting, or an RBAC Group's ID (prefixed `rbac_group_`) for that group's own setting. Writing the `organization` target stops the Plugin from inheriting its marketplace's default, even when the value written equals that default.

- `--installation-preference: "auto_install" or "available" or "not_available" or "required"`

  The installation setting the target is to hold for this Plugin: one of `required`, `auto_install`, `available`, `not_available`.

  - `"auto_install"`

  - `"available"`

  - `"not_available"`

  - `"required"`

- `--beta: optional array of AnthropicBeta` (header parameter)

  This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this header.

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

### Returns

- `beta_plugin_installation_setting: object`

  The installation setting an organization-owned Plugin holds for one
  target. It has no ID of its own: it is addressed by the Plugin's ID and the
  target.

  - `type: "plugin_installation_setting"`

    Always `plugin_installation_setting`.

  - `created_at: string`

    When the target was first given a setting for this Plugin.

    format: date-time

  - `installation_preference: "auto_install" or "available" or "not_available" or "required"`

    The setting the target holds for this Plugin. One of `required`, `auto_install`, `available`, `not_available`; a value this API does not yet name is returned as stored.

    - `"auto_install"`

    - `"available"`

    - `"not_available"`

    - `"required"`

  - `plugin_id: string`

    The Plugin's ID.

  - `target: BetaPluginTargetOrganization or BetaPluginTargetRBACGroup or BetaPluginTargetOrganizationMember`

    Whose setting this is: `organization` (the Plugin's own organization-wide setting) or `rbac_group` (one RBAC Group's own setting); `organization_member` does not occur here.

    - `beta_plugin_target_organization: object`

      - `type: "organization"`

        Every member of the organization.

    - `beta_plugin_target_rbac_group: object`

      - `type: "rbac_group"`

        An RBAC Group.

      - `rbac_group_id: string`

        The RBAC Group's ID.

    - `beta_plugin_target_organization_member: object`

      - `type: "organization_member"`

        One member of the organization.

      - `user_id: string`

        The member's User ID.

  - `updated_at: string`

    When its setting last changed.

    format: date-time

### Example

```bash
ant beta:organization:plugins:installation-settings set \
  --plugin-id plugin_id \
  --target target \
  --installation-preference required
```

#### Response (200)

```json
{
  "created_at": "2026-03-14T09:26:53.589793Z",
  "installation_preference": "required",
  "plugin_id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
  "target": {
    "type": "organization"
  },
  "type": "plugin_installation_setting",
  "updated_at": "2026-03-14T09:26:53.589793Z"
}
```

## Remove Plugin Installation Setting

`$ ant beta:organization:plugins:installation-settings remove`

**DELETE** `/v1/organizations/plugins/{plugin_id}/installation_settings/{target}`

Remove an organization-owned Plugin's own installation setting for the whole
organization or for one RBAC Group.

Removing the `organization` target returns the Plugin to its marketplace's default
installation setting and leaves the groups' settings in place. Removing a group's
setting makes the group's members fall back to the Plugin's organization-wide setting
or to the settings of their other groups.

A target that holds no setting of its own returns 404 (a Plugin that already inherits
its marketplace's default holds no `organization` setting), and so does a member-owned
Plugin.

A removal counts as one of the Plugin's installation-setting writes: send all of those
writes one at a time. If several arrive for the same Plugin at the same time, the server
handles them one after another and can answer some of them with `503` and
`x-should-retry: true` instead of applying them; wait a second or two and send the
removal again. A `404` on the repeat means the setting is already gone.

**Accepted credentials:** an Admin API key with the `write:plugins` scope.

Every request must include the beta header `anthropic-beta: ce-plugins-2026-09-01`. A request without it returns `404`, exactly as if the endpoint did not exist. The Plugins API is in beta and is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations, or to organizations with HIPAA readiness enabled.

### Parameters

- `--plugin-id: string` (path parameter)

  ID of the Plugin (prefixed `plugin_`).

- `--target: string` (path parameter)

  The target whose own setting is removed: the literal `organization` for the Plugin's organization-wide setting, or an RBAC Group's ID (prefixed `rbac_group_`) for that group's own setting. Removing the `organization` setting returns the Plugin to its marketplace's default.

- `--beta: optional array of AnthropicBeta` (header parameter)

  This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this header.

  - `"message-batches-2024-09-24"`

  - `"prompt-caching-2024-07-31"`

  - `"computer-use-2024-10-22"`

  - `"computer-use-2025-01-24"`

  - `"pdfs-2024-09-25"`

  - `"token-counting-2024-11-01"`

  - `"token-efficient-tools-2025-02-19"`

  - `"output-128k-2025-02-19"`

  - `"files-api-2025-04-14"`

  - `"mcp-client-2025-04-04"`

  - `"mcp-client-2025-11-20"`

  - `"dev-full-thinking-2025-05-14"`

  - `"interleaved-thinking-2025-05-14"`

  - `"code-execution-2025-05-22"`

  - `"extended-cache-ttl-2025-04-11"`

  - `"context-1m-2025-08-07"`

  - `"context-management-2025-06-27"`

  - `"model-context-window-exceeded-2025-08-26"`

  - `"skills-2025-10-02"`

  - `"fast-mode-2026-02-01"`

  - `"output-300k-2026-03-24"`

  - `"user-profiles-2026-03-24"`

  - `"user-profiles-2026-08-18"`

  - `"user-profiles-2026-09-04"`

  - `"advisor-tool-2026-03-01"`

  - `"managed-agents-2026-04-01"`

  - `"cache-diagnosis-2026-04-07"`

  - `"dreaming-2026-04-21"`

  - `"thinking-token-count-2026-05-13"`

  - `"server-side-fallback-2026-06-01"`

  - `"server-side-fallback-2026-07-01"`

  - `"fallback-credit-2026-06-01"`

  - `"fallback-credit-2026-07-01"`

  - `"agent-memory-2026-07-22"`

  - `"mid-conversation-tool-changes-2026-07-01"`

  - `"compact-2026-01-12"`

  - `"computer-use-2025-11-24"`

  - `"mcp-tunnels-2026-06-22"`

  - `"structured-outputs-2025-11-13"`

  - `"task-budgets-2026-03-13"`

  - `"thinking-display-updates-2026-08-18"`

  - `"ce-user-management-2026-07-13"`

  - `"mid-conversation-output-config-2026-07-01"`

  - `"thinking-binding-controls-2026-08-01"`

  - `"mid-conversation-system-clear-at-2026-08-21"`

  - `"compact-2026-09-04"`

  - `"inline-tools-2026-09-15"`

  - `"mcp-client-2026-09-15"`

  - `"ce-plugins-2026-09-01"`

  - `"spend-limit-reads-2026-09-26"`

  - `"telemetry-destinations-2026-08-11"`

  - `"webhooks-2026-10-07"`

  - `"admin-user-sign-out-2026-10-08"`

  - `"message-threads-2026-08-12"`

  - `"analytics-usage-cost-2026-08-24"`

  - `"experimental-claude-tag-2026-10-21"`

### Returns

- `beta_deleted_plugin_installation_setting: object`

  Confirmation that one target's installation setting was removed, naming
  the Plugin and the target in place of an ID.

  - `type: "plugin_installation_setting_deleted"`

    Always `plugin_installation_setting_deleted`.

  - `plugin_id: string`

    The Plugin's ID.

  - `target: BetaPluginTargetOrganization or BetaPluginTargetRBACGroup or BetaPluginTargetOrganizationMember`

    Whose setting was removed.

    - `beta_plugin_target_organization: object`

      - `type: "organization"`

        Every member of the organization.

    - `beta_plugin_target_rbac_group: object`

      - `type: "rbac_group"`

        An RBAC Group.

      - `rbac_group_id: string`

        The RBAC Group's ID.

    - `beta_plugin_target_organization_member: object`

      - `type: "organization_member"`

        One member of the organization.

      - `user_id: string`

        The member's User ID.

### Example

```bash
ant beta:organization:plugins:installation-settings remove \
  --plugin-id plugin_id \
  --target target
```

#### Response (200)

```json
{
  "plugin_id": "plugin_01JyHfbRkZvD1gW7oTqXc3Ne",
  "target": {
    "rbac_group_id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
    "type": "rbac_group"
  },
  "type": "plugin_installation_setting_deleted"
}
```

## Domain types

### Beta Deleted Plugin Installation Setting

- `beta_deleted_plugin_installation_setting: object`

  Confirmation that one target's installation setting was removed, naming
  the Plugin and the target in place of an ID.

  - `type: "plugin_installation_setting_deleted"`

    Always `plugin_installation_setting_deleted`.

  - `plugin_id: string`

    The Plugin's ID.

  - `target: BetaPluginTargetOrganization or BetaPluginTargetRBACGroup or BetaPluginTargetOrganizationMember`

    Whose setting was removed.

    - `beta_plugin_target_organization: object`

      - `type: "organization"`

        Every member of the organization.

    - `beta_plugin_target_rbac_group: object`

      - `type: "rbac_group"`

        An RBAC Group.

      - `rbac_group_id: string`

        The RBAC Group's ID.

    - `beta_plugin_target_organization_member: object`

      - `type: "organization_member"`

        One member of the organization.

      - `user_id: string`

        The member's User ID.

### Beta Plugin Installation Setting

- `beta_plugin_installation_setting: object`

  The installation setting an organization-owned Plugin holds for one
  target. It has no ID of its own: it is addressed by the Plugin's ID and the
  target.

  - `type: "plugin_installation_setting"`

    Always `plugin_installation_setting`.

  - `created_at: string`

    When the target was first given a setting for this Plugin.

    format: date-time

  - `installation_preference: "auto_install" or "available" or "not_available" or "required"`

    The setting the target holds for this Plugin. One of `required`, `auto_install`, `available`, `not_available`; a value this API does not yet name is returned as stored.

    - `"auto_install"`

    - `"available"`

    - `"not_available"`

    - `"required"`

  - `plugin_id: string`

    The Plugin's ID.

  - `target: BetaPluginTargetOrganization or BetaPluginTargetRBACGroup or BetaPluginTargetOrganizationMember`

    Whose setting this is: `organization` (the Plugin's own organization-wide setting) or `rbac_group` (one RBAC Group's own setting); `organization_member` does not occur here.

    - `beta_plugin_target_organization: object`

      - `type: "organization"`

        Every member of the organization.

    - `beta_plugin_target_rbac_group: object`

      - `type: "rbac_group"`

        An RBAC Group.

      - `rbac_group_id: string`

        The RBAC Group's ID.

    - `beta_plugin_target_organization_member: object`

      - `type: "organization_member"`

        One member of the organization.

      - `user_id: string`

        The member's User ID.

  - `updated_at: string`

    When its setting last changed.

    format: date-time
