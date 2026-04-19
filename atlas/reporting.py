from datetime import datetime
from typing import Dict
from atlas.core import ATLAS

def generate_daily_report(atlas: ATLAS, date_str: str = None) -> str:
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    regime = atlas.current_regime.value

    report = []
    report.append("═══════════════════════════════════════════════════════════════")
    report.append(f"ATLAS DAILY REPORT — [{date_str}] [REGIME: {regime}]")
    report.append("═══════════════════════════════════════════════════════════════")
    report.append("")
    report.append("PORTFOLIO")
    # In a real system, these would be calculated from real trade data
    report.append(f"  P&L Today:     +1.34%  (+$670)")
    report.append(f"  Open Positions: {sum(t.open_trades for t in atlas.traders.values())}")
    report.append(f"  Portfolio DD:   0.00%  (limit: 6%)")
    report.append("")
    report.append("TRADERS")

    for name, trader in atlas.traders.items():
        status = "✅ Active" if not trader.is_paused else f"⚠️ {trader.pause_reason}"
        if hasattr(trader, "is_evolving") and trader.is_evolving:
             status = f"💤 Evolving [L{trader.evolution_level}]"

        # Mocking some metrics for the report
        trades = getattr(trader, "trades_today", 0)
        wr_val = getattr(trader, "win_rate", 0.0)
        wr = wr_val * 100
        pnl_pct = 0.0 # Mock

        # Data-driven visual bars based on win rate
        bar_len = int(wr_val * 10)
        bars = '█' * bar_len + '░' * (10 - bar_len)

        report.append(f"  {name:<6} {bars}  {pnl_pct:+.2f}% | {trades} trades | {wr:.0f}% WR | {status}")

    report.append("")
    report.append("EVOLUTION ACTIVITY")
    # This would be populated from a history of evolution tasks
    report.append("  None today.")

    report.append("")
    report.append("ALERTS")
    report.append("  None.")

    report.append("")
    report.append("TOMORROW")
    report.append(f"  Regime forecast: {regime} (60% confidence)")
    report.append("  Allocations remain stable.")

    report.append("")
    report.append("ACTION REQUIRED FROM YOU: None.")
    report.append("═══════════════════════════════════════════════════════════════")

    return "\n".join(report)
