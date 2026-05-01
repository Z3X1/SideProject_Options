# Unified Field Theory v1.8 — GEX Oracle Core Rules

> Snapshot S21 · 2026-03-27 · Version v1.8

---

## Unified Field Equation

```
P(settlement at X) = 0.40×GBM + 0.10×GEX + 0.28×behavioral signals
                   + 0.12×Bayesian + 0.10×time decay
```

---

## Core Rules

### Rule #1 — Put Wall Three-State Model
- OTM (Spot far above PW) → Gamma ≈ 0, no impact on price
- ATM (Spot ≈ PW) → Maximum gamma, most unstable zone
- ITM (Spot below PW) → Market maker net long = dynamic support floor

### Rule #2 — MACD Signal Lifetime Standard
- 15min: minimum 6.5 hours
- 4h: minimum 104 hours
- 1D: minimum 26 days
- Signal below minimum lifetime = noise; do not record as a valid signal

### Rule #3 — RSI Mechanical Oversold Filter
- Mechanical rollover (RSI rebounds sharply while Spot falls simultaneously) = effect ×0.5
- Genuine oversold (duration > 1 candle + RSI direction consistent with price) = effect ×1.0

### Rule #4 — Diminishing Returns on Repeated Confirmation
- N=1 (first time): ×1.5–2.0
- N=2–3: ×1.1–1.2
- N=4–5: ×1.05
- N≥6: ×1.02

### Rule #5 — Funding Rate Oscillation Pattern
- Shorts reload every 8h cycle
- Deeper oscillation floor trend = stronger short conviction
- FR crossing 0% = change in long/short cost direction = most important trigger signal

### Rule #6 — GEX Data Representativeness
- USDC subset: absolute quantities invalid; direction and structure valid
- Cross-expiry PCR requires OI ≥ 100 contracts for statistical significance

### Rule #7 — USDT LPI Five-Level Scale
- $0.9999+ (normal) / $0.999x (micro-stress) / $0.99x (tense)
- $0.97x (panic) / <$0.97 (crisis)

### Rule #8 — Short Squeeze Sufficient-Condition Product Method
```
P(SS) = P(FR negative) × P(catalyst 15%) × P(breakout holds) × P(time)
```
- 27MAR cycle: 12–25%
- 24APR cycle (28 days): 35%

### Rule #9 — EMH Boundary
- Best point prediction = current spot price
- Framework alpha lies in: distribution shape + conditional probability + risk management

### Rule #10 — Regime Framework  ✦ NEW in v1.8
- POS Regime (Spot > Gamma Flip): market maker acts as stabilizer; Layer1 + Layer2 merged
- NEG Regime (Spot < Gamma Flip): market maker acts as amplifier; Layer1 / Layer2 strictly separated

---

## Trigger Conditions

### Hard Triggers (any one satisfied → immediate update + deep collision)
- FR crossover: -0.01% / -0.005% / 0% / +0.005% / +0.01%
- Spot move: > ±0.5σ (T=28d ≈ ±$4,954)
- L/S round number: 1.5 / 2.0 / 2.5 / 3.0 (behavioral signal; reduces GEX weight)
- OI jump: > ±300 contracts, must align with FR direction
- Forced time updates: T = 24h / 6h / 2h (one update each)

### Non-Trigger Conditions
- Mechanical RSI rollover (RSI rises while Spot falls)
- Repeated confirmation N≥6
- MACD signal with insufficient lifetime
- T < 1h (stop analysis, monitor only)
- Subjective desire (no signal condition is satisfied)

---

## Version History

| Version | Snapshot | Core Update |
|---------|----------|-------------|
| v1.0 | S13 | Initial framework established |
| v1.3 | S16 | SS sufficient-condition product method |
| v1.5 | S17 | Full 9-round adversarial collision specification |
| v1.6 | S18 | Fibonacci support three-state model |
| v1.7 | S19 | 4h RSI dual-oversold classification |
| v1.7b | S20 | RSI mechanical filter (Rule #3 supplement) |
| v1.8 | S21 | POS/NEG Regime complete separation (Rule #10) |
