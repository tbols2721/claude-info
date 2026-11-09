---
title: Compliance Settings
url: https://platform.claude.com/docs/en/api/cli/organization/compliance_settings
---

# Compliance Settings

## Get Compliance Settings

`$ ant organization:compliance-settings retrieve`

**GET** `/v1/organizations/compliance_settings`

Retrieve your organization's Compliance Settings.

Compliance Settings is a singleton resource: there is exactly one per
organization, addressed without an identifier. The `state` field reflects
whether the Compliance API is enabled. An organization with a parent
organization reads the state inherited from the parent's configuration.

### Returns

- `organization_compliance_settings: object`

  - `type: "compliance_settings"`

  - `state: ComplianceSettingsStateEnabled or ComplianceSettingsStateDisabled`

    Whether the Compliance API is enabled for this organization.

    - `compliance_settings_state_enabled: object`

      - `type: "enabled"`

    - `compliance_settings_state_disabled: object`

      - `type: "disabled"`

### Example

```bash
ant organization:compliance-settings retrieve
```

#### Response (200)

```json
{
  "state": {
    "type": "enabled"
  },
  "type": "compliance_settings"
}
```

## Update Compliance Settings

`$ ant organization:compliance-settings update`

**POST** `/v1/organizations/compliance_settings`

Update your organization's Compliance Settings.

Setting `state` to `enabled` turns on the Compliance API and begins
capturing organization activity events. Setting it to `disabled` turns
both off. Access Transparency events are an exception: they are still
captured while the Compliance API is disabled, and the Compliance API
activity feed returns them once it is enabled again. `state` reflects
whether the Compliance API is enabled.

A request that sets `state` to its current value succeeds and leaves the
resource unchanged. A `disabled` request stays in effect until a later
`enabled` request or the organization's next provisioning action that
enables Access Transparency: enabling Access Transparency also enables
the Compliance API, which serves its activity events, so such
provisioning (including re-runs) re-enables the Compliance API even
after a `disabled` request. Automated provisioning never disables
compliance settings.

### Parameters

- `--state: ComplianceSettingsStateParam`

  Desired state. Accepts the string shorthand "enabled" or "disabled" in place of the object form; the response always returns the canonical object form.

  - `compliance_settings_state_enabled_param: object`

    - `type: "enabled"`

  - `compliance_settings_state_disabled_param: object`

    - `type: "disabled"`

### Returns

- `organization_compliance_settings: object`

  - `type: "compliance_settings"`

  - `state: ComplianceSettingsStateEnabled or ComplianceSettingsStateDisabled`

    Whether the Compliance API is enabled for this organization.

    - `compliance_settings_state_enabled: object`

      - `type: "enabled"`

    - `compliance_settings_state_disabled: object`

      - `type: "disabled"`

### Example

```bash
ant organization:compliance-settings update \
  --state '{type: enabled}'
```

#### Response (200)

```json
{
  "state": {
    "type": "enabled"
  },
  "type": "compliance_settings"
}
```

## Domain types

### Compliance Settings State

- `compliance_settings_state: ComplianceSettingsStateEnabled or ComplianceSettingsStateDisabled`

  - `compliance_settings_state_enabled: object`

    - `type: "enabled"`

  - `compliance_settings_state_disabled: object`

    - `type: "disabled"`

### Compliance Settings State Disabled

- `compliance_settings_state_disabled: object`

  - `type: "disabled"`

### Compliance Settings State Disabled Param

- `compliance_settings_state_disabled_param: object`

  - `type: "disabled"`

### Compliance Settings State Enabled

- `compliance_settings_state_enabled: object`

  - `type: "enabled"`

### Compliance Settings State Enabled Param

- `compliance_settings_state_enabled_param: object`

  - `type: "enabled"`

### Compliance Settings State Param

- `compliance_settings_state_param: ComplianceSettingsStateEnabledParam or ComplianceSettingsStateDisabledParam`

  - `compliance_settings_state_enabled_param: object`

    - `type: "enabled"`

  - `compliance_settings_state_disabled_param: object`

    - `type: "disabled"`

### Organization Compliance Settings

- `organization_compliance_settings: object`

  - `type: "compliance_settings"`

  - `state: ComplianceSettingsStateEnabled or ComplianceSettingsStateDisabled`

    Whether the Compliance API is enabled for this organization.

    - `compliance_settings_state_enabled: object`

      - `type: "enabled"`

    - `compliance_settings_state_disabled: object`

      - `type: "disabled"`
