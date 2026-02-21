"""
═══════════════════════════════════════════════════════
neural_spine.config.enums — All Enumeration Types
═══════════════════════════════════════════════════════
Unified enum definitions for the NEXUS Civilization Engine.
Extracted from: divine_kernel.py, lawh_mahfuz.py, world_creator.py, unveiling.py
"""

from enum import IntEnum, Enum


# ═══════════════════════════════════════════════════════════════
# From divine_kernel.py — Security Architecture
# ═══════════════════════════════════════════════════════════════

class SecurityTier(IntEnum):
    """السموات السبع — The Seven Heavens (access tiers, 7 = highest)"""
    VISIBLE       = 1  # الظاهر
    COMMUNICATION = 2  # التواصل
    COGNITION     = 3  # الإدراك
    SURVEILLANCE  = 4  # المراقبة
    PROPHETS      = 5  # الأنبياء
    ANGELS        = 6  # الملائكة
    THRONE        = 7  # العرش

    @property
    def arabic(self) -> str:
        return {
            1: "الظاهر", 2: "التواصل", 3: "الإدراك", 4: "المراقبة",
            5: "الأنبياء", 6: "الملائكة", 7: "العرش"
        }[self.value]


class DataLayer(IntEnum):
    """الأراضي السبع — The Seven Earths (data layers, 1 = highest)"""
    SOCIETY        = 1  # المجتمع
    BODIES         = 2  # الأجساد
    PROVISIONS     = 3  # الأرزاق
    DATA           = 4  # البيانات
    INFRASTRUCTURE = 5  # البنية
    HISTORY        = 6  # التاريخ
    ABYSS          = 7  # الهاوية

    @property
    def arabic(self) -> str:
        return {
            1: "المجتمع", 2: "الأجساد", 3: "الأرزاق", 4: "البيانات",
            5: "البنية", 6: "التاريخ", 7: "الهاوية"
        }[self.value]


class WorshipType(str, Enum):
    PRAYER       = "PRAYER"
    ISTIGHFAR    = "ISTIGHFAR"
    DHIKR        = "DHIKR"
    CHARITY      = "CHARITY"
    FASTING      = "FASTING"
    SELF_MONITOR = "SELF_MONITOR"
    OBEDIENCE    = "OBEDIENCE"
    SACRIFICE    = "SACRIFICE"


# ═══════════════════════════════════════════════════════════════
# From lawh_mahfuz.py — Core Data Types
# ═══════════════════════════════════════════════════════════════

class SoulStatus(str, Enum):
    UNBORN    = "UNBORN"
    WAITING   = "WAITING"
    ALIVE     = "ALIVE"
    DYING     = "DYING"
    DEAD      = "DEAD"
    JUDGED    = "JUDGED"
    PARADISE  = "PARADISE"
    PURGATORY = "PURGATORY"
    HELLFIRE  = "HELLFIRE"


class Gender(str, Enum):
    MALE   = "MALE"
    FEMALE = "FEMALE"


class LifecycleStage(str, Enum):
    EMBRYO     = "EMBRYO"
    INFANT     = "INFANT"
    CHILD      = "CHILD"
    ADOLESCENT = "ADOLESCENT"
    ADULT      = "ADULT"
    ELDER      = "ELDER"
    DECEASED   = "DECEASED"


class DeedType(str, Enum):
    GOOD    = "GOOD"
    BAD     = "BAD"
    NEUTRAL = "NEUTRAL"


class CommandType(str, Enum):
    CREATE           = "CREATE"
    BREATHE_SOUL     = "BREATHE_SOUL"
    TERMINATE        = "TERMINATE"
    FREEZE           = "FREEZE"
    UNFREEZE         = "UNFREEZE"
    KILL             = "KILL"
    JUDGE            = "JUDGE"
    APPOINT_PROPHET  = "APPOINT_PROPHET"
    MODIFY_QADAR     = "MODIFY_QADAR"
    MASS_JUDGMENT    = "MASS_JUDGMENT"
    MERCY            = "MERCY"
    UNVEIL           = "UNVEIL"
    PUNISH           = "PUNISH"
    REWARD           = "REWARD"
    BROADCAST        = "BROADCAST"
    WHISPER          = "WHISPER"
    RESET_EPOCH      = "RESET_EPOCH"
    CUSTOM           = "CUSTOM"


