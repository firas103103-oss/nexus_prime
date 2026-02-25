#!/bin/bash
# Deploy landing page and legal pages from repo to nginx web root
# Usage: ./deploy-landing.sh  (from landing-pages/ or NEXUS_PRIME_UNIFIED/)

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEST_DIR="/var/www/nexus-landing"

for f in index.html terms.html privacy.html copyright.html; do
  SRC="$SCRIPT_DIR/$f"
  if [[ -f "$SRC" ]]; then
    cp "$SRC" "$DEST_DIR/$f"
    echo "✓ Deployed $f"
  fi
done

# Deploy branches
if [[ -d "$SCRIPT_DIR/branches" ]]; then
  mkdir -p "$DEST_DIR/branches"
  for f in publisher.html sovereign.html xbio.html fourth.html; do
    SRC="$SCRIPT_DIR/branches/$f"
    if [[ -f "$SRC" ]]; then
      cp "$SRC" "$DEST_DIR/branches/$f"
      echo "✓ Deployed branches/$f"
    fi
  done
fi

echo "  Live at: https://mrf103.com"
echo "  Branches: https://mrf103.com/branches/publisher.html | sovereign.html | xbio.html | fourth.html"
echo "  Legal: https://mrf103.com/terms.html | /privacy.html | /copyright.html"
