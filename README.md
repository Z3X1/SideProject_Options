# SideProject_Options — GEX Oracle BTC Deribit Options Analytics

> 對抗性碰撞框架 × 統一場論  
> Twitter: [@BTC_OptionsTW](https://twitter.com/BTC_OptionsTW) | [@kai6366](https://twitter.com/kai6366)

---

## 專案結構

```
gex-oracle/
├── dashboards/        # HTML 儀表板（每個快照一份，版本化）
│   └── S{N}_YYYYMMDD_dashboard.html
├── framework/         # 統一場論規則文件 & 狀態轉移文件
│   ├── unified_field_theory_v{N}.md
│   └── state_transfer_S{N}.md
├── data/              # CSV 原始數據快照（.gitignore 可選排除）
│   └── snapshots/
├── scripts/           # 自動化腳本
│   └── upload.sh
└── docs/              # 方法論說明
    └── methodology.md
```

---

## 分析框架版本

| 版本 | 快照 | 主要更新 |
|------|------|----------|
| v1.0 | S13 | 初始對抗性碰撞框架 |
| v1.3 | S16 | SS 結構建立 |
| v1.5 | S17 | 9 輪全面反駁完成 |
| v1.6 | S18 | Fib 驗證（誤差 $3） |
| v1.7 | S19 | 4h RSI 雙超賣規則 |
| v1.7b | S20 | RSI 機械篩選補充 |
| v1.8 | S21 | POS Regime 完整框架 |
| v2.0 | S31 | 當前最新版本 |

---

## 預測驗證記錄

| 到期日 | 預測中位 | 實際結算 | 誤差 | σ |
|--------|---------|---------|------|---|
| 26MAR26 | $70,860 | $70,020 | $840 | 0.41σ ✓ |
| 27MAR26 | $68,636 | $68,625.39 | $10.6 | 0.02σ ✓✓ |

---

## 統一場方程式

```
P(結算在X) = 0.40×GBM + 0.10×GEX + 0.28×行為信號
             + 0.12×貝葉斯 + 0.10×時間衰減
```

---

## 數據來源

- **期權數據**：Deribit CSV Export（BTC-* 完整工具集）
- **價格/技術**：Binance（15min / 4h / 1D）
- **DVOL**：Deribit 波動率指數
