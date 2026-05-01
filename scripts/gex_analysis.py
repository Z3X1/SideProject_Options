"""
GEX Oracle — BTC Deribit Options Analysis Engine
Unified Field Theory v1.8 · Python Analysis Script

Usage:
  python gex_analysis.py --csv BTC_USDC-24APR26-export.csv --spot 68350 --dvol 52.35

Dependencies:
  pip install pandas numpy scipy matplotlib
"""

import argparse
import math
import json
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# Constants & Parameters
# ─────────────────────────────────────────────
FIELD_WEIGHTS = {
    "gbm":        0.40,
    "gex":        0.10,
    "behavioral": 0.28,
    "bayesian":   0.12,
    "time_decay": 0.10,
}

RSI_OVERSOLD   = 30
RSI_OVERBOUGHT = 70

MACD_MIN_LIFE = {
    "15m": 6.5,   # 小時
    "4h":  104,   # 小時
    "1D":  26 * 24,  # 小時（26天）
}

FR_TRIGGERS = [-0.01, -0.005, 0.0, 0.005, 0.01]  # 百分比
LS_TRIGGERS = [1.5, 2.0, 2.5, 3.0]

# ─────────────────────────────────────────────
# Core Calculations
# ─────────────────────────────────────────────

def compute_gbm_distribution(spot: float, dvol: float, days_to_expiry: int):
    """
    GBM（幾何布朗運動）正態分布
    Returns: (mean, sigma, percentiles)
    """
    T_years = days_to_expiry / 365
    sigma_dollar = spot * (dvol / 100) * math.sqrt(T_years)

    percentiles = {}
    z_scores = {
        "p2.5": -1.96, "p16": -1.0, "p25": -0.674,
        "p50": 0.0,
        "p75": 0.674,  "p84": 1.0,  "p97.5": 1.96,
    }
    for label, z in z_scores.items():
        percentiles[label] = round(spot * math.exp(z * sigma_dollar / spot), 0)

    return {
        "mean": spot,
        "sigma_dollar": round(sigma_dollar, 0),
        "sigma_pct": round((dvol / 100) * math.sqrt(T_years) * 100, 2),
        "percentiles": percentiles,
    }


def classify_regime(spot: float, gamma_flip: float) -> dict:
    """
    Rule #10：POS / NEG Regime 分類
    """
    if spot > gamma_flip:
        return {
            "regime": "POS",
            "description": "POS Regime — market maker穩定器",
            "layer_mode": "Layer1 + Layer2 merged",
            "mm_behavior": "counter-hedging; volatility self-suppresses",
        }
    else:
        return {
            "regime": "NEG",
            "description": "NEG Regime — market maker放大器",
            "layer_mode": "Layer1 / Layer2 strictly separated",
            "mm_behavior": "directional hedging; volatility self-reinforces",
        }


def classify_put_wall(spot: float, put_wall: float) -> dict:
    """
    Rule #1：Put Wall 三態
    """
    distance_pct = (spot - put_wall) / spot * 100
    if distance_pct > 5:
        state = "OTM"
        description = "Gamma ≈ 0; Put Wall has no impact on spot"
        impact = 0.0
    elif abs(distance_pct) <= 5:
        state = "ATM"
        description = "Maximum gamma; most unstable zone"
        impact = 1.0
    else:
        state = "ITM"
        description = "market maker淨買入 = 動態支撐"
        impact = 0.8
    return {"state": state, "description": description, "impact": impact, "distance_pct": round(distance_pct, 2)}


def compute_ss_probability(fr_negative: bool, catalyst_prob: float,
                            breakout_prob: float, days_to_expiry: int) -> float:
    """
    Rule #8：SS 充分條件乘積法
    P(SS) = P(FR負) × P(催化劑) × P(突破站穩) × P(時間)
    """
    p_fr = 0.7 if fr_negative else 0.2
    p_time = min(days_to_expiry / 28, 1.0)
    p_ss = p_fr * catalyst_prob * breakout_prob * p_time
    return round(p_ss, 3)


