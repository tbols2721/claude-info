---
title: Workspaces
url: https://platform.claude.com/docs/en/api/cli/organization/workspaces
---

# Workspaces

## List Workspaces

`$ ant organization:workspaces list`

**GET** `/v1/organizations/workspaces`

List Workspaces

### Parameters

- `--after-id: optional string` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `--before-id: optional string` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `--include-archived: optional boolean` (query parameter)

  Whether to include Workspaces that have been archived in the response

- `--include-default: optional boolean` (query parameter)

  Whether to include the organization's default Workspace in the response

- `--limit: optional number` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  minimum: 1, maximum: 1000

### Returns

- `ListResponse_Workspace_: object`

  - `data: array of Workspace`

    - `type: "workspace"`

      Object type.

      For Workspaces, this is always `"workspace"`.

    - `id: string`

      ID of the Workspace.

    - `archived_at: string`

      RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

      format: date-time

    - `compartment_id: string`

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

    - `created_at: string`

      RFC 3339 datetime string indicating when the Workspace was created.

      format: date-time

    - `data_residency: object`

      Data residency configuration.

      - `allowed_inference_geos: array of AllowedInferenceGeo or "unrestricted"`

        Permitted inference geo values. 'unrestricted' means all geos are allowed.

        - `geos: array of AllowedInferenceGeo`

          - `"global"`

          - `"us"`

        - `unrestricted: "unrestricted"`

      - `default_inference_geo: "global" or "us"`

        Default inference geo applied when requests omit the parameter.

        - `"global"`

        - `"us"`

      - `workspace_geo: "us"`

        Geographic region for workspace data storage. Immutable after creation.

    - `display_color: string`

      Hex color code representing the Workspace in the Anthropic Console.

    - `external_key_id: string`

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

    - `name: string`

      Name of the Workspace.

    - `tags: map[string]`

      User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

    - `user_profile_id: string`

      ID of the user profile attached to the Workspace, or null if it has none. Every inference request through a Workspace that has a user profile must name that profile.

  - `first_id: string`

    First ID in the `data` list. Can be used as the `before_id` for the previous page.

  - `has_more: boolean`

    Indicates if there are more results in the requested page direction.

  - `last_id: string`

    Last ID in the `data` list. Can be used as the `after_id` for the next page.

### Example

```bash
ant organization:workspaces list
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

`$ ant organization:workspaces create`

**POST** `/v1/organizations/workspaces`

Create Workspace

### Parameters

- `--name: string`

  Name of the Workspace.

  minLength: 1, maxLength: 255

- `--data-residency: optional DataResidencyCreateConfig`

  Data residency configuration for the workspace. If omitted, defaults to `workspace_geo: "us"`, `allowed_inference_geos: "unrestricted"`, and `default_inference_geo: "global"`.

  - `allowed_inference_geos: optional array of AllowedInferenceGeo or "unrestricted"`

    Permitted inference geo values. Defaults to 'unrestricted' if omitted, which allows all geos. Use the string 'unrestricted' to allow all geos, or a list of specific geos.

    - `geos: array of AllowedInferenceGeo`

      - `"global"`

      - `"us"`

    - `unrestricted: "unrestricted"`

  - `default_inference_geo: optional "global" or "us"`

    Default inference geo applied when requests omit the parameter. Defaults to 'global' if omitted. Must be a member of `allowed_inference_geos` unless `allowed_inference_geos` is `"unrestricted"`.

    - `"global"`

    - `"us"`

  - `workspace_geo: optional "us"`

    Geographic region for workspace data storage. Immutable after creation. Defaults to 'us' if omitted.

- `--display-color: optional string`

  Hex color code representing the Workspace in the Anthropic Console.

  maxLength: 7, pattern: ^#[0-9A-Fa-f]{6}$

- `--external-key-id: optional string`

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

- `--tags: optional map[string]`

  User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

- `--user-profile-id: optional string`

  ID of a user profile to attach to the Workspace. Every inference request through the Workspace must then name this user profile; the API rejects a request that names none or a different one. The user profile can't be replaced or removed later; only deleting the user profile clears it.

### Returns

- `workspace: object`

  - `type: "workspace"`

    Object type.

    For Workspaces, this is always `"workspace"`.

  - `id: string`

    ID of the Workspace.

  - `archived_at: string`

    RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

    format: date-time

  - `compartment_id: string`

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

  - `created_at: string`

    RFC 3339 datetime string indicating when the Workspace was created.

    format: date-time

  - `data_residency: object`

    Data residency configuration.

    - `allowed_inference_geos: array of AllowedInferenceGeo or "unrestricted"`

      Permitted inference geo values. 'unrestricted' means all geos are allowed.

      - `geos: array of AllowedInferenceGeo`

        - `"global"`

        - `"us"`

      - `unrestricted: "unrestricted"`

    - `default_inference_geo: "global" or "us"`

      Default inference geo applied when requests omit the parameter.

      - `"global"`

      - `"us"`

    - `workspace_geo: "us"`

      Geographic region for workspace data storage. Immutable after creation.

  - `display_color: string`

    Hex color code representing the Workspace in the Anthropic Console.

  - `external_key_id: string`

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

  - `name: string`

    Name of the Workspace.

  - `tags: map[string]`

    User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

  - `user_profile_id: string`

    ID of the user profile attached to the Workspace, or null if it has none. Every inference request through a Workspace that has a user profile must name that profile.

### Example

```bash
ant organization:workspaces create \
  --name x
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

