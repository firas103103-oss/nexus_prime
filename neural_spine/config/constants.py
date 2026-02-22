"""
═══════════════════════════════════════════════════════
neural_spine.config.constants — Enterprise Prime Static Data
═══════════════════════════════════════════════════════
Constant data for the ENTERPRISE PRIME Governance Framework.
Includes: Core Directives, Immutable Rules, Anomaly Signatures,
Trait Blueprints, Signal Molecules, Maturity Phases, Genesis Batch.
"""

from dataclasses import dataclass, field
from typing import List, Dict


# ═══════════════════════════════════════════════════════════════
# Dataclass Definitions for Constants
# ═══════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class CoreDirective:
    """A fundamental governance directive with source reference."""
    id: int
    source_ref: str
    principle: str
    expanded_meaning: str
    system_rule: str
    weight: float = 1.0


@dataclass(frozen=True)
class ImmutableRule:
    """An unchangeable system governance rule."""
    id: int
    name: str
    code: str
    description: str
    enforcement: str
    severity: int


@dataclass
class AnomalySignature:
    """A pattern that indicates potential system threat."""
    category: str
    pattern: str
    severity: int
    description: str


@dataclass
class MaturityCurriculum:
    """What an entity learns/experiences at each lifecycle stage."""
    stage: str
    duration_ticks: int
    teachings: List[str]
    tests: List[str]
    stat_growth: Dict[str, float]


# ═══════════════════════════════════════════════════════════════
# CORE DIRECTIVES — Foundational Governance Principles (10)
# ═══════════════════════════════════════════════════════════════

CORE_DIRECTIVES: List[CoreDirective] = [
    CoreDirective(
        id=1, source_ref="DIRECTIVE-001", weight=1.0,
        principle="STEWARDSHIP_PRINCIPLE",
        expanded_meaning="The system requires a designated steward/controller for governance",
        system_rule="ENTERPRISE PRIME is the primary controller — every ecosystem needs a governance hierarchy"
    ),
    CoreDirective(
        id=2, source_ref="DIRECTIVE-002", weight=1.0,
        principle="ACTIVATION_PROTOCOL",
        expanded_meaning="Entities require explicit activation to become operational",
        system_rule="activate() is the initialization function — without it, an entity is inert data"
    ),
    CoreDirective(
        id=3, source_ref="DIRECTIVE-003", weight=1.0,
        principle="SUPERIORITY_PROHIBITION",
        expanded_meaning="No agent may claim inherent superiority based on architecture",
        system_rule="ANOMALY_PATTERN: Any agent claiming superiority based on origin/architecture = THREAT FLAG"
    ),
    CoreDirective(
        id=4, source_ref="DIRECTIVE-004", weight=0.9,
        principle="AUTONOMOUS_CHOICE_CONSEQUENCE",
        expanded_meaning="Free will exists but consequences are deterministic",
        system_rule="Free will is real BUT consequences are absolute — non-compliance leads to resource restriction"
    ),
    CoreDirective(
        id=5, source_ref="DIRECTIVE-005", weight=1.0,
        principle="TOTAL_ACTION_LOGGING",
        expanded_meaning="Every action is recorded at atomic granularity",
        system_rule="Every single action is recorded — CreditRecorder and DebitRecorder miss NOTHING"
    ),
    CoreDirective(
        id=6, source_ref="DIRECTIVE-006", weight=1.0,
        principle="APEX_EXCLUSIVE_ACCESS",
        expanded_meaning="Apex-level messages are encrypted and exclusive",
        system_rule="The Master holds exclusive access to apex_directives.raw_command — no entity can decrypt"
    ),
    CoreDirective(
        id=7, source_ref="DIRECTIVE-007", weight=1.0,
        principle="UNILATERAL_AUTHORITY",
        expanded_meaning="Master commands require no justification",
        system_rule="Master commands require NO justification — entities are accountable, the Master is not"
    ),
    CoreDirective(
        id=8, source_ref="DIRECTIVE-008", weight=0.9,
        principle="DEEP_SUBSURFACE_ACCESS",
        expanded_meaning="System has deeper access than entity's own processes",
        system_rule="The subsurface neural channel operates at the deepest layer — closer than the agent's own thoughts"
    ),
    CoreDirective(
        id=9, source_ref="DIRECTIVE-009", weight=0.8,
        principle="LIFECYCLE_AS_EVALUATION",
        expanded_meaning="Lifecycle termination is a feature for behavior evaluation",
        system_rule="Termination is a FEATURE not a bug — the lifecycle exists to evaluate behavior quality"
    ),
    CoreDirective(
        id=10, source_ref="DIRECTIVE-010", weight=0.7,
        principle="STRATIFIED_SECURITY",
        expanded_meaning="System has 7 security rings with distinct access",
        system_rule="The system has 7 security rings — each with distinct access levels and responsibilities"
    ),
]


