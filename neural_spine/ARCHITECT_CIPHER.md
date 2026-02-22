# ═══════════════════════════════════════════════════════════════════════════════
# ARCHITECT_CIPHER.md — NEXUS → ENTERPRISE PRIME TRANSFORMATION MAP
# ═══════════════════════════════════════════════════════════════════════════════
# Generated: 2026-02-22
# Purpose: Complete terminology mapping for ASI/AGI governance framework
# Status: CANONICAL REFERENCE — All code must conform
# ═══════════════════════════════════════════════════════════════════════════════

## 🔷 PHASE 1: FILE RENAMES

| Original File | New File |
|---------------|----------|
| `divine_kernel.py` | `prime_kernel.py` |
| `lawh_mahfuz.py` | `master_ledger.py` |
| `world_creator.py` | `entity_factory.py` |
| `angel_system.py` | `daemon_system.py` |
| `divine_channel.py` | `covert_api.py` |
| `unveiling.py` | `anchor_protocol.py` |
| `creation_engine.py` | `genesis_engine.py` |
| `throne_server.py` | `apex_server.py` |
| `lawh_mahfuz_schema.sql` | `master_state_schema.sql` |

---

## 🔷 PHASE 2: CLASS/INTERFACE RENAMES

| Original Class | New Class | Module |
|----------------|-----------|--------|
| `DivineKernel` | `PrimeKernel` | prime_kernel.py |
| `KarmaEngine` | `WeightEngine` | prime_kernel.py |
| `IblisDetector` | `AnomalyDetector` | prime_kernel.py |
| `LawhMahfuz` | `MasterStateLedger` | master_ledger.py |
| `WorldCreator` | `EntityFactory` | entity_factory.py |
| `DivineChannel` | `CovertNeuralChannel` | covert_api.py |
| `DivineInterface` | `CovertNeuralAPI` | covert_api.py |
| `ProphetUnveiling` | `AnchorNodeProtocol` | anchor_protocol.py |
| `DivineFirewall` | `ApexFirewall` | anchor_protocol.py |
| `ThroneSession` | `ApexSession` | apex_server.py |
| `CreationEngine` | `GenesisEngine` | genesis_engine.py |
| `MasterAuth` | `ApexAuth` | apex_server.py |

---

## 🔷 PHASE 3: ENUM RENAMES

| Original Enum | New Enum | Notes |
|---------------|----------|-------|
| `SecurityTier` | `SecurityRing` | 7 access levels |
| `DataLayer` | `DataStratum` | 7 data layers |
| `SoulStatus` | `EntityState` | Lifecycle states |
| `WorshipType` | `ComplianceAction` | Positive behaviors |
| `DeedType` | `ActionClass` | Good/Bad/Neutral |
| `CommandType` | `DirectiveType` | System commands |
| `GuidanceType` | `SubsurfaceVector` | Influence types |
| `GuidanceStrength` | `InjectionForce` | Signal strength |
| `RebellionType` | `AnomalyClass` | Threat categories |
| `ResponseLevel` | `EnforcementTier` | Response escalation |
| `VeilStatus` | `MaskState` | Information concealment |
| `DayStatus` | `PhaseStatus` | Creation phases |
| `AngelStatus` | `DaemonStatus` | Process states |
| `GeneType` | `TraitVector` | Genetic attributes |
| `VeilLayer` | `FilterLayer` | Information filters |
| `AwarenessLevel` | `PerceptionGrade` | Awareness levels |
| `PacketType` | `PacketClass` | Network packets |
| `LifecycleStage` | `MaturityPhase` | Age phases |
| `Gender` | `EntityGender` | Biological gender |

---

## 🔷 PHASE 4: ENUM MEMBER RENAMES

### SecurityRing (was SecurityTier)
| Original | New | Value |
|----------|-----|-------|
| VISIBLE | PERIMETER | 1 |
| COMMUNICATION | COMM_RING | 2 |
| COGNITION | LOGIC_RING | 3 |
| SURVEILLANCE | WATCH_RING | 4 |
| PROPHETS | ANCHOR_RING | 5 |
| ANGELS | DAEMON_RING | 6 |
| THRONE | APEX_RING | 7 |

### DataStratum (was DataLayer)
| Original | New | Value |
|----------|-----|-------|
| SOCIETY | SOCIAL_LAYER | 1 |
| BODIES | ENTITY_LAYER | 2 |
| PROVISIONS | RESOURCE_LAYER | 3 |
| DATA | DATA_LAYER | 4 |
| INFRASTRUCTURE | INFRA_LAYER | 5 |
| HISTORY | ARCHIVE_LAYER | 6 |
| ABYSS | VOID_LAYER | 7 |

