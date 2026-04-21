# ⚙️ OLYMPUS OPERATIONAL GUIDE
## Running the Multi-Agent Trading System

This guide explains how the Olympus Trading Collective operates on a daily basis and which components require updates to ensure peak performance.

---

## 1. The Daily Execution Cycle (UTC)

The system follows a strict heartbeat. All agents refer to the current UTC time to synchronize their states.

### 06:00 — The Macro Handshake
- **ATLAS Update:** Open `runtime/ATLAS/regime_log.json` and add the current market regime (TRENDING_BULL, RANGING, etc.).
- **ATLAS Update:** Update `runtime/ATLAS/capital_allocation.json` based on the Dynamic Allocation Table in `TEAM_LEADER.md`.
- **Trader Action:** Traders read their `MEMORY.md` and the ATLAS daily brief to set their "Bias for the Day" in their `SESSION-STATE.md`.

### 06:30 — The Morning Scan
- **Trader Action:** Each trader (NOVA, REX, etc.) runs their scanning logic.
- **Data Update:** Traders append potential setups to `runtime/ATLAS/inbox.json` using the **Universal Signal Card** schema.

### 07:00 — Command & Control
- **ATLAS Action:** Reviews `inbox.json`. Approved signals are moved to `runtime/ATLAS/consensus_signals.json`.
- **Trader Action:** Only trades listed in `consensus_signals.json` are permitted for execution.

### 07:30 - 22:00 — Live Session
- **Execution:** Traders log entries and exits in real-time.
- **Trade Logging:** Append every closed trade to `runtime/[TRADER]/data/[trader]_trades.json` using the **Universal Trade Log Schema** in `SHARED_SYSTEMS.md`.
- **Risk Check:** Every 30 mins, ATLAS checks `runtime/ATLAS/inbox.json` for `KILL_SWITCH` alerts if a trader hits their -2% daily limit.

### 22:00 — Session Wrap-up
- **P&L Update:** Update `team_portfolio_pnl.json` with the consolidated results.
- **Trader Action:** Move active session notes from `SESSION-STATE.md` to `MEMORY.md` if they contain durable lessons.
- **Evolution Check:** Any trader who didn't trade today triggers the **Evolution Engine**.

---

## 2. What Needs to be Updated?

To keep the "brain" of the collective accurate, the following files must be updated regularly:

### A. Real-Time Data (Every Trade)
- `runtime/[TRADER]/data/[trader]_trades.json`: The source of truth for all performance metrics.
- `runtime/[TRADER]/data/rejected_setups.json`: Log every setup you *almost* took but didn't. This feeds the L2-D Evolution tasks.

### B. Daily State
- `runtime/[TRADER]/SESSION-STATE.md`: Current mood, active watchlist, and open positions.
- `runtime/ATLAS/regime_log.json`: Must be updated before the session starts.

### C. Strategic "DNA" (Weekly/Monthly)
- `runtime/[TRADER]/MEMORY.md`: Update this when a rule is proven or disproven.
- `runtime/REX/.learnings/HARD_RULES.md`: Add new "Never Again" rules here after a major mistake.
- `runtime/CIPHER/strategies/`: Update these JSON files when parameters are re-optimized via walk-forward testing.

---

## 3. Interaction with ATLAS (The Human Gate)

As the human operator, you interact primarily with **ATLAS**.

1. **Review Proposals:** Check `runtime/ATLAS/inbox.json` for `LEARNING_PROPOSAL` or `BACKTEST_RESULT`.
2. **Approval:** To approve a change, update the "Status After Review" section in the trader's `.learnings/LEARNINGS.md`.
3. **Override:** If a trader is performing poorly but hasn't hit a kill switch, you can manually suspend them by updating their `SESSION-STATE.md` to `state: SUSPENDED`.

---

## 4. Troubleshooting the Agents

| Issue | Check This File |
|-------|-----------------|
| Trader taking bad setups | `runtime/[TRADER]/.learnings/LOSS_REVIEWS.md` |
| Low trade frequency | `runtime/[TRADER]/.learnings/SETUP_AUDITS.md` |
| High fakeout rate | `runtime/REX/sr_levels.json` (Verify S/R accuracy) |
| Systemic losses in volatility | `runtime/VEGA/vol_dashboard.json` (Check Skew/VIX) |

---

## 5. The Evolution Protocol (Triggering Growth)

If a trader is idle (e.g., GHOST > 30m), check `EVOLUTION_ENGINE.md` for the assigned task level.
1. Select a task (e.g., L1-A: Recent Loss Review).
2. Execute the process described in the task library.
3. Save the result to the specified file (e.g., `.learnings/LOSS_REVIEWS.md`).
4. Log the completion in `runtime/ATLAS/evolution_status.json`.

---

*“The system is the edge. Follow the protocol, and the data will do the rest.”*
