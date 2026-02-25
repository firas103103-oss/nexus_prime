"""
Genome-Driven Agent Creation — 82 Traits × 46 Chromosomes → LLM Params
═══════════════════════════════════════════════════════════════════════
Maps TRAIT_BLUEPRINTS to LiteLLM/OpenAI-compatible parameters.
Creativity 0.9 → temperature ↑, top_p ↑
"""
from typing import Dict, Any

# Trait → LLM param mapping (from neural_spine/config/constants.py)
TRAIT_TO_LLM_PARAMS = {
    "CREATIVE": {"temperature": 0.8, "top_p": 0.95},      # imagination, risk_tolerance
    "COGNITION": {"temperature": 0.3, "top_p": 0.9},      # logical, precise
    "AFFECTIVE": {"temperature": 0.6, "top_p": 0.92},     # emotional depth
    "ETHICAL": {"temperature": 0.2, "top_p": 0.85},      # conservative, aligned
    "EXECUTIVE": {"temperature": 0.4, "top_p": 0.88},    # decisive
    "RESILIENCE": {"temperature": 0.5, "top_p": 0.9},   # adaptable
    "ALIGNMENT": {"temperature": 0.25, "top_p": 0.82},   # compliant
    "REPLICATION": {"temperature": 0.55, "top_p": 0.9}, # nurturing
    "ACQUISITION": {"temperature": 0.45, "top_p": 0.92},# learning
    "SENTIENCE": {"temperature": 0.5, "top_p": 0.9},    # self-aware
}

SIGNAL_MOLECULES = [
    "dopamine", "serotonin", "cortisol", "oxytocin",
    "testosterone", "estrogen", "adrenaline", "melatonin",
    "insulin", "ghrelin", "endorphin", "gaba"
]


def trait_summary_to_llm_params(trait_summary: Dict[str, float]) -> Dict[str, Any]:
    """
    Convert genome trait_summary (10 categories) to LiteLLM params.
    High Creativity → higher temperature, top_p.
    High Compliance/Alignment → lower temperature.
    Accepts both legacy keys (CREATIVITY, INTELLIGENCE, MORALS) and TRAIT_BLUEPRINT groups (CREATIVE, COGNITION, ETHICAL).
    """
    if not trait_summary:
        return {"temperature": 0.5, "top_p": 0.9, "max_tokens": 2048}

    # Support both legacy and TRAIT_BLUEPRINT keys
    creative = trait_summary.get("CREATIVITY", trait_summary.get("CREATIVE", 0.5))
    ethical = (
        trait_summary.get("MORALS", trait_summary.get("ETHICAL", 0.5)) * 0.6
        + trait_summary.get("SPIRITUALITY", trait_summary.get("ALIGNMENT", 0.5)) * 0.4
    )
    cognition = trait_summary.get("INTELLIGENCE", trait_summary.get("COGNITION", 0.5))

    # Base: 0.3–0.9 range
    temp = 0.3 + (creative * 0.5) - (ethical * 0.2) + (cognition * 0.1)
    temp = max(0.1, min(0.95, round(temp, 2)))

    top_p = 0.8 + (creative * 0.15) - (ethical * 0.1)
    top_p = max(0.7, min(1.0, round(top_p, 2)))

    return {
        "temperature": temp,
        "top_p": top_p,
        "max_tokens": 2048,
        "frequency_penalty": 0.1 - (cognition * 0.05) if cognition > 0.5 else 0.0,
        "presence_penalty": 0.0,
        "genome_source": trait_summary,
    }


def signal_to_mood(signals: Dict[str, float]) -> str:
    """Derive mood from signal state (from cognitive_bridge)."""
    d = signals.get("dopamine", 0.5)
    s = signals.get("serotonin", 0.5)
    c = signals.get("cortisol", 0.3)
    a = signals.get("adrenaline", 0.2)
    g = signals.get("gaba", 0.5)
    o = signals.get("oxytocin", 0.4)
    if d > 0.7 and s > 0.6:
        return "JOYFUL"
    if c > 0.6 and a > 0.5:
        return "STRESSED"
    if s < 0.3:
        return "DEPRESSED"
    if a > 0.7:
        return "ALERT"
    if o > 0.7:
        return "BONDED"
    if g > 0.7 and c < 0.3:
        return "CALM"
    return "NEUTRAL"


def apply_mood_modifier(llm_params: Dict[str, Any], mood: str) -> Dict[str, Any]:
    """
    Apply mood-based adjustment to LLM params (per SOVEREIGN_ARCHITECTURAL_GOVERNANCE).
    STRESSED: -0.15 temp, -0.05 top_p | JOYFUL: +0.1 temp, +0.03 top_p
    CALM: -0.05 temp | ALERT: -0.1 temp, -0.03 top_p | NEUTRAL: no change
    """
    out = dict(llm_params)
    temp = out.get("temperature", 0.5)
    top_p = out.get("top_p", 0.9)
    if mood == "STRESSED":
        temp = max(0.1, temp - 0.15)
        top_p = max(0.7, top_p - 0.05)
    elif mood == "JOYFUL":
        temp = min(0.95, temp + 0.1)
        top_p = min(1.0, top_p + 0.03)
    elif mood == "CALM":
        temp = max(0.1, temp - 0.05)
    elif mood == "ALERT":
        temp = max(0.1, temp - 0.1)
        top_p = max(0.7, top_p - 0.03)
    out["temperature"] = round(temp, 2)
    out["top_p"] = round(top_p, 2)
    return out
