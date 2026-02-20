# Shared Authentication (SSO) 🔐

Single Sign-On system for all NEXUS products.

## Features

- JWT-based authentication
- Cross-product session sharing
- Role-based access control
- Token expiration (24 hours)

## Usage

```bash
# Start SSO
python3 main.py

# Login
curl -X POST http://localhost:8002/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@mrf103.com", "password": "admin123"}'

# Verify token
curl http://localhost:8002/api/v1/auth/verify?token=YOUR_TOKEN
```

## Test Credentials

- **Admin**: admin@mrf103.com / admin123
- **User**: user@mrf103.com / user123