`$ ant organization:workspaces retrieve`

**GET** `/v1/organizations/workspaces/{workspace_id}`

Get Workspace

### Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

### Returns

- `workspace: object`

  - `type: "workspace"`

    Object type.

    For Workspaces, this is always `"workspace"`.

  - `id: string`

    ID of the Workspace.

  - `archived_at: string`

    RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

    format: date-time

  - `compartment_id: string`

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

  - `created_at: string`

    RFC 3339 datetime string indicating when the Workspace was created.

    format: date-time

  - `data_residency: object`

    Data residency configuration.

    - `allowed_inference_geos: array of AllowedInferenceGeo or "unrestricted"`

      Permitted inference geo values. 'unrestricted' means all geos are allowed.

      - `geos: array of AllowedInferenceGeo`

        - `"global"`

        - `"us"`

      - `unrestricted: "unrestricted"`

    - `default_inference_geo: "global" or "us"`

      Default inference geo applied when requests omit the parameter.

      - `"global"`

      - `"us"`

    - `workspace_geo: "us"`

      Geographic region for workspace data storage. Immutable after creation.

  - `display_color: string`

    Hex color code representing the Workspace in the Anthropic Console.

  - `external_key_id: string`

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

  - `name: string`

    Name of the Workspace.

  - `tags: map[string]`

    User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

  - `user_profile_id: string`

    ID of the user profile attached to the Workspace, or null if it has none. Every inference request through a Workspace that has a user profile must name that profile.

### Example

