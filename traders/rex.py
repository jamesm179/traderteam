from traders.base import BaseTrader

class Rex(BaseTrader):
    def __init__(self):
        super().__init__("REX")
        self.avg_setup_frequency_minutes = 240

    def evolve(self):
        super().evolve()
        if self.evolution_level == 3:
             print(f"{self.name}: Building new pattern variant (bearish version of existing setup).")
