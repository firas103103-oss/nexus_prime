# ═══════════════════════════════════════════════════════════════════════════
# NEXUS PRIME — Generic Agent Dockerfile (Production-Grade)
# ═══════════════════════════════════════════════════════════════════════════
# Multi-stage build for optimized image size
# Includes: gRPC health probe, proto stubs, metrics support
# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# STAGE 1: Proto Compilation (Get compiled stubs from orchestrator)
# ═══════════════════════════════════════════════════════════════════════════

FROM python:3.12-slim AS proto-builder

WORKDIR /proto

# Copy proto files
COPY nexus_prime_core/shared_protos/nexus_pulse.proto ./

# Install grpcio-tools
RUN pip install --no-cache-dir grpcio-tools==1.68.1

# Compile protos
RUN python -m grpc_tools.protoc \
    --python_out=. \
    --grpc_python_out=. \
    --pyi_out=. \
    -I. \
    nexus_pulse.proto

# ═══════════════════════════════════════════════════════════════════════════
# STAGE 2: gRPC Health Probe Download
# ═══════════════════════════════════════════════════════════════════════════

FROM alpine:latest AS health-probe-downloader

# Download grpc_health_probe for health checks
RUN apk add --no-cache curl && \
    GRPC_HEALTH_PROBE_VERSION=v0.4.25 && \
    curl -L https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64 \
    -o /grpc_health_probe && \
    chmod +x /grpc_health_probe

# ═══════════════════════════════════════════════════════════════════════════
# STAGE 3: Runtime Image
# ═══════════════════════════════════════════════════════════════════════════

FROM python:3.12-slim

WORKDIR /app

# Copy proto stubs from builder
COPY --from=proto-builder /proto/*.py /app/
COPY --from=proto-builder /proto/*.pyi /app/

# Copy grpc_health_probe from downloader
COPY --from=health-probe-downloader /grpc_health_probe /bin/grpc_health_probe

# Copy requirements
COPY nexus_prime_core/agents/requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY nexus_prime_core/agents/generic_agent/agent_client_v2.py ./agent_client.py

# Create non-root user for security
RUN useradd -m -u 1000 nexusagent && \
    chown -R nexusagent:nexusagent /app

USER nexusagent

# Environment variables (can be overridden in K8s)
ENV AGENT_ID="GENERIC-AGENT" \
    AGENT_TYPE="planet" \
    ORCHESTRATOR_HOST="nexus-orchestrator:50051" \
    HEARTBEAT_INTERVAL="10" \
    MAX_RETRIES="10" \
    PYTHONUNBUFFERED=1

# Health check using grpc_health_probe
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD /bin/grpc_health_probe -addr=${ORCHESTRATOR_HOST} || exit 1

# Expose no ports (agent initiates connection)

ENTRYPOINT ["python", "agent_client.py"]
