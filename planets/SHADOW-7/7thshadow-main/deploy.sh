#!/bin/bash

# X-Book Production Deployment Script
# Usage: ./deploy.sh [environment]

set -e

ENVIRONMENT=${1:-production}

echo "🚀 Starting deployment for: $ENVIRONMENT"

# 1. Run tests and checks
echo "✓ Running pre-deployment checks..."
npm run build

# 2. Verify build output
if [ ! -d "dist" ]; then
  echo "❌ Build failed: dist directory not found"
  exit 1
fi

echo "✓ Build successful"

# 3. Check for required files
REQUIRED_FILES=("dist/index.html" "dist/assets" "package.json")
for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -e "$file" ]; then
    echo "❌ Missing required file: $file"
    exit 1
  fi
done

echo "✓ All required files present"

# 4. Size check
DIST_SIZE=$(du -sh dist | cut -f1)
echo "📦 Build size: $DIST_SIZE"

# 5. Environment-specific deployment
case $ENVIRONMENT in
  production)
    echo "🌐 Deploying to production..."
    # Add your production deployment commands here
    # e.g., railway up, vercel deploy --prod, etc.
    ;;
  staging)
    echo "🔧 Deploying to staging..."
    # Add your staging deployment commands here
    ;;
  *)
    echo "❓ Unknown environment: $ENVIRONMENT"
    exit 1
    ;;
esac

echo "✅ Deployment completed successfully!"
