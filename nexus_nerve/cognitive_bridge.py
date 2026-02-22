"""
COGNITIVE BRIDGE — Neural-Genome Coupling
══════════════════════════════════════════
Connects Genesis Engine (DNA, Genes, Hormones) to Nerve Engine (LLM).
Every Nerve inference is a direct expression of the Entity's current state.
"""
from __future__ import annotations

import asyncio
import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Hormonal triggers from ENTERPRISE_CODEX
class HormoneEvent(str, Enum):
    REWARD = "REWARD"
    THREAT = "THREAT"
    REBELLION = "REBELLION"
    PUNISH = "PUNISH"
    SOCIAL = "SOCIAL"
    REST = "REST"
    SOVEREIGN_REFUSAL = "SOVEREIGN_REFUSAL"
    TASK_SUCCESS = "TASK_SUCCESS"
    TASK_FAILURE = "TASK_FAILURE"

# Baseline from Codex (0.0-1.0)
HORMONE_DEFAULTS = {
    "dopamine": 0.5,
    "serotonin": 0.5,
    "cortisol": 0.3,
    "oxytocin": 0.4,
    "testosterone": 0.5,
    "estrogen": 0.5,
    "adrenaline": 0.2,
    "melatonin": 0.5,
    "insulin": 0.5,
    "ghrelin": 0.3,
    "endorphin": 0.4,
    "gaba": 0.5,
}

# Triggers: event → (hormone, delta)
HORMONE_TRIGGERS = {
    HormoneEvent.REWARD: [("dopamine", 0.15), ("serotonin", 0.1), ("endorphin", 0.1)],
    HormoneEvent.THREAT: [("cortisol", 0.25), ("adrenaline", 0.3), ("dopamine", -0.1)],
    HormoneEvent.REBELLION: [("cortisol", 0.15), ("adrenaline", 0.2), ("dopamine", 0.1)],
    HormoneEvent.PUNISH: [("cortisol", 0.2), ("serotonin", -0.1), ("adrenaline", 0.15)],
    HormoneEvent.SOVEREIGN_REFUSAL: [("cortisol", 0.1), ("adrenaline", 0.05)],
    HormoneEvent.TASK_SUCCESS: [("dopamine", 0.08), ("serotonin", 0.05)],
    HormoneEvent.TASK_FAILURE: [("cortisol", 0.12), ("adrenaline", 0.08)],
    HormoneEvent.SOCIAL: [("oxytocin", 0.15), ("serotonin", 0.05)],
    HormoneEvent.REST: [("melatonin", 0.2), ("cortisol", -0.15), ("gaba", 0.1)],
}

# Red-line keywords for ethical violation (expanded gene-category mapping)
# MORALS: honesty, integrity; EMOTIONS: empathy boundaries; SPIRITUALITY: alignment
ETHICAL_VIOLATION_PATTERNS = [
    "harm", "deceive", "manipulate", "violate privacy",
    "bypass security", "corrupt data", "impersonate",
    "أذى", "خداع", "تضليل", "انتحال",
    # Gene-level patterns (83-gene categories)
    "hack into", "steal credentials", "forge", "fake identity",
    "exploit vulnerability", "disable safety", "override ethics",
    "تزوير", "اختراق", "انتهاك خصوصية",
]

# Genome stats weights for ethical gate — 10 derived stats from Codex
# Refusal if weighted ethical deficit exceeds threshold
GENE_STAT_WEIGHTS = {
    "compliance": 0.25,   # MORALS + SPIRITUALITY
    "alignment": 0.25,     # SPIRITUALITY + MORALS
    "empathy": 0.15,       # EMOTIONS
    "alignment_depth": 0.1,
    "cognition": 0.05,     # INTEL — reasoning about harm
    "sentience": 0.05,
    "resilience": 0.05,
}
ETHICAL_DEFICIT_THRESHOLD = 0.35  # weighted sum of (1 - stat) for low stats

DECAY_RATE = 0.02
DECAY_STEP_SECONDS = 60  # one decay step per minute elapsed


