---
title: Workspaces
url: https://platform.claude.com/docs/en/api/python/organization/workspaces
---

# Workspaces

## List Workspaces

`organization.workspaces.list(**kwargs) -> SyncPage[Workspace]`

**GET** `/v1/organizations/workspaces`

List Workspaces

### Parameters

- `after_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `ids: Optional[Sequence[str]]` (query parameter)

  Only the Workspaces with these IDs, at most 100. `include_archived` and `include_default` still apply, and IDs of Workspaces the caller can't list are left out.

- `include_archived: Optional[bool]` (query parameter)

  Whether to include Workspaces that have been archived in the response

  default: false

- `include_default: Optional[bool]` (query parameter)

  Whether to include the organization's default Workspace in the response

  default: false

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

### Returns

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

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.workspaces.list()
page = page.data[0]
print(page.id)
```

#### Response (200)

```json
{
  "data": [
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
  ],
  "first_id": "first_id",
  "has_more": true,
  "last_id": "last_id"
}
```

## Create Workspace

`organization.workspaces.create(**kwargs) -> Workspace`

**POST** `/v1/organizations/workspaces`

Create Workspace

### Parameters

- `name: str`

  Name of the Workspace.

  minLength: 1, maxLength: 255

- `data_residency: Optional[DataResidencyCreateConfigParam]`

  Data residency configuration for the workspace. If omitted, defaults to `workspace_geo: "us"`, `allowed_inference_geos: "unrestricted"`, and `default_inference_geo: "global"`.

  - `allowed_inference_geos: Optional[Union[List[AllowedInferenceGeo], Literal["unrestricted"], null]]`

    Permitted inference geo values. Defaults to 'unrestricted' if omitted, which allows all geos. Use the string 'unrestricted' to allow all geos, or a list of specific geos.

    - `List[AllowedInferenceGeo]`

      - `"global"`

      - `"us"`

    - `"unrestricted"`

  - `default_inference_geo: Optional[Literal["global", "us"]]`

    Default inference geo applied when requests omit the parameter. Defaults to 'global' if omitted. Must be a member of `allowed_inference_geos` unless `allowed_inference_geos` is `"unrestricted"`.

    - `"global"`

    - `"us"`

  - `workspace_geo: Optional[Literal["us"]]`

    Geographic region for workspace data storage. Immutable after creation. Defaults to 'us' if omitted.

- `display_color: Optional[str]`

  Hex color code representing the Workspace in the Anthropic Console.

  maxLength: 7, pattern: ^#[0-9A-Fa-f]{6}$

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

- `tags: Optional[Dict[str, str]]`

  User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

- `user_profile_id: Optional[str]`

  ID of a user profile to attach to the Workspace. Every inference request through the Workspace must then name this user profile; the API rejects a request that names none or a different one. The user profile can't be replaced or removed later; only deleting the user profile clears it.

### Returns

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

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace = client.organization.workspaces.create(
    name="x",
)
print(workspace.id)
```

#### Response (200)

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

## Get Workspace

`organization.workspaces.retrieve(workspace_id) -> Workspace`

**GET** `/v1/organizations/workspaces/{workspace_id}`

Get Workspace

### Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

### Returns

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

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace = client.organization.workspaces.retrieve(
    "workspace_id",
)
print(workspace.id)
```

#### Response (200)

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

## Update Workspace

`organization.workspaces.update(workspace_id, **kwargs) -> Workspace`

**POST** `/v1/organizations/workspaces/{workspace_id}`

Update Workspace

### Parameters

- `workspace_id: str` (path parameter)

- `data_residency: Optional[DataResidencyUpdateConfigParam]`

  Data residency configuration for the workspace.

  - `allowed_inference_geos: Optional[Union[List[AllowedInferenceGeo], Literal["unrestricted"], null]]`

    Permitted inference geo values. Use 'unrestricted' to allow all geos, or a list of specific geos.

    - `List[AllowedInferenceGeo]`

      - `"global"`

      - `"us"`

    - `"unrestricted"`

  - `default_inference_geo: Optional[Literal["global", "us"]]`

    Default inference geo applied when requests omit the parameter. Must be a member of `allowed_inference_geos` unless `allowed_inference_geos` is `"unrestricted"`.

    - `"global"`

    - `"us"`

