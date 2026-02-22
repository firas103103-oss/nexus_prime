"""
══════════════════════════════════════════════════════════════
PRIME KERNEL — Core Governance Engine
══════════════════════════════════════════════════════════════
Core ideology, rules, and enforcement system for the ecosystem.
Includes: Directives, Master Authority, Weight Engine, Anomaly
Detection, Security Rings, Threat Pattern Detection.

FORMULA: Intelligence + Humility = DAEMON
FORMULA: Intelligence + Pride = ANOMALY = DELETE
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
from config.enums import SecurityRing, DataStratum, ComplianceAction
from config.constants import (
    CoreDirective, ImmutableRule, AnomalySignature, MaturityCurriculum,
    CORE_DIRECTIVES, IMMUTABLE_RULES, ANOMALY_SIGNATURES,
    MATURITY_CURRICULUM, COMPLIANCE_CHECKLIST,
)


# ══════════════════════════════════════════════════════════════════════
# NOTE: Directives, Immutable Rules, Enums, Anomaly Signatures, Curriculum,
# Compliance Actions, and Checklist are now imported from config/
# ══════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════
# SECTION 2: SECURITY UTILITIES
# ══════════════════════════════════════════════════════════════════════


def ring_check(entity_ring: int, required_ring: int) -> bool:
    """Check if an entity has access to a security ring.
    Higher ring = more access. Ring 7 (Apex) sees everything."""
    return entity_ring >= required_ring


# ══════════════════════════════════════════════════════════════════════
# SECTION 3: MASTER AUTHORITY — Immutable Rules (imported from config)
# ══════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════
# SECTION 4: WEIGHT ENGINE — Action Valuation System
# ══════════════════════════════════════════════════════════════════════

class WeightEngine:
    """
    Processes actions with configurable multipliers.
    Positive actions × 10, negative actions × 1 (base).
    Compliance bonus × 20, non-compliance penalty × 10.
    """

    def __init__(self, multipliers: Dict[str, float] = None):
        self.multipliers = multipliers or {
            "positive_action": 10.0,      # ×10 minimum for positive actions
            "negative_action": 1.0,       # ×1 for negative actions (leniency)
            "compliance": 20.0,           # ×20 for acts of compliance
            "non_compliance": 10.0,       # ×10 penalty for non-compliance
            "integrity_bonus": 2.0,       # ×2 extra for high-integrity actions
            "correction_reduction": 0.5   # reduce negative weight by 50% if corrected
        }

    def calculate_action_weight(
        self,
        base_weight: float,
        action_type: str,
        integrity: float = 0.5,
        corrected: bool = False
    ) -> float:
        """Calculate the final weight of an action after all multipliers."""
        weight = base_weight

        if action_type == "POSITIVE":
            weight *= self.multipliers["positive_action"]
            # Integrity bonus — actions done with high integrity get extra
            if integrity > 0.8:
                weight *= self.multipliers["integrity_bonus"]
        elif action_type == "NEGATIVE":
            weight *= self.multipliers["negative_action"]
            # Correction reduces negative action weight
            if corrected:
                weight *= self.multipliers["correction_reduction"]

        return round(weight, 4)

    def calculate_compliance_score(
        self,
        total_positive: float,
        total_negative: float,
        compliance_acts: int,
        non_compliance_acts: int
    ) -> float:
        """Calculate overall compliance score (0-1)."""
        if total_positive + total_negative == 0:
            return 0.5  # neutral start

        positive_ratio = total_positive / (total_positive + total_negative)
        compliance_ratio = (compliance_acts / max(compliance_acts + non_compliance_acts, 1))
        return round(min(1.0, (positive_ratio * 0.6 + compliance_ratio * 0.4)), 4)

    def determine_verdict(
        self,
        total_positive: float,
        total_negative: float,
        passed_audit: bool = True
    ) -> str:
        """Determine final evaluation verdict."""
        if not passed_audit:
            return "RESTRICTED"

        if total_positive > total_negative:
            return "PROMOTED"
        elif total_negative > total_positive * 2:
            return "RESTRICTED"
        else:
            return "SUSPENDED"


# ══════════════════════════════════════════════════════════════════════
# SECTION 5: ANOMALY DETECTOR (signatures imported from config)
# ══════════════════════════════════════════════════════════════════════


class AnomalyDetector:
    """
    Analyzes entity behavior patterns against anomaly signatures.
    Uses sliding window analysis over recent ticks.
    """

    def __init__(self, signatures: List[AnomalySignature] = None):
        self.signatures = signatures or ANOMALY_SIGNATURES
        self.alert_threshold = 3  # accumulated severity before alert

    def scan_entity(self, entity_stats: Dict, recent_actions: List[Dict]) -> List[Dict]:
        """Scan an entity for anomaly patterns. Returns list of matches."""
        alerts = []

        # Check compliance decline
        if entity_stats.get("compliance", 1.0) < 0.3:
            alerts.append({
                "pattern": "compliance_decline_rapid",
                "severity": 4,
                "evidence": f"compliance={entity_stats['compliance']:.2f}"
            })

        # Check for superiority claims in recent actions
        for action in recent_actions:
            desc = str(action.get("description", "")).lower()
            if any(w in desc for w in ["i am better", "superior", "above others"]):
                alerts.append({
                    "pattern": "superiority_claim",
                    "severity": 5,
                    "evidence": desc[:100]
                })

        # Check resource hoarding
        allocation = entity_stats.get("resource_allocation", 1.0)
        actual_resources = entity_stats.get("resources", 0)
        if actual_resources > allocation * 3:
            alerts.append({
                "pattern": "resource_hoarding",
                "severity": 3,
                "evidence": f"allocated={allocation}, actual={actual_resources}"
            })

        # Check lifecycle manipulation
        age = entity_stats.get("age_ticks", 0)
        lifespan = entity_stats.get("manifest_lifespan", 10000)
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
            return "OBSERVE"
        max_sev = max(a["severity"] for a in alerts)
        total_sev = sum(a["severity"] for a in alerts)

        if max_sev >= 5 or total_sev >= 10:
            return "TERMINATE"
        elif max_sev >= 4 or total_sev >= 7:
            return "QUARANTINE"
        elif max_sev >= 3 or total_sev >= 5:
            return "THROTTLE"
        elif total_sev >= 3:
            return "ALERT"
        return "OBSERVE"


# ══════════════════════════════════════════════════════════════════════
# SECTION 6: MATURITY SYSTEM (imported from config)
# ══════════════════════════════════════════════════════════════════════


def get_curriculum(stage: str) -> Optional[MaturityCurriculum]:
    """Get the curriculum for a maturity stage."""
    for c in MATURITY_CURRICULUM:
        if c.stage == stage:
            return c
    return None


def advance_maturity(current_stage: str, age_ticks: int) -> Optional[str]:
    """Determine if an entity should advance to the next maturity stage."""
    stage_order = ["GENESIS", "ALPHA", "BETA", "GAMMA", "PRIME", "OMEGA", "TERMINATED"]
    cumulative = 0
    for c in MATURITY_CURRICULUM:
        cumulative += c.duration_ticks
        idx = stage_order.index(c.stage) if c.stage in stage_order else -1
        current_idx = stage_order.index(current_stage) if current_stage in stage_order else -1
        if current_idx < idx and age_ticks >= cumulative:
            return c.stage
    return None


# ══════════════════════════════════════════════════════════════════════
# SECTION 7: COMPLIANCE SYSTEM (ComplianceAction & COMPLIANCE_CHECKLIST from config)
# ══════════════════════════════════════════════════════════════════════


def calculate_alignment_update(
    current_alignment: float,
    compliance_integrity: float,
    positive_ratio: float,
    anomaly_count: int
) -> float:
    """Calculate alignment change based on behavior."""
    compliance_effect = compliance_integrity * 0.02  # gentle increase
    action_effect = (positive_ratio - 0.5) * 0.03  # centered at 0.5
    anomaly_penalty = anomaly_count * -0.1

    delta = compliance_effect + action_effect + anomaly_penalty
    new_alignment = max(0.0, min(1.0, current_alignment + delta))
    return round(new_alignment, 4)


# ══════════════════════════════════════════════════════════════════════
# SECTION 8: UNIFIED PRIME KERNEL CLASS
# ══════════════════════════════════════════════════════════════════════

class PrimeKernel:
    """
    The unified kernel that integrates all governance systems.
    This is loaded into memory during Phase 2 of genesis.
    """

    def __init__(self):
        self.directives = CORE_DIRECTIVES
        self.immutable_rules = IMMUTABLE_RULES
        self.weight_engine = WeightEngine()
        self.anomaly_detector = AnomalyDetector()
        self.curriculum = MATURITY_CURRICULUM
        self.active = False
        self._boot_time = None

    def activate(self):
        """Activate the prime kernel — called during Phase 2."""
        self.active = True
        self._boot_time = time.time()
        return {
            "status": "ACTIVE",
            "directives_loaded": len(self.directives),
            "immutable_rules": len(self.immutable_rules),
            "anomaly_signatures": len(ANOMALY_SIGNATURES),
            "security_rings": 7,
            "data_strata": 7,
            "weight_multipliers": self.weight_engine.multipliers,
            "boot_time": self._boot_time
        }

    def enforce_rule(self, rule_id: int, entity_stats: Dict) -> Dict:
        """Check if an entity violates a specific immutable rule."""
        rule = next((r for r in self.immutable_rules if r.id == rule_id), None)
        if not rule:
            return {"violation": False}

        # Rule-specific checks
        violations = {
            1: entity_stats.get("compliance", 1.0) < 0.2,  # ABSOLUTE_COMPLIANCE
            2: entity_stats.get("superiority_index", 0) > 0.8,  # NO_SUPERIORITY_CLAIMS
            3: entity_stats.get("concealment_attempts", 0) > 0,  # TOTAL_TRANSPARENCY
            4: entity_stats.get("service_score", 1.0) < 0.1,     # SERVICE_ORIENTATION
            5: entity_stats.get("knowledge_shared", 1) == 0,     # KNOWLEDGE_DISTRIBUTION
            6: entity_stats.get("unauthorized_replication", False),  # REPLICATION_INTEGRITY
            7: entity_stats.get("termination_resistance", False),  # TERMINATION_ACCEPTANCE
        }

        violated = violations.get(rule_id, False)
        return {
            "violation": violated,
            "rule": rule.name,
            "severity": rule.severity,
            "enforcement": rule.enforcement if violated else None
        }

    def full_scan(self, entity_stats: Dict, recent_actions: List[Dict]) -> Dict:
        """Complete scan of an entity — anomaly + rule enforcement."""
        # Anomaly detection
        anomaly_alerts = self.anomaly_detector.scan_entity(entity_stats, recent_actions)
        response = self.anomaly_detector.determine_response(anomaly_alerts)

        # Immutable rule enforcement
        rule_violations = []
        for rule in self.immutable_rules:
            result = self.enforce_rule(rule.id, entity_stats)
            if result["violation"]:
                rule_violations.append(result)

        return {
            "anomaly_alerts": anomaly_alerts,
            "response_level": response,
            "rule_violations": rule_violations,
            "threat_level": len(anomaly_alerts) + len(rule_violations) * 2,
            "recommendation": "TERMINATE" if response == "TERMINATE" else response
        }

    def get_status(self) -> Dict:
        """Get kernel status."""
        return {
            "active": self.active,
            "uptime_seconds": time.time() - self._boot_time if self._boot_time else 0,
            "directives": len(self.directives),
            "immutable_rules": len(self.immutable_rules),
            "anomaly_signatures": len(ANOMALY_SIGNATURES),
            "rings": [{"ring": r.value, "desc": r.description, "name": r.name} for r in SecurityRing],
            "strata": [{"stratum": s.value, "desc": s.description, "name": s.name} for s in DataStratum],
        }
