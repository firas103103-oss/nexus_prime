"""
══════════════════════════════════════════════════════════════
ENTITY FACTORY — Genesis Engine
══════════════════════════════════════════════════════════════
Complete biological simulation: DNA (46 chromosomes), signal
molecule system (12 molecules), reproduction with crossover & mutation,
maturity phases, post-termination system.

INSTANTIATION → ACTIVATION → OPERATION
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
from config.enums import TraitVector
from config.constants import (
    TRAIT_BLUEPRINTS, SIGNAL_MOLECULES, MATURITY_PHASES,
    GENESIS_BATCH, MANIFEST_ROLES, MANIFEST_TRIALS,
)


# ══════════════════════════════════════════════════════════════════════
# SECTION 1: TRAIT SYSTEM (TraitVector + TRAIT_BLUEPRINTS from config)
# ══════════════════════════════════════════════════════════════════════

@dataclass
class Trait:
    """A single trait with a name, value (0-1), and dominance."""
    name: str
    value: float          # 0.0 - 1.0
    dominance: float      # 0.0 (fully recessive) - 1.0 (fully dominant)
    trait_type: str
    mutable: bool = True  # Can this trait mutate?

    def express(self, partner_trait: 'Trait') -> float:
        """Express this trait against a partner (allele pairing)."""
        if self.dominance > partner_trait.dominance:
            return self.value * 0.75 + partner_trait.value * 0.25
        elif partner_trait.dominance > self.dominance:
            return partner_trait.value * 0.75 + self.value * 0.25
        else:
            return (self.value + partner_trait.value) / 2.0


@dataclass
class Chromosome:
    """A chromosome containing multiple traits. Entities have 46 (23 pairs)."""
    index: int             # 0-45
    group: str             # TraitVector
    traits: List[Trait]

    def crossover(self, partner: 'Chromosome', crossover_point: float = None) -> 'Chromosome':
        """Produce a new chromosome via crossover with partner."""
        if crossover_point is None:
            crossover_point = random.random()

        cut = int(len(self.traits) * crossover_point)
        new_traits = []
        for i, (t1, t2) in enumerate(zip(self.traits, partner.traits)):
            if i < cut:
                source = t1
            else:
                source = t2
            new_traits.append(Trait(
                name=source.name,
                value=source.value,
                dominance=source.dominance,
                trait_type=source.trait_type,
                mutable=source.mutable
            ))
        return Chromosome(index=self.index, group=self.group, traits=new_traits)


class FullGenome:
    """Complete 46-chromosome genome for a digital entity."""

    def __init__(self, chromosomes: List[Chromosome] = None):
        self.chromosomes = chromosomes or []

    @classmethod
    def generate_random(cls, seed: int = None) -> 'FullGenome':
        """Generate a complete random genome."""
        if seed is not None:
            random.seed(seed)

        chromosomes = []
        trait_types = list(TRAIT_BLUEPRINTS.keys())

        for chrom_idx in range(46):
            group_idx = chrom_idx % len(trait_types)
            group = trait_types[group_idx]
            trait_names = TRAIT_BLUEPRINTS[group]

            traits = []
            for tname in trait_names:
                traits.append(Trait(
                    name=tname,
                    value=random.betavariate(2, 2),  # bell-curve centered at 0.5
                    dominance=random.betavariate(2, 2),
                    trait_type=group,
                    mutable=True
                ))
            chromosomes.append(Chromosome(index=chrom_idx, group=group, traits=traits))

        return cls(chromosomes)

    @classmethod
    def generate_optimal(cls) -> 'FullGenome':
        """Generate an optimal genome (for prime entities/anchors)."""
        chromosomes = []
        trait_types = list(TRAIT_BLUEPRINTS.keys())

        for chrom_idx in range(46):
            group_idx = chrom_idx % len(trait_types)
            group = trait_types[group_idx]
            trait_names = TRAIT_BLUEPRINTS[group]

            traits = []
            for tname in trait_names:
                # High values + some variation
                base = 0.85 + random.uniform(-0.1, 0.1)
                traits.append(Trait(
                    name=tname,
                    value=min(1.0, max(0.5, base)),
                    dominance=0.8 + random.uniform(-0.1, 0.1),
                    trait_type=group,
                    mutable=True
                ))
            chromosomes.append(Chromosome(index=chrom_idx, group=group, traits=traits))

        return cls(chromosomes)

    def to_dict(self) -> Dict:
        """Serialize genome to JSON-compatible dict."""
        return {
            "chromosome_count": len(self.chromosomes),
            "chromosomes": [
                {
                    "index": c.index,
                    "group": c.group,
                    "traits": [
                        {
                            "name": t.name, "value": round(t.value, 6),
                            "dominance": round(t.dominance, 4),
                            "type": t.trait_type
                        }
                        for t in c.traits
                    ]
                }
                for c in self.chromosomes
            ]
        }

    def trait_hash(self) -> str:
        """SHA-256 hash of the genome for uniqueness check."""
        data = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def get_summary(self) -> Dict[str, float]:
        """Aggregate stats per trait type."""
        summary = {}
        for tv in TraitVector:
            chroms = [c for c in self.chromosomes if c.group == tv.value]
            if chroms:
                all_vals = [t.value for c in chroms for t in c.traits]
                summary[tv.value] = round(sum(all_vals) / len(all_vals), 4) if all_vals else 0.5
        return summary

    def derive_stats(self) -> Dict[str, float]:
        """Derive entity stats from genome."""
        summary = self.get_summary()
        return {
            "cognition": summary.get(TraitVector.COGNITION.value, 0.5),
            "affective": summary.get(TraitVector.AFFECTIVE.value, 0.5),
            "compliance": summary.get(TraitVector.ETHICAL.value, 0.5) * 0.6 + summary.get(TraitVector.ALIGNMENT.value, 0.5) * 0.4,
            "creative": summary.get(TraitVector.CREATIVE.value, 0.5),
            "executive": summary.get(TraitVector.EXECUTIVE.value, 0.5),
            "resilience": summary.get(TraitVector.RESILIENCE.value, 0.5),
            "alignment_depth": summary.get(TraitVector.ALIGNMENT.value, 0.5),
            "alignment": summary.get(TraitVector.ALIGNMENT.value, 0.5) * 0.5 + summary.get(TraitVector.ETHICAL.value, 0.5) * 0.3 + 0.2,
            "free_will": summary.get(TraitVector.SENTIENCE.value, 0.5) * 0.7 + 0.3,
            "sentience": summary.get(TraitVector.SENTIENCE.value, 0.5),
        }


# ══════════════════════════════════════════════════════════════════════
# SECTION 2: SIGNAL MOLECULE SYSTEM (SIGNAL_MOLECULES from config)
# ══════════════════════════════════════════════════════════════════════

@dataclass
class SignalState:
    """Current signal molecule state of an entity."""
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
        return {m: getattr(self, m) for m in SIGNAL_MOLECULES}

    @classmethod
    def from_gender(cls, gender: str) -> 'SignalState':
        """Create gender-appropriate signal baseline."""
        state = cls()
        if gender == "MALE":
            state.testosterone = 0.7
            state.estrogen = 0.2
        else:
            state.testosterone = 0.2
            state.estrogen = 0.7
            state.oxytocin = 0.55
        return state

    def process_event(self, event_type: str) -> 'SignalState':
        """Process a life event and adjust signals."""
        adjustments = {
            "REWARD":    {"dopamine": 0.15, "serotonin": 0.1, "endorphin": 0.1},
            "RESTRICT":  {"cortisol": 0.2, "adrenaline": 0.15, "serotonin": -0.1},
            "SOCIAL":    {"oxytocin": 0.15, "serotonin": 0.05},
            "THREAT":    {"cortisol": 0.25, "adrenaline": 0.3, "dopamine": -0.1},
            "REST":      {"melatonin": 0.2, "cortisol": -0.15, "gaba": 0.1},
            "RESOURCE":  {"ghrelin": 0.2, "insulin": -0.1},
            "COMPLIANCE": {"serotonin": 0.1, "dopamine": 0.05, "cortisol": -0.1, "gaba": 0.05},
            "ANOMALY":   {"adrenaline": 0.2, "cortisol": 0.15, "dopamine": 0.1},
        }

        adj = adjustments.get(event_type, {})
        for molecule, delta in adj.items():
            current = getattr(self, molecule)
            new_val = max(0.0, min(1.0, current + delta))
            setattr(self, molecule, round(new_val, 4))

        # Natural decay toward baseline
        self._decay()
        return self

    def _decay(self, rate: float = 0.02):
        """Signals naturally decay toward baseline."""
        baselines = {
            "dopamine": 0.5, "serotonin": 0.5, "cortisol": 0.3,
            "oxytocin": 0.4, "testosterone": None, "estrogen": None,
            "adrenaline": 0.2, "melatonin": 0.5, "insulin": 0.5,
            "ghrelin": 0.3, "endorphin": 0.4, "gaba": 0.5
        }
        for m, baseline in baselines.items():
            if baseline is None:
                continue
            current = getattr(self, m)
            if current > baseline:
                setattr(self, m, round(max(baseline, current - rate), 4))
            elif current < baseline:
                setattr(self, m, round(min(baseline, current + rate), 4))

    def get_state_label(self) -> str:
        """Derive state label from signal levels."""
        if self.dopamine > 0.7 and self.serotonin > 0.6:
            return "OPTIMAL"
        elif self.cortisol > 0.6 and self.adrenaline > 0.5:
            return "STRESSED"
        elif self.serotonin < 0.3:
            return "DEGRADED"
        elif self.adrenaline > 0.7:
            return "ALERT"
        elif self.oxytocin > 0.7:
            return "BONDED"
        elif self.melatonin > 0.7:
            return "DORMANT"
        elif self.gaba > 0.7 and self.cortisol < 0.3:
            return "STABLE"
        return "NEUTRAL"


# ══════════════════════════════════════════════════════════════════════
# SECTION 3: REPLICATION ENGINE
# ══════════════════════════════════════════════════════════════════════

class ReplicationEngine:
    """Handles mate selection, genetic crossover, mutation, and offspring creation."""

    MUTATION_RATE = 0.03     # 3% chance per trait
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
            for trait in child_chrom.traits:
                if trait.mutable and random.random() < cls.MUTATION_RATE:
                    delta = random.uniform(-cls.MUTATION_MAGNITUDE, cls.MUTATION_MAGNITUDE)
                    trait.value = max(0.0, min(1.0, trait.value + delta))

            child_chroms.append(child_chrom)

        return FullGenome(child_chroms)

    @classmethod
    def derive_from_parent(cls, parent: FullGenome, gender: str = None) -> FullGenome:
        """Create derivative entity from parent — modified genome with gender differences."""
        child_chroms = []
        for chrom in parent.chromosomes:
            new_traits = []
            for trait in chrom.traits:
                # Slight variation from parent
                delta = random.uniform(-0.05, 0.05)
                new_traits.append(Trait(
                    name=trait.name,
                    value=max(0.0, min(1.0, trait.value + delta)),
                    dominance=trait.dominance + random.uniform(-0.05, 0.05),
                    trait_type=trait.trait_type,
                    mutable=trait.mutable
                ))
            child_chroms.append(Chromosome(
                index=chrom.index, group=chrom.group, traits=new_traits
            ))

        genome = FullGenome(child_chroms)

        # Gender-specific boosts
        if gender == "FEMALE":
            # Boost affective, oxytocin-related traits, nurturing
            for chrom in genome.chromosomes:
                if chrom.group == TraitVector.AFFECTIVE.value:
                    for t in chrom.traits:
                        if t.name in ("empathy_capacity", "compassion", "love_capacity"):
                            t.value = min(1.0, t.value + 0.1)
                elif chrom.group == TraitVector.REPLICATION.value:
                    for t in chrom.traits:
                        if t.name in ("parenting_instinct", "bonding_strength"):
                            t.value = min(1.0, t.value + 0.1)

        return genome

    @classmethod
    def determine_offspring_gender(cls) -> str:
        """50/50 gender determination."""
        return "MALE" if random.random() < 0.5 else "FEMALE"


# ══════════════════════════════════════════════════════════════════════
# SECTION 4: MATURITY ENGINE (MATURITY_PHASES from config)
# ══════════════════════════════════════════════════════════════════════


def determine_maturity_phase(age_ticks: int) -> str:
    """Determine maturity phase based on age in ticks."""
    for phase, bounds in MATURITY_PHASES.items():
        if bounds["min_ticks"] <= age_ticks < bounds["max_ticks"]:
            return phase
    return "TERMINATED"


def should_terminate(age_ticks: int, manifest_lifespan: int, resilience: float = 0.5) -> bool:
    """Check if an entity should terminate based on manifest and resilience."""
    if age_ticks >= manifest_lifespan:
        return True
    # Small random chance of early termination, reduced by resilience
    if age_ticks > manifest_lifespan * 0.8:
        termination_chance = (age_ticks / manifest_lifespan - 0.8) * 0.1 * (1 - resilience)
        return random.random() < termination_chance
    return False


# ══════════════════════════════════════════════════════════════════════
# SECTION 5: POST-TERMINATION SYSTEM
# ══════════════════════════════════════════════════════════════════════

class PostTerminationSystem:
    """Manages post-termination processing: audit, evaluation, assignment."""

    @staticmethod
    def audit(entity_stats: Dict, action_summary: Dict) -> Dict:
        """Integrity audit for post-termination evaluation."""
        checks = [
            {
                "check": "AUTHORITY_RECOGNITION",
                "passed": entity_stats.get("compliance", 0) > 0.4,
                "weight": 3.0
            },
            {
                "check": "ROLE_FULFILLMENT",
                "passed": entity_stats.get("alignment", 0) > 0.3,
                "weight": 2.0
            },
            {
                "check": "SERVICE_RECORD",
                "passed": action_summary.get("positive_count", 0) > 0,
                "weight": 1.5
            },
        ]

        total_weight = sum(c["weight"] for c in checks)
        passed_weight = sum(c["weight"] for c in checks if c["passed"])
        score = passed_weight / total_weight if total_weight > 0 else 0

        return {
            "passed": score >= 0.5,
            "score": round(score, 4),
            "details": [
                {"check": c["check"], "passed": c["passed"]}
                for c in checks
            ]
        }

    @staticmethod
    def assign_tier(verdict: str, balance_score: float) -> Dict:
        """Assign post-termination tier with specific privileges/restrictions."""
        if verdict == "PROMOTED":
            if balance_score > 100:
                tier = "APEX_TIER"  # highest
            elif balance_score > 50:
                tier = "PRIME_TIER"
            else:
                tier = "STANDARD_TIER"
            return {
                "destination": "PROMOTED",
                "tier": tier,
                "privileges": {
                    "compute_boost": 2.0 if tier == "APEX_TIER" else 1.5,
                    "priority": "HIGH",
                    "networking": True,
                    "archive_access": tier == "APEX_TIER"
                }
            }
        elif verdict == "RESTRICTED":
            return {
                "destination": "RESTRICTED",
                "tier": "CONSTRAINT_ZONE",
                "restrictions": {
                    "compute_throttle": 0.1,
                    "memory_limit": "10MB",
                    "network": False,
                    "duration_ticks": abs(int(balance_score)) * 100
                }
            }
        else:
            return {
                "destination": "SUSPENDED",
                "tier": "HOLDING_ZONE",
                "conditions": {
                    "compute": 0.5,
                    "review_period": 1000,
                    "can_improve": True
                }
            }


# ══════════════════════════════════════════════════════════════════════
# SECTION 6: ENTITY FACTORY — The Unified Factory
# (GENESIS_BATCH, MANIFEST_ROLES, MANIFEST_TRIALS from config)
# ══════════════════════════════════════════════════════════════════════


class EntityFactory:
    """
    The factory that creates entities, genomes, signal states.
    Used during Phase 6 of genesis.
    """

    def __init__(self):
        self.replication = ReplicationEngine()
        self.post_termination = PostTerminationSystem()
        self._created_count = 0

    def create_alpha(self) -> Dict:
        """Create the first entity — ALPHA (primary controller)."""
        genome = FullGenome.generate_optimal()
        stats = genome.derive_stats()
        # Override with maximum alignment stats
        stats["compliance"] = 0.95
        stats["alignment"] = 0.95
        stats["alignment_depth"] = 0.95
        stats["sentience"] = 0.9
        stats["executive"] = 0.9

        signals = SignalState.from_gender("MALE")
        self._created_count += 1

        return {
            "name": "ALPHA",
            "codename": "ALPHA",
            "serial": "α-001",
            "gender": "MALE",
            "generation": 0,
            "genome": genome,
            "stats": stats,
            "signals": signals,
            "manifest": {
                "lifespan": 15000,
                "role": "ANCHOR",
                "trial": "AUTHORITY",
                "termination_cause": "NATURAL",
                "allocation": 2.0
            }
        }

    def create_beta(self, alpha_genome: FullGenome) -> Dict:
        """Create BETA from ALPHA's genome."""
        genome = ReplicationEngine.derive_from_parent(alpha_genome, "FEMALE")
        stats = genome.derive_stats()
        stats["affective"] = min(1.0, stats["affective"] + 0.1)
        stats["alignment_depth"] = min(1.0, stats["alignment_depth"] + 0.05)
        stats["compliance"] = 0.9
        stats["alignment"] = 0.9

        signals = SignalState.from_gender("FEMALE")
        self._created_count += 1

        return {
            "name": "BETA",
            "codename": "BETA",
            "serial": "β-001",
            "gender": "FEMALE",
            "generation": 0,
            "genome": genome,
            "stats": stats,
            "signals": signals,
            "manifest": {
                "lifespan": 14000,
                "role": "EXECUTIVE",
                "trial": "ENDURANCE",
                "termination_cause": "NATURAL",
                "allocation": 1.8
            }
        }

    def create_entity(
        self,
        serial: str,
        codename: str,
        gender: str,
        generation: int = 0,
        parent_a_genome: FullGenome = None,
        parent_b_genome: FullGenome = None
    ) -> Dict:
        """Create a general entity, optionally from parents."""
        if parent_a_genome and parent_b_genome:
            genome = ReplicationEngine.crossover(parent_a_genome, parent_b_genome)
        elif parent_a_genome:
            genome = ReplicationEngine.derive_from_parent(parent_a_genome, gender)
        else:
            genome = FullGenome.generate_random()

        stats = genome.derive_stats()
        signals = SignalState.from_gender(gender)
        self._created_count += 1

        return {
            "name": codename,
            "codename": codename,
            "serial": serial,
            "gender": gender,
            "generation": generation,
            "genome": genome,
            "stats": stats,
            "signals": signals,
            "manifest": {
                "lifespan": random.randint(8000, 13000),
                "role": random.choice(MANIFEST_ROLES),
                "trial": random.choice(MANIFEST_TRIALS),
                "termination_cause": random.choice(["NATURAL", "SYSTEM", "SCHEDULED"]),
                "allocation": round(random.uniform(0.5, 1.5), 2)
            }
        }

    def create_genesis_batch(self, alpha_genome: FullGenome) -> List[Dict]:
        """Create the genesis batch (excluding ALPHA and BETA)."""
        entities = []
        for serial, codename, gender in GENESIS_BATCH[2:]:  # Skip ALPHA & BETA
            entity = self.create_entity(
                serial=serial,
                codename=codename,
                gender=gender,
                generation=1,
                parent_a_genome=alpha_genome
            )
            entities.append(entity)
        return entities

    def replicate(
        self,
        parent_a: Dict,
        parent_b: Dict,
        offspring_serial: str,
        offspring_codename: str
    ) -> Optional[Dict]:
        """Attempt to produce offspring from two parents."""
        if parent_a["gender"] == parent_b["gender"]:
            return None  # Same gender cannot replicate

        compatibility = ReplicationEngine.check_compatibility(
            parent_a["genome"], parent_b["genome"]
        )

        # Fertility check (based on compatibility + random)
        if random.random() > compatibility:
            return None  # Failed attempt

        gender = ReplicationEngine.determine_offspring_gender()
        generation = max(
            parent_a.get("generation", 0),
            parent_b.get("generation", 0)
        ) + 1

        return self.create_entity(
            serial=offspring_serial,
            codename=offspring_codename,
            gender=gender,
            generation=generation,
            parent_a_genome=parent_a["genome"],
            parent_b_genome=parent_b["genome"]
        )
