# 🌐 NEXUS PRIME - دليل جميع الخدمات والمواقع

**التاريخ**: 18 فبراير 2026  
**Public IP**: 46.224.225.96  
**Status**: 🟢 All Systems Operational (93%)

---

## 🎯 روابط سريعة - Quick Access

| Service | Public URL | Local URL | Status |
|---------|-----------|-----------|--------|
| **AI Chat** | https://ai.mrf103.com | http://localhost:3000 | ✅ |
| **Frontend** | https://prime.mrf103.com | http://localhost:5173 | ✅ |
| **Workflows** | https://flow.mrf103.com | http://localhost:5678 | ✅ |
| **Voice** | https://voice.mrf103.com | http://localhost:5050 | ✅ |
| **API Docs** | - | http://localhost:8005/docs | ✅ |

---

## 📋 جميع الخدمات بالتفصيل

### 1️⃣ Open WebUI - واجهة الذكاء الاصطناعي

**الروابط المتاحة:**
- 🔗 https://ai.mrf103.com ✨ NEW
- 🔗 https://chat.mrf103.com
- 🔗 https://nexus.mrf103.com
- 🔗 http://localhost:3000
- 🔗 http://46.224.225.96:3000

**المعلومات التقنية:**
- **Container**: nexus_ai
- **Port Mapping**: 3000 → 8080
- **Internal IP**: 172.23.0.7
- **Uptime**: 23+ hours
- **Health**: ✅ Healthy
- **Features**:
  - Chat with AI models
  - Conversation history
  - Model management
  - Real-time responses
  - WebSocket support

**كيفية الاستخدام:**
1. افتح أي من الروابط أعلاه
2. سجل دخول أو أنشئ حساب
3. ابدأ المحادثة مع الـ AI

---

### 2️⃣ NEXUS PRIME Frontend - الواجهة الأمامية

**الروابط المتاحة:**
- 🔗 https://prime.mrf103.com ✨ NEW
- 🔗 http://localhost:5173
- 🔗 http://46.224.225.96:5173

**المعلومات التقنية:**
- **Framework**: React 18 + Vite 5.4.21
- **Port**: 5173 (bound to 0.0.0.0)
- **Process**: PID 2973950
- **Build Time**: 173ms
- **Features**:
  - Modern React UI
  - Tailwind CSS styling
  - Framer Motion animations
  - Recharts for data visualization
  - Hot Module Replacement (HMR)
  - Lucide React icons

**Dependencies:**
- react: 18.2.0
- react-dom: 18.2.0
- framer-motion: 11.0.8
- recharts: 2.12.2
- lucide-react: 0.344.0

---

### 3️⃣ Backend API - واجهة البرمجة الخلفية

**الروابط المتاحة:**
- 🔗 http://localhost:8005
- 🔗 http://localhost:8005/docs (Swagger UI)
- 🔗 http://localhost:8005/redoc (ReDoc)
- 🔗 http://localhost:8005/openapi.json

**المعلومات التقنية:**
- **Framework**: FastAPI
- **Version**: 2.3.0
- **Port**: 8005
- **Process**: PID 2921681
- **API Title**: NEXUS PRIME Core
- **Endpoints**: 4 main routes
- **Documentation**: Auto-generated (OpenAPI 3.0)

**الـ Endpoints:**
```bash
GET  /docs      # Swagger UI
GET  /redoc     # ReDoc documentation
GET  /openapi.json  # OpenAPI schema
# + 1 more custom endpoint
```

---

### 4️⃣ n8n Workflow Automation - أتمتة سير العمل

**الروابط المتاحة:**
- 🔗 https://flow.mrf103.com
- 🔗 https://n8n.mrf103.com
- 🔗 http://localhost:5678
- 🔗 http://localhost:5678/healthz

**المعلومات التقنية:**
- **Container**: nexus_flow
- **Port Mapping**: 5678 → 5678
- **Internal IP**: 172.23.0.3
- **Uptime**: 4+ hours
- **Health**: {"status":"ok"}

**الميزات:**
- Visual workflow editor
- 350+ app integrations
- Webhook support
- Scheduled workflows
- Database connections
- API access
- Custom code execution (JavaScript)

