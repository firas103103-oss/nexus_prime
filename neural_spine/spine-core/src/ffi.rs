//! ═══════════════════════════════════════════════════════════════════════════════
//! FFI: C ABI exports for Python integration
//! ═══════════════════════════════════════════════════════════════════════════════
//!
//! Exposes shared memory operations to Python via ctypes/cffi.
//! The Python reflex agents use these functions to read/write agent buffers
//! and interact with the ring buffer without serialization overhead.
//! ═══════════════════════════════════════════════════════════════════════════════

use crate::agent_buffer::AgentMemoryRegion;
use crate::ring_buffer::{InterruptRingBuffer, InterruptEntry};
use crate::shm::SharedMemoryRegion;

/// Global shared memory pointers (set during init)
static mut AGENT_REGION: Option<*mut AgentMemoryRegion> = None;
static mut RING_BUFFER: Option<*mut InterruptRingBuffer> = None;
static mut SHM_REGION: Option<SharedMemoryRegion> = None;

/// Initialize shared memory and return a handle.
/// Returns 0 on success, -1 on failure.
#[no_mangle]
pub extern "C" fn spine_init(shm_name: *const std::ffi::c_char) -> i32 {
    let name = if shm_name.is_null() {
        "/nexus_spine"
    } else {
        unsafe {
            match std::ffi::CStr::from_ptr(shm_name).to_str() {
                Ok(s) => s,
                Err(_) => "/nexus_spine",
            }
        }
    };

    let total_size = crate::shm::required_shm_size();

    match SharedMemoryRegion::allocate(total_size, Some(name)) {
        Ok(region) => {
            unsafe {
                let ptr = region.ptr;

                // Initialize agent memory region at the start
                let agent_ptr = ptr as *mut AgentMemoryRegion;
                AgentMemoryRegion::init_at(agent_ptr);
                AGENT_REGION = Some(agent_ptr);

                // Initialize ring buffer after agent region
                let agent_size = std::mem::size_of::<AgentMemoryRegion>();
                let ring_ptr = ptr.add(agent_size) as *mut InterruptRingBuffer;
                InterruptRingBuffer::init_at(ring_ptr);
                RING_BUFFER = Some(ring_ptr);

                SHM_REGION = Some(region);
            }
            0
        }
        Err(e) => {
            eprintln!("[FFI] spine_init failed: {}", e);
            -1
        }
    }
}

/// Attach to existing shared memory (for client processes)
#[no_mangle]
pub extern "C" fn spine_attach(shm_name: *const std::ffi::c_char) -> i32 {
    let name = if shm_name.is_null() {
        "/nexus_spine"
    } else {
        unsafe {
            match std::ffi::CStr::from_ptr(shm_name).to_str() {
                Ok(s) => s,
                Err(_) => "/nexus_spine",
            }
        }
    };

    let total_size = crate::shm::required_shm_size();

    match SharedMemoryRegion::attach(name, total_size) {
        Ok(region) => {
            unsafe {
                let ptr = region.ptr;
                AGENT_REGION = Some(ptr as *mut AgentMemoryRegion);

                let agent_size = std::mem::size_of::<AgentMemoryRegion>();
                RING_BUFFER = Some(ptr.add(agent_size) as *mut InterruptRingBuffer);

                SHM_REGION = Some(region);
            }
            0
        }
        Err(e) => {
            eprintln!("[FFI] spine_attach failed: {}", e);
            -1
        }
    }
}

/// Write data to an agent's buffer with seqlock protection
#[no_mangle]
pub extern "C" fn spine_write_buffer(
    agent_id: u32,
    buffer_type: u32,
    data: *const u8,
    len: u32,
) -> i32 {
    unsafe {
        let region = match AGENT_REGION {
            Some(ptr) => &*ptr,
            None => return -1,
        };

        if agent_id >= 32 || buffer_type >= 5 || data.is_null() {
            return -2;
        }

        let slice = std::slice::from_raw_parts(data, len as usize);
        region.agents[agent_id as usize].write_buffer(buffer_type as usize, slice);
        0
    }
}

