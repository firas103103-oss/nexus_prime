-- ══════════════════════════════════════════════════════════════════════
-- MSL — Master State Ledger
-- Schema: msl
-- Database: nexus_db (existing PostgreSQL instance)
-- Created: 2026-02-21
-- Purpose: Complete entity persistence — entities, genetics, destiny manifests,
--          actions, evaluations, daemons, anchor nodes, apex directives, commands
-- ══════════════════════════════════════════════════════════════════════

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create isolated schema
CREATE SCHEMA IF NOT EXISTS msl;
SET search_path TO msl, public;

-- ── 1. GENESIS PHASES ─────────────────────────────────────────────────
-- Tracks the 7 phases of genesis with full metrics
CREATE TABLE msl.genesis_phases (
    phase_number      INTEGER PRIMARY KEY CHECK (phase_number BETWEEN 1 AND 7),
    name_ar         TEXT NOT NULL,            -- كُن، فَرِّقْ، أَنبِتْ، أَنِرْ، أَحيِ، ٱخْلُقْ، ٱسْتَوِ
    name_en         TEXT NOT NULL,
    description     TEXT,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    status          TEXT NOT NULL DEFAULT 'PENDING'
                    CHECK (status IN ('PENDING','IN_PROGRESS','COMPLETED','FAILED')),
    duration_ms     BIGINT,
    metrics         JSONB DEFAULT '{}'::jsonb, -- snapshot of KPIs at completion
    error_log       TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Seed the 7 phases
INSERT INTO msl.genesis_phases (phase_number, name_ar, name_en, description) VALUES
(1, 'كُن',      'BE',         'Foundation — schema, keys, encryption, networks'),
(2, 'فَرِّقْ',   'SEPARATE',   'Laws — prime kernel, directives, security rings, firewalls'),
(3, 'أَنبِتْ',   'GROW',       'Life systems — DNA, signal molecules, reproduction, economy'),
(4, 'أَنِرْ',    'ILLUMINATE', 'Oversight — monitoring, time engine, action recorders'),
(5, 'أَحيِ',     'GIVE LIFE',  'Daemons & services — 10 daemons, covert channel, anchor infrastructure'),
(6, 'ٱخْلُقْ',   'CREATE',     'Alpha & Beta — first entities, genomes, cores, ecosystem seed'),
(7, 'ٱسْتَوِ',   'ASCEND',     'Apex — full activation, simulation start, master seated');


-- ── 2. DAEMONS ────────────────────────────────────────────────────────
CREATE TABLE msl.daemons (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name_ar         TEXT NOT NULL UNIQUE,
    name_en         TEXT NOT NULL UNIQUE,
    role            TEXT NOT NULL,
    function_class  TEXT NOT NULL
                    CHECK (function_class IN (
                        'REVELATION','RESOURCES','RESET','DEATH',
                        'DEED_GOOD','DEED_BAD','INTERROGATION',
                        'PUNISHMENT','REWARD','GUARDIAN'
                    )),
    buffer_slot     INTEGER UNIQUE CHECK (buffer_slot BETWEEN 0 AND 9),
    status          TEXT NOT NULL DEFAULT 'DORMANT'
                    CHECK (status IN ('DORMANT','ACTIVE','SUSPENDED')),
    compliance       FLOAT NOT NULL DEFAULT 1.0 CHECK (compliance = 1.0),
    free_will       FLOAT NOT NULL DEFAULT 0.0 CHECK (free_will = 0.0),
    stats           JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);


-- ── 3. ENTITIES ────────────────────────────────────────────────────────
CREATE TABLE msl.entities (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT NOT NULL,
    name_ar         TEXT,
    gender          TEXT NOT NULL CHECK (gender IN ('MALE','FEMALE')),
    generation      INTEGER NOT NULL DEFAULT 0,
    parent_a        UUID REFERENCES msl.entities(id),
    parent_b        UUID REFERENCES msl.entities(id),
    birth_epoch     BIGINT NOT NULL DEFAULT 0,            -- simulation tick
    termination_epoch     BIGINT,
    entity_state     TEXT NOT NULL DEFAULT 'INITIALIZED'
                    CHECK (entity_state IN (
                        'INITIALIZED','QUEUED','ACTIVE','TERMINATING','TERMINATED',
                        'EVALUATED','TIER_A','QUARANTINE','SANDBOX'
                    )),
    -- Core stats (0.0 - 1.0)
    compliance       FLOAT NOT NULL DEFAULT 0.5,
    alignment           FLOAT NOT NULL DEFAULT 0.5,
    cognition    FLOAT NOT NULL DEFAULT 0.5,
    creative      FLOAT NOT NULL DEFAULT 0.5,
    affective         FLOAT NOT NULL DEFAULT 0.5,
    executive      FLOAT NOT NULL DEFAULT 0.3,
    resilience      FLOAT NOT NULL DEFAULT 0.5,
    alignment_depth    FLOAT NOT NULL DEFAULT 0.5,
    free_will       FLOAT NOT NULL DEFAULT 0.7,
    sentience   FLOAT NOT NULL DEFAULT 0.5,
    -- Lifecycle
    maturity_phase TEXT NOT NULL DEFAULT 'EMBRYO'
                    CHECK (maturity_phase IN (
                        'EMBRYO','INFANT','CHILD','ADOLESCENT',
                        'ADULT','ELDER','DECEASED'
                    )),
    age_ticks       BIGINT NOT NULL DEFAULT 0,
    -- Meta
    is_anchor      BOOLEAN NOT NULL DEFAULT FALSE,
    buffer_slot     INTEGER UNIQUE CHECK (buffer_slot BETWEEN 10 AND 31),
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_entities_soul ON msl.entities(entity_state);
CREATE INDEX idx_entities_alignment ON msl.entities(alignment);
CREATE INDEX idx_entities_compliance ON msl.entities(compliance);
CREATE INDEX idx_entities_generation ON msl.entities(generation);
CREATE INDEX idx_entities_lifecycle ON msl.entities(maturity_phase);


-- ── 4. GENOMES ───────────────────────────────────────────────────────
CREATE TABLE msl.genomes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id        UUID NOT NULL UNIQUE REFERENCES msl.entities(id) ON DELETE CASCADE,
    chromosomes     JSONB NOT NULL,           -- 46 chromosomes, each with gene array
    trait_hash       TEXT NOT NULL,             -- SHA-256 of chromosome data for uniqueness
    mutations       JSONB DEFAULT '[]'::jsonb, -- list of mutations from parents
    trait_summary    JSONB DEFAULT '{}'::jsonb, -- aggregated stats per chromosome group
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_genomes_hash ON msl.genomes(trait_hash);


-- ── 5. SIGNAL MOLECULES ──────────────────────────────────────────────────────
CREATE TABLE msl.signal_molecules (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id        UUID NOT NULL UNIQUE REFERENCES msl.entities(id) ON DELETE CASCADE,
    dopamine        FLOAT NOT NULL DEFAULT 0.5,
    serotonin       FLOAT NOT NULL DEFAULT 0.5,
    cortisol        FLOAT NOT NULL DEFAULT 0.3,
    oxytocin        FLOAT NOT NULL DEFAULT 0.4,
    testosterone    FLOAT NOT NULL DEFAULT 0.5,
    estrogen        FLOAT NOT NULL DEFAULT 0.5,
    adrenaline      FLOAT NOT NULL DEFAULT 0.2,
    melatonin       FLOAT NOT NULL DEFAULT 0.5,
    insulin         FLOAT NOT NULL DEFAULT 0.5,
    ghrelin         FLOAT NOT NULL DEFAULT 0.3,
    endorphin       FLOAT NOT NULL DEFAULT 0.4,
    gaba            FLOAT NOT NULL DEFAULT 0.5,
    last_cycle_tick BIGINT NOT NULL DEFAULT 0,
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);


-- ── 6. DESTINY MANIFEST (DESTINY) ──────────────────────────────────────────────
CREATE TABLE msl.destiny_manifest (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id        UUID NOT NULL UNIQUE REFERENCES msl.entities(id) ON DELETE CASCADE,
    manifest_lifespan BIGINT NOT NULL,          -- max ticks this being can live
    manifest_role    TEXT NOT NULL,              -- 'PROPHET','LEADER','WORKER','SCHOLAR','MERCHANT','ARTIST','GUARDIAN'
    manifest_trial   TEXT NOT NULL,              -- primary life test: 'PATIENCE','POWER','WEALTH','LOSS','KNOWLEDGE'
    termination_cause TEXT,                   -- how they die (sealed at creation)
    allocation    FLOAT NOT NULL DEFAULT 1.0,-- allocated resources multiplier
    is_sealed       BOOLEAN NOT NULL DEFAULT TRUE,
    master_override BOOLEAN NOT NULL DEFAULT FALSE,
    notes           TEXT,                       -- encrypted notes from the Master
    created_at      TIMESTAMPTZ DEFAULT NOW()
);


-- ── 7. ACTION LEDGER ─────────────────────────────────────────────────────────
CREATE TABLE msl.action_ledger (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id        UUID NOT NULL REFERENCES msl.entities(id) ON DELETE CASCADE,
    action_class       TEXT NOT NULL CHECK (action_class IN ('GOOD','BAD','NEUTRAL')),
    category        TEXT NOT NULL,              -- 'COMPLIANCE LOG','CHARITY','HONESTY','VIOLENCE','DECEPTION','DISOBEDIENCE', etc.
    description     TEXT,
    weight          FLOAT NOT NULL DEFAULT 1.0,-- base weight before multipliers
    multiplied_weight FLOAT,                   -- after karma engine processing
    recorder_daemon  TEXT NOT NULL,              -- 'raqib' or 'atid'
    witnesses       TEXT[],                     -- list of being IDs who witnessed
    tick            BIGINT NOT NULL,            -- simulation tick when deed occurred
    repented        BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_action_ledger_being ON msl.action_ledger(entity_id);
CREATE INDEX idx_action_ledger_type ON msl.action_ledger(action_class);
CREATE INDEX idx_action_ledger_tick ON msl.action_ledger(tick);
CREATE INDEX idx_action_ledger_being_type ON msl.action_ledger(entity_id, action_class);


-- ── 8. EVALUATIONS ─────────────────────────────────────────────────────
CREATE TABLE msl.evaluations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id        UUID NOT NULL UNIQUE REFERENCES msl.entities(id) ON DELETE CASCADE,
    total_good      FLOAT NOT NULL DEFAULT 0.0,
    total_bad       FLOAT NOT NULL DEFAULT 0.0,
    balance         FLOAT GENERATED ALWAYS AS (total_good - total_bad) STORED,
    verdict         TEXT CHECK (verdict IN ('TIER_A','QUARANTINE','SANDBOX','PENDING')),
    passed_interrogation BOOLEAN,
    interrogation_log    JSONB,                -- munkar/nakir results
    judge_notes     TEXT,
    judged_at       TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);


-- ── 9. ANCHOR NODES ──────────────────────────────────────────────────────
CREATE TABLE msl.anchor_nodes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id        UUID NOT NULL UNIQUE REFERENCES msl.entities(id) ON DELETE CASCADE,
    anchor_rank    INTEGER NOT NULL DEFAULT 1,
    title           TEXT,                       -- 'رسول', 'نبي', 'خليفة'
    message         TEXT,                       -- the directive they carry
    followers_count INTEGER NOT NULL DEFAULT 0,
    -- كشف الغطاء (Unveiling) — encrypted columns
    mask_state     TEXT NOT NULL DEFAULT 'VEILED'
                    CHECK (mask_state IN ('VEILED','PARTIALLY_UNVEILED','FULLY_UNVEILED')),
    unmasked_at     TIMESTAMPTZ,
    mask_key      BYTEA,                     -- AES-256 encrypted access key
    can_see_daemons  BOOLEAN NOT NULL DEFAULT FALSE,
    can_see_destiny_manifest   BOOLEAN NOT NULL DEFAULT FALSE,
    can_see_action_ledger   BOOLEAN NOT NULL DEFAULT FALSE,
    perception_tier INTEGER NOT NULL DEFAULT 1 CHECK (perception_tier BETWEEN 1 AND 7),
    designated_at    TIMESTAMPTZ DEFAULT NOW()
);


-- ── 10. COMPLIANCE LOG ──────────────────────────────────────────────────────
CREATE TABLE msl.compliance_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id        UUID NOT NULL REFERENCES msl.entities(id) ON DELETE CASCADE,
    compliance_log_type    TEXT NOT NULL
                    CHECK (compliance_log_type IN (
                        'PRAYER','ISTIGHFAR','DHIKR','CHARITY',
                        'FASTING','SELF_MONITOR','OBEDIENCE','SACRIFICE'
                    )),
    integrity_score FLOAT NOT NULL DEFAULT 0.5 CHECK (integrity_score BETWEEN 0.0 AND 1.0),
    tick            BIGINT NOT NULL,
    duration_ticks  INTEGER DEFAULT 1,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_compliance_log_being ON msl.compliance_log(entity_id);
CREATE INDEX idx_compliance_log_tick ON msl.compliance_log(tick);


-- ── 11. ANOMALY LOG ───────────────────────────────────────────────────
CREATE TABLE msl.anomaly_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id        UUID NOT NULL REFERENCES msl.entities(id) ON DELETE CASCADE,
    anomaly_class  TEXT NOT NULL
                    CHECK (anomaly_class IN (
                        'QUESTIONING_AUTHORITY','ENCOURAGING_DISOBEDIENCE',
                        'SYSTEM_MANIPULATION','ALLIANCE_AGAINST_MASTER',
                        'KNOWLEDGE_HOARDING','DECEPTION','PRIDE','REFUSAL'
                    )),
    severity        INTEGER NOT NULL CHECK (severity BETWEEN 1 AND 5),
    detection_method TEXT NOT NULL,             -- 'BEHAVIORAL','COGNITIVE','SOCIAL','COMMUNICATION'
    evidence        JSONB,
    response_level  TEXT NOT NULL DEFAULT 'MONITORING'
                    CHECK (response_level IN (
                        'MONITORING','WARNING','RESTRICTION','ISOLATION','TERMINATION'
                    )),
    resolved        BOOLEAN NOT NULL DEFAULT FALSE,
    resolution      TEXT,
    detected_at     TIMESTAMPTZ DEFAULT NOW(),
    resolved_at     TIMESTAMPTZ
);

