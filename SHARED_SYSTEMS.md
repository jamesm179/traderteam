# SHARED SYSTEMS
## Infrastructure Used by All Olympus Traders

---

## Overview

All 6 traders + ATLAS share these common systems. This file defines the universal protocols every trader must implement identically. Individual trader files extend these with strategy-specific logic.

---

## 1. Universal Trade Log Schema

Every trader logs **every trade** in JSON format. All fields are required.

```json
{
  "trade_id": "GHOST-20260418-001",
  "trader": "GHOST",
  "timestamp_entry": "2026-04-18T09:32:00Z",
  "timestamp_exit": "2026-04-18T09:45:00Z",
  "asset": "BTC/USDT",
  "market_type": "crypto",
  "direction": "long",
  "entry_price": 84250.00,
  "exit_price": 84610.00,
  "position_size_usd": 5000,
  "stop_loss": 84080.00,
  "take_profit_1": 84500.00,
  "take_profit_2": 84900.00,
  "pnl_usd": 180.00,
  "pnl_pct": 0.43,
  "r_multiple": 2.1,
  "exit_reason": "tp2",
  "hold_time_minutes": 13,

  "context": {
    "atlas_regime": "RANGING",
    "atlas_allocation_pct": 0.25,
    "vix_at_entry": 18.4,
    "btc_dominance": 58.2,
    "broad_market_trend": "neutral",
    "near_macro_event": false,
    "macro_event_name": null
  },

  "setup": {
    "setup_type": "micro_structure_long",
    "timeframe_bias": "15m_bullish",
    "timeframe_entry": "1m",
    "signal_quality_score": 8,
    "checklist_passed": true,
    "checklist_items_failed": []
  },

  "outcome": {
    "result": "win",
    "mistake_type": null,
    "classification": "GOOD",
    "exit_efficiency": 0.72,
    "max_adverse_excursion_pct": -0.08,
    "max_favorable_excursion_pct": 0.60,
    "notes": "Clean trade. Could have held for TP2 earlier."
  }
}
```

---

## 2. Universal Signal Card (Submitted to ATLAS)

When any trader identifies a setup, they submit this card to ATLAS for aggregation:

```json
{
  "trader": "NOVA",
  "timestamp": "2026-04-18T07:15:00Z",
  "asset": "NVDA",
  "direction": "long",
  "conviction_score": 8,
  "setup_type": "pullback_to_ema_20",
  "entry_zone": [118.50, 119.00],
  "stop_loss": 116.20,
  "tp1": 122.50,
  "tp2": 126.00,
  "tp3": 131.00,
  "timeframe_structure": "4H_bullish",
  "invalidation": "daily_close_below_ema50",
  "notes": "Strong relative strength vs QQQ. Volume declining on pullback. Clean setup.",
  "status": "PENDING_ATLAS_APPROVAL"
}
```

---

## 3. Universal Learning Entry Format

All traders use this identical format for learning logs:

```markdown
## [LRN-TRADERNAME-YYYYMMDD-XXX] category

**Trader**: GHOST | NOVA | REX | SAGE | VEGA | CIPHER
**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | implemented | rejected | testing
**Area**: entry | exit | position_sizing | regime_filter | risk | setup_type

### Summary
One-line description of the lesson

### What Happened
Specific trade(s) that generated this lesson. Include trade IDs.

### What Was Wrong / What Was Correct
Contrast old belief with new understanding

### Rule Change Proposed
Specific, testable change to strategy rules

### Backtest Required?
[ ] Yes — run backtest on last 90 days with new rule
[ ] No — directional improvement is obvious

### Status After Review
ATLAS approved/rejected on [DATE]: [RATIONALE]

---
```

---

## 4. Universal Backtest Template

```markdown
## Backtest Report — [TRADER] — [DATE]

**Strategy**: [Strategy name/version]
**Asset(s)**: [List]
**Test Period**: [START] to [END] (N months)
**Validation Method**: [ ] In-sample only  [ ] Walk-forward  [ ] OOS split

---

### Parameters Tested

| Parameter | Old Value | New Value | Range Tested |
|-----------|-----------|-----------|--------------|
| | | | |

### Results Comparison

| Metric | Old Params | New Params | Change |
|--------|-----------|-----------|--------|
| Total Trades | | | |
| Win Rate | | | |
| Avg Win % | | | |
| Avg Loss % | | | |
| Profit Factor | | | |
| Sharpe Ratio | | | |
| Max Drawdown | | | |
| Avg Hold Time | | | |

### Out-of-Sample Validation (Required for Promotion)

- OOS Period: [DATE] to [DATE]
- OOS Sharpe: [VALUE]
- OOS Win Rate: [VALUE]
- Pass/Fail: [ ] Pass (OOS Sharpe > 1.5 and within 20% of IS) [ ] Fail

### Key Finding
[One paragraph: What changed, why it improved/degraded, what we learned]

### Decision
[ ] PROMOTE — New params go live at 50% size for 2-week trial
[ ] MORE TESTING — Need larger sample size
[ ] REJECT — OOS doesn't hold. Log to ERRORS.md
[ ] ARCHIVE — Strategy retired

### ATLAS Sign-Off
[ ] Approved by ATLAS on [DATE]
[ ] Override: [Rationale if rejected despite strong results]
```

---

## 5. Regime Classification (ATLAS Standard)

All traders reference the same regime labels when logging trades:

```python
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
```

---

## 6. Risk Module (Shared Across All Traders)

```python
class RiskModule:
    """All traders instantiate this class. It enforces universal rules."""

    def __init__(self, trader_name, daily_capital):
        self.trader = trader_name
        self.daily_capital = daily_capital
        self.daily_pnl = 0
        self.trades_today = []
        self.consecutive_losses = 0

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
```

---

## 7. ATLAS Communication Protocol

```python
# All traders use these standard message types when communicating with ATLAS

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

def send_to_atlas(message_type, payload):
    message = {
        "type": message_type,
        "from": TRADER_ID,
        "timestamp": now_iso(),
        "payload": payload
    }
    append_to_json("runtime/ATLAS/inbox.json", message)
```

---

## 8. Session Start / End Ritual (All Traders)

```markdown
### SESSION START (run every morning before trading)

1. Read SESSION-STATE.md — restore active context
2. Read MEMORY.md — load durable rules and preferences
3. Read .learnings/ERRORS.md — check for unresolved issues
4. Read ATLAS daily brief — get today's regime + allocation
5. Run morning scan (trader-specific)
6. Submit top setups to ATLAS via SIGNAL_CARDs

---

### SESSION END (run every evening after close)

1. Flush all trade logs to data/[trader]_trades.json
2. Classify each trade outcome (win/loss + mistake type)
3. Note any new patterns or lessons to .learnings/LEARNINGS.md
4. Update SESSION-STATE.md with final state
5. Send session summary to ATLAS (daily P&L, trade count, observations)
```

---

*Shared infrastructure version 1.0.0 — Olympus Trading Collective*
