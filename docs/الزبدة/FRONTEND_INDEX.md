# NEXUS PRIME Frontend Index

**Date:** 2026-02-24  
**Purpose:** Master inventory of all frontend pages, dashboards, and routes. Dual-plane classification (Control vs Data).

---

## 1. Summary

| Metric | Count |
|--------|-------|
| **Frontend projects** | 8 |
| **Total pages/routes** | 78+ |
| **Control Plane pages** | ~25 |
| **Data Plane pages** | ~45 |
| **Shared** | Imperial UI, shared-auth |

---

## 2. Project Overview

| Project | Location | Framework | Plane |
|---------|----------|-----------|-------|
| Dashboard ARC | `dashboard-arc/client` | React 18 + Vite + Wouter | Both |
| Web Dashboards | `web-dashboards/source` | Static HTML | Both |
| Shadow Seven Publisher | `products/shadow-seven-publisher` | React + Vite + React Router | Data |
| X-BIO Sentinel | `planets/X-BIO/xbioss-main` | React 19 + Vite | Data |
| 7th Shadow | `planets/SHADOW-7/7thshadow-main` | React + Vite | Data |
| Imperial UI | `products/imperial-ui` | React + Vite | Shared |
| Admin Portal | `web-dashboards/source/admin` | Static HTML | Control |
| Citadel | `web-dashboards/source/citadel` | Static HTML + Three.js | Control |

---

## 3. Dashboard ARC Routes (35)

**Base:** `dashboard.mrf103.com` → nexus_dashboard:5001

### 3.1 Auth / Landing (unauthenticated)

| Path | Component | Plane |
|------|-----------|-------|
| `/` | LandingPage | — |
| `/auth` | OperatorLogin | — |
| `/cloning` | Cloning | Data |

### 3.2 ARC 2.0 Hierarchy (authenticated)

| Path | Component | Plane |
|------|-----------|-------|
| `/` | Home | Both |
| `/mrf` | MRFDashboard | Control |
| `/maestros` | MaestrosHub | Control |
| `/security` | SecurityCenter | Control |
| `/finance` | FinanceHub | Control |
| `/legal` | LegalArchive | Control |
| `/life` | LifeManager | Data |
| `/rnd` | RnDLab | Control |
| `/xbio` | XBioSentinel | Data |
| `/reports` | ReportsCenter | Both |
| `/settings` | Settings | Both |
| `/integrations` | Integrations | Both |
| `/chat` | AgentChat | Both |

### 3.3 Legacy Pages

| Path | Component | Plane |
|------|-----------|-------|
| `/dashboard` | VirtualOffice | Both |
| `/bio-sentinel` | BioSentinel | Data |
| `/team-command` | TeamCommandCenter | Control |
| `/admin` | AdminControlPanel | Control |
| `/master-agent` | MasterAgentCommand | Control |
| `/growth-roadmap` | GrowthRoadmap | Both |
| `/analytics` | AnalyticsHub | Both |
| `/system-architecture` | SystemArchitecture | Control |
| `/investigation-lounge` | InvestigationLounge | Control |
| `/operations-simulator` | OperationsSimulator | Control |
| `/quantum-warroom` | QuantumWarRoom | Control |
| `/temporal-anomaly-lab` | TemporalAnomalyLab | Control |
| `/self-check` | SelfCheck | Both |
| `/virtual-office` | VirtualOffice | Both |

### 3.4 Fallback

| Path | Component |
|------|-----------|
| `*` | NotFound |

---

## 4. Shadow Seven Publisher Routes (12)

**Base:** `publisher.mrf103.com`

| Path | Page | Plane |
|------|------|-------|
| `/login` | LoginPage | — |
| `/pricing` | PricingPage | Data |
| `/` | Dashboard | Data |
| `/upload` | UploadPage | Data |
| `/submit` | SubmitWizardPage | Data |
| `/manuscripts` | ManuscriptsPage | Data |
| `/elite-editor/:id` | EliteEditorPage | Data |
| `/export` | ExportPage | Data |
| `/book-merger` | BookMergerPage | Data |
| `/cover-designer` | CoverDesignerPage | Data |
| `/settings` | SettingsPage | Data |
| `/analytics` | AnalyticsDashboardPage | Data |

---

## 5. Web Dashboards (Static HTML)

**Base:** `web-dashboards/source/` — served via nginx

| Directory | Purpose | Plane |
|-----------|----------|-------|
| `admin/` | Admin dashboard, user/role overview | Control |
| `citadel/` | Sovereign Enterprise landing | Control |
| `imperial/` | Imperial UI | Shared |
| `prime/` | Nexus Prime | Data |
| `sultan/` | Sultan | Data |
| `jarvis/` | Jarvis | Control |
| `finance/` | Finance | Data |
| `monitor/` | Service monitor | Control |
| `marketing/` | Marketing | Data |
| `platform/` | Platform | Data |
| `portal/` | Portal | Data |
| `publishing/` | Publishing | Data |
| `landing/` | Landing | Data |

