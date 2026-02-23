# NEXUS PRIME — Runbook التشغيل

**آخر تحديث:** 2026-02-23

---

## التشغيل الكامل

```bash
cd /root/NEXUS_PRIME_UNIFIED

# 1. الخدمات الأساسية
docker compose up -d

# 2. مراقبة (Grafana + Prometheus)
docker compose -f monitoring/docker-compose.monitoring.yml up -d

# 3. Dify (اختياري)
./scripts/dify_launch.sh
```

---

## الإيقاف

```bash
cd /root/NEXUS_PRIME_UNIFIED

# إيقاف الخدمات الأساسية
docker compose down

# إيقاف المراقبة
docker compose -f monitoring/docker-compose.monitoring.yml down

# إيقاف Dify
cd dify/docker && docker compose -f docker-compose.yaml -f docker-compose.nexus-override.yaml -p dify down
```

---

## التحقق من الصحة

```bash
./scripts/full_health_check.sh
# exit 0 = كل الخدمات تعمل
```

## التحقق من واقعية التوثيق واختبارات التوافقية

```bash
# تحقق شامل: المنافذ، APIs، Clone Hub، Ethical Gate
python3 scripts/verify_documentation_reality.py

# اختبارات التوافقية البرمجية والتقنية
./scripts/compatibility_tests.sh
```

---

## الاستعادة من النسخ الاحتياطي

```bash
# استعادة .env
cp backups/env.YYYYMMDD .env

# استعادة nginx
cp backups/nginx_YYYYMMDD.conf nginx/nexus_unified.conf
sudo cp nginx/nexus_unified.conf /etc/nginx/sites-enabled/
sudo nginx -s reload

# استعادة docker-compose
cp backups/docker-compose.yml .
cp backups/docker-compose.dify.yml .
```

---

## المنافذ الرئيسية

| المنفذ | الخدمة |
|--------|--------|
| 3000 | Open WebUI |
| 3002 | Grafana |
| 4000 | LiteLLM |
| 5050 | Voice (Edge TTS) |
| 5678 | n8n |
| 8080 | X-BIO Sentinel |
| 8085 | Dify |
| 8200 | Nerve Center |
| 8501 | Boardroom |
| 8888 | Sovereign Bridge |
| 9000 | Memory Keeper |
| 9999 | Gateway |

---

## المتغيرات الحرجة (.env)

- `DIFY_API_KEY` — لتفعيل trigger الـ workflow من X-BIO
- `DIFY_DEFENSIVE_WORKFLOW_ID` — (اختياري) معرف الـ workflow
- `POSTGRES_PASSWORD` — كلمة مرور قاعدة البيانات
