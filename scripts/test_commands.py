from atlas.core import ATLAS
from atlas.commands import CommandHandler

class MockTrader:
    def __init__(self, name):
        self.name = name
        self.is_paused = False
    def pause(self, reason):
        self.is_paused = True
    def resume(self):
        self.is_paused = False

def test_commands():
    atlas = ATLAS()
    atlas.traders = {"GHOST": MockTrader("GHOST"), "NOVA": MockTrader("NOVA")}
    handler = CommandHandler(atlas)

    # Test Capital Commands
    print(handler.handle("Set total capital to $50,000"))
    assert atlas.total_capital == 50000.0

    print(handler.handle("Set max daily loss to 4%"))
    assert atlas.max_daily_loss_percent == 4.0

    # Test Control Commands
    print(handler.handle("PAUSE all trading"))
    assert atlas.is_paused == True
    assert atlas.traders["GHOST"].is_paused == True

    print(handler.handle("RESUME trading"))
    assert atlas.is_paused == False
    assert atlas.traders["GHOST"].is_paused == False

    # Test Market Commands
    print(handler.handle("Add ADA to the watchlist"))
    assert "ADA" in atlas.watchlist

    print("Command interface test passed.")

if __name__ == "__main__":
    test_commands()
