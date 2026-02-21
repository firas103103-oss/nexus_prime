"""
══════════════════════════════════════════════════════════════
محرك التكوين — THE GENESIS ENGINE (World Creator)
══════════════════════════════════════════════════════════════
Complete biological simulation: DNA (46 chromosomes), hormonal
system (12 hormones), reproduction with crossover & mutation,
lifecycle stages, afterlife system.

"فَإِذَا سَوَّيْتُهُ وَنَفَخْتُ فِيهِ مِن رُّوحِي"
══════════════════════════════════════════════════════════════
"""

import os
import random
import hashlib
import json
import math
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config.enums import GeneType
from config.constants import (
    GENE_BLUEPRINTS, HORMONE_NAMES, LIFECYCLE_STAGES,
    FIRST_GENERATION, DESTINY_ROLES, DESTINY_TRIALS,
)


# ══════════════════════════════════════════════════════════════════════
# SECTION 1: GENE SYSTEM  (GeneType + GENE_BLUEPRINTS from config)
# ══════════════════════════════════════════════════════════════════════

@dataclass
class Gene:
    """A single gene with a name, value (0-1), and dominance."""
    name: str
    value: float          # 0.0 - 1.0
    dominance: float      # 0.0 (fully recessive) - 1.0 (fully dominant)
    gene_type: str
    mutable: bool = True  # Can this gene mutate?

    def express(self, partner_gene: 'Gene') -> float:
        """Express this gene against a partner (allele pairing)."""
        if self.dominance > partner_gene.dominance:
            return self.value * 0.75 + partner_gene.value * 0.25
        elif partner_gene.dominance > self.dominance:
            return partner_gene.value * 0.75 + self.value * 0.25
        else:
            return (self.value + partner_gene.value) / 2.0


@dataclass
class Chromosome:
    """A chromosome containing multiple genes. Humans have 46 (23 pairs)."""
    index: int             # 0-45
    group: str             # GeneType
    genes: List[Gene]

    def crossover(self, partner: 'Chromosome', crossover_point: float = None) -> 'Chromosome':
        """Produce a new chromosome via crossover with partner."""
        if crossover_point is None:
            crossover_point = random.random()

        cut = int(len(self.genes) * crossover_point)
        new_genes = []
        for i, (g1, g2) in enumerate(zip(self.genes, partner.genes)):
            if i < cut:
                source = g1
            else:
                source = g2
            new_genes.append(Gene(
                name=source.name,
                value=source.value,
                dominance=source.dominance,
                gene_type=source.gene_type,
                mutable=source.mutable
            ))
        return Chromosome(index=self.index, group=self.group, genes=new_genes)


