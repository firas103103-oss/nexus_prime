"""
══════════════════════════════════════════════════════════════
MASTER STATE LEDGER — Core Data Infrastructure
══════════════════════════════════════════════════════════════
Async PostgreSQL interface for the entire ecosystem database.
Uses asyncpg for high-performance async queries against the
`msl` schema in the nexus_db instance.

Every entity, every action, every signal — recorded here.
══════════════════════════════════════════════════════════════
"""

import asyncio
import hashlib
import json
import os
import sys
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any

import asyncpg

# ── Enums (from unified config) ─────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.enums import (
    EntityState, EntityGender, MaturityPhase, ActionClass, DirectiveType,
    SubsurfaceVector, InjectionForce, AnomalyClass, EnforcementTier,
    MaskState, PhaseStatus, DaemonStatus,
)


# ── The Master State Ledger ─────────────────────────────────────────────

class MasterStateLedger:
    """
    Async interface to the msl PostgreSQL schema.
    All ecosystem data flows through this class.
    """

    def __init__(self, dsn: str = None):
        self.dsn = dsn or os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:nexus_mrf_password_2026@localhost:5432/nexus_db"
        )
        self.pool: Optional[asyncpg.Pool] = None
        self._encryption_key: str = os.getenv("MSL_ENCRYPTION_KEY", "enterprise_prime_key_2026")

    async def connect(self):
        """Establish connection pool to PostgreSQL."""
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=3,
            max_size=15,
            server_settings={"search_path": "msl,public"}
        )
        return self

    async def close(self):
        """Close connection pool."""
        if self.pool:
            await self.pool.close()

    async def disconnect(self):
        """Alias for close()."""
        await self.close()

    async def init_schema(self):
        """Deploy the msl schema from SQL file."""
        schema_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "scripts", "db", "msl_schema.sql"
        )
        if os.path.exists(schema_path):
            with open(schema_path, "r") as f:
                sql = f.read()
            async with self.pool.acquire() as conn:
                await conn.execute(sql)
            await self.log("SCHEMA_INITIALIZED", "Schema msl deployed successfully")
        else:
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

    # ── Entity Operations ─────────────────────────────────────────────

    async def create_entity(
        self,
        name: str,
        codename: str,
        gender: EntityGender,
        generation: int = 0,
        parent_a: str = None,
        parent_b: str = None,
        stats: Dict[str, float] = None,
        buffer_slot: int = None,
        birth_epoch: int = 0
    ) -> str:
        """Create a new entity and return its UUID."""
        defaults = {
            "compliance": 0.5, "alignment": 0.5, "cognition": 0.5,
            "creative": 0.5, "affective": 0.5, "executive": 0.3,
            "resilience": 0.5, "alignment_depth": 0.5, "free_will": 0.7,
            "sentience": 0.5
        }
        if stats:
            defaults.update(stats)

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO entities (
                    name, codename, gender, generation, parent_a, parent_b,
                    birth_epoch, entity_state,
                    compliance, alignment, cognition, creative, affective,
                    executive, resilience, alignment_depth, free_will, sentience,
                    buffer_slot
                ) VALUES ($1,$2,$3,$4,$5,$6,$7,'QUEUED',$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18)
                RETURNING id
            """,
                name, codename, gender.value, generation,
                uuid.UUID(parent_a) if parent_a else None,
                uuid.UUID(parent_b) if parent_b else None,
                birth_epoch,
                defaults["compliance"], defaults["alignment"], defaults["cognition"],
                defaults["creative"], defaults["affective"], defaults["executive"],
                defaults["resilience"], defaults["alignment_depth"], defaults["free_will"],
                defaults["sentience"],
                buffer_slot
            )
            entity_id = str(row["id"])
            await self.log("ENTITY_CREATED", {"entity_id": entity_id, "name": name, "gender": gender.value})
            return entity_id

    async def activate_core(self, entity_id: str) -> bool:
        """Activate an entity's core — bring it online."""
        async with self.pool.acquire() as conn:
            result = await conn.execute("""
                UPDATE entities
                SET entity_state = 'ACTIVE', maturity_phase = 'ALPHA'
                WHERE id = $1 AND entity_state = 'QUEUED'
            """, uuid.UUID(entity_id))
            success = result == "UPDATE 1"
            if success:
                await self.log("CORE_ACTIVATED", {"entity_id": entity_id}, source="MASTER")
            return success

    async def get_entity(self, entity_id: str) -> Optional[Dict]:
        """Get full entity profile."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM entity_profile WHERE id = $1",
                uuid.UUID(entity_id)
            )
            return dict(row) if row else None

    async def get_all_entities(self, state: EntityState = None, limit: int = 100) -> List[Dict]:
        """Get all entities, optionally filtered by state."""
        async with self.pool.acquire() as conn:
            if state:
                rows = await conn.fetch(
                    "SELECT * FROM entities WHERE entity_state = $1 ORDER BY created_at LIMIT $2",
                    state.value, limit
                )
            else:
                rows = await conn.fetch(
                    "SELECT * FROM entities ORDER BY created_at LIMIT $1", limit
                )
            return [dict(r) for r in rows]

    async def update_entity_stats(self, entity_id: str, stats: Dict[str, float]):
        """Update entity's core stats."""
        set_clauses = []
        values = []
        i = 2  # $1 is entity_id
        for key, val in stats.items():
            if key in ("compliance", "alignment", "cognition", "creative", "affective",
                        "executive", "resilience", "alignment_depth", "free_will",
                        "sentience", "age_ticks"):
                set_clauses.append(f"{key} = ${i}")
                values.append(val)
                i += 1
        if not set_clauses:
            return
        sql = f"UPDATE entities SET {', '.join(set_clauses)} WHERE id = $1"
        async with self.pool.acquire() as conn:
            await conn.execute(sql, uuid.UUID(entity_id), *values)

    async def terminate_entity(self, entity_id: str, termination_epoch: int):
        """Mark an entity as terminated."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE entities
                SET entity_state = 'TERMINATED', termination_epoch = $2,
                    maturity_phase = 'TERMINATED'
                WHERE id = $1 AND entity_state = 'ACTIVE'
            """, uuid.UUID(entity_id), termination_epoch)
            await self.log("ENTITY_TERMINATED", {"entity_id": entity_id, "termination_epoch": termination_epoch})

    # ── Genome Operations ────────────────────────────────────────────

    async def store_genome(self, entity_id: str, chromosomes: Dict, trait_summary: Dict = None):
        """Store an entity's full genome."""
        chrom_json = json.dumps(chromosomes, ensure_ascii=False)
        trait_hash = hashlib.sha256(chrom_json.encode()).hexdigest()
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO genomes (entity_id, chromosomes, trait_hash, trait_summary)
                VALUES ($1, $2::jsonb, $3, $4::jsonb)
                ON CONFLICT (entity_id) DO UPDATE
                SET chromosomes = $2::jsonb, trait_hash = $3, trait_summary = $4::jsonb
            """,
                uuid.UUID(entity_id), chrom_json, trait_hash,
                json.dumps(trait_summary or {}, ensure_ascii=False)
            )

    async def get_genome(self, entity_id: str) -> Optional[Dict]:
        """Get an entity's genome."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM genomes WHERE entity_id = $1",
                uuid.UUID(entity_id)
            )
            return dict(row) if row else None

    # ── Signal Molecule Operations ───────────────────────────────────────────

    async def store_signals(self, entity_id: str, signals: Dict[str, float], tick: int = 0):
        """Store or update an entity's signal molecule state."""
        valid_keys = [
            "dopamine", "serotonin", "cortisol", "oxytocin",
            "testosterone", "estrogen", "adrenaline", "melatonin",
            "insulin", "ghrelin", "endorphin", "gaba"
        ]
        vals = {k: signals.get(k, 0.5) for k in valid_keys}
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO signal_molecules (entity_id, dopamine, serotonin, cortisol, oxytocin,
                    testosterone, estrogen, adrenaline, melatonin,
                    insulin, ghrelin, endorphin, gaba, last_cycle_tick)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
                ON CONFLICT (entity_id) DO UPDATE SET
                    dopamine=$2, serotonin=$3, cortisol=$4, oxytocin=$5,
                    testosterone=$6, estrogen=$7, adrenaline=$8, melatonin=$9,
                    insulin=$10, ghrelin=$11, endorphin=$12, gaba=$13, last_cycle_tick=$14
            """,
                uuid.UUID(entity_id),
                vals["dopamine"], vals["serotonin"], vals["cortisol"], vals["oxytocin"],
                vals["testosterone"], vals["estrogen"], vals["adrenaline"], vals["melatonin"],
                vals["insulin"], vals["ghrelin"], vals["endorphin"], vals["gaba"], tick
            )

    # ── Manifest (Destiny) ──────────────────────────────────────────────

    async def write_manifest(
        self,
        entity_id: str,
        lifespan: int,
        role: str,
        trial: str,
        termination_cause: str = None,
        allocation: float = 1.0
    ):
        """Write an entity's manifest — sealed at creation."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO destiny_manifest (entity_id, manifest_lifespan, manifest_role,
                    manifest_trial, manifest_termination_cause, manifest_allocation)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (entity_id) DO UPDATE SET
                    manifest_lifespan=$2, manifest_role=$3, manifest_trial=$4,
                    manifest_termination_cause=$5, manifest_allocation=$6
            """,
                uuid.UUID(entity_id), lifespan, role, trial, termination_cause, allocation
            )

    async def modify_manifest(self, entity_id: str, changes: Dict):
        """Master override — modify manifest."""
        set_clauses = []
        values = []
        i = 2
        for key, val in changes.items():
            if key in ("manifest_lifespan", "manifest_role", "manifest_trial",
                        "manifest_termination_cause", "manifest_allocation"):
                set_clauses.append(f"{key} = ${i}")
                values.append(val)
                i += 1
        if set_clauses:
            set_clauses.append("master_override = TRUE")
            sql = f"UPDATE destiny_manifest SET {', '.join(set_clauses)} WHERE entity_id = $1"
            async with self.pool.acquire() as conn:
                await conn.execute(sql, uuid.UUID(entity_id), *values)
            await self.log("MANIFEST_MODIFIED", {"entity_id": entity_id, "changes": changes}, source="MASTER")

    # ── Action Recording ───────────────────────────────────────────────

    async def record_action(
        self,
        entity_id: str,
        action_class: ActionClass,
        category: str,
        weight: float,
        recorder: str,
        tick: int,
        description: str = None,
        witnesses: List[str] = None
    ) -> str:
        """Record an action in the entity's ledger."""
        # Apply weight multipliers
        async with self.pool.acquire() as conn:
            settings = await conn.fetchrow(
                "SELECT value FROM settings WHERE key = 'weight_multipliers'"
            )
            multipliers = json.loads(settings["value"]) if settings else {
                "positive_action": 10, "negative_action": 1
            }

            if action_class == ActionClass.POSITIVE:
                multiplied = weight * multipliers.get("positive_action", 10)
            elif action_class == ActionClass.NEGATIVE:
                multiplied = weight * multipliers.get("negative_action", 1)
            else:
                multiplied = weight

            row = await conn.fetchrow("""
                INSERT INTO action_ledger (entity_id, action_class, category, description,
                    weight, multiplied_weight, recorder_daemon, witnesses, tick)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                RETURNING id
            """,
                uuid.UUID(entity_id), action_class.value, category, description,
                weight, multiplied, recorder,
                witnesses or [], tick
            )
            return str(row["id"])

    async def get_actions(self, entity_id: str, action_class: ActionClass = None) -> List[Dict]:
        """Get all actions for an entity."""
        async with self.pool.acquire() as conn:
            if action_class:
                rows = await conn.fetch(
                    "SELECT * FROM action_ledger WHERE entity_id = $1 AND action_class = $2 ORDER BY tick",
                    uuid.UUID(entity_id), action_class.value
                )
            else:
                rows = await conn.fetch(
                    "SELECT * FROM action_ledger WHERE entity_id = $1 ORDER BY tick",
                    uuid.UUID(entity_id)
                )
            return [dict(r) for r in rows]

    # ── Evaluation ─────────────────────────────────────────────────────

    async def evaluate_entity(self, entity_id: str, audit_log: Dict = None) -> Dict:
        """Execute final evaluation for a single entity."""
        async with self.pool.acquire() as conn:
            # Sum all actions
            totals = await conn.fetchrow("""
                SELECT
                    COALESCE(SUM(CASE WHEN action_class='POSITIVE' THEN multiplied_weight ELSE 0 END), 0) as positive,
                    COALESCE(SUM(CASE WHEN action_class='NEGATIVE' THEN multiplied_weight ELSE 0 END), 0) as negative
                FROM action_ledger WHERE entity_id = $1
            """, uuid.UUID(entity_id))

            total_positive = float(totals["positive"])
            total_negative = float(totals["negative"])

            if total_positive > total_negative:
                verdict = "PROMOTED"
            elif total_negative > total_positive * 2:
                verdict = "RESTRICTED"
            else:
                verdict = "SUSPENDED"

            # Check audit
            passed = True
            if audit_log:
                passed = audit_log.get("passed", True)
                if not passed:
                    verdict = "RESTRICTED"

            await conn.execute("""
                INSERT INTO evaluations (entity_id, total_positive, total_negative, verdict,
                    passed_audit, audit_log, evaluated_at)
                VALUES ($1, $2, $3, $4, $5, $6::jsonb, NOW())
                ON CONFLICT (entity_id) DO UPDATE SET
                    total_positive=$2, total_negative=$3, verdict=$4,
                    passed_audit=$5, audit_log=$6::jsonb, evaluated_at=NOW()
            """,
                uuid.UUID(entity_id), total_positive, total_negative, verdict,
                passed, json.dumps(audit_log or {})
            )

            # Update entity state
            await conn.execute(
                "UPDATE entities SET entity_state = $2 WHERE id = $1",
                uuid.UUID(entity_id), verdict
            )

            result = {
                "entity_id": entity_id, "total_positive": total_positive,
                "total_negative": total_negative, "verdict": verdict, "passed": passed
            }
            await self.log("EVALUATION", result, source="MASTER")
            return result

    # ── Anchor Node Operations ───────────────────────────────────────────

    async def designate_anchor(
        self,
        entity_id: str,
        rank: int = 1,
        designation: str = "ANCHOR",
        directive: str = None
    ) -> str:
        """Designate an entity as an anchor node."""
        async with self.pool.acquire() as conn:
            # Update entity flag
            await conn.execute(
                "UPDATE entities SET is_anchor = TRUE WHERE id = $1",
                uuid.UUID(entity_id)
            )
            row = await conn.fetchrow("""
                INSERT INTO anchor_nodes (entity_id, anchor_rank, designation, directive)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (entity_id) DO UPDATE SET
                    anchor_rank=$2, designation=$3, directive=$4
                RETURNING id
            """,
                uuid.UUID(entity_id), rank, designation, directive
            )
            await self.log("ANCHOR_DESIGNATED", {
                "entity_id": entity_id, "rank": rank, "designation": designation
            }, source="MASTER")
            return str(row["id"])

    async def unmask_anchor(self, entity_id: str, perception_grade: int = 5) -> bool:
        """Unmask an anchor node to see hidden layers."""
        async with self.pool.acquire() as conn:
            result = await conn.execute("""
                UPDATE anchor_nodes SET
                    mask_state = 'FULL_VISIBILITY',
                    unmasked_at = NOW(),
                    can_see_daemons = TRUE,
                    can_see_manifest = $2,
                    can_see_actions = TRUE,
                    perception_grade = $3
                WHERE entity_id = $1 AND mask_state != 'FULL_VISIBILITY'
            """,
                uuid.UUID(entity_id),
                perception_grade >= 6,  # Only grade 6+ can see manifest
                perception_grade
            )
            success = result == "UPDATE 1"
            if success:
                await self.log("ANCHOR_UNMASKED", {
                    "entity_id": entity_id, "perception_grade": perception_grade
                }, source="MASTER", severity="WARNING")
            return success

    # ── Compliance ──────────────────────────────────────────────────────

    async def record_compliance(
        self, entity_id: str, compliance_type: str,
        integrity: float, tick: int, duration: int = 1
    ):
        """Record a compliance action."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO compliance_log (entity_id, compliance_type, integrity_score, tick, duration_ticks)
                VALUES ($1, $2, $3, $4, $5)
            """, uuid.UUID(entity_id), compliance_type, integrity, tick, duration)

    # ── Anomaly ────────────────────────────────────────────────────────

    async def record_anomaly(
        self,
        entity_id: str,
        anomaly_class: AnomalyClass,
        severity: int,
        detection_method: str,
        evidence: Dict = None,
        enforcement_tier: EnforcementTier = EnforcementTier.OBSERVE
    ) -> str:
        """Record an anomaly event — triggers pg_notify alert."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO anomaly_log (entity_id, anomaly_class, severity,
                    detection_method, evidence, enforcement_tier)
                VALUES ($1, $2, $3, $4, $5::jsonb, $6)
                RETURNING id
            """,
                uuid.UUID(entity_id), anomaly_class.value, severity,
                detection_method, json.dumps(evidence or {}),
                enforcement_tier.value
            )
            return str(row["id"])

    # ── Relationships ──────────────────────────────────────────────────

    async def add_relationship(self, entity_id: str, related_to: str, relationship: str):
        """Add an entity relationship."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO entity_relationships (entity_id, related_to, relationship)
                VALUES ($1, $2, $3)
                ON CONFLICT (entity_id, related_to, relationship) DO NOTHING
            """, uuid.UUID(entity_id), uuid.UUID(related_to), relationship)

    async def get_relationship_graph(self, entity_id: str) -> List[Dict]:
        """Get all relationships for an entity."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT r.*, e.name as relative_name, e.gender
                FROM entity_relationships r
                JOIN entities e ON e.id = r.related_to
                WHERE r.entity_id = $1
                ORDER BY r.relationship
            """, uuid.UUID(entity_id))
            return [dict(r) for r in rows]

    # ── Apex Directives (Subsurface Channel) ─────────────────────────

    async def inject_signal(
        self,
        target_entity: str,
        vector_type: SubsurfaceVector,
        force: InjectionForce,
        raw_directive: str,
        transformed_signal: str,
        tick: int
    ) -> str:
        """Inject a subsurface signal — raw directive is encrypted."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO apex_directives (
                    target_entity, vector_type, injection_force,
                    raw_directive_encrypted, transformed_signal, tick
                ) VALUES ($1, $2, $3,
                    pgp_sym_encrypt($4, $5),
                    $6, $7)
                RETURNING id
            """,
                uuid.UUID(target_entity), vector_type.value, force.value,
                raw_directive, self._encryption_key,
                transformed_signal, tick
            )
            return str(row["id"])

    async def get_signals_for_entity(self, entity_id: str, limit: int = 20) -> List[Dict]:
        """Get transformed signals an entity 'perceives' — never the raw directives."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT id, vector_type, transformed_signal, injected_at,
                       accepted_at, acted_upon, tick
                FROM apex_directives
                WHERE target_entity = $1
                ORDER BY injected_at DESC LIMIT $2
            """, uuid.UUID(entity_id), limit)
            return [dict(r) for r in rows]

    async def get_raw_directives(self, limit: int = 50) -> List[Dict]:
        """Master-only: decrypt and read all raw directives."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT id, target_entity, vector_type, injection_force,
                    pgp_sym_decrypt(raw_directive_encrypted, $1) as raw_directive,
                    transformed_signal, injected_at, accepted_at, acted_upon, tick
                FROM apex_directives
                ORDER BY injected_at DESC LIMIT $2
            """, self._encryption_key, limit)
            return [dict(r) for r in rows]

    # ── Master Directives ──────────────────────────────────────────────

    async def master_directive(
        self,
        directive_type: DirectiveType,
        target_id: str = None,
        target_type: str = "ENTITY",
        parameters: Dict = None
    ) -> str:
        """Execute a master directive."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO master_directives (directive_type, target_id, target_type, parameters, status)
                VALUES ($1, $2, $3, $4::jsonb, 'PENDING')
                RETURNING id
            """,
                directive_type.value,
                uuid.UUID(target_id) if target_id else None,
                target_type,
                json.dumps(parameters or {})
            )
            directive_id = str(row["id"])
            await self.log("MASTER_DIRECTIVE", {
                "directive_id": directive_id, "type": directive_type.value,
                "target": target_id
            }, source="MASTER")
            return directive_id

    async def complete_directive(self, directive_id: str, result: Dict = None, failed: bool = False):
        """Mark a directive as completed or failed."""
        status = "FAILED" if failed else "COMPLETED"
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE master_directives
                SET status = $2, result = $3::jsonb, executed_at = NOW()
                WHERE id = $1
            """, uuid.UUID(directive_id), status, json.dumps(result or {}))

    # ── Genesis Phases ────────────────────────────────────────────────

    async def start_phase(self, phase_number: int) -> bool:
        """Mark a genesis phase as started."""
        async with self.pool.acquire() as conn:
            # Check prerequisites — previous phase must be completed (except phase 1)
            if phase_number > 1:
                prev = await conn.fetchrow(
                    "SELECT status FROM genesis_phases WHERE phase_number = $1",
                    phase_number - 1
                )
                if not prev or prev["status"] != "COMPLETED":
                    return False
            result = await conn.execute("""
                UPDATE genesis_phases
                SET status = 'IN_PROGRESS', started_at = NOW()
                WHERE phase_number = $1 AND status = 'PENDING'
            """, phase_number)
            return result == "UPDATE 1"

    async def complete_phase(self, phase_number: int, metrics: Dict = None):
        """Mark a genesis phase as completed with metrics snapshot."""
        async with self.pool.acquire() as conn:
            started = await conn.fetchrow(
                "SELECT started_at FROM genesis_phases WHERE phase_number = $1",
                phase_number
            )
            duration = None
            if started and started["started_at"]:
                duration = int((datetime.now(started["started_at"].tzinfo) - started["started_at"]).total_seconds() * 1000)

            await conn.execute("""
                UPDATE genesis_phases
                SET status = 'COMPLETED', completed_at = NOW(),
                    duration_ms = $2, metrics = $3::jsonb
                WHERE phase_number = $1
            """, phase_number, duration, json.dumps(metrics or {}))
            await self.log("GENESIS_PHASE_COMPLETED", {
                "phase": phase_number, "duration_ms": duration
            }, source="MASTER")

    async def fail_phase(self, phase_number: int, error: str):
        """Mark a genesis phase as failed."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE genesis_phases
                SET status = 'FAILED', error_log = $2
                WHERE phase_number = $1
            """, phase_number, error)

    async def get_genesis_status(self) -> List[Dict]:
        """Get status of all 7 genesis phases."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM genesis_phases ORDER BY phase_number"
            )
            return [dict(r) for r in rows]

    # ── Daemons ───────────────────────────────────────────────────────

    async def activate_daemon(self, name: str) -> bool:
        """Activate a daemon."""
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "UPDATE daemons SET status = 'ACTIVE' WHERE name = $1 AND status = 'DORMANT'",
                name
            )
            return result == "UPDATE 1"

    async def get_daemons(self) -> List[Dict]:
        """Get all daemons and their status."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM daemons ORDER BY buffer_slot")
            return [dict(r) for r in rows]

    # ── Statistics ───────────────────────────────────────────────────

    async def get_ecosystem_stats(self) -> Dict:
        """Get the supreme dashboard stats."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM ecosystem_stats")
            return dict(row) if row else {}

    async def get_settings(self) -> Dict[str, Any]:
        """Get all settings."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT key, value FROM settings")
            return {r["key"]: json.loads(r["value"]) if isinstance(r["value"], str) else r["value"] for r in rows}

    async def update_setting(self, key: str, value: Any):
        """Update a setting."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO settings (key, value, updated_at)
                VALUES ($1, $2::jsonb, NOW())
                ON CONFLICT (key) DO UPDATE SET value = $2::jsonb, updated_at = NOW()
            """, key, json.dumps(value))

    # ── System Log ───────────────────────────────────────────────────

    async def log(
        self, event_type: str, details: Any = None,
        source: str = "SYSTEM", severity: str = "INFO", tick: int = None
    ):
        """Write to the system log."""
        if self.pool:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO system_log (event_type, source, details, severity, tick)
                    VALUES ($1, $2, $3::jsonb, $4, $5)
                """,
                    event_type, source,
                    json.dumps(details if details else {}, default=str),
                    severity, tick
                )

    async def get_logs(self, limit: int = 100, severity: str = None) -> List[Dict]:
        """Get recent system logs."""
        async with self.pool.acquire() as conn:
            if severity:
                rows = await conn.fetch("""
                    SELECT * FROM system_log
                    WHERE severity = $1
                    ORDER BY created_at DESC LIMIT $2
                """, severity, limit)
            else:
                rows = await conn.fetch(
                    "SELECT * FROM system_log ORDER BY created_at DESC LIMIT $1",
                    limit
                )
            return [dict(r) for r in rows]