**Root duplicates:** `landing/`, `finance/`, `monitor/`, `marketing/`

---

## 6. X-BIO Sentinel

**Location:** `planets/X-BIO/xbioss-main`  
**Type:** Single-page application (multi-tab)  
**Plane:** Data

| Tab | Purpose |
|-----|---------|
| Overview | Bio-sensor overview |
| Specs | Specifications |
| Inventions | Invention catalog |
| Hierarchy | Entity hierarchy |

---

## 7. 7th Shadow

**Location:** `planets/SHADOW-7/7thshadow-main`  
**Type:** Single-page wizard  
**Plane:** Data

| Step | Purpose |
|------|---------|
| Language Select | Language selection |
| Intro | Introduction |
| Upload | Content upload |
| Processing | AI processing |
| Completed | Result display |

---

## 8. Dual-Plane Map

### Control Plane (The Citadel) — Super Admin / Mr. F

- Dashboard ARC: Admin, Master Agent, Team Command, System Architecture, Quantum War Room, Temporal Anomaly Lab, MaestrosHub, SecurityCenter, RnDLab, InvestigationLounge, OperationsSimulator
- Enhanced Dashboard: live-stats, service-health, activity-feed
- Admin Portal (web-dashboards)
- Citadel (web-dashboards)
- God Mode (sovereign_dify_bridge:8888)
- Jarvis, Monitor (web-dashboards)

### Data Plane (The Nexus) — End User / Client

- Shadow Seven Publisher (all pages)
- X-BIO Sentinel
- 7th Shadow
- Dashboard ARC: BioSentinel, Cloning, LifeManager, XBioSentinel
- Web Dashboards: finance, marketing, platform, portal, publishing, prime, sultan, landing

### Shared

- Imperial UI (design system)
- shared-auth (RS256 JWT)

---

## 9. Hidden Gates Audit (2026-02-24)

| # | Location | Type | Status |
|---|----------|------|--------|
| 1 | `web-dashboards/source/citadel/index.html` | Fake gate (PASSKEY + fake biometrics) | **Dismantled** — LOG IN now opens arsenal directly |

Standard auth (Dashboard ARC, shared-auth) preserved.

---

## 10. Cloudflare DNS & Ingress Mapping

**Server IP:** 46.224.225.96  
**All subdomains below resolve via Cloudflare A records.**

### Control Plane Subdomains

| Subdomain | Internal Path / Port | Plane |
|-----------|----------------------|-------|
| admin.mrf103.com | ecosystem_api:8005 / /var/www/admin | Control |
| citadel.mrf103.com | /var/www/citadel | Control |
| dashboard.mrf103.com | nexus_dashboard:5001 | Control |
| dash.mrf103.com | nexus_dashboard:5001 | Control |
| monitor.mrf103.com | /var/www/monitor | Control |
| grafana.mrf103.com | Grafana:3002 | Control |
| nerve-ui.mrf103.com | /var/www/nerve + nexus_nerve:8200 | Control |
| god.mrf103.com | sovereign_dify_bridge:8888 | Control |

### Data Plane / Product Subdomains

| Subdomain | Internal Path / Port | Plane |
|-----------|----------------------|-------|
| ai.mrf103.com | nexus_ai:3000 | Data |
| chat.mrf103.com | nexus_ai:3000 | Data |
| xbio.mrf103.com | xbio-sentinel:8080 | Data |
| sultan.mrf103.com | ecosystem_api:8005 | Data |
| publisher.mrf103.com | shadow-seven:3001 | Data |
| finance.mrf103.com | /var/www/finance | Data |
| marketing.mrf103.com | /var/www/marketing | Data |
| app.mrf103.com | nexus_dashboard:5001 | Data |
| boardroom.mrf103.com | nexus_boardroom:8501 | Data |
| platform.mrf103.com | ecosystem_api:8005 | Data |
| sovereign.mrf103.com | sovereign_dify_bridge:8888 | Data |
| voice.mrf103.com | nexus_voice:5050 | Data |

### Infrastructure / Integrations Subdomains

| Subdomain | Internal Path / Port |
|-----------|----------------------|
| api.mrf103.com | ecosystem_api:8005 |
| gateway.mrf103.com | sovereign_gateway:9999 |
| dify.mrf103.com | Dify:8085 |
| flow.mrf103.com | nexus_flow:5678 |
| n8n.mrf103.com | nexus_flow:5678 |
| memory.mrf103.com | nexus_memory_keeper:9000 |
| oracle.mrf103.com | nexus_oracle:8100 |
| nerve.mrf103.com | nexus_nerve:8200 |
| cortex.mrf103.com | nexus_cortex:8090 |
| nexus.mrf103.com | nexus_ai:3000 |
| prime.mrf103.com | Static / NEXUS PRIME |
| imperial.mrf103.com | /var/www/imperial |
| jarvis.mrf103.com | /var/www/jarvis |
