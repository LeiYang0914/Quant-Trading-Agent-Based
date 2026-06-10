"""Quick ETH backtest runner."""
import pandas as pd
from pathlib import Path

from src.signals.funding_rate_carry import FundingRateCarryConfig, compute_signals
from src.backtest.event_backtester import BacktestConfig, EventBacktester
from src.backtest.metrics import compute_metrics, PERIODS_PER_YEAR
from src.execution.fee_model import FeeModel
from src.execution.slippage_model import SlippageModel

ASSET = "ETH"
DATA_DIR = Path("data/glassnode")

fr = pd.read_parquet(DATA_DIR / f"{ASSET}_funding_rate_8h.parquet")
ohlc = pd.read_parquet(DATA_DIR / f"{ASSET}_spot_ohlc_8h.parquet")
merged = fr[["timestamp", "funding_rate", "asset"]].copy()
merged["spot_price"] = ohlc["close"].values[: len(merged)]
merged["mark_price"] = merged["spot_price"]

print(f"ETH data: {len(merged):,} rows, {merged['timestamp'].iloc[0]} -> {merged['timestamp'].iloc[-1]}")

sig_cfg = FundingRateCarryConfig(
    funding_lookback_days=30, funding_threshold_pct=5.0,
    crowding_upper_pct=90.0, crowding_lower_pct=10.0,
    max_position_pct=0.20, dynamic_carry_cap_pct=30.0,
)
bt_cfg = BacktestConfig(
    initial_capital=100_000.0, fee_model=FeeModel(taker_bps=4.0, maker_bps=2.0),
    slippage_model=SlippageModel(base_bps=2.0), max_position_pct=0.20,
    enable_carry_leg=True, enable_crowding_leg=True, rebalance_threshold=0.05,
)

signals_df = compute_signals(merged, sig_cfg)
tester = EventBacktester(bt_cfg)

# Full period
r = tester.run(signals_df, ohlc)
m = compute_metrics(r.equity_curve, None, periods_per_year=PERIODS_PER_YEAR)

# In-sample 2023
s_is = signals_df[signals_df["timestamp"] < "2024-01-01"]
o_is = ohlc[ohlc["timestamp"] < "2024-01-01"]
r_is = tester.run(s_is, o_is) if len(s_is) > 1 else None
m_is = compute_metrics(r_is.equity_curve, None, periods_per_year=PERIODS_PER_YEAR) if r_is and len(r_is.equity_curve) > 1 else None

# Out-of-sample 2024-2025
s_oos = signals_df[signals_df["timestamp"] >= "2024-01-01"]
o_oos = ohlc[ohlc["timestamp"] >= "2024-01-01"]
r_oos = tester.run(s_oos, o_oos) if len(s_oos) > 1 else None
m_oos = compute_metrics(r_oos.equity_curve, None, periods_per_year=PERIODS_PER_YEAR) if r_oos and len(r_oos.equity_curve) > 1 else None

fr_d = signals_df["funding_rate"].describe()
ann_d = signals_df["annualized_fr_pct"].describe()

def f(v, spec=".2f"):
    return "N/A" if v is None else format(v, spec)

print(f"""
=== ETH Backtest Results (Real Glassnode Data) ===

Full Period (2023-2025):
  Total return:       {m.total_return_pct:.2f}%
  Ann. return:        {m.annualized_return_pct:.2f}%
  Ann. volatility:    {m.annualized_volatility_pct:.2f}%
  Sharpe:             {f(m.sharpe_ratio)}
  Sortino:            {f(m.sortino_ratio)}
  Calmar:             {f(m.calmar_ratio)}
  Max DD:             {m.max_drawdown_pct:.2f}%
  Max DD duration:    {m.max_drawdown_duration_days:.1f} days
  Trades:             {m.total_trades}
  Turnover:           {m.turnover_pct:.0f}% pa
  End equity:         ${r.equity_curve.iloc[-1]:,.2f}

PnL Attribution:
  Funding PnL:        ${r.funding_pnl_total:,.2f}
  Price PnL:          ${r.price_pnl_total:,.2f}
  Fees:               ${r.fees_total:,.2f}
  Slippage:           ${r.slippage_total:,.2f}
  Net PnL:            ${r.funding_pnl_total + r.price_pnl_total - r.fees_total - r.slippage_total:,.2f}

Subperiod:
  IS (2023):          Ret={f(m_is.total_return_pct) if m_is else 'N/A'}%  Sharpe={f(m_is.sharpe_ratio) if m_is else 'N/A'}  MaxDD={f(m_is.max_drawdown_pct) if m_is else 'N/A'}%
  OOS (2024-2025):    Ret={f(m_oos.total_return_pct) if m_oos else 'N/A'}%  Sharpe={f(m_oos.sharpe_ratio) if m_oos else 'N/A'}  MaxDD={f(m_oos.max_drawdown_pct) if m_oos else 'N/A'}%

Signal Stats:
  Carry-active:       {int((signals_df['carry_weight'].abs() > 0.001).sum()):,} ({(signals_df['carry_weight'].abs() > 0.001).mean()*100:.1f}%)
  Crowding long:      {int((signals_df['crowding_signal'] == 1).sum()):,}
  Crowding short:     {int((signals_df['crowding_signal'] == -1).sum()):,}

Funding Rate (Real ETH):
  Mean:               {fr_d['mean']:.6f} (ann: {ann_d['mean']:.2f}%)
  Std:                {fr_d['std']:.6f} (ann: {ann_d['std']:.2f}%)
  Min:                {fr_d['min']:.6f} (ann: {ann_d['min']:.2f}%)
  Max:                {fr_d['max']:.6f} (ann: {ann_d['max']:.2f}%)
""")
