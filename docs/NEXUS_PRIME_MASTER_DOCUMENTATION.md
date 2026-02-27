# NEXUS PRIME — توثيق شامل

**آخر تحديث:** 2026-02-27  
**السلطة:** Mr.F — Super Admin & Lead Systems Architect

---

## 1. نظرة عامة

| العنصر | الوصف |
|--------|-------|
| **النظام** | NEXUS PRIME — منصة سيادية موحدة (11 كوكب) |
| **البيئة** | Ubuntu Server — Sovereign Node v1.0 |
| **الذكاء** | Ollama محلي (Adam/Eve) — لا اعتماد على السحابة |
| **المسار** | `/root/NEXUS_PRIME_UNIFIED` أو `~/nexus_prime_unified` |

---

## 2. الملفات والموارد الرئيسية

### 2.1 MRF Sovereign Node (التنفيذ الحالي)

| الملف | الموقع | المحتوى |
|-------|--------|---------|
| **MRF_SOVEREIGN_NODE_IMPLEMENTATION.md** | `docs/` | SovereignMasterContext، NexusCoreRouter، GalaxyDashboard، SultanAnalysisEngine، XBioGateway، useBioSentinel، المسارات والـ env |

---

### 2.2 جرد الملكية الفكرية (Treasure Hunt)

| الملف | الموقع | المحتوى |
|-------|--------|---------|
| **NEXUS_PRIME_TREASURE_HUNT.xlsx** | `products/xbio-sentinel/docs/specs/` | 14 ورقة: جرد IP، التفكيك العلمي A01-A24، كنوز جاهزة، غير مكتملة، غير مرئية، Stubs، خدمات معطلة، Env فارغة، خوارزميات غير منفذة، أرشيفات، خطط مكررة، TODO، تكاملات، ملخص |
| **build_treasure_hunt.py** | `products/xbio-sentinel/docs/specs/` | سكربت توليد Excel. تشغيل: `python build_treasure_hunt.py` |

**إحصائيات:** ~95 ابتكاراً، 55+ في جرد IP، 24 في التفكيك العلمي.

---

### 2.3 الكيان المستقل (Sovereign Autonomous Entity)

| الملف | الموقع | المحتوى |
|-------|--------|---------|
| **SOVEREIGN_AUTONOMOUS_ENTITY_DEPLOYMENT_PLAN.md** | `docs/` | خطة النشر، OpenHands، GraphRAG، المراحل 1–4 |
| **PHASE1_DIRECTIVE.md** | `the_entity_workspace/` | توجيه Phase 1 للكيان — رسم خريطة المجلدات |

**الوصول:** http://localhost:3010 (OpenHands)  
**الحاوية:** `sovereign-entity` — port 3010

---

### 2.4 الوثائق الأساسية

| الملف | الغرض |
|-------|-------|
| `docs/00_START_HERE_MASTER_GUIDE.md` | نقطة البداية |
| `docs/MASTER_GUIDE_INDEX_TREE_MAP_AR.md` | فهرس الأدلة |
| `nexus_prime_mindmap.md` | خريطة عقلية للنظام |
| `ENTERPRISE_CODEX.yaml` | 82 بديهية، 46 كروموسوم، 12 هرمون |

---

### 2.5 العلوم والبحث (Science & RnD)

| الملف | الغرض |
|-------|-------|
| `docs/Science_and_RnD/NEXUS_PRIME_SCIENTIFIC_DECONSTRUCTION_AND_INNOVATION_BASE.md` | التفكيك العلمي A01-A24، أساس براءات |
| `docs/Science_and_RnD/PATENT_01_BioCognitive_Architecture.md` | براءة البنية المعرفية |
| `docs/Science_and_RnD/PATENT_02_Predictive_Sensoring.md` | براءة الاستشعار التنبؤي |
| `docs/Science_and_RnD/PATENT_03_Acoustic_CyberPhysical_Deterrence.md` | براءة الردع الصوتي |

---

## 3. المكونات الحرجة

### X-BIO Sentinel
- **19 خوارزمية براءات** (9 منفذة، 10 معلنة)
- OMEGA، Kinetic Silo، SEI-10، FDIP-11
- المسار: `products/xbio-sentinel/`

### SULTAN
- TaqwaShield، FurqanClassifier، Sovereign Refusal
- بحث قرآني دلالي
- المسار: `products/alsultan-intelligence/`

### ENTERPRISE_CODEX
- 82 بديهية قرآنية
- 46 كروموسوم، 12 جزيء إشارة
- Phi*، Eve Protocol، 7 قوانين حديدية

---

## 4. أوامر سريعة

```bash
# توليد Treasure Hunt Excel
cd /root/products/xbio-sentinel/docs/specs
/root/products/shadow-seven-publisher/backend/venv/bin/python build_treasure_hunt.py

# تشغيل الكيان المستقل (OpenHands)
cd /root/NEXUS_PRIME_UNIFIED
docker start sovereign-entity

# إيقاف الكيان
docker stop sovereign-entity
```

---

## 5. المنافذ الرئيسية

| الخدمة | المنفذ |
|--------|--------|
| nexus_ai (Open WebUI) | 3000 |
| OpenHands (الكيان المستقل) | 3010 |
| PostgREST | 3001 |
| Grafana | 3002 |
| Sovereign Gateway | 9999 |
| Nexus Nerve | 8200 |
| Ollama | 11434 |

---

## 6. Cursor God Mode — ملف السياق الشامل

| الملف | الغرض |
|-------|-------|
| **CURSOR_MASTER_CONTEXT.md** | مانيفست + خطة تنفيذ + برومبت ماستر. ارفعه لـ Cursor Composer |
| **NEXUS_SYSTEM_MAP.md** | مخرجات السكربت — منافذ، حاويات، ذاكرة، DB |
| **scripts/generate_nexus_manifest.sh** | سكربت إعادة توليد المانيفست |

```bash
./scripts/generate_nexus_manifest.sh          # يولد NEXUS_SYSTEM_MAP.md
./scripts/generate_nexus_manifest.sh custom.md # مخرجات مخصصة
```

---

## 7. المسارات الرئيسية (Sovereign Node)

| المسار | المكون |
|--------|--------|
| `/galaxy` | GalaxyDashboard — 11 كواكب |
| `/galaxy/X-BIO` | XBioSentinel |
| `/galaxy/AS-SULTAN` | SultanPage |
| `/sultan` | SultanPage (iframe) |

---

## 8. مراجع إضافية

- **الخطة:** `.cursor/plans/رحلة_كشف_الكنوز_excel_612e215c.plan.md`
- **الفهرس:** `docs/INDEX.md`
- **البنية:** `docs/ARCHITECTURE.md`
