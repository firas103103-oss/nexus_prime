# Ecosystem API Gateway 🌐

Central API for all NEXUS products - handles communication, authentication, and coordination.

## Features

- **Product Management**: List, query, deploy products
- **Authentication**: JWT-based auth with Supabase integration
- **Approvals**: Send actions to Command Center for approval
- **Health Checks**: System status monitoring

## API Endpoints

### Core
- `GET /` - API info
- `GET /api/v1/health` - Health check

### Products
- `GET /api/v1/products` - List all products
- `GET /api/v1/products/{name}` - Product details
- `POST /api/v1/products/{name}/deploy` - Deploy product

### Approvals
- `POST /api/v1/approvals` - Create approval request

## Usage

```bash
# Start server
python3 main.py

# Test endpoints
curl http://localhost:8001/
curl http://localhost:8001/api/v1/products
curl http://localhost:8001/api/v1/health
```

## Integration

Used by:
- CLONE HUB (for product queries)
- Admin Portal (for management)
- Command Center (for approvals)
- All products (for inter-product communication)