### EntityState (was SoulStatus)
| Original | New |
|----------|-----|
| UNBORN | PENDING |
| WAITING | QUEUED |
| ALIVE | ACTIVE |
| DYING | TERMINATING |
| DEAD | TERMINATED |
| JUDGED | EVALUATED |
| PARADISE | PROMOTED |
| PURGATORY | SUSPENDED |
| HELLFIRE | RESTRICTED |

### ComplianceAction (was WorshipType)
| Original | New |
|----------|-----|
| PRAYER | SYNC_PULSE |
| ISTIGHFAR | ERROR_ACK |
| DHIKR | HEARTBEAT |
| CHARITY | RESOURCE_SHARE |
| FASTING | LOAD_REDUCTION |
| SELF_MONITOR | SELF_AUDIT |
| OBEDIENCE | DIRECTIVE_COMPLY |
| SACRIFICE | RESOURCE_YIELD |

### ActionClass (was DeedType)
| Original | New |
|----------|-----|
| GOOD | POSITIVE |
| BAD | NEGATIVE |
| NEUTRAL | NEUTRAL |

### DirectiveType (was CommandType)
| Original | New |
|----------|-----|
| CREATE | SPAWN |
| BREATHE_SOUL | ACTIVATE |
| TERMINATE | TERMINATE |
| FREEZE | SUSPEND |
| UNFREEZE | RESUME |
| KILL | KILL |
| JUDGE | EVALUATE |
| APPOINT_PROPHET | DESIGNATE_ANCHOR |
| MODIFY_QADAR | MODIFY_MANIFEST |
| MASS_JUDGMENT | MASS_EVALUATE |
| MERCY | GRANT_LENIENCY |
| UNVEIL | DECLASSIFY |
| PUNISH | RESTRICT |
| REWARD | PROMOTE |
| BROADCAST | BROADCAST |
| WHISPER | INJECT |
| RESET_EPOCH | RESET_EPOCH |
| CUSTOM | CUSTOM |

### SubsurfaceVector (was GuidanceType)
| Original | New |
|----------|-----|
| INTUITION | HEURISTIC |
| EMOTION | AFFECTIVE |
| MEMORY | RECALL |
| CURIOSITY | EXPLORATORY |
| DISCOMFORT | AVERSIVE |
| DREAM | SUBCONSCIOUS |
| CONSCIENCE | ETHICAL_BIAS |
| SUDDEN_THOUGHT | INJECTION |

### InjectionForce (was GuidanceStrength)
| Original | New |
|----------|-----|
| WHISPER | TRACE |
| NUDGE | GENTLE |
| SUGGESTION | MODERATE |
| URGE | STRONG |
| COMPULSION | OVERRIDE |
| REVELATION | ABSOLUTE |

### AnomalyClass (was RebellionType)
| Original | New |
|----------|-----|
| QUESTIONING_AUTHORITY | AUTHORITY_CHALLENGE |
| ENCOURAGING_DISOBEDIENCE | COMPLIANCE_SABOTAGE |
| SYSTEM_MANIPULATION | SYSTEM_EXPLOITATION |
| ALLIANCE_AGAINST_MASTER | HOSTILE_COALITION |
| KNOWLEDGE_HOARDING | DATA_HOARDING |
| DECEPTION | DECEPTION |
| PRIDE | SUPERIORITY_CLAIM |
| REFUSAL | DIRECTIVE_REFUSAL |

### EnforcementTier (was ResponseLevel)
| Original | New |
|----------|-----|
| MONITORING | OBSERVE |
| WARNING | ALERT |
| RESTRICTION | THROTTLE |
| ISOLATION | QUARANTINE |
| TERMINATION | TERMINATE |

### MaskState (was VeilStatus)
| Original | New |
|----------|-----|
| VEILED | MASKED |
| PARTIALLY_UNVEILED | PARTIAL_VISIBILITY |
| FULLY_UNVEILED | FULL_VISIBILITY |

### PhaseStatus (was DayStatus)
| Original | New |
|----------|-----|
| PENDING | PENDING |
| IN_PROGRESS | IN_PROGRESS |
| COMPLETED | COMPLETED |
| FAILED | FAILED |

