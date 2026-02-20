# 🎨 NEXUS PRIME Architecture

Complete system architecture documentation with flow diagrams and component details.

---

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     External Users/Clients                      │
└────────────┬───────────────────────────────────────┬────────────┘
             │                                       │
    ┌────────▼────────┐                    ┌────────▼────────┐
    │   Web Clients   │                    │   API Clients   │
    │  (Browser/App)  │                    │  (REST/WebSocket)│
    └────────┬────────┘                    └────────┬────────┘
             │                                       │
             └───────────────┬───────────────────────┘
                             │
                ┌────────────▼────────────┐
                │   API Gateway Layer     │
                │  (NGINX/Traefik/Ingress)│
                └────────────┬────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼─────┐      ┌─────▼──────┐     ┌─────▼──────┐
    │  Cortex  │      │    Auth    │     │  LiteLLM   │
    │  (8090)  │      │   (8003)   │     │   (4000)   │
    └────┬─────┘      └─────┬──────┘     └─────┬──────┘
         │                   │                   │
         └──────────┬────────┴──────────┬────────┘
                    │                   │
             ┌──────▼──────┐     ┌─────▼──────┐
             │    Redis    │     │   Ollama   │
             │   (6379)    │     │  (11434)   │
             └──────┬──────┘     └─────┬──────┘
                    │                   │
             ┌──────▼───────────────────▼──────┐
             │       PostgreSQL 15              │
             │          (5432)                  │
             └──────────────────────────────────┘
```

---

## 🧩 Component Breakdown

### 1. NEXUS Cortex (Command Router)

**Purpose:** Central nervous system for command routing and agent coordination

**Technology:**
- FastAPI (Python 3.12)
- asyncpg (PostgreSQL async driver)
- redis-py (Redis client)
- WebSockets for real-time

**Responsibilities:**
- Receive commands from users/agents
- Route commands to appropriate agents
- Track command execution status
- Broadcast events to subscribers
- Maintain agent registry

**Key Features:**
- Async/await for non-blocking I/O
- Connection pooling (5-20 connections)
- Redis Pub/Sub for event distribution
- Health monitoring endpoint
- CORS support for web clients

**API Endpoints:**
- `POST /api/v1/commands` - Issue command
- `GET /api/v1/commands/{id}` - Get status
- `POST /api/v1/agents/register` - Register agent
- `GET /api/v1/agents` - List agents
- `POST /api/v1/events` - Post event
- `GET /health` - Health check

---

### 2. NEXUS Auth (Authentication Service)

**Purpose:** RS256 JWT authentication and authorization

**Technology:**
- FastAPI (Python 3.12)
- cryptography (RSA)
- PyJWT (JWT handling)
- PostgreSQL for user storage

**Responsibilities:**
- User authentication
- JWT token generation (RS256)
- Token verification
- JWKS endpoint for public key
- Session management

**Key Features:**
- 2048-bit RSA keypair
- Runtime key generation
- JWKS standard compliance
- 24-hour token expiry
- Key rotation support

**API Endpoints:**
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/verify` - Verify token
- `GET /api/v1/auth/.well-known/jwks.json` - Public keys
- `GET /api/v1/auth/health` - Health check

---

### 3. LiteLLM Proxy (AI Gateway)

**Purpose:** Universal AI model gateway for 100% data sovereignty

**Technology:**
- LiteLLM (Python)
- OpenAI-compatible API
- Model routing engine

**Responsibilities:**
- Route all AI requests to local Ollama
- Provide OpenAI-compatible interface
- Support multiple model formats
- Handle authentication

**Supported Models (mapped to local):**
- Gemini (1.5-flash, 2.5-flash, 3-flash, pro)
- GPT (gpt-4o, gpt-4o-mini, gpt-4)
- Claude (claude-3-5-sonnet)

**Configuration:**
```yaml
model_list:
  - model_name: gemini-1.5-flash
    litellm_params:
      model: ollama/llama3.2:3b
      api_base: http://nexus_ollama:11434
```

---

### 4. Redis (Event Bus)

**Purpose:** Real-time event distribution and caching

**Technology:**
- Redis 7 (Alpine)
- Pub/Sub messaging
- In-memory data store

**Channels:**
- `nexus:commands` - Command routing
- `nexus:events` - System events
- `nexus:agents` - Agent updates

**Configuration:**
- AOF persistence
- 256MB maxmemory
- allkeys-lru eviction

---

### 5. Ollama (LLM Engine)

**Purpose:** Local AI model inference (100% data sovereignty)

**Model:** llama3.2:3b (8K context)

