from atlas.core import ATLAS

class MockTrader:
    def __init__(self):
        self.open_trades = 0
        self.pending_signals = 0
        self.scan_returned_no_setups = True
        self.minutes_since_last_trade = 100
        self.avg_setup_frequency_minutes = 60

def test_idle_detection():
    atlas = ATLAS()
    trader = MockTrader()

    # Idle case
    assert atlas.is_trader_idle(trader) == True

    # Not idle (has open trade)
    trader.open_trades = 1
    assert atlas.is_trader_idle(trader) == False
    trader.open_trades = 0

    # Not idle (has pending signal)
    trader.pending_signals = 1
    assert atlas.is_trader_idle(trader) == False
    trader.pending_signals = 0

    # Not idle (scan returned setups)
    trader.scan_returned_no_setups = False
    assert atlas.is_trader_idle(trader) == False
    trader.scan_returned_no_setups = True

    # Not idle (recently traded)
    trader.minutes_since_last_trade = 80 # 80 < 60 * 1.5
    assert atlas.is_trader_idle(trader) == False

    print("Idle detection test passed.")

def test_evolution_level():
    atlas = ATLAS()
    assert atlas.get_evolution_level(20) is None
    assert atlas.get_evolution_level(40) == 1
    assert atlas.get_evolution_level(100) == 2
    assert atlas.get_evolution_level(300) == 3
    print("Evolution level mapping test passed.")

if __name__ == "__main__":
    test_idle_detection()
    test_evolution_level()
