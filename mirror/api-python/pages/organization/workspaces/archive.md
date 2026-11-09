---
title: Archive Workspace
url: https://platform.claude.com/docs/en/api/python/organization/workspaces/archive
---

# Archive Workspace

`organization.workspaces.archive(workspace_id) -> Workspace`

**POST** `/v1/organizations/workspaces/{workspace_id}/archive`

Archive Workspace

## Parameters

- `workspace_id: str` (path parameter)

## Returns

- `class Workspace`

  - `type: Literal["workspace"]`

    Object type.

    For Workspaces, this is always `"workspace"`.

    default: workspace

  - `id: str`

    ID of the Workspace.

  - `archived_at: Optional[datetime]`

    RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

    format: date-time

  - `compartment_id: str`

    Identifier for this Workspace's encryption compartment. When you configure an
    AWS KMS customer-managed encryption key (CMEK) that isn't bound to a user
    profile, reference this value in your KMS key-policy condition so the key is
    scoped to this compartment. On GCP and Azure, Anthropic enforces the compartment
    binding automatically; you do not need to reference this value in your key
    configuration. See the CMEK integration guide for the required key
    configuration; unless your organization is on Claude Platform on AWS, it
    includes a separate value used during key validation. On Claude Platform on AWS
    there is no separate validation value: your organization's own key is validated
    against this Workspace's own value when it is attached, so if its key policy
    uses the compartment condition, add this value to it before attaching the key.

  - `created_at: datetime`

    RFC 3339 datetime string indicating when the Workspace was created.

    format: date-time

  - `data_residency: DataResidency`

    Data residency configuration.

    - `allowed_inference_geos: Union[List[AllowedInferenceGeo], Literal["unrestricted"]]`

      Permitted inference geo values. 'unrestricted' means all geos are allowed.

      - `List[AllowedInferenceGeo]`

        - `"global"`

        - `"us"`

      - `"unrestricted"`

    - `default_inference_geo: Literal["global", "us"]`

      Default inference geo applied when requests omit the parameter.

      - `"global"`

      - `"us"`

    - `workspace_geo: Literal["us"]`

      Geographic region for workspace data storage. Immutable after creation.

  - `display_color: str`

    Hex color code representing the Workspace in the Anthropic Console.

  - `external_key_id: Optional[str]`

    ID of the customer-managed encryption key (CMEK) configuration to use for this
    Workspace. Setting this field requires CMEK to be enabled for your
    organization. When set, data stored for this Workspace is encrypted with the
    referenced key. Create key configurations with the External Keys API. On
    Claude Platform on AWS the value for an AWS KMS key is the key's ARN, and your
    organization's own key must be a single-Region key in the same AWS account and
    Region as the Workspace. On that platform the key is validated against this
    Workspace when it is attached, so a key-policy problem is reported as an error
    on this request. This field is write-once: once a key is attached to a Workspace
    it cannot be detached or replaced. To rotate key material, rotate the underlying
    key on your cloud KMS; the `external_key_id` stays the same.

  - `name: str`

    Name of the Workspace.

  - `tags: Dict[str, str]`

    User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

  - `user_profile_id: Optional[str]`

    ID of the user profile attached to the Workspace, or null if it has none. Every inference request through a Workspace that has a user profile must name that profile.

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace = client.organization.workspaces.archive(
    "workspace_id",
)
print(workspace.id)
```

### Response (200)

```json
{
  "id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "archived_at": "2024-11-01T23:59:27.427722Z",
  "compartment_id": "f8a7b6c5-4d3e-4f1a-8b9c-0d1e2f3a4b5c",
  "created_at": "2024-10-30T23:58:27.427722Z",
  "data_residency": {
    "allowed_inference_geos": "unrestricted",
    "default_inference_geo": "global",
    "workspace_geo": "us"
  },
  "display_color": "#6C5BB9",
  "external_key_id": "ekey_01SDCCSbTxrXDpWc1phhtcfK",
  "name": "Workspace Name",
  "tags": {
    "env": "prod",
    "team": "platform"
  },
  "type": "workspace",
  "user_profile_id": "uprof_01SDCCSbTxrXDpWc1phhtcfK"
}
```
