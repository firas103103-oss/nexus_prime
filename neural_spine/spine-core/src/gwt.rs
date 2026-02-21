//! ═══════════════════════════════════════════════════════════════════════════════
//! Global Workspace Theory (GWT) Broadcast Engine
//! ═══════════════════════════════════════════════════════════════════════════════
//!
//! Implements the cognitive broadcast cycle:
//! 1. Each agent writes its current workspace state (competition input)
//! 2. GWT engine scores all workspaces by salience = recency × relevance × surprise
//! 3. Top-K (K=3) winning workspaces are broadcast to ALL agents' BROADCAST buffers
//! 4. This creates "shared consciousness" — every agent aware of the collective's focus
//!
//! The broadcast cycle runs every cognitive tick (~500μs target on EPYC hardware).
//! ═══════════════════════════════════════════════════════════════════════════════

use crate::agent_buffer::AgentMemoryRegion;
use crate::{NUM_AGENTS, BUFFER_SIZE, BUF_WORKSPACE, BUF_BROADCAST};
use std::sync::atomic::Ordering;

/// Salience score for a workspace entry
#[derive(Clone, Debug, serde::Serialize)]
pub struct SalienceScore {
    pub agent_id: usize,
    /// Recency: how recently was this workspace updated (higher = more recent)
    pub recency: f64,
    /// Relevance: how much information content (non-zero bytes, entropy proxy)
    pub relevance: f64,
    /// Surprise: how different from the previous workspace state
    pub surprise: f64,
    /// Combined salience score
    pub salience: f64,
}

/// GWT Broadcast Engine state
pub struct GwtEngine {
    /// Number of top workspaces to broadcast
    top_k: usize,
    /// Previous workspace hashes for surprise computation
    prev_hashes: [u64; NUM_AGENTS],
    /// Previous broadcast sequence numbers for recency
    prev_sequences: [u64; NUM_AGENTS],
    /// Cycle counter
    pub cycle_count: u64,
    /// Last broadcast winners
    pub last_winners: Vec<SalienceScore>,
    /// Total broadcast time in nanoseconds (for monitoring)
    pub total_broadcast_ns: u64,
    /// Number of broadcasts performed
    pub broadcast_count: u64,
}

impl GwtEngine {
    pub fn new(top_k: usize) -> Self {
        Self {
            top_k,
            prev_hashes: [0u64; NUM_AGENTS],
            prev_sequences: [0u64; NUM_AGENTS],
            cycle_count: 0,
            last_winners: Vec::new(),
            total_broadcast_ns: 0,
            broadcast_count: 0,
        }
    }

    /// Run one GWT broadcast cycle.
    ///
    /// Reads all agents' WORKSPACE buffers, scores them by salience,
    /// and broadcasts the top-K winners to all agents' BROADCAST buffers.
    ///
    /// Returns the winning salience scores.
    pub fn broadcast_cycle(&mut self, region: &AgentMemoryRegion) -> Vec<SalienceScore> {
        let start = std::time::Instant::now();
        self.cycle_count += 1;

        let mut scores: Vec<SalienceScore> = Vec::with_capacity(NUM_AGENTS);
        let mut workspace_data: Vec<[u8; BUFFER_SIZE]> = Vec::with_capacity(NUM_AGENTS);

        // Phase 1: Read all workspace buffers and compute salience
        for agent_id in 0..NUM_AGENTS {
            let agent = &region.agents[agent_id];

            // Skip inactive agents
            if agent.active.load(Ordering::Relaxed) == 0 {
                workspace_data.push([0u8; BUFFER_SIZE]);
                continue;
            }

            // Read workspace with seqlock protection
            let mut ws = [0u8; BUFFER_SIZE];
            agent.buffers[BUF_WORKSPACE].read(&mut ws);
            let ws_copy = ws;

            // Compute salience components
            let seq = agent.buffers[BUF_WORKSPACE].sequence_number();
            let recency = if seq > self.prev_sequences[agent_id] {
                1.0 // Updated since last cycle
            } else {
                0.3 // Stale — reduced weight
            };

            let relevance = compute_relevance(&ws_copy);
            let hash = fast_hash(&ws_copy);
            let surprise = if hash != self.prev_hashes[agent_id] {
                1.0
            } else {
                0.1
            };

            let salience = recency * relevance * surprise;

            self.prev_hashes[agent_id] = hash;
            self.prev_sequences[agent_id] = seq;

            scores.push(SalienceScore {
                agent_id,
                recency,
                relevance,
                surprise,
                salience,
            });

            workspace_data.push(ws_copy);
        }

        // Phase 2: Select top-K by salience
        scores.sort_by(|a, b| b.salience.partial_cmp(&a.salience).unwrap_or(std::cmp::Ordering::Equal));
        let winners: Vec<SalienceScore> = scores.into_iter().take(self.top_k).collect();

        // Phase 3: Broadcast winners to ALL agents' BROADCAST buffers
        // Format: [winner_count: u8] [winner_0_agent_id: u8] [data...] [winner_1...] ...
        let mut broadcast_payload = [0u8; BUFFER_SIZE];
        broadcast_payload[0] = winners.len() as u8;

        let mut offset = 1usize;
        for winner in &winners {
            if offset + 1 + 128 > BUFFER_SIZE {
                break; // Don't overflow
            }
            broadcast_payload[offset] = winner.agent_id as u8;
            offset += 1;

            // Copy first 128 bytes of winner's workspace as summary
            let ws = &workspace_data[winner.agent_id];
            let copy_len = 128.min(BUFFER_SIZE - offset);
            broadcast_payload[offset..offset + copy_len].copy_from_slice(&ws[..copy_len]);
            offset += copy_len;
        }

        // Write broadcast to ALL active agents
        for agent_id in 0..NUM_AGENTS {
            if region.agents[agent_id].active.load(Ordering::Relaxed) != 0 {
                region.agents[agent_id].buffers[BUF_BROADCAST].write(&broadcast_payload);
            }
        }

        let elapsed_ns = start.elapsed().as_nanos() as u64;
        self.total_broadcast_ns += elapsed_ns;
        self.broadcast_count += 1;
        self.last_winners = winners.clone();

        winners
    }

