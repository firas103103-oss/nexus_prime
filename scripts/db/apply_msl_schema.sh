#!/bin/bash
# Apply MSL schema to nexus_db — required for Sovereign Dify Bridge, Nerve, cognitive_bridge
# Run: ./scripts/db/apply_msl_schema.sh  (from NEXUS_PRIME_UNIFIED root)

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA_FILE="${SCRIPT_DIR}/msl_schema.sql"
CONTAINER="${NEXUS_DB_CONTAINER:-nexus_db}"

if [ ! -f "$SCHEMA_FILE" ]; then
  echo "ERROR: msl_schema.sql not found at $SCHEMA_FILE"
  exit 1
fi

echo "Applying MSL schema to $CONTAINER..."
docker exec -i "$CONTAINER" psql -U postgres -d "${POSTGRES_DB:-nexus_db}" < "$SCHEMA_FILE"
echo "MSL schema applied successfully."
