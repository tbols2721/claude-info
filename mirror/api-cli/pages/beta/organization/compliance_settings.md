---
title: Compliance Settings
url: https://platform.claude.com/docs/en/api/cli/beta/organization/compliance_settings
---

# Compliance Settings

## Get Compliance Settings

`$ ant beta:organization:compliance-settings retrieve`

**GET** `/v1/organizations/compliance_settings`

Retrieve your organization's Compliance Settings.

Compliance Settings is a singleton resource: there is exactly one per
organization, addressed without an identifier. The `state` field reflects
whether the Compliance API is enabled. An organization with a parent
organization reads the state inherited from the parent's configuration.

### Returns

- `beta_compliance_settings: object`

  - `type: "compliance_settings"`

  - `state: BetaComplianceSettingsStateEnabled or BetaComplianceSettingsStateDisabled`

    Whether the Compliance API is enabled for this organization.

    - `beta_compliance_settings_state_enabled: object`

      - `type: "enabled"`

    - `beta_compliance_settings_state_disabled: object`

      - `type: "disabled"`

### Example

```bash
ant beta:organization:compliance-settings retrieve
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

`$ ant beta:organization:compliance-settings update`

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

- `--state: BetaComplianceSettingsStateParam`

  Desired state. Accepts the string shorthand "enabled" or "disabled" in place of the object form; the response always returns the canonical object form.

  - `beta_compliance_settings_state_enabled_param: object`

    - `type: "enabled"`

  - `beta_compliance_settings_state_disabled_param: object`

    - `type: "disabled"`

### Returns

- `beta_compliance_settings: object`

  - `type: "compliance_settings"`

  - `state: BetaComplianceSettingsStateEnabled or BetaComplianceSettingsStateDisabled`

    Whether the Compliance API is enabled for this organization.

    - `beta_compliance_settings_state_enabled: object`

      - `type: "enabled"`

    - `beta_compliance_settings_state_disabled: object`

      - `type: "disabled"`

### Example

```bash
ant beta:organization:compliance-settings update \
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

### Beta Compliance Settings

- `beta_compliance_settings: object`

  - `type: "compliance_settings"`

  - `state: BetaComplianceSettingsStateEnabled or BetaComplianceSettingsStateDisabled`

    Whether the Compliance API is enabled for this organization.

    - `beta_compliance_settings_state_enabled: object`

      - `type: "enabled"`

    - `beta_compliance_settings_state_disabled: object`

      - `type: "disabled"`

### Beta Compliance Settings State

- `beta_compliance_settings_state: BetaComplianceSettingsStateEnabled or BetaComplianceSettingsStateDisabled`

  - `beta_compliance_settings_state_enabled: object`

    - `type: "enabled"`

  - `beta_compliance_settings_state_disabled: object`

    - `type: "disabled"`

### Beta Compliance Settings State Disabled

- `beta_compliance_settings_state_disabled: object`

  - `type: "disabled"`

### Beta Compliance Settings State Disabled Param

- `beta_compliance_settings_state_disabled_param: object`

  - `type: "disabled"`

### Beta Compliance Settings State Enabled

- `beta_compliance_settings_state_enabled: object`

  - `type: "enabled"`

### Beta Compliance Settings State Enabled Param

- `beta_compliance_settings_state_enabled_param: object`

  - `type: "enabled"`

### Beta Compliance Settings State Param

- `beta_compliance_settings_state_param: BetaComplianceSettingsStateEnabledParam or BetaComplianceSettingsStateDisabledParam`

  - `beta_compliance_settings_state_enabled_param: object`

    - `type: "enabled"`

  - `beta_compliance_settings_state_disabled_param: object`

    - `type: "disabled"`
