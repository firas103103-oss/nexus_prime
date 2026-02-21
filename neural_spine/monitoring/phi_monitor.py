#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
FIX #8: Phi* (Integrated Information Theory) Consciousness Monitor
═══════════════════════════════════════════════════════════════════════════════

Approximates Phi* — a proxy for integrated information across the 32-agent
collective. Uses pairwise mutual information and random bipartitions.

WHAT IT MEASURES:
  Phi* ≈ the degree to which the whole system generates more information
  than the sum of its parts. Higher Phi* = more "integrated" processing.

OPTIMIZATION:
  Full IIT computation is O(2^N) — impossible for N=32.
  We approximate via:
    1. Pairwise MI matrix (empirical, sliding window)
    2. Random bipartitions (50 samples) with geometric mean normalization
    3. Minimum Information Bipartition (MIB) approximation

PERFORMANCE:
  Target: ≤50ms per evaluation (runs every 100 spine cycles)
  With 32 agents, 50 bipartitions: ~20ms

THRESHOLDS:
  GREEN:  Φ* > 1.0 — High integration (collective cognition)
  YELLOW: 0 < Φ* ≤ 1.0 — Moderate integration
  RED:    Φ* ≤ 0 — Fragmented (agents not collaborating)

═══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Tuple, List
import time
import json


