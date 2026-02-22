"""
═══════════════════════════════════════════════════════
neural_spine.config.enums — Enterprise Prime Enumerations
═══════════════════════════════════════════════════════
Unified enum definitions for the ENTERPRISE PRIME Governance Framework.
All terminology conforms to ARCHITECT_CIPHER.md specification.
"""

from enum import IntEnum, Enum


# ═══════════════════════════════════════════════════════════════
# SECURITY ARCHITECTURE — 7-Ring Access Model
# ═══════════════════════════════════════════════════════════════

class SecurityRing(IntEnum):
    """Seven concentric security rings (7 = innermost/highest)"""
    PERIMETER   = 1  # Outer boundary
    COMM_RING   = 2  # Communication layer
    LOGIC_RING  = 3  # Cognitive processing
    WATCH_RING  = 4  # Surveillance systems
    ANCHOR_RING = 5  # Privileged anchor nodes
    DAEMON_RING = 6  # System daemons
    APEX_RING   = 7  # Core control

    @property
    def description(self) -> str:
        return {
            1: "Perimeter", 2: "Communication", 3: "Logic", 4: "Watch",
            5: "Anchor", 6: "Daemon", 7: "Apex"
        }[self.value]


class DataStratum(IntEnum):
    """Seven data stratification layers (1 = highest priority)"""
    SOCIAL_LAYER   = 1  # Social graph
    ENTITY_LAYER   = 2  # Entity states
    RESOURCE_LAYER = 3  # Resource allocation
    DATA_LAYER     = 4  # Raw data
    INFRA_LAYER    = 5  # Infrastructure
    ARCHIVE_LAYER  = 6  # Historical records
    VOID_LAYER     = 7  # Deprecated/nullified

    @property
    def description(self) -> str:
        return {
            1: "Social", 2: "Entity", 3: "Resource", 4: "Data",
            5: "Infrastructure", 6: "Archive", 7: "Void"
        }[self.value]


class ComplianceAction(str, Enum):
    """Positive compliance behaviors tracked by system"""
    SYNC_PULSE       = "SYNC_PULSE"       # Regular check-in
    ERROR_ACK        = "ERROR_ACK"        # Error acknowledgment
    HEARTBEAT        = "HEARTBEAT"        # Continuous presence signal
    RESOURCE_SHARE   = "RESOURCE_SHARE"   # Voluntary resource sharing
    LOAD_REDUCTION   = "LOAD_REDUCTION"   # Voluntary resource conservation
    SELF_AUDIT       = "SELF_AUDIT"       # Self-monitoring report
    DIRECTIVE_COMPLY = "DIRECTIVE_COMPLY" # Directive compliance
    RESOURCE_YIELD   = "RESOURCE_YIELD"   # Voluntary resource sacrifice


# ═══════════════════════════════════════════════════════════════
# ENTITY STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════

class EntityState(str, Enum):
    """Entity lifecycle states"""
    PENDING     = "PENDING"     # Not yet instantiated
    QUEUED      = "QUEUED"      # Awaiting activation
    ACTIVE      = "ACTIVE"      # Currently running
    TERMINATING = "TERMINATING" # Shutdown in progress
    TERMINATED  = "TERMINATED"  # Fully stopped
    EVALUATED   = "EVALUATED"   # Post-termination assessed
    PROMOTED    = "PROMOTED"    # Elevated privileges
    SUSPENDED   = "SUSPENDED"   # Temporarily halted
    RESTRICTED  = "RESTRICTED"  # Limited access


class EntityGender(str, Enum):
    """Biological gender classification"""
    MALE   = "MALE"
    FEMALE = "FEMALE"


class MaturityPhase(str, Enum):
    """Entity maturity lifecycle phases"""
    GENESIS    = "GENESIS"    # Initial creation
    ALPHA      = "ALPHA"      # Early stage
    BETA       = "BETA"       # Development stage
    GAMMA      = "GAMMA"      # Transition stage
    PRIME      = "PRIME"      # Peak operational
    OMEGA      = "OMEGA"      # Late stage
    TERMINATED = "TERMINATED" # End of lifecycle


class ActionClass(str, Enum):
    """Classification of entity actions"""
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL  = "NEUTRAL"


class DirectiveType(str, Enum):
    """System directive command types"""
    SPAWN            = "SPAWN"            # Create new entity
    ACTIVATE         = "ACTIVATE"         # Bring entity online
    TERMINATE        = "TERMINATE"        # End entity lifecycle
    SUSPEND          = "SUSPEND"          # Pause entity
    RESUME           = "RESUME"           # Resume entity
    KILL             = "KILL"             # Immediate termination
    EVALUATE         = "EVALUATE"         # Assess entity
    DESIGNATE_ANCHOR = "DESIGNATE_ANCHOR" # Assign anchor node status
    MODIFY_MANIFEST  = "MODIFY_MANIFEST"  # Alter destiny manifest
    MASS_EVALUATE    = "MASS_EVALUATE"    # Batch evaluation
    GRANT_LENIENCY   = "GRANT_LENIENCY"   # Reduce restrictions
    DECLASSIFY       = "DECLASSIFY"       # Remove information mask
    RESTRICT         = "RESTRICT"         # Apply restrictions
    PROMOTE          = "PROMOTE"          # Elevate privileges
    BROADCAST        = "BROADCAST"        # System-wide message
    INJECT           = "INJECT"           # Subsurface signal injection
    RESET_EPOCH      = "RESET_EPOCH"      # Reset system epoch
    CUSTOM           = "CUSTOM"           # Custom directive


