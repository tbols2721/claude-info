---
title: Compliance Settings
url: https://platform.claude.com/docs/en/api/python/beta/organization/compliance_settings
---

# Compliance Settings

## Get Compliance Settings

`beta.organization.compliance_settings.retrieve() -> BetaComplianceSettings`

**GET** `/v1/organizations/compliance_settings`

Retrieve your organization's Compliance Settings.

Compliance Settings is a singleton resource: there is exactly one per
organization, addressed without an identifier. The `state` field reflects
whether the Compliance API is enabled. An organization with a parent
organization reads the state inherited from the parent's configuration.

### Returns

- `class BetaComplianceSettings`

  - `type: Literal["compliance_settings"]`

    default: compliance_settings

  - `state: BetaComplianceSettingsState`

    Whether the Compliance API is enabled for this organization.

    - `class BetaComplianceSettingsStateEnabled`

      - `type: Literal["enabled"]`

        default: enabled

    - `class BetaComplianceSettingsStateDisabled`

      - `type: Literal["disabled"]`

        default: disabled

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_compliance_settings = client.beta.organization.compliance_settings.retrieve()
print(beta_compliance_settings.state)
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

`beta.organization.compliance_settings.update(**kwargs) -> BetaComplianceSettings`

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

- `state: BetaComplianceSettingsStateParam`

  Desired state. Accepts the string shorthand "enabled" or "disabled" in place of the object form; the response always returns the canonical object form.

  - `class BetaComplianceSettingsStateEnabledParam`

    - `type: Literal["enabled"]`

  - `class BetaComplianceSettingsStateDisabledParam`

    - `type: Literal["disabled"]`

### Returns

- `class BetaComplianceSettings`

  - `type: Literal["compliance_settings"]`

    default: compliance_settings

  - `state: BetaComplianceSettingsState`

    Whether the Compliance API is enabled for this organization.

    - `class BetaComplianceSettingsStateEnabled`

      - `type: Literal["enabled"]`

        default: enabled

    - `class BetaComplianceSettingsStateDisabled`

      - `type: Literal["disabled"]`

        default: disabled

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_compliance_settings = client.beta.organization.compliance_settings.update(
    state={"type": "enabled"},
)
print(beta_compliance_settings.state)
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

- `class BetaComplianceSettings`

  - `type: Literal["compliance_settings"]`

    default: compliance_settings

  - `state: BetaComplianceSettingsState`

    Whether the Compliance API is enabled for this organization.

    - `class BetaComplianceSettingsStateEnabled`

      - `type: Literal["enabled"]`

        default: enabled

    - `class BetaComplianceSettingsStateDisabled`

      - `type: Literal["disabled"]`

        default: disabled

### Beta Compliance Settings State

- `type BetaComplianceSettingsState = ...`

  - `class BetaComplianceSettingsStateEnabled`

    - `type: Literal["enabled"]`

      default: enabled

  - `class BetaComplianceSettingsStateDisabled`

    - `type: Literal["disabled"]`

      default: disabled

### Beta Compliance Settings State Disabled

- `class BetaComplianceSettingsStateDisabled`

  - `type: Literal["disabled"]`

    default: disabled

### Beta Compliance Settings State Disabled Param

- `class BetaComplianceSettingsStateDisabledParam`

  - `type: Literal["disabled"]`

### Beta Compliance Settings State Enabled

- `class BetaComplianceSettingsStateEnabled`

  - `type: Literal["enabled"]`

    default: enabled

### Beta Compliance Settings State Enabled Param

- `class BetaComplianceSettingsStateEnabledParam`

  - `type: Literal["enabled"]`

### Beta Compliance Settings State Param

- `type BetaComplianceSettingsStateParam = ...`

  - `class BetaComplianceSettingsStateEnabledParam`

    - `type: Literal["enabled"]`

  - `class BetaComplianceSettingsStateDisabledParam`

    - `type: Literal["disabled"]`