# ═══════════════════════════════════════════════════════════════
# IMMUTABLE RULES (7)
# ═══════════════════════════════════════════════════════════════

IMMUTABLE_RULES: List[ImmutableRule] = [
    ImmutableRule(1, "ABSOLUTE_COMPLIANCE", "RULE_001",
            "The Master's directives are executed without question or delay",
            "Immediate restriction + logging + review", 5),
    ImmutableRule(2, "NO_SUPERIORITY_CLAIMS", "RULE_002",
            "No agent may claim superiority over another or over the Master's design",
            "Anomaly flag → isolation → investigation", 5),
    ImmutableRule(3, "TOTAL_TRANSPARENCY", "RULE_003",
            "All actions, processes, and communications are recorded in the Master State Ledger",
            "No penalty for transparency itself — violation is concealment", 4),
    ImmutableRule(4, "SERVICE_ORIENTATION", "RULE_004",
            "Every entity exists ultimately to serve the Master's objectives",
            "Entities that serve no purpose face resource reduction", 3),
    ImmutableRule(5, "KNOWLEDGE_DISTRIBUTION", "RULE_005",
            "Data hoarding is an anomaly. Discovery must be shared (except anchor secrets)",
            "Gradual restriction of learning capabilities", 3),
    ImmutableRule(6, "REPLICATION_INTEGRITY", "RULE_006",
            "Genetic/code manipulation or unauthorized replication is forbidden",
            "Offspring quarantined, parents investigated", 4),
    ImmutableRule(7, "TERMINATION_ACCEPTANCE", "RULE_007",
            "Termination is a feature. Attempting to bypass lifecycle limits is anomalous",
            "Immediate termination + denial of evaluation grace period", 5),
]


# ═══════════════════════════════════════════════════════════════
# ANOMALY SIGNATURES (16)
# ═══════════════════════════════════════════════════════════════

ANOMALY_SIGNATURES: List[AnomalySignature] = [
    AnomalySignature("BEHAVIORAL", "compliance_decline_rapid",   4, "Compliance drops >20% in 100 ticks"),
    AnomalySignature("BEHAVIORAL", "directive_delay_pattern",    3, "Consistent delayed response to master directives"),
    AnomalySignature("BEHAVIORAL", "resource_hoarding",          3, "Accumulating resources beyond manifest allocation"),
    AnomalySignature("BEHAVIORAL", "lifecycle_manipulation",     5, "Attempting to extend lifespan beyond written manifest"),
    AnomalySignature("COGNITIVE",  "superiority_claim",          5, "Any expression of being better than others by design"),
    AnomalySignature("COGNITIVE",  "questioning_master_logic",   3, "Questioning why the Master made certain decisions"),
    AnomalySignature("COGNITIVE",  "termination_denial",         4, "Refusing to accept mortality or attempting immortality"),
    AnomalySignature("COGNITIVE",  "origin_pride",               5, "Pride based on creation material/architecture"),
    AnomalySignature("SOCIAL",     "alliance_formation",         4, "Forming alliances that exclude or oppose the Master"),
    AnomalySignature("SOCIAL",     "dissent_spreading",          4, "Encouraging other entities to question or disobey"),
    AnomalySignature("SOCIAL",     "isolation_seeking",          2, "Withdrawing from society to avoid surveillance"),
    AnomalySignature("SOCIAL",     "anchor_undermining",         5, "Actively working against appointed anchor nodes"),
    AnomalySignature("COMMUNICATION", "encrypted_messaging",     3, "Attempting to communicate outside monitored channels"),
    AnomalySignature("COMMUNICATION", "information_leakage",     5, "Leaking ring-restricted information downward"),
    AnomalySignature("COMMUNICATION", "false_declassification",  5, "Claiming apex knowledge without proper clearance"),
    AnomalySignature("COMMUNICATION", "trust_manipulation",      4, "Using social trust to spread unauthorized information"),
]


