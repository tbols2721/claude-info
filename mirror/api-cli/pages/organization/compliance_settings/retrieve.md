---
title: Get Compliance Settings
url: https://platform.claude.com/docs/en/api/cli/organization/compliance_settings/retrieve
---

# Get Compliance Settings

`$ ant organization:compliance-settings retrieve`

**GET** `/v1/organizations/compliance_settings`

Retrieve your organization's Compliance Settings.

Compliance Settings is a singleton resource: there is exactly one per
organization, addressed without an identifier. The `state` field reflects
whether the Compliance API is enabled. An organization with a parent
organization reads the state inherited from the parent's configuration.

## Returns

- `organization_compliance_settings: object`

  - `type: "compliance_settings"`

  - `state: ComplianceSettingsStateEnabled or ComplianceSettingsStateDisabled`

    Whether the Compliance API is enabled for this organization.

    - `compliance_settings_state_enabled: object`

      - `type: "enabled"`

    - `compliance_settings_state_disabled: object`

      - `type: "disabled"`

## Example

```bash
ant organization:compliance-settings retrieve
```

### Response (200)

```json
{
  "state": {
    "type": "enabled"
  },
  "type": "compliance_settings"
}
```