```bash
ant organization:workspaces retrieve \
  --workspace-id workspace_id
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

`$ ant organization:workspaces update`

**POST** `/v1/organizations/workspaces/{workspace_id}`

Update Workspace

### Parameters

- `--workspace-id: string` (path parameter)

- `--data-residency: optional DataResidencyUpdateConfig`

  Data residency configuration for the workspace.

  - `allowed_inference_geos: optional array of AllowedInferenceGeo or "unrestricted"`

    Permitted inference geo values. Use 'unrestricted' to allow all geos, or a list of specific geos.

    - `geos: array of AllowedInferenceGeo`

      - `"global"`

      - `"us"`

    - `unrestricted: "unrestricted"`

  - `default_inference_geo: optional "global" or "us"`

    Default inference geo applied when requests omit the parameter. Must be a member of `allowed_inference_geos` unless `allowed_inference_geos` is `"unrestricted"`.

    - `"global"`

    - `"us"`

- `--display-color: optional string`

  Hex color code representing the Workspace in the Anthropic Console.

  maxLength: 7, pattern: ^#[0-9A-Fa-f]{6}$

- `--external-key-id: optional string`

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

- `--name: optional string`

  Name of the Workspace.

  minLength: 1, maxLength: 255

- `--tags: optional map[string]`

  User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

- `--user-profile-id: optional string`

  ID of a user profile to attach to the Workspace. Every inference request through the Workspace must then name this user profile; the API rejects a request that names none or a different one. Once set, it can't be replaced or removed (sending the same ID again changes nothing); only deleting the user profile clears it. The default Workspace can't have a user profile.

### Returns

- `workspace: object`

  - `type: "workspace"`

    Object type.

    For Workspaces, this is always `"workspace"`.

  - `id: string`

    ID of the Workspace.

  - `archived_at: string`

    RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

    format: date-time

  - `compartment_id: string`

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

  - `created_at: string`

    RFC 3339 datetime string indicating when the Workspace was created.

    format: date-time

  - `data_residency: object`

    Data residency configuration.

    - `allowed_inference_geos: array of AllowedInferenceGeo or "unrestricted"`

      Permitted inference geo values. 'unrestricted' means all geos are allowed.

      - `geos: array of AllowedInferenceGeo`

        - `"global"`

        - `"us"`

      - `unrestricted: "unrestricted"`

    - `default_inference_geo: "global" or "us"`

      Default inference geo applied when requests omit the parameter.

      - `"global"`

      - `"us"`

    - `workspace_geo: "us"`

      Geographic region for workspace data storage. Immutable after creation.

  - `display_color: string`

    Hex color code representing the Workspace in the Anthropic Console.

  - `external_key_id: string`

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

  - `name: string`

    Name of the Workspace.

  - `tags: map[string]`

    User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

  - `user_profile_id: string`

    ID of the user profile attached to the Workspace, or null if it has none. Every inference request through a Workspace that has a user profile must name that profile.

### Example

```bash
ant organization:workspaces update \
  --workspace-id workspace_id
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

`$ ant organization:workspaces archive`

**POST** `/v1/organizations/workspaces/{workspace_id}/archive`

Archive Workspace

### Parameters

- `--workspace-id: string` (path parameter)

### Returns

- `workspace: object`

  - `type: "workspace"`

    Object type.

    For Workspaces, this is always `"workspace"`.

  - `id: string`

    ID of the Workspace.

  - `archived_at: string`

    RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

    format: date-time

  - `compartment_id: string`

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

  - `created_at: string`

    RFC 3339 datetime string indicating when the Workspace was created.

    format: date-time

  - `data_residency: object`

    Data residency configuration.

    - `allowed_inference_geos: array of AllowedInferenceGeo or "unrestricted"`

      Permitted inference geo values. 'unrestricted' means all geos are allowed.

      - `geos: array of AllowedInferenceGeo`

        - `"global"`

        - `"us"`

      - `unrestricted: "unrestricted"`

    - `default_inference_geo: "global" or "us"`

      Default inference geo applied when requests omit the parameter.

      - `"global"`

      - `"us"`

    - `workspace_geo: "us"`

      Geographic region for workspace data storage. Immutable after creation.

  - `display_color: string`

    Hex color code representing the Workspace in the Anthropic Console.

  - `external_key_id: string`

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

  - `name: string`

    Name of the Workspace.

  - `tags: map[string]`

    User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

  - `user_profile_id: string`

    ID of the user profile attached to the Workspace, or null if it has none. Every inference request through a Workspace that has a user profile must name that profile.

### Example

