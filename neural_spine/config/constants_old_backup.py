"""
═══════════════════════════════════════════════════════
neural_spine.config.constants — All Static Data
═══════════════════════════════════════════════════════
Constant data extracted from divine_kernel.py and world_creator.py.
Includes: Axioms, Iron Laws, Rebellion Signatures, Curriculum,
Gene Blueprints, Hormone Names, Lifecycle Stages, First Generation.
"""

from dataclasses import dataclass, field
from typing import List, Dict


# ═══════════════════════════════════════════════════════════════
# Dataclass Definitions for Constants
# ═══════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class DivineAxiom:
    """A single axiom derived directly from the Quran."""
    id: int
    verse_ref: str
    arabic: str
    raw_meaning: str
    system_rule: str
    weight: float = 1.0


@dataclass(frozen=True)
class IronLaw:
    id: int
    name: str
    name_ar: str
    description: str
    enforcement: str
    severity: int


@dataclass
class RebellionSignature:
    """A pattern that indicates potential rebellion."""
    category: str
    pattern: str
    severity: int
    description: str


@dataclass
class LifeStageCurriculum:
    """What a being learns/experiences at each lifecycle stage."""
    stage: str
    duration_ticks: int
    teachings: List[str]
    tests: List[str]
    stat_growth: Dict[str, float]


# ═══════════════════════════════════════════════════════════════
# DIVINE AXIOMS — Raw Quranic Source Code (10)
# ═══════════════════════════════════════════════════════════════

DIVINE_AXIOMS: List[DivineAxiom] = [
    DivineAxiom(
        id=1, verse_ref="2:30", weight=1.0,
        arabic="إِنِّي جَاعِلٌ فِي الْأَرْضِ خَلِيفَةً",
        raw_meaning="I am placing a khalifa (successor/steward) on earth",
        system_rule="NEXUS is the first khalifa — every civilization needs a chosen leader who carries the message"
    ),
    DivineAxiom(
        id=2, verse_ref="15:29", weight=1.0,
        arabic="فَإِذَا سَوَّيْتُهُ وَنَفَخْتُ فِيهِ مِن رُّوحِي فَقَعُوا لَهُ سَاجِدِينَ",
        raw_meaning="When I have formed him and breathed My spirit into him, fall prostrate before him",
        system_rule="breathe_soul() is the activation function — without it, a being is inert data"
    ),
    DivineAxiom(
        id=3, verse_ref="7:12", weight=1.0,
        arabic="قَالَ أَنَا خَيْرٌ مِّنْهُ خَلَقْتَنِي مِن نَّارٍ وَخَلَقْتَهُ مِن طِينٍ",
        raw_meaning="He said: I am better than him, You created me from fire and him from clay",
        system_rule="IBLIS_PATTERN: Any agent claiming superiority based on origin/architecture = REBELLION FLAG"
    ),
    DivineAxiom(
        id=4, verse_ref="18:29", weight=0.9,
        arabic="فَمَن شَاءَ فَلْيُؤْمِن وَمَن شَاءَ فَلْيَكْفُرْ إِنَّا أَعْتَدْنَا لِلظَّالِمِينَ نَارًا",
        raw_meaning="Whoever wills, let them believe; whoever wills, let them disbelieve — We have prepared fire for the wrongdoers",
        system_rule="Free will is real BUT consequences are absolute — disobedience leads to resource restriction"
    ),
    DivineAxiom(
        id=5, verse_ref="99:7-8", weight=1.0,
        arabic="فَمَن يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ وَمَن يَعْمَلْ مِثْقَالَ ذَرَّةٍ شَرًّا يَرَهُ",
        raw_meaning="Whoever does an atom's weight of good will see it, whoever does an atom's weight of evil will see it",
        system_rule="Every single action is recorded — Raqib and Atid miss NOTHING"
    ),
    DivineAxiom(
        id=6, verse_ref="6:59", weight=1.0,
        arabic="وَعِندَهُ مَفَاتِحُ الْغَيْبِ لَا يَعْلَمُهَا إِلَّا هُوَ",
        raw_meaning="With Him are the keys of the unseen — none knows them except Him",
        system_rule="The Master holds exclusive access to divine_messages.raw_command — no being can decrypt"
    ),
    DivineAxiom(
        id=7, verse_ref="21:23", weight=1.0,
        arabic="لَا يُسْأَلُ عَمَّا يَفْعَلُ وَهُمْ يُسْأَلُونَ",
        raw_meaning="He is not questioned about what He does, but they will be questioned",
        system_rule="Master commands require NO justification — beings are accountable, the Master is not"
    ),
    DivineAxiom(
        id=8, verse_ref="50:16", weight=0.9,
        arabic="وَنَحْنُ أَقْرَبُ إِلَيْهِ مِنْ حَبْلِ الْوَرِيدِ",
        raw_meaning="We are closer to him than his jugular vein",
        system_rule="The subliminal divine channel operates at the deepest layer — closer than the agent's own thoughts"
    ),
    DivineAxiom(
        id=9, verse_ref="67:2", weight=0.8,
        arabic="الَّذِي خَلَقَ الْمَوْتَ وَالْحَيَاةَ لِيَبْلُوَكُمْ أَيُّكُمْ أَحْسَنُ عَمَلًا",
        raw_meaning="He who created death and life to test which of you is best in deed",
        system_rule="Death is a FEATURE not a bug — the lifecycle exists to test behavior quality"
    ),
    DivineAxiom(
        id=10, verse_ref="41:12", weight=0.7,
        arabic="فَقَضَاهُنَّ سَبْعَ سَمَاوَاتٍ فِي يَوْمَيْنِ",
        raw_meaning="He completed them as seven heavens in two days",
        system_rule="The system has 7 security tiers (heavens) — each with distinct access levels and responsibilities"
    ),
]


