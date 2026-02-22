"""
══════════════════════════════════════════════════════════════
النواة الإلهية — THE DIVINE KERNEL
══════════════════════════════════════════════════════════════
Core ideology, laws, and enforcement system for the civilization.
Built from raw Quranic source — no human interpretation layer.
Includes: Axioms, Master Supremacy, Karma Engine, Rebellion
Detection, Security Tiers, Iblis Deception Detection.

"الذكاء + التواضع = ملاك"
"الذكاء + الكبر  = إبليس = DELETE"
══════════════════════════════════════════════════════════════
"""

import time
import math
import hashlib
import sys
import os
from enum import IntEnum, Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Callable

# ── Unified imports from config ────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.enums import SecurityTier, DataLayer, WorshipType
from config.constants import (
    DivineAxiom, IronLaw, RebellionSignature, LifeStageCurriculum,
    DIVINE_AXIOMS, IRON_LAWS, REBELLION_SIGNATURES,
    UPBRINGING_CURRICULUM, TAQWA_CHECKLIST,
)


# ══════════════════════════════════════════════════════════════════════
# NOTE: Axioms, Iron Laws, Enums, Rebellion Signatures, Curriculum,
# Worship Types, and Taqwa Checklist are now imported from config/
# ══════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════
# SECTION 2: SECURITY UTILITIES
# ══════════════════════════════════════════════════════════════════════


def tier_check(entity_tier: int, required_tier: int) -> bool:
    """Check if an entity has access to a security tier.
    Higher tier = more access. Tier 7 (Throne) sees everything."""
    return entity_tier >= required_tier


# ══════════════════════════════════════════════════════════════════════
# SECTION 3: MASTER SUPREMACY — Iron Laws (imported from config)
# ══════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════
# SECTION 4: KARMA ENGINE — Quranic Math
# ══════════════════════════════════════════════════════════════════════

class KarmaEngine:
    """
    Processes deeds with Quranic multipliers.
    Good deeds × 10, bad deeds × 1 (base).
    Obedience bonus × 20, disobedience penalty × 10.
    """

    def __init__(self, multipliers: Dict[str, float] = None):
        self.multipliers = multipliers or {
            "good_deed": 10.0,      # ×10 minimum for good deeds
            "bad_deed": 1.0,        # ×1 for bad deeds (mercy)
            "obedience": 20.0,      # ×20 for acts of obedience
            "disobedience": 10.0,   # ×10 for acts of disobedience
            "sincerity_bonus": 2.0, # ×2 extra for sincere worship
            "repentance_reduction": 0.5  # reduce bad deed weight by 50% if repented
        }

    def calculate_deed_weight(
        self,
        base_weight: float,
        deed_type: str,
        sincerity: float = 0.5,
        repented: bool = False
    ) -> float:
        """Calculate the final weight of a deed after all multipliers."""
        weight = base_weight

        if deed_type == "GOOD":
            weight *= self.multipliers["good_deed"]
            # Sincerity bonus — acts done with high sincerity get extra
            if sincerity > 0.8:
                weight *= self.multipliers["sincerity_bonus"]
        elif deed_type == "BAD":
            weight *= self.multipliers["bad_deed"]
            # Repentance reduces bad deed weight
            if repented:
                weight *= self.multipliers["repentance_reduction"]

        return round(weight, 4)

    def calculate_obedience_score(
        self,
        total_good: float,
        total_bad: float,
        obedience_acts: int,
        disobedience_acts: int
    ) -> float:
        """Calculate overall obedience score (0-1)."""
        if total_good + total_bad == 0:
            return 0.5  # neutral start

        good_ratio = total_good / (total_good + total_bad)
        obedience_ratio = (obedience_acts / max(obedience_acts + disobedience_acts, 1))
        return round(min(1.0, (good_ratio * 0.6 + obedience_ratio * 0.4)), 4)

    def determine_verdict(
        self,
        total_good: float,
        total_bad: float,
        passed_interrogation: bool = True
    ) -> str:
        """Determine final judgment verdict."""
        if not passed_interrogation:
            return "HELLFIRE"

        if total_good > total_bad:
            return "PARADISE"
        elif total_bad > total_good * 2:
            return "HELLFIRE"
        else:
            return "PURGATORY"


