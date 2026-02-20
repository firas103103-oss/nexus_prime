#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# 🔥 NEXUS PRIME - Chaos Engineering & Disaster Recovery Test
# ═══════════════════════════════════════════════════════════════════════════
# Purpose: اختبار قدرة النظام على التعافي من الكوارث
# Tests: Container Failures, Network Issues, Resource Exhaustion
# ═══════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

LOGFILE="/tmp/chaos_test_$(date +%Y%m%d_%H%M%S).log"

# ═══════════════════════════════════════════════════════════════════════════
# 📝 Logging Functions
# ═══════════════════════════════════════════════════════════════════════════
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1" | tee -a "$LOGFILE"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOGFILE"
}

log_error() {
    echo -e "${RED}❌ $1${NC}" | tee -a "$LOGFILE"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}" | tee -a "$LOGFILE"
}

log_test() {
    echo -e "${PURPLE}🧪 TEST: $1${NC}" | tee -a "$LOGFILE"
}

# ═══════════════════════════════════════════════════════════════════════════
# 🔍 Health Check Function
# ═══════════════════════════════════════════════════════════════════════════
check_system_health() {
    local component=$1
    local url=$2
    local max_retries=${3:-30}
    local retry_interval=${4:-2}
    
    log "Checking health of $component..."
    
    for i in $(seq 1 $max_retries); do
        if curl -sf "$url" > /dev/null 2>&1; then
            log_success "$component is healthy (attempt $i/$max_retries)"
            return 0
        fi
        sleep $retry_interval
    done
    
    log_error "$component failed to recover after $max_retries attempts"
    return 1
}

# ═══════════════════════════════════════════════════════════════════════════
# 📊 Capture System State
# ═══════════════════════════════════════════════════════════════════════════
capture_state() {
    local state_name=$1
    log "Capturing system state: $state_name"
    
    {
        echo "=== System State: $state_name ==="
        echo "Timestamp: $(date)"
        echo ""
        echo "=== Running Containers ==="
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        echo ""
        echo "=== Container Resource Usage ==="
        docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
        echo ""
        echo "=== Database Connections ==="
        docker exec nexus_db psql -U postgres -d nexus_db -c "SELECT count(*) as connections FROM pg_stat_activity;" 2>/dev/null || echo "DB check failed"
        echo ""
    } >> "$LOGFILE"
}

# ═══════════════════════════════════════════════════════════════════════════
# 🔥 CHAOS TEST 1: Database Container Failure
# ═══════════════════════════════════════════════════════════════════════════
test_database_failure() {
    log_test "Database Container Failure & Recovery"
    
    capture_state "before_db_failure"
    
    log "Stopping PostgreSQL container..."
    docker stop nexus_db
    
    sleep 5
    log_warning "Database is down. Checking dependent services..."
    
    # Check if services handle DB failure gracefully
    cortex_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8005/health || echo "failed")
    log "Cortex response during DB outage: $cortex_response"
    
    log "Restarting PostgreSQL..."
    docker start nexus_db
    
    if check_system_health "PostgreSQL" "http://localhost:8005/health" 30 2; then
        log_success "Database recovered successfully"
        capture_state "after_db_recovery"
        return 0
    else
        log_error "Database failed to recover"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 🔥 CHAOS TEST 2: Redis Cache Failure
