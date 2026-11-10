---
title: Issuers
url: https://platform.claude.com/docs/en/api/python/beta/organization/federation/issuers
---

# Issuers

## Create Federation Issuer

`beta.organization.federation.issuers.create(**kwargs) -> BetaFederationIssuer`

**POST** `/v1/organizations/federation_issuers`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Register an OIDC issuer that Anthropic will trust for workload identity
federation in your organization.

The `jwks` field controls how the issuer's signing keys are obtained and
takes one of three shapes selected by `type`: `discovery` (resolve keys
through OIDC discovery), `explicit_url` (fetch keys from a fixed JWKS
URL), or `inline` (provide a static key set). When `jwks.type` is
`discovery` and no `discovery_base` is set, the issuer URL must be
publicly reachable over HTTPS so Anthropic can fetch the discovery
document; for `explicit_url` and `inline` modes the issuer URL is only
matched as the JWT's `iss` claim and is not fetched.

### Parameters

- `issuer_url: str`

  The `iss` claim value to match against.

  minLength: 1

- `name: str`

  Slug identifier (lowercase, digits, hyphens). Unique within the organization; a duplicate name returns 409.

  minLength: 1, maxLength: 255

- `check_jti: Optional[bool]`

  Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Defaults to true. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

- `jwks: Optional[JWKS]`

  How signing keys are obtained. Defaults to OIDC discovery.

  - `class BetaJWKSDiscovery`

    JWKS via the issuer's OIDC discovery document.

    - `type: Literal["discovery"]`

    - `ca_cert_pem: Optional[str]`

      Optional custom CA (PEM) for TLS verification of the JWKS fetch.

      maxLength: 8192

    - `discovery_base: Optional[str]`

      Set when the discovery URL differs from `issuer_url`.

  - `class BetaJWKSExplicitURL`

    JWKS fetched from a fixed endpoint.

    - `type: Literal["explicit_url"]`

    - `url: str`

      JWKS endpoint.

      minLength: 1

    - `ca_cert_pem: Optional[str]`

      Optional custom CA (PEM) for TLS verification of the JWKS fetch.

      maxLength: 8192

  - `class BetaJWKSInline`

    JWKS supplied directly; no network fetch.

    - `type: Literal["inline"]`

    - `keys: List[Dict[str, object]]`

      Inline JWK objects.

      minItems: 1

