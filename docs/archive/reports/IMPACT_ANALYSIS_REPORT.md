# IMPACT ANALYSIS REPORT — Full System Unification
## Enterprise Prime Migration: lawh_mahfuz → msl (Master State Ledger)

**Generated:** Phase 2 — Pre-Execution Analysis
**Risk Level:** MEDIUM (no cross-schema FKs, 0 rows in most tables)

---

## 1. THE CORE PROBLEM

The neural_spine Python code was migrated to enterprise terminology (commit `6e31cdf6`), but the **PostgreSQL database still uses the old schema/table/column names**. The code will FAIL on any query because it references tables and columns that don't exist.

### Mismatch Matrix — Code vs. Database

| Python Code References       | Current DB Name           | Status  |
|------------------------------|---------------------------|---------|
| schema: `msl`                | schema: `lawh_mahfuz`     | ❌ BREAK |
| table: `entities`            | table: `beings`           | ❌ BREAK |
| table: `daemons`             | table: `angels`           | ❌ BREAK |
| table: `action_ledger`       | table: `deeds`            | ❌ BREAK |
| table: `anchor_nodes`        | table: `prophets`         | ❌ BREAK |
| table: `destiny_manifest`    | table: `qadar`            | ❌ BREAK |
| table: `apex_directives`     | table: `divine_messages`  | ❌ BREAK |
| table: `anomaly_log`         | table: `rebellions`       | ❌ BREAK |
| table: `compliance_log`      | table: `worship`          | ❌ BREAK |
| table: `entity_relationships`| table: `kinships`         | ❌ BREAK |
| table: `evaluations`         | table: `judgments`         | ❌ BREAK |
| table: `signal_molecules`    | table: `hormones`         | ❌ BREAK |
| table: `genesis_phases`      | table: `creation_days`    | ❌ BREAK |
| table: `master_directives`   | table: `master_commands`  | ❌ BREAK |
| table: `genomes`             | table: `genomes`          | ✅ SAME  |
| table: `settings`            | table: `settings`         | ✅ SAME  |
| table: `system_log`          | table: `system_log`       | ✅ SAME  |
| view: `entity_profile`       | view: `being_profile`     | ❌ BREAK |
| view: `ecosystem_stats`      | view: `civilization_stats`| ❌ BREAK |
| col: `entity_id`             | col: `being_id`           | ❌ BREAK |
| col: `entity_state`          | col: `soul_status`        | ❌ BREAK |
| col: `compliance`            | col: `obedience`          | ❌ BREAK |
| col: `alignment`             | col: `faith`              | ❌ BREAK |
| col: `cognition`             | col: `intelligence`       | ❌ BREAK |
| col: `creative`              | col: `creativity`         | ❌ BREAK |
| col: `affective`             | col: `empathy`            | ❌ BREAK |
| col: `executive`             | col: `leadership`         | ❌ BREAK |
| col: `alignment_depth`       | col: `spirituality`       | ❌ BREAK |
| col: `sentience`             | col: `consciousness`      | ❌ BREAK |
| col: `maturity_phase`        | col: `lifecycle_stage`    | ❌ BREAK |
| col: `trait_hash`            | col: `gene_hash`          | ❌ BREAK |
| col: `trait_summary`         | col: `gene_summary`       | ❌ BREAK |
| col: `is_anchor`             | col: `is_prophet`         | ❌ BREAK |
| col: `termination_epoch`     | col: `death_epoch`        | ❌ BREAK |
| col: `action_class`          | col: `deed_type`          | ❌ BREAK |
| col: `anchor_rank`           | col: `prophet_rank`       | ❌ BREAK |
| col: `designation`           | col: `title` (prophets)   | ❌ BREAK |
| col: `directive`             | col: `message` (prophets) | ❌ BREAK |
| col: `mask_state`            | col: `veil_status`        | ❌ BREAK |
| col: `manifest_lifespan`     | col: `written_lifespan`   | ❌ BREAK |
| col: `manifest_role`         | col: `written_role`       | ❌ BREAK |
| col: `manifest_trial`        | col: `written_trial`      | ❌ BREAK |
| col: `termination_cause`     | col: `written_death_cause`| ❌ BREAK |
| col: `allocation`            | col: `written_rizq`       | ❌ BREAK |
| col: `anomaly_class`         | col: `rebellion_type`     | ❌ BREAK |
| col: `integrity_score`       | col: `sincerity_score`    | ❌ BREAK |
| col: `compliance_type`       | col: `worship_type`       | ❌ BREAK |