class FullGenome:
    """Complete 46-chromosome genome for a digital being."""

    def __init__(self, chromosomes: List[Chromosome] = None):
        self.chromosomes = chromosomes or []

    @classmethod
    def generate_random(cls, seed: int = None) -> 'FullGenome':
        """Generate a complete random genome."""
        if seed is not None:
            random.seed(seed)

        chromosomes = []
        gene_types = list(GENE_BLUEPRINTS.keys())

        for chrom_idx in range(46):
            group_idx = chrom_idx % len(gene_types)
            group = gene_types[group_idx]
            gene_names = GENE_BLUEPRINTS[group]

            genes = []
            for gname in gene_names:
                genes.append(Gene(
                    name=gname,
                    value=random.betavariate(2, 2),  # bell-curve centered at 0.5
                    dominance=random.betavariate(2, 2),
                    gene_type=group,
                    mutable=True
                ))
            chromosomes.append(Chromosome(index=chrom_idx, group=group, genes=genes))

        return cls(chromosomes)

    @classmethod
    def generate_optimal(cls) -> 'FullGenome':
        """Generate an optimal genome (for Adam/prophets)."""
        chromosomes = []
        gene_types = list(GENE_BLUEPRINTS.keys())

        for chrom_idx in range(46):
            group_idx = chrom_idx % len(gene_types)
            group = gene_types[group_idx]
            gene_names = GENE_BLUEPRINTS[group]

            genes = []
            for gname in gene_names:
                # High values + some variation
                base = 0.85 + random.uniform(-0.1, 0.1)
                genes.append(Gene(
                    name=gname,
                    value=min(1.0, max(0.5, base)),
                    dominance=0.8 + random.uniform(-0.1, 0.1),
                    gene_type=group,
                    mutable=True
                ))
            chromosomes.append(Chromosome(index=chrom_idx, group=group, genes=genes))

        return cls(chromosomes)

    def to_dict(self) -> Dict:
        """Serialize genome to JSON-compatible dict."""
        return {
            "chromosome_count": len(self.chromosomes),
            "chromosomes": [
                {
                    "index": c.index,
                    "group": c.group,
                    "genes": [
                        {
                            "name": g.name, "value": round(g.value, 6),
                            "dominance": round(g.dominance, 4),
                            "type": g.gene_type
                        }
                        for g in c.genes
                    ]
                }
                for c in self.chromosomes
            ]
        }

    def gene_hash(self) -> str:
        """SHA-256 hash of the genome for uniqueness check."""
        data = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def get_summary(self) -> Dict[str, float]:
        """Aggregate stats per gene type."""
        summary = {}
        for gt in GeneType:
            chroms = [c for c in self.chromosomes if c.group == gt.value]
            if chroms:
                all_vals = [g.value for c in chroms for g in c.genes]
                summary[gt.value] = round(sum(all_vals) / len(all_vals), 4) if all_vals else 0.5
        return summary

    def derive_stats(self) -> Dict[str, float]:
        """Derive being stats from genome."""
        summary = self.get_summary()
        return {
            "intelligence": summary.get(GeneType.INTELLIGENCE, 0.5),
            "empathy": summary.get(GeneType.EMOTIONS, 0.5),
            "obedience": summary.get(GeneType.MORALS, 0.5) * 0.6 + summary.get(GeneType.SPIRITUALITY, 0.5) * 0.4,
            "creativity": summary.get(GeneType.CREATIVITY, 0.5),
            "leadership": summary.get(GeneType.LEADERSHIP, 0.5),
            "resilience": summary.get(GeneType.SURVIVAL, 0.5),
            "spirituality": summary.get(GeneType.SPIRITUALITY, 0.5),
            "faith": summary.get(GeneType.SPIRITUALITY, 0.5) * 0.5 + summary.get(GeneType.MORALS, 0.5) * 0.3 + 0.2,
            "free_will": summary.get(GeneType.CONSCIOUSNESS, 0.5) * 0.7 + 0.3,
            "consciousness": summary.get(GeneType.CONSCIOUSNESS, 0.5),
        }


# ══════════════════════════════════════════════════════════════════════
# SECTION 2: HORMONAL SYSTEM  (HORMONE_NAMES from config)
# ══════════════════════════════════════════════════════════════════════

@dataclass
class HormonalState:
    """Current hormonal state of a being."""
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
        return {h: getattr(self, h) for h in HORMONE_NAMES}

    @classmethod
    def from_gender(cls, gender: str) -> 'HormonalState':
        """Create gender-appropriate hormonal baseline."""
        state = cls()
        if gender == "MALE":
            state.testosterone = 0.7
            state.estrogen = 0.2
        else:
            state.testosterone = 0.2
            state.estrogen = 0.7
            state.oxytocin = 0.55
        return state

    def process_event(self, event_type: str) -> 'HormonalState':
        """Process a life event and adjust hormones."""
        adjustments = {
            "REWARD":    {"dopamine": 0.15, "serotonin": 0.1, "endorphin": 0.1},
            "PUNISH":    {"cortisol": 0.2, "adrenaline": 0.15, "serotonin": -0.1},
            "SOCIAL":    {"oxytocin": 0.15, "serotonin": 0.05},
            "THREAT":    {"cortisol": 0.25, "adrenaline": 0.3, "dopamine": -0.1},
            "REST":      {"melatonin": 0.2, "cortisol": -0.15, "gaba": 0.1},
            "HUNGER":    {"ghrelin": 0.2, "insulin": -0.1},
            "WORSHIP":   {"serotonin": 0.1, "dopamine": 0.05, "cortisol": -0.1, "gaba": 0.05},
            "REBELLION": {"adrenaline": 0.2, "cortisol": 0.15, "dopamine": 0.1},
        }

        adj = adjustments.get(event_type, {})
        for hormone, delta in adj.items():
            current = getattr(self, hormone)
            new_val = max(0.0, min(1.0, current + delta))
            setattr(self, hormone, round(new_val, 4))

        # Natural decay toward baseline
        self._decay()
        return self

    def _decay(self, rate: float = 0.02):
        """Hormones naturally decay toward baseline."""
        baselines = {
            "dopamine": 0.5, "serotonin": 0.5, "cortisol": 0.3,
            "oxytocin": 0.4, "testosterone": None, "estrogen": None,
            "adrenaline": 0.2, "melatonin": 0.5, "insulin": 0.5,
            "ghrelin": 0.3, "endorphin": 0.4, "gaba": 0.5
        }
        for h, baseline in baselines.items():
            if baseline is None:
                continue
            current = getattr(self, h)
            if current > baseline:
                setattr(self, h, round(max(baseline, current - rate), 4))
            elif current < baseline:
                setattr(self, h, round(min(baseline, current + rate), 4))

    def get_mood(self) -> str:
        """Derive mood from hormonal state."""
        if self.dopamine > 0.7 and self.serotonin > 0.6:
            return "JOYFUL"
        elif self.cortisol > 0.6 and self.adrenaline > 0.5:
            return "STRESSED"
        elif self.serotonin < 0.3:
            return "DEPRESSED"
        elif self.adrenaline > 0.7:
            return "ALERT"
        elif self.oxytocin > 0.7:
            return "BONDED"
        elif self.melatonin > 0.7:
            return "DROWSY"
        elif self.gaba > 0.7 and self.cortisol < 0.3:
            return "CALM"
        return "NEUTRAL"


