# NEXUS PRIME — مطابقة حالة السيرفر | Server State Match

**التاريخ:** 2026-02-25  
**الغرض:** مطابقة ما يجب أن يكون محمّلًا ومفعّلًا وموجودًا على السيرفر من الأول

---

## 1. الخدمات النظامية | System Services

| الخدمة | يجب | الحالة الفعلية | ملاحظات |
|--------|-----|----------------|----------|
| Docker | enabled + active | enabled, active | OK |
| Nginx | enabled + active | enabled, active | OK |
| UFW | active | active | OK |
| Redis 6379 | DENY | DENY | OK (BSI fix) |

~~**إجراء:** تفعيل Nginx عند الإقلاع~~ — **تم** (2026-02-25)

---

## 2. الملفات والتهيئة | Files & Config

| الملف/المجلد | يجب | موجود | ملاحظات |
|--------------|-----|--------|----------|
| `/root/NEXUS_PRIME_UNIFIED/.env` | نعم | نعم | مفاتيح مملوءة |
| `/root/NEXUS_PRIME_UNIFIED/.env.example` | نعم | نعم | قالب |
| `/root/NEXUS_PRIME_UNIFIED/dify/docker/.env` | نعم | نعم | Dify config |
| `/root/NEXUS_PRIME_UNIFIED/dify/docker/middleware.env` | اختياري | لا | لتعطيل تعريض Redis |
| `/etc/letsencrypt/live/mrf103.com/fullchain.pem` | نعم | نعم | شهادة SSL |
| `/etc/letsencrypt/live/mrf103.com/fullchain.pem` | نعم | نعم | مفتاح SSL |
| `/etc/nginx/conf.d/nexus_unified.conf` | symlink | نعم | → infrastructure/nginx/nexus_unified.conf |

---

## 3. الحاويات — المحددة في Compose | Containers Defined

### 3.1 docker-compose.yml + docker-compose.dify.yml

| الخدمة | يجب تشغيله | الحالة | المنفذ |
|--------|-------------|--------|--------|
| nexus_db | نعم | Up (healthy) | 5432 داخلي |
| nexus_redis | نعم | Up (healthy) | 6379 داخلي فقط |
| nexus_ollama | نعم | Up | 11434 |
| nexus_litellm | نعم | Up (healthy) | 4000 |
| nexus_voice | نعم | Up | 5050 |
| nexus_boardroom | نعم | Up (healthy) | 8501 |
| nexus_xbio | نعم | Up (healthy) | 8080 |
| nexus_dashboard | نعم | Up | 5001 |
| nexus_ai | نعم | Up (healthy) | 3000 |
| nexus_flow | نعم | Up | 5678 |
| nexus_cortex | نعم | Up (healthy) | 8090 |
| shadow7_api | نعم | Up (healthy) | 8002 |
| nexus_postgrest | نعم | Up | 3001 |
| nexus_auth | نعم | Up (healthy) | 8003 |
| nexus_memory_keeper | نعم | Up (healthy) | 9000-9001 |
| nexus_orchestrator | نعم | Up (healthy) | 50051 |
| nexus_nerve | نعم | Up (healthy) | 8200 |
| sovereign_gateway | نعم | Up (healthy) | 9999 |
| ecosystem_api | نعم | Up (healthy) | 8005 |
| nexus_oracle | نعم | Up (healthy) | 8100 |
| sovereign_dify_bridge | نعم | Up (healthy) | 8888 |

### 3.2 docker-compose.override.yml

| الخدمة | يجب تشغيله | الحالة | ملاحظات |
|--------|-------------|--------|----------|
| neural_spine | نعم | Up (healthy) | 8300 |
| reflex_agents | نعم | Up (healthy) | — |
| apex (nexus_apex) | نعم | Up | 127.0.0.1:7777 |

---

## 4. التطابقات الخاصة | Special Cases

### 4.1 ecosystem_api (8005)

- **Compose:** حاوية `ecosystem_api` — Up (healthy)
- **الفعلي:** تم إنشاء `integration/ecosystem-api` وتشغيله في Docker
- **النتيجة:** الخدمة تعمل من الحاوية

### 4.2 neural_spine (8300)

- **Compose:** حاوية `neural_spine` — Up (healthy)
- **الفعلي:** يعمل في Docker

### 4.3 Dify (Stack منفصل)

| الحاوية | الحالة | المنفذ |
|---------|--------|--------|
| dify-nginx-1 | Up | 8085, 8445 |
| dify-api-1 | Up | 5001 داخلي |
| dify-worker-1 | Up | — |
| dify-worker_beat-1 | Up | — |
| dify-db_postgres-1 | Up (healthy) | 5432 داخلي |
| dify-redis-1 | Up (healthy) | 6379 داخلي |
| dify-web-1 | Up | 3000 داخلي |
| dify-sandbox-1 | Up | — |
| dify-weaviate-1 | Up | — |
| dify-ssrf_proxy-1 | Up | — |
| dify-plugin_daemon-1 | Up | 5003 |

---

## 5. مراقبة (Monitoring) — غير من compose الرئيسي

| الحاوية | الحالة | المنفذ |
|---------|--------|--------|
| nexus_grafana | Up | 3002 |
| nexus_prometheus | Up | 9090 |
| nexus_node_exporter | Up | 9100 |
| nexus_alertmanager | Up | 9093 |
| nexus_cadvisor | Up | 8081 |

---

## 6. ملخص الفجوات | Gap Summary

| البند | الحالة | ملاحظات |
|-------|--------|----------|
| Nginx | ✅ enabled | تم 2026-02-25 |
| ecosystem_api | ✅ Up (healthy) | تم إنشاء integration/ecosystem-api |
| neural_spine | ✅ Up (healthy) | يعمل في Docker |
| reflex_agents | ✅ Up (healthy) | healthcheck: Redis ping |
| apex | ✅ Up | 127.0.0.1:7777 |
| nexus_nerve | ✅ healthy | healthcheck: Python urllib بدل curl |
| sovereign_dify_bridge | ✅ healthy | healthcheck: Python urllib بدل curl |

---

## 7. أوامر التحقق السريع

```bash
# حالة الحاويات
docker ps -a --format 'table {{.Names}}\t{{.Status}}'

# المنافذ المستمعة
ss -tlnp | grep -E "3000|4000|5001|5678|8002|8005|8085|8090|8200|8300|9999"

# Nginx
systemctl status nginx
systemctl is-enabled nginx

# UFW
sudo ufw status | grep 6379
```

---

**التوقيع:** Principal Cybersecurity Architect