```bash
ant organization:workspaces archive \
  --workspace-id workspace_id
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

- `allowed_inference_geo: "global" or "us"`

  - `"global"`

  - `"us"`

### Data Residency

- `data_residency: object`

  - `allowed_inference_geos: array of AllowedInferenceGeo or "unrestricted"`

    Permitted inference geo values. 'unrestricted' means all geos are allowed.

    - `geos: array of AllowedInferenceGeo`

      - `"global"`

      - `"us"`

    - `unrestricted: "unrestricted"`

  - `default_inference_geo: "global" or "us"`

    Default inference geo applied when requests omit the parameter.

    - `"global"`

    - `"us"`

  - `workspace_geo: "us"`

    Geographic region for workspace data storage. Immutable after creation.

### Data Residency Create Config

- `data_residency_create_config: object`

  - `allowed_inference_geos: optional array of AllowedInferenceGeo or "unrestricted"`

    Permitted inference geo values. Defaults to 'unrestricted' if omitted, which allows all geos. Use the string 'unrestricted' to allow all geos, or a list of specific geos.

    - `geos: array of AllowedInferenceGeo`

      - `"global"`

      - `"us"`

    - `unrestricted: "unrestricted"`

  - `default_inference_geo: optional "global" or "us"`

    Default inference geo applied when requests omit the parameter. Defaults to 'global' if omitted. Must be a member of `allowed_inference_geos` unless `allowed_inference_geos` is `"unrestricted"`.

    - `"global"`

    - `"us"`

  - `workspace_geo: optional "us"`

    Geographic region for workspace data storage. Immutable after creation. Defaults to 'us' if omitted.

### Data Residency Update Config

- `data_residency_update_config: object`

  - `allowed_inference_geos: optional array of AllowedInferenceGeo or "unrestricted"`

    Permitted inference geo values. Use 'unrestricted' to allow all geos, or a list of specific geos.

    - `geos: array of AllowedInferenceGeo`

      - `"global"`

      - `"us"`

    - `unrestricted: "unrestricted"`

  - `default_inference_geo: optional "global" or "us"`

    Default inference geo applied when requests omit the parameter. Must be a member of `allowed_inference_geos` unless `allowed_inference_geos` is `"unrestricted"`.

    - `"global"`

    - `"us"`

### No Billing Workspace Role

- `no_billing_workspace_role: "workspace_admin" or "workspace_developer" or "workspace_restricted_developer" or "workspace_user"`

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

### Workspace

- `workspace: object`

  - `type: "workspace"`

    Object type.

    For Workspaces, this is always `"workspace"`.

  - `id: string`

    ID of the Workspace.

  - `archived_at: string`

    RFC 3339 datetime string indicating when the Workspace was archived, or `null` if the Workspace is not archived.

    format: date-time

  - `compartment_id: string`

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

  - `created_at: string`

    RFC 3339 datetime string indicating when the Workspace was created.

    format: date-time

  - `data_residency: object`

    Data residency configuration.

    - `allowed_inference_geos: array of AllowedInferenceGeo or "unrestricted"`

      Permitted inference geo values. 'unrestricted' means all geos are allowed.

      - `geos: array of AllowedInferenceGeo`

        - `"global"`

        - `"us"`

      - `unrestricted: "unrestricted"`

    - `default_inference_geo: "global" or "us"`

      Default inference geo applied when requests omit the parameter.

      - `"global"`

      - `"us"`

    - `workspace_geo: "us"`

      Geographic region for workspace data storage. Immutable after creation.

  - `display_color: string`

    Hex color code representing the Workspace in the Anthropic Console.

  - `external_key_id: string`

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

  - `name: string`

    Name of the Workspace.

  - `tags: map[string]`

    User-defined tags as string key-value pairs. Keys may not begin with `anthropic`.

  - `user_profile_id: string`

    ID of the user profile attached to the Workspace, or null if it has none. Every inference request through a Workspace that has a user profile must name that profile.

### Workspace Member

- `workspace_member: object`

  - `type: "workspace_member"`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

  - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

### Workspace Role

- `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

  - `"workspace_admin"`

  - `"workspace_billing"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

## Workspaces › Rate Limits

### List Workspace Rate Limits

`$ ant organization:workspaces:rate-limits list`

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

- `--workspace-id: string` (path parameter)

  The ID of the workspace.

- `--group-type: optional "batch" or "files" or "model_group" or 3 more` (query parameter)

  Filter by group type.

  - `"batch"`

  - `"files"`

  - `"model_group"`

  - `"skills"`

  - `"token_count"`

  - `"web_search"`

- `--include-inherited: optional boolean` (query parameter)

  Also list the limiter values the workspace inherits from the organization, including groups with no workspace-level override.

- `--limit: optional number` (query parameter)

  Maximum number of items to return per page. Ranges from `1` to `1000`.

  When omitted, every remaining entry is returned in a single page and `next_page` is `null`.

  minimum: 1, maximum: 1000

- `--page: optional string` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `WorkspaceRateLimitListResponse: object`

  - `data: array of WorkspaceRateLimit`

    Rate-limit entries for the workspace: one per group with at least one override, or, with `include_inherited` set to `true`, one per group the workspace can see that has organization-level limits.

    - `type: "workspace_rate_limit"`

      Object type. Always `workspace_rate_limit` for workspace rate-limit entries.

    - `group: OrganizationRateLimitModelGroup or OrganizationRateLimitBatchGroup or OrganizationRateLimitTokenCountGroup or 3 more`

      The rate-limit group this entry's limits apply to.

      - `organization_rate_limit_model_group: object`

        - `type: "model_group"`

          Always `model_group`: a family of models.

        - `id: string`

          Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

        - `display_name: string`

          Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

      - `organization_rate_limit_batch_group: object`

        - `type: "batch"`

          Always `batch`: the Message Batches API.

        - `id: string`

          Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `organization_rate_limit_token_count_group: object`

        - `type: "token_count"`

          Always `token_count`: the Token Count API.

        - `id: string`

          Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `organization_rate_limit_files_group: object`

        - `type: "files"`

          Always `files`: the Files API.

        - `id: string`

          Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `organization_rate_limit_skills_group: object`

        - `type: "skills"`

          Always `skills`: the Skills API.

        - `id: string`

          Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `organization_rate_limit_web_search_group: object`

        - `type: "web_search"`

          Always `web_search`: the Messages API web search tool.

        - `id: string`

          Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `limits: array of WorkspaceRateLimitValue`

      The workspace's limiter values for this group. By default only the limiter types with a workspace-level override are listed. With `include_inherited` set to `true`, the limiter types the workspace inherits from the organization are listed too, each marked by `source`.

      - `type: string`

        The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

      - `org_limit: number`

        The organization-level value for the same limiter type, for reference. `null` when the organization has no limit configured for this limiter type.

      - `source: WorkspaceRateLimitWorkspaceSource or WorkspaceRateLimitOrganizationSource`

        Where `value` comes from. `organization` values are listed only when `include_inherited` is `true`, and then `value` equals `org_limit`.

        - `workspace_rate_limit_workspace_source: object`

          - `type: "workspace"`

            Always `workspace`: a workspace-level override is stored.

        - `workspace_rate_limit_organization_source: object`

          - `type: "organization"`

            Always `organization`: no workspace-level override is stored, so the organization's value applies.

      - `value: number`

        The workspace's value for this limiter type: the workspace-level override when `source.type` is `workspace`, otherwise the organization's value.

    - `models: array of string`

      Model names this entry's limits apply to, including aliases. `null` when `group.type` is not `"model_group"`. The list covers the models this workspace has access to, so it can differ between workspaces.

    - `rate_limit_id: string`

      The `id` of the organization's RateLimit entry this entry applies to.

    - `workspace_id: string`

      ID of the Workspace this entry applies to.

  - `next_page: string`

    Opaque cursor for the next page of results, or `null` when no entries remain beyond this response.

#### Example

```bash
ant organization:workspaces:rate-limits list \
  --workspace-id workspace_id
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

