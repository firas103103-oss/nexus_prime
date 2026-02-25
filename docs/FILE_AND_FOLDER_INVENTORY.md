# NEXUS PRIME UNIFIED — Total File & Folder Inventory

**Generated:** 2025-02-24  
**Scope:** All files and folders (excluding `node_modules`, `.git`, `target`, `data`)

---

## Summary

| Metric | Count |
|--------|-------|
| **Total files** | 11,398 |
| **Total folders** | 2,557 |
| **Root-level files** | 36 |
| **Root-level directories** | 27 |

---

## By Server / Component Type

### Backend services (Python)

| Component | Files | Role |
|-----------|-------|------|
| **nexus_nerve** | 9 | Nerve service, cognitive bridge |
| **nexus_oracle** | 5 | Oracle service |
| **nexus_cortex** | 5 | Cortex service |
| **nexus_middleware** | 11 | Middleware layer |
| **nexus_prime_core** | 23 | Core orchestration |
| **sovereign_dify_bridge** | 10 | Genome mapper, Eve protocol, hormonal orchestrator |
| **memory_keeper** | 5 | Memory persistence |
| **dify** | 7,616 | Dify platform (submodule) |
| **Total backend** | ~7,704 | |

### Rust / systems

| Component | Files | Role |
|-----------|-------|------|
| **neural_spine** | 74 | Spine server, entity factory, phi_monitor |
| **neural_spine_backup_pre_restructure** | (backup) | Pre-restructure backup |

### Frontend / dashboards

| Component | Files | Role |
|-----------|-------|------|
| **dashboard-arc** | 555 | React dashboard |
| **web-dashboards** | 24 | Web dashboards |
| **landing-pages** | 2 | Landing pages |
| **Total frontend** | ~581 | |

### Planets (sub-projects)

| Component | Files | Role |
|-----------|-------|------|
| **planets** | 1,315 | SHADOW-7, X-BIO, AI-ARCH, etc. |

### Docs & content

| Component | Files | Role |
|-----------|-------|------|
| **docs** | 275 | Main docs, archive, Science_and_RnD, PERSONAL_DOCS |
| **AI_HR_REGISTRY** | 64 | HR registry, specialists, agency |

### DevOps & infra

| Component | Files | Role |
|-----------|-------|------|
| **scripts** | 35 | Automation scripts |
| **k8s-manifests** | 15 | Kubernetes manifests |
| **monitoring** | 6 | Grafana, monitoring |
| **nginx** | 2 | Nginx config |
| **n8n-workflows** | 5 | n8n workflow definitions |
| **edge-tts-repo** | 3 | Edge TTS integration |
| **marketing** | 1 | Marketing assets |

### Other

| Component | Files | Role |
|-----------|-------|------|
| **baselines** | 3 | Baseline configs |
| **backups** | 4 | Backup artifacts |
| **products** | 0 | Product definitions (empty) |
| **integration** | 0 | Integration configs (empty) |

---

## By File Type

### Code

| Extension | Count | Category |
|-----------|-------|----------|
| **tsx** | 3,220 | TypeScript React |
| **py** | 2,568 | Python |
| **ts** | 1,109 | TypeScript |
| **js** | 375 | JavaScript |
| **jsx** | 273 | React JSX |
| **c** | 147 | C |
| **cpp** | 32 | C++ |
| **rs** | 16 | Rust |
| **ino** | 24 | Arduino |
| **kt** | 7 | Kotlin |
| **java** | 3 | Java |

### Config & data

| Extension | Count | Category |
|-----------|-------|----------|
| **json** | 1,259 | JSON config/data |
| **yml** | 79 | YAML |
| **yaml** | 75 | YAML |
| **toml** | 19 | TOML config |
| **xml** | 32 | XML |
| **properties** | 11 | Properties files |
| **gradle** | 11 | Gradle |
| **env** | 3 | Environment |
| **ini** | 6 | INI config |
| **conf** | 6 | Config files |

### Markup & styling

| Extension | Count | Category |
|-----------|-------|----------|
| **svg** | 561 | Vector graphics |
| **html** | 109 | HTML |
| **css** | 128 | Stylesheets |
| **scss** | 2 | SCSS |
| **md** | 454 | Markdown |
| **mdx** | 12 | MDX |

### Scripts & tooling

| Extension | Count | Category |
|-----------|-------|----------|
| **sh** | 83 | Shell scripts |
| **lock** | 7 | Lock files |
| **mjs** | 8 | ES modules |
| **cjs** | 5 | CommonJS |

### Assets & media

| Extension | Count | Category |
|-----------|-------|----------|
| **png** | 108 | Images |
| **jpg** | 8 | Images |
| **pdf** | 58 | PDFs |
| **docx** | 7 | Word |
| **pptx** | 7 | PowerPoint |
| **xlsx** | 1 | Excel |

### Database & SQL

| Extension | Count | Category |
|-----------|-------|----------|
| **sql** | 28 | SQL scripts |

### Other / misc

| Extension | Count | Category |
|-----------|-------|----------|
| **txt** | 123 | Plain text |
| **h** | 216 | C headers |
| **gitignore** | 21 | Git ignore |
| **dockerignore** | 7 | Docker ignore |
| **prettierrc** | 3 | Prettier |
| **eslintignore** | 3 | ESLint |
| **example** | 12 | Example files |
| **template** | 6 | Templates |

---

## Top-level directory layout

```
NEXUS_PRIME_UNIFIED/
├── AI_HR_REGISTRY/          # HR registry
├── backups/
├── baselines/
├── dashboard-arc/           # React dashboard
├── data/                    # Runtime data (excluded from counts)
├── dify/                    # Dify submodule
├── docs/                    # Documentation
├── edge-tts-repo/
├── integration/
├── k8s-manifests/
├── landing-pages/
├── marketing/
├── memory_keeper/
├── monitoring/
├── n8n-workflows/
├── neural_spine/            # Rust spine
├── neural_spine_backup_pre_restructure/
├── nexus_cortex/
├── nexus_middleware/
├── nexus_nerve/
├── nexus_oracle/
├── nexus_prime_core/
├── nginx/
├── planets/                 # SHADOW-7, X-BIO, AI-ARCH
├── products/
├── scripts/
├── sovereign_dify_bridge/
└── web-dashboards/
```

---

## File type categories (grouped)

| Category | Extensions | Approx. count |
|----------|------------|---------------|
| **TypeScript/React** | tsx, ts, jsx, js | ~4,977 |
| **Python** | py | ~2,568 |
| **Config** | json, yml, yaml, toml, xml, env | ~1,507 |
| **Markdown** | md, mdx | ~466 |
| **Assets** | svg, png, jpg, pdf, docx, pptx | ~741 |
| **C/C++/Rust** | c, cpp, h, rs | ~447 |
| **Styles** | css, scss | ~130 |
| **Shell** | sh | ~83 |
| **Embedded** | ino | ~24 |
| **SQL** | sql | ~28 |
| **Other** | txt, lock, gradle, properties, etc. | ~200+ |
