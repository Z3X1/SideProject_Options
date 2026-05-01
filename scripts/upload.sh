#!/bin/bash
# GEX Oracle — GitHub Auto-Upload Script
# Usage:./scripts/upload.sh <GITHUB_TOKEN> <REPO_URL> [COMMIT_MSG]

set -e

TOKEN="${1:?GitHub Personal Access Token required}"
REPO_URL="${2:?Repo URL required, e.g. https://github.com/Z3X1/SideProject_Options}"
COMMIT_MSG="${3:-"chore: auto-upload snapshot $(date +%Y%m%d-%H%M%S)"}"

# Extract owner/repo from REPO_URL
REPO_PATH=$(echo "$REPO_URL" | sed 's|https://github.com/||')

# Build authenticated remote URL
AUTH_URL="https://${TOKEN}@github.com/${REPO_PATH}.git"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"

echo "📁 Working directory：$ROOT_DIR"
echo "📦 Target repo：$REPO_PATH"

# Initialize git repo if not already done
if [ ! -d ".git" ]; then
  echo "🔧 Initializing Git repository..."
  git init
  git branch -M main
fi

# Configure git identity
git config user.email "gex-oracle@btc-options.tw"
git config user.name "GEX Oracle Bot"

# Set remote origin
git remote remove origin 2>/dev/null || true
git remote add origin "$AUTH_URL"

# .gitignore
cat > .gitignore << 'EOF'
# Raw CSV data (upload selectively)
data/snapshots/*.csv

# OS files
.DS_Store
*.swp
*~
EOF

# Stage all changes
git add -A

# Only commit if there are staged changes
if git diff --cached --quiet; then
  echo "✅ No changes to commit"
else
  git commit -m "$COMMIT_MSG"
  echo "✅ Committed：$COMMIT_MSG"
fi

# Push to remote
echo "🚀 Pushing to GitHub..."
git push -u origin main --force-with-lease 2>/dev/null || git push -u origin main --force

echo ""
echo "✅ Upload complete！"
echo "🔗 https://github.com/$REPO_PATH"