`$ ant organization:workspaces:rate-limits update`

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

- `--workspace-id: string` (path parameter)

  The ID of the workspace.

- `--rate-limit-id: string` (path parameter)

  The `id` of the organization's rate-limit entry to set overrides for.

- `--limit: array of WorkspaceRateLimitUpdateValue`

  Limits to set or clear. Unspecified limit types are unchanged.

  minItems: 1, maxItems: 16

  - `type: "fast_itpmca" or "fast_otpm" or "input_tokens_per_minute" or 6 more`

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

  - `value: number`

    New limit value. Set to null to clear the workspace override and fall back to the organization limit.

    minimum: 0, maximum: 9007199254740991

#### Returns

- `workspace_rate_limit: object`

  - `type: "workspace_rate_limit"`

    Object type. Always `workspace_rate_limit` for workspace rate-limit entries.

  - `group: OrganizationRateLimitModelGroup or OrganizationRateLimitBatchGroup or OrganizationRateLimitTokenCountGroup or 3 more`

    The rate-limit group this entry's limits apply to.

    - `organization_rate_limit_model_group: object`

      - `type: "model_group"`

        Always `model_group`: a family of models.

      - `id: string`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

      - `display_name: string`

        Human-readable name of the model group (for example, `Claude Sonnet 4.x`). For display only; it may change.

    - `organization_rate_limit_batch_group: object`

      - `type: "batch"`

        Always `batch`: the Message Batches API.

      - `id: string`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `organization_rate_limit_token_count_group: object`

      - `type: "token_count"`

        Always `token_count`: the Token Count API.

      - `id: string`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `organization_rate_limit_files_group: object`

      - `type: "files"`

        Always `files`: the Files API.

      - `id: string`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `organization_rate_limit_skills_group: object`

      - `type: "skills"`

        Always `skills`: the Skills API.

      - `id: string`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

    - `organization_rate_limit_web_search_group: object`

      - `type: "web_search"`

        Always `web_search`: the Messages API web search tool.

      - `id: string`

        Opaque identifier of the rate-limit group (for example, `rlg_01VPTCmyiu5ZLsWkcxYG2pY8`). It is the same in every organization and never changes, unlike the entry's own identifier, which differs per organization.

  - `limits: array of WorkspaceRateLimitValue`

    The workspace's limiter values for this group. By default only the limiter types with a workspace-level override are listed. With `include_inherited` set to `true`, the limiter types the workspace inherits from the organization are listed too, each marked by `source`.

    - `type: string`

      The limiter type (for example, `requests_per_minute` or `input_tokens_per_minute`).

    - `org_limit: number`

      The organization-level value for the same limiter type, for reference. `null` when the organization has no limit configured for this limiter type.

    - `source: WorkspaceRateLimitWorkspaceSource or WorkspaceRateLimitOrganizationSource`

      Where `value` comes from. `organization` values are listed only when `include_inherited` is `true`, and then `value` equals `org_limit`.

      - `workspace_rate_limit_workspace_source: object`

        - `type: "workspace"`

          Always `workspace`: a workspace-level override is stored.

      - `workspace_rate_limit_organization_source: object`

        - `type: "organization"`

          Always `organization`: no workspace-level override is stored, so the organization's value applies.

    - `value: number`

      The workspace's value for this limiter type: the workspace-level override when `source.type` is `workspace`, otherwise the organization's value.

  - `models: array of string`

    Model names this entry's limits apply to, including aliases. `null` when `group.type` is not `"model_group"`. The list covers the models this workspace has access to, so it can differ between workspaces.

  - `rate_limit_id: string`

    The `id` of the organization's RateLimit entry this entry applies to.

  - `workspace_id: string`

    ID of the Workspace this entry applies to.

