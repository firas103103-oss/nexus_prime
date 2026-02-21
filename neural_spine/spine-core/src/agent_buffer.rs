//! ═══════════════════════════════════════════════════════════════════════════════
//! FIX #5: AgentBufferSet — Seqlock-protected per-agent memory buffers
//! ═══════════════════════════════════════════════════════════════════════════════
//!
//! Each agent has 5 buffers × 1024 bytes = 5120 bytes:
//!   PERCEPT   (0) — sensory input from environment / interrupts
//!   WORKSPACE (1) — current working state (GWT competition input)
//!   BROADCAST (2) — received GWT broadcast (shared consciousness)
//!   ACTION    (3) — output decisions / motor commands
//!   META      (4) — genome, performance metrics, config
//!
//! The seqlock pattern prevents torn reads during hot-swap snapshots:
//! - Writer increments sequence to ODD before writing (signals "in progress")
//! - Writer increments sequence to EVEN after writing (signals "stable")
//! - Reader spins until it gets two matching EVEN sequence numbers
//! - Worst case: +200ns (one retry), acceptable within 500μs budget
//! ═══════════════════════════════════════════════════════════════════════════════

use std::sync::atomic::{AtomicU64, Ordering};
use crate::{NUM_AGENTS, BUFFER_SIZE, NUM_BUFFER_TYPES};

/// A single seqlock-protected buffer (1024 bytes + sequence counter)
#[repr(C, align(64))]
pub struct SeqlockBuffer {
    /// Sequence counter: even = stable, odd = writer active
    sequence: AtomicU64,
    /// Padding to separate sequence from data on different cache lines
    _pad: [u8; 56],
    /// The actual data buffer
    data: [u8; BUFFER_SIZE],
}

impl SeqlockBuffer {
    /// Write data with seqlock protection.
    ///
    /// Increments sequence to odd (writing), copies data, increments to even (stable).
    /// This is NOT reentrant — only ONE writer per buffer at a time.
    pub fn write(&self, src: &[u8]) {
        let len = src.len().min(BUFFER_SIZE);

        // Signal: write in progress (odd sequence)
        self.sequence.fetch_add(1, Ordering::Release);

        // Atomic fence ensures the sequence increment is visible before data write
        std::sync::atomic::fence(Ordering::Release);

        unsafe {
            let dst = self.data.as_ptr() as *mut u8;
            std::ptr::copy_nonoverlapping(src.as_ptr(), dst, len);
            // Zero remaining bytes if src is shorter than buffer
            if len < BUFFER_SIZE {
                std::ptr::write_bytes(dst.add(len), 0, BUFFER_SIZE - len);
            }
        }

        // Signal: write complete (even sequence)
        std::sync::atomic::fence(Ordering::Release);
        self.sequence.fetch_add(1, Ordering::Release);
    }

    /// Read data with seqlock protection.
    ///
    /// Retries until a consistent (non-torn) read is achieved.
    /// Returns the number of retries needed (0 = first attempt succeeded).
    pub fn read(&self, dest: &mut [u8]) -> u32 {
        let len = dest.len().min(BUFFER_SIZE);
        let mut retries = 0u32;

        loop {
            // Read sequence (must be even = stable)
            let seq1 = self.sequence.load(Ordering::Acquire);
            if seq1 & 1 != 0 {
                // Writer is active — spin
                retries += 1;
                std::hint::spin_loop();
                continue;
            }

            // Copy data
            unsafe {
                std::ptr::copy_nonoverlapping(
                    self.data.as_ptr(),
                    dest.as_mut_ptr(),
                    len,
                );
            }

            // Verify sequence hasn't changed
            std::sync::atomic::fence(Ordering::Acquire);
            let seq2 = self.sequence.load(Ordering::Acquire);

            if seq1 == seq2 {
                // Consistent read!
                return retries;
            }

            // Torn read — retry
            retries += 1;
            std::hint::spin_loop();
        }
    }

    /// Get the current sequence number (for monitoring)
    pub fn sequence_number(&self) -> u64 {
        self.sequence.load(Ordering::Relaxed)
    }

    /// Check if a writer is currently active
    pub fn is_writing(&self) -> bool {
        self.sequence.load(Ordering::Acquire) & 1 != 0
    }

    /// Get raw data pointer (for bulk operations — caller must handle synchronization)
    pub fn data_ptr(&self) -> *const u8 {
        self.data.as_ptr()
    }
}

/// Complete buffer set for one agent (5 buffers = 5120 bytes of data)
#[repr(C, align(64))]
pub struct AgentBufferSet {
    /// Agent ID (0-31)
    pub agent_id: u32,
    /// Whether this agent slot is active
    pub active: AtomicU64,
    /// Padding
    _pad: [u8; 48],
    /// The 5 seqlock-protected buffers
    pub buffers: [SeqlockBuffer; NUM_BUFFER_TYPES],
}

impl AgentBufferSet {
    /// Write to a specific buffer type with seqlock protection
    pub fn write_buffer(&self, buffer_type: usize, data: &[u8]) {
        if buffer_type < NUM_BUFFER_TYPES {
            self.buffers[buffer_type].write(data);
        }
    }

    /// Read from a specific buffer type with seqlock protection
    pub fn read_buffer(&self, buffer_type: usize, dest: &mut [u8]) -> u32 {
        if buffer_type < NUM_BUFFER_TYPES {
            self.buffers[buffer_type].read(dest)
        } else {
            0
        }
    }

    /// Snapshot ALL buffers atomically (each individually seqlock-protected)
    /// Returns: (data: [5 × 1024 bytes], total_retries)
    pub fn snapshot_all(&self) -> ([u8; 5120], u32) {
        let mut data = [0u8; 5120];
        let mut total_retries = 0u32;

        for i in 0..NUM_BUFFER_TYPES {
            let offset = i * BUFFER_SIZE;
            let retries = self.buffers[i].read(
                &mut data[offset..offset + BUFFER_SIZE]
            );
            total_retries += retries;
        }

        (data, total_retries)
    }
}