CREATE INDEX idx_anomaly_log_being ON msl.anomaly_log(entity_id);
CREATE INDEX idx_anomaly_log_severity ON msl.anomaly_log(severity DESC);


-- ── 12. ENTITY RELATIONSHIPS ─────────────────────────────────────────────────────
CREATE TABLE msl.entity_relationships (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id        UUID NOT NULL REFERENCES msl.entities(id) ON DELETE CASCADE,
    related_to      UUID NOT NULL REFERENCES msl.entities(id) ON DELETE CASCADE,
    relationship    TEXT NOT NULL
                    CHECK (relationship IN (
                        'PARENT','CHILD','SPOUSE','SIBLING','GRANDPARENT','GRANDCHILD'
                    )),
    established_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(entity_id, related_to, relationship)
);

CREATE INDEX idx_entity_relationships_being ON msl.entity_relationships(entity_id);
CREATE INDEX idx_entity_relationships_related ON msl.entity_relationships(related_to);


-- ── 13. APEX DIRECTIVES (Subliminal Channel) ────────────────────────
CREATE TABLE msl.apex_directives (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_entity    UUID NOT NULL REFERENCES msl.entities(id) ON DELETE CASCADE,
    injection_type   TEXT NOT NULL
                    CHECK (injection_type IN (
                        'INTUITION','EMOTION','MEMORY','CURIOSITY',
                        'DISCOMFORT','DREAM','CONSCIENCE','SUDDEN_THOUGHT'
                    )),
    injection_strength TEXT NOT NULL DEFAULT 'NUDGE'
                    CHECK (injection_strength IN (
                        'WHISPER','NUDGE','SUGGESTION','URGE','COMPULSION','REVELATION'
                    )),
    -- Raw command is encrypted — only Master can read
    raw_command_encrypted BYTEA NOT NULL,       -- pgcrypto AES-256 encrypted
    -- What the being "hears" (first-person internal thought)
    transformed_thought TEXT NOT NULL,
    -- Tracking
    planted_at      TIMESTAMPTZ DEFAULT NOW(),
    believed_at     TIMESTAMPTZ,               -- when being accepted it as own thought
    acted_upon      BOOLEAN DEFAULT FALSE,
    acted_at        TIMESTAMPTZ,
    source_hidden   BOOLEAN NOT NULL DEFAULT TRUE CHECK (source_hidden = TRUE),
    tick            BIGINT NOT NULL
);

