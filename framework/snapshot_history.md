# GEX Oracle — Snapshot History

## Settlement Validation Record

| Expiry | Predicted Median | Actual Settlement | Error | σ | Status |
|--------|-----------------|-------------------|-------|---|--------|
| 26MAR26 | $70,860 | $70,020 | $840 | 0.41σ | ✓ |
| Fib $68,112 | — | $68,115.8 | $3.8 | — | ✓ |
| 27MAR26 | $68,636 | $68,625.39 | $10.6 | 0.02σ | ✓✓ |

---

## Snapshot Detail Log

| Snapshot | Time (UTC+8) | Spot | FR | L/S | OI | Notes | Version |
|----------|-------------|------|----|-----|----|-------|---------|
| S12 | 3/26 12:29 | $71,443 | +0.535% | — | — | σ=$2,072 | — |
| S13 | 3/26 11:12 | $70,848 | +0.032% | 1.479 | — | Scenario B 52% | v1.0 |
| S14 | 3/26 16:28 | $69,800 | +0.091% | 1.775 | — | 26MAR settlement $70,020 ✓ | — |
| S15 | 3/26 17:27 | $69,950 | +0.025% | 1.791 | — | — | — |
| S16 | 3/26 20:10 | $69,355 | -0.396% | 1.923 | — | SS structure established | v1.3 |
| S17 | 3/26 21:38 | $69,356 | -0.538% | 2.033 | — | 9-round full refutation | v1.5 |
| S18 | 3/27 11:00 | $68,867 | +0.001% | 2.239 | — | Fib $68,112 error $3 ✓ | v1.6 |
| S19 | 3/27 13:10 | $68,671 | -0.469% | 2.261 | — | 4h RSI dual oversold | v1.7 |
| S20 | 3/27 13:32 | $68,546 | -0.528% | 2.268 | — | RSI mechanical filter | v1.7b |
| Settlement | 3/27 16:00 | $68,625.39 | — | — | — | Error $10.6 (0.02σ) ✓✓ | — |
| S21 | 3/27 16:20 | $68,350 | -0.669% | 2.287 | 89,100 | POS Regime; new cycle begins | v1.8 |

---

## Current Cycle State (S21, 2026-03-27)

### Market Parameters
- **Spot**: $68,350
- **DVOL**: 52.35%
- **FR**: -0.00669% (deepest in series)
- **L/S**: 2.2870
- **OI**: 89,100 contracts (series high)

### Primary Expiry: 24APR26
- T = 28 days, σ = $9,908
- Gamma Flip: ~$67,500 (POS Regime active)
- Gamma-MP: $72,000 (↑ +$3,650, +0.37σ)
- Call Wall: $78,000
- Put Wall: $57,000 (far OTM, weak)
- PCR: 1.398

### Scenario Probabilities
- **Scenario B**: 82% (Bayesian; Layer1 + Layer2 merged)
- **SS probability (28 days)**: 35%

### Technical Summary
- 15min MACD: death cross; DIF = -69.01
- 4h MACD: accelerating deterioration; DIF = -447.31
- 1D MACD: continued deterioration; DIF = -165.90
- 4h RSI6: 25.48 (genuine oversold)

---

## Adversarial Collision Statistics

- Total collision rounds in series: **59**
- Framework version evolution: v1.0 → v1.8 (10 versions)
- Hit rate: 3/3 verifiable predictions (100%; small sample)