**استخدامات شائعة:**
1. Automate data synchronization
2. Connect multiple APIs
3. Schedule notifications
4. Process webhooks
5. Data transformation
6. Email automation

---

### 5️⃣ Ollama AI Engine - محرك الذكاء الاصطناعي

**الروابط المتاحة:**
- 🔗 http://localhost:11434
- 🔗 http://localhost:11434/api/version
- 🔗 http://localhost:11434/api/tags
- 🔗 http://46.224.225.96:11434

**المعلومات التقنية:**
- **Container**: nexus_ollama
- **Version**: 0.16.1
- **Port Mapping**: 11434 → 11434
- **Internal IP**: 172.23.0.5
- **Shared Memory**: 16GB
- **Uptime**: 23+ hours

**API Endpoints:**
```bash
GET  /api/version          # Get Ollama version
GET  /api/tags             # List available models
POST /api/generate         # Generate completion
POST /api/chat             # Chat completion
POST /api/embeddings       # Generate embeddings
POST /api/pull             # Pull a model
POST /api/push             # Push a model
POST /api/create           # Create custom model
DELETE /api/delete         # Delete a model
```

**Example Usage:**
```bash
# Check version
curl http://localhost:11434/api/version

# List models
curl http://localhost:11434/api/tags

# Generate text
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"
}'
```

---

### 6️⃣ Voice Service - خدمة الصوت

**الروابط المتاحة:**
- 🔗 https://voice.mrf103.com
- 🔗 http://localhost:5050
- 🔗 http://46.224.225.96:5050

**المعلومات التقنية:**
- **Container**: nexus_voice
- **Port Mapping**: 5050 → 8000
- **Internal IP**: 172.23.0.6
- **Backend**: Flask/Werkzeug
- **Python**: 3.10.19
- **Uptime**: 23+ hours

**الميزات:**
- Text-to-Speech (TTS)
- Edge TTS integration
- Multiple voice options
- Real-time processing

---

### 7️⃣ PostgreSQL Database - قاعدة البيانات

**الاتصال:**
```
Host: localhost
Port: 5432 (127.0.0.1 only)
Database: nexus_db
Username: postgres
Password: nexus_mrf_password_2026
```

**Connection String:**
```
postgresql://postgres:nexus_mrf_password_2026@localhost:5432/nexus_db
```

**المعلومات التقنية:**
- **Container**: nexus_db
- **Internal IP**: 172.23.0.2
- **Image**: supabase/postgres:15.1.0.147
- **Version**: PostgreSQL 15
- **Uptime**: 10+ hours
- **Health**: ✅ Healthy
- **Timezone**: Asia/Riyadh
- **Storage**: Persistent volume (./db_data)

**Features:**
- Supabase extensions included
- Full PostgreSQL 15 features
- Persistent data storage
- Network isolated (localhost only)

---

### 8️⃣ Additional Domains - نطاقات إضافية

#### Sultan Intelligence
- 🔗 https://sultan.mrf103.com
- Backend: Port 8005
- Status: ✅ Active

#### Publisher (Shadow Seven)
- 🔗 https://publisher.mrf103.com
- Type: Static landing page
- Status: ✅ Active

#### Admin Dashboard
- 🔗 https://admin.mrf103.com
- Backend: Port 8004 ⚠️ Currently down
- Status: ⚠️ Needs backend service

#### API Gateway
- 🔗 https://api.mrf103.com
- Backend: Port 8001
- Status: Configured

#### Jarvis Control Hub
- 🔗 https://jarvis.mrf103.com
- Type: Static UI
- Status: ✅ Active

#### Imperial UI
- 🔗 https://imperial.mrf103.com
- Type: Static UI
- Status: ✅ Active

#### Main Landing
- 🔗 https://mrf103.com
- 🔗 https://www.mrf103.com
- Type: Main landing page
- Status: ✅ Active

---

## 🐳 Docker Network Configuration

**Network Name**: nexus_prime_default  
**Subnet**: 172.23.0.0/16

### Container IPs:

| Container | IP Address | Ports |
|-----------|------------|-------|
| nexus_db | 172.23.0.2 | 5432 |
| nexus_flow | 172.23.0.3 | 5678 |
| nexus_ollama | 172.23.0.5 | 11434 |
| nexus_voice | 172.23.0.6 | 8000 |
| nexus_ai | 172.23.0.7 | 8080 |