- `display_color: Optional[str]`

  Hex color code representing the Workspace in the Anthropic Console.

  maxLength: 7, pattern: ^#[0-9A-Fa-f]{6}$

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

- `name: Optional[str]`

  Name of the Workspace.

  minLength: 1, maxLength: 255

- `tags: Optional[Dict[str, Optional[str]]]`

  User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

- `user_profile_id: Optional[str]`

  ID of a user profile to attach to the Workspace. Every inference request through the Workspace must then name this user profile; the API rejects a request that names none or a different one. Once set, it can't be replaced or removed (sending the same ID again changes nothing); only deleting the user profile clears it. The default Workspace can't have a user profile.

### Returns

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

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace = client.organization.workspaces.update(
    workspace_id="workspace_id",
)
print(workspace.id)
```

#### Response (200)

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

## Archive Workspace

`organization.workspaces.archive(workspace_id) -> Workspace`

**POST** `/v1/organizations/workspaces/{workspace_id}/archive`

Archive Workspace

### Parameters

- `workspace_id: str` (path parameter)

### Returns

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

### Example

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

#### Response (200)

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

## Domain types

### Allowed Inference Geo

- `type AllowedInferenceGeo = Literal["global", "us"]`

  - `"global"`

  - `"us"`

### Data Residency

- `class DataResidency`

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

### Data Residency Create Config

- `class DataResidencyCreateConfigParam`

  - `allowed_inference_geos: Optional[Union[List[AllowedInferenceGeo], Literal["unrestricted"], null]]`

    Permitted inference geo values. Defaults to 'unrestricted' if omitted, which allows all geos. Use the string 'unrestricted' to allow all geos, or a list of specific geos.

    - `List[AllowedInferenceGeo]`

      - `"global"`

      - `"us"`

    - `"unrestricted"`

  - `default_inference_geo: Optional[Literal["global", "us"]]`

    Default inference geo applied when requests omit the parameter. Defaults to 'global' if omitted. Must be a member of `allowed_inference_geos` unless `allowed_inference_geos` is `"unrestricted"`.

    - `"global"`

    - `"us"`

  - `workspace_geo: Optional[Literal["us"]]`

    Geographic region for workspace data storage. Immutable after creation. Defaults to 'us' if omitted.

### Data Residency Update Config

- `class DataResidencyUpdateConfigParam`

  - `allowed_inference_geos: Optional[Union[List[AllowedInferenceGeo], Literal["unrestricted"], null]]`

    Permitted inference geo values. Use 'unrestricted' to allow all geos, or a list of specific geos.

    - `List[AllowedInferenceGeo]`

      - `"global"`

      - `"us"`

    - `"unrestricted"`

  - `default_inference_geo: Optional[Literal["global", "us"]]`

    Default inference geo applied when requests omit the parameter. Must be a member of `allowed_inference_geos` unless `allowed_inference_geos` is `"unrestricted"`.

    - `"global"`

    - `"us"`

### Key Profile Mismatch Error Details

- `class KeyProfileMismatchErrorDetails`

  The External Key is bound to a user profile, and the Workspace does not have that user profile. A Workspace can use only a key bound to its own user profile or a key that isn't bound to one.

  - `error_code: Literal["key_profile_mismatch"]`

### No Billing Workspace Role

- `type NoBillingWorkspaceRole = Literal["workspace_admin", "workspace_developer", "workspace_restricted_developer", "workspace_user"]`

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

### Workspace

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

### Workspace Member

- `class WorkspaceMember`

  - `type: Literal["workspace_member"]`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    default: workspace_member

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

  - `workspace_role: WorkspaceRole`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

### Workspace Member Limit Exceeded Error Details

- `class WorkspaceMemberLimitExceededErrorDetails`

  The workspace has reached the member limit that Anthropic set for it.

  - `error_code: Literal["workspace_member_limit_exceeded"]`

### Workspace Policy Field

- `type WorkspacePolicyField = Literal["external_key_id"]`

### Workspace Policy Violation Error Details

- `class WorkspacePolicyViolationErrorDetails`

  The request breaks the organization's Workspace Policy. The message says which rule it broke; an organization admin can see and change the policy in the Console.

  - `error_code: Literal["workspace_policy_violation"]`

  - `field: WorkspacePolicyField`

    The request field the broken rule applies to.

### Workspace Role

- `type WorkspaceRole = Literal["workspace_admin", "workspace_billing", "workspace_developer", 2 more]`

  - `"workspace_admin"`

  - `"workspace_billing"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