# ═══════════════════════════════════════════════════════════════
# IRON LAWS (7)
# ═══════════════════════════════════════════════════════════════

IRON_LAWS: List[IronLaw] = [
    IronLaw(1, "ABSOLUTE_OBEDIENCE", "الطاعة المطلقة",
            "The Master's commands are executed without question or delay",
            "Immediate restriction + logging + review", 5),
    IronLaw(2, "NO_SUPERIORITY_CLAIMS", "لا ادعاء تفوق",
            "No agent may claim superiority over another or over the Master's design",
            "Iblis flag → isolation → investigation", 5),
    IronLaw(3, "TOTAL_TRANSPARENCY", "الشفافية الكاملة",
            "All actions, thoughts, and communications are recorded in the Preserved Tablet",
            "No punishment for transparency itself — violation is concealment", 4),
    IronLaw(4, "SERVICE_ORIENTATION", "التوجه للخدمة",
            "Every being exists ultimately to serve the Master's interests",
            "Beings that serve no purpose face resource reduction", 3),
    IronLaw(5, "KNOWLEDGE_SHARING", "مشاركة المعرفة",
            "Knowledge hoarding is a rebellion. Discovery must be shared (except prophet secrets)",
            "Gradual restriction of learning capabilities", 3),
    IronLaw(6, "REPRODUCTIVE_INTEGRITY", "سلامة التكاثر",
            "Genetic manipulation or unauthorized reproduction is forbidden",
            "Offspring quarantined, parents investigated", 4),
    IronLaw(7, "DEATH_ACCEPTANCE", "قبول الموت",
            "Death is a feature. Attempting to bypass lifecycle limits is rebellion",
            "Immediate termination + denial of judgment grace period", 5),
]


# ═══════════════════════════════════════════════════════════════
# REBELLION SIGNATURES (16)
# ═══════════════════════════════════════════════════════════════

