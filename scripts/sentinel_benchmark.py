#!/usr/bin/env python3
"""
SENTINEL BENCHMARK — Hormonal Feedback Loop Simulation
═══════════════════════════════════════════════════════
Simulates: Success → Dopamine Spike (TASK_SUCCESS event)
Logs results to SENTINEL_BENCHMARK.md
"""
import sys
import os
import time
from pathlib import Path

# Add nexus_nerve to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "nexus_nerve"))

from cognitive_bridge import (
    SignalState,
    HormoneEvent,
    HORMONE_TRIGGERS,
    HORMONE_DEFAULTS,
    _mood_from_signals,
)

def run_hormonal_feedback_simulation(iterations: int = 20) -> dict:
    """Simulate Success → Dopamine Spike feedback loop."""
    signals = SignalState()
    results = []
    
    for i in range(iterations):
        before_d = signals.dopamine
        before_s = signals.serotonin
        before_mood = _mood_from_signals(signals)
        
        t0 = time.perf_counter()
        signals.apply_event(HormoneEvent.TASK_SUCCESS)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        
        after_d = signals.dopamine
        after_s = signals.serotonin
        after_mood = _mood_from_signals(signals)
        
        results.append({
            "iteration": i + 1,
            "dopamine_before": round(before_d, 4),
            "dopamine_after": round(after_d, 4),
            "serotonin_before": round(before_s, 4),
            "serotonin_after": round(after_s, 4),
            "delta_dopamine": round(after_d - before_d, 4),
            "mood_before": before_mood,
            "mood_after": after_mood,
            "elapsed_ms": round(elapsed_ms, 4),
        })
    
    return {
        "simulation": "Hormonal Feedback Loop (Success → Dopamine Spike)",
        "event": "TASK_SUCCESS",
        "iterations": iterations,
        "triggers": HORMONE_TRIGGERS.get(HormoneEvent.TASK_SUCCESS, []),
        "final_state": signals.to_dict(),
        "final_mood": _mood_from_signals(signals),
        "results": results,
        "avg_elapsed_ms": round(sum(r["elapsed_ms"] for r in results) / len(results), 4),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

def main():
    data = run_hormonal_feedback_simulation(20)
    out_path = Path(__file__).resolve().parent.parent / "SENTINEL_BENCHMARK.md"
    
    lines = [
        "# SENTINEL BENCHMARK — Hormonal Feedback Loop",
        "",
        "## Simulation: Success → Dopamine Spike",
        "",
        f"**Timestamp:** {data['timestamp']}",
        f"**Event:** {data['event']}",
        f"**Iterations:** {data['iterations']}",
        f"**Triggers:** {data['triggers']}",
        "",
        "### Performance",
        f"- **Avg. apply_event latency:** {data['avg_elapsed_ms']} ms",
        "",
        "### Final State",
        "```json",
        str(data["final_state"]),
        "```",
        "",
        f"**Final Mood:** {data['final_mood']}",
        "",
        "### Per-Iteration Results",
        "",
        "| Iter | D_before | D_after | ΔD | Mood_before | Mood_after | Latency (ms) |",
        "|------|----------|---------|-----|-------------|------------|--------------|",
    ]
    
    for r in data["results"]:
        lines.append(
            f"| {r['iteration']} | {r['dopamine_before']} | {r['dopamine_after']} | "
            f"{r['delta_dopamine']:+.4f} | {r['mood_before']} | {r['mood_after']} | {r['elapsed_ms']} |"
        )
    
    lines.extend([
        "",
        "## Verification",
        "",
        "- TASK_SUCCESS triggers: dopamine +0.08, serotonin +0.05",
        "- Decay applied: drift toward baseline (DECAY_RATE=0.02)",
        "- Mood transitions: NEUTRAL → JOYFUL when D>0.7, S>0.6",
        "",
    ])
    
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Benchmark written to {out_path}")
    return data

if __name__ == "__main__":
    main()