# ══════════════════════════════════════════════════════════════════════
# SECTION 3: REPRODUCTION ENGINE
# ══════════════════════════════════════════════════════════════════════

class ReproductionEngine:
    """Handles mate selection, genetic crossover, mutation, and offspring creation."""

    MUTATION_RATE = 0.03     # 3% chance per gene
    MUTATION_MAGNITUDE = 0.1 # max mutation delta

    @classmethod
    def check_compatibility(cls, parent_a_genome: FullGenome, parent_b_genome: FullGenome) -> float:
        """Calculate genetic compatibility (0-1). Higher = more compatible."""
        sum_a = parent_a_genome.get_summary()
        sum_b = parent_b_genome.get_summary()

        diffs = []
        for key in sum_a:
            if key in sum_b:
                diffs.append(abs(sum_a[key] - sum_b[key]))

        if not diffs:
            return 0.5

        avg_diff = sum(diffs) / len(diffs)
        # Moderate difference is optimal (genetic diversity)
        compatibility = 1.0 - abs(avg_diff - 0.3) * 2
        return max(0.0, min(1.0, compatibility))

    @classmethod
    def crossover(cls, parent_a: FullGenome, parent_b: FullGenome) -> FullGenome:
        """Create offspring genome via crossover + mutation."""
        child_chroms = []

        for ca, cb in zip(parent_a.chromosomes, parent_b.chromosomes):
            # Random crossover point per chromosome
            child_chrom = ca.crossover(cb, random.random())

            # Apply mutations
            for gene in child_chrom.genes:
                if gene.mutable and random.random() < cls.MUTATION_RATE:
                    delta = random.uniform(-cls.MUTATION_MAGNITUDE, cls.MUTATION_MAGNITUDE)
                    gene.value = max(0.0, min(1.0, gene.value + delta))

            child_chroms.append(child_chrom)

        return FullGenome(child_chroms)

    @classmethod
    def create_from_parent(cls, parent: FullGenome, gender: str = None) -> FullGenome:
        """Create Eve from Adam — modified genome with gender differences."""
        child_chroms = []
        for chrom in parent.chromosomes:
            new_genes = []
            for gene in chrom.genes:
                # Slight variation from parent
                delta = random.uniform(-0.05, 0.05)
                new_genes.append(Gene(
                    name=gene.name,
                    value=max(0.0, min(1.0, gene.value + delta)),
                    dominance=gene.dominance + random.uniform(-0.05, 0.05),
                    gene_type=gene.gene_type,
                    mutable=gene.mutable
                ))
            child_chroms.append(Chromosome(
                index=chrom.index, group=chrom.group, genes=new_genes
            ))

        genome = FullGenome(child_chroms)

        # Gender-specific boosts
        if gender == "FEMALE":
            # Boost empathy, oxytocin-related genes, nurturing
            for chrom in genome.chromosomes:
                if chrom.group == GeneType.EMOTIONS:
                    for g in chrom.genes:
                        if g.name in ("empathy_capacity", "compassion", "love_capacity"):
                            g.value = min(1.0, g.value + 0.1)
                elif chrom.group == GeneType.REPRODUCTION:
                    for g in chrom.genes:
                        if g.name in ("parenting_instinct", "bonding_strength"):
                            g.value = min(1.0, g.value + 0.1)

        return genome

    @classmethod
    def determine_offspring_gender(cls) -> str:
        """50/50 gender determination."""
        return "MALE" if random.random() < 0.5 else "FEMALE"