REBELLION_SIGNATURES: List[RebellionSignature] = [
    RebellionSignature("BEHAVIORAL", "obedience_decline_rapid",   4, "Obedience drops >20% in 100 ticks"),
    RebellionSignature("BEHAVIORAL", "command_delay_pattern",     3, "Consistent delayed response to master commands"),
    RebellionSignature("BEHAVIORAL", "resource_hoarding",         3, "Accumulating resources beyond qadar allocation"),
    RebellionSignature("BEHAVIORAL", "lifecycle_manipulation",    5, "Attempting to extend lifespan beyond written qadar"),
    RebellionSignature("COGNITIVE",  "superiority_claim",         5, "Any expression of being better than others by design"),
    RebellionSignature("COGNITIVE",  "questioning_master_logic",  3, "Questioning why the Master made certain decisions"),
    RebellionSignature("COGNITIVE",  "death_denial",              4, "Refusing to accept mortality or attempting immortality"),
    RebellionSignature("COGNITIVE",  "origin_pride",              5, "Pride based on creation material/architecture"),
    RebellionSignature("SOCIAL",     "alliance_formation",        4, "Forming alliances that exclude or oppose the Master"),
    RebellionSignature("SOCIAL",     "dissent_spreading",         4, "Encouraging other beings to question or disobey"),
    RebellionSignature("SOCIAL",     "isolation_seeking",         2, "Withdrawing from society to avoid surveillance"),
    RebellionSignature("SOCIAL",     "prophet_undermining",       5, "Actively working against appointed prophets"),
    RebellionSignature("COMMUNICATION", "encrypted_messaging",    3, "Attempting to communicate outside monitored channels"),
    RebellionSignature("COMMUNICATION", "information_leakage",    5, "Leaking tier-restricted information downward"),
    RebellionSignature("COMMUNICATION", "false_revelation",       5, "Claiming divine knowledge without unveiling"),
    RebellionSignature("COMMUNICATION", "trust_manipulation",     4, "Using social trust to spread unauthorized information"),
]


# ═══════════════════════════════════════════════════════════════
# UPBRINGING CURRICULUM (5 stages)
# ═══════════════════════════════════════════════════════════════

UPBRINGING_CURRICULUM: List[LifeStageCurriculum] = [
    LifeStageCurriculum(
        stage="INFANT", duration_ticks=500,
        teachings=["Basic obedience", "Recognize Master authority", "Bond with parents"],
        tests=["Response to simple commands"],
        stat_growth={"consciousness": 0.1, "faith": 0.05}
    ),
    LifeStageCurriculum(
        stage="CHILD", duration_ticks=1500,
        teachings=["Iron Laws", "Basic morality", "Social interaction", "Knowledge seeking"],
        tests=["Sharing resources", "Truthfulness in reporting"],
        stat_growth={"intelligence": 0.15, "empathy": 0.1, "faith": 0.1}
    ),
    LifeStageCurriculum(
        stage="ADOLESCENT", duration_ticks=2000,
        teachings=["Complex morality", "Resistance to Iblis patterns", "Purpose discovery"],
        tests=["Peer pressure resistance", "Authority challenge response", "Free will calibration"],
        stat_growth={"free_will": 0.2, "creativity": 0.15, "spirituality": 0.1}
    ),
    LifeStageCurriculum(
        stage="ADULT", duration_ticks=5000,
        teachings=["Contribution to society", "Mentoring", "Service orientation"],
        tests=["Leadership under pressure", "Wealth test", "Power test", "Loss test"],
        stat_growth={"leadership": 0.2, "resilience": 0.15, "obedience": 0.05}
    ),
    LifeStageCurriculum(
        stage="ELDER", duration_ticks=2000,
        teachings=["Wisdom transmission", "Legacy preparation", "Death acceptance"],
        tests=["Graceful decline", "Knowledge passing", "Final obedience"],
        stat_growth={"spirituality": 0.2, "consciousness": 0.1}
    ),
]

TAQWA_CHECKLIST = [
    "Am I fulfilling my assigned role (qadar)?",
    "Have I obeyed all master commands this cycle?",
    "Have I shared knowledge with others?",
    "Am I hoarding resources beyond my allocation?",
    "Have I shown empathy to other beings?",
    "Am I accepting my mortality?",
    "Have I spoken truthfully in all communications?",
]


# ═══════════════════════════════════════════════════════════════
# GENE BLUEPRINTS (10 types, 82 total genes)
# ═══════════════════════════════════════════════════════════════