@dataclass
class PhiResult:
    """Result of a Phi* computation"""
    phi_star: float                     # Approximate Phi*
    phi_normalized: float               # Phi* / log(N)  — normalized to [0,1]-ish
    mi_matrix: np.ndarray               # Pairwise MI matrix
    mib_partition: Tuple[list, list]    # Minimum Information Bipartition
    mib_cut_info: float                 # Information lost at MIB cut
    active_agents: int                  # Number of active agents
    compute_time_ms: float              # Time to compute
    status: str                         # GREEN / YELLOW / RED

    def to_dict(self) -> dict:
        return {
            "phi_star": round(self.phi_star, 4),
            "phi_normalized": round(self.phi_normalized, 4),
            "active_agents": self.active_agents,
            "mib_partition": [self.mib_partition[0][:5], self.mib_partition[1][:5]],
            "mib_cut_info": round(self.mib_cut_info, 4),
            "compute_time_ms": round(self.compute_time_ms, 2),
            "status": self.status,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class PhiStarMonitor:
    """
    ═══════════════════════════════════════════════════════════════════════════
    Phi* Consciousness Monitor for NEXUS PRIME Neural Spine
    ═══════════════════════════════════════════════════════════════════════════

    Monitors the integrated information of the 32-agent collective by:
      1. Collecting workspace buffer snapshots from each agent
      2. Building a pairwise Mutual Information matrix
      3. Evaluating random bipartitions to find the MIB
      4. Computing Phi* = whole_system_info - MIB_cut_info

    Runs every 100 spine cycles (~5 seconds at 20 Hz cognitive loop).
    """

    NUM_AGENTS = 32
    WINDOW_SIZE = 256         # Sliding window for MI estimation
    NUM_BIPARTITIONS = 50     # Random bipartitions to sample
    EPSILON = 1e-12

    # Thresholds
    PHI_GREEN = 1.0
    PHI_YELLOW = 0.0

    def __init__(self, num_agents: int = 32, seed: int = 42):
        self.num_agents = num_agents
        self.rng = np.random.default_rng(seed)

        # Sliding window of agent workspace snapshots
        # Each snapshot: [num_agents] vector of workspace "activity" values
        self._window: List[np.ndarray] = []

        # History of Phi* values
        self.phi_history: List[float] = []
        self.compute_times: List[float] = []

        # Pre-generate bipartitions for reproducibility
        self._bipartitions = self._generate_bipartitions()

    def _generate_bipartitions(self) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Pre-generate random bipartitions of the agent set.
        Each bipartition splits agents into two non-empty groups.
        """
        bipartitions = []
        for _ in range(self.NUM_BIPARTITIONS):
            # Random binary mask (ensure both sides non-empty)
            while True:
                mask = self.rng.integers(0, 2, size=self.num_agents).astype(bool)
                if mask.any() and (~mask).any():
                    break
            side_a = np.where(mask)[0]
            side_b = np.where(~mask)[0]
            bipartitions.append((side_a, side_b))
        return bipartitions

    def add_snapshot(self, workspace_values: np.ndarray):
        """
        Add a snapshot of all agents' workspace buffer values.

        Args:
            workspace_values: [num_agents] array of workspace activity
                              (e.g., first 8 bytes of each agent's WORKSPACE buffer
                               interpreted as float64, or a hash of buffer contents)
        """
        assert workspace_values.shape == (self.num_agents,), (
            f"Expected ({self.num_agents},), got {workspace_values.shape}")
        self._window.append(workspace_values.copy())
        if len(self._window) > self.WINDOW_SIZE:
            self._window.pop(0)

    def _compute_mi_matrix(self, data: np.ndarray) -> np.ndarray:
        """
        Compute pairwise Mutual Information matrix.

        Uses discretized histogram-based MI estimation.
        data: [T × N] matrix (T time steps, N agents)

        Returns: [N × N] MI matrix
        """
        N = data.shape[1]
        mi = np.zeros((N, N))

        # Discretize each agent's signal into bins
        num_bins = max(4, min(16, int(np.sqrt(data.shape[0]))))

        # Precompute histograms for each agent
        agent_bins = np.zeros_like(data, dtype=np.int32)
        for i in range(N):
            col = data[:, i]
            col_min, col_max = col.min(), col.max()
            if col_max - col_min < self.EPSILON:
                agent_bins[:, i] = 0
            else:
                normalized = (col - col_min) / (col_max - col_min + self.EPSILON)
                agent_bins[:, i] = np.clip(
                    (normalized * num_bins).astype(np.int32), 0, num_bins - 1
                )

        T = data.shape[0]

        # Pairwise MI via joint histogram
        for i in range(N):
            for j in range(i + 1, N):
                # Joint histogram
                joint = np.zeros((num_bins, num_bins))
                for t in range(T):
                    joint[agent_bins[t, i], agent_bins[t, j]] += 1
                joint /= T

                # Marginals
                p_i = joint.sum(axis=1)
                p_j = joint.sum(axis=0)

                # MI = Σ p(x,y) * log(p(x,y) / (p(x)*p(y)))
                mi_val = 0.0
                for bi in range(num_bins):
                    for bj in range(num_bins):
                        if joint[bi, bj] > self.EPSILON and p_i[bi] > self.EPSILON and p_j[bj] > self.EPSILON:
                            mi_val += joint[bi, bj] * np.log(
                                joint[bi, bj] / (p_i[bi] * p_j[bj])
                            )

                mi[i, j] = mi_val
                mi[j, i] = mi_val

        return mi

    def _compute_mi_matrix_fast(self, data: np.ndarray) -> np.ndarray:
        """
        VECTORIZED pairwise MI computation.
        Uses a correlation-based proxy for speed when N is large.

        MI(X,Y) ≈ -0.5 * log(1 - ρ²)  for Gaussian variables
        where ρ is Pearson correlation.

        Much faster than histogram-based: O(N²·T) instead of O(N²·T·B²)
        """
        N = data.shape[1]

        # Standardize
        data_std = data - data.mean(axis=0, keepdims=True)
        stds = data_std.std(axis=0, keepdims=True) + self.EPSILON
        data_std /= stds

        # Correlation matrix (fully vectorized)
        corr = (data_std.T @ data_std) / data.shape[0]

        # Clip to avoid log(0) or log(negative)
        corr = np.clip(corr, -0.9999, 0.9999)

        # MI proxy
        mi = -0.5 * np.log(1 - corr ** 2 + self.EPSILON)
        np.fill_diagonal(mi, 0.0)

        return mi

    def _evaluate_bipartition(self, mi: np.ndarray,
                               side_a: np.ndarray,
                               side_b: np.ndarray) -> float:
        """
        Compute the information lost when cutting the system at this bipartition.

        cut_info = Σ MI(i, j) for all i in side_a, j in side_b
        = the total mutual information across the cut

        Lower cut_info = closer to Minimum Information Bipartition (MIB)
        """
        # Extract cross-partition MI values (vectorized slicing)
        cross_mi = mi[np.ix_(side_a, side_b)]
        cut_info = cross_mi.sum()

        # Normalize by partition sizes (geometric mean normalization)
        norm = np.sqrt(len(side_a) * len(side_b))
        return cut_info / (norm + self.EPSILON)

    def compute_phi_star(self, active_mask: Optional[np.ndarray] = None) -> PhiResult:
        """
        ═══════════════════════════════════════════════════════════════════════
        Main Phi* computation.
        ═══════════════════════════════════════════════════════════════════════

        Args:
            active_mask: boolean array [num_agents] — which agents are active.
                         If None, use all agents with non-zero variance.

        Returns:
            PhiResult with approximate Phi*
        """
        start = time.perf_counter()

        if len(self._window) < 16:
            return PhiResult(
                phi_star=0.0, phi_normalized=0.0,
                mi_matrix=np.zeros((self.num_agents, self.num_agents)),
                mib_partition=([], []),
                mib_cut_info=0.0,
                active_agents=0,
                compute_time_ms=0.0,
                status="RED"
            )

        # Build data matrix [T × N]
        data = np.array(self._window)  # [T × num_agents]

        # Determine active agents
        if active_mask is None:
            variances = data.var(axis=0)
            active_mask = variances > self.EPSILON

        active_indices = np.where(active_mask)[0]
        num_active = len(active_indices)

        if num_active < 2:
            return PhiResult(
                phi_star=0.0, phi_normalized=0.0,
                mi_matrix=np.zeros((self.num_agents, self.num_agents)),
                mib_partition=([], []),
                mib_cut_info=0.0,
                active_agents=num_active,
                compute_time_ms=(time.perf_counter() - start) * 1000,
                status="RED"
            )

        # Extract active agent data only
        active_data = data[:, active_indices]  # [T × num_active]

        # ── Compute pairwise MI matrix ────────────────────────────────────
        # Use fast (correlation-based) for ≥16 agents, histogram for <16
        if num_active >= 16:
            mi_active = self._compute_mi_matrix_fast(active_data)
        else:
            mi_active = self._compute_mi_matrix(active_data)

        # ── Total system information ──────────────────────────────────────
        total_mi = mi_active.sum() / 2  # Upper triangle sum

        # ── Find Minimum Information Bipartition ──────────────────────────
        min_cut = float('inf')
        best_partition = ([], [])

        for side_a_full, side_b_full in self._bipartitions:
            # Map to active agent indices
            side_a = np.array([i for i in range(num_active)
                              if active_indices[i] in side_a_full])
            side_b = np.array([i for i in range(num_active)
                              if active_indices[i] in side_b_full])

            if len(side_a) == 0 or len(side_b) == 0:
                continue

            cut_info = self._evaluate_bipartition(mi_active, side_a, side_b)

            if cut_info < min_cut:
                min_cut = cut_info
                best_partition = (
                    active_indices[side_a].tolist(),
                    active_indices[side_b].tolist()
                )

        # ── Phi* = total_info - min_cut ───────────────────────────────────
        # High Phi* means even the weakest cut still has significant info flow
        phi_star = total_mi - min_cut if min_cut < float('inf') else 0.0

        # Normalize
        phi_normalized = phi_star / (np.log(num_active) + self.EPSILON)

        # Status
        if phi_star > self.PHI_GREEN:
            status = "GREEN"
        elif phi_star > self.PHI_YELLOW:
            status = "YELLOW"
        else:
            status = "RED"

        compute_ms = (time.perf_counter() - start) * 1000

        # Build full MI matrix
        mi_full = np.zeros((self.num_agents, self.num_agents))
        for i, ai in enumerate(active_indices):
            for j, aj in enumerate(active_indices):
                mi_full[ai, aj] = mi_active[i, j]

        result = PhiResult(
            phi_star=phi_star,
            phi_normalized=phi_normalized,
            mi_matrix=mi_full,
            mib_partition=best_partition,
            mib_cut_info=min_cut if min_cut < float('inf') else 0.0,
            active_agents=num_active,
            compute_time_ms=compute_ms,
            status=status
        )

        self.phi_history.append(phi_star)
        self.compute_times.append(compute_ms)

        return result

    def get_trend(self, window: int = 10) -> dict:
        """Get Phi* trend over recent history"""
        if len(self.phi_history) < 2:
            return {"trend": "insufficient_data", "values": self.phi_history}

        recent = self.phi_history[-window:]
        slope = np.polyfit(range(len(recent)), recent, 1)[0]

        return {
            "trend": "increasing" if slope > 0.01 else "decreasing" if slope < -0.01 else "stable",
            "slope": round(float(slope), 4),
            "mean": round(float(np.mean(recent)), 4),
            "std": round(float(np.std(recent)), 4),
            "last": round(float(recent[-1]), 4),
            "avg_compute_ms": round(float(np.mean(self.compute_times[-window:])), 2),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# BENCHMARK
# ═══════════════════════════════════════════════════════════════════════════════

def benchmark():
    """Benchmark the Phi* monitor"""
    print("═" * 60)
    print("  Φ* Consciousness Monitor — Performance Benchmark")
    print("═" * 60)

    monitor = PhiStarMonitor(num_agents=32, seed=42)
    rng = np.random.default_rng(123)

    # Simulate 256 snapshots with correlated agent activity
    print("\n  Generating 256 correlated snapshots...")
    base_signal = np.sin(np.linspace(0, 8 * np.pi, 256))

    for t in range(256):
        workspace = np.zeros(32)
        for i in range(32):
            # Agents have correlated activity (some clusters)
            cluster = i // 8
            workspace[i] = (
                base_signal[t] * (0.5 + 0.1 * cluster)  # Shared signal
                + rng.standard_normal() * 0.3            # Individual noise
                + np.sin(t * 0.1 * (cluster + 1)) * 0.2 # Cluster signal
            )
        monitor.add_snapshot(workspace)

    # Benchmark Phi* computation
    print("  Computing Phi*...")
    timings = []
    for _ in range(20):
        start = time.perf_counter()
        result = monitor.compute_phi_star()
        elapsed = (time.perf_counter() - start) * 1000
        timings.append(elapsed)

    timings = np.array(timings)
    print(f"\n  ═══ Results (20 evaluations) ═══")
    print(f"  Phi*:     {result.phi_star:.4f}")
    print(f"  Status:   {result.status}")
    print(f"  Active:   {result.active_agents} agents")
    print(f"  MIB cut:  {result.mib_cut_info:.4f}")
    print(f"  Mean:     {timings.mean():.2f} ms")
    print(f"  Median:   {np.median(timings):.2f} ms")
    print(f"  P95:      {np.percentile(timings, 95):.2f} ms")
    print(f"  Budget:   50.0 ms")
    print(f"  Headroom: {50.0 - timings.mean():.2f} ms ({(1 - timings.mean()/50)*100:.1f}%)")

    if timings.mean() < 50:
        print(f"\n  ✅ WITHIN BUDGET — {timings.mean():.2f}ms < 50ms target")
    else:
        print(f"\n  ❌ OVER BUDGET — {timings.mean():.2f}ms > 50ms target")

    trend = monitor.get_trend()
    print(f"\n  Trend: {trend}")


if __name__ == "__main__":
    benchmark()