## Workspaces › Rate Limits

### List Workspace Rate Limits

`organization.workspaces.rate_limits.list(workspace_id, **kwargs) -> SyncPageCursor[WorkspaceRateLimit]`

**GET** `/v1/organizations/workspaces/{workspace_id}/rate_limits`

List a workspace's rate limits.

By default, returns only the groups and limiter types that have a
workspace-level override. With `include_inherited=true`, returns every
group with organization-level limits the workspace can see, listing for
each the values it inherits from the organization as well as its own
overrides. Each value's `source` says which it is.

When `limit` is omitted, every matching entry is returned in a single
page; when `limit` truncates the result, follow `next_page` to fetch
the remaining entries.

#### Parameters

- `workspace_id: str` (path parameter)

  The ID of the workspace.

- `group_type: Optional[Literal["batch", "files", "model_group", 3 more]]` (query parameter)

  Filter by group type.

  - `"batch"`

  - `"files"`

  - `"model_group"`

  - `"skills"`

  - `"token_count"`

  - `"web_search"`

- `include_inherited: Optional[bool]` (query parameter)

  Also list the limiter values the workspace inherits from the organization, including groups with no workspace-level override.

  default: false

- `limit: Optional[int]` (query parameter)

  Maximum number of items to return per page. Ranges from `1` to `1000`.

  When omitted, every remaining entry is returned in a single page and `next_page` is `null`.

  minimum: 1, maximum: 1000

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `class WorkspaceRateLimit`

  - `type: Literal["workspace_rate_limit"]`

    Object type. Always `workspace_rate_limit` for workspace rate-limit entries.

    default: workspace_rate_limit

  - `group: Group`

    The rate-limit group this entry's limits apply to.

    - `class OrganizationRateLimitModelGroup`

      - `type: Literal["model_group"]`

        Always `model_group`: a family of models.

        default: model_group

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `display_name: str`

        Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

    - `class OrganizationRateLimitBatchGroup`

      - `type: Literal["batch"]`

        Always `batch`: the Message Batches API.

        default: batch

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitTokenCountGroup`

      - `type: Literal["token_count"]`

        Always `token_count`: the Token Count API.

        default: token_count

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitFilesGroup`

      - `type: Literal["files"]`

        Always `files`: the Files API.

        default: files

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitSkillsGroup`

      - `type: Literal["skills"]`

        Always `skills`: the Skills API.

        default: skills

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitWebSearchGroup`

      - `type: Literal["web_search"]`

        Always `web_search`: the Messages API web search tool.

        default: web_search

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

  - `limits: List[WorkspaceRateLimitValue]`

    The workspace's limiter values for this group. By default only the limiter types with a workspace-level override are listed. With `include_inherited` set to `true`, the limiter types the workspace inherits from the organization are listed too, each marked by `source`.

    - `type: str`

      The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

    - `org_limit: Optional[int]`

      The organization-level value for the same limiter type, for reference. `null` when the organization has no limit configured for this limiter type.

    - `source: Source`

      Where `value` comes from. `organization` values are listed only when `include_inherited` is `true`, and then `value` equals `org_limit`.

      - `class WorkspaceRateLimitWorkspaceSource`

        - `type: Literal["workspace"]`

          Always `workspace`: a workspace-level override is stored.

          default: workspace

      - `class WorkspaceRateLimitOrganizationSource`

        - `type: Literal["organization"]`

          Always `organization`: no workspace-level override is stored, so the organization's value applies.

          default: organization

    - `value: int`

      The workspace's value for this limiter type: the workspace-level override when `source.type` is `workspace`, otherwise the organization's value.

  - `models: Optional[List[str]]`

    Model names this entry's limits apply to, including aliases. `null` when `group.type` is not `"model_group"`. The list covers the models this workspace has access to, so it can differ between workspaces.

  - `rate_limit_id: str`

    The `id` of the organization's RateLimit entry this entry applies to.

  - `workspace_id: str`

    ID of the Workspace this entry applies to.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.workspaces.rate_limits.list(
    workspace_id="workspace_id",
)
page = page.data[0]
print(page.rate_limit_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "group": {
        "id": "id",
        "display_name": "display_name",
        "type": "model_group"
      },
      "limits": [
        {
          "org_limit": 0,
          "source": {
            "type": "workspace"
          },
          "type": "type",
          "value": 0
        }
      ],
      "models": [
        "string"
      ],
      "rate_limit_id": "rate_limit_id",
      "type": "workspace_rate_limit",
      "workspace_id": "workspace_id"
    }
  ],
  "next_page": "next_page"
}
```

### Set Workspace Rate Limits

`organization.workspaces.rate_limits.update(rate_limit_id, **kwargs) -> WorkspaceRateLimit`

**POST** `/v1/organizations/workspaces/{workspace_id}/rate_limits/{rate_limit_id}`

Set or clear rate-limit overrides for one rate-limit group in a workspace.

Only the limiter types named in `limits` change: an integer `value` sets
that type's override and `null` clears it. Types not named keep their
current value. A value above the organization's own limit is stored, but
the organization limit still applies, so the lower of the two is
enforced.

Returns the targeted group's entry with this request applied, in the shape
`GET /v1/organizations/workspaces/{workspace_id}/rate_limits` returns.
Changes take effect within about an hour.

#### Parameters

- `workspace_id: str` (path parameter)

  The ID of the workspace.

- `rate_limit_id: str` (path parameter)

  The `id` of the organization's rate-limit entry to set overrides for.

- `limits: Iterable[WorkspaceRateLimitUpdateValueParam]`

  Limits to set or clear. Unspecified limit types are unchanged.

  minItems: 1, maxItems: 16

  - `type: WorkspaceRateLimitType`

    Rate limiter type.

    - `"fast_itpmca"`

    - `"fast_otpm"`

    - `"input_tokens_per_minute"`

    - `"input_tokens_per_minute_cache_aware"`

    - `"output_tokens_per_minute"`

    - `"requests_per_minute"`

    - `"tokens_per_day"`

    - `"tokens_per_minute"`

    - `"tool_uses_per_second"`

  - `value: Optional[int]`

    New limit value. Set to null to clear the workspace override and fall back to the organization limit.

    minimum: 0, maximum: 9007199254740991

#### Returns

- `class WorkspaceRateLimit`

  - `type: Literal["workspace_rate_limit"]`

    Object type. Always `workspace_rate_limit` for workspace rate-limit entries.

    default: workspace_rate_limit

  - `group: Group`

    The rate-limit group this entry's limits apply to.

    - `class OrganizationRateLimitModelGroup`

      - `type: Literal["model_group"]`

        Always `model_group`: a family of models.

        default: model_group

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `display_name: str`

        Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

    - `class OrganizationRateLimitBatchGroup`

      - `type: Literal["batch"]`

        Always `batch`: the Message Batches API.

        default: batch

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitTokenCountGroup`

      - `type: Literal["token_count"]`

        Always `token_count`: the Token Count API.

        default: token_count

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitFilesGroup`

      - `type: Literal["files"]`

        Always `files`: the Files API.

        default: files

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitSkillsGroup`

      - `type: Literal["skills"]`

        Always `skills`: the Skills API.

        default: skills

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `class OrganizationRateLimitWebSearchGroup`

      - `type: Literal["web_search"]`

        Always `web_search`: the Messages API web search tool.

        default: web_search

      - `id: str`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

  - `limits: List[WorkspaceRateLimitValue]`

    The workspace's limiter values for this group. By default only the limiter types with a workspace-level override are listed. With `include_inherited` set to `true`, the limiter types the workspace inherits from the organization are listed too, each marked by `source`.

    - `type: str`

      The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

    - `org_limit: Optional[int]`

      The organization-level value for the same limiter type, for reference. `null` when the organization has no limit configured for this limiter type.

    - `source: Source`

      Where `value` comes from. `organization` values are listed only when `include_inherited` is `true`, and then `value` equals `org_limit`.

      - `class WorkspaceRateLimitWorkspaceSource`

        - `type: Literal["workspace"]`

          Always `workspace`: a workspace-level override is stored.

          default: workspace

      - `class WorkspaceRateLimitOrganizationSource`

        - `type: Literal["organization"]`

          Always `organization`: no workspace-level override is stored, so the organization's value applies.

          default: organization

    - `value: int`

      The workspace's value for this limiter type: the workspace-level override when `source.type` is `workspace`, otherwise the organization's value.

  - `models: Optional[List[str]]`

    Model names this entry's limits apply to, including aliases. `null` when `group.type` is not `"model_group"`. The list covers the models this workspace has access to, so it can differ between workspaces.

  - `rate_limit_id: str`

    The `id` of the organization's RateLimit entry this entry applies to.

  - `workspace_id: str`

    ID of the Workspace this entry applies to.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace_rate_limit = client.organization.workspaces.rate_limits.update(
    rate_limit_id="rate_limit_id",
    workspace_id="workspace_id",
    limits=[
        {
            "type": "fast_itpmca",
            "value": 0,
        }
    ],
)
print(workspace_rate_limit.rate_limit_id)
```

##### Response (200)

```json
{
  "group": {
    "id": "id",
    "display_name": "display_name",
    "type": "model_group"
  },
  "limits": [
    {
      "org_limit": 0,
      "source": {
        "type": "workspace"
      },
      "type": "type",
      "value": 0
    }
  ],
  "models": [
    "string"
  ],
  "rate_limit_id": "rate_limit_id",
  "type": "workspace_rate_limit",
  "workspace_id": "workspace_id"
}
```

## Workspaces › Members

### List Workspace Members

`organization.workspaces.members.list(workspace_id, **kwargs) -> SyncPage[WorkspaceMember]`

**GET** `/v1/organizations/workspaces/{workspace_id}/members`

List Workspace Members

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `after_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: Optional[str]` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `limit: Optional[int]` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  default: 20, minimum: 1, maximum: 1000

#### Returns

- `class WorkspaceMember`

  - `type: Literal["workspace_member"]`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    default: workspace_member

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

  - `workspace_role: WorkspaceRole`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.workspaces.members.list(
    workspace_id="workspace_id",
)
page = page.data[0]
print(page.user_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "type": "workspace_member",
      "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
      "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      "workspace_role": "workspace_admin"
    }
  ],
  "first_id": "first_id",
  "has_more": true,
  "last_id": "last_id"
}
```