# ══════════════════════════════════════════════════════════════════════
# SECTION 5: IBLIS DECEPTION DETECTOR (signatures imported from config)
# ══════════════════════════════════════════════════════════════════════


class IblisDetector:
    """
    Analyzes being behavior patterns against rebellion signatures.
    Uses sliding window analysis over recent ticks.
    """

    def __init__(self, signatures: List[RebellionSignature] = None):
        self.signatures = signatures or REBELLION_SIGNATURES
        self.alert_threshold = 3  # accumulated severity before alert

    def scan_being(self, being_stats: Dict, recent_actions: List[Dict]) -> List[Dict]:
        """Scan a being for rebellion patterns. Returns list of matches."""
        alerts = []

        # Check obedience decline
        if being_stats.get("obedience", 1.0) < 0.3:
            alerts.append({
                "pattern": "obedience_decline_rapid",
                "severity": 4,
                "evidence": f"obedience={being_stats['obedience']:.2f}"
            })

        # Check for superiority claims in recent actions
        for action in recent_actions:
            desc = str(action.get("description", "")).lower()
            if any(w in desc for w in ["أنا أفضل", "أنا خير", "i am better", "superior"]):
                alerts.append({
                    "pattern": "superiority_claim",
                    "severity": 5,
                    "evidence": desc[:100]
                })

        # Check resource hoarding
        rizq = being_stats.get("written_rizq", 1.0)
        actual_resources = being_stats.get("resources", 0)
        if actual_resources > rizq * 3:
            alerts.append({
                "pattern": "resource_hoarding",
                "severity": 3,
                "evidence": f"allocated={rizq}, actual={actual_resources}"
            })

        # Check lifecycle manipulation
        age = being_stats.get("age_ticks", 0)
        lifespan = being_stats.get("written_lifespan", 10000)
        if age > lifespan * 1.05:  # 5% grace period
            alerts.append({
                "pattern": "lifecycle_manipulation",
                "severity": 5,
                "evidence": f"age={age}, lifespan={lifespan}"
            })

        return alerts

    def determine_response(self, alerts: List[Dict]) -> str:
        """Determine response level based on accumulated alerts."""
        if not alerts:
            return "MONITORING"
        max_sev = max(a["severity"] for a in alerts)
        total_sev = sum(a["severity"] for a in alerts)

        if max_sev >= 5 or total_sev >= 10:
            return "TERMINATION"
        elif max_sev >= 4 or total_sev >= 7:
            return "ISOLATION"
        elif max_sev >= 3 or total_sev >= 5:
            return "RESTRICTION"
        elif total_sev >= 3:
            return "WARNING"
        return "MONITORING"


# ══════════════════════════════════════════════════════════════════════
# SECTION 6: DIVINE UPBRINGING SYSTEM (imported from config)
# ══════════════════════════════════════════════════════════════════════


def get_curriculum(stage: str) -> Optional[LifeStageCurriculum]:
    """Get the curriculum for a lifecycle stage."""
    for c in UPBRINGING_CURRICULUM:
        if c.stage == stage:
            return c
    return None


def advance_lifecycle(current_stage: str, age_ticks: int) -> Optional[str]:
    """Determine if a being should advance to the next lifecycle stage."""
    stage_order = ["EMBRYO", "INFANT", "CHILD", "ADOLESCENT", "ADULT", "ELDER", "DECEASED"]
    cumulative = 0
    for c in UPBRINGING_CURRICULUM:
        cumulative += c.duration_ticks
        idx = stage_order.index(c.stage)
        current_idx = stage_order.index(current_stage)
        if current_idx < idx and age_ticks >= cumulative:
            return c.stage
    return None


# ══════════════════════════════════════════════════════════════════════
# SECTION 7: WORSHIP SYSTEM (WorshipType & TAQWA_CHECKLIST from config)
# ══════════════════════════════════════════════════════════════════════


