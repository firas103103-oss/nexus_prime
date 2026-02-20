#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Nexus Oracle Reindex — Ephemeral Container (RAM-Safe)
# Runs the indexer in a one-shot container with --memory=4g limit
# Processes .md files → ChromaDB in data/rag/chromadb/
# ═══════════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MEMORY_LIMIT="4g"

echo "═══════════════════════════════════════════════════════"
echo "  Nexus Oracle — Reindexing Knowledge Base"
echo "  Memory limit: ${MEMORY_LIMIT}"
echo "═══════════════════════════════════════════════════════"

cd "$PROJECT_DIR"

# Build the Oracle image if not exists
echo ""
echo "[1/3] Building Oracle image..."
docker build -t nexus_oracle:latest ./nexus_oracle/

# Create Dockerfile.indexer (extends Oracle image with indexer)
INDEXER_DOCKERFILE=$(mktemp)
cat > "$INDEXER_DOCKERFILE" << 'EOF'
FROM nexus_oracle:latest
COPY nexus_oracle/indexer.py /app/indexer.py
CMD ["python", "indexer.py"]
EOF

echo "[2/3] Building indexer image..."
docker build -t nexus_oracle_indexer:latest -f "$INDEXER_DOCKERFILE" .
rm -f "$INDEXER_DOCKERFILE"

# Run indexer in ephemeral container with memory limit
echo "[3/3] Running indexer (memory limit: ${MEMORY_LIMIT})..."
echo ""

docker run --rm \
    --name nexus_oracle_indexer \
    --memory="${MEMORY_LIMIT}" \
    --memory-swap="${MEMORY_LIMIT}" \
    -v "${PROJECT_DIR}:/workspace:ro" \
    -v "${PROJECT_DIR}/data/rag:/data/rag" \
    -e DOCS_PATH=/workspace \
    -e CHROMA_PATH=/data/rag/chromadb \
    -e CHUNK_SIZE=1000 \
    -e CHUNK_OVERLAP=200 \
    nexus_oracle_indexer:latest

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  ✅ Indexing complete!"
echo "  ChromaDB location: data/rag/chromadb/"
echo ""
echo "  Restart Oracle API to load new index:"
echo "  docker compose restart nexus_oracle"
echo "═══════════════════════════════════════════════════════"