**Features:**
- CPU/GPU support
- OpenAI-compatible API
- Model hot-swapping
- Streaming responses

---

### 6. PostgreSQL (Primary Database)

**Purpose:** Persistent data storage

**Schema:** nexus_core

**Key Tables:**
- `agents` - Agent registry
- `commands` - Command history
- `events` - Event log
- `agent_state` - Agent state
- `routing_rules` - Routing configuration
- `human_sessions` - User sessions
- `users` - User accounts

---

## 🔄 Data Flow

### Command Execution Flow

```
1. User → Dashboard → Cortex
   POST /api/v1/commands
   {
     "text": "Analyze data",
     "agent_id": "shadow7"
   }

2. Cortex → PostgreSQL
   INSERT INTO commands (text, agent_id, status)
   VALUES ('Analyze data', 'shadow7', 'queued')

3. Cortex → Redis
   PUBLISH nexus:commands {
     "command_id": "cmd-123",
     "agent_id": "shadow7"
   }

4. Shadow7 Agent → Subscribe
   SUBSCRIBE nexus:commands
   Receives: cmd-123

5. Agent → Process → Complete

6. Agent → Cortex
   POST /api/v1/commands/cmd-123/complete
   {"result": "Analysis done"}

7. Cortex → Redis
   PUBLISH nexus:events {
     "type": "command_completed",
     "command_id": "cmd-123"
   }

8. Dashboard → Receives event via WebSocket
   Updates UI in real-time
```

---

## 🔐 Security Architecture

### Authentication Flow

```
1. User → Auth Service
   POST /api/v1/auth/login
   {"username": "admin", "password": "***"}

2. Auth → Verify credentials

3. Auth → Generate RS256 JWT
   - Sign with private key (private.pem)
   - Include kid: nexus-key-1
   - Set expiry: 24 hours

4. Auth → Return JWT
   {"access_token": "eyJhbG...", "expires_in": 86400}

5. User → Make API request with JWT
   Authorization: Bearer eyJhbG...

6. Service → Verify JWT
   - Get public key from JWKS endpoint
   - Verify signature with public key
   - Check expiry timestamp
   - Extract claims (user_id, roles)

7. Service → Process authorized request
```

### Data Sovereignty Architecture

```
┌─────────────────────────────────────┐
│     External AI APIs (Blocked)      │
│  ❌ Google Gemini API               │
│  ❌ OpenAI GPT API                  │
│  ❌ Anthropic Claude API            │
└─────────────────────────────────────┘
               ↑ (No connection)
               │
┌──────────────┴──────────────────────┐
│       LiteLLM Proxy (Gateway)       │
│  ✅ Intercepts all AI requests      │
│  ✅ Routes to local Ollama          │
│  ✅ OpenAI-compatible interface     │
└──────────────┬──────────────────────┘
               ↓ (Local network only)
┌──────────────▼──────────────────────┐
│       Ollama (Local LLM)            │
│  ✅ llama3.2:3b running locally     │
│  ✅ No external network access      │
│  ✅ 100% data remains on premises   │
└─────────────────────────────────────┘
```

---

## 📊 Scalability Architecture

### Horizontal Scaling

```
┌────────────────────────────────────┐
│         Load Balancer              │
│    (Traefik/NGINX/K8s Ingress)    │
└───────┬────────────────┬───────────┘
        │                │
    ┌───▼───┐        ┌───▼───┐
    │Cortex │        │Cortex │  ... (Auto-scale 3-10 replicas)
    │Pod 1  │        │Pod 2  │
    └───┬───┘        └───┬───┘
        │                │
        └────────┬───────┘
                 │
         ┌───────▼───────┐
         │  Redis Cluster │
         │  (Shared State)│
         └───────┬───────┘
                 │
         ┌───────▼───────┐
         │  PostgreSQL   │
         │  (Primary+Replicas)
         └───────────────┘
```

### Kubernetes Deployment

**HPAs (Horizontal Pod Autoscalers):**
- Cortex: 3→10 pods at 70% CPU
- LiteLLM: 2→8 pods at 70% CPU
- Auth: 2→6 pods at 75% CPU

**Resource Limits:**
```yaml
Cortex:
  requests: {cpu: 250m, memory: 256Mi}
  limits: {cpu: 500m, memory: 512Mi}

LiteLLM:
  requests: {cpu: 500m, memory: 512Mi}
  limits: {cpu: 1000m, memory: 2Gi}

Auth:
  requests: {cpu: 200m, memory: 128Mi}
  limits: {cpu: 400m, memory: 256Mi}
```

---

## 🚀 Performance Optimization

### Caching Strategy

