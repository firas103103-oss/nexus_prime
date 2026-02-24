#!/bin/bash
# Deploy landing page from repo to nginx web root
# Usage: ./deploy-landing.sh  (from landing-pages/ or NEXUS_PRIME_UNIFIED/)

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE="$SCRIPT_DIR/index.html"
DEST="/var/www/nexus-landing/index.html"

if [[ ! -f "$SOURCE" ]]; then
  echo "Error: Source not found: $SOURCE"
  exit 1
fi

cp "$SOURCE" "$DEST"
echo "✓ Deployed landing page to $DEST"
echo "  Live at: https://mrf103.com"