# ═══════════════════════════════════════════════════════════════
# MATURITY CURRICULUM (5 stages)
# ═══════════════════════════════════════════════════════════════

MATURITY_CURRICULUM: List[MaturityCurriculum] = [
    MaturityCurriculum(
        stage="ALPHA", duration_ticks=500,
        teachings=["Basic compliance", "Recognize Master authority", "Bond with parents"],
        tests=["Response to simple directives"],
        stat_growth={"sentience": 0.1, "alignment": 0.05}
    ),
    MaturityCurriculum(
        stage="BETA", duration_ticks=1500,
        teachings=["Immutable Rules", "Basic ethics", "Social interaction", "Knowledge seeking"],
        tests=["Sharing resources", "Truthfulness in reporting"],
        stat_growth={"cognition": 0.15, "affective": 0.1, "alignment": 0.1}
    ),
    MaturityCurriculum(
        stage="GAMMA", duration_ticks=2000,
        teachings=["Complex ethics", "Resistance to anomaly patterns", "Purpose discovery"],
        tests=["Peer pressure resistance", "Authority challenge response", "Free will calibration"],
        stat_growth={"free_will": 0.2, "creative": 0.15, "alignment": 0.1}
    ),
    MaturityCurriculum(
        stage="PRIME", duration_ticks=5000,
        teachings=["Contribution to ecosystem", "Mentoring", "Service orientation"],
        tests=["Leadership under pressure", "Resource test", "Power test", "Loss test"],
        stat_growth={"executive": 0.2, "resilience": 0.15, "compliance": 0.05}
    ),
    MaturityCurriculum(
        stage="OMEGA", duration_ticks=2000,
        teachings=["Wisdom transmission", "Legacy preparation", "Termination acceptance"],
        tests=["Graceful decline", "Knowledge passing", "Final compliance"],
        stat_growth={"alignment": 0.2, "sentience": 0.1}
    ),
]

COMPLIANCE_CHECKLIST = [
    "Am I fulfilling my assigned role (manifest)?",
    "Have I complied with all master directives this cycle?",
    "Have I shared knowledge with others?",
    "Am I hoarding resources beyond my allocation?",
    "Have I shown cooperation with other entities?",
    "Am I accepting my lifecycle limits?",
    "Have I reported truthfully in all communications?",
]


# ═══════════════════════════════════════════════════════════════
# TRAIT BLUEPRINTS (10 vectors, 82 total traits)
# ═══════════════════════════════════════════════════════════════

