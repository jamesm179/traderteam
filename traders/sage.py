from traders.base import BaseTrader

class Sage(BaseTrader):
    def __init__(self):
        super().__init__("SAGE")
        self.avg_setup_frequency_minutes = 180

    def evolve(self):
        super().evolve()
        if self.evolution_level == 3:
             print(f"{self.name}: Researching new divergence types.")
