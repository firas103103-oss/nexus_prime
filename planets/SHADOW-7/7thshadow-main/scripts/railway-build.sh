#!/usr/bin/env bash
set -euo pipefail

# Railway build wrapper: ensure devDependencies are installed during build
# Note: npm will automatically include devDependencies during build phase
echo "Starting Railway build process..."

# Install and build (skip if already done in install phase)
if [ ! -d "dist" ]; then
  npm run build
else
  echo "Build artifacts already exist, skipping build"
fi

echo "Railway build script completed." 