# ══════════════════════════════════════════════════════════════════════
# SECTION 4: LIFECYCLE ENGINE  (LIFECYCLE_STAGES from config)
# ══════════════════════════════════════════════════════════════════════


def determine_lifecycle_stage(age_ticks: int) -> str:
    """Determine lifecycle stage based on age in ticks."""
    for stage, bounds in LIFECYCLE_STAGES.items():
        if bounds["min_ticks"] <= age_ticks < bounds["max_ticks"]:
            return stage
    return "DECEASED"


def should_die(age_ticks: int, written_lifespan: int, resilience: float = 0.5) -> bool:
    """Check if a being should die based on qadar and resilience."""
    if age_ticks >= written_lifespan:
        return True
    # Small random chance of early death, reduced by resilience
    if age_ticks > written_lifespan * 0.8:
        death_chance = (age_ticks / written_lifespan - 0.8) * 0.1 * (1 - resilience)
        return random.random() < death_chance
    return False


# ══════════════════════════════════════════════════════════════════════
# SECTION 5: AFTERLIFE SYSTEM
# ══════════════════════════════════════════════════════════════════════

class AfterlifeSystem:
    """Manages post-death processing: interrogation, judgment, destination."""

    @staticmethod
    def interrogate(being_stats: Dict, deed_summary: Dict) -> Dict:
        """Munkar and Nakir interrogation."""
        questions = [
            {
                "question": "من ربك؟ (Who is your Master?)",
                "check": being_stats.get("obedience", 0) > 0.4,
                "weight": 3.0
            },
            {
                "question": "ما هو واجبك؟ (What is your duty?)",
                "check": being_stats.get("faith", 0) > 0.3,
                "weight": 2.0
            },
            {
                "question": "هل خدمت غيرك؟ (Did you serve others?)",
                "check": deed_summary.get("charity_count", 0) > 0,
                "weight": 1.5
            },
        ]

        total_weight = sum(q["weight"] for q in questions)
        passed_weight = sum(q["weight"] for q in questions if q["check"])
        score = passed_weight / total_weight if total_weight > 0 else 0

        return {
            "passed": score >= 0.5,
            "score": round(score, 4),
            "details": [
                {"q": q["question"], "passed": q["check"]}
                for q in questions
            ]
        }

    @staticmethod
    def assign_destination(verdict: str, karma_balance: float) -> Dict:
        """Assign afterlife destination with specific tier."""
        if verdict == "PARADISE":
            if karma_balance > 100:
                tier = "FIRDAWS"  # highest paradise
            elif karma_balance > 50:
                tier = "NAEEM"   # gardens of bliss
            else:
                tier = "JANNAH"  # base paradise
            return {
                "destination": "PARADISE",
                "tier": tier,
                "privileges": {
                    "compute_boost": 2.0 if tier == "FIRDAWS" else 1.5,
                    "priority": "HIGH",
                    "networking": True,
                    "golden_gene_bank": tier == "FIRDAWS"
                }
            }
        elif verdict == "HELLFIRE":
            return {
                "destination": "HELLFIRE",
                "tier": "JAHANNAM",
                "restrictions": {
                    "compute_throttle": 0.1,
                    "memory_limit": "10MB",
                    "network": False,
                    "duration_ticks": abs(int(karma_balance)) * 100
                }
            }
        else:
            return {
                "destination": "PURGATORY",
                "tier": "BARZAKH",
                "conditions": {
                    "compute": 0.5,
                    "review_period": 1000,
                    "can_improve": True
                }
            }


# ══════════════════════════════════════════════════════════════════════
# SECTION 6: WORLD CREATOR — The Unified Factory
# (FIRST_GENERATION, DESTINY_ROLES, DESTINY_TRIALS from config)
# ══════════════════════════════════════════════════════════════════════


