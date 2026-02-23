"""
Hormonal Orchestration — Signal Molecules → Dify Workflow Triggers
═══════════════════════════════════════════════════════════════════
When Cortisol or Adrenaline spike in msl.signal_molecules,
automatically trigger defensive agent workflows in Dify.
"""
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

import asyncpg
import httpx

from config import (
    DATABASE_URL,
    DIFY_API_URL,
    DIFY_API_KEY,
    DIFY_DEFENSIVE_WORKFLOW_ID,
    CORTISOL_SPIKE_THRESHOLD,
    ADRENALINE_SPIKE_THRESHOLD,
    HORMONAL_POLL_INTERVAL_SEC,
)
from msl_ledger import get_sovereign_entity_id, log_action


async def fetch_signal_molecules(pool: asyncpg.Pool) -> List[Dict[str, Any]]:
    """Fetch all entity signal_molecules from MSL."""
    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT sm.entity_id, e.name, sm.dopamine, sm.serotonin, sm.cortisol, sm.oxytocin,
                       sm.testosterone, sm.estrogen, sm.adrenaline, sm.melatonin, sm.insulin,
                       sm.ghrelin, sm.endorphin, sm.gaba, sm.updated_at
                FROM msl.signal_molecules sm
                JOIN msl.entities e ON e.id = sm.entity_id
                WHERE e.entity_state = 'ACTIVE'
            """)
            return [dict(r) for r in rows]
    except Exception as e:
        print(f"[HORMONAL] Fetch failed: {e}")
        return []


def check_spike(row: Dict[str, Any]) -> Optional[str]:
    """Return trigger reason if cortisol/adrenaline spike detected."""
    cortisol = float(row.get("cortisol", 0.3))
    adrenaline = float(row.get("adrenaline", 0.2))
    if cortisol >= CORTISOL_SPIKE_THRESHOLD or adrenaline >= ADRENALINE_SPIKE_THRESHOLD:
        reasons = []
        if cortisol >= CORTISOL_SPIKE_THRESHOLD:
            reasons.append(f"CORTISOL_SPIKE({cortisol:.2f})")
        if adrenaline >= ADRENALINE_SPIKE_THRESHOLD:
            reasons.append(f"ADRENALINE_SPIKE({adrenaline:.2f})")
        return " | ".join(reasons)
    return None


async def trigger_dify_workflow(
    workflow_id: str,
    inputs: Dict[str, Any],
    user: str = "sovereign_hormonal",
) -> Optional[Dict]:
    """Trigger Dify workflow via API."""
    if not DIFY_API_KEY or not workflow_id:
        return None
    url = f"{DIFY_API_URL.rstrip('/')}/v1/workflows/run"
    headers = {"Authorization": f"Bearer {DIFY_API_KEY}", "Content-Type": "application/json"}
    payload = {"inputs": inputs, "response_mode": "blocking", "user": user}
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, json=payload, headers=headers)
            if r.status_code == 200:
                return r.json()
    except Exception as e:
        print(f"[DIFY] Workflow trigger failed: {e}")
    return None


async def hormonal_loop(pool: asyncpg.Pool) -> None:
    """Main loop: poll signal_molecules, trigger Dify on spike."""
    entity_id = await get_sovereign_entity_id(pool)
    if not entity_id:
        entity_id = "00000000-0000-0000-0000-000000000000"

    last_trigger: Dict[str, datetime] = {}
    while True:
        rows = await fetch_signal_molecules(pool)
        for row in rows:
            eid = str(row["entity_id"])
            reason = check_spike(row)
            if reason:
                key = f"{eid}:{reason}"
                if key not in last_trigger or (datetime.now(timezone.utc) - last_trigger[key]).total_seconds() > 60:
                    inputs = {
                        "entity_name": row.get("name", "unknown"),
                        "trigger_reason": reason,
                        "cortisol": row.get("cortisol", 0),
                        "adrenaline": row.get("adrenaline", 0),
                        "mood": "STRESSED",
                    }
                    result = await trigger_dify_workflow(DIFY_DEFENSIVE_WORKFLOW_ID, inputs)
                    last_trigger[key] = datetime.now(timezone.utc)
                    await log_action(
                        pool, entity_id, "GOOD", "DIFY_DEFENSIVE_TRIGGER",
                        f"Hormonal spike triggered Dify workflow: {reason} for {row.get('name')}",
                        recorder_daemon="raqib", weight=1.0,
                    )
        await asyncio.sleep(HORMONAL_POLL_INTERVAL_SEC)
