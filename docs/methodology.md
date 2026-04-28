# GEX Oracle 方法論說明

## 核心架構

### 對抗性碰撞框架
H_BULL 和 H_BEAR 輪流攻擊對方論點，Oracle 裁判收斂。
- 每輪結束後更新統一場論版本
- 終止條件：重複論點出現

### GEX（Gamma Exposure）分析
- **Gamma Flip**：造市商從空 Gamma 轉為多 Gamma 的臨界點
- **Gamma-MP（磁力點）**：最大 Gamma 集中，對 Spot 有吸引力
- **Call Wall / Put Wall**：期權牆，大量 OI 集中，形成阻力/支撐
- **PCR（Put/Call Ratio）**：跨期比較，近端防禦 vs. 遠端進攻

### Regime 框架
| Regime | 條件 | 造市商行為 | Layer 合併 |
|--------|------|-----------|-----------|
| POS | Spot > Gamma Flip | 穩定器（反向對沖） | Layer1 + Layer2 合併 |
| NEG | Spot < Gamma Flip | 放大器（同向對沖） | Layer1 / Layer2 嚴格分離 |

---

## 數據分層

### Layer 1（高可信度）
- GEX 結構（Gamma Flip、Call/Put Wall）
- 貝葉斯情境概率
- FR 穿越觸發

### Layer 2（中可信度）
- 技術指標（MACD、RSI、EMA）
- L/S 比率行為信號
- 跨期 PCR 結構

### Layer 3（低可信度，僅輔助）
- 15min 短線信號（可靠性 30%）
- 機械 RSI 滾動
- 壽命不足的 MACD 信號

---

## 輸出格式

每個快照生成：
1. **HTML 儀表板**（深色主題，多 Tab）
   - GEX 結構分析
   - 對抗性碰撞過程
   - 情境概率分布
   - 技術面摘要
   - 統一場論規則
   - 名詞解釋（完整版）

2. **狀態轉移文件**（跨對話繼承）

---

## 免責聲明

本框架為學術研究性質的期權分析工具，不構成投資建議。
所有分析基於公開數據，預測存在固有不確定性。
