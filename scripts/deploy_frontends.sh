#!/bin/bash
# NEXUS PRIME — نشر الواجهات الأمامية
# يشغّل: ./scripts/deploy_frontends.sh

set -e
cd "$(dirname "$0")/.."

echo "=== نشر دار النشر (Shadow Seven) ==="
cd ../products/shadow-seven-publisher
npm run build
sudo rm -rf /var/www/publisher/*
sudo cp -r dist/* /var/www/publisher/
echo "✓ publisher.mrf103.com محدّث"

echo ""
echo "=== نشر اللانينق ==="
cd "$(dirname "$0")/.."
./landing-pages/deploy-landing.sh
echo "✓ mrf103.com محدّث"

echo ""
echo "=== انتهى ==="
echo "  publisher: https://publisher.mrf103.com"
echo "  login:     https://publisher.mrf103.com/login"
echo "  landing:   https://mrf103.com"
echo "  dashboard: https://dashboard.mrf103.com (يُشغّل من Docker)"
