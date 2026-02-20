FROM python:3.12-slim

LABEL maintainer="MrF <mrf@nexus-prime.com>"
LABEL description="NEXUS Memory Keeper - حارس الذاكرة المركزية"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY schema.sql .
COPY main.py .
COPY ui.py .

# Expose ports
EXPOSE 9000 9001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:9000/health || exit 1

# Start both API and UI
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 9000 & streamlit run ui.py --server.port 9001 --server.address 0.0.0.0 --server.headless true --server.runOnSave false && wait"]
