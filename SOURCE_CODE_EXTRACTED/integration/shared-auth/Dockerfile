FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8002/api/v1/auth/health || exit 1

# Generate keys at RUNTIME (not build time) so volume mount gets them
CMD ["sh", "-c", "python generate_keys.py && uvicorn main:app --host 0.0.0.0 --port 8002"]