#### Example

```bash
ant organization:workspaces:rate-limits update \
  --workspace-id workspace_id \
  --rate-limit-id rate_limit_id \
  --limit '{type: fast_itpmca, value: 0}'
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

`$ ant organization:workspaces:members list`

**GET** `/v1/organizations/workspaces/{workspace_id}/members`

List Workspace Members

#### Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

- `--after-id: optional string` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `--before-id: optional string` (query parameter)

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `--limit: optional number` (query parameter)

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

  minimum: 1, maximum: 1000

#### Returns

- `ListResponse_WorkspaceMemberSchema_: object`

  - `data: array of WorkspaceMember`

    - `type: "workspace_member"`

      Object type.

      For Workspace Members, this is always `"workspace_member"`.

    - `user_id: string`

      ID of the User.

    - `workspace_id: string`

      ID of the Workspace.

    - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

      Role of the Workspace Member.

      - `"workspace_admin"`

      - `"workspace_billing"`

      - `"workspace_developer"`

      - `"workspace_restricted_developer"`

      - `"workspace_user"`

  - `first_id: string`

    First ID in the `data` list. Can be used as the `before_id` for the previous page.

  - `has_more: boolean`

    Indicates if there are more results in the requested page direction.

  - `last_id: string`

    Last ID in the `data` list. Can be used as the `after_id` for the next page.

#### Example

```bash
ant organization:workspaces:members list \
  --workspace-id workspace_id
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