/// The full agent memory region: 32 agent buffer sets
#[repr(C)]
pub struct AgentMemoryRegion {
    pub agents: [AgentBufferSet; NUM_AGENTS],
}

impl AgentMemoryRegion {
    /// Initialize the memory region in-place (for shared memory)
    ///
    /// # Safety
    /// `ptr` must point to a valid, zero-initialized region of sufficient size.
    pub unsafe fn init_at(ptr: *mut Self) {
        std::ptr::write_bytes(ptr, 0, 1);
        for i in 0..NUM_AGENTS {
            (*ptr).agents[i].agent_id = i as u32;
            (*ptr).agents[i].active.store(0, Ordering::Relaxed);
        }
    }

    /// Activate an agent slot
    pub fn activate_agent(&self, agent_id: usize) {
        if agent_id < NUM_AGENTS {
            self.agents[agent_id].active.store(1, Ordering::Release);
        }
    }

    /// Deactivate an agent slot
    pub fn deactivate_agent(&self, agent_id: usize) {
        if agent_id < NUM_AGENTS {
            self.agents[agent_id].active.store(0, Ordering::Release);
        }
    }

    /// Count active agents
    pub fn active_count(&self) -> usize {
        self.agents.iter()
            .filter(|a| a.active.load(Ordering::Relaxed) != 0)
            .count()
    }

    /// Get metadata for monitoring
    pub fn agent_metadata(&self, agent_id: usize) -> Option<AgentMeta> {
        if agent_id >= NUM_AGENTS {
            return None;
        }
        let agent = &self.agents[agent_id];
        Some(AgentMeta {
            agent_id: agent.agent_id,
            active: agent.active.load(Ordering::Relaxed) != 0,
            sequences: [
                agent.buffers[0].sequence_number(),
                agent.buffers[1].sequence_number(),
                agent.buffers[2].sequence_number(),
                agent.buffers[3].sequence_number(),
                agent.buffers[4].sequence_number(),
            ],
        })
    }
}

/// Monitoring snapshot for a single agent
#[derive(Clone, Debug, serde::Serialize)]
pub struct AgentMeta {
    pub agent_id: u32,
    pub active: bool,
    pub sequences: [u64; 5],
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Arc;

    #[test]
    fn test_seqlock_write_read() {
        let region = Box::new(unsafe {
            let mut r = std::mem::MaybeUninit::<AgentMemoryRegion>::zeroed();
            AgentMemoryRegion::init_at(r.as_mut_ptr());
            r.assume_init()
        });

        let data = b"Hello, Neural Spine!";
        region.agents[0].write_buffer(0, data); // PERCEPT

        let mut read_buf = [0u8; 1024];
        let retries = region.agents[0].read_buffer(0, &mut read_buf);
        assert_eq!(retries, 0); // No contention
        assert_eq!(&read_buf[..data.len()], data);
    }

    #[test]
    fn test_snapshot_all() {
        let region = Box::new(unsafe {
            let mut r = std::mem::MaybeUninit::<AgentMemoryRegion>::zeroed();
            AgentMemoryRegion::init_at(r.as_mut_ptr());
            r.assume_init()
        });

        // Write to each buffer
        for i in 0..5 {
            let data = vec![i as u8; 100];
            region.agents[3].write_buffer(i, &data);
        }

        let (snapshot, retries) = region.agents[3].snapshot_all();
        assert_eq!(retries, 0);
        assert_eq!(snapshot[0], 0); // PERCEPT first byte
        assert_eq!(snapshot[1024], 1); // WORKSPACE first byte
        assert_eq!(snapshot[2048], 2); // BROADCAST first byte
    }

    #[test]
    fn test_concurrent_write_read() {
        let region = Arc::new(unsafe {
            let mut r = std::mem::MaybeUninit::<AgentMemoryRegion>::zeroed();
            AgentMemoryRegion::init_at(r.as_mut_ptr());
            r.assume_init()
        });

        let region_w = region.clone();
        let writer = std::thread::spawn(move || {
            for i in 0..1000u32 {
                let data = i.to_le_bytes();
                let mut buf = [0u8; 1024];
                buf[..4].copy_from_slice(&data);
                region_w.agents[0].write_buffer(0, &buf);
            }
        });

        let region_r = region.clone();
        let reader = std::thread::spawn(move || {
            let mut max_retries = 0u32;
            for _ in 0..1000 {
                let mut buf = [0u8; 1024];
                let retries = region_r.agents[0].read_buffer(0, &mut buf);
                if retries > max_retries {
                    max_retries = retries;
                }
                // The value should be a valid u32 (never torn)
                let val = u32::from_le_bytes([buf[0], buf[1], buf[2], buf[3]]);
                assert!(val < 1000); // Must be a value we actually wrote
            }
            max_retries
        });

        writer.join().unwrap();
        let max_retries = reader.join().unwrap();
        // With seqlock, retries should be rare
        println!("Max concurrent retries: {}", max_retries);
    }

    #[test]
    fn test_active_count() {
        let region = Box::new(unsafe {
            let mut r = std::mem::MaybeUninit::<AgentMemoryRegion>::zeroed();
            AgentMemoryRegion::init_at(r.as_mut_ptr());
            r.assume_init()
        });

        assert_eq!(region.active_count(), 0);
        region.activate_agent(0);
        region.activate_agent(15);
        region.activate_agent(31);
        assert_eq!(region.active_count(), 3);
        region.deactivate_agent(15);
        assert_eq!(region.active_count(), 2);
    }
}