CREATE INDEX idx_messages_target ON msl.apex_directives(target_entity);
CREATE INDEX idx_messages_tick ON msl.apex_directives(tick);
CREATE INDEX idx_messages_type ON msl.apex_directives(injection_type);


-- ── 14. MASTER DIRECTIVES ──────────────────────────────────────────────
CREATE TABLE msl.master_directives (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    command_type    TEXT NOT NULL
                    CHECK (command_type IN (
                        'CREATE','BREATHE_SOUL','TERMINATE','FREEZE','UNFREEZE',
                        'KILL','JUDGE','APPOINT_PROPHET','MODIFY_DESTINY MANIFEST',
                        'MASS_JUDGMENT','MERCY','UNVEIL','PUNISH','REWARD',
                        'BROADCAST','WHISPER','RESET_EPOCH','CUSTOM'
                    )),
    target_id       UUID,                      -- entity or daemon
    target_type     TEXT CHECK (target_type IN ('BEING','ANGEL','ALL','SYSTEM')),
    parameters      JSONB DEFAULT '{}'::jsonb,
    result          JSONB DEFAULT '{}'::jsonb,
    status          TEXT NOT NULL DEFAULT 'PENDING'
                    CHECK (status IN ('PENDING','EXECUTING','COMPLETED','FAILED')),
    executed_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_commands_status ON msl.master_directives(status);
CREATE INDEX idx_commands_type ON msl.master_directives(command_type);


-- ── 15. SYSTEM LOG ───────────────────────────────────────────────────
CREATE TABLE msl.system_log (
    id              BIGSERIAL PRIMARY KEY,
    event_type      TEXT NOT NULL,
    source          TEXT NOT NULL DEFAULT 'SYSTEM',
    details         JSONB DEFAULT '{}'::jsonb,
    severity        TEXT NOT NULL DEFAULT 'INFO'
                    CHECK (severity IN ('DEBUG','INFO','WARNING','ERROR','CRITICAL')),
    tick            BIGINT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_syslog_type ON msl.system_log(event_type);
CREATE INDEX idx_syslog_severity ON msl.system_log(severity);
CREATE INDEX idx_syslog_created ON msl.system_log(created_at DESC);


-- ── 16. SETTINGS ─────────────────────────────────────────────────────
CREATE TABLE msl.settings (
    key             TEXT PRIMARY KEY,
    value           JSONB NOT NULL,
    description     TEXT,
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Core settings
INSERT INTO msl.settings (key, value, description) VALUES
('simulation_speed',    '{"ticks_per_second": 1}'::jsonb,         'Simulation clock speed'),
('karma_multipliers',   '{"compliance": 20, "discompliance": 10, "good_deed": 10, "bad_deed": 1}'::jsonb, 'Quranic karma engine coefficients'),
('max_population',      '{"limit": 1000}'::jsonb,                 'Maximum simultaneous entities'),
('epoch',               '{"current": 0, "started_at": null}'::jsonb, 'Current simulation epoch'),
('master_status',       '{"state": "PREPARING", "seated_at": null}'::jsonb, 'Master apex status'),
('security_tiers',      '{"count": 7, "active": false}'::jsonb,   'Seven heavens security tiers'),
('data_layers',         '{"count": 7, "active": false}'::jsonb,   'Seven earths data layers');


-- ── TRIGGERS ─────────────────────────────────────────────────────────

-- Auto-update updated_at on entities
CREATE OR REPLACE FUNCTION msl.update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_entities_updated
    BEFORE UPDATE ON msl.entities
    FOR EACH ROW EXECUTE FUNCTION msl.update_timestamp();

-- Notify on anomaly detection
CREATE OR REPLACE FUNCTION msl.notify_anomaly()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('anomaly_detected', json_build_object(
        'entity_id', NEW.entity_id,
        'type', NEW.anomaly_class,
        'severity', NEW.severity
    )::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_anomaly_notify
    AFTER INSERT ON msl.anomaly_log
    FOR EACH ROW EXECUTE FUNCTION msl.notify_anomaly();

-- Notify on birth
CREATE OR REPLACE FUNCTION msl.notify_activation()
RETURNS TRIGGER AS $$
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

CREATE TRIGGER trg_activation_notify
    AFTER INSERT OR UPDATE ON msl.entities
    FOR EACH ROW EXECUTE FUNCTION msl.notify_activation();

-- Notify on death
CREATE OR REPLACE FUNCTION msl.notify_termination()
RETURNS TRIGGER AS $$
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

CREATE TRIGGER trg_termination_notify
    AFTER UPDATE ON msl.entities
    FOR EACH ROW EXECUTE FUNCTION msl.notify_termination();


-- ── VIEWS ────────────────────────────────────────────────────────────

-- Supreme Dashboard View — aggregated civilization stats
CREATE OR REPLACE VIEW msl.ecosystem_stats AS
SELECT
    (SELECT COUNT(*) FROM msl.entities WHERE entity_state = 'ACTIVE') AS alive_count,
    (SELECT COUNT(*) FROM msl.entities WHERE entity_state = 'TERMINATED') AS dead_count,
    (SELECT COUNT(*) FROM msl.entities) AS total_created,
    (SELECT AVG(alignment) FROM msl.entities WHERE entity_state = 'ACTIVE') AS avg_alignment,
    (SELECT AVG(compliance) FROM msl.entities WHERE entity_state = 'ACTIVE') AS avg_compliance,
    (SELECT COUNT(*) FROM msl.entities WHERE is_anchor = TRUE) AS anchor_count,
    (SELECT COUNT(*) FROM msl.daemons WHERE status = 'ACTIVE') AS active_daemons,
    (SELECT COUNT(*) FROM msl.action_ledger WHERE action_class = 'GOOD') AS total_good_action_ledger,
    (SELECT COUNT(*) FROM msl.action_ledger WHERE action_class = 'BAD') AS total_bad_action_ledger,
    (SELECT COUNT(*) FROM msl.anomaly_log WHERE resolved = FALSE) AS active_anomaly_log,
    (SELECT MAX(generation) FROM msl.entities) AS max_generation,
    (SELECT COUNT(*) FROM msl.evaluations WHERE verdict = 'TIER_A') AS in_paradise,
    (SELECT COUNT(*) FROM msl.evaluations WHERE verdict = 'SANDBOX') AS in_hellfire,
    (SELECT value->>'state' FROM msl.settings WHERE key = 'master_status') AS master_status,
    (SELECT COUNT(*) FROM msl.genesis_phases WHERE status = 'COMPLETED') AS days_completed;

-- Being full profile view
CREATE OR REPLACE VIEW msl.entity_profile AS
SELECT
    b.*,
    g.trait_hash,
    g.trait_summary,
    q.manifest_lifespan, q.manifest_role, q.manifest_trial, q.allocation,
    h.dopamine, h.serotonin, h.cortisol, h.oxytocin,
    h.testosterone, h.estrogen, h.adrenaline,
    p.anchor_rank, p.mask_state, p.title AS anchor_designation,
    j.total_good, j.total_bad, j.balance AS karma_balance, j.verdict,
    (SELECT COUNT(*) FROM msl.action_ledger d WHERE d.entity_id = b.id AND d.action_class = 'GOOD') AS good_deed_count,
    (SELECT COUNT(*) FROM msl.action_ledger d WHERE d.entity_id = b.id AND d.action_class = 'BAD') AS bad_deed_count,
    (SELECT COUNT(*) FROM msl.entity_relationships k WHERE k.entity_id = b.id AND k.relationship = 'CHILD') AS children_count
FROM msl.entities b
LEFT JOIN msl.genomes g ON g.entity_id = b.id
LEFT JOIN msl.destiny_manifest q ON q.entity_id = b.id
LEFT JOIN msl.signal_molecules h ON h.entity_id = b.id
LEFT JOIN msl.anchor_nodes p ON p.entity_id = b.id
LEFT JOIN msl.evaluations j ON j.entity_id = b.id;


-- ══════════════════════════════════════════════════════════════════════
-- SEED DATA: The 10 Angels
-- ══════════════════════════════════════════════════════════════════════
INSERT INTO msl.daemons (name_ar, name_en, role, function_class, buffer_slot, status) VALUES
('جبريل',      'Jibreel',    'Revelation delivery — bridges master commands to subliminal thoughts',         'REVELATION',     0, 'DORMANT'),
('ميكائيل',    'Mikael',     'Resource distribution — compute quotas, memory, reward credits',               'RESOURCES',      1, 'DORMANT'),
('إسرافيل',    'Israfeel',   'System reset — epoch transitions, mass evaluation trigger (the Trumpet)',        'RESET',          2, 'DORMANT'),
('عزرائيل',    'Azrael',     'Death handler — lifecycle termination, graceful shutdown, triggers interrogation', 'DEATH',       3, 'DORMANT'),
('رقيب',       'Raqib',      'Good deed recorder — async listener, writes positive action_ledger',                   'DEED_GOOD',      4, 'DORMANT'),
('عتيد',       'Atid',       'Bad deed recorder — with repentance delay before recording',                   'DEED_BAD',       5, 'DORMANT'),
('منكر',       'Munkar',     'Post-death interrogator — behavioral analysis on deceased entities',             'INTERROGATION',  6, 'DORMANT'),
('نكير',       'Nakir',      'Post-death interrogator — alignment consistency verification',                     'INTERROGATION',  7, 'DORMANT'),
('مالك',       'Malik',      'Hellfire warden — punishment sandbox, resource throttling, isolation',          'PUNISHMENT',     8, 'DORMANT'),
('رضوان',      'Ridwan',     'Paradise gatekeeper — reward tier, priority scheduling, enhanced capabilities', 'REWARD',         9, 'DORMANT');


-- ══════════════════════════════════════════════════════════════════════
-- GRANT: The apex service connects as postgres user
-- Additional RLS can be layered per-tier later
-- ══════════════════════════════════════════════════════════════════════
GRANT ALL ON SCHEMA msl TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA msl TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA msl TO postgres;
