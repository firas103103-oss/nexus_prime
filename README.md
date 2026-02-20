# 🧠 NEXUS PRIME - Command Intelligence Platform

<div align="center">

![NEXUS PRIME](https://img.shields.io/badge/NEXUS-PRIME-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/version-2.0.0--sovereign-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)
![Data Sovereignty](https://img.shields.io/badge/Data%20Sovereignty-100%25-success?style=for-the-badge)

**المنصة الذكية للقيادة والتحكم | Enterprise Command Intelligence Platform**

[Documentation](#-documentation) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [API Reference](#-api-reference) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Deployment](#-deployment)
- [Monitoring](#-monitoring)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**NEXUS PRIME** is an enterprise-grade command intelligence platform that provides **100% data sovereignty** for AI-powered applications. It combines real-time event processing, secure authentication, and local AI inference to deliver a complete solution for organizations requiring full control over their data.

### 🌟 Why NEXUS PRIME?

- **🔒 100% Data Sovereignty**: All AI processing happens locally - zero external API calls
- **⚡ Real-time Processing**: Redis-powered event bus for instant command routing
- **🛡️ Enterprise Security**: RS256 JWT with JWKS endpoint support
- **📈 Production Ready**: Built for 1K-100K concurrent users
- **🚀 Cloud Native**: Kubernetes-ready with auto-scaling
- **🔧 Developer Friendly**: OpenAPI documentation, Docker Compose for local dev

---

## ✨ Key Features

### 🤖 AI & Intelligence

- **Local LLM Engine**: Ollama-powered (llama3.2:3b, 8K context)
- **LiteLLM Proxy**: Universal AI gateway supporting 9+ model formats
- **Model Agnostic**: Gemini, GPT, Claude API compatibility
- **Zero Latency**: No external API calls = faster responses

### 🔄 Event Processing

- **Redis Pub/Sub**: Real-time event bus with 3 channels
- **Command Routing**: Intelligent agent task distribution
- **Event Streaming**: WebSocket support for live updates
- **State Management**: Persistent agent state tracking

### 🔐 Security & Auth

- **RS256 JWT**: Asymmetric cryptography (2048-bit RSA)
- **JWKS Endpoint**: Standard key distribution
- **Key Rotation**: Built-in support for zero-downtime rotation
- **Session Management**: Secure user session handling

### 📊 Monitoring & Observability

- **Health Checks**: All services expose `/health` endpoints
- **Metrics Ready**: Prometheus-compatible metrics
- **Structured Logging**: JSON logs for easy parsing
- **Dashboard Integration**: Grafana-ready

### 🎨 User Interfaces

- **Cognitive Boardroom**: AI-powered meeting assistant (Port 8501)
- **Command Dashboard**: Real-time operations center (Port 5001)
- **Voice Interface**: Natural language control (Port 5050)
- **Open WebUI**: Chat interface for AI models (Port 3000)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        NEXUS PRIME v2.0.0                       │
│                   Command Intelligence Platform                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
        │   Cortex     │ │    Auth    │ │  LiteLLM   │
        │   (8090)     │ │   (8003)   │ │   (4000)   │
        │              │ │            │ │            │
        │ Command      │ │ RS256 JWT  │ │ AI Proxy   │
        │ Router       │ │ + JWKS     │ │ Sovereign  │
        └──────┬───────┘ └─────┬──────┘ └─────┬──────┘
               │               │               │
               └───────┬───────┴───────┬───────┘
                       │               │
                ┌──────▼──────┐ ┌─────▼──────┐
                │    Redis    │ │  Ollama    │
                │   (6379)    │ │  (11434)   │
                │             │ │            │
                │  Event Bus  │ │ LLM Engine │
                │  Pub/Sub    │ │ llama3.2   │
                └──────┬──────┘ └─────┬──────┘
                       │               │
                ┌──────▼───────────────▼──────┐
                │      PostgreSQL 15          │
                │         (5432)              │
                │                             │
                │   Central Data Store        │
                └─────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼─────┐ ┌─────▼──────┐ ┌────▼─────┐
│ Boardroom   │ │ Dashboard  │ │  Voice   │
│   (8501)    │ │   (5001)   │ │  (5050)  │
└─────────────┘ └────────────┘ └──────────┘
```

### 📦 Components

| Component | Version | Port | Purpose |
|-----------|---------|------|---------|
| **NEXUS Cortex** | 2.0.0-sovereign | 8090 | Command routing & agent coordination |
| **NEXUS Auth** | 2.0.0-rs256 | 8003 | RS256 JWT authentication service |
| **LiteLLM Proxy** | main-latest | 4000 | AI sovereignty gateway |
| **Redis** | 7-alpine | 6379 | Event bus & real-time pub/sub |
| **Ollama** | latest | 11434 | Local LLM inference engine |
| **PostgreSQL** | 15.1.0.147 | 5432 | Primary data store |
| **Boardroom AI** | 1.0.0 | 8501 | Meeting intelligence |
| **Dashboard** | 1.0.0 | 5001 | Command center UI |
| **Voice Assistant** | 1.0.0 | 5050 | Voice interface |
| **Open WebUI** | main | 3000 | AI chat interface |
| **n8n** | latest | 5678 | Workflow automation |
| **Shadow7 API** | 1.0.0 | 8002 | Publishing platform |

---

## 🚀 Quick Start

### Prerequisites

- Docker 24.0+ & Docker Compose v2.20+
- 16GB RAM minimum (23GB recommended)
- 4 CPU cores minimum (6 recommended)
- 50GB disk space

### One-Command Launch

```bash
git clone https://github.com/mrf103/nexus-prime.git
cd nexus-prime
docker compose up -d
```

**That's it!** 🎉 All 12 services will start automatically.

### Verify Installation

```bash
# Check all containers
docker compose ps

# Test health endpoints
curl localhost:8090/health              # Cortex
curl localhost:4000/health/liveliness   # LiteLLM
curl localhost:8003/api/v1/auth/health  # Auth
```

### Access UIs

- **Dashboard**: http://localhost:5001
- **Boardroom AI**: http://localhost:8501
- **Open WebUI**: http://localhost:3000
- **n8n Workflows**: http://localhost:5678
- **Voice Interface**: http://localhost:5050

---

## 💻 System Requirements

### Minimum Requirements

```yaml
CPU: 4 cores
RAM: 16 GB
Disk: 50 GB SSD
Network: 100 Mbps
OS: Linux (Ubuntu 20.04+), macOS 12+
```

### Recommended (Production)

```yaml
CPU: 6-8 cores
RAM: 23-32 GB
Disk: 100 GB NVMe SSD
Network: 1 Gbps
OS: Ubuntu 22.04 LTS
```

---

## 📥 Installation

See [INSTALLATION.md](docs/INSTALLATION.md) for detailed instructions.

---

## ⚙️ Configuration

See [CONFIGURATION.md](docs/CONFIGURATION.md) for all configuration options.

---

## 📖 Usage

See [API_REFERENCE.md](docs/API_REFERENCE.md) for complete API documentation.

---

## 🚢 Deployment

See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for production deployment instructions.

---

## 📊 Monitoring

See [MONITORING.md](docs/MONITORING.md) for monitoring setup and best practices.

---

## 🔒 Security

See [SECURITY.md](docs/SECURITY.md) for security guidelines and best practices.

---

## 🐛 Troubleshooting

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues and solutions.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 📞 Support

- **Documentation**: Full documentation in `/docs` directory
- **Issues**: [GitHub Issues](https://github.com/mrf103/nexus-prime/issues)
- **Email**: support@mrf103.com

---

<div align="center">

**⭐ Star us on GitHub if you find NEXUS PRIME useful! ⭐**

Made with ❤️ by MRF103 Team

[Website](https://mrf103.com) • [Documentation](docs/) • [API Reference](docs/API_REFERENCE.md)

</div>
