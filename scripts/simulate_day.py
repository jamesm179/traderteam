import time
from atlas.core import ATLAS, Regime
from atlas.commands import CommandHandler
from atlas.reporting import generate_daily_report
from traders.ghost import Ghost
from traders.nova import Nova
from traders.rex import Rex
from traders.sage import Sage
from traders.vega import Vega
from traders.cipher import Cipher

def simulate_day():
    print("--- STARTING ATLAS DAILY SIMULATION ---")

    # 05:45 Wake up and initialize
    atlas = ATLAS()
    atlas.traders = {
        "GHOST": Ghost(),
        "NOVA": Nova(),
        "REX": Rex(),
        "SAGE": Sage(),
        "VEGA": Vega(),
        "CIPHER": Cipher()
    }
    print("05:45 - ATLAS and traders initialized.")

    # 06:00 Classify Regime
    market_data = {"VIX": 18.5, "BTC_CHANGE": 0.02}
    regime = atlas.classify_regime(market_data)
    print(f"06:00 - Regime classified as: {regime}")

    # 06:15 Broadcast Daily Brief & Allocate Capital
    atlas.allocate_capital()
    print("06:15 - Daily brief broadcasted and capital allocated.")
    for name, trader in atlas.traders.items():
        print(f"  {name} allocation: ${trader.capital_limit:,.2f}")

    # 06:30 Traders begin scanning
    for trader in atlas.traders.values():
        trader.scan()
    print("06:30 - Morning scans complete.")

    # 07:30 Session starts - simulating some trades
    print("07:30 - Market session begins.")
    atlas.traders["GHOST"].execute_trade("BTC Order Book Imbalance")
    atlas.traders["CIPHER"].execute_trade("SOL Momentum Breakout")

    # Intraday loop (simplified)
    print("... Simulating midday ...")
    atlas.traders["GHOST"].daily_loss = 200 # Some loss
    atlas.check_kill_switches()

    # 22:00 Post-session review
    print("22:00 - Post-session review.")
    report = generate_daily_report(atlas)
    print("\n--- DAILY SUMMARY ---")
    print(report)
    print("----------------------\n")

    # 22:30 Overnight Evolution
    atlas.run_overnight_cycle()

    print("--- SIMULATION COMPLETE ---")

if __name__ == "__main__":
    simulate_day()
