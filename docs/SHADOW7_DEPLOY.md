# Shadow-7 Publisher — سير النشر

**آخر تحديث:** 2026-02-27

---

## 1. البناء

```bash
cd /root/products/shadow-seven-publisher
npm run build
```

المخرجات في `dist/`

---

## 2. النشر (الفرونت إند)

```bash
sudo rm -rf /var/www/publisher/*
sudo cp -r dist/* /var/www/publisher/
```

Nginx يوجّه `publisher.mrf103.com` إلى `/var/www/publisher/`

---

## 3. الباك إند (shadow7_api)

```bash
cd /root/NEXUS_PRIME_UNIFIED
docker compose build shadow7_api
docker compose up -d shadow7_api
```

البورت: 8002. Nginx يوجّه `/api/shadow7/` إلى `localhost:8002`

---

## 4. السكربت الموحّد

```bash
cd /root/NEXUS_PRIME_UNIFIED
./scripts/deploy_frontends.sh
```

ينفّذ: بناء Shadow-7 → نسخ إلى /var/www/publisher → نشر اللانينق (إن وُجد)

---

## 5. متغيرات البيئة

| المتغير | القيمة | ملاحظة |
|---------|--------|--------|
| `VITE_API_URL` | فارغ | same-origin — الطلبات تذهب لنفس المنشأ، Nginx يوجّه /api/shadow7/ |
| `VITE_OLLAMA_BASE_URL` | `/ai` أو `https://publisher.mrf103.com/ai` | للإنتاج |

---

## 6. الروابط

| الخدمة | الرابط |
|--------|--------|
| الموقع | https://publisher.mrf103.com |
| تسجيل الدخول | https://publisher.mrf103.com/login |
| API | https://publisher.mrf103.com/api/shadow7/ |