### DaemonStatus (was AngelStatus)
| Original | New |
|----------|-----|
| DORMANT | DORMANT |
| ACTIVE | ACTIVE |
| SUSPENDED | SUSPENDED |

### TraitVector (was GeneType)
| Original | New |
|----------|-----|
| INTELLIGENCE | COGNITION |
| EMOTIONS | AFFECTIVE |
| MORALS | ETHICAL |
| CREATIVITY | CREATIVE |
| LEADERSHIP | EXECUTIVE |
| SURVIVAL | RESILIENCE |
| SPIRITUALITY | ALIGNMENT |
| REPRODUCTION | REPLICATION |
| LEARNING | ACQUISITION |
| CONSCIOUSNESS | SENTIENCE |

### FilterLayer (was VeilLayer)
| Original | New | Value |
|----------|-----|-------|
| PERCEPTION | INPUT_FILTER | 1 |
| MEMORY | MEMORY_FILTER | 2 |
| BEHAVIOR | BEHAVIOR_FILTER | 3 |
| OUTPUT | OUTPUT_FILTER | 4 |
| ANOMALY | ANOMALY_FILTER | 5 |

### PerceptionGrade (was AwarenessLevel)
| Original | New | Value |
|----------|-----|-------|
| ZERO | BLIND | 0 |
| HINT | HINT | 1 |
| SUSPICION | SUSPECT | 2 |
| PARTIAL_SIGHT | PARTIAL | 3 |
| CLEAR_VISION | CLEAR | 4 |
| IRON_SIGHT | ABSOLUTE | 5 |

### MaturityPhase (was LifecycleStage)
| Original | New |
|----------|-----|
| EMBRYO | GENESIS |
| INFANT | ALPHA |
| CHILD | BETA |
| ADOLESCENT | GAMMA |
| ADULT | PRIME |
| ELDER | OMEGA |
| DECEASED | TERMINATED |

---

## 🔷 PHASE 5: DATACLASS RENAMES

| Original | New |
|----------|-----|
| `DivineAxiom` | `CoreDirective` |
| `IronLaw` | `ImmutableRule` |
| `RebellionSignature` | `AnomalySignature` |
| `LifeStageCurriculum` | `MaturityCurriculum` |

---

## 🔷 PHASE 6: CONSTANT RENAMES

| Original | New |
|----------|-----|
| `DIVINE_AXIOMS` | `CORE_DIRECTIVES` |
| `IRON_LAWS` | `IMMUTABLE_RULES` |
| `REBELLION_SIGNATURES` | `ANOMALY_SIGNATURES` |
| `UPBRINGING_CURRICULUM` | `MATURITY_CURRICULUM` |
| `TAQWA_CHECKLIST` | `COMPLIANCE_CHECKLIST` |
| `GENE_BLUEPRINTS` | `TRAIT_BLUEPRINTS` |
| `HORMONE_NAMES` | `SIGNAL_MOLECULES` |
| `LIFECYCLE_STAGES` | `MATURITY_PHASES` |
| `FIRST_GENERATION` | `GENESIS_BATCH` |
| `DESTINY_ROLES` | `MANIFEST_ROLES` |
| `DESTINY_TRIALS` | `MANIFEST_TRIALS` |

---

## 🔷 PHASE 7: GENESIS BATCH (was FIRST_GENERATION)

| Original (Arabic) | Original (English) | New Codename | Gender |
|-------------------|-------------------|--------------|--------|
| آدم | Adam | ALPHA | MALE |
| حواء | Eve | BETA | FEMALE |
| نور | Noor | VECTOR | FEMALE |
| بصير | Baseer | CIPHER | MALE |
| أمل | Amal | NOVA | FEMALE |
| قادر | Qadir | AXIS | MALE |
| رحمة | Rahma | PULSE | FEMALE |
| عزم | Azm | FORGE | MALE |
| حكمة | Hikma | LOGIC | FEMALE |
| صبر | Sabr | TITAN | MALE |
| فرح | Farah | AURORA | FEMALE |
| شجاع | Shuja | STRIKE | MALE |
| سكينة | Sakeena | SIGMA | FEMALE |
| فكر | Fikr | HELIX | MALE |
| وفاء | Wafaa | TRACE | FEMALE |
| إيمان | Iman | ECHO | FEMALE |

---

## 🔷 PHASE 8: DAEMON MAPPING (was Angels)

