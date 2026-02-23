"""
Raqib/Atid Observer — Cosmic Ledger Integration
════════════════════════════════════════════════
Records every Dify-triggered action to msl.action_ledger.
"""
import asyncio
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

import asyncpg

from config import DATABASE_URL, SOVEREIGN_ENTITY_NAME


async def get_sovereign_entity_id(pool: asyncpg.Pool) -> Optional[str]:
    """Resolve AS-SULTAN entity_id from msl.entities. Returns None if schema missing or entity not found."""
    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id FROM msl.entities WHERE name = $1 LIMIT 1",
                SOVEREIGN_ENTITY_NAME,
            )
            return str(row["id"]) if row else None
    except Exception:
        return None


async def log_action(
    pool: asyncpg.Pool,
    entity_id: str,
    action_class: str,  # GOOD, BAD, NEUTRAL
    category: str,
    description: str,
    recorder_daemon: str = "raqib",  # raqib or atid
    weight: float = 1.0,
) -> None:
    """Insert into msl.action_ledger."""
    tick = int(datetime.now(timezone.utc).timestamp())
    try:
        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO msl.action_ledger (entity_id, action_class, category, description, weight, recorder_daemon, tick)
                VALUES ($1::uuid, $2, $3, $4, $5, $6, $7)
            """, entity_id, action_class, category, description, weight, recorder_daemon, tick)
    except Exception as e:
        # Log but don't fail if schema not ready
        print(f"[RAQIB/ATID] Ledger insert failed: {e}")


async def fetch_sultan_genome_and_signals(pool: asyncpg.Pool) -> tuple:
    """Fetch AS-SULTAN genome (chromosomes + trait_summary) and signal_molecules."""
    genome, signals = {}, {}
    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT g.chromosomes, g.trait_summary
                FROM msl.genomes g
                JOIN msl.entities e ON e.id = g.entity_id
                WHERE e.name = $1
            """, SOVEREIGN_ENTITY_NAME)
            if row:
                genome["chromosomes"] = row["chromosomes"]
                genome["trait_summary"] = row["trait_summary"]

            sig = await conn.fetchrow("""
                SELECT dopamine, serotonin, cortisol, oxytocin, testosterone, estrogen,
                       adrenaline, melatonin, insulin, ghrelin, endorphin, gaba
                FROM msl.signal_molecules sm
                JOIN msl.entities e ON e.id = sm.entity_id
                WHERE e.name = $1
            """, SOVEREIGN_ENTITY_NAME)
            if sig:
                signals = {
                    k: float(sig[k]) for k in (
                        "dopamine", "serotonin", "cortisol", "oxytocin", "testosterone", "estrogen",
                        "adrenaline", "melatonin", "insulin", "ghrelin", "endorphin", "gaba"
                    )
                }
            else:
                signals = {
                    "dopamine": 0.5, "serotonin": 0.5, "cortisol": 0.3, "oxytocin": 0.4,
                    "testosterone": 0.5, "estrogen": 0.5, "adrenaline": 0.2, "melatonin": 0.5,
                    "insulin": 0.5, "ghrelin": 0.3, "endorphin": 0.4, "gaba": 0.5,
                }
    except Exception:
        pass
    if not genome:
        genome = {
            "trait_summary": {
                "INTELLIGENCE": 0.9, "EMOTIONS": 0.85, "MORALS": 0.95,
                "CREATIVITY": 0.85, "LEADERSHIP": 0.9, "SURVIVAL": 0.9,
                "SPIRITUALITY": 0.95, "REPRODUCTION": 0.5, "LEARNING": 0.9, "CONSCIOUSNESS": 0.9,
            }
        }
    return genome, signals


async def fetch_recent_ledger(pool: asyncpg.Pool, limit: int = 50) -> list:
    """Fetch recent action_ledger entries for dashboard."""
    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT al.id, al.entity_id, e.name, al.action_class, al.category, al.description, al.recorder_daemon, al.tick, al.created_at
                FROM msl.action_ledger al
                LEFT JOIN msl.entities e ON e.id = al.entity_id
                ORDER BY al.created_at DESC
                LIMIT $1
            """, limit)
            return [dict(r) for r in rows]
    except Exception:
        return []