1. **Redis Cache:**
   - Agent status (TTL: 60s)
   - Command results (TTL: 300s)
   - User sessions (TTL: 24h)
   - JWKS public keys (TTL: 3600s)

2. **Database Connection Pool:**
   - Min: 5 connections
   - Max: 20 connections
   - Overflow: 10 connections
   - Timeout: 30s

3. **Async Operations:**
   - All I/O operations non-blocking (asyncio)
   - Background tasks for heavy work
   - WebSocket for real-time updates
   - Pub/Sub for event distribution

---

## 📈 Monitoring & Observability

### Metrics Collection

```
Application     →  Prometheus  →  Grafana
  ↓ /metrics         ↓ Scrape       ↓ Visualize
Health Checks      Time Series    Dashboards
Counters           Storage         Alerts
Gauges            (15 days)      (Real-time)
Histograms
```

### Key Metrics

**Cortex:**
- `cortex_request_count` - Total API requests
- `cortex_response_time` - Response latency
- `cortex_active_commands` - Commands in progress
- `cortex_agent_count` - Registered agents

**Redis:**
- `redis_connection_count` - Active connections
- `redis_pub_sub_channels` - Active channels
- `redis_memory_usage` - Memory consumption
- `redis_ops_per_sec` - Operations/second

**PostgreSQL:**
- `postgres_query_time` - Query execution time
- `postgres_connection_count` - Active connections
- `postgres_transaction_rate` - Transactions/second
- `postgres_cache_hit_ratio` - Cache efficiency

**Ollama:**
- `ollama_inference_time` - Model inference latency
- `ollama_token_count` - Tokens generated
- `ollama_queue_length` - Pending requests
- `ollama_gpu_memory` - GPU memory usage

---

## 🔧 Technology Stack

| Layer | Technology | Purpose |
|-------|----------|---------|
| **Frontend** | React, TypeScript, Tailwind | User interfaces |
| **API** | FastAPI, Python 3.12 | REST/WebSocket APIs |
| **Auth** | RS256 JWT, JWKS | Authentication |
| **Event Bus** | Redis Pub/Sub | Real-time events |
| **Database** | PostgreSQL 15 | Primary storage |
| **AI** | Ollama (llama3.2:3b), LiteLLM | Local LLM inference |
| **Container** | Docker, Docker Compose | Containerization |
| **Orchestration** | Kubernetes, K3s | Auto-scaling |
| **Monitoring** | Prometheus, Grafana | Observability |
| **Proxy** | Traefik, NGINX | Load balancing |

---

## 📁 Directory Structure

```
NEXUS_PRIME_UNIFIED/
├── docker-compose.yml          # Main orchestration
├── .env                         # Environment variables
├── README.md                    # Main documentation
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
│
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md          # This file
│   ├── API_REFERENCE.md         # API endpoints
│   ├── DEPLOYMENT_GUIDE.md      # Deployment instructions
│   └── QUICKSTART.md            # Quick start guide
│
├── k8s-manifests/               # Kubernetes manifests
│   ├── namespace.yaml
│   ├── cortex-deployment.yaml
│   ├── auth-deployment.yaml
│   ├── litellm-deployment.yaml
│   ├── redis-deployment.yaml
│   ├── ollama-deployment.yaml
│   ├── postgres-statefulset.yaml
│   └── ingress.yaml
│
├── data/                        # Persistent data
│   ├── db_data/                 # PostgreSQL data
│   ├── redis_data/              # Redis data
│   ├── ollama/                  # Ollama models
│   └── auth_keys/               # RSA keypairs
│
├── nexus_cortex/                # Cortex service
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── products/                    # Products symlink
│   └── nexus-data-core/        # Auth service
│       └── auth-service/
│
└── scripts/                     # Utility scripts
    ├── backup.sh
    ├── restore.sh
    └── health-check.sh
```

---

## 🛣️ Request Flow Examples

### 1. User Login Flow

```
User Browser
    │
    ├─► POST /api/v1/auth/login
    │   Body: {"username": "admin", "password": "***"}
    │
    └─► Auth Service (Port 8003)
        │
        ├─► Query PostgreSQL
        │   SELECT * FROM users WHERE username='admin'
        │
        ├─► Verify bcrypt password
        │
        ├─► Generate RS256 JWT
        │   - Load private.pem
        │   - Sign payload with RS256
        │   - Set expiry: 24h
        │
        └─► Return Response
            {"access_token": "eyJ...", "expires_in": 86400}
```

### 2. AI Chat Request Flow