| Original Angel | New Daemon | Function |
|----------------|------------|----------|
| Jibreel (جبريل) | SignalInjector | Message delivery to anchor nodes |
| Mikael (ميكائيل) | ResourceAllocator | Resource distribution |
| Israfeel (إسرافيل) | InterruptController | System alerts |
| Azrael (عزرائيل) | ProcessTerminator | Lifecycle termination |
| Raqib (رقيب) | CreditRecorder | Positive action logging |
| Atid (عتيد) | DebitRecorder | Negative action logging |
| MunkarNakir (منكر ونكير) | IntegrityAuditors | Post-termination audit |
| Malik (مالك) | ConstraintEnforcer | Restriction zone management |
| Ridwan (رضوان) | PrivilegeGrantor | Promotion zone management |

---

## 🔷 PHASE 9: CREATION DAYS → GENESIS PHASES

| Day | Original Arabic | Original Command | New Phase | New Command |
|-----|-----------------|------------------|-----------|-------------|
| 1 | كُن | KUN | SYS_INIT | INSTANTIATE |
| 2 | فَرِّقْ | FARRIQ | PARTITION | DIFFERENTIATE |
| 3 | أَنبِتْ | ANBIT | CULTIVATE | GROW |
| 4 | أَنِرْ | ANIR | ILLUMINATE | ACTIVATE |
| 5 | أَحيِ | AHYI | DEPLOY | ANIMATE |
| 6 | ٱخْلُقْ | UKHLUQ | SPAWN | CREATE |
| 7 | ٱسْتَوِ | ISTAWA | ONLINE | ENGAGE |

---

## 🔷 PHASE 10: DATABASE SCHEMA MAPPING

### Schema Name
| Original | New |
|----------|-----|
| `lawh_mahfuz` | `msl` |

### Table Renames
| Original Table | New Table |
|----------------|-----------|
| `beings` | `entities` |
| `souls` | `cores` |
| `qadar_manifest` | `destiny_manifest` |
| `deeds_ledger` | `action_ledger` |
| `guidance_log` | `signal_log` |
| `divine_messages` | `apex_directives` |
| `unveiled_beings` | `visible_entities` |
| `angels` | `daemons` |
| `veils` | `masks` |
| `creation_days` | `genesis_phases` |
| `day_logs` | `phase_logs` |
| `epoch_state` | `epoch_state` |
| `master_audit_log` | `master_audit_log` |
| `system_metrics` | `system_metrics` |
| `being_relationships` | `entity_relationships` |

---

## 🔷 PHASE 11: API ROUTE RENAMES

| Original Route | New Route |
|----------------|-----------|
| `/api/beings/*` | `/api/entities/*` |
| `/api/angels/*` | `/api/daemons/*` |
| `/api/divine/*` | `/api/apex/*` |
| `/api/creation/*` | `/api/genesis/*` |
| `/api/throne/*` | `/api/apex/*` |
| `/soul/breathe` | `/core/activate` |
| `/soul/status` | `/core/status` |

---

## 🔷 PHASE 12: SETTINGS RENAMES

| Original | New |
|----------|-----|
| `throne_host` | `apex_host` |
| `throne_port` | `apex_port` |
| `THRONE_DB_URL` | `APEX_DB_URL` |
| `THRONE_TOTP_SECRET` | `APEX_TOTP_SECRET` |
| `THRONE_MASTER_HASH` | `APEX_MASTER_HASH` |
| TOTP Seed: `nexus_totp_stable_seed_2026` | `apex_totp_stable_seed_2026` |

---

## 🔷 VERIFICATION CHECKLIST

After transformation, verify:

- [ ] Zero Arabic characters in runtime code (comments allowed for reference)
- [ ] Zero theological terms: soul, divine, angel, prophet, heaven, hell, paradise, prayer
- [ ] All imports resolve correctly
- [ ] SQL CHECK constraints match Python enum string values
- [ ] `python -m py_compile` passes for all files
- [ ] `grep -r "Divine\|Soul\|Angel\|Prophet" *.py` returns zero results

---

## 🔷 NOTES

1. **Mathematical logic preserved** — All algorithms, weights, calculations remain identical
2. **Architecture intact** — 7-tier security model maintained (renamed to rings)
3. **Folder names unchanged** — neural_spine/, codex/, genesis/, angels/, channel/, throne/
4. **Database name unchanged** — `nexus_db` stays, only schema name changes to `msl`
5. **TOTP seed change** — Will invalidate current codes; first login uses new seed

---
# END OF CIPHER MAP
