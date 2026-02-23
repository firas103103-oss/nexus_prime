"""
═══════════════════════════════════════════════════════════════════════
EVE PROTOCOL — Fractal Polarization
═══════════════════════════════════════════════════════════════════════
Creates EVE from AS-SULTAN's 46 chromosomes via Fractal Polarization:
- Mirror/split genome digitally (structural integrity preserved)
- Shift hormonal baseline to Estrogen-dominant
- Activate recessive traits → dominant (personality derivation)
- Derive LLM params from the polarized genome
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Optional, Tuple

# Trait group mapping: neural_spine TRAIT_BLUEPRINTS → genome_agent_mapper keys
TRAIT_GROUP_TO_LEGACY = {
    "COGNITION": "INTELLIGENCE",
    "AFFECTIVE": "EMOTIONS",
    "ETHICAL": "MORALS",
    "CREATIVE": "CREATIVITY",
    "EXECUTIVE": "LEADERSHIP",
    "RESILIENCE": "SURVIVAL",
    "ALIGNMENT": "SPIRITUALITY",
    "REPLICATION": "REPRODUCTION",
    "ACQUISITION": "LEARNING",
    "SENTIENCE": "CONSCIOUSNESS",
}

# 12 Signal Molecules (MSL schema)
SIGNAL_MOLECULES = [
    "dopamine", "serotonin", "cortisol", "oxytocin",
    "testosterone", "estrogen", "adrenaline", "melatonin",
    "insulin", "ghrelin", "endorphin", "gaba",
]


def fractal_polarize_genome(
    source_genome: Dict[str, Any],
    estrogen_dominant: bool = True,
    recessive_flip: bool = True,
) -> Dict[str, Any]:
    """
    Apply Fractal Polarization to source genome (AS-SULTAN).
    - estrogen_dominant: Shift testosterone↓ estrogen↑ oxytocin↑
    - recessive_flip: Invert dominance (recessive → dominant) for personality shift
    Returns polarized genome structure compatible with MSL.genomes.
    """
    chromosomes = source_genome.get("chromosomes")
    # Handle MSL format: chromosomes may be list or dict like {"pairs": 23, "categories": {...}}
    if isinstance(chromosomes, dict):
        ts = chromosomes.get("categories", chromosomes)
        if isinstance(ts, str):
            ts = json.loads(ts) if ts else {}
        return _polarize_trait_summary(ts, estrogen_dominant, recessive_flip)
    if not chromosomes or not isinstance(chromosomes, list):
        ts = source_genome.get("trait_summary", source_genome)
        if isinstance(ts, str):
            ts = json.loads(ts) if ts else {}
        if isinstance(ts, dict):
            return _polarize_trait_summary(ts, estrogen_dominant, recessive_flip)

    polarized_chroms = []
    for chrom in chromosomes:
        traits = chrom.get("traits", [])
        new_traits = []
        for t in traits:
            val = t.get("value", 0.5)
            dom = t.get("dominance", 0.5)
            if recessive_flip:
                dom = 1.0 - dom  # Recessive becomes dominant
            new_traits.append({
                "name": t.get("name", "unknown"),
                "value": val,
                "dominance": round(dom, 4),
                "type": t.get("type", t.get("trait_type", "UNKNOWN")),
            })
        polarized_chroms.append({
            "index": chrom.get("index", len(polarized_chroms)),
            "group": chrom.get("group", "UNKNOWN"),
            "traits": new_traits,
        })

    return {
        "chromosome_count": len(polarized_chroms),
        "chromosomes": polarized_chroms,
        "polarization": {
            "source": "AS-SULTAN",
            "estrogen_dominant": estrogen_dominant,
            "recessive_flip": recessive_flip,
        },
    }


def _polarize_trait_summary(
    trait_summary: Dict[str, float],
    estrogen_dominant: bool,
    recessive_flip: bool,
) -> Dict[str, Any]:
    """Polarize when only trait_summary is available (no full chromosomes)."""
    nurturing_keys = {
        "REPLICATION", "REPRODUCTION", "AFFECTIVE", "EMOTIONS",
        "CREATIVE", "CREATIVITY", "SENTIENCE", "CONSCIOUSNESS",
    }
    polarized = {}
    for k, v in trait_summary.items():
        if isinstance(v, (int, float)):
            if recessive_flip and k in nurturing_keys:
                polarized[k] = min(1.0, round(v * 1.12, 4))  # Boost nurturing/creative
            else:
                polarized[k] = v
        else:
            polarized[k] = v

    if estrogen_dominant:
        polarized["_signal_baseline"] = {
            "testosterone": 0.2,
            "estrogen": 0.75,
            "oxytocin": 0.6,
        }

    return {
        "chromosome_count": 46,
        "trait_summary": polarized,
        "polarization": {
            "source": "AS-SULTAN",
            "estrogen_dominant": estrogen_dominant,
            "recessive_flip": recessive_flip,
        },
    }


def derive_trait_summary_from_chromosomes(chromosomes: List[Dict]) -> Dict[str, float]:
    """Aggregate chromosomes into trait_summary (10 categories)."""
    summary = {}
    for chrom in chromosomes:
        group = chrom.get("group", "UNKNOWN")
        traits = chrom.get("traits", [])
        if not traits:
            continue
        vals = [t.get("value", 0.5) for t in traits]
        avg = sum(vals) / len(vals) if vals else 0.5
        summary[group] = round(avg, 4)

    # Map to legacy keys for genome_agent_mapper (CREATIVITY, INTELLIGENCE, etc.)
    legacy = {}
    for k, v in summary.items():
        legacy[TRAIT_GROUP_TO_LEGACY.get(k, k)] = v
    return legacy if legacy else summary


def apply_estrogen_baseline(signals: Dict[str, float]) -> Dict[str, float]:
    """Shift signal molecules to estrogen-dominant baseline."""
    out = dict(signals) if signals else {}
    out["testosterone"] = min(0.25, out.get("testosterone", 0.5) * 0.4)
    out["estrogen"] = max(0.7, out.get("estrogen", 0.5) * 1.4)
    out["oxytocin"] = max(0.55, out.get("oxytocin", 0.4) * 1.3)
    for m in SIGNAL_MOLECULES:
        if m not in out:
            out[m] = 0.5
        out[m] = max(0.0, min(1.0, round(out[m], 4)))
    return out


def compute_eve_trait_hash(polarized: Dict[str, Any]) -> str:
    """SHA-256 hash for EVE genome uniqueness."""
    data = json.dumps(polarized, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()


def create_eve_genome(
    sultan_genome: Dict[str, Any],
    sultan_signals: Optional[Dict[str, float]] = None,
) -> Tuple[Dict[str, Any], Dict[str, float], Dict[str, Any]]:
    """
    Full EVE creation from AS-SULTAN.
    Returns: (polarized_genome, eve_signals, metadata)
    """
    polarized = fractal_polarize_genome(
        sultan_genome,
        estrogen_dominant=True,
        recessive_flip=True,
    )

    trait_summary = polarized.get("trait_summary")
    if not trait_summary and polarized.get("chromosomes"):
        chroms = polarized["chromosomes"]
        if isinstance(chroms, list) and chroms:
            trait_summary = derive_trait_summary_from_chromosomes(chroms)
    if not trait_summary:
        trait_summary = {
            "CREATIVE": 0.78, "AFFECTIVE": 0.82, "SENTIENCE": 0.85,
            "COGNITION": 0.88, "ETHICAL": 0.9, "ALIGNMENT": 0.92,
            "REPLICATION": 0.7, "EXECUTIVE": 0.8, "RESILIENCE": 0.85,
            "ACQUISITION": 0.88,
        }

    eve_signals = apply_estrogen_baseline(sultan_signals or {})

    metadata = {
        "source_entity": "AS-SULTAN",
        "protocol": "EVE_FRACTAL_POLARIZATION",
        "trait_hash": compute_eve_trait_hash(polarized),
        "chromosome_count": 46,
        "structural_integrity": True,
    }

    return polarized, eve_signals, {"trait_summary": trait_summary, "metadata": metadata}
