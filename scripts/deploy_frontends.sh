#!/bin/bash
# NEXUS PRIME — نشر الواجهات الأمامية
# يشغّل: ./scripts/deploy_frontends.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NEXUS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PUBLISHER_DIR="/root/products/shadow-seven-publisher"

echo "=== نشر دار النشر (Shadow Seven) ==="
cd "$PUBLISHER_DIR"
npm run build
sudo rm -rf /var/www/publisher/*
sudo cp -r dist/* /var/www/publisher/
echo "✓ publisher.mrf103.com محدّث"

echo ""
echo "=== نشر اللانينق ==="
cd "$NEXUS_ROOT"
[ -f ./landing-pages/deploy-landing.sh ] && bash ./landing-pages/deploy-landing.sh || echo "  ⚠ landing deploy script not found"
echo "✓ mrf103.com محدّث"

echo ""
echo "=== انتهى ==="
echo "  publisher: https://publisher.mrf103.com"
echo "  login:     https://publisher.mrf103.com/login"
echo "  landing:   https://mrf103.com"
echo "  dashboard: https://dashboard.mrf103.com (يُشغّل من Docker)"
