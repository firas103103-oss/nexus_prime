# NEXUS PRIME — الصورة التثبتية التوسعية للمنظمة

**التاريخ:** 2026-02-24  
**الغرض:** هيكلية وبنية ومكونات المنظمة للتحقق الكامل والفعال

---

## 1. الهيكل العام للسيرفر

```
/root
├── NEXUS_PRIME_UNIFIED/          # المشروع الرئيسي الموحد
├── products/                     # المنتجات (14+ مشروع)
├── integration/                  # أنظمة التكامل (5 خدمات)
├── nexus_*.sh                    # سكربتات التشغيل
├── nexus_prime_backups/          # نسخ احتياطية
└── nexus_prime_backup_*.tar.gz   # أرشيف كامل
```

---

## 2. بنية NEXUS PRIME UNIFIED

### 2.1 الخدمات الأساسية (Docker)

| الخدمة | المنفذ | الدور |
|--------|--------|------|
| nexus_db | 5432 | PostgreSQL + MSL schema |
| nexus_ollama | 11434 | LLM محلي |
| nexus_litellm | 4000 | وكيل LLM |
| nexus_nerve | 8200 | الجهاز العصبي — Cognitive Bridge, Genome → LLM |
| nexus_oracle | 8100 | RAG — موسوعة السلطان |
| nexus_cortex | 8090 | Cortex |
| nexus_memory_keeper | 9000, 9001 | حارس الذاكرة |
| sovereign_gateway | 9999 | AS-SULTAN Gateway |
| nexus_auth | 8003 | RS256 Auth |
| ecosystem_api | 8005 | Ecosystem API |
| nexus_dashboard | 5001 | Dashboard ARC |
| nexus_ai | 3000→8080 | Open WebUI |
| nexus_flow | 5678 | n8n |
| nexus_voice | 5050→8000 | Edge-TTS |
| nexus_postgrest | 3001 | PostgREST |
| nexus_redis | 6379 | Redis |
| nexus_orchestrator | 50051 | gRPC Orchestrator |

### 2.2 مسار البيانات

```
nexus_db (msl)
    ├── nexus_nerve (cognitive_bridge, genome, hormones)
    ├── sovereign_dify_bridge (hormonal_orchestrator, genome_agent_mapper, eve_protocol)
    ├── neural_spine (daemon_system, genesis, entity_factory)
    └── memory_keeper (cognitive timeline)
```

### 2.3 مسار الـ LLM

```
User → Nerve /api/command
    → cognitive_bridge.fetch_entity_state()
    → cognitive_bridge.get_llm_params()  [temperature, top_p من genome + mood]
    → _ollama_chat_with_ethical_gate(options=llm_params)
    → Ollama /api/chat
```

### 2.4 المكونات الرئيسية

| المكون | الملف الرئيسي | الوظيفة |
|--------|---------------|---------|
| Cognitive Bridge | nexus_nerve/cognitive_bridge.py | ربط الجينوم والهرمونات بالـ LLM |
| Sultan Engine | neural_spine/codex/sultan_engine.py | TaqwaShield, FurqanClassifier |
| Genome Mapper | sovereign_dify_bridge/genome_agent_mapper.py | trait_summary → LLM params |
| Hormonal Orchestrator | sovereign_dify_bridge/hormonal_orchestrator.py | Cortisol/Adrenaline spike → Dify |
| Eve Protocol | sovereign_dify_bridge/eve_protocol.py | Fractal polarization |
| Entity Factory | neural_spine/genesis/entity_factory.py | 46 chromosomes, 82 traits |

---

## 3. المجلدات خارج NEXUS_PRIME_UNIFIED

| المسار | المحتوى | العلاقة |
|--------|---------|---------|
| /root/products | 14 منتج | يُربط عبر ecosystem_api volume |
| /root/integration | clone-hub, ecosystem-api, shared-auth, admin-portal, command-center | NEXUS_PRIME_UNIFIED/integration مستخدم في Docker |
| /root/nexus_*.sh | سكربتات تشغيل | نقطة الدخول للتشغيل |

---

## 4. التحقق من الصلاحية

| الفحص | الأمر |
|-------|-------|
| MSL schema | `docker exec nexus_db psql -U postgres -d nexus_db -c "\dn msl"` |
| Nerve health | `curl http://localhost:8200/health` |
| Oracle RAG | `curl -X POST http://localhost:8100/ask -H "Content-Type: application/json" -d '{"question":"كُن","top_k":3}'` |
| Gateway | `curl http://localhost:9999/health` |
| Dashboard live-stats | `curl http://localhost:5001/api/enhanced/live-stats` |