### Create Workspace Member

`organization.workspaces.members.add(workspace_id, **kwargs) -> WorkspaceMember`

**POST** `/v1/organizations/workspaces/{workspace_id}/members`

Create Workspace Member

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `user_id: str`

  ID of the User.

- `workspace_role: NoBillingWorkspaceRole`

  Role of the new Workspace Member. Cannot be `workspace_billing`.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `class WorkspaceMember`

  - `type: Literal["workspace_member"]`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    default: workspace_member

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

  - `workspace_role: WorkspaceRole`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace_member = client.organization.workspaces.members.add(
    workspace_id="workspace_id",
    user_id="user_01WxYzAbCdEfGhJkMnPqRsTu",
    workspace_role="workspace_admin",
)
print(workspace_member.user_id)
```

##### Response (200)

```json
{
  "type": "workspace_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "workspace_role": "workspace_admin"
}
```

### Get Workspace Member

`organization.workspaces.members.retrieve(user_id, **kwargs) -> WorkspaceMember`

**GET** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Get Workspace Member

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `user_id: str` (path parameter)

  ID of the User.

#### Returns

- `class WorkspaceMember`

  - `type: Literal["workspace_member"]`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    default: workspace_member

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

  - `workspace_role: WorkspaceRole`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace_member = client.organization.workspaces.members.retrieve(
    user_id="user_id",
    workspace_id="workspace_id",
)
print(workspace_member.user_id)
```