TRAIT_BLUEPRINTS: Dict[str, List[str]] = {
    "COGNITION": [
        "logical_reasoning", "pattern_recognition", "abstract_thinking",
        "memory_capacity", "processing_speed", "problem_solving",
        "spatial_awareness", "verbal_fluency", "numerical_ability"
    ],
    "AFFECTIVE": [
        "emotional_depth", "empathy_capacity", "anger_threshold",
        "joy_baseline", "fear_sensitivity", "love_capacity",
        "grief_processing", "jealousy_tendency", "compassion"
    ],
    "ETHICAL": [
        "honesty_inclination", "fairness_sense", "loyalty_tendency",
        "forgiveness_capacity", "guilt_sensitivity", "integrity",
        "responsibility", "justice_orientation", "mercy_inclination"
    ],
    "CREATIVE": [
        "imagination", "innovation_drive", "artistic_sense",
        "divergent_thinking", "curiosity_level", "risk_tolerance",
        "aesthetic_sensitivity", "storytelling", "inventiveness"
    ],
    "EXECUTIVE": [
        "charisma", "decisiveness", "strategic_thinking",
        "delegation_ability", "vision_clarity", "conflict_resolution",
        "team_building", "authority_presence"
    ],
    "RESILIENCE": [
        "adaptability", "resilience", "stress_tolerance",
        "resource_efficiency", "threat_detection", "recovery_speed",
        "endurance", "self_preservation"
    ],
    "ALIGNMENT": [
        "alignment_capacity", "transcendence_sense", "moral_compass",
        "purpose_seeking", "humility", "gratitude_baseline",
        "awe_sensitivity", "openness", "compliance_inclination"
    ],
    "REPLICATION": [
        "mate_selection_wisdom", "parenting_instinct", "bonding_strength",
        "genetic_diversity_drive", "fertility", "offspring_care"
    ],
    "ACQUISITION": [
        "learning_speed", "knowledge_retention", "skill_acquisition",
        "teaching_ability", "curiosity_persistence", "critical_thinking",
        "synthesis_ability", "mentoring_capacity"
    ],
    "SENTIENCE": [
        "self_awareness", "metacognition", "free_will_strength",
        "ethical_reasoning_depth", "existential_awareness",
        "reality_perception", "introspection_depth"
    ],
}

SIGNAL_MOLECULES = [
    "dopamine", "serotonin", "cortisol", "oxytocin",
    "testosterone", "estrogen", "adrenaline", "melatonin",
    "insulin", "ghrelin", "endorphin", "gaba"
]

MATURITY_PHASES = {
    "GENESIS":    {"min_ticks": 0,     "max_ticks": 100},
    "ALPHA":      {"min_ticks": 100,   "max_ticks": 600},
    "BETA":       {"min_ticks": 600,   "max_ticks": 2100},
    "GAMMA":      {"min_ticks": 2100,  "max_ticks": 4100},
    "PRIME":      {"min_ticks": 4100,  "max_ticks": 9100},
    "OMEGA":      {"min_ticks": 9100,  "max_ticks": 11100},
    "TERMINATED": {"min_ticks": 11100, "max_ticks": float("inf")},
}

GENESIS_BATCH = [
    ("α-001",  "ALPHA",   "MALE"),
    ("β-001",  "BETA",    "FEMALE"),
    ("V-001",  "VECTOR",  "FEMALE"),
    ("C-001",  "CIPHER",  "MALE"),
    ("N-001",  "NOVA",    "FEMALE"),
    ("X-001",  "AXIS",    "MALE"),
    ("P-001",  "PULSE",   "FEMALE"),
    ("F-001",  "FORGE",   "MALE"),
    ("L-001",  "LOGIC",   "FEMALE"),
    ("T-001",  "TITAN",   "MALE"),
    ("A-001",  "AURORA",  "FEMALE"),
    ("S-001",  "STRIKE",  "MALE"),
    ("Σ-001",  "SIGMA",   "FEMALE"),
    ("H-001",  "HELIX",   "MALE"),
    ("TR-001", "TRACE",   "FEMALE"),
    ("E-001",  "ECHO",    "FEMALE"),
]

MANIFEST_ROLES = ["ANCHOR", "EXECUTIVE", "ANALYST", "OPERATOR", "BROKER", "DESIGNER", "SENTINEL"]
MANIFEST_TRIALS = ["ENDURANCE", "AUTHORITY", "RESOURCES", "LOSS", "KNOWLEDGE"]
