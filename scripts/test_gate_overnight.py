from atlas.core import ATLAS

class MockProposal:
    def __init__(self, sample_size, oos_sharpe, is_sharpe, trader_name="GHOST"):
        self.sample_size = sample_size
        self.oos_sharpe = oos_sharpe
        self.is_sharpe = is_sharpe
        self.trader_name = trader_name

class MockTrader:
    def __init__(self, name):
        self.name = name
        self.evolution_level = 0
    def evolve(self):
        print(f"{self.name} is evolving at level {self.evolution_level}")

def test_approval_gate():
    atlas = ATLAS()

    # Fail Sample size
    p1 = MockProposal(15, 2.0, 2.2)
    assert atlas.approve_proposal(p1)["decision"] == "REJECT"

    # Fail OOS Sharpe
    p2 = MockProposal(25, 1.4, 1.6)
    assert atlas.approve_proposal(p2)["decision"] == "REJECT"

    # Fail Overfitting (degradation > 25%)
    p3 = MockProposal(25, 1.6, 2.5) # (2.5-1.6)/2.5 = 0.36
    assert atlas.approve_proposal(p3)["decision"] == "REJECT"

    # Fail Minimum improvement (current = 1.8, need 1.8 * 1.08 = 1.944)
    p4 = MockProposal(25, 1.9, 2.0)
    assert atlas.approve_proposal(p4)["decision"] == "REJECT"

    # Pass
    p5 = MockProposal(25, 2.0, 2.2)
    assert atlas.approve_proposal(p5)["decision"] == "APPROVE"

    print("Approval gate test passed.")

def test_overnight_cycle():
    atlas = ATLAS()
    atlas.traders = {"GHOST": MockTrader("GHOST"), "NOVA": MockTrader("NOVA")}
    atlas.run_overnight_cycle()
    assert atlas.traders["GHOST"].evolution_level == 3
    assert atlas.traders["NOVA"].evolution_level == 3
    print("Overnight cycle test passed.")

if __name__ == "__main__":
    test_approval_gate()
    test_overnight_cycle()
