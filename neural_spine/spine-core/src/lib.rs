//! ═══════════════════════════════════════════════════════════════════════════════
//! NEXUS PRIME Neural Spine — Core Library
//! ═══════════════════════════════════════════════════════════════════════════════
//! Lock-free shared memory cognitive backbone for 32-agent collective.
//!
//! Modules:
//!   ring_buffer    — SPSC interrupt ring buffer with page-spacer (Fix #4)
//!   agent_buffer   — Seqlock-protected per-agent buffer sets (Fix #5)
//!   gwt            — Global Workspace Theory broadcast engine
//!   consolidation  — Memory pruning with bulk-copy optimization (Fix #2)
//!   shm            — Shared memory allocation with hugepage support (Fix #3)
//!   ffi            — C ABI exports for Python integration
//! ═══════════════════════════════════════════════════════════════════════════════

pub mod ring_buffer;
pub mod agent_buffer;
pub mod gwt;
pub mod consolidation;
pub mod shm;
pub mod ffi;

/// Number of agents in the collective
pub const NUM_AGENTS: usize = 32;
/// Size of each individual buffer (PERCEPT, WORKSPACE, BROADCAST, ACTION, META)
pub const BUFFER_SIZE: usize = 1024;
/// Number of buffer types per agent
pub const NUM_BUFFER_TYPES: usize = 5;
/// Total bytes per agent buffer set
pub const AGENT_BUFFER_TOTAL: usize = BUFFER_SIZE * NUM_BUFFER_TYPES; // 5120
/// Ring buffer capacity (must be power of 2)
pub const RING_CAPACITY: usize = 4096;

/// Buffer type indices
pub const BUF_PERCEPT: usize = 0;
pub const BUF_WORKSPACE: usize = 1;
pub const BUF_BROADCAST: usize = 2;
pub const BUF_ACTION: usize = 3;
pub const BUF_META: usize = 4;
