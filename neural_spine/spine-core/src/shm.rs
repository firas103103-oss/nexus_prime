//! ═══════════════════════════════════════════════════════════════════════════════
//! FIX #3: Shared Memory Allocation with Hugepage Support
//! ═══════════════════════════════════════════════════════════════════════════════
//!
//! Allocates the shared memory region used by all agents and the spine.
//! Supports:
//!   - Regular mmap (always available)
//!   - 2MB Hugepages (when configured via kernel_tune.sh)
//!   - POSIX shm for cross-process sharing
//!
//! On single-NUMA VM: allocates on the only node (node0)
//! On multi-NUMA bare metal: would use mbind() for NUMA-aware allocation
//! ═══════════════════════════════════════════════════════════════════════════════

use libc;
use std::ptr;

/// Shared memory region descriptor
pub struct SharedMemoryRegion {
    /// Pointer to the mapped memory
    pub ptr: *mut u8,
    /// Size in bytes
    pub size: usize,
    /// Whether hugepages were used
    pub hugepages: bool,
    /// Whether this is a named POSIX shm segment
    pub shm_name: Option<String>,
}

impl SharedMemoryRegion {
    /// Allocate a shared memory region.
    ///
    /// Tries hugepages first, falls back to regular mmap.
    /// If `shm_name` is provided, creates a named POSIX shared memory segment
    /// that other processes can attach to.
    pub fn allocate(size: usize, shm_name: Option<&str>) -> Result<Self, String> {
        // Try named POSIX shm first (for cross-process sharing)
        if let Some(name) = shm_name {
            return Self::allocate_posix_shm(size, name);
        }

        // Try hugepages first
        match Self::allocate_hugepages(size) {
            Ok(region) => {
                eprintln!("[SHM] Allocated {} bytes with hugepages", size);
                Ok(region)
            }
            Err(e) => {
                eprintln!("[SHM] Hugepage allocation failed ({}), falling back to regular mmap", e);
                Self::allocate_regular(size)
            }
        }
    }

    /// Allocate using 2MB hugepages
    fn allocate_hugepages(size: usize) -> Result<Self, String> {
        // Round up to 2MB boundary
        let hugepage_size = 2 * 1024 * 1024;
        let aligned_size = (size + hugepage_size - 1) & !(hugepage_size - 1);

        unsafe {
            let ptr = libc::mmap(
                ptr::null_mut(),
                aligned_size,
                libc::PROT_READ | libc::PROT_WRITE,
                libc::MAP_PRIVATE | libc::MAP_ANONYMOUS | libc::MAP_HUGETLB,
                -1,
                0,
            );

            if ptr == libc::MAP_FAILED {
                return Err(format!("mmap MAP_HUGETLB failed: {}", std::io::Error::last_os_error()));
            }

            // Lock pages to prevent swapping
            libc::mlock(ptr, aligned_size);

            Ok(SharedMemoryRegion {
                ptr: ptr as *mut u8,
                size: aligned_size,
                hugepages: true,
                shm_name: None,
            })
        }
    }

    /// Allocate using regular mmap (fallback)
    fn allocate_regular(size: usize) -> Result<Self, String> {
        // Align to page boundary
        let page_size = 4096;
        let aligned_size = (size + page_size - 1) & !(page_size - 1);

        unsafe {
            let ptr = libc::mmap(
                ptr::null_mut(),
                aligned_size,
                libc::PROT_READ | libc::PROT_WRITE,
                libc::MAP_PRIVATE | libc::MAP_ANONYMOUS | libc::MAP_POPULATE,
                -1,
                0,
            );

            if ptr == libc::MAP_FAILED {
                return Err(format!("mmap failed: {}", std::io::Error::last_os_error()));
            }

            // Lock pages to prevent swapping
            libc::mlock(ptr, aligned_size);

            Ok(SharedMemoryRegion {
                ptr: ptr as *mut u8,
                size: aligned_size,
                hugepages: false,
                shm_name: None,
            })
        }
    }