def classify_rsi(rsi: float, timeframe: str,
                 mechanical_rollup: bool = False) -> dict:
    """
    Rule #3：RSI 機械超賣篩選
    """
    if rsi <= RSI_OVERSOLD:
        if mechanical_rollup:
            signal = "機械超賣"
            multiplier = 0.5
        else:
            signal = "真實超賣"
            multiplier = 1.0
    elif rsi >= RSI_OVERBOUGHT:
        signal = "超買"
        multiplier = 1.0
    else:
        signal = "中性"
        multiplier = 0.0

    return {
        "rsi": rsi,
        "timeframe": timeframe,
        "signal": signal,
        "multiplier": multiplier,
    }


def check_fr_trigger(current_fr: float) -> list:
    """
    Rule #5：FR 觸發條件檢查
    """
    triggered = []
    for threshold in FR_TRIGGERS:
        if abs(current_fr - threshold) < 0.001:
            triggered.append(f"FR crossed {threshold}% (hard trigger)")
    return triggered


def repeat_confirmation_weight(n: int) -> float:
    """
    Rule #4：重複確認邊際遞減
    """
    if n == 1:
        return 1.75   # 1.5-2x 中值
    elif n <= 3:
        return 1.15
    elif n <= 5:
        return 1.05
    else:
        return 1.02


def compute_bayesian_scenario(
    regime: str,
    fr: float,
    rsi_4h: float,
    ls_ratio: float,
    pcr: float,
) -> dict:
    """
    貝葉斯情境概率（簡化版）
    Returns: Scenario B (Mean Reversion)、Scenario A (Strong Rally)、SS 概率
    """
    # Base probabilities
    p_b = 0.60
    p_a = 0.15
    p_ss = 0.25

    # Regime adjustment
    if regime == "POS":
        p_b += 0.10
        p_ss -= 0.05
    else:
        p_ss += 0.15
        p_b -= 0.10

    # FR adjustment
    if fr < -0.005:
        p_ss += 0.10
        p_b -= 0.05
    elif fr > 0.005:
        p_a += 0.05
        p_ss -= 0.05

    # RSI adjustment
    if rsi_4h < 30:
        p_b += 0.05

    # L/S adjustment
    if ls_ratio > 2.0:
        p_ss += 0.05

    # Normalize
    total = p_a + p_b + p_ss
    return {
        "scenario_b": round(p_b / total, 3),
        "scenario_a": round(p_a / total, 3),
        "ss":         round(p_ss / total, 3),
    }


# ─────────────────────────────────────────────
# CSV parsing (Deribit format)
# ─────────────────────────────────────────────

def parse_deribit_csv(filepath: str) -> dict:
    """
    解析 Deribit CSV Export，計算 GEX 結構
    Expected columns: instrument_name, strike, type, open_interest, mark_price, gamma
    """
    try:
        import pandas as pd
    except ImportError:
        print("⚠ pandas required：pip install pandas")
        return {}

    df = pd.read_csv(filepath)

    # Normalize column names
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

    calls = df[df['type'].str.upper() == 'C'].copy()
    puts  = df[df['type'].str.upper() == 'P'].copy()

    # GEX = gamma x OI x spot^2 x 0.01 (market maker inverse position)
    # Simplified calculation (no spot-weighting)
    call_oi_by_strike = calls.groupby('strike')['open_interest'].sum()
    put_oi_by_strike  = puts.groupby('strike')['open_interest'].sum()

    # Compute net GEX across all strikes
    all_strikes = sorted(set(call_oi_by_strike.index) | set(put_oi_by_strike.index))
    gex_by_strike = {}
    for strike in all_strikes:
        c_oi = call_oi_by_strike.get(strike, 0)
        p_oi = put_oi_by_strike.get(strike, 0)
        gex_by_strike[strike] = c_oi - p_oi  # positive = Call dominant

    # Locate key price levels
    max_call_strike = call_oi_by_strike.idxmax() if len(call_oi_by_strike) > 0 else None
    max_put_strike  = put_oi_by_strike.idxmax()  if len(put_oi_by_strike) > 0 else None

    # PCR
    total_call_oi = calls['open_interest'].sum()
    total_put_oi  = puts['open_interest'].sum()
    pcr = round(total_put_oi / total_call_oi, 3) if total_call_oi > 0 else 0

    return {
        "total_call_oi":  int(total_call_oi),
        "total_put_oi":   int(total_put_oi),
        "pcr":            pcr,
        "call_wall":      int(max_call_strike) if max_call_strike else None,
        "put_wall":       int(max_put_strike) if max_put_strike else None,
        "gex_by_strike":  {int(k): round(v, 2) for k, v in gex_by_strike.items()},
    }