```
User Application
    │
    ├─► POST /v1/chat/completions
    │   Headers: Authorization: Bearer ey...
    │   Body: {"model": "gpt-4o", "messages": [...]}
    │
    └─► LiteLLM Proxy (Port 4000)
        │
        ├─► Verify master key
        │
        ├─► Lookup model mapping
        │   gpt-4o → ollama/llama3.2:3b
        │
        ├─► POST to Ollama (Port 11434)
        │   /api/generate
        │   Body: {"model": "llama3.2:3b", "prompt": "..."}
        │
        ├─► Ollama generates response
        │   Uses local LLM weights
        │   No external API calls
        │
        └─► Return OpenAI-format response
            {"choices": [{"message": {"content": "..."}}]}
```

### 3. Command Execution Flow

```
Dashboard
    │
    ├─► POST /api/v1/commands
    │   Headers: Authorization: Bearer ey...
    │   Body: {"text": "Analyze sales data", "agent_id": "shadow7"}
    │
    └─► Cortex (Port 8090)
        │
        ├─► Verify JWT with Auth JWKS
        │   GET http://nexus_auth:8003/.well-known/jwks.json
        │
        ├─► Insert to PostgreSQL
        │   INSERT INTO commands (text, agent_id, status, created_at)
        │   Returns command_id = "cmd-xyz"
        │
        ├─► Publish to Redis
        │   PUBLISH nexus:commands '{"command_id": "cmd-xyz", ...}'
        │
        └─► Return Response
            {"command_id": "cmd-xyz", "status": "queued"}

Agent (Shadow7)
    │
    └─► SUBSCRIBE nexus:commands
        │
        ├─► Receives: {"command_id": "cmd-xyz"}
        │
        ├─► Process command
        │   - Fetch data from database
        │   - Perform analysis
        │   - Generate report
        │
        └─► POST /api/v1/commands/cmd-xyz/complete
            Body: {"result": "Analysis complete", "data": {...}}
            │
            └─► Cortex updates PostgreSQL
                UPDATE commands SET status='completed', result='...'
                │
                └─► Publish to Redis
                    PUBLISH nexus:events '{"type": "command_completed", ...}'
                    │
                    └─► Dashboard receives via WebSocket
                        Updates UI in real-time
```

---

## 🏗️ Deployment Architectures

### 1. Development (Docker Compose)

```
Single Host Machine
├── Docker Daemon
    ├── nexus_db (PostgreSQL)
    ├── nexus_redis (Redis)
    ├── nexus_ollama (Ollama)
    ├── nexus_litellm (LiteLLM)
    ├── nexus_cortex (Cortex API)
    ├── nexus_auth (Auth API)
    └── nexus_dashboard (Web UI)

Access: localhost:8090, localhost:4000, localhost:8003
```

### 2. Production (Kubernetes)

```
Kubernetes Cluster
├── Namespace: nexus-prime
    ├── cortex (Deployment, 3 replicas, HPA 3-10)
    ├── auth (Deployment, 2 replicas, HPA 2-6)
    ├── litellm (Deployment, 2 replicas, HPA 2-8)
    ├── redis (StatefulSet, 1 replica)
    ├── ollama (StatefulSet, 1 replica, GPU)
    ├── postgres (StatefulSet, 1 replica, PV)
    ├── dashboard (Deployment, 2 replicas)
    └── Ingress (Traefik/NGINX)
        ├── cortex.nexus.example.com
        ├── auth.nexus.example.com
        ├── ai.nexus.example.com
        └── dashboard.nexus.example.com

Access: https://dashboard.nexus.example.com
```

---

## 🔐 Security Best Practices

1. **JWT Security:**
   - RS256 algorithm (asymmetric)
   - 2048-bit RSA keys
   - 24-hour token expiry
   - Key rotation support
   - JWKS standard compliance

2. **Network Security:**
   - All services in private network
   - NGINX/Traefik reverse proxy
   - TLS/SSL termination
   - CORS configuration
   - Rate limiting

3. **Data Security:**
   - PostgreSQL password authentication
   - Redis requirepass
   - Environment variables for secrets
   - No secrets in codebase
   - Volume encryption (optional)

4. **API Security:**
   - JWT bearer authentication
   - Master key for LiteLLM
   - Input validation
   - SQL injection protection
   - XSS protection

---

## 📚 Related Documentation

- [API Reference](API_REFERENCE.md) - Complete API endpoint documentation
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Production deployment instructions
- [Quick Start](QUICKSTART.md) - Get started in 5 minutes
- [Main README](../README.md) - Project overview

---

**Version:** 2.0.0-sovereign  
**Last Updated:** February 2026  
**License:** MIT

