#!/bin/bash
# Dify launch script — NEXUS PRIME integration
# Requires: nexus stack running (nexus_litellm, nexus_network)

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DIFY_DIR="$PROJECT_ROOT/dify/docker"

cd "$DIFY_DIR"

# Ensure .env exists
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

# Apply nexus overrides if not set
grep -q "nexus_litellm" .env || sed -i 's|^OPENAI_API_BASE=.*|OPENAI_API_BASE=http://nexus_litellm:4000/v1|' .env
grep -q "8085" .env || sed -i 's|^EXPOSE_NGINX_PORT=.*|EXPOSE_NGINX_PORT=8085|' .env
grep -q "8445" .env || sed -i 's|^EXPOSE_NGINX_SSL_PORT=.*|EXPOSE_NGINX_SSL_PORT=8445|' .env

echo "Starting Dify (port 8085, LiteLLM via nexus_network)..."
docker compose -f docker-compose.yaml -f docker-compose.nexus-override.yaml -p dify up -d

echo ""
echo "Dify started. Access:"
echo "  Local:  http://localhost:8085"
echo "  Domain: https://dify.mrf103.com"
echo ""
echo "First run: open /install to create admin account."
echo "Then create a workflow and set DIFY_API_KEY + DIFY_DEFENSIVE_WORKFLOW_ID in bridge env."
