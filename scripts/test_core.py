from atlas.core import ATLAS, Regime

class MockTrader:
    def __init__(self, name):
        self.name = name
        self.capital_limit = 0.0
        self.daily_loss_limit = 0.0
        self.daily_loss = 0.0
        self.is_paused = False

    def pause(self, reason):
        self.is_paused = True
        self.pause_reason = reason

def test_regime_classification():
    atlas = ATLAS()

    # High Vol
    assert atlas.classify_regime({"VIX": 35}) == Regime.HIGH_VOL

    # Trending
    assert atlas.classify_regime({"VIX": 20, "BTC_CHANGE": 0.06}) == Regime.TRENDING
    assert atlas.classify_regime({"VIX": 20, "SPX_CHANGE": -0.03}) == Regime.TRENDING

    # Ranging
    assert atlas.classify_regime({"VIX": 12, "BTC_CHANGE": 0.01}) == Regime.RANGING

    # Choppy
    assert atlas.classify_regime({"VIX": 22, "BTC_CHANGE": 0.01}) == Regime.CHOPPY
    print("Regime classification test passed.")

def test_allocation_and_kill_switch():
    atlas = ATLAS()
    atlas.traders = {name: MockTrader(name) for name in ["GHOST", "NOVA"]}
    atlas.allocations = {"GHOST": 0.6, "NOVA": 0.4}
    atlas.total_capital = 10000
    atlas.max_daily_loss_percent = 5

    atlas.allocate_capital()

    assert atlas.traders["GHOST"].capital_limit == 6000
    assert atlas.traders["GHOST"].daily_loss_limit == 300
    assert atlas.traders["NOVA"].capital_limit == 4000
    assert atlas.traders["NOVA"].daily_loss_limit == 200

    # Test kill switch
    atlas.traders["GHOST"].daily_loss = 350
    atlas.check_kill_switches()
    assert atlas.traders["GHOST"].is_paused == True
    assert atlas.traders["NOVA"].is_paused == False

    print("Allocation and kill switch test passed.")

if __name__ == "__main__":
    test_regime_classification()
    test_allocation_and_kill_switch()