    /// Allocate named POSIX shared memory (for cross-process sharing)
    fn allocate_posix_shm(size: usize, name: &str) -> Result<Self, String> {
        let page_size = 4096;
        let aligned_size = (size + page_size - 1) & !(page_size - 1);

        let c_name = std::ffi::CString::new(name)
            .map_err(|e| format!("Invalid shm name: {}", e))?;

        unsafe {
            // Create or open the shared memory segment
            let fd = libc::shm_open(
                c_name.as_ptr(),
                libc::O_CREAT | libc::O_RDWR,
                0o600,
            );

            if fd < 0 {
                return Err(format!("shm_open failed: {}", std::io::Error::last_os_error()));
            }

            // Set the size
            if libc::ftruncate(fd, aligned_size as libc::off_t) < 0 {
                libc::close(fd);
                return Err(format!("ftruncate failed: {}", std::io::Error::last_os_error()));
            }

            // Map it
            let ptr = libc::mmap(
                ptr::null_mut(),
                aligned_size,
                libc::PROT_READ | libc::PROT_WRITE,
                libc::MAP_SHARED,
                fd,
                0,
            );

            libc::close(fd); // fd no longer needed after mmap

            if ptr == libc::MAP_FAILED {
                return Err(format!("mmap shm failed: {}", std::io::Error::last_os_error()));
            }

            // Zero-initialize
            libc::memset(ptr, 0, aligned_size);
            // Lock pages
            libc::mlock(ptr, aligned_size);

            eprintln!("[SHM] Allocated {} bytes as POSIX shm '{}'", aligned_size, name);

            Ok(SharedMemoryRegion {
                ptr: ptr as *mut u8,
                size: aligned_size,
                hugepages: false,
                shm_name: Some(name.to_string()),
            })
        }
    }

    /// Attach to an existing named shared memory segment
    pub fn attach(name: &str, size: usize) -> Result<Self, String> {
        let page_size = 4096;
        let aligned_size = (size + page_size - 1) & !(page_size - 1);

        let c_name = std::ffi::CString::new(name)
            .map_err(|e| format!("Invalid shm name: {}", e))?;

        unsafe {
            let fd = libc::shm_open(
                c_name.as_ptr(),
                libc::O_RDWR,
                0o600,
            );

            if fd < 0 {
                return Err(format!("shm_open attach failed: {}", std::io::Error::last_os_error()));
            }

            let ptr = libc::mmap(
                ptr::null_mut(),
                aligned_size,
                libc::PROT_READ | libc::PROT_WRITE,
                libc::MAP_SHARED,
                fd,
                0,
            );

            libc::close(fd);

            if ptr == libc::MAP_FAILED {
                return Err(format!("mmap attach failed: {}", std::io::Error::last_os_error()));
            }

            eprintln!("[SHM] Attached to POSIX shm '{}' ({} bytes)", name, aligned_size);

            Ok(SharedMemoryRegion {
                ptr: ptr as *mut u8,
                size: aligned_size,
                hugepages: false,
                shm_name: Some(name.to_string()),
            })
        }
    }
}

impl Drop for SharedMemoryRegion {
    fn drop(&mut self) {
        unsafe {
            libc::munmap(self.ptr as *mut libc::c_void, self.size);
            // Only unlink named shm from the allocator (not attachees)
            // Caller must explicitly unlink if needed
        }
    }
}

// SharedMemoryRegion contains a raw pointer but is safe to send across threads
// because the pointer refers to a memory-mapped region that doesn't alias
unsafe impl Send for SharedMemoryRegion {}
unsafe impl Sync for SharedMemoryRegion {}

/// Calculate the total shared memory size needed for the Neural Spine
pub fn required_shm_size() -> usize {
    let agent_region = std::mem::size_of::<crate::agent_buffer::AgentMemoryRegion>();
    let ring_buffer = std::mem::size_of::<crate::ring_buffer::InterruptRingBuffer>();

    // Add some padding for alignment
    let total = agent_region + ring_buffer + 4096;
    eprintln!("[SHM] Required: agent_region={} + ring_buffer={} + pad=4096 = {} bytes",
             agent_region, ring_buffer, total);
    total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_regular_allocation() {
        let region = SharedMemoryRegion::allocate(4096, None).unwrap();
        assert!(!region.ptr.is_null());
        assert!(region.size >= 4096);
        assert!(!region.hugepages);

        // Write and read back
        unsafe {
            *region.ptr = 42;
            assert_eq!(*region.ptr, 42);
        }
    }

    #[test]
    fn test_shm_size_calculation() {
        let size = required_shm_size();
        assert!(size > 0);
        println!("Required SHM size: {} bytes ({:.2} MB)", size, size as f64 / (1024.0 * 1024.0));
    }
}
