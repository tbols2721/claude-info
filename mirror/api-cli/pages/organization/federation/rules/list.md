---
title: List Federation Rules
url: https://platform.claude.com/docs/en/api/cli/organization/federation/rules/list
---

# List Federation Rules

`$ ant organization:federation:rules list`

**GET** `/v1/organizations/federation_rules`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=cli).

List federation rules in your organization.

Optionally filter by issuer with `issuer_id`. Archived rules are excluded
unless `include_archived=true`.

## Parameters

- `--include-archived: optional boolean` (query parameter)

  Include archived resources. Defaults to false.

- `--issuer-id: optional string` (query parameter)

  Filter to rules referencing this federation issuer.

- `--limit: optional number` (query parameter)

  Number of results per page.

  minimum: 1, maximum: 100

- `--page: optional string` (query parameter)

  Opaque cursor from a previous response's `next_page`.

## Returns

- `FederationRuleListResponse: object`

  - `data: array of FederationRule`

    - `type: "federation_rule"`

    - `id: string`

      Tagged ID of the federation rule.

    - `applies_to_all_workspaces: boolean`

      When true, this rule is enabled for every workspace in the org (including ones created after the rule). `workspace_ids` is ignored at exchange time.

    - `archived_at: string`

      If set, this rule is archived and rejects token exchange.

      format: date-time

    - `archived_by_actor_id: string`

      Tagged ID (`user_`/`svac_`) of the actor that archived this rule.

    - `created_at: string`

      When this rule was created.

      format: date-time

    - `created_by_actor_id: string`

      Tagged ID (`user_`/`svac_`) of the actor that created this rule.

    - `description: string`

      Optional free-text description.

    - `issuer_id: string`

      Tagged ID of the issuer whose tokens this rule accepts.

    - `issuer_name: string`

      Issuer's display name at read time.

    - `match: object`

      Conditions the verified JWT must satisfy for this rule to apply. All populated matcher fields must pass.

      - `audience: optional string`

        Exact match against the `aud` claim (any element if array). When omitted, the JWT's `aud` must still equal Anthropic's expected audience for the issuer; setting this field overrides that default.

        maxLength: 1024

      - `claims: optional map[string]`

        Exact-match `{claim: value}` pairs against top-level claims. Only string-valued claims can be matched; use `condition` for non-string claims.

      - `condition: optional string`

        CEL expression over claims for logic the structural fields can't express. Must evaluate to a boolean and may reference only the `claims` variable; a constant-true expression (such as `true`) is rejected with 400.

        maxLength: 4096

      - `subject_prefix: optional string`

        Match the verified JWT `sub` claim. Exact match unless the value ends with `*`, in which case it is a prefix match. Example: `repo:my-org/my-repo:ref:refs/heads/main`.

        maxLength: 1024

    - `name: string`

      Admin-chosen slug identifier.

    - `oauth_scope: string`

      Space-separated OAuth scopes granted on the minted token.

    - `target: object`

      What this rule targets. Check `type` before reading the other fields. Tokens minted via a rule whose target `type` is `service_account` act as that service account.

      - `type: "service_account"`

      - `service_account_id: string`

        Tagged ID of the service account to mint tokens for.

      - `service_account_name: optional string`

        Service account's display name at read time. Ignored on writes.

    - `token_lifetime_seconds: number`

      Lifetime in seconds of access tokens minted via this rule. Minted tokens are capped at `max(60, min(this value, 2 × remaining assertion validity))` seconds.

    - `updated_at: string`

      When this rule was last updated.

      format: date-time

    - `updated_by_actor_id: string`

      Tagged ID (`user_`/`svac_`) of the actor that last updated this rule.

    - `workspace_ids: array of string`

      Tagged IDs of the workspaces this rule is enabled for. May be empty for older rules that only carry the legacy `workspace_id` binding. Ignored at exchange time when `applies_to_all_workspaces` is true (the list may still be non-empty).

  - `next_page: string`

    Opaque cursor for the next page, or null if no more results.

## Example

```bash
ant organization:federation:rules list
```

### Response (200)

```json
{
  "data": [
    {
      "id": "fdrl_01SDCCSbTxrXDpWc1phhtcfK",
      "applies_to_all_workspaces": true,
      "archived_at": "2019-12-27T18:11:19.117Z",
      "archived_by_actor_id": "archived_by_actor_id",
      "attributes": {
        "foo": "string"
      },
      "created_at": "2024-10-30T23:58:27.427722Z",
      "created_by_actor_id": "created_by_actor_id",
      "description": "description",
      "issuer_id": "issuer_id",
      "issuer_name": "issuer_name",
      "match": {
        "audience": "audience",
        "claims": {
          "foo": "string"
        },
        "condition": "condition",
        "subject_prefix": "subject_prefix"
      },
      "name": "prod-deploy-pipeline",
      "oauth_scope": "oauth_scope",
      "target": {
        "service_account_id": "svac_01SDCCSbTxrXDpWc1phhtcfK",
        "type": "service_account",
        "service_account_name": "service_account_name"
      },
      "token_lifetime_seconds": 0,
      "type": "federation_rule",
      "updated_at": "2024-10-30T23:58:27.427722Z",
      "updated_by_actor_id": "updated_by_actor_id",
      "workspace_id": "workspace_id",
      "workspace_ids": [
        "string"
      ]
    }
  ],
  "next_page": "next_page"
}
```
