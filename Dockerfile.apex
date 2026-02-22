FROM python:3.11-slim

LABEL name="apex" \
      description="Apex — The Command Layer — Invisible Control System"

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Python deps
RUN pip install --no-cache-dir \
    fastapi==0.128.0 \
    uvicorn[standard]==0.34.0 \
    asyncpg==0.30.0 \
    pyotp==2.9.0 \
    cryptography==41.0.7 \
    websockets==14.1

# Copy code
COPY neural_spine/ /app/neural_spine/

# Non-root user
RUN useradd -m apex && chown -R apex:apex /app
USER apex

EXPOSE 7777

CMD ["python", "-m", "neural_spine.throne.apex_server"]