    /// Average broadcast latency in microseconds
    pub fn avg_broadcast_us(&self) -> f64 {
        if self.broadcast_count == 0 {
            return 0.0;
        }
        (self.total_broadcast_ns as f64) / (self.broadcast_count as f64) / 1000.0
    }

    /// Get engine statistics for monitoring
    pub fn stats(&self) -> GwtStats {
        GwtStats {
            cycle_count: self.cycle_count,
            broadcast_count: self.broadcast_count,
            avg_broadcast_us: self.avg_broadcast_us(),
            last_winners: self.last_winners.clone(),
        }
    }
}

/// Compute information relevance (proxy: ratio of non-zero bytes × entropy estimate)
fn compute_relevance(data: &[u8]) -> f64 {
    let non_zero = data.iter().filter(|&&b| b != 0).count();
    if non_zero == 0 {
        return 0.0;
    }

    // Simple entropy proxy: count unique byte values
    let mut seen = [false; 256];
    let mut unique = 0usize;
    for &b in data {
        if !seen[b as usize] {
            seen[b as usize] = true;
            unique += 1;
        }
    }

    let density = non_zero as f64 / data.len() as f64;
    let diversity = unique as f64 / 256.0;

    // Combined relevance: geometric mean of density and diversity
    (density * diversity).sqrt()
}

/// Fast non-cryptographic hash for surprise detection
fn fast_hash(data: &[u8]) -> u64 {
    // FNV-1a hash
    let mut hash: u64 = 0xcbf29ce484222325;
    for &byte in data {
        hash ^= byte as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    hash
}

#[derive(Clone, Debug, serde::Serialize)]
pub struct GwtStats {
    pub cycle_count: u64,
    pub broadcast_count: u64,
    pub avg_broadcast_us: f64,
    pub last_winners: Vec<SalienceScore>,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_broadcast_cycle() {
        let region = Box::new(unsafe {
            let mut r = std::mem::MaybeUninit::<AgentMemoryRegion>::zeroed();
            AgentMemoryRegion::init_at(r.as_mut_ptr());
            r.assume_init()
        });

        // Activate 4 agents
        for i in 0..4 {
            region.activate_agent(i);
        }

        // Write workspace data
        region.agents[0].write_buffer(BUF_WORKSPACE, &[42u8; 100]);
        region.agents[1].write_buffer(BUF_WORKSPACE, &[1, 2, 3, 4, 5]);
        region.agents[2].write_buffer(BUF_WORKSPACE, &[0u8; 50]); // empty-ish
        region.agents[3].write_buffer(BUF_WORKSPACE, &(0..200).map(|i| i as u8).collect::<Vec<_>>());

        let mut engine = GwtEngine::new(2);
        let winners = engine.broadcast_cycle(&region);

        assert_eq!(winners.len(), 2);
        // Agent 3 should win (highest diversity/relevance)
        assert_eq!(winners[0].agent_id, 3);

        // Verify broadcast was written to all active agents
        let mut broadcast = [0u8; BUFFER_SIZE];
        region.agents[0].read_buffer(BUF_BROADCAST, &mut broadcast);
        assert!(broadcast[0] > 0); // winner_count > 0
    }

    #[test]
    fn test_relevance_empty() {
        let data = [0u8; 1024];
        assert_eq!(compute_relevance(&data), 0.0);
    }

    #[test]
    fn test_relevance_diverse() {
        let data: Vec<u8> = (0..=255).cycle().take(1024).collect();
        let rel = compute_relevance(&data);
        assert!(rel > 0.5); // High density + high diversity
    }

    #[test]
    fn test_fast_hash_different() {
        let a = [1u8; 100];
        let b = [2u8; 100];
        assert_ne!(fast_hash(&a), fast_hash(&b));
    }
}
