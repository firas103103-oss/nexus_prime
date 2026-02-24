# Identity & Compliance Protocol — Kier

**التاريخ:** 2026-02-24  
**الحالة:** ACTIVE — Sovereign Positioning  
**المرجع:** NEXUS PRIME Launch Readiness Checklist

---

## Executive Context

| Attribute | Value |
|-----------|-------|
| **Founder Status** | Syrian National / Resident in Saudi Arabia (Riyadh) |
| **Entity** | UK-incorporated (First Formations) |
| **Operating Base** | Riyadh, KSA |
| **Ecosystem** | NEXUS PRIME — Sovereign AI Assets |

---

## 1. Geopolitical Navigation

### 1.1 Provider Tolerance Matrix

Prioritize providers with **proven high-tolerance** or **specific frameworks** for Syrian founders with GCC residency. Avoid providers with automated sanctions screening that may trigger false positives.

| Provider | Tier | Notes | Recommendation |
|----------|------|-------|-----------------|
| **Wise Business** | ✅ Primary | UK-based, multi-currency, accepts non-UK directors. Widely used by GCC startups. One-time £45 fee. | **Use as primary FX & payments** |
| **Revolut Business** | ✅ Primary | 250K+ businesses, multi-currency, UK banking infrastructure. Non-UK founders accepted. | **Use for operational banking** |
| **Stripe** | ⚠️ Secondary | Strong KYC; entity-first (UK company) reduces founder-level scrutiny. Route via UK entity. | **Use for SaaS payments — entity-led** |
| **Mercury** | ❌ Avoid | US entity required. Stripe Atlas partnership targets US corps. Not applicable for UK entity. | **Skip — US-only** |
| **Payoneer** | ✅ Fallback | Cross-border payments, GCC presence, flexible KYC for freelancers/startups. | **Backup for contractor payouts** |
| **Wio Bank (UAE)** | 🔶 Future | Stripe partnership; UAE entity. Consider for GCC expansion phase. | **Q3–Q4 2026 expansion** |

### 1.2 Friction-Less Path: Syrian-Owned UK Firm from Riyadh

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SOVEREIGN POSITIONING FLOW                                │
└─────────────────────────────────────────────────────────────────────────────┘

  [Kier — Riyadh]                    [UK Entity — First Formations]
         │                                        │
         │  Proof of Residency (KSA)              │  Company Registration
         │  Source of Funds (prepared)             │  UK Address (Registered Office)
         │                                        │
         └────────────────────┬───────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   UK ENTITY AS BRIDGE         │
              │   • All contracts in UK name   │
              │   • Invoicing from UK entity   │
              │   • Bank accounts: UK entity   │
              └───────────────┬───────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
   [Wise Business]     [Revolut Business]     [Stripe]
   FX, international   Operational banking   SaaS payments
   payments            Cards, payroll        (entity-level KYC)
```

**Core Principle:** The UK entity is the **contracting party**. Kier acts as director/UBO — identity verified once, then the entity carries all commercial relationships.

---

## 2. Compliance Shield

### 2.1 Proactive Document Readiness

Build a **pre-submission pack** to avoid delays when providers request Source of Funds (SoF) or Proof of Residency (PoR). Never submit large unorganized bundles — use a clear index and aligned dates.

| Document Type | Purpose | Status |
|---------------|---------|--------|
| **Proof of Residency (PoR)** | Utility bill, bank statement, or government letter from KSA (≤3 months) | 🔲 Prepare |
| **Source of Funds (SoF)** | Narrative + supporting docs: employment contracts, business income, investment letters | 🔲 Prepare |
| **Source of Wealth (SoW)** | How wealth accumulated: salary, dividends, business sale, inheritance | 🔲 Prepare |
| **UK Company Docs** | Certificate of Incorporation, Articles, Director/UBO list | ✅ First Formations |
| **AML Policy** | One-page policy for NEXUS PRIME / MRF | 🔲 Draft |
| **Document Index** | Single PDF with table of contents, dates, names aligned | 🔲 Create |

### 2.2 Compliance Shield Checklist (NEXUS PRIME)

Integrated into `LAUNCH_READINESS_CHECKLIST.md` — see Section 7.

| Shield Item | Action | Trigger |
|-------------|--------|---------|
| **SoF Narrative** | One-page letter: "Funds originate from [employment/business/investment]. Supporting docs attached." | Before first banking application |
| **PoR Ready** | KSA utility/bank statement, name + address, ≤3 months | Before Wise/Revolut/Stripe |
| **Entity-First Onboarding** | Apply as UK company; add Kier as director/UBO only when prompted | All providers |
| **No Large Bundles** | Submit only requested docs; use index if multiple files | Any KYC request |
| **AML Policy** | Draft 1-pager: risk assessment, monitoring, reporting | Stripe, payment processors |
| **Consistent Naming** | Same spelling of name across all docs (passport, utility, company) | All submissions |

### 2.3 Avoiding Automated Freezes

- **Entity-led applications:** Start with company details; founder details come later in flow.
- **Clear business description:** "UK software company developing AI platforms. B2B SaaS. No cash handling."
- **Predictable flows:** Avoid sudden large transfers; document purpose of each significant movement.
- **Single narrative:** Use the same SoF/SoW story across all providers — consistency builds trust.

---

## 3. Sovereign Positioning

### 3.1 UK Entity as Bridge

The UK entity ensures NEXUS PRIME's sovereign AI assets remain **unhindered by regional banking restrictions**:

| Risk | Mitigation |
|------|------------|
| GCC bank restrictions on Syrian nationals | UK entity holds contracts; payments flow to UK accounts |
| US sanctions screening (Stripe, etc.) | Entity-level KYC; UK company is customer, not individual |
| Regional payment rails | Wise/Revolut provide GBP/EUR/USD without GCC intermediary |
| Investor/invoice credibility | UK incorporation (First Formations) signals institutional structure |

### 3.2 Recommended Stack (Riyadh → UK → Global)

| Layer | Provider | Role |
|-------|----------|------|
| **Incorporation** | First Formations | UK company, registered office |
| **Primary Banking** | Revolut Business | Day-to-day ops, cards, payroll |
| **FX & International** | Wise Business | Multi-currency, low-fee transfers |
| **Payments (SaaS)** | Stripe | Subscriptions, one-time (entity-level) |
| **Contractor Payouts** | Payoneer (fallback) | If Revolut/Wise restrict |
| **Future GCC** | Wio / local KSA bank | When scaling in-region |

### 3.3 Execution Order

1. **UK entity** — Already done (First Formations).
2. **Compliance Shield pack** — Prepare SoF, PoR, SoW, AML policy, index.
3. **Wise Business** — Apply first (lowest friction, entity-led).
4. **Revolut Business** — Apply second (operational banking).
5. **Stripe** — Apply when ready for payments (Ecosystem API, Shadow Seven).
6. **Monitor** — Keep docs updated; refresh PoR every 6–12 months.

---

## 4. Summary: Friction-Less Path

```
Kier (Syrian / KSA Resident) + UK Entity (First Formations)
                    │
                    ├── Compliance Shield: SoF, PoR, SoW, AML, Index — READY
                    ├── Banking: Wise + Revolut (entity-led)
                    ├── Payments: Stripe (entity-level)
                    └── Sovereign: UK entity = bridge; NEXUS PRIME assets protected
```

**Outcome:** Syrian-owned UK firm operating from Riyadh with minimal friction, compliant posture, and sovereign AI assets channeled through a UK bridge.

---

*Document linked to: LAUNCH_READINESS_CHECKLIST.md — Section 7 (Compliance Shield)*
