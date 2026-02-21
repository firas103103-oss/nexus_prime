#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# Neural Spine — Kernel Tuning Script (Fix #1)
# ═══════════════════════════════════════════════════════════════════════════════
#
# TARGET: AMD EPYC-Genoa VM, 12 vCPUs, single NUMA node, 23GB RAM
#
# WHAT THIS DOES:
#   1. Allocates hugepages (2MB pages) for shared memory
#   2. Disables Transparent Huge Pages (THP) — THP causes latency spikes
#   3. Sets sysctl network/memory tuning
#   4. Validates the configuration
#
# USAGE:
#   sudo ./kernel_tune.sh [--apply|--check|--revert]
#
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

# Hugepages: 512 × 2MB = 1GB reserved for shared memory
HUGEPAGES_TARGET=512
HUGEPAGE_SIZE_KB=2048

# Shared memory minimum (bytes) — enough for 32 agents × 5 buffers × 1KB + ring buffer
SHM_MIN=$((256 * 1024 * 1024))  # 256MB

# CPU pinning layout (for reference — Docker handles actual pinning)
# Spine server:  cores 0-2
# Redis coord:   core  3
# Agent workers:  cores 4-11

# ═══════════════════════════════════════════════════════════════════════════════
# Check Mode
# ═══════════════════════════════════════════════════════════════════════════════