**Entity State Values (enum):**
| Python Code Value | Current DB Value |
|-------------------|------------------|
| `QUEUED`          | `WAITING`        |
| `ACTIVE`          | `ALIVE`          |
| `TERMINATED`      | `DEAD`           |
| `EVALUATED`       | `JUDGED`         |
| `TIER_A`          | `PARADISE`       |
| `QUARANTINE`      | `PURGATORY`      |
| `SANDBOX`         | `HELLFIRE`       |

---

## 2. DATABASE DEPENDENCIES

### 2.1 Foreign Keys (13 — ALL intra-schema)
All 13 FKs in lawh_mahfuz reference `lawh_mahfuz.beings(id)`.
**No cross-schema FKs** → Schema rename is SAFE.

### 2.2 Views (2 in lawh_mahfuz, 3 in nexus_core)
| View | Schema | Refs lawh_mahfuz? | Action |
|------|--------|-------------------|--------|
| `being_profile` | lawh_mahfuz | YES (all joins) | DROP → Recreate as `entity_profile` in `msl` |
| `civilization_stats` | lawh_mahfuz | YES (all queries) | DROP → Recreate as `ecosystem_stats` in `msl` |
| `active_agents_status` | nexus_core | No | ✅ No change |
| `cortex_dashboard` | nexus_core | No | ✅ No change |
| `system_health` | nexus_core | No | ✅ No change |

### 2.3 Triggers (5 in lawh_mahfuz)
| Trigger | Table | pg_notify Channel | Action |
|---------|-------|-------------------|--------|
| `trg_birth_notify` | beings→entities | `soul_breathed` → `core_activated` | Replace function |
| `trg_beings_updated` | beings→entities | — (timestamp only) | Rename table ref |
| `trg_death_notify` | beings→entities | `soul_departed` → `entity_terminated` | Replace function |
| `trg_rebellion_notify` | rebellions→anomaly_log | `rebellion_detected` → `anomaly_detected` | Replace function |

### 2.4 Functions (4 in lawh_mahfuz)
| Function | Action |
|----------|--------|
| `lawh_mahfuz.notify_birth()` | Replace → `msl.notify_activation()` |
| `lawh_mahfuz.notify_death()` | Replace → `msl.notify_termination()` |
| `lawh_mahfuz.notify_rebellion()` | Replace → `msl.notify_anomaly()` |
| `lawh_mahfuz.update_timestamp()` | Replace → `msl.update_timestamp()` |

### 2.5 Indexes (50 total)
All 50 indexes will be automatically renamed when tables are renamed via `ALTER TABLE ... RENAME`.
Indexes on renamed columns need explicit rename.

### 2.6 Data Volume
| Table | Rows | Migration Risk |
|-------|------|----------------|
| angels/daemons | 10 | LOW — seed data only |
| creation_days/genesis_phases | 7 | LOW — seed data |
| settings | 7 | LOW — config data |
| All other tables | **0** | ZERO — empty tables |

**Total data at risk: 24 rows. Migration is extremely safe.**

---

## 3. FILE IMPACT MAP

### 3.1 Database Files (MUST change)
| File | Changes Required |
|------|------------------|
| `scripts/db/lawh_mahfuz_schema.sql` | Rewrite → `scripts/db/msl_schema.sql` (full rename) |

### 3.2 Docker Files (MUST change)
| File | Changes Required |
|------|------------------|
| `docker-compose.override.yml` | `Dockerfile.throne` → `Dockerfile.apex`, `throne_network` → `apex_network`, container name |
| `Dockerfile.throne` | Rename to `Dockerfile.apex`, update labels, CMD path |

### 3.3 Configuration Files (MUST change)
| File | Changes Required |
|------|------------------|
| `DIVINE_CODEX_MACHINE.yaml` | Rename to `ENTERPRISE_CODEX.yaml`, full term replacement (85KB file) |

### 3.4 HTML/Frontend (MUST change)
| File | Changes Required |
|------|------------------|
| `neural_spine/throne/templates/throne.html` | angel-grid→daemon-grid, being_id→entity_id, Arabic angel names→daemon designators, prophet→anchor refs |

