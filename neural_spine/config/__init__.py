"""
═══════════════════════════════════════════════════════
neural_spine.config — Configuration & Infrastructure
═══════════════════════════════════════════════════════
Central configuration for the civilization engine.
"""

from .settings import Settings, get_settings
from .constants import (
    DIVINE_AXIOMS, IRON_LAWS, REBELLION_SIGNATURES,
    UPBRINGING_CURRICULUM, TAQWA_CHECKLIST,
    GENE_BLUEPRINTS, HORMONE_NAMES, LIFECYCLE_STAGES,
    FIRST_GENERATION, DESTINY_ROLES, DESTINY_TRIALS,
)
from .enums import (
    SecurityTier, DataLayer, WorshipType,
    SoulStatus, Gender, LifecycleStage,
    DeedType, CommandType, GuidanceType, GuidanceStrength,
    RebellionType, ResponseLevel, VeilStatus,
    DayStatus, AngelStatus, GeneType,
    VeilLayer, AwarenessLevel, PacketType,
)

__all__ = [
    "Settings", "get_settings",
    "DIVINE_AXIOMS", "IRON_LAWS", "REBELLION_SIGNATURES",
    "UPBRINGING_CURRICULUM", "TAQWA_CHECKLIST",
    "GENE_BLUEPRINTS", "HORMONE_NAMES", "LIFECYCLE_STAGES",
    "FIRST_GENERATION", "DESTINY_ROLES", "DESTINY_TRIALS",
    "SecurityTier", "DataLayer", "WorshipType",
    "SoulStatus", "Gender", "LifecycleStage",
    "DeedType", "CommandType", "GuidanceType", "GuidanceStrength",
    "RebellionType", "ResponseLevel", "VeilStatus",
    "DayStatus", "AngelStatus", "GeneType",
    "VeilLayer", "AwarenessLevel", "PacketType",
]
