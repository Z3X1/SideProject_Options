# GEX Oracle 自動化部署說明

## 三步完成部署

### Step 1：把檔案放到正確位置

```
你的 GitHub repo（建議用 SideProject_Options）
├── gex_oracle_auto.py          ← 主腳本
├── .github/
│   └── workflows/
│       └── gex_oracle.yml      ← Actions workflow
├── docs/                       ← GitHub Pages輸出目錄（自動生成）
└── data/                       ← SQLite快照（自動生成）
```

### Step 2：設置 GitHub Secrets

在 repo Settings → Secrets → Actions 新增：

| Secret名稱 | 說明 | 哪裡取得 |
|-----------|------|---------|
| `GH_PAT` | GitHub Personal Access Token | Settings → Developer settings → Tokens |
| `ANTHROPIC_API_KEY` | Claude API金鑰 | console.anthropic.com |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | @BotFather |
| `TELEGRAM_CHAT_ID` | 你的Telegram ID | @userinfobot |

### Step 3：開啟 GitHub Pages

repo Settings → Pages → Source 選 **gh-pages branch**

---

## 結果

- **Dashboard**: `https://Z3X1.github.io/SideProject_Options/`
- **更新頻率**: 每6h自動（00/06/12/18 UTC）
- **Telegram**: 每次更新後推送摘要
- **成本**: Claude API ~$0.20-0.40/天

---

## 注意事項

### Deribit CSV的問題
Deribit API可以直接抓到期權OI和IV，**不再需要手動匯出CSV**。
自動化版本使用 `/api/v2/public/get_book_summary_by_currency`。

### 手動覆蓋
若你覺得某個快照需要深度碰撞（例如結算日、極端行情），
直接把截圖和數字丟給我，我做完整11層分析 + 新HTML。
自動化版本是「監控系統」，手動版本是「深度分析系統」，兩者互補。

### DVOL備選
若Deribit DVOL API失效，腳本自動使用上次值。
你可以在每次手動快照時補充真實DVOL。

---

## 費用估算

| 項目 | 費用 |
|------|------|
| GitHub Actions | 免費（公開repo） |
| Claude API（每次~1000 tokens）| ~$0.003/次 × 4次/天 = **$0.012/天** |
| Telegram Bot | 免費 |
| 合計 | **~$0.36/月** |
