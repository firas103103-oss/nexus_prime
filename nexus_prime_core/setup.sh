#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# NEXUS PRIME CORE — Automated Setup Script
# ═══════════════════════════════════════════════════════════════════════════════
# Creates full directory structure, installs dependencies, compiles protobufs.
# Run from: /root/NEXUS_PRIME_UNIFIED/nexus_prime_core/
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "═══════════════════════════════════════════════════════════════════════"
echo "  NEXUS PRIME CORE — Setup & Proto Compilation"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# ── 1. Verify directory structure ────────────────────────────────────────────
echo "📁 Verifying directory structure..."
DIRS=(
    "shared_protos"
    "orchestrator"
    "agents/shadow_7"
    "agents/clone_hub"
    "agents/xbio_sentinel"
    "agents/generic_agent"
)

for d in "${DIRS[@]}"; do
    mkdir -p "$d"
    touch "$d/__init__.py" 2>/dev/null || true
done
echo "   ✅ All directories verified"

# ── 2. Install Python dependencies ──────────────────────────────────────────
echo ""
echo "📦 Installing Python dependencies..."
if command -v pip3 &>/dev/null; then
    pip3 install --quiet --no-cache-dir -r requirements.txt 2>&1 | tail -5
    echo "   ✅ Dependencies installed"
else
    echo "   ⚠️ pip3 not found — install manually: pip3 install -r requirements.txt"
fi

# ── 3. Compile Protocol Buffers ──────────────────────────────────────────────
echo ""
echo "🔧 Compiling nexus_pulse.proto → Python stubs..."

if ! python3 -c "import grpc_tools" 2>/dev/null; then
    echo "   ❌ grpc_tools not found. Install: pip3 install grpcio-tools"
    exit 1
fi

python3 -m grpc_tools.protoc \
    -I./shared_protos \
    --python_out=./orchestrator \
    --grpc_python_out=./orchestrator \
    --pyi_out=./orchestrator \
    ./shared_protos/nexus_pulse.proto

# Fix protobuf import paths (grpc_tools generates absolute imports)
# In the orchestrator directory, the import should be local
if [[ -f "orchestrator/nexus_pulse_pb2_grpc.py" ]]; then
    sed -i 's/^import nexus_pulse_pb2/from . import nexus_pulse_pb2/' \
        orchestrator/nexus_pulse_pb2_grpc.py 2>/dev/null || true
    # Revert — for direct execution (not as package), keep absolute imports
    sed -i 's/^from \. import nexus_pulse_pb2/import nexus_pulse_pb2/' \
        orchestrator/nexus_pulse_pb2_grpc.py 2>/dev/null || true
fi

echo "   ✅ Proto compilation successful"
echo ""

# ── 4. Verify compilation ───────────────────────────────────────────────────
echo "🔍 Verifying generated files..."
EXPECTED_FILES=(
    "orchestrator/nexus_pulse_pb2.py"
    "orchestrator/nexus_pulse_pb2_grpc.py"
    "orchestrator/nexus_pulse_pb2.pyi"
)

ALL_OK=true
for f in "${EXPECTED_FILES[@]}"; do
    if [[ -f "$f" ]]; then
        SIZE=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f" 2>/dev/null || echo "?")
        echo "   ✅ $f (${SIZE} bytes)"
    else
        echo "   ❌ MISSING: $f"
        ALL_OK=false
    fi
done

# ── 5. Quick import test ────────────────────────────────────────────────────
echo ""
echo "🧪 Testing proto imports..."
cd orchestrator
python3 -c "
import nexus_pulse_pb2 as pb
import nexus_pulse_pb2_grpc as pb_grpc

# Verify service descriptor
svc = pb.DESCRIPTOR.services_by_name.get('NexusPulseService')
assert svc is not None, 'Service NexusPulseService not found!'

# Verify core messages
pulse = pb.AgentPulse(agent_id='TEST', pulse_type=pb.PULSE_TYPE_HEARTBEAT)
assert pulse.agent_id == 'TEST'

directive = pb.OrchestratorDirective(
    directive_id='test-uuid',
    directive_type=pb.DIRECTIVE_TYPE_ACK,
    message='Proto test passed'
)
assert directive.message == 'Proto test passed'

# Verify enums
assert pb.AGENT_STATUS_IDLE == 1
assert pb.PULSE_TYPE_REGISTRATION == 5
assert pb.DIRECTIVE_TYPE_EXECUTE_TASK == 1

# Verify all RPC methods
methods = [m.name for m in svc.methods]
expected = ['Pulse', 'RegisterAgent', 'SubmitCommand', 'GetSystemStatus']
for m in expected:
    assert m in methods, f'Missing RPC method: {m}'

print('   ✅ All proto imports and messages verified')
print(f'   ✅ Service: {svc.full_name}')
print(f'   ✅ RPCs: {methods}')
print(f'   ✅ Message types: {len(pb.DESCRIPTOR.message_types_by_name)} messages')
print(f'   ✅ Enum types: {len(pb.DESCRIPTOR.enum_types_by_name)} enums')
" || { echo "   ❌ Proto import test FAILED"; exit 1; }
cd "$SCRIPT_DIR"

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════════════════"
if $ALL_OK; then
    echo "  ✅ NEXUS PRIME CORE — Setup Complete"
else
    echo "  ⚠️ NEXUS PRIME CORE — Setup completed with warnings"
fi
echo ""
echo "  Proto compilation command (for reference):"
echo "    python3 -m grpc_tools.protoc \\"
echo "      -I./shared_protos \\"
echo "      --python_out=./orchestrator \\"
echo "      --grpc_python_out=./orchestrator \\"
echo "      --pyi_out=./orchestrator \\"
echo "      ./shared_protos/nexus_pulse.proto"
echo ""
echo "  To start the Meta-Orchestrator:"
echo "    cd orchestrator && python3 orchestrator_server.py"
echo ""
echo "  To start a test agent:"
echo "    cd agents/generic_agent && python3 agent_client.py"
echo ""
echo "  To build Docker container:"
echo "    docker compose up -d nexus_orchestrator"
echo "═══════════════════════════════════════════════════════════════════════"