check_system() {
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Neural Spine — System Configuration Check"
    echo "═══════════════════════════════════════════════════════════════"

    # CPU
    echo ""
    info "CPU: $(lscpu | grep 'Model name' | sed 's/.*: *//')"
    info "Cores: $(nproc)"
    info "NUMA nodes: $(lscpu | grep 'NUMA node(s)' | awk '{print $NF}')"

    # Hugepages
    echo ""
    local current_hp=0
    if [[ -f /sys/kernel/mm/hugepages/hugepages-${HUGEPAGE_SIZE_KB}kB/nr_hugepages ]]; then
        current_hp=$(cat /sys/kernel/mm/hugepages/hugepages-${HUGEPAGE_SIZE_KB}kB/nr_hugepages)
    fi
    if [[ $current_hp -ge $HUGEPAGES_TARGET ]]; then
        info "Hugepages: ${current_hp}/${HUGEPAGES_TARGET} ✅"
    else
        warn "Hugepages: ${current_hp}/${HUGEPAGES_TARGET} ❌ (need ${HUGEPAGES_TARGET})"
    fi

    # THP
    local thp_status="unknown"
    if [[ -f /sys/kernel/mm/transparent_hugepage/enabled ]]; then
        thp_status=$(cat /sys/kernel/mm/transparent_hugepage/enabled)
        if echo "$thp_status" | grep -q '\[never\]'; then
            info "THP: disabled ✅"
        else
            warn "THP: enabled ❌ (causes latency spikes)"
        fi
    else
        warn "THP: status file not found"
    fi

    # SHM
    local shm_max=$(cat /proc/sys/kernel/shmmax 2>/dev/null || echo 0)
    if [[ $shm_max -ge $SHM_MIN ]]; then
        info "SHMMAX: $(numfmt --to=iec $shm_max) ✅"
    else
        warn "SHMMAX: $(numfmt --to=iec $shm_max) ❌ (need $(numfmt --to=iec $SHM_MIN))"
    fi

    # Memory
    echo ""
    local mem_total=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    local mem_avail=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
    info "Memory: $(numfmt --to=iec --from=iec "${mem_total}K") total, $(numfmt --to=iec --from=iec "${mem_avail}K") available"

    # Shared memory mount
    local shm_size=$(df /dev/shm 2>/dev/null | tail -1 | awk '{print $2}')
    if [[ -n "$shm_size" ]]; then
        info "/dev/shm: $(numfmt --to=iec --from=iec "${shm_size}K")"
    fi

    # Kernel
    echo ""
    info "Kernel: $(uname -r)"
    info "Governor: $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo 'N/A (VM)')"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Apply Mode
# ═══════════════════════════════════════════════════════════════════════════════

apply_tuning() {
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Neural Spine — Applying Kernel Tuning"
    echo "═══════════════════════════════════════════════════════════════"

    if [[ $EUID -ne 0 ]]; then
        error "Must run as root: sudo $0 --apply"
        exit 1
    fi

    # 1. Hugepages
    echo ""
    info "Allocating hugepages..."
    if [[ -f /sys/kernel/mm/hugepages/hugepages-${HUGEPAGE_SIZE_KB}kB/nr_hugepages ]]; then
        echo $HUGEPAGES_TARGET > /sys/kernel/mm/hugepages/hugepages-${HUGEPAGE_SIZE_KB}kB/nr_hugepages
        local actual=$(cat /sys/kernel/mm/hugepages/hugepages-${HUGEPAGE_SIZE_KB}kB/nr_hugepages)
        if [[ $actual -ge $HUGEPAGES_TARGET ]]; then
            info "  Hugepages: $actual allocated ✅"
        else
            warn "  Only $actual/$HUGEPAGES_TARGET allocated (insufficient memory?)"
        fi
    else
        warn "  Hugepage sysfs not available (VM limitation)"
    fi

    # 2. Disable THP
    info "Disabling Transparent Huge Pages..."
    if [[ -f /sys/kernel/mm/transparent_hugepage/enabled ]]; then
        echo never > /sys/kernel/mm/transparent_hugepage/enabled
        echo never > /sys/kernel/mm/transparent_hugepage/defrag 2>/dev/null || true
        info "  THP disabled ✅"
    else
        warn "  THP control not available"
    fi

    # 3. Sysctl tuning
    info "Applying sysctl settings..."

    # Shared memory
    sysctl -w kernel.shmmax=$SHM_MIN > /dev/null 2>&1 || warn "  Failed to set shmmax"
    sysctl -w kernel.shmall=$((SHM_MIN / 4096)) > /dev/null 2>&1 || warn "  Failed to set shmall"

    # VM tuning
    sysctl -w vm.swappiness=10 > /dev/null 2>&1 || true
    sysctl -w vm.dirty_ratio=15 > /dev/null 2>&1 || true
    sysctl -w vm.dirty_background_ratio=5 > /dev/null 2>&1 || true

    # Network (for Redis and gRPC)
    sysctl -w net.core.somaxconn=1024 > /dev/null 2>&1 || true
    sysctl -w net.ipv4.tcp_max_syn_backlog=1024 > /dev/null 2>&1 || true
    sysctl -w net.core.netdev_max_backlog=5000 > /dev/null 2>&1 || true

    info "  Sysctl applied ✅"

    # 4. Ensure /dev/shm is large enough
    local shm_size_kb=$(df /dev/shm | tail -1 | awk '{print $2}')
    local shm_need_kb=$((SHM_MIN / 1024))
    if [[ $shm_size_kb -lt $shm_need_kb ]]; then
        info "Resizing /dev/shm..."
        mount -o remount,size=${SHM_MIN} /dev/shm 2>/dev/null || warn "  Could not resize /dev/shm"
    fi

    # 5. Create persistent config
    info "Writing persistent config to /etc/sysctl.d/99-nexus-spine.conf..."
    cat > /etc/sysctl.d/99-nexus-spine.conf << 'SYSCTL'
# Neural Spine performance tuning
kernel.shmmax = 268435456
kernel.shmall = 65536
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
net.core.somaxconn = 1024
net.ipv4.tcp_max_syn_backlog = 1024
net.core.netdev_max_backlog = 5000
SYSCTL
    info "  Config saved ✅"

    echo ""
    info "Kernel tuning applied. Run '$0 --check' to verify."
}

# ═══════════════════════════════════════════════════════════════════════════════
# Revert Mode
# ═══════════════════════════════════════════════════════════════════════════════

revert_tuning() {
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Neural Spine — Reverting Kernel Tuning"
    echo "═══════════════════════════════════════════════════════════════"

    if [[ $EUID -ne 0 ]]; then
        error "Must run as root: sudo $0 --revert"
        exit 1
    fi

    # Remove persistent config
    rm -f /etc/sysctl.d/99-nexus-spine.conf
    info "Removed /etc/sysctl.d/99-nexus-spine.conf"

    # Re-enable THP
    if [[ -f /sys/kernel/mm/transparent_hugepage/enabled ]]; then
        echo madvise > /sys/kernel/mm/transparent_hugepage/enabled
        info "THP set to madvise"
    fi

    # Free hugepages
    if [[ -f /sys/kernel/mm/hugepages/hugepages-${HUGEPAGE_SIZE_KB}kB/nr_hugepages ]]; then
        echo 0 > /sys/kernel/mm/hugepages/hugepages-${HUGEPAGE_SIZE_KB}kB/nr_hugepages
        info "Hugepages freed"
    fi

    # Reload default sysctl
    sysctl --system > /dev/null 2>&1
    info "Sysctl defaults restored"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

case "${1:---check}" in
    --apply)
        apply_tuning
        ;;
    --check)
        check_system
        ;;
    --revert)
        revert_tuning
        ;;
    *)
        echo "Usage: $0 [--apply|--check|--revert]"
        echo "  --check   Show current system configuration (default)"
        echo "  --apply   Apply kernel tuning (requires root)"
        echo "  --revert  Revert kernel tuning (requires root)"
        exit 1
        ;;
esac