/// Read data from an agent's buffer with seqlock protection
/// Returns the number of retries needed (0 = no contention)
#[no_mangle]
pub extern "C" fn spine_read_buffer(
    agent_id: u32,
    buffer_type: u32,
    dest: *mut u8,
    len: u32,
) -> i32 {
    unsafe {
        let region = match AGENT_REGION {
            Some(ptr) => &*ptr,
            None => return -1,
        };

        if agent_id >= 32 || buffer_type >= 5 || dest.is_null() {
            return -2;
        }

        let slice = std::slice::from_raw_parts_mut(dest, len as usize);
        region.agents[agent_id as usize].read_buffer(buffer_type as usize, slice) as i32
    }
}

/// Activate an agent slot
#[no_mangle]
pub extern "C" fn spine_activate_agent(agent_id: u32) -> i32 {
    unsafe {
        let region = match AGENT_REGION {
            Some(ptr) => &*ptr,
            None => return -1,
        };
        if agent_id >= 32 { return -2; }
        region.activate_agent(agent_id as usize);
        0
    }
}

/// Push an interrupt to the ring buffer
#[no_mangle]
pub extern "C" fn spine_push_interrupt(
    source: u16,
    target: u16,
    interrupt_type: u8,
    priority: u8,
    payload: *const u8,
    payload_len: u32,
) -> i32 {
    unsafe {
        let ring = match RING_BUFFER {
            Some(ptr) => &*ptr,
            None => return -1,
        };

        let mut entry = InterruptEntry::default();
        entry.source_agent = source;
        entry.target_agent = target;
        entry.interrupt_type = interrupt_type;
        entry.priority = priority;

        // Get timestamp
        let mut ts = libc::timespec { tv_sec: 0, tv_nsec: 0 };
        libc::clock_gettime(libc::CLOCK_MONOTONIC, &mut ts);
        entry.timestamp = (ts.tv_sec as u64) * 1_000_000_000 + (ts.tv_nsec as u64);

        if !payload.is_null() && payload_len > 0 {
            let copy_len = (payload_len as usize).min(44);
            std::ptr::copy_nonoverlapping(payload, entry.payload.as_mut_ptr(), copy_len);
        }

        if ring.push(entry) { 0 } else { -3 } // -3 = buffer full
    }
}

/// Pop an interrupt from the ring buffer
/// Returns 0 if an entry was popped, 1 if empty
#[no_mangle]
pub extern "C" fn spine_pop_interrupt(
    source: *mut u16,
    target: *mut u16,
    interrupt_type: *mut u8,
    priority: *mut u8,
    payload: *mut u8,
    timestamp: *mut u64,
) -> i32 {
    unsafe {
        let ring = match RING_BUFFER {
            Some(ptr) => &*ptr,
            None => return -1,
        };

        match ring.pop() {
            Some(entry) => {
                if !source.is_null() { *source = entry.source_agent; }
                if !target.is_null() { *target = entry.target_agent; }
                if !interrupt_type.is_null() { *interrupt_type = entry.interrupt_type; }
                if !priority.is_null() { *priority = entry.priority; }
                if !payload.is_null() {
                    std::ptr::copy_nonoverlapping(entry.payload.as_ptr(), payload, 44);
                }
                if !timestamp.is_null() { *timestamp = entry.timestamp; }
                0
            }
            None => 1, // Empty
        }
    }
}

/// Get active agent count
#[no_mangle]
pub extern "C" fn spine_active_count() -> i32 {
    unsafe {
        match AGENT_REGION {
            Some(ptr) => (*ptr).active_count() as i32,
            None => -1,
        }
    }
}

/// Get ring buffer length
#[no_mangle]
pub extern "C" fn spine_ring_len() -> i32 {
    unsafe {
        match RING_BUFFER {
            Some(ptr) => (*ptr).len() as i32,
            None => -1,
        }
    }
}