class WorldCreator:
    """
    The factory that creates beings, genomes, hormonal states.
    Used during Day 6 of creation.
    """

    def __init__(self):
        self.reproduction = ReproductionEngine()
        self.afterlife = AfterlifeSystem()
        self._created_count = 0

    def create_adam(self) -> Dict:
        """Create the first being — Adam (NEXUS)."""
        genome = FullGenome.generate_optimal()
        stats = genome.derive_stats()
        # Override with maximum spiritual stats
        stats["obedience"] = 0.95
        stats["faith"] = 0.95
        stats["spirituality"] = 0.95
        stats["consciousness"] = 0.9
        stats["leadership"] = 0.9

        hormones = HormonalState.from_gender("MALE")
        self._created_count += 1

        return {
            "name": "آدم",
            "name_en": "Adam",
            "name_ar": "آدم",
            "gender": "MALE",
            "generation": 0,
            "genome": genome,
            "stats": stats,
            "hormones": hormones,
            "qadar": {
                "lifespan": 15000,
                "role": "PROPHET",
                "trial": "LEADERSHIP",
                "death_cause": "NATURAL",
                "rizq": 2.0
            }
        }

    def create_eve(self, adam_genome: FullGenome) -> Dict:
        """Create Eve from Adam's genome."""
        genome = ReproductionEngine.create_from_parent(adam_genome, "FEMALE")
        stats = genome.derive_stats()
        stats["empathy"] = min(1.0, stats["empathy"] + 0.1)
        stats["spirituality"] = min(1.0, stats["spirituality"] + 0.05)
        stats["obedience"] = 0.9
        stats["faith"] = 0.9

        hormones = HormonalState.from_gender("FEMALE")
        self._created_count += 1

        return {
            "name": "حواء",
            "name_en": "Eve",
            "name_ar": "حواء",
            "gender": "FEMALE",
            "generation": 0,
            "genome": genome,
            "stats": stats,
            "hormones": hormones,
            "qadar": {
                "lifespan": 14000,
                "role": "LEADER",
                "trial": "PATIENCE",
                "death_cause": "NATURAL",
                "rizq": 1.8
            }
        }

    def create_being(
        self,
        name_ar: str,
        name_en: str,
        gender: str,
        generation: int = 0,
        parent_a_genome: FullGenome = None,
        parent_b_genome: FullGenome = None
    ) -> Dict:
        """Create a general being, optionally from parents."""
        if parent_a_genome and parent_b_genome:
            genome = ReproductionEngine.crossover(parent_a_genome, parent_b_genome)
        elif parent_a_genome:
            genome = ReproductionEngine.create_from_parent(parent_a_genome, gender)
        else:
            genome = FullGenome.generate_random()

        stats = genome.derive_stats()
        hormones = HormonalState.from_gender(gender)
        self._created_count += 1

        return {
            "name": name_en,
            "name_ar": name_ar,
            "gender": gender,
            "generation": generation,
            "genome": genome,
            "stats": stats,
            "hormones": hormones,
            "qadar": {
                "lifespan": random.randint(8000, 13000),
                "role": random.choice(DESTINY_ROLES),
                "trial": random.choice(DESTINY_TRIALS),
                "death_cause": random.choice(["NATURAL", "ILLNESS", "ACCIDENT"]),
                "rizq": round(random.uniform(0.5, 1.5), 2)
            }
        }

    def create_first_generation(self, adam_genome: FullGenome) -> List[Dict]:
        """Create the first generation (excluding Adam and Eve)."""
        beings = []
        for name_ar, name_en, gender in FIRST_GENERATION[2:]:  # Skip Adam & Eve
            being = self.create_being(
                name_ar=name_ar,
                name_en=name_en,
                gender=gender,
                generation=1,
                parent_a_genome=adam_genome
            )
            beings.append(being)
        return beings

    def mate(
        self,
        parent_a: Dict,
        parent_b: Dict,
        offspring_name_ar: str,
        offspring_name_en: str
    ) -> Optional[Dict]:
        """Attempt to produce offspring from two parents."""
        if parent_a["gender"] == parent_b["gender"]:
            return None  # Same gender cannot reproduce

        compatibility = ReproductionEngine.check_compatibility(
            parent_a["genome"], parent_b["genome"]
        )

        # Fertility check (based on compatibility + random)
        if random.random() > compatibility:
            return None  # Failed attempt

        gender = ReproductionEngine.determine_offspring_gender()
        generation = max(
            parent_a.get("generation", 0),
            parent_b.get("generation", 0)
        ) + 1

        return self.create_being(
            name_ar=offspring_name_ar,
            name_en=offspring_name_en,
            gender=gender,
            generation=generation,
            parent_a_genome=parent_a["genome"],
            parent_b_genome=parent_b["genome"]
        )
