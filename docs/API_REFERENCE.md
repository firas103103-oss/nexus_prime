# NEXUS PRIME API Reference

**Version:** 2.0.0-sovereign  
**Base URL (Cortex):** `http://localhost:8090/api/v1`  
**Base URL (Auth):** `http://localhost:8003/api/v1/auth`  
**Base URL (LiteLLM):** `http://localhost:4000`

---

## 🔑 Authentication

All API requests require valid JWT token in header:
```
Authorization: Bearer <your_jwt_token>
```

Get token from Auth service:
```bash
curl -X POST http://localhost:8003/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'
```

---

## 📡 NEXUS Cortex API

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "cortex": "online",
  "version": "2.0.0-sovereign",
  "db": "ok",
  "redis": "ok"
}
```

### Issue Command

```http
POST /commands
Content-Type: application/json

{
  "text": "Analyze sales data",
  "agent_id": "shadow7",
  "priority": "high",
  "context": {
    "user_id": "user-123"
  }
}
```

**Response:**
```json
{
  "command_id": "cmd-789",
  "status": "queued",
  "agent_id": "shadow7",
  "created_at": "2026-02-20T01:30:00Z"
}
```

### Get Command Status

```http
GET /commands/{command_id}
```

### Register Agent

```http
POST /agents/register
Content-Type: application/json

{
  "agent_id": "agent-001",
  "agent_type": "shadow7",
  "capabilities": ["data_analysis", "reporting"]
}
```

### List Agents

```http
GET /agents
```

### Post Event

```http
POST /events
Content-Type: application/json

{
  "event_type": "command_completed",
  "data": {
    "command_id": "cmd-789",
    "result": "Analysis complete"
  }
}
```

---

## 🔐 NEXUS Auth API

### Login

```http
POST /login
Content-Type: application/json

{
  "username": "admin",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbG...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

### Verify Token

```http
POST /verify
Content-Type: application/json

{
  "token": "eyJhbG..."
}
```

### Get JWKS

```http
GET /.well-known/jwks.json
```

**Response:**
```json
{
  "keys": [{
    "kty": "RSA",
    "kid": "nexus-key-1",
    "use": "sig",
    "alg": "RS256",
    "n": "...",
    "e": "AQAB"
  }]
}
```

---

## 🤖 LiteLLM API

OpenAI-compatible API.

### Chat Completion

```http
POST /v1/chat/completions
Content-Type: application/json
Authorization: Bearer sk-nexus-sovereign-mrf103

{
  "model": "gemini-1.5-flash",
  "messages": [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 500
}
```

**Response:**
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gemini-1.5-flash",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hello! How can I help?"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

### List Models

```http
GET /v1/models
```

### Health Check

```http
GET /health/liveliness
```

---

## 📊 Redis Pub/Sub Channels

### Subscribe to Events

```python
import redis

r = redis.Redis(host='localhost', port=6379)
pubsub = r.pubsub()
pubsub.subscribe('nexus:commands', 'nexus:events')

for message in pubsub.listen():
    print(message)
```

### Channels

- `nexus:commands` - Command routing messages
- `nexus:events` - System events
- `nexus:agents` - Agent status updates

---

## 🔢 Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

## 📝 Examples

### Full Workflow Example

```python
import requests

# 1. Login
auth_resp = requests.post(
    "http://localhost:8003/api/v1/auth/login",
    json={"username": "admin", "password": "pass"}
)
token = auth_resp.json()["access_token"]

# 2. Issue Command
cmd_resp = requests.post(
    "http://localhost:8090/api/v1/commands",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "text": "Generate report",
        "agent_id": "shadow7"
    }
)
command_id = cmd_resp.json()["command_id"]

# 3. Check Status
status_resp = requests.get(
    f"http://localhost:8090/api/v1/commands/{command_id}",
    headers={"Authorization": f"Bearer {token}"}
)
print(status_resp.json())

# 4. AI Chat
ai_resp = requests.post(
    "http://localhost:4000/v1/chat/completions",
    headers={"Authorization": "Bearer sk-nexus-sovereign-mrf103"},
    json={
        "model": "gemini-1.5-flash",
        "messages": [{"role": "user", "content": "Summarize data"}]
    }
)
print(ai_resp.json())
```

---

For more examples, see [examples/](../examples/) directory.