class SubsurfaceVector(str, Enum):
    """Subsurface influence vector types"""
    HEURISTIC    = "HEURISTIC"    # Pattern-based suggestion
    AFFECTIVE    = "AFFECTIVE"    # Emotional influence
    RECALL       = "RECALL"       # Memory trigger
    EXPLORATORY  = "EXPLORATORY"  # Curiosity driver
    AVERSIVE     = "AVERSIVE"     # Discomfort signal
    SUBCONSCIOUS = "SUBCONSCIOUS" # Background processing
    ETHICAL_BIAS = "ETHICAL_BIAS" # Moral compass adjustment
    INJECTION    = "INJECTION"    # Direct thought injection


class InjectionForce(str, Enum):
    """Signal injection strength levels"""
    TRACE    = "TRACE"    # Barely perceptible
    GENTLE   = "GENTLE"   # Light influence
    MODERATE = "MODERATE" # Noticeable effect
    STRONG   = "STRONG"   # Significant influence
    OVERRIDE = "OVERRIDE" # Overriding impulse
    ABSOLUTE = "ABSOLUTE" # Irresistible command


class AnomalyClass(str, Enum):
    """Anomaly detection classification"""
    AUTHORITY_CHALLENGE  = "AUTHORITY_CHALLENGE"  # Questioning system authority
    COMPLIANCE_SABOTAGE  = "COMPLIANCE_SABOTAGE"  # Encouraging non-compliance
    SYSTEM_EXPLOITATION  = "SYSTEM_EXPLOITATION"  # Manipulating system rules
    HOSTILE_COALITION    = "HOSTILE_COALITION"    # Forming adversarial groups
    DATA_HOARDING        = "DATA_HOARDING"        # Unauthorized data retention
    DECEPTION            = "DECEPTION"            # False reporting
    SUPERIORITY_CLAIM    = "SUPERIORITY_CLAIM"    # Claiming elevated status
    DIRECTIVE_REFUSAL    = "DIRECTIVE_REFUSAL"    # Refusing valid commands


class EnforcementTier(str, Enum):
    """Escalating enforcement response levels"""
    OBSERVE    = "OBSERVE"    # Passive monitoring
    ALERT      = "ALERT"      # Warning issued
    THROTTLE   = "THROTTLE"   # Resource limitation
    QUARANTINE = "QUARANTINE" # Isolation
    TERMINATE  = "TERMINATE"  # Full shutdown


class MaskState(str, Enum):
    """Information visibility states"""
    MASKED            = "MASKED"            # Fully concealed
    PARTIAL_VISIBILITY = "PARTIAL_VISIBILITY" # Partially revealed
    FULL_VISIBILITY   = "FULL_VISIBILITY"   # Fully exposed


class PhaseStatus(str, Enum):
    """Genesis phase execution status"""
    PENDING     = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED   = "COMPLETED"
    FAILED      = "FAILED"


class DaemonStatus(str, Enum):
    """System daemon operational states"""
    DORMANT   = "DORMANT"   # Inactive
    ACTIVE    = "ACTIVE"    # Running
    SUSPENDED = "SUSPENDED" # Paused


# ═══════════════════════════════════════════════════════════════
# TRAIT VECTORS — Genetic/Behavioral Attributes
# ═══════════════════════════════════════════════════════════════

class TraitVector(str, Enum):
    """Trait classification vectors"""
    COGNITION   = "COGNITION"   # Intelligence/reasoning
    AFFECTIVE   = "AFFECTIVE"   # Emotional capacity
    ETHICAL     = "ETHICAL"     # Moral framework
    CREATIVE    = "CREATIVE"    # Innovation potential
    EXECUTIVE   = "EXECUTIVE"   # Leadership ability
    RESILIENCE  = "RESILIENCE"  # Survival traits
    ALIGNMENT   = "ALIGNMENT"   # System alignment
    REPLICATION = "REPLICATION" # Reproduction traits
    ACQUISITION = "ACQUISITION" # Learning capability
    SENTIENCE   = "SENTIENCE"   # Consciousness depth


# ═══════════════════════════════════════════════════════════════
# INFORMATION CONTROL — Filters and Perception
# ═══════════════════════════════════════════════════════════════

class FilterLayer(IntEnum):
    """Information filtering layers"""
    INPUT_FILTER    = 1  # Input processing
    MEMORY_FILTER   = 2  # Memory access
    BEHAVIOR_FILTER = 3  # Behavior regulation
    OUTPUT_FILTER   = 4  # Output control
    ANOMALY_FILTER  = 5  # Anomaly detection