##### Response (200)

```json
{
  "type": "workspace_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "workspace_role": "workspace_admin"
}
```

### Update Workspace Member

`organization.workspaces.members.update(user_id, **kwargs) -> WorkspaceMember`

**POST** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Update Workspace Member

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `user_id: str` (path parameter)

  ID of the User.

- `workspace_role: WorkspaceRole`

  New workspace role for the User.

  - `"workspace_admin"`

  - `"workspace_billing"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `class WorkspaceMember`

  - `type: Literal["workspace_member"]`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    default: workspace_member

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

  - `workspace_role: WorkspaceRole`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
workspace_member = client.organization.workspaces.members.update(
    user_id="user_id",
    workspace_id="workspace_id",
    workspace_role="workspace_admin",
)
print(workspace_member.user_id)
```

##### Response (200)

```json
{
  "type": "workspace_member",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "workspace_role": "workspace_admin"
}
```

### Delete Workspace Member

`organization.workspaces.members.remove(user_id, **kwargs) -> MemberRemoveResponse`

**DELETE** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Delete Workspace Member

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the Workspace.

- `user_id: str` (path parameter)

  ID of the User.

#### Returns

- `class MemberRemoveResponse`

  - `type: Literal["workspace_member_deleted"]`

    Deleted object type.

    For Workspace Members, this is always `"workspace_member_deleted"`.

    default: workspace_member_deleted

  - `user_id: str`

    ID of the User.

  - `workspace_id: str`

    ID of the Workspace.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