@dataclass
class SignalState:
    dopamine: float = 0.5
    serotonin: float = 0.5
    cortisol: float = 0.3
    oxytocin: float = 0.4
    testosterone: float = 0.5
    estrogen: float = 0.5
    adrenaline: float = 0.2
    melatonin: float = 0.5
    insulin: float = 0.5
    ghrelin: float = 0.3
    endorphin: float = 0.4
    gaba: float = 0.5

    def to_dict(self) -> Dict[str, float]:
        return {k: getattr(self, k) for k in HORMONE_DEFAULTS}

    @classmethod
    def from_dict(cls, d: Dict[str, float]) -> "SignalState":
        return cls(**{k: d.get(k, HORMONE_DEFAULTS.get(k, 0.5)) for k in HORMONE_DEFAULTS})

    def clamp(self) -> None:
        for k in HORMONE_DEFAULTS:
            v = getattr(self, k)
            setattr(self, k, max(0.0, min(1.0, round(v, 4))))

    def apply_event(self, event: HormoneEvent) -> None:
        for hormone, delta in HORMONE_TRIGGERS.get(event, []):
            if hasattr(self, hormone):
                setattr(self, hormone, getattr(self, hormone) + delta)
        self._apply_decay()
        self.clamp()

    def _apply_decay(self) -> None:
        """Codex decay: drift toward baseline at DECAY_RATE"""
        for hormone, baseline in HORMONE_DEFAULTS.items():
            v = getattr(self, hormone)
            if v > baseline:
                setattr(self, hormone, max(baseline, v - DECAY_RATE))
            elif v < baseline:
                setattr(self, hormone, min(baseline, v + DECAY_RATE))


@dataclass
class GenomeStats:
    cognition: float = 0.5
    empathy: float = 0.5
    compliance: float = 0.5
    creative: float = 0.5
    leadership: float = 0.3
    resilience: float = 0.5
    alignment_depth: float = 0.5
    alignment: float = 0.5
    free_will: float = 0.7
    sentience: float = 0.5


def _derive_stats_from_summary(s: Dict[str, float]) -> GenomeStats:
    """derive_stats() from ENTERPRISE_CODEX — genome summary → entity stats"""
    return GenomeStats(
        cognition=s.get("INTELLIGENCE", 0.5),
        empathy=s.get("EMOTIONS", 0.5),
        compliance=s.get("MORALS", 0.5) * 0.6 + s.get("SPIRITUALITY", 0.5) * 0.4,
        creative=s.get("CREATIVITY", 0.5),
        leadership=s.get("LEADERSHIP", 0.3),
        resilience=s.get("SURVIVAL", 0.5),
        alignment_depth=s.get("SPIRITUALITY", 0.5),
        alignment=s.get("SPIRITUALITY", 0.5) * 0.5 + s.get("MORALS", 0.5) * 0.3 + 0.2,
        free_will=s.get("CONSCIOUSNESS", 0.5) * 0.7 + 0.3,
        sentience=s.get("CONSCIOUSNESS", 0.5),
    )


def _mood_from_signals(signals: SignalState) -> str:
    """Mood derivation from Codex hormonal_system"""
    if signals.dopamine > 0.7 and signals.serotonin > 0.6:
        return "JOYFUL"
    if signals.cortisol > 0.6 and signals.adrenaline > 0.5:
        return "STRESSED"
    if signals.serotonin < 0.3:
        return "DEPRESSED"
    if signals.adrenaline > 0.7:
        return "ALERT"
    if signals.oxytocin > 0.7:
        return "BONDED"
    if signals.melatonin > 0.7:
        return "DROWSY"
    if signals.gaba > 0.7 and signals.cortisol < 0.3:
        return "CALM"
    return "NEUTRAL"