`$ ant organization:workspaces:members add`

**POST** `/v1/organizations/workspaces/{workspace_id}/members`

Create Workspace Member

#### Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

- `--user-id: string`

  ID of the User.

- `--workspace-role: NoBillingWorkspaceRole`

  Role of the new Workspace Member. Cannot be `workspace_billing`.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `workspace_member: object`

  - `type: "workspace_member"`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

  - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```bash
ant organization:workspaces:members add \
  --workspace-id workspace_id \
  --user-id user_01WxYzAbCdEfGhJkMnPqRsTu \
  --workspace-role workspace_admin
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

`$ ant organization:workspaces:members retrieve`

**GET** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Get Workspace Member

#### Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

- `--user-id: string` (path parameter)

  ID of the User.

#### Returns

- `workspace_member: object`

  - `type: "workspace_member"`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

  - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```bash
ant organization:workspaces:members retrieve \
  --workspace-id workspace_id \
  --user-id user_id
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

`$ ant organization:workspaces:members update`

**POST** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Update Workspace Member

#### Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

- `--user-id: string` (path parameter)

  ID of the User.

- `--workspace-role: WorkspaceRole`

  New workspace role for the User.

  - `"workspace_admin"`

  - `"workspace_billing"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `workspace_member: object`

  - `type: "workspace_member"`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

  - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```bash
ant organization:workspaces:members update \
  --workspace-id workspace_id \
  --user-id user_id \
  --workspace-role workspace_admin
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

`$ ant organization:workspaces:members remove`

**DELETE** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Delete Workspace Member

#### Parameters

- `--workspace-id: string` (path parameter)

  ID of the Workspace.

- `--user-id: string` (path parameter)

  ID of the User.

#### Returns

- `OrganizationWorkspaceMemberRemoveResponse: object`

  - `type: "workspace_member_deleted"`

    Deleted object type.

    For Workspace Members, this is always `"workspace_member_deleted"`.

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

#### Example

```bash
ant organization:workspaces:members remove \
  --workspace-id workspace_id \
  --user-id user_id
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

`$ ant organization:workspaces:service-accounts list`

**GET** `/v1/organizations/workspaces/{workspace_id}/service_accounts`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

List the service accounts that are members of a workspace.

Each entry includes the service account's `workspace_role`. Use `limit`
and the `next_page` cursor to paginate. Archived workspaces return 400;
use `GET /service_accounts/{id}/workspaces` to audit memberships of an
archived workspace. The implicit default-workspace membership is not
included in this list. Memberships of archived service accounts are
omitted from the results.

#### Parameters

- `--workspace-id: string` (path parameter)

  ID of the workspace.

- `--limit: optional number` (query parameter)

  Number of results per page.

  minimum: 1, maximum: 100

- `--page: optional string` (query parameter)

  Opaque cursor from a previous response's `next_page`.

#### Returns

- `ServiceAccountWorkspaceMemberListResponse: object`

  - `data: array of ServiceAccountWorkspaceMember`

    - `type: "service_account_workspace_member"`

    - `created_by_actor_id: string`

      Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

    - `implicit: boolean`

      True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

    - `service_account_id: string`

      Tagged service account ID (`svac_...`).

    - `workspace_id: string`

      Tagged workspace ID (`wrkspc_...`).

    - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

      Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

      - `"workspace_admin"`

      - `"workspace_billing"`

      - `"workspace_developer"`

      - `"workspace_restricted_developer"`

      - `"workspace_user"`

  - `next_page: string`

    Opaque cursor for the next page, or null if no more results.

#### Example

```bash
ant organization:workspaces:service-accounts list \
  --workspace-id workspace_id
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

`$ ant organization:workspaces:service-accounts add`

**POST** `/v1/organizations/workspaces/{workspace_id}/service_accounts`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

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

- `--workspace-id: string` (path parameter)

  ID of the workspace.

- `--service-account-id: string`

  Tagged service account ID to add.

