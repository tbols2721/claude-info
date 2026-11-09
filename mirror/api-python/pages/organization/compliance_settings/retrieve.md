---
title: Get Compliance Settings
url: https://platform.claude.com/docs/en/api/python/organization/compliance_settings/retrieve
---

# Get Compliance Settings

`organization.compliance_settings.retrieve() -> OrganizationComplianceSettings`

**GET** `/v1/organizations/compliance_settings`

Retrieve your organization's Compliance Settings.

Compliance Settings is a singleton resource: there is exactly one per
organization, addressed without an identifier. The `state` field reflects
whether the Compliance API is enabled. An organization with a parent
organization reads the state inherited from the parent's configuration.

## Returns

- `class OrganizationComplianceSettings`

  - `type: Literal["compliance_settings"]`

    default: compliance_settings

  - `state: ComplianceSettingsState`

    Whether the Compliance API is enabled for this organization.

    - `class ComplianceSettingsStateEnabled`

      - `type: Literal["enabled"]`

        default: enabled

    - `class ComplianceSettingsStateDisabled`

      - `type: Literal["disabled"]`

        default: disabled

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
organization_compliance_settings = client.organization.compliance_settings.retrieve()
print(organization_compliance_settings.state)
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
