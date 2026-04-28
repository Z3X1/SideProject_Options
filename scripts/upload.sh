#!/bin/bash
# GEX Oracle — GitHub 自動上傳腳本
# 使用方式：./scripts/upload.sh <GITHUB_TOKEN> <REPO_URL> [COMMIT_MSG]

set -e

TOKEN="${1:?請提供 GitHub Personal Access Token}"
REPO_URL="${2:?請提供 Repo URL，例如 https://github.com/kai6366/gex-oracle}"
COMMIT_MSG="${3:-"chore: auto-upload snapshot $(date +%Y%m%d-%H%M%S)"}"

# 從 REPO_URL 提取 owner/repo
REPO_PATH=$(echo "$REPO_URL" | sed 's|https://github.com/||')

# 設定帶認證的遠端 URL
AUTH_URL="https://${TOKEN}@github.com/${REPO_PATH}.git"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"

echo "📁 工作目錄：$ROOT_DIR"
echo "📦 目標 Repo：$REPO_PATH"

# 初始化 git（如尚未初始化）
if [ ! -d ".git" ]; then
  echo "🔧 初始化 Git 倉庫..."
  git init
  git branch -M main
fi

# 配置 git
git config user.email "gex-oracle@btc-options.tw"
git config user.name "GEX Oracle Bot"

# 設定遠端
git remote remove origin 2>/dev/null || true
git remote add origin "$AUTH_URL"

# .gitignore
cat > .gitignore << 'EOF'
# 原始 CSV 數據（選擇性上傳）
data/snapshots/*.csv

# 系統文件
.DS_Store
*.swp
*~
EOF

# 暫存所有變更
git add -A

# 確認有變更才提交
if git diff --cached --quiet; then
  echo "✅ 沒有新變更，無需提交"
else
  git commit -m "$COMMIT_MSG"
  echo "✅ 已提交：$COMMIT_MSG"
fi

# 推送
echo "🚀 推送至 GitHub..."
git push -u origin main --force-with-lease 2>/dev/null || git push -u origin main --force

echo ""
echo "✅ 上傳完成！"
echo "🔗 https://github.com/$REPO_PATH"