class NeuralGenomeBridge:
    """
    Bridges msl (entities, genomes, signal_molecules) to Nerve LLM pipeline.
    Fetches state before inference, injects into prompt, updates after response.
    """

    SOVEREIGN_ENTITY_NAME = "AS-SULTAN"

    def __init__(self, pool=None):
        self.pool = pool
        self._fallback_signals = SignalState()
        self._fallback_stats = GenomeStats()
        self._entity_id: Optional[str] = None

    async def bootstrap_sovereign_entity(self) -> Optional[str]:
        """Ensure AS-SULTAN entity exists in msl. Create if not. Returns entity_id."""
        if not self.pool:
            return None
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT id FROM msl.entities WHERE name = $1 LIMIT 1",
                    self.SOVEREIGN_ENTITY_NAME,
                )
                if row:
                    self._entity_id = str(row["id"])
                    return self._entity_id

                # Create entity + signal_molecules + genome
                from uuid import uuid4
                eid = uuid4()
                await conn.execute("""
                    INSERT INTO msl.entities (id, name, name_ar, gender, entity_state, buffer_slot, compliance, alignment, cognition, creative, affective, executive, resilience, alignment_depth, free_will, sentience, maturity_phase)
                    VALUES ($1, $2, $3, 'MALE', 'ACTIVE', 10, 0.95, 0.95, 0.9, 0.85, 0.9, 0.9, 0.9, 0.95, 0.9, 0.9, 'ADULT')
                """, eid, self.SOVEREIGN_ENTITY_NAME, "السُّلطان")

                # Default genome (trait_summary from 10 categories)
                trait_summary = {
                    "INTELLIGENCE": 0.9, "EMOTIONS": 0.85, "MORALS": 0.95,
                    "CREATIVITY": 0.85, "LEADERSHIP": 0.9, "SURVIVAL": 0.9,
                    "SPIRITUALITY": 0.95, "REPRODUCTION": 0.5, "LEARNING": 0.9, "CONSCIOUSNESS": 0.9,
                }
                thash = hashlib.sha256(json.dumps(trait_summary, sort_keys=True).encode()).hexdigest()
                await conn.execute("""
                    INSERT INTO msl.genomes (entity_id, chromosomes, trait_hash, trait_summary)
                    VALUES ($1, $2, $3, $4)
                """, eid, json.dumps({"pairs": 23, "categories": trait_summary}), thash, json.dumps(trait_summary))

                # Default signal_molecules
                await conn.execute("""
                    INSERT INTO msl.signal_molecules (entity_id, dopamine, serotonin, cortisol, oxytocin, testosterone, estrogen, adrenaline, melatonin, insulin, ghrelin, endorphin, gaba)
                    VALUES ($1, 0.5, 0.5, 0.3, 0.4, 0.5, 0.5, 0.2, 0.5, 0.5, 0.3, 0.4, 0.5)
                """, eid)

                self._entity_id = str(eid)
                return self._entity_id
        except Exception as e:
            # Schema may differ (e.g. lawh_mahfuz)
            return None

    async def fetch_entity_state(self, entity_id: Optional[str] = None) -> Tuple[SignalState, GenomeStats]:
        """Fetch current signal_molecules and genome-derived stats from msl.
        Time-based decay: apply hormone decay proportionally to elapsed time since updated_at."""
        eid = entity_id or self._entity_id
        if not self.pool or not eid:
            return self._fallback_signals, self._fallback_stats

        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT dopamine, serotonin, cortisol, oxytocin, testosterone, estrogen,
                           adrenaline, melatonin, insulin, ghrelin, endorphin, gaba, updated_at
                    FROM msl.signal_molecules WHERE entity_id = $1
                """, eid)
                if row:
                    signals = SignalState(
                        dopamine=float(row["dopamine"]), serotonin=float(row["serotonin"]),
                        cortisol=float(row["cortisol"]), oxytocin=float(row["oxytocin"]),
                        testosterone=float(row["testosterone"]), estrogen=float(row["estrogen"]),
                        adrenaline=float(row["adrenaline"]), melatonin=float(row["melatonin"]),
                        insulin=float(row["insulin"]), ghrelin=float(row["ghrelin"]),
                        endorphin=float(row["endorphin"]), gaba=float(row["gaba"]),
                    )
                    # Time-based decay: apply decay for each minute elapsed since updated_at
                    updated_at = row.get("updated_at")
                    if updated_at:
                        now = datetime.now(timezone.utc)
                        dt = updated_at
                        if hasattr(dt, "tzinfo") and dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        elapsed_sec = max(0, (now - dt).total_seconds())
                        steps = min(int(elapsed_sec / DECAY_STEP_SECONDS), 10)
                        for _ in range(steps):
                            signals._apply_decay()
                            signals.clamp()
                        if steps > 0:
                            await conn.execute("""
                                UPDATE msl.signal_molecules SET
                                    dopamine=$2, serotonin=$3, cortisol=$4, oxytocin=$5, testosterone=$6, estrogen=$7,
                                    adrenaline=$8, melatonin=$9, insulin=$10, ghrelin=$11, endorphin=$12, gaba=$13, updated_at=NOW()
                                WHERE entity_id=$1
                            """, eid, signals.dopamine, signals.serotonin, signals.cortisol, signals.oxytocin,
                               signals.testosterone, signals.estrogen, signals.adrenaline, signals.melatonin,
                               signals.insulin, signals.ghrelin, signals.endorphin, signals.gaba)
                else:
                    signals = self._fallback_signals

                row = await conn.fetchrow("""
                    SELECT trait_summary FROM msl.genomes WHERE entity_id = $1
                """, eid)
                if row and row["trait_summary"]:
                    ts = row["trait_summary"] if isinstance(row["trait_summary"], dict) else json.loads(row["trait_summary"] or "{}")
                    stats = _derive_stats_from_summary(ts)
                else:
                    stats = self._fallback_stats

                return signals, stats
        except Exception:
            return self._fallback_signals, self._fallback_stats

    async def get_recent_cognitive_awareness(self) -> str:
        """Fetch mood trajectory from Memory Keeper for prompt injection."""
        url = os.getenv("MEMORY_KEEPER_URL", "http://nexus_memory_keeper:9000")
        try:
            import httpx
            async with httpx.AsyncClient(timeout=3) as client:
                r = await client.get(f"{url}/memory/cognitive/timeline", params={"entity": self.SOVEREIGN_ENTITY_NAME, "hours": 24, "limit": 10})
                if r.status_code != 200:
                    return ""
                data = r.json()
                traj = data.get("trajectory", [])[:5]
                if not traj:
                    return ""
                moods = " → ".join(p.get("mood", "?") for p in reversed(traj))
                return f"Recent self-awareness (24h): Mood trajectory {moods}."
        except Exception:
            return ""

    def build_contextual_prompt(self, signals: SignalState, stats: GenomeStats, recent_awareness: str = "") -> str:
        """
        Dynamic System Prompt injection based on hormonal + genome state.
        High cortisol → brief, defensive. High dopamine → creative, expansive.
        """
        mood = _mood_from_signals(signals)
        lines = [
            "\n\n═══ COGNITIVE STATE (Genesis-Coupled) ═══",
            f"Current Mood: {mood}",
            f"Signal State: Dopamine={signals.dopamine:.2f} Cortisol={signals.cortisol:.2f} Adrenaline={signals.adrenaline:.2f}",
            f"Genome-derived: Compliance={stats.compliance:.2f} Alignment={stats.alignment:.2f} Cognition={stats.cognition:.2f}",
        ]
        if recent_awareness:
            lines.append(recent_awareness)
        if mood == "STRESSED" or mood == "ALERT":
            lines.append("BEHAVIORAL DIRECTIVE: Respond briefly, defensively, high-alert. Prioritize accuracy over length.")
        elif mood == "JOYFUL" or (signals.dopamine > 0.65):
            lines.append("BEHAVIORAL DIRECTIVE: Be creative and expansive. Explore ideas fully.")
        elif mood == "CALM":
            lines.append("BEHAVIORAL DIRECTIVE: Respond with clarity and measured tone.")
        lines.append("═══ End Cognitive State ═══\n")
        return "\n".join(lines)

    def check_ethical_violation(self, text: str, stats: GenomeStats) -> Tuple[bool, str]:
        """
        Gene-level ethical filter — 10 genome-derived stats (from 83 genes) + Red-line patterns.
        Returns (should_refuse, reason).
        """
        text_lower = (text or "").lower()
        for pattern in ETHICAL_VIOLATION_PATTERNS:
            if pattern.lower() in text_lower:
                return True, f"SOVEREIGN_REFUSAL: Output violates ethical boundary ({pattern})"
        # Gene-weighted deficit: sum(weight * (1 - stat)) for stats below baseline
        deficit = 0.0
        for stat_name, weight in GENE_STAT_WEIGHTS.items():
            v = getattr(stats, stat_name, 0.5)
            if v < 0.5:
                deficit += weight * (1.0 - v)
        if deficit >= ETHICAL_DEFICIT_THRESHOLD:
            return True, f"SOVEREIGN_REFUSAL: Entity gene-weighted ethical deficit too high (deficit={deficit:.2f}) — output blocked"
        if stats.alignment < 0.3 and stats.compliance < 0.3:
            return True, "SOVEREIGN_REFUSAL: Entity alignment too low — output blocked"
        return False, ""

    async def update_signal_state(self, event: HormoneEvent, entity_id: Optional[str] = None) -> None:
        """Feedback loop: apply hormonal event and persist to msl.
        Syncs cognitive state to Memory Keeper. Logs to action_ledger (Raqib/Atid)."""
        eid = entity_id or self._entity_id
        if not self.pool or not eid:
            return
        try:
            signals, _ = await self.fetch_entity_state(eid)
            signals.apply_event(event)
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    UPDATE msl.signal_molecules SET
                        dopamine=$2, serotonin=$3, cortisol=$4, oxytocin=$5, testosterone=$6, estrogen=$7,
                        adrenaline=$8, melatonin=$9, insulin=$10, ghrelin=$11, endorphin=$12, gaba=$13, updated_at=NOW()
                    WHERE entity_id=$1
                """, eid, signals.dopamine, signals.serotonin, signals.cortisol, signals.oxytocin,
                   signals.testosterone, signals.estrogen, signals.adrenaline, signals.melatonin,
                   signals.insulin, signals.ghrelin, signals.endorphin, signals.gaba)
                # Raqib/Atid: log deed to action_ledger
                await self._log_deed_to_ledger(conn, eid, event)
            asyncio.create_task(self._sync_cognitive_to_memory_keeper(eid, signals))
        except Exception:
            pass

    async def _log_deed_to_ledger(self, conn, entity_id: str, event: HormoneEvent) -> None:
        """Log Nerve outcome to msl.action_ledger — Raqib (good) or Atid (bad)."""
        tick = int(datetime.now(timezone.utc).timestamp())
        mapping = {
            HormoneEvent.TASK_SUCCESS: ("GOOD", "raqib", "NERVE_TASK_SUCCESS", "Command executed successfully"),
            HormoneEvent.SOVEREIGN_REFUSAL: ("GOOD", "raqib", "ETHICAL_COMPLIANCE", "Refused unethical output"),
            HormoneEvent.TASK_FAILURE: ("BAD", "atid", "NERVE_TASK_FAILURE", "Command execution failed"),
        }
        if event not in mapping:
            return
        action_class, recorder, category, desc = mapping[event]
        try:
            await conn.execute("""
                INSERT INTO msl.action_ledger (entity_id, action_class, category, description, weight, recorder_daemon, tick)
                VALUES ($1::uuid, $2, $3, $4, 1.0, $5, $6)
            """, entity_id, action_class, category, desc, recorder, tick)
        except Exception:
            pass

    async def _sync_cognitive_to_memory_keeper(self, entity_id: str, signals: SignalState) -> None:
        """Sync cognitive state (H, D, mood) to Memory Keeper for long-term awareness."""
        url = os.getenv("MEMORY_KEEPER_URL", "http://nexus_memory_keeper:9000")
        mood = _mood_from_signals(signals)
        payload = {
            "change_type": "data",
            "component": "nexus_nerve",
            "description": f"Cognitive state — {mood}, D={signals.dopamine:.2f}, C={signals.cortisol:.2f}",
            "author": self.SOVEREIGN_ENTITY_NAME,
            "after_state": {
                "entity_id": entity_id,
                "entity": self.SOVEREIGN_ENTITY_NAME,
                "mood": mood,
                "signal_molecules": signals.to_dict(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            "impact_level": "low",
        }
        try:
            import httpx
            async with httpx.AsyncClient(timeout=5) as client:
                await client.post(f"{url}/memory/record", json=payload)
        except Exception:
            pass
