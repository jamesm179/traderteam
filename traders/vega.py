from traders.base import BaseTrader

class Vega(BaseTrader):
    def __init__(self):
        super().__init__("VEGA")
        self.avg_setup_frequency_minutes = 480 # Options trader, low frequency setups

    def evolve(self):
        super().evolve()
        if self.evolution_level == 3:
             print(f"{self.name}: Backtesting new options strategies.")
