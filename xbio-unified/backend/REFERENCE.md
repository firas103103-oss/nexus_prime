# Backend — X-BIO Sentinel

Backend X-BIO يعمل من **`products/xbio-sentinel/`** (خارج NEXUS_PRIME_UNIFIED أو ضمنه حسب هيكل المشروع).

## الموقع

```
products/xbio-sentinel/
├── xbio_core.py       # FastAPI — /api/ingest, /api/patents, ...
├── xbio_ingest.py     # منطق التخزين والفلترة
├── xbio_algorithms.py # خوارزميات الـ 19 براءة
├── serial_bridge.py   # نسخة مرجعية (النسخة الموحدة في xbio-unified)
├── Dockerfile
└── migrations/
```

## التشغيل

**عبر Docker:**
```bash
cd NEXUS_PRIME_UNIFIED
docker compose up -d nexus_xbio
```

**محلياً:**
```bash
cd products/xbio-sentinel
export DATABASE_URL="postgresql://user:pass@localhost:5432/nexus_db"
pip install fastapi uvicorn psycopg2-binary
uvicorn xbio_core:app --host 0.0.0.0 --port 8080
```

## التحقق

```bash
curl https://xbio.mrf103.com/health
curl https://xbio.mrf103.com/api/telemetry/latest
```
