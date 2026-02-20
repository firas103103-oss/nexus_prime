# ═══════════════════════════════════════════════════════════════════════════════
# NEXUS PRIME CORE — Meta-Orchestrator Dockerfile
# ═══════════════════════════════════════════════════════════════════════════════
# Build stage: compile .proto → Python stubs
# Runtime: async gRPC server on port 50051
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
FROM python:3.12-slim

LABEL maintainer="MRF — NEXUS PRIME Sovereign AGI"
LABEL version="1.0.0"
LABEL description="Meta-Orchestrator gRPC Server — Multi-Agent Swarm Intelligence"

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy compiled proto stubs
COPY --from=builder /build/compiled/ ./

# Copy orchestrator code
COPY orchestrator/ ./

# Install grpcurl for healthcheck (lightweight)
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 50051

# Health check via gRPC reflection
HEALTHCHECK --interval=15s --timeout=5s --retries=3 --start-period=10s \
    CMD python -c "import grpc; ch = grpc.insecure_channel('localhost:50051'); grpc.channel_ready_future(ch).result(timeout=3); print('OK')" || exit 1

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENTRYPOINT ["python", "orchestrator_server.py"]
