import enum
from typing import Dict, List, Optional
import config

class Regime(enum.Enum):
    TRENDING = "TRENDING"
    RANGING = "RANGING"
    HIGH_VOL = "HIGH_VOL"
    CHOPPY = "CHOPPY"

class ATLAS:
    def __init__(self):
        self.total_capital = config.INITIAL_TOTAL_CAPITAL
        self.max_daily_loss_percent = config.MAX_DAILY_LOSS_PERCENT
        self.current_regime = Regime.RANGING
        self.allocations = config.INITIAL_ALLOCATIONS.copy()
        self.traders = {} # To be populated with trader instances
        self.is_paused = False
        self.watchlist = ["BTC", "ETH", "SOL"] # Default watchlist

    def classify_regime(self, market_data: Dict[str, float]) -> Regime:
        """
        Classifies the market regime based on indicators like VIX, DXY, SPX, BTC.
        This is a simplified implementation for now.
        """
        vix = market_data.get("VIX", 20.0)
        btc_change = market_data.get("BTC_CHANGE", 0.0)
        spx_change = market_data.get("SPX_CHANGE", 0.0)

        if vix > 30:
            self.current_regime = Regime.HIGH_VOL
        elif abs(btc_change) > 0.05 or abs(spx_change) > 0.02:
            self.current_regime = Regime.TRENDING
        elif vix < 15:
            self.current_regime = Regime.RANGING
        else:
            self.current_regime = Regime.CHOPPY

        return self.current_regime

    def set_total_capital(self, amount: float):
        self.total_capital = amount

    def set_max_daily_loss(self, percent: float):
        self.max_daily_loss_percent = percent

    def allocate_capital(self):
        """
        Distributes total capital to traders based on their allocation weights.
        """
        for name, trader in self.traders.items():
            weight = self.allocations.get(name, 0.0)
            trader.capital_limit = self.total_capital * weight
            trader.daily_loss_limit = trader.capital_limit * (self.max_daily_loss_percent / 100.0)

    def check_kill_switches(self):
        """
        Enforces per-trader kill switches if daily loss limits are exceeded.
        """
        for name, trader in self.traders.items():
            if trader.daily_loss >= trader.daily_loss_limit:
                trader.pause(reason="Daily loss limit hit")
                print(f"KILL SWITCH: {name} suspended due to daily loss limit.")

    def rebalance_allocations(self, new_weights: Dict[str, float]):
        """
        Updates allocation weights.
        """
        total_weight = sum(new_weights.values())
        if abs(total_weight - 1.0) > 0.001:
            # Normalize if it doesn't sum to 1
            for name in new_weights:
                new_weights[name] /= total_weight

        self.allocations.update(new_weights)
        self.allocate_capital()

    def is_trader_idle(self, trader) -> bool:
        """
        ATLAS checks every 30 minutes during session.
        """
        return all([
            trader.open_trades == 0,
            trader.pending_signals == 0,
            trader.scan_returned_no_setups == True,
            trader.minutes_since_last_trade > (trader.avg_setup_frequency_minutes * 1.5),
        ])

    def get_evolution_level(self, idle_duration_minutes: int) -> Optional[int]:
        """
        Maps idle duration to evolution level.
        """
        if idle_duration_minutes < 30:
            return None # STANDBY
        elif idle_duration_minutes < 90:
            return 1
        elif idle_duration_minutes < 240:
            return 2
        else:
            return 3

    def approve_proposal(self, proposal) -> Dict:
        """
        Every proposal from every trader must pass this before going live.
        """
        # Gate 1: Sample size
        if proposal.sample_size < 20:
            return {"decision": "REJECT", "reason": f"Need 20+ trades. Currently: {proposal.sample_size}"}

        # Gate 2: OOS Sharpe floor
        if proposal.oos_sharpe < 1.5:
            return {"decision": "REJECT", "reason": f"OOS Sharpe {proposal.oos_sharpe} below floor of 1.5"}

        # Gate 3: Overfitting check
        degradation = (proposal.is_sharpe - proposal.oos_sharpe) / proposal.is_sharpe
        if degradation > 0.25:
            return {"decision": "REJECT", "reason": f"OOS drops {degradation:.0%} from IS. Likely overfit."}

        # Gate 4: Minimum improvement
        current_sharpe = self.get_current_sharpe(proposal.trader_name)
        if proposal.oos_sharpe < current_sharpe * 1.08:
            improvement = (proposal.oos_sharpe / current_sharpe) - 1
            return {"decision": "REJECT", "reason": f"Improvement only {improvement:.0%}. Below 8% threshold."}

        # Gate 5: Rule conflict check
        if self.conflicts_with_team_rules(proposal):
            return {"decision": "FLAG_FOR_HUMAN", "reason": "Conflicts with core team rule. Needs your input."}

        # Gate 6: Deploy safely at half size
        # This would involve actual deployment logic in a real system
        return {"decision": "APPROVE", "reason": "Deploying at 50% size. Full size after 10-trade validation."}

    def get_current_sharpe(self, trader_name: str) -> float:
        # Mocking current Sharpe for now
        return 1.8

    def conflicts_with_team_rules(self, proposal) -> bool:
        # Mocking conflict check
        return False

    def run_overnight_cycle(self):
        """
        Orchestrates the overnight evolution protocol (22:30-06:00 UTC).
        """
        print("22:30 - Post-session review complete. Starting overnight evolution.")

        # 1. Assign Level 3 tasks to all traders
        for name, trader in self.traders.items():
            print(f"Assigning LEVEL 3 evolution task to {name}")
            trader.evolution_level = 3
            trader.evolve()

        print("23:00 - Traders working independently in parallel.")

        print("02:00 - ATLAS midpoint review.")
        # Midpoint review logic would go here

        print("04:00 - Evolution tasks complete. Submissions received.")

        print("04:30 - ATLAS reviewing submissions via Approval Gate.")
        # Review submissions and apply Gate logic

        print("05:00 - Approved changes written to each trader's MEMORY.md.")

        print("05:45 - Day cycle starts fresh with improved rules.")
