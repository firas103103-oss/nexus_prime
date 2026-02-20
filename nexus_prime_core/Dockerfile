# ═══════════════════════════════════════════════════════════════════════════════
# NEXUS PRIME CORE — Meta-Orchestrator Dockerfile v1.1.0
# ═══════════════════════════════════════════════════════════════════════════════
# Build stage: compile .proto → Python stubs + download grpc_health_probe
# Runtime: async gRPC server on port 50051 with production-grade health checks
# ═══════════════════════════════════════════════════════════════════════════════

FROM python:3.12-slim AS builder

WORKDIR /build

# Install build deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy proto sources and compile
COPY shared_protos/ ./shared_protos/
RUN mkdir -p ./compiled && python -m grpc_tools.protoc \
    -I./shared_protos \
    --python_out=./compiled \
    --grpc_python_out=./compiled \
    --pyi_out=./compiled \
    ./shared_protos/nexus_pulse.proto

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 2: Download grpc_health_probe
# ─────────────────────────────────────────────────────────────────────────────

FROM alpine:latest AS health-probe-downloader

RUN apk add --no-cache curl && \
    GRPC_HEALTH_PROBE_VERSION=v0.4.25 && \
    curl -L https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64 \
    -o /grpc_health_probe && \
    chmod +x /grpc_health_probe

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 3: Runtime
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim

LABEL maintainer="MRF — NEXUS PRIME Sovereign AGI"
LABEL version="1.1.0"
LABEL description="Meta-Orchestrator gRPC Server — Multi-Agent Swarm Intelligence (Redis Streams)"

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy compiled proto stubs
COPY --from=builder /build/compiled/ ./

# Copy grpc_health_probe
COPY --from=health-probe-downloader /grpc_health_probe /bin/grpc_health_probe

# Copy orchestrator code
COPY orchestrator/ ./

EXPOSE 50051

# Health check using grpc_health_probe (production-grade)
HEALTHCHECK --interval=15s --timeout=5s --retries=3 --start-period=10s \
    CMD /bin/grpc_health_probe -addr=localhost:50051 || exit 1

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENTRYPOINT ["python", "orchestrator_server.py"]