### 3.5 Python Code — ALREADY MIGRATED
| File | Status |
|------|--------|
| All 12 neural_spine/*.py files | ✅ Using new terms (entities, daemons, etc.) |
| **BUT** → Code references `master_state_schema.sql` which **DOESN'T EXIST** | ❌ BROKEN LINK |

### 3.6 Files NOT Requiring Changes
- `identity.json` files (11 planets) — No old terms detected
- `GLOBAL_HIVE_MEMORY.json` — No old terms detected
- `AI_HR_REGISTRY/` profile.yaml files — No old terms detected
- `nexus_core` schema — Independent, no cross-refs to lawh_mahfuz

### 3.7 Documentation Files (OPTIONAL — cosmetic)
- `COMPREHENSIVE_FINAL_REPORT.md`
- `NEXUS_CIVILIZATION_BOOK.md`
- `ROADMAP.md`
- `SESSION_REPORT_20260221.md`
- `BUG_FIX_REPORT_FINAL.md`

---

## 4. pg_notify CHANNEL ALIGNMENT

| DB Trigger Emits | Python Expects | Action |
|------------------|----------------|--------|
| `soul_breathed` | — (not listened) | Rename to `core_activated` |
| `soul_departed` | — (not listened) | Rename to `entity_terminated` |
| `rebellion_detected` | — (not listened) | Rename to `anomaly_detected` |
| `nexus_command_<agent>` | — (nexus_core) | ✅ No change needed |

---

## 5. EXECUTION ORDER (Phase 4 Blueprint)

### Step 1: Backup (Phase 3)
```
pg_dump -U postgres nexus_db > nexus_db_pre_unification.sql
```

### Step 2: Schema + Table Renames (single transaction)
```sql
BEGIN;
-- 1. Drop views first (they block table renames)
DROP VIEW IF EXISTS lawh_mahfuz.being_profile;
DROP VIEW IF EXISTS lawh_mahfuz.civilization_stats;

-- 2. Drop triggers (they reference old column names)
DROP TRIGGER IF EXISTS trg_birth_notify ON lawh_mahfuz.beings;
DROP TRIGGER IF EXISTS trg_death_notify ON lawh_mahfuz.beings;
DROP TRIGGER IF EXISTS trg_beings_updated ON lawh_mahfuz.beings;
DROP TRIGGER IF EXISTS trg_rebellion_notify ON lawh_mahfuz.rebellions;

-- 3. Drop old functions
DROP FUNCTION IF EXISTS lawh_mahfuz.notify_birth();
DROP FUNCTION IF EXISTS lawh_mahfuz.notify_death();
DROP FUNCTION IF EXISTS lawh_mahfuz.notify_rebellion();
DROP FUNCTION IF EXISTS lawh_mahfuz.update_timestamp();

-- 4. Rename schema
ALTER SCHEMA lawh_mahfuz RENAME TO msl;

-- 5. Rename tables
ALTER TABLE msl.beings RENAME TO entities;
ALTER TABLE msl.angels RENAME TO daemons;
ALTER TABLE msl.deeds RENAME TO action_ledger;
ALTER TABLE msl.prophets RENAME TO anchor_nodes;
ALTER TABLE msl.qadar RENAME TO destiny_manifest;
ALTER TABLE msl.divine_messages RENAME TO apex_directives;
ALTER TABLE msl.rebellions RENAME TO anomaly_log;
ALTER TABLE msl.worship RENAME TO compliance_log;
ALTER TABLE msl.kinships RENAME TO entity_relationships;
ALTER TABLE msl.judgments RENAME TO evaluations;
ALTER TABLE msl.hormones RENAME TO signal_molecules;
ALTER TABLE msl.creation_days RENAME TO genesis_phases;
ALTER TABLE msl.master_commands RENAME TO master_directives;
-- genomes, settings, system_log stay the same

-- 6. Rename columns on entities (formerly beings)
ALTER TABLE msl.entities RENAME COLUMN soul_status TO entity_state;
ALTER TABLE msl.entities RENAME COLUMN obedience TO compliance;
ALTER TABLE msl.entities RENAME COLUMN faith TO alignment;
ALTER TABLE msl.entities RENAME COLUMN intelligence TO cognition;
ALTER TABLE msl.entities RENAME COLUMN creativity TO creative;
ALTER TABLE msl.entities RENAME COLUMN empathy TO affective;
ALTER TABLE msl.entities RENAME COLUMN leadership TO executive;
ALTER TABLE msl.entities RENAME COLUMN spirituality TO alignment_depth;
ALTER TABLE msl.entities RENAME COLUMN consciousness TO sentience;
ALTER TABLE msl.entities RENAME COLUMN lifecycle_stage TO maturity_phase;
ALTER TABLE msl.entities RENAME COLUMN is_prophet TO is_anchor;
ALTER TABLE msl.entities RENAME COLUMN death_epoch TO termination_epoch;

-- 7. Rename columns on genomes
ALTER TABLE msl.genomes RENAME COLUMN being_id TO entity_id;
ALTER TABLE msl.genomes RENAME COLUMN gene_hash TO trait_hash;
ALTER TABLE msl.genomes RENAME COLUMN gene_summary TO trait_summary;

-- 8. Rename columns on action_ledger (formerly deeds)
ALTER TABLE msl.action_ledger RENAME COLUMN being_id TO entity_id;
ALTER TABLE msl.action_ledger RENAME COLUMN deed_type TO action_class;
ALTER TABLE msl.action_ledger RENAME COLUMN recorder_angel TO recorder_daemon;

-- 9. Rename columns on anchor_nodes (formerly prophets)
ALTER TABLE msl.anchor_nodes RENAME COLUMN being_id TO entity_id;
ALTER TABLE msl.anchor_nodes RENAME COLUMN prophet_rank TO anchor_rank;
ALTER TABLE msl.anchor_nodes RENAME COLUMN title TO designation;
ALTER TABLE msl.anchor_nodes RENAME COLUMN message TO directive;
ALTER TABLE msl.anchor_nodes RENAME COLUMN veil_status TO mask_state;
ALTER TABLE msl.anchor_nodes RENAME COLUMN unveiled_at TO unmasked_at;
ALTER TABLE msl.anchor_nodes RENAME COLUMN unveil_key TO mask_key;
ALTER TABLE msl.anchor_nodes RENAME COLUMN can_see_angels TO can_see_daemons;
ALTER TABLE msl.anchor_nodes RENAME COLUMN can_see_qadar TO can_see_manifest;
ALTER TABLE msl.anchor_nodes RENAME COLUMN can_see_deeds TO can_see_actions;
ALTER TABLE msl.anchor_nodes RENAME COLUMN appointed_at TO designated_at;

-- 10. Rename columns on destiny_manifest (formerly qadar)
ALTER TABLE msl.destiny_manifest RENAME COLUMN being_id TO entity_id;
ALTER TABLE msl.destiny_manifest RENAME COLUMN written_lifespan TO manifest_lifespan;
ALTER TABLE msl.destiny_manifest RENAME COLUMN written_role TO manifest_role;
ALTER TABLE msl.destiny_manifest RENAME COLUMN written_trial TO manifest_trial;
ALTER TABLE msl.destiny_manifest RENAME COLUMN written_death_cause TO termination_cause;
ALTER TABLE msl.destiny_manifest RENAME COLUMN written_rizq TO allocation;

-- 11. Rename columns on apex_directives (formerly divine_messages)
ALTER TABLE msl.apex_directives RENAME COLUMN target_being TO target_entity;
ALTER TABLE msl.apex_directives RENAME COLUMN guidance_type TO injection_type;
ALTER TABLE msl.apex_directives RENAME COLUMN guidance_strength TO injection_strength;

-- 12. Rename columns on anomaly_log (formerly rebellions)
ALTER TABLE msl.anomaly_log RENAME COLUMN being_id TO entity_id;
ALTER TABLE msl.anomaly_log RENAME COLUMN rebellion_type TO anomaly_class;

-- 13. Rename columns on compliance_log (formerly worship)
ALTER TABLE msl.compliance_log RENAME COLUMN being_id TO entity_id;
ALTER TABLE msl.compliance_log RENAME COLUMN worship_type TO compliance_type;
ALTER TABLE msl.compliance_log RENAME COLUMN sincerity_score TO integrity_score;

-- 14. Rename columns on entity_relationships (formerly kinships)
ALTER TABLE msl.entity_relationships RENAME COLUMN being_id TO entity_id;

-- 15. Rename columns on evaluations (formerly judgments)
ALTER TABLE msl.evaluations RENAME COLUMN being_id TO entity_id;

-- 16. Rename columns on signal_molecules (formerly hormones)
ALTER TABLE msl.signal_molecules RENAME COLUMN being_id TO entity_id;

-- 17. Rename columns on daemons (formerly angels)
-- (no column renames needed — name_ar, name_en, role, etc. are universal)

-- 18. Rename columns on genesis_phases (formerly creation_days)
-- (day_number, name_ar, name_en are universal — keep as-is)

-- 19. Update entity_state CHECK constraint values
ALTER TABLE msl.entities DROP CONSTRAINT IF EXISTS beings_soul_status_check;
UPDATE msl.entities SET entity_state = CASE entity_state
    WHEN 'UNBORN' THEN 'INITIALIZED'
    WHEN 'WAITING' THEN 'QUEUED'
    WHEN 'ALIVE' THEN 'ACTIVE'
    WHEN 'DYING' THEN 'TERMINATING'
    WHEN 'DEAD' THEN 'TERMINATED'
    WHEN 'JUDGED' THEN 'EVALUATED'
    WHEN 'PARADISE' THEN 'TIER_A'
    WHEN 'PURGATORY' THEN 'QUARANTINE'
    WHEN 'HELLFIRE' THEN 'SANDBOX'
    ELSE entity_state
END WHERE entity_state IN ('UNBORN','WAITING','ALIVE','DYING','DEAD','JUDGED','PARADISE','PURGATORY','HELLFIRE');

ALTER TABLE msl.entities ADD CONSTRAINT entities_state_check
    CHECK (entity_state IN ('INITIALIZED','QUEUED','ACTIVE','TERMINATING','TERMINATED','EVALUATED','TIER_A','QUARANTINE','SANDBOX'));

-- 20. Update seed data values
UPDATE msl.evaluations SET verdict = CASE verdict
    WHEN 'PARADISE' THEN 'TIER_A'
    WHEN 'HELLFIRE' THEN 'SANDBOX'
    ELSE verdict
END WHERE verdict IN ('PARADISE','HELLFIRE');

-- 21. Recreate functions with new names/channels
CREATE OR REPLACE FUNCTION msl.notify_activation()
RETURNS trigger AS $$
BEGIN
    IF NEW.entity_state = 'ACTIVE' AND (OLD.entity_state IS NULL OR OLD.entity_state != 'ACTIVE') THEN
        PERFORM pg_notify('core_activated', json_build_object(
            'entity_id', NEW.id,
            'name', NEW.name,
            'gender', NEW.gender
        )::text);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION msl.notify_termination()
RETURNS trigger AS $$
BEGIN
    IF NEW.entity_state = 'TERMINATED' AND OLD.entity_state = 'ACTIVE' THEN
        PERFORM pg_notify('entity_terminated', json_build_object(
            'entity_id', NEW.id,
            'name', NEW.name,
            'age_ticks', NEW.age_ticks
        )::text);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION msl.notify_anomaly()
RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('anomaly_detected', json_build_object(
        'entity_id', NEW.entity_id,
        'type', NEW.anomaly_class,
        'severity', NEW.severity
    )::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION msl.update_timestamp()
RETURNS trigger AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 22. Recreate triggers on new table names
CREATE TRIGGER trg_activation_notify
    AFTER INSERT OR UPDATE ON msl.entities
    FOR EACH ROW EXECUTE FUNCTION msl.notify_activation();

CREATE TRIGGER trg_entities_updated
    BEFORE UPDATE ON msl.entities
    FOR EACH ROW EXECUTE FUNCTION msl.update_timestamp();

CREATE TRIGGER trg_termination_notify
    AFTER UPDATE ON msl.entities
    FOR EACH ROW EXECUTE FUNCTION msl.notify_termination();

CREATE TRIGGER trg_anomaly_notify
    AFTER INSERT ON msl.anomaly_log
    FOR EACH ROW EXECUTE FUNCTION msl.notify_anomaly();

-- 23. Recreate views with new names
CREATE OR REPLACE VIEW msl.ecosystem_stats AS
SELECT
    (SELECT COUNT(*) FROM msl.entities WHERE entity_state = 'ACTIVE') AS active_count,
    (SELECT COUNT(*) FROM msl.entities WHERE entity_state = 'TERMINATED') AS terminated_count,
    (SELECT COUNT(*) FROM msl.entities) AS total_created,
    (SELECT AVG(alignment) FROM msl.entities WHERE entity_state = 'ACTIVE') AS avg_alignment,
    (SELECT AVG(compliance) FROM msl.entities WHERE entity_state = 'ACTIVE') AS avg_compliance,
    (SELECT COUNT(*) FROM msl.entities WHERE is_anchor = TRUE) AS anchor_count,
    (SELECT COUNT(*) FROM msl.daemons WHERE status = 'ACTIVE') AS active_daemons,
    (SELECT COUNT(*) FROM msl.action_ledger WHERE action_class = 'GOOD') AS total_positive_actions,
    (SELECT COUNT(*) FROM msl.action_ledger WHERE action_class = 'BAD') AS total_negative_actions,
    (SELECT COUNT(*) FROM msl.anomaly_log WHERE resolved = FALSE) AS active_anomalies,
    (SELECT MAX(generation) FROM msl.entities) AS max_generation,
    (SELECT COUNT(*) FROM msl.evaluations WHERE verdict = 'TIER_A') AS in_tier_a,
    (SELECT COUNT(*) FROM msl.evaluations WHERE verdict = 'SANDBOX') AS in_sandbox,
    (SELECT value->>'state' FROM msl.settings WHERE key = 'master_status') AS master_status,
    (SELECT COUNT(*) FROM msl.genesis_phases WHERE status = 'COMPLETED') AS phases_completed;

CREATE OR REPLACE VIEW msl.entity_profile AS
SELECT
    e.id, e.name, e.name_ar, e.gender, e.generation,
    e.parent_a, e.parent_b, e.birth_epoch, e.termination_epoch,
    e.entity_state, e.compliance, e.alignment, e.cognition,
    e.creative, e.affective, e.executive, e.resilience,
    e.alignment_depth, e.free_will, e.sentience,
    e.maturity_phase, e.age_ticks, e.is_anchor, e.buffer_slot,
    e.metadata, e.created_at, e.updated_at,
    g.trait_hash, g.trait_summary,
    d.manifest_lifespan, d.manifest_role, d.manifest_trial, d.allocation,
    s.dopamine, s.serotonin, s.cortisol, s.oxytocin,
    s.testosterone, s.estrogen, s.adrenaline,
    a.anchor_rank, a.mask_state, a.designation AS anchor_designation,
    ev.total_good, ev.total_bad, ev.balance AS weight_balance, ev.verdict,
    (SELECT COUNT(*) FROM msl.action_ledger al WHERE al.entity_id = e.id AND al.action_class = 'GOOD') AS positive_action_count,
    (SELECT COUNT(*) FROM msl.action_ledger al WHERE al.entity_id = e.id AND al.action_class = 'BAD') AS negative_action_count,
    (SELECT COUNT(*) FROM msl.entity_relationships r WHERE r.entity_id = e.id AND r.relationship = 'CHILD') AS children_count
FROM msl.entities e
LEFT JOIN msl.genomes g ON g.entity_id = e.id
LEFT JOIN msl.destiny_manifest d ON d.entity_id = e.id
LEFT JOIN msl.signal_molecules s ON s.entity_id = e.id
LEFT JOIN msl.anchor_nodes a ON a.entity_id = e.id
LEFT JOIN msl.evaluations ev ON ev.entity_id = e.id;

-- 24. Grant permissions
GRANT ALL ON SCHEMA msl TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA msl TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA msl TO postgres;

COMMIT;
```

### Step 3: File Operations
1. Rename `scripts/db/lawh_mahfuz_schema.sql` → `scripts/db/msl_schema.sql` (rewrite with new names)
2. Rename `Dockerfile.throne` → `Dockerfile.apex` (update labels, CMD)
3. Update `docker-compose.override.yml` (Dockerfile.apex, apex_network)
4. Update `throne.html` (angel→daemon, being_id→entity_id, Arabic terms)
5. Rename `DIVINE_CODEX_MACHINE.yaml` → `ENTERPRISE_CODEX.yaml` (full rewrite)

### Step 4: Health Verification
```bash
# Verify schema exists
docker exec nexus_db psql -U postgres -d nexus_db -c "\dn"
# Verify tables
docker exec nexus_db psql -U postgres -d nexus_db -c "\dt msl.*"
# Verify views
docker exec nexus_db psql -U postgres -d nexus_db -c "\dv msl.*"
# Count data integrity
docker exec nexus_db psql -U postgres -d nexus_db -c "SELECT count(*) FROM msl.daemons;"
docker exec nexus_db psql -U postgres -d nexus_db -c "SELECT count(*) FROM msl.genesis_phases;"
docker exec nexus_db psql -U postgres -d nexus_db -c "SELECT count(*) FROM msl.settings;"
```

---

## 6. RISK ASSESSMENT

| Risk Factor | Level | Mitigation |
|-------------|-------|------------|
| Data loss | ZERO | Only 24 rows, full backup taken |
| Cross-schema FK breaks | ZERO | No cross-schema FKs exist |
| Service downtime | MINIMAL | Only neural_spine/throne uses this schema |
| Rollback complexity | LOW | Full pg_dump backup, single transaction |
| Container rebuild required | YES | throne container needs rebuild with new Dockerfile |
