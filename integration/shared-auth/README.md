# NEXUS Shared Auth — RS256 JWT SSO

## Key Generation

Before starting `nexus_auth`, generate RS256 keys:

```bash
KEYS_DIR=/path/to/NEXUS_PRIME_UNIFIED/data/auth_keys python3 generate_keys.py
```

Or from project root:

```bash
KEYS_DIR=$(pwd)/data/auth_keys python3 integration/shared-auth/generate_keys.py
```

## Endpoints

- `POST /api/v1/auth/login` — Login (admin/admin123 bootstrap)
- `POST /api/v1/auth/verify` — Verify token
- `GET /api/v1/auth/.well-known/jwks.json` — JWKS
- `GET /api/v1/auth/health` — Health check
