# SideProject_Options — GEX Oracle BTC Deribit Options Analytics

> Adversarial Collision Framework × Unified Field Theory  
> Twitter: [@BTC_OptionsTW](https://twitter.com/BTC_OptionsTW) | [@kai6366](https://twitter.com/kai6366)

---

## Project Structure

```
gex-oracle/
├── dashboards/        # HTML dashboards (one per snapshot, versioned)
│   └── S{N}_YYYYMMDD_dashboard.html
├── framework/         # Unified Field Theory rule docs & state transfer docs
│   ├── unified_field_theory_v{N}.md
│   └── state_transfer_S{N}.md
├── data/              # Raw CSV data snapshots (.gitignore can optionally exclude)
│   └── snapshots/
├── scripts/           # Automation scripts
│   └── upload.sh
└── docs/              # Methodology documentation
    └── methodology.md
```

---

## Framework Version History

| Version | Snapshot | Key Updates |
|---------|----------|-------------|
| v1.0 | S13 | Initial adversarial collision framework |
| v1.3 | S16 | Short Squeeze structure established |
| v1.5 | S17 | 9-round full adversarial refutation complete |
| v1.6 | S18 | Fibonacci support validation (error $3) |
| v1.7 | S19 | 4h RSI dual-oversold classification rule |
| v1.7b | S20 | RSI mechanical filter supplement |
| v1.8 | S21 | POS/NEG Regime complete separation (Rule #10) |
| v2.0 | S31 | Current active version |

---

## Prediction Validation Record

| Expiry | Predicted Median | Actual Settlement | Error | σ |
|--------|-----------------|-------------------|-------|---|
| 26MAR26 | $70,860 | $70,020 | $840 | 0.41σ ✓ |
| 27MAR26 | $68,636 | $68,625.39 | $10.6 | 0.02σ ✓✓ |

---

## Unified Field Equation

```
P(settlement at X) = 0.40×GBM + 0.10×GEX + 0.28×behavioral signals
                   + 0.12×Bayesian + 0.10×time decay
```

---

## Data Sources

- **Options data**: Deribit CSV Export (full BTC-* instrument set)
- **Price / Technicals**: Binance (15min / 4h / 1D)
- **DVOL**: Deribit Volatility Index
