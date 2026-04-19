import json
import datetime
import os

# 5. Regime Classification (ATLAS Standard)
REGIMES = {
    "TRENDING_BULL": {
        "description": "SPX/BTC in clear uptrend, VIX < 18, HH/HL structure",
        "best_traders": ["NOVA", "REX", "CIPHER"],
        "avoid_traders": ["SAGE"],
    },
    "TRENDING_BEAR": {
        "description": "SPX/BTC in clear downtrend, VIX > 22, LH/LL structure",
        "best_traders": ["REX (short setups)", "CIPHER", "VEGA (puts)"],
        "avoid_traders": ["NOVA"],
    },
    "RANGING": {
        "description": "Price oscillating in defined range, ADX < 25",
        "best_traders": ["GHOST", "SAGE", "VEGA (IC)"],
        "avoid_traders": ["NOVA", "REX"],
    },
    "HIGH_VOLATILITY": {
        "description": "VIX > 28, large daily candles, event-driven",
        "best_traders": ["VEGA", "CIPHER (hedged)"],
        "avoid_traders": ["GHOST (spreads too wide)", "NOVA"],
    },
    "CHOPPY": {
        "description": "No clear direction, failed breakouts everywhere, low conviction",
        "best_traders": ["CIPHER (stat arb only)", "VEGA (theta decay)"],
        "avoid_traders": ["All directional traders — reduce to 50% size"],
    }
}

# 6. Risk Module (Shared Across All Traders)
class RiskModule:
    """All traders instantiate this class. It enforces universal rules."""

    def __init__(self, trader_name, daily_capital):
        self.trader = trader_name
        self.daily_capital = daily_capital
        self.daily_pnl = 0
        self.trades_today = []
        self.consecutive_losses = 0

    def get_atlas_regime(self):
        """Placeholder for regime detection logic or ATLAS feed."""
        return "TRENDING_BULL" # Default for now

    def can_trade(self) -> tuple[bool, str]:
        """Returns (allowed, reason) — must pass before any entry."""

        if self.daily_pnl <= -self.daily_capital * 0.02:
            return False, "Daily loss limit reached (-2%). Suspended."

        if self.consecutive_losses >= 4:
            return False, "4 consecutive losses. Mandatory pause. Review required."

        if self.get_atlas_regime() == "CHOPPY" and len(self.trades_today) >= 3:
            return False, "Choppy regime: max 3 trades. Limit reached."

        return True, "OK"

    def calculate_position_size(self, entry, stop_loss, risk_pct=0.015):
        risk_amount = self.daily_capital * risk_pct
        distance = abs(entry - stop_loss) / entry
        if distance == 0:
            return 0
        size = risk_amount / distance
        return min(size, self.daily_capital * 0.25)  # Never more than 25% in one trade

    def log_trade_result(self, pnl):
        self.daily_pnl += pnl
        if pnl < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0
        self.trades_today.append(pnl)

# 7. ATLAS Communication Protocol
SIGNAL_TYPES = {
    "SIGNAL_CARD":        "New setup identified — requesting approval",
    "TRADE_EXECUTED":     "Trade entered — informing ATLAS",
    "TRADE_CLOSED":       "Trade closed — with P&L",
    "KILL_SWITCH":        "Self-suspending due to loss limit — informing ATLAS",
    "LEARNING_PROPOSAL":  "Proposing rule change — requesting ATLAS review",
    "BACKTEST_RESULT":    "Backtest complete — requesting param update approval",
    "REGIME_ALERT":       "Market condition changed — flagging for ATLAS",
    "HEDGE_REQUEST":      "Requesting VEGA to place hedge (from any trader)",
}

TRADER_ID = "GENERIC_TRADER" # Default, should be overridden by specific traders

def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def append_to_json(filepath, data):
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump([], f)

    with open(filepath, 'r+') as f:
        try:
            current_data = json.load(f)
        except json.JSONDecodeError:
            current_data = []
        current_data.append(data)
        f.seek(0)
        json.dump(current_data, f, indent=2)
        f.truncate()

def send_to_atlas(message_type, payload, trader_id=None):
    effective_trader_id = trader_id or TRADER_ID
    message = {
        "type": message_type,
        "from": effective_trader_id,
        "timestamp": now_iso(),
        "payload": payload
    }
    append_to_json("runtime/ATLAS/inbox.json", message)