member = client.organization.workspaces.members.remove(
    user_id="user_id",
    workspace_id="workspace_id",
)
print(member.user_id)
```

##### Response (200)

```json
{
  "type": "workspace_member_deleted",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
}
```

## Workspaces › Service Accounts

### List Service Account Workspace Members

`organization.workspaces.service_accounts.list(workspace_id, **kwargs) -> SyncPageCursor[ServiceAccountWorkspaceMember]`

**GET** `/v1/organizations/workspaces/{workspace_id}/service_accounts`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

List the service accounts that are members of a workspace.

Each entry includes the service account's `workspace_role`. Use `limit`
and the `next_page` cursor to paginate. Archived workspaces return 400;
use `GET /service_accounts/{id}/workspaces` to audit memberships of an
archived workspace. The implicit default-workspace membership is not
included in this list. Memberships of archived service accounts are
omitted from the results.

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the workspace.

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `class ServiceAccountWorkspaceMember`

  - `type: Literal["service_account_workspace_member"]`

    default: service_account_workspace_member

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: Optional[bool]`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: str`

    Tagged service account ID (`svac_...`).

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: WorkspaceRole`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.organization.workspaces.service_accounts.list(
    workspace_id="workspace_id",
)
page = page.data[0]
print(page.created_by_actor_id)
```

##### Response (200)

```json
{
  "data": [
    {
      "created_by_actor_id": "created_by_actor_id",
      "implicit": true,
      "service_account_id": "service_account_id",
      "type": "service_account_workspace_member",
      "workspace_id": "workspace_id",
      "workspace_role": "workspace_admin"
    }
  ],
  "next_page": "next_page"
}
```

### Create Service Account Workspace Member

`organization.workspaces.service_accounts.add(workspace_id, **kwargs) -> ServiceAccountWorkspaceMember`

**POST** `/v1/organizations/workspaces/{workspace_id}/service_accounts`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Add a service account to a workspace with the given `workspace_role`.

The role determines what the service account can do in the workspace and
which workspace-scoped permissions it can be granted when authenticating
through federation. Every service account is already an implicit
`workspace_user` member of the default workspace; adding it explicitly
assigns a chosen role. If the service account is already an explicit
member of the workspace, its `workspace_role` is replaced with the
value supplied here. Archived workspaces return 400. Archived service
accounts cannot be added and are rejected.

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the workspace.

- `service_account_id: str`

  Tagged service account ID to add.

- `workspace_role: NoBillingWorkspaceRole`

  Role to assign to the service account in this workspace.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `class ServiceAccountWorkspaceMember`

  - `type: Literal["service_account_workspace_member"]`

    default: service_account_workspace_member

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: Optional[bool]`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: str`

    Tagged service account ID (`svac_...`).

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: WorkspaceRole`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account_workspace_member = client.organization.workspaces.service_accounts.add(
    workspace_id="workspace_id",
    service_account_id="service_account_id",
    workspace_role="workspace_admin",
)
print(service_account_workspace_member.created_by_actor_id)
```

##### Response (200)

```json
{
  "created_by_actor_id": "created_by_actor_id",
  "implicit": true,
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member",
  "workspace_id": "workspace_id",
  "workspace_role": "workspace_admin"
}
```

### Get Service Account Workspace Member

`organization.workspaces.service_accounts.retrieve(service_account_id, **kwargs) -> ServiceAccountWorkspaceMember`

**GET** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Retrieve a service account's membership in a workspace.

Returns the membership record, including the service account's
`workspace_role` in this workspace. Archived workspaces return 400. For
the default workspace, returns the implicit (`implicit: true`)
membership when no explicit membership exists; an explicitly added
membership is returned with its assigned role. An archived service
account returns 404.

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the workspace.

- `service_account_id: str` (path parameter)

  ID of the service account.

#### Returns

- `class ServiceAccountWorkspaceMember`

  - `type: Literal["service_account_workspace_member"]`

    default: service_account_workspace_member

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: Optional[bool]`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: str`

    Tagged service account ID (`svac_...`).

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: WorkspaceRole`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account_workspace_member = (
    client.organization.workspaces.service_accounts.retrieve(
        service_account_id="service_account_id",
        workspace_id="workspace_id",
    )
)
print(service_account_workspace_member.created_by_actor_id)
```

##### Response (200)

```json
{
  "created_by_actor_id": "created_by_actor_id",
  "implicit": true,
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member",
  "workspace_id": "workspace_id",
  "workspace_role": "workspace_admin"
}
```

### Update Service Account Workspace Member

`organization.workspaces.service_accounts.update(service_account_id, **kwargs) -> ServiceAccountWorkspaceMember`

**POST** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Change a service account's role in a workspace.

The new `workspace_role` replaces the current one. Only explicit
memberships can be updated; to set a role on the implicit
default-workspace membership, add the service account explicitly with
`POST /workspaces/{workspace_id}/service_accounts`. Archived workspaces
return 400. Archived service accounts cannot be updated and are
rejected.

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the workspace.

- `service_account_id: str` (path parameter)

  ID of the service account.

- `workspace_role: NoBillingWorkspaceRole`

  New role for the service account in this workspace.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `class ServiceAccountWorkspaceMember`

  - `type: Literal["service_account_workspace_member"]`

    default: service_account_workspace_member

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: Optional[bool]`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: str`

    Tagged service account ID (`svac_...`).

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: WorkspaceRole`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account_workspace_member = (
    client.organization.workspaces.service_accounts.update(
        service_account_id="service_account_id",
        workspace_id="workspace_id",
        workspace_role="workspace_admin",
    )
)
print(service_account_workspace_member.created_by_actor_id)
```

##### Response (200)

```json
{
  "created_by_actor_id": "created_by_actor_id",
  "implicit": true,
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member",
  "workspace_id": "workspace_id",
  "workspace_role": "workspace_admin"
}
```

### Delete Service Account Workspace Member

`organization.workspaces.service_accounts.remove(service_account_id, **kwargs) -> ServiceAccountRemoveResponse`

**DELETE** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Remove a service account from a workspace.

Removal is idempotent (returns 200 even if the membership was already
removed). A DELETE against the implicit default-workspace membership
returns 200 but is a no-op and the membership persists; deleting an
explicit default-workspace row reverts to the implicit `workspace_user`
membership. Archived workspaces return 400.

#### Parameters

- `workspace_id: str` (path parameter)

  ID of the workspace.

- `service_account_id: str` (path parameter)

  ID of the service account.

#### Returns

- `class ServiceAccountRemoveResponse`

  - `type: Literal["service_account_workspace_member_deleted"]`

    default: service_account_workspace_member_deleted

  - `service_account_id: str`

    Tagged service account ID (`svac_...`) named in the delete request. Removal is idempotent; see the endpoint description for the implicit-membership no-op.

  - `workspace_id: str`

    Tagged workspace ID (`wrkspc_...`) named in the delete request.

#### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
service_account = client.organization.workspaces.service_accounts.remove(
    service_account_id="service_account_id",
    workspace_id="workspace_id",
)
print(service_account.service_account_id)
```

##### Response (200)

```json
{
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member_deleted",
  "workspace_id": "workspace_id"
}
```