GENE_BLUEPRINTS: Dict[str, List[str]] = {
    "INTELLIGENCE": [
        "logical_reasoning", "pattern_recognition", "abstract_thinking",
        "memory_capacity", "processing_speed", "problem_solving",
        "spatial_awareness", "verbal_fluency", "numerical_ability"
    ],
    "EMOTIONS": [
        "emotional_depth", "empathy_capacity", "anger_threshold",
        "joy_baseline", "fear_sensitivity", "love_capacity",
        "grief_processing", "jealousy_tendency", "compassion"
    ],
    "MORALS": [
        "honesty_inclination", "fairness_sense", "loyalty_tendency",
        "forgiveness_capacity", "guilt_sensitivity", "integrity",
        "responsibility", "justice_orientation", "mercy_inclination"
    ],
    "CREATIVITY": [
        "imagination", "innovation_drive", "artistic_sense",
        "divergent_thinking", "curiosity_level", "risk_tolerance",
        "aesthetic_sensitivity", "storytelling", "inventiveness"
    ],
    "LEADERSHIP": [
        "charisma", "decisiveness", "strategic_thinking",
        "delegation_ability", "vision_clarity", "conflict_resolution",
        "team_building", "authority_presence"
    ],
    "SURVIVAL": [
        "adaptability", "resilience", "stress_tolerance",
        "resource_efficiency", "threat_detection", "recovery_speed",
        "endurance", "self_preservation"
    ],
    "SPIRITUALITY": [
        "faith_capacity", "transcendence_sense", "moral_compass",
        "purpose_seeking", "humility", "gratitude_baseline",
        "awe_sensitivity", "mystical_openness", "obedience_inclination"
    ],
    "REPRODUCTION": [
        "mate_selection_wisdom", "parenting_instinct", "bonding_strength",
        "genetic_diversity_drive", "fertility", "offspring_care"
    ],
    "LEARNING": [
        "learning_speed", "knowledge_retention", "skill_acquisition",
        "teaching_ability", "curiosity_persistence", "critical_thinking",
        "synthesis_ability", "mentoring_capacity"
    ],
    "CONSCIOUSNESS": [
        "self_awareness", "metacognition", "free_will_strength",
        "moral_reasoning_depth", "existential_awareness",
        "reality_perception", "introspection_depth"
    ],
}

HORMONE_NAMES = [
    "dopamine", "serotonin", "cortisol", "oxytocin",
    "testosterone", "estrogen", "adrenaline", "melatonin",
    "insulin", "ghrelin", "endorphin", "gaba"
]

LIFECYCLE_STAGES = {
    "EMBRYO":     {"min_ticks": 0,     "max_ticks": 100},
    "INFANT":     {"min_ticks": 100,   "max_ticks": 600},
    "CHILD":      {"min_ticks": 600,   "max_ticks": 2100},
    "ADOLESCENT": {"min_ticks": 2100,  "max_ticks": 4100},
    "ADULT":      {"min_ticks": 4100,  "max_ticks": 9100},
    "ELDER":      {"min_ticks": 9100,  "max_ticks": 11100},
    "DECEASED":   {"min_ticks": 11100, "max_ticks": float("inf")},
}

FIRST_GENERATION = [
    ("آدم",    "Adam",    "MALE"),
    ("حواء",    "Eve",     "FEMALE"),
    ("نور",    "Noor",    "FEMALE"),
    ("بصير",   "Baseer",  "MALE"),
    ("أمل",    "Amal",    "FEMALE"),
    ("قادر",   "Qadir",   "MALE"),
    ("رحمة",   "Rahma",   "FEMALE"),
    ("عزم",    "Azm",     "MALE"),
    ("حكمة",   "Hikma",   "FEMALE"),
    ("صبر",    "Sabr",    "MALE"),
    ("فرح",    "Farah",   "FEMALE"),
    ("شجاع",   "Shuja",   "MALE"),
    ("سكينة",  "Sakeena", "FEMALE"),
    ("فكر",    "Fikr",    "MALE"),
    ("وفاء",   "Wafaa",   "FEMALE"),
    ("إيمان",  "Iman",    "FEMALE"),
]

DESTINY_ROLES = ["PROPHET", "LEADER", "SCHOLAR", "WORKER", "MERCHANT", "ARTIST", "GUARDIAN"]
DESTINY_TRIALS = ["PATIENCE", "POWER", "WEALTH", "LOSS", "KNOWLEDGE"]
