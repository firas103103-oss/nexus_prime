#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# NEXUS PRIME - Git Sync All Products to GitHub
# ═══════════════════════════════════════════════════════════════
set -e

GIT_USER="MrF"
GIT_EMAIL="admin@mrf103.com"

# Common .gitignore
GITIGNORE_CONTENT='node_modules/
dist/
build/
.env
.env.local
*.log
.DS_Store
.cache/
coverage/
.next/
.nuxt/
.output/
__pycache__/
*.pyc
.venv/
venv/
*.egg-info/
'

SUCCESS=0
FAIL=0

init_and_push() {
  local DIR="$1"
  local REPO="$2"
  local MSG="$3"
  local NAME=$(basename "$DIR")
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📦 $NAME → github.com/firas103103-oss/$REPO"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  if [ ! -d "$DIR" ]; then
    echo "  ❌ Directory not found: $DIR"
    FAIL=$((FAIL+1))
    return
  fi
  
  cd "$DIR"
  
  # Create .gitignore if missing
  if [ ! -f .gitignore ]; then
    echo "$GITIGNORE_CONTENT" > .gitignore
    echo "  📝 Created .gitignore"
  fi
  
  # Init git if needed
  if [ ! -d .git ]; then
    git init -b main
    git config user.name "$GIT_USER"
    git config user.email "$GIT_EMAIL"
    echo "  🔧 Git initialized"
  fi
  
  # Set remote
  git remote remove origin 2>/dev/null || true
  git remote add origin "git@github.com:firas103103-oss/${REPO}.git"
  echo "  🔗 Remote: git@github.com:firas103103-oss/${REPO}.git"
  
  # Add and commit
  git add -A
  if git diff --cached --quiet 2>/dev/null; then
    echo "  ⏭️  No changes to commit"
  else
    git commit -m "$MSG" --quiet
    echo "  ✅ Committed"
  fi
  
  # Push
  echo -n "  🚀 Pushing... "
  if git push -u origin main --force 2>&1 | tail -1; then
    echo "  ✅ Pushed successfully"
    SUCCESS=$((SUCCESS+1))
  else
    echo "  ❌ Push failed"
    FAIL=$((FAIL+1))
  fi
}

echo "═══════════════════════════════════════════"
echo "🚀 NEXUS PRIME - Git Sync All Repos"
echo "═══════════════════════════════════════════"

# 1. Shadow Seven Publisher
init_and_push "/root/products/shadow-seven-publisher" \
  "shadow-seven-publisher" \
  "🚀 Shadow Seven Publisher - AI-powered publishing platform (168 files)"

# 2. AlSultan Intelligence
init_and_push "/root/products/alsultan-intelligence" \
  "alsultan-intelligence" \
  "🚀 AlSultan Intelligence - Quranic AI analysis (3 modules: Chronos, Decoder, Identity)"

# 3. Jarvis Control Hub
init_and_push "/root/products/jarvis-control-hub" \
  "jarvis-control-hub" \
  "🚀 Jarvis Control Hub - Central monitoring & orchestration (Python + FastAPI)"

# 4. Imperial UI (already has .git and commits - just sync)
init_and_push "/root/products/imperial-ui" \
  "imperial-ui" \
  "🔄 Imperial UI - Dashboard interface (React + Vite + Tailwind)"

# 5. MRF103 Mobile
init_and_push "/root/products/mrf103-mobile" \
  "mrf103-mobile-app" \
  "🚀 MRF103 Mobile App - React Native + Expo (87 files)"

# 6. X-BIO Sentinel
init_and_push "/root/products/xbio-sentinel" \
  "xbio-sentinel" \
  "🚀 X-BIO Sentinel - Biometric monitoring system (Python + ESP32)"

# 7. NEXUS Data Core
init_and_push "/root/products/nexus-data-core" \
  "nexus-data-core" \
  "🚀 NEXUS Data Core - Unified data processing engine"

# 8. MRF103 Website (old location - sync too)
init_and_push "/root/mrf103-website" \
  "mrf103-website" \
  "🔄 MRF103 Website - Main landing & marketing site"

# Summary
echo ""
echo "═══════════════════════════════════════════"
echo "📊 Sync Summary"
echo "═══════════════════════════════════════════"
echo "  ✅ Success: $SUCCESS"
echo "  ❌ Failed:  $FAIL"
echo "═══════════════════════════════════════════"
