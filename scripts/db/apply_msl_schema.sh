#!/bin/bash
# Apply MSL schema to nexus_db — required for Sovereign Dify Bridge, Nerve, cognitive_bridge
# Run: ./scripts/db/apply_msl_schema.sh  (from anywhere)

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SCHEMA_FILE="${PROJECT_ROOT}/scripts/db/msl_schema.sql"
CONTAINER="${NEXUS_DB_CONTAINER:-nexus_db}"

if [ ! -f "$SCHEMA_FILE" ]; then
  echo "ERROR: msl_schema.sql not found at $SCHEMA_FILE"
  exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
  echo "ERROR: Container $CONTAINER is not running. Start it first:"
  echo "  cd $PROJECT_ROOT && docker compose -f docker-compose.yml -f docker-compose.dify.yml up -d nexus_db"
  exit 1
fi

echo "Applying MSL schema to $CONTAINER..."
echo "(Re-run safe: 'already exists' errors are normal if schema was applied before)"
docker exec -i "$CONTAINER" psql -U postgres -d "${POSTGRES_DB:-nexus_db}" -v ON_ERROR_STOP=0 < "$SCHEMA_FILE" || true
echo "Applying analytics schema..."
ANALYTICS_FILE="${PROJECT_ROOT}/scripts/db/analytics_schema.sql"
if [ -f "$ANALYTICS_FILE" ]; then
  docker exec -i "$CONTAINER" psql -U postgres -d "${POSTGRES_DB:-nexus_db}" -v ON_ERROR_STOP=0 < "$ANALYTICS_FILE" || true
  echo "Analytics schema applied."
fi
echo "Done."
