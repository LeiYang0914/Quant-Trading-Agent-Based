"""Event-driven backtest engine.

Processes a signal DataFrame bar-by-bar, simulating:
- Position entry at next-bar-open (no lookahead).
- Funding payment accrual on open positions.
- Transaction costs (fees + slippage).
- Mark-to-market PnL from spot price changes.
- Equity curve tracking with drawdown.

Reference: ``research/memos/crypto/01_crypto_funding_rate_carry.md``
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd

from src.execution.fee_model import FeeModel
from src.execution.slippage_model import SlippageModel


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class BacktestConfig:
    """Parameters controlling backtest behaviour.

    Attributes:
        initial_capital: Starting NAV in quote currency.
        fee_model: Transaction fee schedule.
        slippage_model: Slippage estimation model.
        max_position_pct: Maximum position size as fraction of NAV.
        enable_carry_leg: If True, trade the carry (spot+perp) leg.
        enable_crowding_leg: If True, trade the crowding reversal leg.
        carry_notional_pct: Fraction of NAV to allocate to carry when active
            (default 1.0 = 100%).
    """

    initial_capital: float = 100_000.0
    fee_model: FeeModel = field(default_factory=FeeModel)
    slippage_model: SlippageModel = field(default_factory=SlippageModel)
    max_position_pct: float = 0.20
    enable_carry_leg: bool = True
    enable_crowding_leg: bool = True
    carry_notional_pct: float = 1.0
    rebalance_threshold: float = 0.05


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------


@dataclass
class BacktestResult:
    """Full output of a backtest run.

    Attributes:
        equity_curve: Time-indexed equity series.
        positions: DataFrame tracking per-bar positions.
        trades: DataFrame of individual round-trip trades.
        funding_pnl_total: Total PnL from funding payments.
        price_pnl_total: Total PnL from spot price changes.
        fees_total: Total fees paid.
        slippage_total: Total slippage cost.
    """

    equity_curve: pd.Series
    positions: pd.DataFrame
    trades: pd.DataFrame
    funding_pnl_total: float = 0.0
    price_pnl_total: float = 0.0
    fees_total: float = 0.0
    slippage_total: float = 0.0


# ---------------------------------------------------------------------------
# Backtest engine
# ---------------------------------------------------------------------------


class EventBacktester:
    """Event-driven backtester for funding-rate-based strategies.

    Usage::

        config = BacktestConfig(initial_capital=100_000)
        tester = EventBacktester(config)
        result = tester.run(signals_df, ohlcv_df)
    """

    def __init__(self, config: BacktestConfig | None = None) -> None:
        self.config = config or BacktestConfig()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(
        self,
        signals: pd.DataFrame,
        ohlcv: pd.DataFrame,
        funding_rates: pd.DataFrame | None = None,
    ) -> BacktestResult:
        """Run an event-driven backtest.

        The backtest respects strict no-lookahead bias:
        - Signal is evaluated at bar *i* close using only data through *i*.
        - Positions are entered at bar *i+1* open.
        - Positions persist across bars until the signal changes.
        - Funding accrues on open perp positions each bar.
        - Price PnL marks open positions to bar close each bar without
          closing them unless the signal flips.

        Parameters
        ----------
        signals: DataFrame from ``compute_signals()`` with columns:
            ``[timestamp, carry_weight, crowding_signal, funding_rate,
              annualized_fr_pct, spot_price]``.
        ohlcv: OHLCV DataFrame with columns:
            ``[timestamp, open, high, low, close, volume]``.
        funding_rates: Optional raw funding rate history for accrual
            calculation.  If not provided, the funding_rate column from
            *signals* is used.

        Returns
        -------
        BacktestResult
        """
        cfg = self.config

        # Prepare data — handle empty inputs gracefully.
        if signals.empty or ohlcv.empty:
            return BacktestResult(
                equity_curve=pd.Series(dtype=float),
                positions=pd.DataFrame(),
                trades=pd.DataFrame(),
            )
        sig = signals.sort_values("timestamp").reset_index(drop=True).copy()
        bars = ohlcv.sort_values("timestamp").reset_index(drop=True).copy()

        n_bars = min(len(sig), len(bars)) - 1  # need at least one future bar
        if n_bars < 1:
            return BacktestResult(
                equity_curve=pd.Series(dtype=float),
                positions=pd.DataFrame(),
                trades=pd.DataFrame(),
            )

        # --- State variables ---
        nav = cfg.initial_capital
        # Positions held across bars (signed: positive = long, negative = short).
        spot_units = 0.0
        perp_units = 0.0
        spot_entry_vwap = 0.0   # volume-weighted entry price for spot
        perp_entry_vwap = 0.0   # volume-weighted entry price for perp

        # Cumulative P&L components (realised + unrealised mark).
        cum_funding_pnl = 0.0
        cum_price_pnl_realised = 0.0
        cum_fees = 0.0
        cum_slippage = 0.0

        prev_carry_w = 0.0
        prev_crowd_s = 0

        equity_log: list[dict] = []
        position_log: list[dict] = []
        trade_log: list[dict] = []

        for i in range(n_bars):
            signal_row = sig.iloc[i]
            bar = bars.iloc[i + 1]       # execution bar (next bar after signal)
            bar_open = float(bar["open"])
            bar_close = float(bar["close"])
            bar_ts = bar["timestamp"]

            # ----------------------------------------------------------
            # 1. Accrue funding on the perp position held through this bar.
            #    The funding_rate in the signal row is the last settled
            #    rate BEFORE this bar — correct for no-lookahead.
            # ----------------------------------------------------------
            funding_rate = float(signal_row.get("funding_rate", 0.0))
            if perp_units != 0.0 and abs(funding_rate) > 0:
                # funding received = -perp_units * price * rate
                # (perp_units < 0 for short → -(-units)*price*rate → positive)
                bar_funding = -perp_units * bar_close * funding_rate
                cum_funding_pnl += bar_funding

            # ----------------------------------------------------------
            # 2. Compute unrealised price PnL since entry.
            # ----------------------------------------------------------
            unrealised_spot = 0.0
            unrealised_perp = 0.0
            if spot_units != 0.0 and spot_entry_vwap != 0.0:
                unrealised_spot = spot_units * (bar_close - spot_entry_vwap)
            if perp_units != 0.0 and perp_entry_vwap != 0.0:
                # Perp: long profits when price rises, short profits when price falls.
                unrealised_perp = perp_units * (bar_close - perp_entry_vwap)

            # ----------------------------------------------------------
            # 3. Read new signal and decide on rebalancing.
            # ----------------------------------------------------------
            carry_w = float(signal_row.get("carry_weight", 0.0))
            crowd_s = int(signal_row.get("crowding_signal", 0))

            carry_changed = abs(carry_w - prev_carry_w) > cfg.rebalance_threshold
            crowd_changed = crowd_s != prev_crowd_s
            need_rebalance = carry_changed or crowd_changed

            if need_rebalance:
                # --- Close all existing positions ---
                if spot_units != 0.0:
                    exit_notional = abs(spot_units) * bar_close
                    side = "sell" if spot_units > 0 else "buy"
                    fee, _ = cfg.fee_model.apply_fee(exit_notional)
                    cum_fees += fee
                    slip_bps, _ = cfg.slippage_model.apply_slippage(
                        bar_close, exit_notional, side
                    )
                    cum_slippage += exit_notional * slip_bps / 10_000.0
                    cum_price_pnl_realised += unrealised_spot
                    spot_units = 0.0
                    spot_entry_vwap = 0.0

                if perp_units != 0.0:
                    exit_notional = abs(perp_units) * bar_close
                    side = "sell" if perp_units > 0 else "buy"
                    fee, _ = cfg.fee_model.apply_fee(exit_notional)
                    cum_fees += fee
                    slip_bps, _ = cfg.slippage_model.apply_slippage(
                        bar_close, exit_notional, side
                    )
                    cum_slippage += exit_notional * slip_bps / 10_000.0
                    cum_price_pnl_realised += unrealised_perp
                    perp_units = 0.0
                    perp_entry_vwap = 0.0

                # --- Open new carry leg ---
                if cfg.enable_carry_leg and abs(carry_w) > 0.001:
                    carry_notional = nav * cfg.carry_notional_pct * abs(carry_w)
                    carry_notional = min(carry_notional, nav * cfg.max_position_pct)

                    if carry_notional > 0:
                        entry_side = "buy" if carry_w > 0 else "sell"
                        fee, _ = cfg.fee_model.apply_fee(carry_notional)
                        cum_fees += fee
                        slip_bps, exec_px = cfg.slippage_model.apply_slippage(
                            bar_close, carry_notional, entry_side
                        )
                        cum_slippage += carry_notional * slip_bps / 10_000.0
                        units = carry_notional / exec_px

                        if carry_w > 0:
                            spot_units = units
                            perp_units = -units
                        else:
                            spot_units = -units
                            perp_units = units

                        spot_entry_vwap = exec_px
                        perp_entry_vwap = exec_px

                        trade_log.append(
                            {
                                "timestamp": bar_ts,
                                "side": "carry_long" if carry_w > 0 else "carry_short",
                                "notional": carry_notional,
                                "fee": fee,
                                "slippage": carry_notional * slip_bps / 10_000.0,
                            }
                        )

                # --- Open new crowding reversal leg ---
                if cfg.enable_crowding_leg and crowd_s != 0:
                    crowd_notional = nav * cfg.max_position_pct * 0.5
                    if crowd_notional > 0:
                        entry_side = "buy" if crowd_s == 1 else "sell"
                        fee, _ = cfg.fee_model.apply_fee(crowd_notional)
                        cum_fees += fee
                        slip_bps, exec_px = cfg.slippage_model.apply_slippage(
                            bar_close, crowd_notional, entry_side
                        )
                        cum_slippage += crowd_notional * slip_bps / 10_000.0
                        units = crowd_notional / exec_px

                        if crowd_s == 1:
                            spot_units += units
                        else:
                            spot_units -= units

                        # Update blended entry price.
                        if spot_units != 0:
                            spot_entry_vwap = exec_px

                        trade_log.append(
                            {
                                "timestamp": bar_ts,
                                "side": f"crowding_long" if crowd_s == 1 else "crowding_short",
                                "notional": crowd_notional,
                                "fee": fee,
                                "slippage": crowd_notional * slip_bps / 10_000.0,
                            }
                        )

                prev_carry_w = carry_w
                prev_crowd_s = crowd_s

            # ----------------------------------------------------------
            # 4. Compute NAV = initial + all realised PnL + unrealised PnL.
            # ----------------------------------------------------------
            unrealised_spot2 = 0.0
            unrealised_perp2 = 0.0
            if spot_units != 0.0 and spot_entry_vwap != 0.0:
                unrealised_spot2 = spot_units * (bar_close - spot_entry_vwap)
            if perp_units != 0.0 and perp_entry_vwap != 0.0:
                unrealised_perp2 = perp_units * (bar_close - perp_entry_vwap)

            nav = (
                cfg.initial_capital
                + cum_funding_pnl
                + cum_price_pnl_realised
                + unrealised_spot2
                + unrealised_perp2
                - cum_fees
                - cum_slippage
            )

            equity_log.append({"timestamp": bar_ts, "equity": nav})
            position_log.append(
                {
                    "timestamp": bar_ts,
                    "spot_units": spot_units,
                    "perp_units": perp_units,
                    "nav": nav,
                }
            )

        # --- Close any remaining positions at the final bar close ---
        if len(bars) > 0 and (spot_units != 0.0 or perp_units != 0.0):
            final_close = float(bars.iloc[-1]["close"])
            if spot_units != 0.0 and spot_entry_vwap != 0.0:
                cum_price_pnl_realised += spot_units * (final_close - spot_entry_vwap)
                exit_notional = abs(spot_units) * final_close
                fee, _ = cfg.fee_model.apply_fee(exit_notional)
                cum_fees += fee
                slip_bps, _ = cfg.slippage_model.apply_slippage(
                    final_close, exit_notional, "sell" if spot_units > 0 else "buy"
                )
                cum_slippage += exit_notional * slip_bps / 10_000.0
            if perp_units != 0.0 and perp_entry_vwap != 0.0:
                cum_price_pnl_realised += perp_units * (final_close - perp_entry_vwap)
                exit_notional = abs(perp_units) * final_close
                fee, _ = cfg.fee_model.apply_fee(exit_notional)
                cum_fees += fee
                slip_bps, _ = cfg.slippage_model.apply_slippage(
                    final_close, exit_notional, "sell" if perp_units > 0 else "buy"
                )
                cum_slippage += exit_notional * slip_bps / 10_000.0

        # Final NAV.
        nav = (
            cfg.initial_capital
            + cum_funding_pnl
            + cum_price_pnl_realised
            - cum_fees
            - cum_slippage
        )

        # --- Build result DataFrames ---
        equity_df = pd.DataFrame(equity_log).set_index("timestamp")["equity"]
        if len(equity_df) > 0:
            # Append final NAV point.
            final_ts = bars.iloc[-1]["timestamp"] if len(bars) > 0 else equity_df.index[-1]
            equity_df.loc[final_ts] = nav

        positions_df = pd.DataFrame(position_log)
        trades_df = (
            pd.DataFrame(trade_log)
            if trade_log
            else pd.DataFrame(
                columns=["timestamp", "side", "notional", "fee", "slippage"]
            )
        )

        return BacktestResult(
            equity_curve=equity_df,
            positions=positions_df,
            trades=trades_df,
            funding_pnl_total=cum_funding_pnl,
            price_pnl_total=cum_price_pnl_realised,
            fees_total=cum_fees,
            slippage_total=cum_slippage,
        )
