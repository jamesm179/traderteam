from traders.base import BaseTrader

class Nova(BaseTrader):
    def __init__(self):
        super().__init__("NOVA")
        self.avg_setup_frequency_minutes = 120

    def evolve(self):
        super().evolve()
        if self.evolution_level == 3:
             print(f"{self.name}: Researching new relative strength ranking formulas.")
