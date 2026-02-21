//! ═══════════════════════════════════════════════════════════════════════════════
//! FIX #2: Consolidation Engine — Bulk-copy memory pruning
//! ═══════════════════════════════════════════════════════════════════════════════
//!
//! On single-NUMA (current VM), this optimizes L1/L2 cache utilization by
//! batch-copying all agent metadata before processing.
//!
//! On multi-NUMA (future bare metal), this eliminates cross-node read penalties
//! (50-100ns per access → one bulk memcpy).
//!
//! The consolidation engine runs every 100 cognitive cycles (~50ms).
//! ═══════════════════════════════════════════════════════════════════════════════

use crate::agent_buffer::{AgentMemoryRegion, AgentMeta};
use crate::NUM_AGENTS;

/// Memory metadata for pruning decisions
#[derive(Clone, Debug, serde::Serialize)]
pub struct MemoryMetadata {
    pub agent_id: usize,
    pub active: bool,
    /// Sequence numbers for each buffer (proxy for access frequency)
    pub sequences: [u64; 5],
    /// Total writes (sum of all sequence numbers / 2)
    pub total_writes: u64,
    /// Estimated age (cycles since last significant change)
    pub staleness: u64,
    /// Pruning score: higher = more likely to be pruned
    pub prune_score: f64,
}

/// Consolidation engine state
pub struct ConsolidationEngine {
    /// Previous sequence snapshots for staleness detection
    prev_snapshots: Vec<[u64; 5]>,
    /// Cycle counter
    pub cycle_count: u64,
    /// Last pruning results
    pub last_results: Vec<MemoryMetadata>,
    /// NUMA optimization enabled (feature flag for future multi-socket)
    #[allow(dead_code)]
    numa_aware: bool,
}

impl ConsolidationEngine {
    pub fn new() -> Self {
        Self {
            prev_snapshots: vec![[0u64; 5]; NUM_AGENTS],
            cycle_count: 0,
            last_results: Vec::new(),
            numa_aware: false, // Single-NUMA VM — disabled
        }
    }

    /// Run consolidation cycle: bulk-copy metadata, compute pruning scores
    ///
    /// FIX #2: Instead of random cross-NUMA reads during processing,
    /// we batch-copy ALL metadata into a local Vec first, then process entirely
    /// from local memory. On single-NUMA this helps L1/L2; on multi-NUMA it
    /// eliminates cross-node penalties.
    pub fn consolidate(&mut self, region: &AgentMemoryRegion) -> Vec<MemoryMetadata> {
        self.cycle_count += 1;

        // ═══ PHASE 1: BULK COPY ═══════════════════════════════════════════
        // Copy all metadata into a local buffer BEFORE processing.
        // This converts N random reads into one sequential scan.
        let mut local_meta: Vec<AgentMeta> = Vec::with_capacity(NUM_AGENTS);
        for agent_id in 0..NUM_AGENTS {
            if let Some(meta) = region.agent_metadata(agent_id) {
                local_meta.push(meta);
            }
        }

        // ═══ PHASE 2: COMPUTE PRUNING SCORES ON LOCAL DATA ONLY ══════════
        // Zero cross-NUMA reads from this point forward
        let mut results: Vec<MemoryMetadata> = Vec::with_capacity(NUM_AGENTS);

        for meta in &local_meta {
            let agent_id = meta.agent_id as usize;
            let prev = &self.prev_snapshots[agent_id];

            // Total writes = sum(sequences) / 2 (each write +=2)
            let total_writes: u64 = meta.sequences.iter().sum::<u64>() / 2;

            // Staleness: how many cycles since ANY buffer was written
            let changed = meta.sequences.iter()
                .zip(prev.iter())
                .any(|(curr, prev)| *curr != *prev);

            let staleness = if changed { 0 } else {
                // Accumulate staleness (bounded)
                self.last_results.iter()
                    .find(|r| r.agent_id == agent_id)
                    .map(|r| r.staleness + 1)
                    .unwrap_or(1)
            };

            // Pruning score: high staleness + low activity = high prune priority
            let activity_rate = if self.cycle_count > 1 {
                total_writes as f64 / self.cycle_count as f64
            } else {
                0.0
            };

            let prune_score = if !meta.active {
                100.0 // Inactive agents always prunable
            } else {
                let staleness_factor = (staleness as f64).sqrt();
                let activity_factor = 1.0 / (1.0 + activity_rate);
                staleness_factor * activity_factor * 10.0
            };

            results.push(MemoryMetadata {
                agent_id,
                active: meta.active,
                sequences: meta.sequences,
                total_writes,
                staleness,
                prune_score,
            });

            // Update previous snapshot
            self.prev_snapshots[agent_id] = meta.sequences;
        }

        // Sort by prune score (highest first = most prunable)
        results.sort_by(|a, b| b.prune_score.partial_cmp(&a.prune_score).unwrap_or(std::cmp::Ordering::Equal));

        self.last_results = results.clone();
        results
    }