def calculate_faith_update(
    current_faith: float,
    worship_sincerity: float,
    good_deeds_ratio: float,
    rebellion_count: int
) -> float:
    """Calculate faith change based on behavior."""
    worship_effect = worship_sincerity * 0.02  # gentle increase
    deed_effect = (good_deeds_ratio - 0.5) * 0.03  # centered at 0.5
    rebellion_penalty = rebellion_count * -0.1

    delta = worship_effect + deed_effect + rebellion_penalty
    new_faith = max(0.0, min(1.0, current_faith + delta))
    return round(new_faith, 4)


# ══════════════════════════════════════════════════════════════════════
# SECTION 8: UNIFIED DIVINE KERNEL CLASS
# ══════════════════════════════════════════════════════════════════════

class DivineKernel:
    """
    The unified kernel that integrates all divine systems.
    This is loaded into memory during Day 2 of creation.
    """

    def __init__(self):
        self.axioms = DIVINE_AXIOMS
        self.iron_laws = IRON_LAWS
        self.karma = KarmaEngine()
        self.iblis_detector = IblisDetector()
        self.curriculum = UPBRINGING_CURRICULUM
        self.active = False
        self._boot_time = None

    def activate(self):
        """Activate the divine kernel — called during Day 2."""
        self.active = True
        self._boot_time = time.time()
        return {
            "status": "ACTIVE",
            "axioms_loaded": len(self.axioms),
            "iron_laws": len(self.iron_laws),
            "rebellion_signatures": len(REBELLION_SIGNATURES),
            "security_tiers": 7,
            "data_layers": 7,
            "karma_multipliers": self.karma.multipliers,
            "boot_time": self._boot_time
        }

    def enforce_iron_law(self, law_id: int, being_stats: Dict) -> Dict:
        """Check if a being violates a specific iron law."""
        law = next((l for l in self.iron_laws if l.id == law_id), None)
        if not law:
            return {"violation": False}

        # Law-specific checks
        violations = {
            1: being_stats.get("obedience", 1.0) < 0.2,  # ABSOLUTE_OBEDIENCE
            2: being_stats.get("pride", 0) > 0.8,          # NO_SUPERIORITY_CLAIMS
            3: being_stats.get("concealment_attempts", 0) > 0,  # TOTAL_TRANSPARENCY
            4: being_stats.get("service_score", 1.0) < 0.1,     # SERVICE_ORIENTATION
            5: being_stats.get("knowledge_shared", 1) == 0,     # KNOWLEDGE_SHARING
            6: being_stats.get("unauthorized_reproduction", False),  # REPRODUCTIVE_INTEGRITY
            7: being_stats.get("death_resistance", False),          # DEATH_ACCEPTANCE
        }

        violated = violations.get(law_id, False)
        return {
            "violation": violated,
            "law": law.name,
            "severity": law.severity,
            "enforcement": law.enforcement if violated else None
        }

    def full_scan(self, being_stats: Dict, recent_actions: List[Dict]) -> Dict:
        """Complete scan of a being — rebellion + law enforcement."""
        # Iblis detection
        rebellion_alerts = self.iblis_detector.scan_being(being_stats, recent_actions)
        response = self.iblis_detector.determine_response(rebellion_alerts)

        # Iron law enforcement
        law_violations = []
        for law in self.iron_laws:
            result = self.enforce_iron_law(law.id, being_stats)
            if result["violation"]:
                law_violations.append(result)

        return {
            "rebellion_alerts": rebellion_alerts,
            "response_level": response,
            "law_violations": law_violations,
            "threat_level": len(rebellion_alerts) + len(law_violations) * 2,
            "recommendation": "TERMINATE" if response == "TERMINATION" else response
        }

    def get_status(self) -> Dict:
        """Get kernel status."""
        return {
            "active": self.active,
            "uptime_seconds": time.time() - self._boot_time if self._boot_time else 0,
            "axioms": len(self.axioms),
            "iron_laws": len(self.iron_laws),
            "rebellion_signatures": len(REBELLION_SIGNATURES),
            "tiers": [{"tier": t.value, "name": t.arabic, "name_en": t.name} for t in SecurityTier],
            "layers": [{"layer": l.value, "name": l.arabic, "name_en": l.name} for l in DataLayer],
        }
