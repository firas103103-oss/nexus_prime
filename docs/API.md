# NEXUS PRIME - API Documentation

## Overview
NEXUS PRIME provides a unified API across all 7 products.

## Base URL
```
https://api.nexusprime.io/v1
```

## Authentication
All requests require JWT token:
```
Authorization: Bearer <token>
```

## Endpoints

### Products
- `GET /products` - List all products
- `GET /products/:id` - Get product details
- `POST /products` - Create product (admin only)
- `PUT /products/:id` - Update product (admin only)
- `DELETE /products/:id` - Delete product (admin only)

### Users
- `POST /auth/login` - Login
- `POST /auth/register` - Register
- `POST /auth/logout` - Logout
- `GET /auth/me` - Get current user

### Integration Services

#### CLONE HUB
- `POST /clone/analyze` - Analyze codebase
- `GET /clone/reports` - Get analysis reports

#### Ecosystem API
- `GET /ecosystem/status` - Get system status
- `POST /ecosystem/sync` - Trigger synchronization

#### Command Center
- `GET /command/dashboard` - Get dashboard data
- `POST /command/approve` - Approve action
- `POST /command/deny` - Deny action

## Response Format
```json
{
  "success": true,
  "data": {},
  "message": "Success",
  "timestamp": "2026-02-17T00:00:00Z"
}
```

## Error Codes
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Rate Limiting
- 100 requests per minute per IP
- 1000 requests per hour per user

## Webhooks
Configure webhooks for real-time updates:
```
POST /webhooks/register
{
  "url": "https://your-domain.com/webhook",
  "events": ["product.created", "product.updated"]
}
```
