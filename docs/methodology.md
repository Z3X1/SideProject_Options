# GEX Oracle — Methodology

## Core Architecture

### Adversarial Collision Framework
H_BULL and H_BEAR take turns attacking each other's arguments. An Oracle referee adjudicates convergence.
- Framework version is updated after each round concludes
- Termination condition: a repeated argument is detected

### GEX (Gamma Exposure) Analysis
- **Gamma Flip**: The price at which market makers transition from short gamma to long gamma
- **Gamma-MP (Gamma Magnet Point)**: Highest gamma concentration; exerts gravitational pull on spot price
- **Call Wall / Put Wall**: Option walls — large OI concentrations forming resistance / support
- **PCR (Put/Call Ratio)**: Cross-expiry comparison; near-term defense vs. far-term offense

### Regime Framework
| Regime | Condition | Market Maker Behavior | Layer Merge |
|--------|-----------|----------------------|-------------|
| POS | Spot > Gamma Flip | Stabilizer (counter-hedging) | Layer1 + Layer2 merged |
| NEG | Spot < Gamma Flip | Amplifier (directional hedging) | Layer1 / Layer2 strictly separated |

---

## Signal Layers

### Layer 1 (High Confidence)
- GEX structure (Gamma Flip, Call/Put Wall)
- Bayesian scenario probabilities
- Funding rate crossover triggers

### Layer 2 (Medium Confidence)
- Technical indicators (MACD, RSI, EMA)
- Long/Short ratio behavioral signals
- Cross-expiry PCR structure

### Layer 3 (Low Confidence — supplementary only)
- 15min short-term signals (reliability 30%)
- Mechanical RSI rollovers
- MACD signals with insufficient signal lifetime

---

## Output Format

Each snapshot produces:
1. **HTML Dashboard** (dark theme, multi-tab)
   - GEX structure analysis
   - Adversarial collision process
   - Scenario probability distribution
   - Technical summary
   - Unified Field Theory rules
   - Full glossary

2. **State Transfer Document** (for cross-conversation continuity)

---

## Disclaimer

This framework is an academic research-grade options analysis tool and does not constitute investment advice.
All analysis is based on publicly available data. Predictions carry inherent uncertainty.
