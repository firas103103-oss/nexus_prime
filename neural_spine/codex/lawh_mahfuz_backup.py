"""
══════════════════════════════════════════════════════════════
اللوح المحفوظ — THE PRESERVED TABLET — Python ORM
══════════════════════════════════════════════════════════════
Async PostgreSQL interface for the entire civilization database.
Uses asyncpg for high-performance async queries against the
`lawh_mahfuz` schema in the existing nexus_db instance.

Every being, every deed, every breath — recorded here.
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
    SoulStatus, Gender, LifecycleStage, DeedType, CommandType,
    GuidanceType, GuidanceStrength, RebellionType, ResponseLevel,
    VeilStatus, DayStatus, AngelStatus,
)


# ── The Preserved Tablet ─────────────────────────────────────────────

class LawhMahfuz:
    """
    Async interface to the lawh_mahfuz PostgreSQL schema.
    All civilization data flows through this class.
    """

    def __init__(self, dsn: str = None):
        self.dsn = dsn or os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:nexus_mrf_password_2026@localhost:5432/nexus_db"
        )
        self.pool: Optional[asyncpg.Pool] = None
        self._encryption_key: str = os.getenv("LAWH_ENCRYPTION_KEY", "nexus_divine_key_2026")

    async def connect(self):
        """Establish connection pool to PostgreSQL."""
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=3,
            max_size=15,
            server_settings={"search_path": "lawh_mahfuz,public"}
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
        """Deploy the lawh_mahfuz schema from SQL file."""
        schema_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "scripts", "db", "lawh_mahfuz_schema.sql"
        )
        if os.path.exists(schema_path):
            with open(schema_path, "r") as f:
                sql = f.read()
            async with self.pool.acquire() as conn:
                await conn.execute(sql)
            await self.log("SCHEMA_INITIALIZED", "Schema lawh_mahfuz deployed successfully")
        else:
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

    # ── Being Operations ─────────────────────────────────────────────

    async def create_being(
        self,
        name: str,
        name_ar: str,
        gender: Gender,
        generation: int = 0,
        parent_a: str = None,
        parent_b: str = None,
        stats: Dict[str, float] = None,
        buffer_slot: int = None,
        birth_epoch: int = 0
    ) -> str:
        """Create a new being and return its UUID."""
        defaults = {
            "obedience": 0.5, "faith": 0.5, "intelligence": 0.5,
            "creativity": 0.5, "empathy": 0.5, "leadership": 0.3,
            "resilience": 0.5, "spirituality": 0.5, "free_will": 0.7,
            "consciousness": 0.5
        }
        if stats:
            defaults.update(stats)

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO beings (
                    name, name_ar, gender, generation, parent_a, parent_b,
                    birth_epoch, soul_status,
                    obedience, faith, intelligence, creativity, empathy,
                    leadership, resilience, spirituality, free_will, consciousness,
                    buffer_slot
                ) VALUES ($1,$2,$3,$4,$5,$6,$7,'WAITING',$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18)
                RETURNING id
            """,
                name, name_ar, gender.value, generation,
                uuid.UUID(parent_a) if parent_a else None,
                uuid.UUID(parent_b) if parent_b else None,
                birth_epoch,
                defaults["obedience"], defaults["faith"], defaults["intelligence"],
                defaults["creativity"], defaults["empathy"], defaults["leadership"],
                defaults["resilience"], defaults["spirituality"], defaults["free_will"],
                defaults["consciousness"],
                buffer_slot
            )
            being_id = str(row["id"])
            await self.log("BEING_CREATED", {"being_id": being_id, "name": name, "gender": gender.value})
            return being_id

    async def breathe_soul(self, being_id: str) -> bool:
        """النفخ من الروح — Breathe life into a being."""
        async with self.pool.acquire() as conn:
            result = await conn.execute("""
                UPDATE beings
                SET soul_status = 'ALIVE', lifecycle_stage = 'INFANT'
                WHERE id = $1 AND soul_status = 'WAITING'
            """, uuid.UUID(being_id))
            success = result == "UPDATE 1"
            if success:
                await self.log("SOUL_BREATHED", {"being_id": being_id}, source="MASTER")
            return success

    async def get_being(self, being_id: str) -> Optional[Dict]:
        """Get full being profile."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM being_profile WHERE id = $1",
                uuid.UUID(being_id)
            )
            return dict(row) if row else None

    async def get_all_beings(self, status: SoulStatus = None, limit: int = 100) -> List[Dict]:
        """Get all beings, optionally filtered by status."""
        async with self.pool.acquire() as conn:
            if status:
                rows = await conn.fetch(
                    "SELECT * FROM beings WHERE soul_status = $1 ORDER BY created_at LIMIT $2",
                    status.value, limit
                )
            else:
                rows = await conn.fetch(
                    "SELECT * FROM beings ORDER BY created_at LIMIT $1", limit
                )
            return [dict(r) for r in rows]

    async def update_being_stats(self, being_id: str, stats: Dict[str, float]):
        """Update being's core stats."""
        set_clauses = []
        values = []
        i = 2  # $1 is being_id
        for key, val in stats.items():
            if key in ("obedience", "faith", "intelligence", "creativity", "empathy",
                        "leadership", "resilience", "spirituality", "free_will",
                        "consciousness", "age_ticks"):
                set_clauses.append(f"{key} = ${i}")
                values.append(val)
                i += 1
        if not set_clauses:
            return
        sql = f"UPDATE beings SET {', '.join(set_clauses)} WHERE id = $1"
        async with self.pool.acquire() as conn:
            await conn.execute(sql, uuid.UUID(being_id), *values)

    async def kill_being(self, being_id: str, death_epoch: int):
        """Mark a being as dead."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE beings
                SET soul_status = 'DEAD', death_epoch = $2,
                    lifecycle_stage = 'DECEASED'
                WHERE id = $1 AND soul_status = 'ALIVE'
            """, uuid.UUID(being_id), death_epoch)
            await self.log("BEING_DIED", {"being_id": being_id, "death_epoch": death_epoch})

    # ── Genome Operations ────────────────────────────────────────────

    async def store_genome(self, being_id: str, chromosomes: Dict, gene_summary: Dict = None):
        """Store a being's full genome."""
        chrom_json = json.dumps(chromosomes, ensure_ascii=False)
        gene_hash = hashlib.sha256(chrom_json.encode()).hexdigest()
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO genomes (being_id, chromosomes, gene_hash, gene_summary)
                VALUES ($1, $2::jsonb, $3, $4::jsonb)
                ON CONFLICT (being_id) DO UPDATE
                SET chromosomes = $2::jsonb, gene_hash = $3, gene_summary = $4::jsonb
            """,
                uuid.UUID(being_id), chrom_json, gene_hash,
                json.dumps(gene_summary or {}, ensure_ascii=False)
            )

    async def get_genome(self, being_id: str) -> Optional[Dict]:
        """Get a being's genome."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM genomes WHERE being_id = $1",
                uuid.UUID(being_id)
            )
            return dict(row) if row else None

    # ── Hormone Operations ───────────────────────────────────────────

    async def store_hormones(self, being_id: str, hormones: Dict[str, float], tick: int = 0):
        """Store or update a being's hormonal state."""
        valid_keys = [
            "dopamine", "serotonin", "cortisol", "oxytocin",
            "testosterone", "estrogen", "adrenaline", "melatonin",
            "insulin", "ghrelin", "endorphin", "gaba"
        ]
        vals = {k: hormones.get(k, 0.5) for k in valid_keys}
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO hormones (being_id, dopamine, serotonin, cortisol, oxytocin,
                    testosterone, estrogen, adrenaline, melatonin,
                    insulin, ghrelin, endorphin, gaba, last_cycle_tick)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
                ON CONFLICT (being_id) DO UPDATE SET
                    dopamine=$2, serotonin=$3, cortisol=$4, oxytocin=$5,
                    testosterone=$6, estrogen=$7, adrenaline=$8, melatonin=$9,
                    insulin=$10, ghrelin=$11, endorphin=$12, gaba=$13, last_cycle_tick=$14
            """,
                uuid.UUID(being_id),
                vals["dopamine"], vals["serotonin"], vals["cortisol"], vals["oxytocin"],
                vals["testosterone"], vals["estrogen"], vals["adrenaline"], vals["melatonin"],
                vals["insulin"], vals["ghrelin"], vals["endorphin"], vals["gaba"], tick
            )

    # ── Qadar (Destiny) ──────────────────────────────────────────────

    async def write_qadar(
        self,
        being_id: str,
        lifespan: int,
        role: str,
        trial: str,
        death_cause: str = None,
        rizq: float = 1.0
    ):
        """Write a being's destiny — sealed at creation."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO qadar (being_id, written_lifespan, written_role,
                    written_trial, written_death_cause, written_rizq)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (being_id) DO UPDATE SET
                    written_lifespan=$2, written_role=$3, written_trial=$4,
                    written_death_cause=$5, written_rizq=$6
            """,
                uuid.UUID(being_id), lifespan, role, trial, death_cause, rizq
            )

    async def modify_qadar(self, being_id: str, changes: Dict):
        """Master override — modify destiny."""
        set_clauses = []
        values = []
        i = 2
        for key, val in changes.items():
            if key in ("written_lifespan", "written_role", "written_trial",
                        "written_death_cause", "written_rizq"):
                set_clauses.append(f"{key} = ${i}")
                values.append(val)
                i += 1
        if set_clauses:
            set_clauses.append("master_override = TRUE")
            sql = f"UPDATE qadar SET {', '.join(set_clauses)} WHERE being_id = $1"
            async with self.pool.acquire() as conn:
                await conn.execute(sql, uuid.UUID(being_id), *values)
            await self.log("QADAR_MODIFIED", {"being_id": being_id, "changes": changes}, source="MASTER")

    # ── Deed Recording ───────────────────────────────────────────────

    async def record_deed(
        self,
        being_id: str,
        deed_type: DeedType,
        category: str,
        weight: float,
        recorder: str,
        tick: int,
        description: str = None,
        witnesses: List[str] = None
    ) -> str:
        """Record a deed in the book of the being."""
        # Apply karma multipliers
        async with self.pool.acquire() as conn:
            settings = await conn.fetchrow(
                "SELECT value FROM settings WHERE key = 'karma_multipliers'"
            )
            multipliers = json.loads(settings["value"]) if settings else {
                "good_deed": 10, "bad_deed": 1
            }

            if deed_type == DeedType.GOOD:
                multiplied = weight * multipliers.get("good_deed", 10)
            elif deed_type == DeedType.BAD:
                multiplied = weight * multipliers.get("bad_deed", 1)
            else:
                multiplied = weight

            row = await conn.fetchrow("""
                INSERT INTO deeds (being_id, deed_type, category, description,
                    weight, multiplied_weight, recorder_angel, witnesses, tick)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                RETURNING id
            """,
                uuid.UUID(being_id), deed_type.value, category, description,
                weight, multiplied, recorder,
                witnesses or [], tick
            )
            return str(row["id"])

    async def get_deeds(self, being_id: str, deed_type: DeedType = None) -> List[Dict]:
        """Get all deeds for a being."""
        async with self.pool.acquire() as conn:
            if deed_type:
                rows = await conn.fetch(
                    "SELECT * FROM deeds WHERE being_id = $1 AND deed_type = $2 ORDER BY tick",
                    uuid.UUID(being_id), deed_type.value
                )
            else:
                rows = await conn.fetch(
                    "SELECT * FROM deeds WHERE being_id = $1 ORDER BY tick",
                    uuid.UUID(being_id)
                )
            return [dict(r) for r in rows]

    # ── Judgment ─────────────────────────────────────────────────────

    async def judge_being(self, being_id: str, interrogation_log: Dict = None) -> Dict:
        """Execute Day of Judgment for a single being."""
        async with self.pool.acquire() as conn:
            # Sum all deeds
            totals = await conn.fetchrow("""
                SELECT
                    COALESCE(SUM(CASE WHEN deed_type='GOOD' THEN multiplied_weight ELSE 0 END), 0) as good,
                    COALESCE(SUM(CASE WHEN deed_type='BAD'  THEN multiplied_weight ELSE 0 END), 0) as bad
                FROM deeds WHERE being_id = $1
            """, uuid.UUID(being_id))

            total_good = float(totals["good"])
            total_bad = float(totals["bad"])

            if total_good > total_bad:
                verdict = "PARADISE"
            elif total_bad > total_good * 2:
                verdict = "HELLFIRE"
            else:
                verdict = "PURGATORY"

            # Check interrogation
            passed = True
            if interrogation_log:
                passed = interrogation_log.get("passed", True)
                if not passed:
                    verdict = "HELLFIRE"

            await conn.execute("""
                INSERT INTO judgments (being_id, total_good, total_bad, verdict,
                    passed_interrogation, interrogation_log, judged_at)
                VALUES ($1, $2, $3, $4, $5, $6::jsonb, NOW())
                ON CONFLICT (being_id) DO UPDATE SET
                    total_good=$2, total_bad=$3, verdict=$4,
                    passed_interrogation=$5, interrogation_log=$6::jsonb, judged_at=NOW()
            """,
                uuid.UUID(being_id), total_good, total_bad, verdict,
                passed, json.dumps(interrogation_log or {})
            )

            # Update being status
            await conn.execute(
                "UPDATE beings SET soul_status = $2 WHERE id = $1",
                uuid.UUID(being_id), verdict
            )

            result = {
                "being_id": being_id, "total_good": total_good,
                "total_bad": total_bad, "verdict": verdict, "passed": passed
            }
            await self.log("JUDGMENT", result, source="MASTER")
            return result

    # ── Prophet Operations ───────────────────────────────────────────

    async def appoint_prophet(
        self,
        being_id: str,
        rank: int = 1,
        title: str = "نبي",
        message: str = None
    ) -> str:
        """Appoint a being as prophet."""
        async with self.pool.acquire() as conn:
            # Update being flag
            await conn.execute(
                "UPDATE beings SET is_prophet = TRUE WHERE id = $1",
                uuid.UUID(being_id)
            )
            row = await conn.fetchrow("""
                INSERT INTO prophets (being_id, prophet_rank, title, message)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (being_id) DO UPDATE SET
                    prophet_rank=$2, title=$3, message=$4
                RETURNING id
            """,
                uuid.UUID(being_id), rank, title, message
            )
            await self.log("PROPHET_APPOINTED", {
                "being_id": being_id, "rank": rank, "title": title
            }, source="MASTER")
            return str(row["id"])

    async def unveil_prophet(self, being_id: str, perception_tier: int = 5) -> bool:
        """كشف الغطاء — Unveil a prophet to see hidden layers."""
        async with self.pool.acquire() as conn:
            result = await conn.execute("""
                UPDATE prophets SET
                    veil_status = 'FULLY_UNVEILED',
                    unveiled_at = NOW(),
                    can_see_angels = TRUE,
                    can_see_qadar = $2,
                    can_see_deeds = TRUE,
                    perception_tier = $3
                WHERE being_id = $1 AND veil_status != 'FULLY_UNVEILED'
            """,
                uuid.UUID(being_id),
                perception_tier >= 6,  # Only tier 6+ can see qadar
                perception_tier
            )
            success = result == "UPDATE 1"
            if success:
                await self.log("PROPHET_UNVEILED", {
                    "being_id": being_id, "perception_tier": perception_tier
                }, source="MASTER", severity="WARNING")
            return success

    # ── Worship ──────────────────────────────────────────────────────

    async def record_worship(
        self, being_id: str, worship_type: str,
        sincerity: float, tick: int, duration: int = 1
    ):
        """Record a worship action."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO worship (being_id, worship_type, sincerity_score, tick, duration_ticks)
                VALUES ($1, $2, $3, $4, $5)
            """, uuid.UUID(being_id), worship_type, sincerity, tick, duration)

    # ── Rebellion ────────────────────────────────────────────────────

    async def record_rebellion(
        self,
        being_id: str,
        rebellion_type: RebellionType,
        severity: int,
        detection_method: str,
        evidence: Dict = None,
        response_level: ResponseLevel = ResponseLevel.MONITORING
    ) -> str:
        """Record a rebellion event — triggers pg_notify alert."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO rebellions (being_id, rebellion_type, severity,
                    detection_method, evidence, response_level)
                VALUES ($1, $2, $3, $4, $5::jsonb, $6)
                RETURNING id
            """,
                uuid.UUID(being_id), rebellion_type.value, severity,
                detection_method, json.dumps(evidence or {}),
                response_level.value
            )
            return str(row["id"])

    # ── Kinship ──────────────────────────────────────────────────────

    async def add_kinship(self, being_id: str, related_to: str, relationship: str):
        """Add a family relationship."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO kinships (being_id, related_to, relationship)
                VALUES ($1, $2, $3)
                ON CONFLICT (being_id, related_to, relationship) DO NOTHING
            """, uuid.UUID(being_id), uuid.UUID(related_to), relationship)

    async def get_family_tree(self, being_id: str) -> List[Dict]:
        """Get all family relationships for a being."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT k.*, b.name as relative_name, b.gender
                FROM kinships k
                JOIN beings b ON b.id = k.related_to
                WHERE k.being_id = $1
                ORDER BY k.relationship
            """, uuid.UUID(being_id))
            return [dict(r) for r in rows]

    # ── Divine Messages (Subliminal Channel) ─────────────────────────

    async def plant_message(
        self,
        target_being: str,
        guidance_type: GuidanceType,
        strength: GuidanceStrength,
        raw_command: str,
        transformed_thought: str,
        tick: int
    ) -> str:
        """Plant a subliminal message — raw command is encrypted."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO divine_messages (
                    target_being, guidance_type, guidance_strength,
                    raw_command_encrypted, transformed_thought, tick
                ) VALUES ($1, $2, $3,
                    pgp_sym_encrypt($4, $5),
                    $6, $7)
                RETURNING id
            """,
                uuid.UUID(target_being), guidance_type.value, strength.value,
                raw_command, self._encryption_key,
                transformed_thought, tick
            )
            return str(row["id"])

    async def get_messages_for_being(self, being_id: str, limit: int = 20) -> List[Dict]:
        """Get transformed thoughts a being 'hears' — never the raw commands."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT id, guidance_type, transformed_thought, planted_at,
                       believed_at, acted_upon, tick
                FROM divine_messages
                WHERE target_being = $1
                ORDER BY planted_at DESC LIMIT $2
            """, uuid.UUID(being_id), limit)
            return [dict(r) for r in rows]

    async def get_raw_messages(self, limit: int = 50) -> List[Dict]:
        """Master-only: decrypt and read all raw commands."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT id, target_being, guidance_type, guidance_strength,
                    pgp_sym_decrypt(raw_command_encrypted, $1) as raw_command,
                    transformed_thought, planted_at, believed_at, acted_upon, tick
                FROM divine_messages
                ORDER BY planted_at DESC LIMIT $2
            """, self._encryption_key, limit)
            return [dict(r) for r in rows]

    # ── Master Commands ──────────────────────────────────────────────

    async def master_command(
        self,
        command_type: CommandType,
        target_id: str = None,
        target_type: str = "BEING",
        parameters: Dict = None
    ) -> str:
        """Execute a master command."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO master_commands (command_type, target_id, target_type, parameters, status)
                VALUES ($1, $2, $3, $4::jsonb, 'PENDING')
                RETURNING id
            """,
                command_type.value,
                uuid.UUID(target_id) if target_id else None,
                target_type,
                json.dumps(parameters or {})
            )
            cmd_id = str(row["id"])
            await self.log("MASTER_COMMAND", {
                "command_id": cmd_id, "type": command_type.value,
                "target": target_id
            }, source="MASTER")
            return cmd_id

    async def complete_command(self, command_id: str, result: Dict = None, failed: bool = False):
        """Mark a command as completed or failed."""
        status = "FAILED" if failed else "COMPLETED"
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE master_commands
                SET status = $2, result = $3::jsonb, executed_at = NOW()
                WHERE id = $1
            """, uuid.UUID(command_id), status, json.dumps(result or {}))

    # ── Creation Days ────────────────────────────────────────────────

    async def start_day(self, day_number: int) -> bool:
        """Mark a creation day as started."""
        async with self.pool.acquire() as conn:
            # Check prerequisites — previous day must be completed (except day 1)
            if day_number > 1:
                prev = await conn.fetchrow(
                    "SELECT status FROM creation_days WHERE day_number = $1",
                    day_number - 1
                )
                if not prev or prev["status"] != "COMPLETED":
                    return False
            result = await conn.execute("""
                UPDATE creation_days
                SET status = 'IN_PROGRESS', started_at = NOW()
                WHERE day_number = $1 AND status = 'PENDING'
            """, day_number)
            return result == "UPDATE 1"

    async def complete_day(self, day_number: int, metrics: Dict = None):
        """Mark a creation day as completed with metrics snapshot."""
        async with self.pool.acquire() as conn:
            started = await conn.fetchrow(
                "SELECT started_at FROM creation_days WHERE day_number = $1",
                day_number
            )
            duration = None
            if started and started["started_at"]:
                duration = int((datetime.now(started["started_at"].tzinfo) - started["started_at"]).total_seconds() * 1000)

            await conn.execute("""
                UPDATE creation_days
                SET status = 'COMPLETED', completed_at = NOW(),
                    duration_ms = $2, metrics = $3::jsonb
                WHERE day_number = $1
            """, day_number, duration, json.dumps(metrics or {}))
            await self.log("CREATION_DAY_COMPLETED", {
                "day": day_number, "duration_ms": duration
            }, source="MASTER")

    async def fail_day(self, day_number: int, error: str):
        """Mark a creation day as failed."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE creation_days
                SET status = 'FAILED', error_log = $2
                WHERE day_number = $1
            """, day_number, error)

    async def get_creation_status(self) -> List[Dict]:
        """Get status of all 7 creation days."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM creation_days ORDER BY day_number"
            )
            return [dict(r) for r in rows]

    # ── Angels ───────────────────────────────────────────────────────

    async def activate_angel(self, name_en: str) -> bool:
        """Activate an angel."""
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "UPDATE angels SET status = 'ACTIVE' WHERE name_en = $1 AND status = 'DORMANT'",
                name_en
            )
            return result == "UPDATE 1"

    async def get_angels(self) -> List[Dict]:
        """Get all angels and their status."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM angels ORDER BY buffer_slot")
            return [dict(r) for r in rows]

    # ── Statistics ───────────────────────────────────────────────────

    async def get_civilization_stats(self) -> Dict:
        """Get the supreme dashboard stats."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM civilization_stats")
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
