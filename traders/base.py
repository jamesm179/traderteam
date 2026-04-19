from typing import List, Dict, Optional
import os

class BaseTrader:
    def __init__(self, name: str):
        self.name = name
        self.capital_limit = 0.0
        self.daily_loss_limit = 0.0
        self.daily_loss = 0.0
        self.open_trades = 0
        self.pending_signals = 0
        self.scan_returned_no_setups = True
        self.minutes_since_last_trade = 0
        self.avg_setup_frequency_minutes = 60
        self.is_paused = False
        self.pause_reason = ""
        self.evolution_level = 0
        self.trades_today = 0
        self.win_rate = 0.0
        self.sharpe = 0.0

    def pause(self, reason: str):
        self.is_paused = True
        self.pause_reason = reason

    def resume(self):
        self.is_paused = False
        self.pause_reason = ""

    def scan(self):
        """
        Scan markets for setups.
        """
        print(f"{self.name} scanning markets...")
        # Implementation depends on specific trader

    def execute_trade(self, setup):
        """
        Execute a trade based on a setup.
        """
        if not self.is_paused:
            print(f"{self.name} executing trade: {setup}")
            self.open_trades += 1
            self.trades_today += 1
            self.minutes_since_last_trade = 0

    def evolve(self):
        """
        Perform evolution task based on evolution_level.
        """
        print(f"{self.name} evolving at LEVEL {self.evolution_level}")
        # Implementation depends on specific trader and level

    def log_learning(self, level: int, task: str, finding: str):
        path = f".learnings/{self.name}_LEARNINGS.md"
        os.makedirs(".learnings", exist_ok=True)
        with open(path, "a") as f:
            f.write(f"Level {level} - {task}: {finding}\n")