- `max_jwt_lifetime_seconds: Optional[int]`

  Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Defaults to 3600 (1h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  minimum: 1, maximum: 176400

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  Optional header to specify the beta version(s) you want to use.

  - `str`

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

- `class BetaFederationIssuer`

  Registered external OIDC identity provider.

  Records an external IdP the organization trusts for the RFC 7523
  jwt-bearer grant. The `issuer_url` must match the JWT `iss` claim exactly.

  - `type: Literal["federation_issuer"]`

    default: federation_issuer

  - `id: str`

    Tagged ID of the federation issuer.

  - `archived_at: Optional[datetime]`

    If set, all rules referencing this issuer reject token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this issuer.

  - `check_jti: bool`

    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

  - `created_at: datetime`

    When this issuer was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this issuer.

  - `issuer_url: str`

    The `iss` claim value. Incoming JWTs must match exactly.

  - `jwks: JWKS`

    How signing keys are obtained for signature verification.

    - `class BetaJWKSDiscovery`

      JWKS via the issuer's OIDC discovery document.

      - `type: Literal["discovery"]`

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

      - `discovery_base: Optional[str]`

        Set when the discovery URL differs from `issuer_url`.

    - `class BetaJWKSExplicitURL`

      JWKS fetched from a fixed endpoint.

      - `type: Literal["explicit_url"]`

      - `url: str`

        JWKS endpoint.

        minLength: 1

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

    - `class BetaJWKSInline`

      JWKS supplied directly; no network fetch.

      - `type: Literal["inline"]`

      - `keys: List[Dict[str, object]]`

        Inline JWK objects.

        minItems: 1

  - `jwks_polling_disabled_at: Optional[datetime]`

    If set, Anthropic's JWKS poller has paused polling for this issuer after repeated fetch failures. Re-enable by sending `jwks_polling_disabled: false` via the issuer update endpoint (POST) once the upstream JWKS endpoint is fixed. An OAuth caller cannot send this when the issuer backs a rule with any scope other than `workspace:developer` or `workspace:inference`; use a Console session.

    format: date-time

  - `max_jwt_lifetime_seconds: int`

    Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  - `name: str`

    Admin-chosen slug identifier.

  - `poll_status: Optional[BetaFederationIssuerPollStatus]`

    Live state of Anthropic's JWKS polling for this issuer. Populated on both single-issuer retrieval and list responses, including archived issuers. Typically null for inline-key issuers (no polling), or when poll status is temporarily unavailable or polling has not started yet.

    - `consecutive_failures: int`

      Consecutive fetch failures since the last success.

    - `last_fetched_at: Optional[datetime]`

      When the last successful fetch completed.

      format: date-time

    - `next_poll_at: Optional[datetime]`

      When the next fetch is scheduled. Null if paused.

      format: date-time

  - `updated_at: datetime`

    When this issuer was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_federation_issuer = client.beta.organization.federation.issuers.create(
    issuer_url="x",
    name="x",
)
print(beta_federation_issuer.id)
```

#### Response (200)

```json
{
  "id": "fdis_01SDCCSbTxrXDpWc1phhtcfK",
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "check_jti": true,
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "issuer_url": "https://token.actions.githubusercontent.com",
  "jwks": {
    "type": "discovery",
    "ca_cert_pem": "ca_cert_pem",
    "discovery_base": "discovery_base"
  },
  "jwks_polling_disabled_at": "2019-12-27T18:11:19.117Z",
  "max_jwt_lifetime_seconds": 0,
  "name": "github-actions",
  "poll_status": {
    "consecutive_failures": 0,
    "last_fetched_at": "2019-12-27T18:11:19.117Z",
    "next_poll_at": "2019-12-27T18:11:19.117Z"
  },
  "type": "federation_issuer",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id"
}
```

## List Federation Issuers

`beta.organization.federation.issuers.list(**kwargs) -> SyncPageCursor[BetaFederationIssuer]`

**GET** `/v1/organizations/federation_issuers`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

List federation issuers in your organization.

Archived issuers are excluded unless `include_archived=true`.

### Parameters

- `include_archived: Optional[bool]` (query parameter)

  Include archived resources. Defaults to false.

  default: false

- `limit: Optional[int]` (query parameter)

  Number of results per page.

  default: 20, minimum: 1, maximum: 100

- `page: Optional[str]` (query parameter)

  Opaque cursor from a previous response's `next_page`.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  Optional header to specify the beta version(s) you want to use.

  - `str`

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

- `class BetaFederationIssuer`

  Registered external OIDC identity provider.

  Records an external IdP the organization trusts for the RFC 7523
  jwt-bearer grant. The `issuer_url` must match the JWT `iss` claim exactly.

  - `type: Literal["federation_issuer"]`

    default: federation_issuer

  - `id: str`

    Tagged ID of the federation issuer.

  - `archived_at: Optional[datetime]`

    If set, all rules referencing this issuer reject token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this issuer.

  - `check_jti: bool`

    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

  - `created_at: datetime`

    When this issuer was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this issuer.

  - `issuer_url: str`

    The `iss` claim value. Incoming JWTs must match exactly.

  - `jwks: JWKS`

    How signing keys are obtained for signature verification.

    - `class BetaJWKSDiscovery`

      JWKS via the issuer's OIDC discovery document.

      - `type: Literal["discovery"]`

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

      - `discovery_base: Optional[str]`

        Set when the discovery URL differs from `issuer_url`.

    - `class BetaJWKSExplicitURL`

      JWKS fetched from a fixed endpoint.

      - `type: Literal["explicit_url"]`

      - `url: str`

        JWKS endpoint.

        minLength: 1

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

    - `class BetaJWKSInline`

      JWKS supplied directly; no network fetch.

      - `type: Literal["inline"]`

      - `keys: List[Dict[str, object]]`

        Inline JWK objects.

        minItems: 1

  - `jwks_polling_disabled_at: Optional[datetime]`

    If set, Anthropic's JWKS poller has paused polling for this issuer after repeated fetch failures. Re-enable by sending `jwks_polling_disabled: false` via the issuer update endpoint (POST) once the upstream JWKS endpoint is fixed. An OAuth caller cannot send this when the issuer backs a rule with any scope other than `workspace:developer` or `workspace:inference`; use a Console session.

    format: date-time

  - `max_jwt_lifetime_seconds: int`

    Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  - `name: str`

    Admin-chosen slug identifier.

  - `poll_status: Optional[BetaFederationIssuerPollStatus]`

    Live state of Anthropic's JWKS polling for this issuer. Populated on both single-issuer retrieval and list responses, including archived issuers. Typically null for inline-key issuers (no polling), or when poll status is temporarily unavailable or polling has not started yet.

    - `consecutive_failures: int`

      Consecutive fetch failures since the last success.

    - `last_fetched_at: Optional[datetime]`

      When the last successful fetch completed.

      format: date-time

    - `next_poll_at: Optional[datetime]`

      When the next fetch is scheduled. Null if paused.

      format: date-time

  - `updated_at: datetime`

    When this issuer was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
page = client.beta.organization.federation.issuers.list()
page = page.data[0]
print(page.id)
```

#### Response (200)

```json
{
  "data": [
    {
      "id": "fdis_01SDCCSbTxrXDpWc1phhtcfK",
      "archived_at": "2019-12-27T18:11:19.117Z",
      "archived_by_actor_id": "archived_by_actor_id",
      "check_jti": true,
      "created_at": "2024-10-30T23:58:27.427722Z",
      "created_by_actor_id": "created_by_actor_id",
      "issuer_url": "https://token.actions.githubusercontent.com",
      "jwks": {
        "type": "discovery",
        "ca_cert_pem": "ca_cert_pem",
        "discovery_base": "discovery_base"
      },
      "jwks_polling_disabled_at": "2019-12-27T18:11:19.117Z",
      "max_jwt_lifetime_seconds": 0,
      "name": "github-actions",
      "poll_status": {
        "consecutive_failures": 0,
        "last_fetched_at": "2019-12-27T18:11:19.117Z",
        "next_poll_at": "2019-12-27T18:11:19.117Z"
      },
      "type": "federation_issuer",
      "updated_at": "2024-10-30T23:58:27.427722Z",
      "updated_by_actor_id": "updated_by_actor_id"
    }
  ],
  "next_page": "next_page"
}
```

## Get Federation Issuer

`beta.organization.federation.issuers.retrieve(federation_issuer_id, **kwargs) -> BetaFederationIssuer`

**GET** `/v1/organizations/federation_issuers/{federation_issuer_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Retrieve a federation issuer by its ID (`fdis_...`).

### Parameters

- `federation_issuer_id: str` (path parameter)

  ID of the federation issuer.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  Optional header to specify the beta version(s) you want to use.

  - `str`

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

- `class BetaFederationIssuer`

  Registered external OIDC identity provider.

  Records an external IdP the organization trusts for the RFC 7523
  jwt-bearer grant. The `issuer_url` must match the JWT `iss` claim exactly.

  - `type: Literal["federation_issuer"]`

    default: federation_issuer

  - `id: str`

    Tagged ID of the federation issuer.

  - `archived_at: Optional[datetime]`

    If set, all rules referencing this issuer reject token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this issuer.

  - `check_jti: bool`

    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

  - `created_at: datetime`

    When this issuer was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this issuer.

  - `issuer_url: str`

    The `iss` claim value. Incoming JWTs must match exactly.

  - `jwks: JWKS`

    How signing keys are obtained for signature verification.

    - `class BetaJWKSDiscovery`

      JWKS via the issuer's OIDC discovery document.

      - `type: Literal["discovery"]`

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

      - `discovery_base: Optional[str]`

        Set when the discovery URL differs from `issuer_url`.

    - `class BetaJWKSExplicitURL`

      JWKS fetched from a fixed endpoint.

      - `type: Literal["explicit_url"]`

      - `url: str`

        JWKS endpoint.

        minLength: 1

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

    - `class BetaJWKSInline`

      JWKS supplied directly; no network fetch.

      - `type: Literal["inline"]`

      - `keys: List[Dict[str, object]]`

        Inline JWK objects.

        minItems: 1

  - `jwks_polling_disabled_at: Optional[datetime]`

    If set, Anthropic's JWKS poller has paused polling for this issuer after repeated fetch failures. Re-enable by sending `jwks_polling_disabled: false` via the issuer update endpoint (POST) once the upstream JWKS endpoint is fixed. An OAuth caller cannot send this when the issuer backs a rule with any scope other than `workspace:developer` or `workspace:inference`; use a Console session.

    format: date-time

  - `max_jwt_lifetime_seconds: int`

    Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  - `name: str`

    Admin-chosen slug identifier.

  - `poll_status: Optional[BetaFederationIssuerPollStatus]`

    Live state of Anthropic's JWKS polling for this issuer. Populated on both single-issuer retrieval and list responses, including archived issuers. Typically null for inline-key issuers (no polling), or when poll status is temporarily unavailable or polling has not started yet.

    - `consecutive_failures: int`

      Consecutive fetch failures since the last success.

    - `last_fetched_at: Optional[datetime]`

      When the last successful fetch completed.

      format: date-time

    - `next_poll_at: Optional[datetime]`

      When the next fetch is scheduled. Null if paused.

      format: date-time

  - `updated_at: datetime`

    When this issuer was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_federation_issuer = client.beta.organization.federation.issuers.retrieve(
    federation_issuer_id="federation_issuer_id",
)
print(beta_federation_issuer.id)
```

#### Response (200)

```json
{
  "id": "fdis_01SDCCSbTxrXDpWc1phhtcfK",
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "check_jti": true,
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "issuer_url": "https://token.actions.githubusercontent.com",
  "jwks": {
    "type": "discovery",
    "ca_cert_pem": "ca_cert_pem",
    "discovery_base": "discovery_base"
  },
  "jwks_polling_disabled_at": "2019-12-27T18:11:19.117Z",
  "max_jwt_lifetime_seconds": 0,
  "name": "github-actions",
  "poll_status": {
    "consecutive_failures": 0,
    "last_fetched_at": "2019-12-27T18:11:19.117Z",
    "next_poll_at": "2019-12-27T18:11:19.117Z"
  },
  "type": "federation_issuer",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id"
}
```

## Update Federation Issuer

`beta.organization.federation.issuers.update(federation_issuer_id, **kwargs) -> BetaFederationIssuer`

**POST** `/v1/organizations/federation_issuers/{federation_issuer_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Partially update a federation issuer.

Setting `jwks` replaces the full JWKS shape at once. Archived issuers
cannot be updated; this returns 400. Create a new issuer instead.

Updating an issuer that backs a rule with a scope outside
`workspace:developer` or `workspace:inference` requires a Console
session.

### Parameters

- `federation_issuer_id: str` (path parameter)

  ID of the federation issuer to update.

- `check_jti: Optional[bool]`

  Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

- `issuer_url: Optional[str]`

  Replaces the `iss` claim value to match against. For discovery-mode issuers without a `discovery_base`, this is also the URL Anthropic fetches the OIDC discovery document and signing keys from, so changing it repoints the JWKS source. Changing the issuer URL to a well-known shared platform is rejected while any live rule under this issuer would not constrain tenant identity.

  minLength: 1

- `jwks: Optional[JWKS]`

  Replaces the entire JWKS configuration.

  - `class BetaJWKSDiscovery`

    JWKS via the issuer's OIDC discovery document.

    - `type: Literal["discovery"]`

    - `ca_cert_pem: Optional[str]`

      Optional custom CA (PEM) for TLS verification of the JWKS fetch.

      maxLength: 8192

    - `discovery_base: Optional[str]`

      Set when the discovery URL differs from `issuer_url`.

  - `class BetaJWKSExplicitURL`

    JWKS fetched from a fixed endpoint.

    - `type: Literal["explicit_url"]`

    - `url: str`

      JWKS endpoint.

      minLength: 1

    - `ca_cert_pem: Optional[str]`

      Optional custom CA (PEM) for TLS verification of the JWKS fetch.

      maxLength: 8192

  - `class BetaJWKSInline`

    JWKS supplied directly; no network fetch.

    - `type: Literal["inline"]`

    - `keys: List[Dict[str, object]]`

      Inline JWK objects.

      minItems: 1

- `jwks_polling_disabled: Optional[bool]`

  Only `false` is accepted, to re-enable polling after the system pauses it. Polling is paused automatically; sending `true` is rejected.

- `max_jwt_lifetime_seconds: Optional[int]`

  Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  minimum: 1, maximum: 176400

- `name: Optional[str]`

  Replaces the slug identifier (lowercase, digits, hyphens). Unique within the organization; a duplicate name returns 409.

  minLength: 1, maxLength: 255

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  Optional header to specify the beta version(s) you want to use.

  - `str`

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

- `class BetaFederationIssuer`

  Registered external OIDC identity provider.

  Records an external IdP the organization trusts for the RFC 7523
  jwt-bearer grant. The `issuer_url` must match the JWT `iss` claim exactly.

  - `type: Literal["federation_issuer"]`

    default: federation_issuer

  - `id: str`

    Tagged ID of the federation issuer.

  - `archived_at: Optional[datetime]`

    If set, all rules referencing this issuer reject token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this issuer.

  - `check_jti: bool`

    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

  - `created_at: datetime`

    When this issuer was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this issuer.

  - `issuer_url: str`

    The `iss` claim value. Incoming JWTs must match exactly.

  - `jwks: JWKS`

    How signing keys are obtained for signature verification.

    - `class BetaJWKSDiscovery`

      JWKS via the issuer's OIDC discovery document.

      - `type: Literal["discovery"]`

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

      - `discovery_base: Optional[str]`

        Set when the discovery URL differs from `issuer_url`.

    - `class BetaJWKSExplicitURL`

      JWKS fetched from a fixed endpoint.

      - `type: Literal["explicit_url"]`

      - `url: str`

        JWKS endpoint.

        minLength: 1

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

    - `class BetaJWKSInline`

      JWKS supplied directly; no network fetch.

      - `type: Literal["inline"]`

      - `keys: List[Dict[str, object]]`

        Inline JWK objects.

        minItems: 1

  - `jwks_polling_disabled_at: Optional[datetime]`

    If set, Anthropic's JWKS poller has paused polling for this issuer after repeated fetch failures. Re-enable by sending `jwks_polling_disabled: false` via the issuer update endpoint (POST) once the upstream JWKS endpoint is fixed. An OAuth caller cannot send this when the issuer backs a rule with any scope other than `workspace:developer` or `workspace:inference`; use a Console session.

    format: date-time

  - `max_jwt_lifetime_seconds: int`

    Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  - `name: str`

    Admin-chosen slug identifier.

  - `poll_status: Optional[BetaFederationIssuerPollStatus]`

    Live state of Anthropic's JWKS polling for this issuer. Populated on both single-issuer retrieval and list responses, including archived issuers. Typically null for inline-key issuers (no polling), or when poll status is temporarily unavailable or polling has not started yet.

    - `consecutive_failures: int`

      Consecutive fetch failures since the last success.

    - `last_fetched_at: Optional[datetime]`

      When the last successful fetch completed.

      format: date-time

    - `next_poll_at: Optional[datetime]`

      When the next fetch is scheduled. Null if paused.

      format: date-time

  - `updated_at: datetime`

    When this issuer was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_federation_issuer = client.beta.organization.federation.issuers.update(
    federation_issuer_id="federation_issuer_id",
)
print(beta_federation_issuer.id)
```

#### Response (200)

```json
{
  "id": "fdis_01SDCCSbTxrXDpWc1phhtcfK",
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "check_jti": true,
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "issuer_url": "https://token.actions.githubusercontent.com",
  "jwks": {
    "type": "discovery",
    "ca_cert_pem": "ca_cert_pem",
    "discovery_base": "discovery_base"
  },
  "jwks_polling_disabled_at": "2019-12-27T18:11:19.117Z",
  "max_jwt_lifetime_seconds": 0,
  "name": "github-actions",
  "poll_status": {
    "consecutive_failures": 0,
    "last_fetched_at": "2019-12-27T18:11:19.117Z",
    "next_poll_at": "2019-12-27T18:11:19.117Z"
  },
  "type": "federation_issuer",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id"
}
```

## Archive Federation Issuer

`beta.organization.federation.issuers.archive(federation_issuer_id, **kwargs) -> BetaFederationIssuer`

**POST** `/v1/organizations/federation_issuers/{federation_issuer_id}/archive`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Archive a federation issuer.

Idempotent; re-archiving returns the issuer with its original
`archived_at`. Rejected with 400 if any live (non-archived) federation
rule still references the issuer; archive those rules first (a rule's
issuer cannot be changed), or recreate them against another issuer.

### Parameters

- `federation_issuer_id: str` (path parameter)

  ID of the federation issuer to archive.

- `betas: Optional[List[AnthropicBetaParam]]` (header parameter)

  Optional header to specify the beta version(s) you want to use.

  - `str`

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

- `class BetaFederationIssuer`

  Registered external OIDC identity provider.

  Records an external IdP the organization trusts for the RFC 7523
  jwt-bearer grant. The `issuer_url` must match the JWT `iss` claim exactly.

  - `type: Literal["federation_issuer"]`

    default: federation_issuer

  - `id: str`

    Tagged ID of the federation issuer.

  - `archived_at: Optional[datetime]`

    If set, all rules referencing this issuer reject token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this issuer.

  - `check_jti: bool`

    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

  - `created_at: datetime`

    When this issuer was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this issuer.

  - `issuer_url: str`

    The `iss` claim value. Incoming JWTs must match exactly.

  - `jwks: JWKS`

    How signing keys are obtained for signature verification.

    - `class BetaJWKSDiscovery`

      JWKS via the issuer's OIDC discovery document.

      - `type: Literal["discovery"]`

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

      - `discovery_base: Optional[str]`

        Set when the discovery URL differs from `issuer_url`.

    - `class BetaJWKSExplicitURL`

      JWKS fetched from a fixed endpoint.

      - `type: Literal["explicit_url"]`

      - `url: str`

        JWKS endpoint.

        minLength: 1

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

    - `class BetaJWKSInline`

      JWKS supplied directly; no network fetch.

      - `type: Literal["inline"]`

      - `keys: List[Dict[str, object]]`

        Inline JWK objects.

        minItems: 1

  - `jwks_polling_disabled_at: Optional[datetime]`

    If set, Anthropic's JWKS poller has paused polling for this issuer after repeated fetch failures. Re-enable by sending `jwks_polling_disabled: false` via the issuer update endpoint (POST) once the upstream JWKS endpoint is fixed. An OAuth caller cannot send this when the issuer backs a rule with any scope other than `workspace:developer` or `workspace:inference`; use a Console session.

    format: date-time

  - `max_jwt_lifetime_seconds: int`

    Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  - `name: str`

    Admin-chosen slug identifier.

  - `poll_status: Optional[BetaFederationIssuerPollStatus]`

    Live state of Anthropic's JWKS polling for this issuer. Populated on both single-issuer retrieval and list responses, including archived issuers. Typically null for inline-key issuers (no polling), or when poll status is temporarily unavailable or polling has not started yet.

    - `consecutive_failures: int`

      Consecutive fetch failures since the last success.

    - `last_fetched_at: Optional[datetime]`

      When the last successful fetch completed.

      format: date-time

    - `next_poll_at: Optional[datetime]`

      When the next fetch is scheduled. Null if paused.

      format: date-time

  - `updated_at: datetime`

    When this issuer was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer.

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
beta_federation_issuer = client.beta.organization.federation.issuers.archive(
    federation_issuer_id="federation_issuer_id",
)
print(beta_federation_issuer.id)
```

#### Response (200)

```json
{
  "id": "fdis_01SDCCSbTxrXDpWc1phhtcfK",
  "archived_at": "2019-12-27T18:11:19.117Z",
  "archived_by_actor_id": "archived_by_actor_id",
  "check_jti": true,
  "created_at": "2024-10-30T23:58:27.427722Z",
  "created_by_actor_id": "created_by_actor_id",
  "issuer_url": "https://token.actions.githubusercontent.com",
  "jwks": {
    "type": "discovery",
    "ca_cert_pem": "ca_cert_pem",
    "discovery_base": "discovery_base"
  },
  "jwks_polling_disabled_at": "2019-12-27T18:11:19.117Z",
  "max_jwt_lifetime_seconds": 0,
  "name": "github-actions",
  "poll_status": {
    "consecutive_failures": 0,
    "last_fetched_at": "2019-12-27T18:11:19.117Z",
    "next_poll_at": "2019-12-27T18:11:19.117Z"
  },
  "type": "federation_issuer",
  "updated_at": "2024-10-30T23:58:27.427722Z",
  "updated_by_actor_id": "updated_by_actor_id"
}
```

## Domain types

### Beta Federation Issuer

- `class BetaFederationIssuer`

  Registered external OIDC identity provider.

  Records an external IdP the organization trusts for the RFC 7523
  jwt-bearer grant. The `issuer_url` must match the JWT `iss` claim exactly.

  - `type: Literal["federation_issuer"]`

    default: federation_issuer

  - `id: str`

    Tagged ID of the federation issuer.

  - `archived_at: Optional[datetime]`

    If set, all rules referencing this issuer reject token exchange.

    format: date-time

  - `archived_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that archived this issuer.

  - `check_jti: bool`

    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for tokens from this issuer. Applies only to assertions carrying a `jti` claim; tokens without one are accepted without single-use enforcement.

  - `created_at: datetime`

    When this issuer was created.

    format: date-time

  - `created_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that created this issuer.

  - `issuer_url: str`

    The `iss` claim value. Incoming JWTs must match exactly.

  - `jwks: JWKS`

    How signing keys are obtained for signature verification.

    - `class BetaJWKSDiscovery`

      JWKS via the issuer's OIDC discovery document.

      - `type: Literal["discovery"]`

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

      - `discovery_base: Optional[str]`

        Set when the discovery URL differs from `issuer_url`.

    - `class BetaJWKSExplicitURL`

      JWKS fetched from a fixed endpoint.

      - `type: Literal["explicit_url"]`

      - `url: str`

        JWKS endpoint.

        minLength: 1

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

    - `class BetaJWKSInline`

      JWKS supplied directly; no network fetch.

      - `type: Literal["inline"]`

      - `keys: List[Dict[str, object]]`

        Inline JWK objects.

        minItems: 1

  - `jwks_polling_disabled_at: Optional[datetime]`

    If set, Anthropic's JWKS poller has paused polling for this issuer after repeated fetch failures. Re-enable by sending `jwks_polling_disabled: false` via the issuer update endpoint (POST) once the upstream JWKS endpoint is fixed. An OAuth caller cannot send this when the issuer backs a rule with any scope other than `workspace:developer` or `workspace:inference`; use a Console session.

    format: date-time

  - `max_jwt_lifetime_seconds: int`

    Maximum allowed iat→exp spread for assertions from this issuer (1-176400 seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing `iat` is rejected.

  - `name: str`

    Admin-chosen slug identifier.

  - `poll_status: Optional[BetaFederationIssuerPollStatus]`

    Live state of Anthropic's JWKS polling for this issuer. Populated on both single-issuer retrieval and list responses, including archived issuers. Typically null for inline-key issuers (no polling), or when poll status is temporarily unavailable or polling has not started yet.

    - `consecutive_failures: int`

      Consecutive fetch failures since the last success.

    - `last_fetched_at: Optional[datetime]`

      When the last successful fetch completed.

      format: date-time

    - `next_poll_at: Optional[datetime]`

      When the next fetch is scheduled. Null if paused.

      format: date-time

  - `updated_at: datetime`

    When this issuer was last updated.

    format: date-time

  - `updated_by_actor_id: Optional[str]`

    Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer.

### Beta Federation Issuer Poll Status

- `class BetaFederationIssuerPollStatus`

  Status of automatic JWKS polling for a federation issuer.

  Anthropic periodically fetches the issuer's signing keys in the
  background. These fields summarize the most recent fetches so the
  health of the JWKS endpoint can be monitored.

  - `consecutive_failures: int`

    Consecutive fetch failures since the last success.

  - `last_fetched_at: Optional[datetime]`

    When the last successful fetch completed.

    format: date-time

  - `next_poll_at: Optional[datetime]`

    When the next fetch is scheduled. Null if paused.

    format: date-time

### Beta JWKS Discovery

- `class BetaJWKSDiscovery`

  JWKS via the issuer's OIDC discovery document.

  - `type: Literal["discovery"]`

  - `ca_cert_pem: Optional[str]`

    Optional custom CA (PEM) for TLS verification of the JWKS fetch.

    maxLength: 8192

  - `discovery_base: Optional[str]`

    Set when the discovery URL differs from `issuer_url`.

### Beta JWKS Explicit URL

- `class BetaJWKSExplicitURL`

  JWKS fetched from a fixed endpoint.

  - `type: Literal["explicit_url"]`

  - `url: str`

    JWKS endpoint.

    minLength: 1

  - `ca_cert_pem: Optional[str]`

    Optional custom CA (PEM) for TLS verification of the JWKS fetch.

    maxLength: 8192

### Beta JWKS Inline

- `class BetaJWKSInline`

  JWKS supplied directly; no network fetch.

  - `type: Literal["inline"]`

  - `keys: List[Dict[str, object]]`

    Inline JWK objects.

    minItems: 1
