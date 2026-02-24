# Dify — Sovereign Encyclopedia Ingestion Guide

**Authority:** Supreme Systems Architect (Kier)  
**Purpose:** Ingest موسوعة السلطان (The Sovereign Encyclopedia) into Dify as the primary Knowledge Base for God Mode and Sovereign Gateway RAG.

---

## 1. Content Bundle Location

| File | Description |
|------|-------------|
| `docs/SOVEREIGN_ENCYCLOPEDIA.md` | Primary RAG source — axioms, laws, genome, hormones, daemons |
| `ENTERPRISE_CODEX.yaml` | Full machine-format Codex (YAML) |
| `docs/SOVEREIGN_ARCHITECTURAL_GOVERNANCE.md` | Architecture and gap analysis |

---

## 2. Manual Upload via Dify UI

1. Log in: https://dify.mrf103.com
2. Knowledge → Create Knowledge Base
3. Name: `Sovereign Encyclopedia`
4. Upload: `docs/SOVEREIGN_ENCYCLOPEDIA.md` (and optionally ENTERPRISE_CODEX.yaml)
5. Wait for indexing
6. In Chat/Workflow apps, add Knowledge Retrieval node and select this dataset

---

## 3. Nexus Oracle (Already Active)

Oracle (port 8100) has ingested the content. API: `POST http://nexus_oracle:8100/ask`