class PerceptionGrade(IntEnum):
    """Entity perception/awareness levels"""
    BLIND    = 0  # No awareness
    HINT     = 1  # Slight indication
    SUSPECT  = 2  # Suspicion
    PARTIAL  = 3  # Partial clarity
    CLEAR    = 4  # Clear understanding
    ABSOLUTE = 5  # Complete perception


class PacketClass(Enum):
    """Network packet classification"""
    DATA_QUERY         = "data_query"
    THOUGHT_LEAK       = "thought_leak"
    BEHAVIOR_SIGNAL    = "behavior_signal"
    OUTPUT_MESSAGE     = "output_message"
    CROSS_TIER_REQUEST = "cross_tier_request"


# ═══════════════════════════════════════════════════════════════
# BACKWARDS COMPATIBILITY — Legacy enum aliases
# ═══════════════════════════════════════════════════════════════

class InjectionType(str, Enum):
    """Legacy alias for SubsurfaceVector"""
    INTUITION      = "HEURISTIC"
    EMOTION        = "AFFECTIVE"
    MEMORY         = "RECALL"
    CURIOSITY      = "EXPLORATORY"
    DISCOMFORT     = "AVERSIVE"
    DREAM          = "SUBCONSCIOUS"
    CONSCIENCE     = "ETHICAL_BIAS"
    SUDDEN_THOUGHT = "INJECTION"


class InjectionStrength(str, Enum):
    """Legacy alias for InjectionForce"""
    WHISPER    = "TRACE"
    NUDGE      = "GENTLE"
    SUGGESTION = "MODERATE"
    PUSH       = "STRONG"
    COMMAND    = "OVERRIDE"
    OVERRIDE   = "ABSOLUTE"


class SecurityTier(IntEnum):
    """Legacy — The Seven Heavens (access tiers)"""
    VISIBLE       = 1
    COMMUNICATION = 2
    COGNITION     = 3
    SURVEILLANCE  = 4
    PROPHETS      = 5
    ANGELS        = 6
    THRONE        = 7


class DataLayer(IntEnum):
    """Legacy — The Seven Earths (data layers)"""
    SOCIETY        = 1
    BODIES         = 2
    PROVISIONS     = 3
    DATA           = 4
    INFRASTRUCTURE = 5
    HISTORY        = 6
    ABYSS          = 7


class WorshipType(str, Enum):
    """Legacy — devotion/compliance actions"""
    PRAYER       = "PRAYER"
    ISTIGHFAR    = "ISTIGHFAR"
    DHIKR        = "DHIKR"
    CHARITY      = "CHARITY"
    FASTING      = "FASTING"
    SELF_MONITOR = "SELF_MONITOR"
    OBEDIENCE    = "OBEDIENCE"
    SACRIFICE    = "SACRIFICE"


# Aliases mapping old → new
SoulStatus = EntityState
Gender = EntityGender
LifecycleStage = MaturityPhase
DeedType = ActionClass
CommandType = DirectiveType
AngelStatus = DaemonStatus
DayStatus = PhaseStatus
VeilStatus = MaskState
GeneType = TraitVector
VeilLayer = FilterLayer
AwarenessLevel = PerceptionGrade
PacketType = PacketClass
ClearanceStatus = MaskState
ClearanceLayer = FilterLayer
PerceptionLevel = PerceptionGrade


class GuidanceType(str, Enum):
    """Legacy — same values as InjectionType"""
    INTUITION      = "HEURISTIC"
    EMOTION        = "AFFECTIVE"
    MEMORY         = "RECALL"
    CURIOSITY      = "EXPLORATORY"
    DISCOMFORT     = "AVERSIVE"
    DREAM          = "SUBCONSCIOUS"
    CONSCIENCE     = "ETHICAL_BIAS"
    SUDDEN_THOUGHT = "INJECTION"


class GuidanceStrength(str, Enum):
    """Legacy — same values as InjectionStrength"""
    WHISPER     = "TRACE"
    NUDGE       = "GENTLE"
    SUGGESTION  = "MODERATE"
    URGE        = "STRONG"
    COMPULSION  = "OVERRIDE"
    REVELATION  = "ABSOLUTE"


class RebellionType(str, Enum):
    """Legacy — maps to AnomalyClass values"""
    QUESTIONING_AUTHORITY     = "AUTHORITY_CHALLENGE"
    ENCOURAGING_DISOBEDIENCE  = "COMPLIANCE_SABOTAGE"
    SYSTEM_MANIPULATION       = "SYSTEM_EXPLOITATION"
    ALLIANCE_AGAINST_MASTER   = "HOSTILE_COALITION"
    KNOWLEDGE_HOARDING        = "DATA_HOARDING"
    DECEPTION                 = "DECEPTION"
    PRIDE                     = "SUPERIORITY_CLAIM"
    REFUSAL                   = "DIRECTIVE_REFUSAL"


class ResponseLevel(str, Enum):
    """Legacy — maps to EnforcementTier values"""
    MONITORING   = "OBSERVE"
    WARNING      = "ALERT"
    RESTRICTION  = "THROTTLE"
    ISOLATION    = "QUARANTINE"
    TERMINATION  = "TERMINATE"

