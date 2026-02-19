# 🌌 NEXUS PRIME

<div align="center">

![Version](https://img.shields.io/badge/version-2.6.2-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Docker](https://img.shields.io/badge/docker-11%20services-blue)
![License](https://img.shields.io/badge/license-Proprietary-red)

**Complete AI-Powered Sovereign Digital Ecosystem**

[العربية](docs/README_AR.md) | English

</div>

---

## 🎯 What is NEXUS PRIME?

NEXUS PRIME is a unified, self-hosted AI ecosystem that consolidates multiple AI-powered products, automation workflows, and intelligent agents into one cohesive platform. It was created to bring order to 105GB of scattered projects, resulting in a lean 3.9GB organized system.

### Core Philosophy
- **Sovereignty**: Complete ownership and control over your AI infrastructure
- **Unity**: One platform, multiple AI-powered products
- **Intelligence**: 12 specialized AI agents (Planets) working in harmony
- **Automation**: n8n workflows for lead capture, nurturing, and onboarding

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone git@github.com:firas103103-oss/nexus_prime.git
cd NEXUS_PRIME_UNIFIED

# Launch all services
bash scripts/IGNITION.sh

# Check system status
bash scripts/STATUS.sh

# Run comprehensive tests
bash scripts/final_test.sh
```

---

## 📦 Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      NEXUS PRIME v2.2.0                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Ollama    │  │  Open-WebUI │  │     n8n     │          │
│  │  (Brain)    │  │ (Interface) │  │(Automation) │          │
│  │ Port 11434  │  │  Port 3000  │  │  Port 5678  │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
│         │                │                │                  │
│         └────────────────┴────────────────┘                  │
│                          │                                   │
│  ┌───────────────────────┴───────────────────────┐          │
│  │              PostgreSQL Database               │          │
│  │                  Port 5432                     │          │
│  └────────────────────────────────────────────────┘          │
│                                                              │
│  ┌────────────────────────────────────────────────┐          │
│  │                 12 AI Planets                  │          │
│  │  AI-ARCH · AS-SULTAN · CLONE-HUB · LEGAL-EAGLE │          │
│  │  NAV-ORACLE · NEXUS-ANALYST · N-TARGET · OPS   │          │
│  │  RAG-CORE · SEC-GUARD · SHADOW-7 · X-BIO       │          │
│  └────────────────────────────────────────────────┘          │
│                                                              │
│  ┌────────────────────────────────────────────────┐          │
│  │               7 Products Suite                 │          │
│  │  Shadow Seven · AlSultan · Jarvis · Imperial   │          │
│  │  MRF103 Mobile · X-BIO Sentinel · Data Core    │          │
│  └────────────────────────────────────────────────┘          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🐳 Docker Services

| Service | Container | Port | Description |
|---------|-----------|------|-------------|
| **Database** | nexus_db | 5432 | PostgreSQL 15.1 (Supabase) |
| **Brain** | nexus_ollama | 11434 | Ollama LLM Engine (llama3.2, qwen2.5:14b) |
| **Interface** | nexus_ai | 3000→8080 | Open-WebUI Chat Interface |
| **Automation** | nexus_flow | 5678 | n8n Workflow Engine |
| **Voice** | nexus_voice | 5050→8000 | Edge-TTS Text-to-Speech |

```bash
# Status
docker ps

# Restart all
cd /root/nexus_prime && docker compose restart

# Logs
docker logs -f nexus_ai
```

---

## 🪐 The 12 Planets (AI Agents)

Each "Planet" is a specialized AI agent with its own identity and purpose:

| Planet | Role | Specialty |
|--------|------|-----------|
| **AI-ARCH** | AI Architecture | System design, ARC-Namer protocol |
| **AS-SULTAN** | Quranic Analysis | Islamic text interpretation |
| **CLONE-HUB** | Repository Management | Code cloning and versioning |
| **LEGAL-EAGLE** | Legal Affairs | Contracts, compliance |
| **NAV-ORACLE** | Navigation | User journey optimization |
| **NEXUS-ANALYST** | Data Analysis | Business intelligence |
| **N-TARGET** | Business Targeting | Lead identification |
| **OPS-CTRL** | Operations Control | System monitoring |
| **RAG-CORE** | Knowledge Engine | RAG-based retrieval |
| **SEC-GUARD** | Security | Threat detection |
| **SHADOW-7** | Publishing | AI content distribution |
| **X-BIO** | IoT Biomedical | ESP32 sensor integration |

---

## 📦 7 Products

| Product | Tech Stack | Description |
|---------|------------|-------------|
| **Shadow Seven Publisher** | Python + AI | AI-powered publishing platform |
| **AlSultan Intelligence** | Python + Gemini | Quranic analysis (Chronos, Decoder, Identity) |
| **Jarvis Control Hub** | Python + FastAPI | Central monitoring and coordination |
| **Imperial UI** | React + Vite + Tailwind | Admin dashboard interface |
| **MRF103 Mobile** | React Native + Expo | Mobile application |
| **X-BIO Sentinel** | Python + ESP32 | Biomedical IoT monitoring |
| **NEXUS Data Core** | Python | Unified data processing engine |

---

## 🔗 Integrations

```
integration/
├── admin-portal/      # Unified admin interface
├── clone-hub/         # Repository management
├── command-center/    # Central command dispatch
├── ecosystem-api/     # Unified REST API
└── shared-auth/       # SSO authentication
```

---

## 🌐 Domains & SSL

**Primary:** `mrf103.com` (Cloudflare + Let's Encrypt Wildcard)

| Subdomain | Service |
|-----------|---------|
| `ai.mrf103.com` | Open-WebUI |
| `flow.mrf103.com` | n8n Automation |
| `voice.mrf103.com` | Edge-TTS |
| `publisher.mrf103.com` | Shadow Seven |
| `sultan.mrf103.com` | AlSultan |
| `admin.mrf103.com` | Dashboard |

---

## 🔧 Scripts

| Script | Purpose |
|--------|---------|
| `IGNITION.sh` | Full system launch |
| `STATUS.sh` | Quick status report |
| `final_test.sh` | Comprehensive testing (41 tests) |
| `git_sync_all.sh` | Sync all products to GitHub |
| `setup_dns.sh` | Configure Cloudflare DNS |
| `monitor.sh` | Service monitoring |

---

## 📊 Stats

| Metric | Value |
|--------|-------|
| Total Files | ~55,000+ |
| System Size | 3.9 GB |
| Active Repos | 9 |
| Products | 7 |
| AI Planets | 12 |
| Docker Services | 5 |
| Test Score | 100% (41/41) ✅ |
| Space Freed | 13 GB |

---

## 📚 Documentation

- [MASTER_DOCUMENTATION.md](MASTER_DOCUMENTATION.md) - Complete reference (Arabic)
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Technical architecture
- [QUICKSTART.md](docs/QUICKSTART.md) - Getting started guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions

---

## 🔒 Security

- ✅ All API keys use environment variables
- ✅ UFW firewall with Cloudflare IP whitelist
- ✅ Internal services blocked from external access
- ✅ SSL/TLS via Let's Encrypt wildcard
- ✅ Shell injection vulnerabilities patched

---

## 📝 License

Proprietary - All rights reserved by MrF

---

## 🤝 Contact

- **GitHub:** [firas103103-oss](https://github.com/firas103103-oss)
- **Domain:** [mrf103.com](https://mrf103.com)
- **Email:** admin@mrf103.com

---

<div align="center">

**NEXUS PRIME v2.2.0** - Built with 💜 by MrF

*Last updated: February 18, 2026*

</div>
