#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NEXUS PRIME — Model Initialization Script
# Downloads AI models via Docker instead of storing in Git
#
# Usage: bash scripts/init_models.sh
# Run on: Fresh server clones, CI/CD init stage
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
FLAG_FILE="$PROJECT_DIR/data/ollama/.initialized"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🧠 NEXUS PRIME — Model Initialization${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if already initialized
if [ -f "$FLAG_FILE" ]; then
    echo -e "${GREEN}✅ Models already initialized (flag: $FLAG_FILE)${NC}"
    echo "   To force re-download, delete the flag file and re-run."
    exit 0
fi

# Ensure data directories exist
mkdir -p "$PROJECT_DIR/data/ollama"
mkdir -p "$PROJECT_DIR/data/open-webui"
mkdir -p "$PROJECT_DIR/data/rag"

# Verify nexus_ollama container is running
if ! docker ps --format '{{.Names}}' | grep -q '^nexus_ollama$'; then
    echo -e "${YELLOW}⚠️  nexus_ollama container is not running.${NC}"
    echo "   Starting it via docker-compose..."
    cd "$PROJECT_DIR"
    docker-compose up -d nexus_ollama
    echo "   Waiting 10s for Ollama to initialize..."
    sleep 10
fi

# Pull the LLM model (1.9GB)
echo -e "${BLUE}📦 [1/1] Pulling Ollama model: llama3.2:3b (1.9GB)...${NC}"
echo "   This may take several minutes on first run."
echo ""

docker exec nexus_ollama ollama pull llama3.2:3b

echo ""
echo -e "${GREEN}✅ Model pulled successfully.${NC}"
echo ""

# Whisper + Embedding models auto-download on first use by Open WebUI
echo -e "${BLUE}ℹ️  Whisper (139MB) and Embedding models (696MB) will${NC}"
echo -e "${BLUE}   auto-download on first use via Open WebUI.${NC}"
echo ""

# Set initialization flag
touch "$FLAG_FILE"

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Model initialization complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "   Ollama LLM:     llama3.2:3b  (~1.9 GB) ✓"
echo "   Whisper STT:    auto on first use       ⏳"
echo "   Embeddings:     auto on first use       ⏳"
echo ""
echo "   Run: docker-compose up -d"
