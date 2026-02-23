# دليل النشر — Deployment Guide

**NEXUS PRIME UNIFIED — Production Deployment**

---

## المتطلبات المسبقة

- Docker 24.0+ و Docker Compose v2.20+
- 16GB RAM كحد أدنى (23GB موصى به للإنتاج)
- 4 أنوية CPU كحد أدنى
- 50GB مساحة تخزين
- Nginx مع شهادات SSL (Let's Encrypt)
- دومين يشير إلى السيرفر (مثل mrf103.com)

---

## خطوات النشر

### 1. الاستنساخ والإعداد

```bash
cd /root  # أو المسار المطلوب
git clone <repository-url> NEXUS_PRIME_UNIFIED
cd NEXUS_PRIME_UNIFIED
```

### 2. إعداد البيئة

```bash
cp .env.example .env  # إن وُجد
# تعديل .env بالقيم الصحيحة:
# - POSTGRES_PASSWORD
# - JWT_SECRET
# - SMTP_* للإشعارات
# - DIFY_API_KEY (اختياري)
```

### 3. نسخ احتياطي قبل النشر

```bash
mkdir -p backups
cp .env backups/env.$(date +%Y%m%d)
cp nginx/nexus_unified.conf backups/
cp docker-compose*.yml backups/
```

### 4. تشغيل الخدمات

```bash
# الخدمات الأساسية
docker compose up -d

# انتظار استقرار قاعدة البيانات
sleep 30

# مراقبة (Grafana + Prometheus)
docker compose -f monitoring/docker-compose.monitoring.yml up -d

# Dify (اختياري)
./scripts/dify_launch.sh
```

### 5. إعداد Nginx

```bash
# نسخ الإعدادات
sudo cp nginx/nexus_unified.conf /etc/nginx/sites-enabled/
# أو إنشاء symlink
sudo ln -sf /root/NEXUS_PRIME_UNIFIED/nginx/nexus_unified.conf /etc/nginx/sites-enabled/

# التحقق
sudo nginx -t

# إعادة التحميل
sudo nginx -s reload
```

### 6. التحقق

```bash
./scripts/full_health_check.sh
# يجب أن يكون Exit 0
```

---

## DNS

تأكد من أن السجلات A أو CNAME تشير إلى عنوان IP السيرفر:

```
mrf103.com          A    <server-ip>
*.mrf103.com        A    <server-ip>
# أو CNAME للسب دومينات
publisher.mrf103.com CNAME mrf103.com
chat.mrf103.com     CNAME mrf103.com
# ... إلخ
```

---

## SSL

استخدم Certbot لشهادات Let's Encrypt:

```bash
sudo certbot certonly --nginx -d mrf103.com -d "*.mrf103.com"
```

الشهادات تُخزّن عادة في:
`/etc/letsencrypt/live/mrf103.com/`

---

## التحديث

```bash
cd /root/NEXUS_PRIME_UNIFIED
git pull
docker compose pull
docker compose up -d
./scripts/full_health_check.sh
```

---

## الاستعادة من الفشل

انظر [RUNBOOK.md](../RUNBOOK.md) — قسم "الاستعادة من النسخ الاحتياطي".

---

## مراجع

- [PRODUCTION_VERIFICATION.md](../PRODUCTION_VERIFICATION.md) — التحقق من الإنتاج
- [RUNBOOK.md](../RUNBOOK.md) — التشغيل والإيقاف والاستعادة