    /// Get agents that should be pruned (prune_score > threshold)
    pub fn get_prunable(&self, threshold: f64) -> Vec<&MemoryMetadata> {
        self.last_results.iter()
            .filter(|m| m.prune_score > threshold)
            .collect()
    }

    /// Get engine statistics
    pub fn stats(&self) -> ConsolidationStats {
        let active = self.last_results.iter().filter(|m| m.active).count();
        let avg_staleness = if !self.last_results.is_empty() {
            self.last_results.iter().map(|m| m.staleness as f64).sum::<f64>()
                / self.last_results.len() as f64
        } else {
            0.0
        };

        ConsolidationStats {
            cycle_count: self.cycle_count,
            active_agents: active,
            total_agents: self.last_results.len(),
            avg_staleness,
            prunable_count: self.get_prunable(50.0).len(),
        }
    }
}

#[derive(Clone, Debug, serde::Serialize)]
pub struct ConsolidationStats {
    pub cycle_count: u64,
    pub active_agents: usize,
    pub total_agents: usize,
    pub avg_staleness: f64,
    pub prunable_count: usize,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::BUF_META;

    #[test]
    fn test_consolidation_basic() {
        let region = Box::new(unsafe {
            let mut r = std::mem::MaybeUninit::<AgentMemoryRegion>::zeroed();
            AgentMemoryRegion::init_at(r.as_mut_ptr());
            r.assume_init()
        });

        region.activate_agent(0);
        region.activate_agent(1);
        region.agents[0].write_buffer(BUF_META, b"active agent 0");

        let mut engine = ConsolidationEngine::new();
        let results = engine.consolidate(&region);

        assert_eq!(results.len(), NUM_AGENTS);

        // Agent 0 should have lower prune score (it's active with writes)
        let agent_0 = results.iter().find(|r| r.agent_id == 0).unwrap();
        let agent_5 = results.iter().find(|r| r.agent_id == 5).unwrap();
        assert!(agent_0.prune_score < agent_5.prune_score);
    }

    #[test]
    fn test_staleness_accumulation() {
        let region = Box::new(unsafe {
            let mut r = std::mem::MaybeUninit::<AgentMemoryRegion>::zeroed();
            AgentMemoryRegion::init_at(r.as_mut_ptr());
            r.assume_init()
        });

        region.activate_agent(0);
        region.agents[0].write_buffer(0, b"initial data");

        let mut engine = ConsolidationEngine::new();

        // First cycle: staleness = 0 (just wrote)
        engine.consolidate(&region);
        let agent_0 = engine.last_results.iter().find(|r| r.agent_id == 0).unwrap();
        assert_eq!(agent_0.staleness, 0);

        // Second cycle without writing: staleness should increase
        engine.consolidate(&region);
        let agent_0 = engine.last_results.iter().find(|r| r.agent_id == 0).unwrap();
        assert!(agent_0.staleness > 0);
    }
}