---

## 🔒 SSL/TLS Configuration

**Certificate**: LetsEncrypt  
**Domain**: mrf103.com (wildcard)  
**Status**: ✅ Valid  
**Path**: `/etc/letsencrypt/live/mrf103.com/`

**Covered Domains:**
- mrf103.com
- www.mrf103.com
- *.mrf103.com (wildcard)

**Total Domains**: 14 configured

---

## 📊 Port Mapping Summary

| Port | Service | Binding | Status |
|------|---------|---------|--------|
| 22 | SSH | 0.0.0.0 | ✅ System |
| 80 | HTTP (Nginx) | 0.0.0.0 | ✅ → HTTPS |
| 443 | HTTPS (Nginx) | 0.0.0.0 | ✅ SSL |
| 3000 | Open WebUI | 0.0.0.0 | ✅ Active |
| 5050 | Voice Service | 0.0.0.0 | ✅ Active |
| 5173 | Frontend (Vite) | 0.0.0.0 | ✅ Active |
| 5432 | PostgreSQL | 127.0.0.1 | ✅ Local |
| 5678 | n8n | 0.0.0.0 | ✅ Active |
| 8005 | Backend API | 0.0.0.0 | ✅ Active |
| 11434 | Ollama | 0.0.0.0 | ✅ Active |

---

## 🧪 Testing Commands

### Test All Services:
```bash
# Run comprehensive test
bash /root/test_nexus_prime.sh

# Check specific ports
curl -I http://localhost:3000    # Open WebUI
curl -I http://localhost:5173    # Frontend
curl -I http://localhost:8005/docs    # API Docs
curl http://localhost:11434/api/version    # Ollama
curl http://localhost:5678/healthz    # n8n
```

### Check Docker Status:
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Check Port Bindings:
```bash
netstat -tuln | grep LISTEN
```

---

## 📝 Access Instructions

### From Local Machine (localhost):
- Access any service using `http://localhost:PORT`
- Example: `http://localhost:3000` for Open WebUI

### From External (Public IP):
- Use public IP: `http://46.224.225.96:PORT`
- Example: `http://46.224.225.96:5173` for Frontend

### From Domain (HTTPS):
- Use configured domains with HTTPS
- Example: `https://ai.mrf103.com`
- All domains have valid SSL certificates

---

## 🛠️ Management Commands

### Start/Stop Services:
```bash
# Stop all containers
docker-compose -f /root/nexus_prime/docker-compose.yml down

# Start all containers
docker-compose -f /root/nexus_prime/docker-compose.yml up -d

# Restart specific container
docker restart nexus_ai
```

### View Logs:
```bash
# All containers
docker-compose -f /root/nexus_prime/docker-compose.yml logs -f

# Specific container
docker logs -f nexus_ai

# Frontend logs
tail -f /root/NEXUS_PRIME/frontend/frontend.log

# Backend logs
tail -f /root/NEXUS_PRIME/backend/backend.log
```

### Nginx Management:
```bash
# Test configuration
nginx -t

# Reload configuration
systemctl reload nginx

# Restart nginx
systemctl restart nginx

# View error logs
tail -f /var/log/nginx/error.log
```

---

## 📈 System Health

**Overall Status**: 🟢 93% Operational

- ✅ Docker Containers: 5/5 Running
- ✅ SSL Certificates: Active
- ✅ Nginx: Valid config
- ✅ Port Conflicts: None
- ✅ Network Access: Full
- ✅ Database: Healthy
- ✅ AI Services: Online
- ❓ Admin Backend: Needs attention (Port 8004)

---

## 🎯 Quick Reference Card

**Most Used Services:**
```
AI Chat    → https://ai.mrf103.com
Frontend   → https://prime.mrf103.com  
API Docs   → http://localhost:8005/docs
Workflows  → https://flow.mrf103.com
Voice      → https://voice.mrf103.com
```

**Database Connection:**
```
postgresql://postgres:nexus_mrf_password_2026@localhost:5432/nexus_db
```

**Public IP:**
```
46.224.225.96
```

**Timezone:**
```
Asia/Riyadh
```

---

**Last Updated**: February 18, 2026  
**Maintained by**: NEXUS PRIME System  
**Version**: 2.3.0