# ─────────────────────────────────────────────
# Main Analysis Engine
# ─────────────────────────────────────────────

def run_analysis(params: dict) -> dict:
    """
    統一場論完整分析流程
    """
    spot     = params["spot"]
    dvol     = params["dvol"]
    days     = params.get("days_to_expiry", 28)
    fr       = params.get("fr", 0.0)
    ls_ratio = params.get("ls_ratio", 1.0)
    pcr      = params.get("pcr", 1.0)

    gamma_flip = params.get("gamma_flip", spot * 0.99)
    gamma_mp   = params.get("gamma_mp", spot * 1.05)
    call_wall  = params.get("call_wall", spot * 1.15)
    put_wall   = params.get("put_wall", spot * 0.85)

    rsi_4h     = params.get("rsi_4h", 50.0)
    rsi_4h_mechanical = params.get("rsi_4h_mechanical", False)

    # --- Compute modules ---
    gbm      = compute_gbm_distribution(spot, dvol, days)
    regime   = classify_regime(spot, gamma_flip)
    pw_state = classify_put_wall(spot, put_wall)
    rsi_sig  = classify_rsi(rsi_4h, "4h", rsi_4h_mechanical)
    fr_trig  = check_fr_trigger(fr)

    ss_prob = compute_ss_probability(
        fr_negative   = fr < 0,
        catalyst_prob = 0.15,
        breakout_prob = 0.60 if regime["regime"] == "NEG" else 0.40,
        days_to_expiry = days,
    )

    scenarios = compute_bayesian_scenario(
        regime   = regime["regime"],
        fr       = fr,
        rsi_4h   = rsi_4h,
        ls_ratio = ls_ratio,
        pcr      = pcr,
    )

    # --- Prediction targets ---
    target_median = gamma_mp  # Gamma-MP = settlement median anchor (POS Regime)
    target_lower  = gbm["percentiles"]["p16"]
    target_upper  = gbm["percentiles"]["p84"]

    return {
        "timestamp":    datetime.utcnow().isoformat() + "Z",
        "spot":         spot,
        "dvol":         dvol,
        "days_to_expiry": days,
        "framework_version": "v1.8",
        "regime":       regime,
        "gbm":          gbm,
        "put_wall_state": pw_state,
        "rsi_signal":   rsi_sig,
        "fr_triggers":  fr_trig,
        "ss_probability": ss_prob,
        "scenarios":    scenarios,
        "target": {
            "median": target_median,
            "lower_1sigma": target_lower,
            "upper_1sigma": target_upper,
        },
        "gex_structure": {
            "gamma_flip": gamma_flip,
            "gamma_mp":   gamma_mp,
            "call_wall":  call_wall,
            "put_wall":   put_wall,
        },
    }


