---
title: Get Federation Issuer
url: https://platform.claude.com/docs/en/api/python/organization/federation/issuers/retrieve
---

# Get Federation Issuer

`organization.federation.issuers.retrieve(federation_issuer_id) -> FederationIssuer`

**GET** `/v1/organizations/federation_issuers/{federation_issuer_id}`

**Requires an OAuth access token with the `org:admin` scope**, from `ant auth login --scope org:admin` or a workload identity federation rule; Admin API keys are not accepted. See [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api?sdk_languages=python).

Retrieve a federation issuer by its ID (`fdis_...`).

## Parameters

- `federation_issuer_id: str` (path parameter)

  ID of the federation issuer.

## Returns

- `class FederationIssuer`

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

    - `class JWKSDiscovery`

      JWKS via the issuer's OIDC discovery document.

      - `type: Literal["discovery"]`

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

      - `discovery_base: Optional[str]`

        Set when the discovery URL differs from `issuer_url`.

    - `class JWKSExplicitURL`

      JWKS fetched from a fixed endpoint.

      - `type: Literal["explicit_url"]`

      - `url: str`

        JWKS endpoint.

        minLength: 1

      - `ca_cert_pem: Optional[str]`

        Optional custom CA (PEM) for TLS verification of the JWKS fetch.

        maxLength: 8192

    - `class JWKSInline`

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

  - `poll_status: Optional[FederationIssuerPollStatus]`

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

## Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get(
        "ANTHROPIC_API_KEY"
    ),  # This is the default and can be omitted
)
federation_issuer = client.organization.federation.issuers.retrieve(
    "federation_issuer_id",
)
print(federation_issuer.id)
```

### Response (200)

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