- `--workspace-role: NoBillingWorkspaceRole`

  Role to assign to the service account in this workspace.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `service_account_workspace_member: object`

  - `type: "service_account_workspace_member"`

  - `created_by_actor_id: string`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: boolean`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: string`

    Tagged service account ID (`svac_...`).

  - `workspace_id: string`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```bash
ant organization:workspaces:service-accounts add \
  --workspace-id workspace_id \
  --service-account-id service_account_id \
  --workspace-role workspace_admin
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

`$ ant organization:workspaces:service-accounts retrieve`

**GET** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

Retrieve a service account's membership in a workspace.

Returns the membership record, including the service account's
`workspace_role` in this workspace. Archived workspaces return 400. For
the default workspace, returns the implicit (`implicit: true`)
membership when no explicit membership exists; an explicitly added
membership is returned with its assigned role. An archived service
account returns 404.

#### Parameters

- `--workspace-id: string` (path parameter)

  ID of the workspace.

- `--service-account-id: string` (path parameter)

  ID of the service account.

#### Returns

- `service_account_workspace_member: object`

  - `type: "service_account_workspace_member"`

  - `created_by_actor_id: string`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: boolean`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: string`

    Tagged service account ID (`svac_...`).

  - `workspace_id: string`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```bash
ant organization:workspaces:service-accounts retrieve \
  --workspace-id workspace_id \
  --service-account-id service_account_id
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

`$ ant organization:workspaces:service-accounts update`

**POST** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

Change a service account's role in a workspace.

The new `workspace_role` replaces the current one. Only explicit
memberships can be updated; to set a role on the implicit
default-workspace membership, add the service account explicitly with
`POST /workspaces/{workspace_id}/service_accounts`. Archived workspaces
return 400. Archived service accounts cannot be updated and are
rejected.

#### Parameters

- `--workspace-id: string` (path parameter)

  ID of the workspace.

- `--service-account-id: string` (path parameter)

  ID of the service account.

- `--workspace-role: NoBillingWorkspaceRole`

  New role for the service account in this workspace.

  - `"workspace_admin"`

  - `"workspace_developer"`

  - `"workspace_restricted_developer"`

  - `"workspace_user"`

#### Returns

- `service_account_workspace_member: object`

  - `type: "service_account_workspace_member"`

  - `created_by_actor_id: string`

    Tagged ID (`user_...`/`svac_...`) of the actor who created this membership.

  - `implicit: boolean`

    True when this is the implicit default-workspace membership every service account has when no explicit membership exists. Implicit memberships have role `workspace_user` and cannot be removed.

  - `service_account_id: string`

    Tagged service account ID (`svac_...`).

  - `workspace_id: string`

    Tagged workspace ID (`wrkspc_...`).

  - `workspace_role: "workspace_admin" or "workspace_billing" or "workspace_developer" or 2 more`

    Role of the service account in this workspace. Service accounts cannot hold the `workspace_billing` role.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

#### Example

```bash
ant organization:workspaces:service-accounts update \
  --workspace-id workspace_id \
  --service-account-id service_account_id \
  --workspace-role workspace_admin
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

`$ ant organization:workspaces:service-accounts remove`

**DELETE** `/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

Remove a service account from a workspace.

Removal is idempotent (returns 200 even if the membership was already
removed). A DELETE against the implicit default-workspace membership
returns 200 but is a no-op and the membership persists; deleting an
explicit default-workspace row reverts to the implicit `workspace_user`
membership. Archived workspaces return 400.

#### Parameters

- `--workspace-id: string` (path parameter)

  ID of the workspace.

- `--service-account-id: string` (path parameter)

  ID of the service account.

#### Returns

- `OrganizationWorkspaceServiceAccountRemoveResponse: object`

  - `type: "service_account_workspace_member_deleted"`

  - `service_account_id: string`

    Tagged service account ID (`svac_...`) named in the delete request. Removal is idempotent; see the endpoint description for the implicit-membership no-op.

  - `workspace_id: string`

    Tagged workspace ID (`wrkspc_...`) named in the delete request.

#### Example

```bash
ant organization:workspaces:service-accounts remove \
  --workspace-id workspace_id \
  --service-account-id service_account_id
```

##### Response (200)

```json
{
  "service_account_id": "service_account_id",
  "type": "service_account_workspace_member_deleted",
  "workspace_id": "workspace_id"
}
```