# ═══════════════════════════════════════════════════════════════════════════
test_redis_failure() {
    log_test "Redis Cache Failure & Recovery"
    
    capture_state "before_redis_failure"
    
    log "Stopping Redis container..."
    docker stop nexus_redis
    
    sleep 3
    log_warning "Redis is down. System should continue with degraded performance..."
    
    # Test if system still responds
    cortex_response=$(curl -s http://localhost:8005/health | jq -r '.status' 2>/dev/null || echo "failed")
    log "Cortex status during Redis outage: $cortex_response"
    
    log "Restarting Redis..."
    docker start nexus_redis
    
    if check_system_health "Redis" "http://localhost:8005/health" 20 2; then
        log_success "Redis recovered successfully"
        capture_state "after_redis_recovery"
        return 0
    else
        log_error "Redis failed to recover"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 🔥 CHAOS TEST 3: API Gateway (Cortex) Failure
# ═══════════════════════════════════════════════════════════════════════════
test_cortex_failure() {
    log_test "Cortex API Gateway Failure & Recovery"
    
    capture_state "before_cortex_failure"
    
    log "Killing Cortex container..."
    docker kill nexus_cortex
    
    sleep 5
    log "Checking if Docker Compose restarts Cortex automatically..."
    
    # Docker Compose should restart it
    if check_system_health "Cortex" "http://localhost:8005/health" 30 2; then
        log_success "Cortex auto-recovered via Docker restart policy"
        capture_state "after_cortex_recovery"
        return 0
    else
        log_warning "Auto-restart failed. Manual restart..."
        docker compose -f /root/NEXUS_PRIME_UNIFIED/docker-compose.yml up -d nexus_cortex
        
        if check_system_health "Cortex" "http://localhost:8005/health" 20 2; then
            log_success "Cortex recovered after manual restart"
            return 0
        else
            log_error "Cortex failed to recover"
            return 1
        fi
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 🔥 CHAOS TEST 4: Ollama AI Engine Failure
# ═══════════════════════════════════════════════════════════════════════════
test_ollama_failure() {
    log_test "Ollama AI Engine Failure & Recovery"
    
    capture_state "before_ollama_failure"
    
    log "Stopping Ollama container..."
    docker stop nexus_ollama
    
    sleep 3
    log_warning "Ollama is down. AI requests should queue or fail gracefully..."
    
    log "Restarting Ollama..."
    docker start nexus_ollama
    
    # Ollama takes longer to start
    if check_system_health "Ollama" "http://localhost:11434/" 60 3; then
        log_success "Ollama recovered successfully"
        capture_state "after_ollama_recovery"
        return 0
    else
        log_error "Ollama failed to recover"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 🔥 CHAOS TEST 5: Network Partition (Container Isolation)
# ═══════════════════════════════════════════════════════════════════════════
test_network_partition() {
    log_test "Network Partition Simulation"
    
    capture_state "before_network_partition"
    
    log "Disconnecting Cortex from network..."
    docker network disconnect nexus_network nexus_cortex 2>/dev/null || log_warning "Failed to disconnect"
    
    sleep 5
    log_warning "Cortex is isolated. Services should timeout gracefully..."
    
    # Check if other services continue
    db_status=$(docker exec nexus_db pg_isready -U postgres 2>/dev/null && echo "ready" || echo "failed")
    log "Database status during network partition: $db_status"
    
    log "Reconnecting Cortex to network..."
    docker network connect nexus_network nexus_cortex
    
    if check_system_health "Cortex" "http://localhost:8005/health" 20 2; then
        log_success "Network partition resolved"
        capture_state "after_network_recovery"
        return 0
    else
        log_error "Failed to recover from network partition"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 💾 DISASTER RECOVERY TEST: Backup & Restore
# ═══════════════════════════════════════════════════════════════════════════
test_backup_restore() {
    log_test "Backup & Restore Verification"
    
    local backup_file="/tmp/nexus_chaos_test_backup_$(date +%Y%m%d_%H%M%S).sql"
    
    log "Creating database backup..."
    docker exec nexus_db pg_dump -U postgres -d nexus_db > "$backup_file"
    
    if [ -f "$backup_file" ] && [ -s "$backup_file" ]; then
        local backup_size=$(du -h "$backup_file" | cut -f1)
        log_success "Backup created successfully: $backup_file ($backup_size)"
        
        # Test restore (to a test database)
        log "Testing restore to test_db..."
        docker exec nexus_db psql -U postgres -c "DROP DATABASE IF EXISTS test_db;" 2>/dev/null || true
        docker exec nexus_db psql -U postgres -c "CREATE DATABASE test_db;" 2>/dev/null
        
        if docker exec -i nexus_db psql -U postgres -d test_db < "$backup_file" > /dev/null 2>&1; then
            log_success "Backup restore test successful"
            docker exec nexus_db psql -U postgres -c "DROP DATABASE test_db;" 2>/dev/null || true
            return 0
        else
            log_error "Backup restore test failed"
            return 1
        fi
    else
        log_error "Backup creation failed"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 🔥 CHAOS TEST 6: Memory Pressure Simulation
# ═══════════════════════════════════════════════════════════════════════════
test_memory_pressure() {
    log_test "Memory Pressure Simulation"
    
    log "Creating memory stress container..."
    docker run -d --name chaos_memory_stress \
        --network nexus_network \
        --memory="200m" \
        --memory-swap="200m" \
        alpine:latest \
        sh -c 'yes | tr \\n x | head -c 150m | grep n || true; sleep 30' 2>/dev/null || true
    
    sleep 10
    log "Checking if system remains stable under memory pressure..."
    
    cortex_healthy=$(check_system_health "Cortex" "http://localhost:8005/health" 10 2 && echo "yes" || echo "no")
    db_healthy=$(docker exec nexus_db pg_isready -U postgres 2>/dev/null && echo "yes" || echo "no")
    
    log "Removing stress container..."
    docker rm -f chaos_memory_stress 2>/dev/null || true
    
    if [ "$cortex_healthy" == "yes" ] && [ "$db_healthy" == "yes" ]; then
        log_success "System remained stable under memory pressure"
        return 0
    else
        log_warning "System showed degradation under memory pressure"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 📊 Generate Final Report
# ═══════════════════════════════════════════════════════════════════════════
generate_report() {
    local total_tests=$1
    local passed_tests=$2
    local failed_tests=$3
    
    local report_file="/root/NEXUS_PRIME_UNIFIED/CHAOS_TEST_REPORT_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$report_file" << EOF
# 🔥 NEXUS PRIME - Chaos Engineering & DR Test Report

**Generated:** $(date)
**Log File:** $LOGFILE

## 📊 Test Summary

- **Total Tests:** $total_tests
- **Passed:** $passed_tests ✅
- **Failed:** $failed_tests ❌
- **Success Rate:** $(echo "scale=2; $passed_tests * 100 / $total_tests" | bc)%

## 🧪 Tests Executed

1. **Database Container Failure** - PostgreSQL stop/start recovery
2. **Redis Cache Failure** - Cache service interruption handling
3. **API Gateway Failure** - Cortex auto-recovery via Docker restart policy
4. **AI Engine Failure** - Ollama service interruption and recovery
5. **Network Partition** - Container network isolation simulation
6. **Memory Pressure** - Resource exhaustion behavior
7. **Backup & Restore** - Data persistence verification

## 📈 System Resilience Summary

EOF

    if [ $failed_tests -eq 0 ]; then
        echo "✅ **All tests passed!** النظام يتمتع بمرونة ممتازة." >> "$report_file"
    elif [ $failed_tests -le 2 ]; then
        echo "⚠️  **معظم الاختبارات نجحت** مع بعض المشاكل البسيطة." >> "$report_file"
    else
        echo "❌ **النظام يحتاج تحسينات كبيرة** في المرونة والتعافي." >> "$report_file"
    fi
    
    cat >> "$report_file" << EOF

## 📝 Detailed Logs

\`\`\`
$(tail -100 "$LOGFILE")
\`\`\`

## 🔄 Recommendations

1. **Auto-healing:** تأكد من أن جميع الحاويات لديها \`restart: always\`
2. **Health Checks:** تفعيل healthchecks لجميع الخدمات
3. **Monitoring:** تشغيل Prometheus + Grafana للمراقبة الحية
4. **Backups:** جدولة نسخ احتياطي يومي تلقائي
5. **Alerts:** تفعيل إشعارات AlertManager للحوادث الحرجة

---
**NEXUS PRIME Sovereign™** - Built for Resilience 🛡️
EOF

    log_success "Report generated: $report_file"
    echo "$report_file"
}

# ═══════════════════════════════════════════════════════════════════════════
# 🚀 MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════
main() {
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo -e "${RED}🔥 NEXUS PRIME - CHAOS ENGINEERING TEST SUITE${NC}"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    log "Starting chaos engineering tests..."
    log "Log file: $LOGFILE"
    echo ""
    
    # Confirm before proceeding
    read -p "⚠️  This will intentionally disrupt services. Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warning "Test cancelled by user"
        exit 0
    fi
    
    local total_tests=0
    local passed_tests=0
    local failed_tests=0
    
    # Capture initial state
    capture_state "initial"
    
    # Run tests
    tests=(
        "test_database_failure"
        "test_redis_failure"
        "test_cortex_failure"
        "test_ollama_failure"
        "test_network_partition"
        "test_memory_pressure"
        "test_backup_restore"
    )
    
    for test_func in "${tests[@]}"; do
        ((total_tests++))
        echo ""
        echo "────────────────────────────────────────────────────────────────"
        
        if $test_func; then
            ((passed_tests++))
        else
            ((failed_tests++))
        fi
        
        sleep 5 # Cool down between tests
    done
    
    # Final state
    capture_state "final"
    
    # Generate report
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo -e "${CYAN}📊 FINAL RESULTS${NC}"
    echo "════════════════════════════════════════════════════════════════"
    echo -e "Total Tests:  ${BLUE}$total_tests${NC}"
    echo -e "Passed:       ${GREEN}$passed_tests ✅${NC}"
    echo -e "Failed:       ${RED}$failed_tests ❌${NC}"
    echo -e "Success Rate: ${PURPLE}$(echo "scale=2; $passed_tests * 100 / $total_tests" | bc)%${NC}"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    
    local report=$(generate_report $total_tests $passed_tests $failed_tests)
    echo -e "${GREEN}📄 Full report:${NC} $report"
    echo -e "${BLUE}📋 Logs:${NC} $LOGFILE"
    echo ""
}

# Run main
main