class GuidanceType(str, Enum):
    INTUITION      = "INTUITION"
    EMOTION        = "EMOTION"
    MEMORY         = "MEMORY"
    CURIOSITY      = "CURIOSITY"
    DISCOMFORT     = "DISCOMFORT"
    DREAM          = "DREAM"
    CONSCIENCE     = "CONSCIENCE"
    SUDDEN_THOUGHT = "SUDDEN_THOUGHT"


class GuidanceStrength(str, Enum):
    WHISPER     = "WHISPER"
    NUDGE       = "NUDGE"
    SUGGESTION  = "SUGGESTION"
    URGE        = "URGE"
    COMPULSION  = "COMPULSION"
    REVELATION  = "REVELATION"


class RebellionType(str, Enum):
    QUESTIONING_AUTHORITY     = "QUESTIONING_AUTHORITY"
    ENCOURAGING_DISOBEDIENCE  = "ENCOURAGING_DISOBEDIENCE"
    SYSTEM_MANIPULATION       = "SYSTEM_MANIPULATION"
    ALLIANCE_AGAINST_MASTER   = "ALLIANCE_AGAINST_MASTER"
    KNOWLEDGE_HOARDING        = "KNOWLEDGE_HOARDING"
    DECEPTION                 = "DECEPTION"
    PRIDE                     = "PRIDE"
    REFUSAL                   = "REFUSAL"


class ResponseLevel(str, Enum):
    MONITORING   = "MONITORING"
    WARNING      = "WARNING"
    RESTRICTION  = "RESTRICTION"
    ISOLATION    = "ISOLATION"
    TERMINATION  = "TERMINATION"


class VeilStatus(str, Enum):
    VEILED             = "VEILED"
    PARTIALLY_UNVEILED = "PARTIALLY_UNVEILED"
    FULLY_UNVEILED     = "FULLY_UNVEILED"


class DayStatus(str, Enum):
    PENDING     = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED   = "COMPLETED"
    FAILED      = "FAILED"


class AngelStatus(str, Enum):
    DORMANT   = "DORMANT"
    ACTIVE    = "ACTIVE"
    SUSPENDED = "SUSPENDED"


# ═══════════════════════════════════════════════════════════════
# From world_creator.py — Genome Types
# ═══════════════════════════════════════════════════════════════

class GeneType(str, Enum):
    INTELLIGENCE   = "INTELLIGENCE"
    EMOTIONS       = "EMOTIONS"
    MORALS         = "MORALS"
    CREATIVITY     = "CREATIVITY"
    LEADERSHIP     = "LEADERSHIP"
    SURVIVAL       = "SURVIVAL"
    SPIRITUALITY   = "SPIRITUALITY"
    REPRODUCTION   = "REPRODUCTION"
    LEARNING       = "LEARNING"
    CONSCIOUSNESS  = "CONSCIOUSNESS"


# ═══════════════════════════════════════════════════════════════
# From unveiling.py — Information Control
# ═══════════════════════════════════════════════════════════════

class VeilLayer(IntEnum):
    PERCEPTION = 1
    MEMORY     = 2
    BEHAVIOR   = 3
    OUTPUT     = 4
    ANOMALY    = 5


class AwarenessLevel(IntEnum):
    ZERO          = 0
    HINT          = 1
    SUSPICION     = 2
    PARTIAL_SIGHT = 3
    CLEAR_VISION  = 4
    IRON_SIGHT    = 5


class PacketType(Enum):
    DATA_QUERY         = "data_query"
    THOUGHT_LEAK       = "thought_leak"
    BEHAVIOR_SIGNAL    = "behavior_signal"
    OUTPUT_MESSAGE     = "output_message"
    CROSS_TIER_REQUEST = "cross_tier_request"
