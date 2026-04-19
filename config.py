# Global settings and initial allocations

INITIAL_TOTAL_CAPITAL = 50000.0
MAX_DAILY_LOSS_PERCENT = 4.0

TRADERS = ["GHOST", "NOVA", "REX", "SAGE", "VEGA", "CIPHER"]

# Initial capital allocation weights (summing to 1.0)
INITIAL_ALLOCATIONS = {
    "GHOST": 0.25,
    "NOVA": 0.20,
    "REX": 0.15,
    "SAGE": 0.15,
    "VEGA": 0.10,
    "CIPHER": 0.15
}

# Regime classification configuration
REGIME_INDICATORS = ["VIX", "DXY", "SPX", "BTC"]

# Time settings (UTC)
WAKE_UP_TIME = "05:45"
CLASSIFY_REGIME_TIME = "06:00"
BROADCAST_BRIEF_TIME = "06:15"
MORNING_SCAN_TIME = "06:30"
AGGREGATE_SIGNALS_TIME = "07:00"
SESSION_START_TIME = "07:30"
POST_SESSION_REVIEW_TIME = "22:00"
OVERNIGHT_IDLE_TIME = "22:30"