def print_report(result: dict):
    """
    終端機輸出報告
    """
    print("\n" + "═" * 60)
    print(f"  GEX Oracle 分析報告 · {result['framework_version']}")
    print(f"  {result['timestamp']}")
    print("═" * 60)

    print(f"\n[Market State]")
    print(f"  Spot    : ${result['spot']:,.0f}")
    print(f"  DVOL    : {result['dvol']}%")
    print(f"  σ(T={result['days_to_expiry']}d): ±${result['gbm']['sigma_dollar']:,.0f}")

    r = result['regime']
    print(f"\n[Regime Classification]")
    print(f"  {r['description']}")
    print(f"  {r['layer_mode']}")

    g = result['gex_structure']
    print(f"\n[GEX Key Price Levels]")
    print(f"  Put Wall   : ${g['put_wall']:,}  （{result['put_wall_state']['state']}）")
    print(f"  Gamma Flip : ${g['gamma_flip']:,}")
    print(f"  Spot       : ${result['spot']:,}  ← current")
    print(f"  Gamma-MP   : ${g['gamma_mp']:,}")
    print(f"  Call Wall  : ${g['call_wall']:,}")

    s = result['scenarios']
    print(f"\n[Scenario Probabilities]")
    print(f"  Scenario B (Mean Reversion): {s['scenario_b']*100:.0f}%")
    print(f"  Scenario A (Strong Rally)  : {s['scenario_a']*100:.0f}%")
    print(f"  SS (Shock Scenario)       : {result['ss_probability']*100:.0f}%")

    t = result['target']
    print(f"\n[Prediction Target]")
    print(f"  Median: ${t['median']:,}")
    print(f"  -1σ  : ${t['lower_1sigma']:,}")
    print(f"  +1σ  : ${t['upper_1sigma']:,}")

    if result['fr_triggers']:
        print(f"\n⚠ Hard trigger: {', '.join(result['fr_triggers'])}")

    print("\n" + "═" * 60 + "\n")


# ─────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="GEX Oracle 分析引擎")
    parser.add_argument("--spot",     type=float, required=True,  help="Current BTC spot price")
    parser.add_argument("--dvol",     type=float, required=True,  help="DVOL volatility (percent, e.g. 52.35)")
    parser.add_argument("--days",     type=int,   default=28,     help="Days to expiry (default: 28)")
    parser.add_argument("--fr",       type=float, default=0.0,    help="Funding rate (percent, e.g. -0.669)")
    parser.add_argument("--ls",       type=float, default=1.0,    help="Long/Short ratio")
    parser.add_argument("--pcr",      type=float, default=1.0,    help="Put/Call Ratio")
    parser.add_argument("--gamma-flip", type=float, default=None, help="Gamma Flip price")
    parser.add_argument("--gamma-mp",   type=float, default=None, help="Gamma-MP price")
    parser.add_argument("--call-wall",  type=float, default=None, help="Call Wall price")
    parser.add_argument("--put-wall",   type=float, default=None, help="Put Wall price")
    parser.add_argument("--rsi-4h",   type=float, default=50.0,  help="4h RSI6")
    parser.add_argument("--csv",      type=str,   default=None,   help="Deribit CSV file path")
    parser.add_argument("--json",     action="store_true",        help="Output in JSON format")

    args = parser.parse_args()

    params = {
        "spot":          args.spot,
        "dvol":          args.dvol,
        "days_to_expiry": args.days,
        "fr":            args.fr / 100,  # convert to decimal
        "ls_ratio":      args.ls,
        "pcr":           args.pcr,
        "rsi_4h":        args.rsi_4h,
        "gamma_flip":    args.gamma_flip or args.spot * 0.988,
        "gamma_mp":      args.gamma_mp   or args.spot * 1.054,
        "call_wall":     args.call_wall  or args.spot * 1.14,
        "put_wall":      args.put_wall   or args.spot * 0.834,
    }

    # If CSV provided, parse GEX structure first
    if args.csv:
        print(f"📊 Parsing CSV: {args.csv}")
        gex_data = parse_deribit_csv(args.csv)
        if gex_data:
            if gex_data.get("call_wall"):
                params["call_wall"] = gex_data["call_wall"]
            if gex_data.get("put_wall"):
                params["put_wall"] = gex_data["put_wall"]
            if gex_data.get("pcr"):
                params["pcr"] = gex_data["pcr"]
            print(f"  Call Wall: ${gex_data.get('call_wall')}")
            print(f"  Put Wall : ${gex_data.get('put_wall')}")
            print(f"  PCR      : {gex_data.get('pcr')}")

    result = run_analysis(params)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
