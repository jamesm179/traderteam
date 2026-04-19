from atlas.core import ATLAS
from atlas.reporting import generate_daily_report

class MockTrader:
    def __init__(self, name):
        self.name = name
        self.is_paused = False
        self.open_trades = 0
        self.trades_today = 5
        self.win_rate = 0.6
        self.is_evolving = False

def test_reporting():
    atlas = ATLAS()
    atlas.traders = {"GHOST": MockTrader("GHOST"), "NOVA": MockTrader("NOVA")}
    atlas.traders["NOVA"].is_paused = True
    atlas.traders["NOVA"].pause_reason = "Manual pause"

    report = generate_daily_report(atlas, "2023-10-27")
    print(report)

    assert "ATLAS DAILY REPORT — [2023-10-27]" in report
    assert "GHOST" in report
    assert "NOVA" in report
    assert "Active" in report
    assert "Manual pause" in report

if __name__ == "__main__":
    test_reporting()
