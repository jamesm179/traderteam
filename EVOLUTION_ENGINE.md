# EVOLUTION ENGINE
## Idle Time → Self-Improvement System

---

## Purpose

The Evolution Engine ensures no trader ever wastes idle time.
When a trader cannot find a valid setup, they automatically shift into
research, backtesting, and strategy improvement mode.

This is ATLAS-orchestrated but fully autonomous — the human never needs
to trigger or monitor it.

---

## The Core Principle

```
IDLE TIME IS NOT DOWNTIME.
IDLE TIME IS EVOLUTION TIME.

A trader who can't trade today becomes a better trader tomorrow.
```

---

## Idle Detection (ATLAS checks this every 30 min)

```python
IDLE_THRESHOLDS = {
    "GHOST":  30,    # Scalper expects frequent setups — 30 min = idle
    "NOVA":   120,   # Momentum trader — a 2h dry spell is normal
    "REX":    180,   # Breakout trader — can wait hours for right setup
    "SAGE":   120,   # Mean reversion — extremes don't always happen
    "VEGA":   180,   # Options — event-driven, long waits are normal
    "CIPHER": 60,    # Algo — always has signals; 1h idle = something's wrong
}

def check_idle(trader):
    minutes_idle = trader.minutes_since_last_setup_or_trade

    if minutes_idle >= IDLE_THRESHOLDS[trader.name]:
        if trader.state != EVOLVING:
            atlas.activate_evolution(trader, minutes_idle)
```

---

## Evolution Level Assignment Logic

```python
def assign_evolution_level(trader, minutes_idle):

    # Priority 1: ATLAS-forced tasks (overrides idle duration)
    if atlas.has_forced_task(trader):
        return atlas.get_forced_task(trader)

    # Priority 2: Pending backtest proposals (run these if idle)
    if trader.has_pending_backtest():
        return Task("L3-A", "FULL_BACKTEST_CYCLE")

    # Priority 3: Recent loss investigation (if lost 2+ today)
    if trader.today_loss_count >= 2:
        return Task("L1-A", "RECENT_LOSS_REVIEW")

    # Priority 4: Duration-based level
    if 30 <= minutes_idle < 90:
        return random_L1_task(trader)

    elif 90 <= minutes_idle < 240:
        return random_L2_task(trader)

    else:
        return random_L3_task(trader)
```

---

## Full Task Library with Output Specs

Each task has a defined output. Traders produce exactly this output and submit to ATLAS.

---

### L1-A: Recent Loss Review

```
INPUT:   Last 5 losing trades from trade log
PROCESS: For each trade, answer:
           1. Was the entry setup valid per current rules?
           2. Was stop placement correct?
           3. Was this a "valid loss" or a "mistake"?
           4. Do any 2+ losses share a common condition?
OUTPUT:  loss_review_[DATE].md with structured answers
SUBMIT:  Write to .learnings/LOSS_REVIEWS.md
         Notify ATLAS: "L1-A complete. [N] valid losses, [M] mistakes found."
TIME:    ~30–45 minutes
```

### L1-B: Support/Resistance Mapping

```
INPUT:   Current watchlist assets (from ATLAS daily brief)
PROCESS: For each asset:
           - Identify last 3 major swing highs/lows on daily chart
           - Identify round numbers ± 0.5% of current price
           - Identify weekly open/close levels
           - Identify high-volume nodes (HVN) from volume profile
OUTPUT:  sr_levels.json updated with structured S/R data
SUBMIT:  Save to runtime/[TRADER]/sr_levels.json
         Notify ATLAS: "S/R mapping updated for [N] assets."
TIME:    ~20–40 minutes
```

### L1-C: Setup Frequency Audit

```
INPUT:   Last 30 days of chart data on watchlist
PROCESS: Count occurrences of each defined setup type
         Count how many were actually entered vs. scanned
         Calculate "missed opportunity rate" per setup
OUTPUT:  setup_audit_[DATE].md
         Columns: setup_type | appeared | entered | missed | miss_reason
SUBMIT:  Write to .learnings/SETUP_AUDITS.md
         If any setup has missed > 40%: flag for filter review
TIME:    ~45–60 minutes
```

### L1-D: Peer Trade Review

```
INPUT:   ATLAS provides one redacted trade from another trader
PROCESS: Analyze the setup:
           - Would my rules have identified this opportunity?
           - What would I need to add to catch this in my style?
           - Is this a one-off or a repeatable edge?
OUTPUT:  peer_review_note in team_learnings.md
SUBMIT:  Write finding to runtime/ATLAS/team_learnings.md
TIME:    ~20–30 minutes
```

---

### L2-A: Hypothesis Generation

```
INPUT:   Last 60 days of own trade data
PROCESS: Identify 3 untested hypotheses of the form:
           "My [SETUP] win rate is higher when [CONDITION] is true"
           Each must be: specific, testable, falsifiable
OUTPUT:  hypothesis_[DATE].json
         Format per hypothesis:
         {
           "hypothesis": "Bull flag win rate is higher when RSI > 55 at entry",
           "setup": "BULL_FLAG",
           "condition": "rsi_daily > 55",
           "expected_improvement": "10%+ win rate",
           "test_period": "last 90 days",
           "min_sample": 15
         }
SUBMIT:  Write to runtime/ATLAS/backtest_queue.json
         ATLAS schedules and runs the backtests
TIME:    ~60–90 minutes
```

### L2-B: Parameter Sensitivity Analysis

```
INPUT:   Current strategy parameters, last 60 days trade data
PROCESS: For each parameter in [param_A, param_B]:
           Test at: -30%, -20%, -10%, current, +10%, +20%, +30%
           Measure: win rate, profit factor, Sharpe at each level
           Find: optimal value and direction of improvement
OUTPUT:  sensitivity_[PARAM]_[DATE].md
         Table: param_value | win_rate | profit_factor | sharpe | trades
         Recommendation: increase / decrease / keep current
SUBMIT:  If Sharpe improves >8%: submit parameter_update_proposal
         If no improvement: log as "parameter is at optimal level"
TIME:    ~60–90 minutes
```

### L2-C: Regime Performance Deep Dive

```
INPUT:   All own historical trades tagged with regime label
PROCESS: For each regime (TRENDING / RANGING / HIGH_VOL / CHOPPY):
           Calculate: win rate, avg R:R, Sharpe, total trades
           Identify: which setup types worked best in each regime
           Find: the single rule that would have most improved worst regime
OUTPUT:  regime_analysis_[DATE].md
         Matrix: regime × metric table + rule change recommendation
SUBMIT:  Write to .learnings/REGIME_ANALYSIS.md
         If regime underperformance < 35% WR: submit regime_rule_proposal
TIME:    ~90–120 minutes
```

### L2-D: Rejected Setup Audit

```
INPUT:   Log of setups that were scanned but NOT entered (last 30 days)
         Note: all traders must maintain a rejected_setups.json log
PROCESS: For each rejected setup:
           Track: what happened next (price moved? how far? direction?)
           Classify: good rejection / missed opportunity
           If missed opportunity: which specific rule blocked it?
OUTPUT:  rejected_audit_[DATE].md
         Stats: total_rejected | good_rejections | missed_opportunities
         If missed > 40%: list the top 3 blocking rules
SUBMIT:  If missed > 40%: submit filter_relaxation_proposal to ATLAS
         Otherwise: log to .learnings/ only
TIME:    ~60–90 minutes
```

---

### L3-A: Full Backtest Cycle

```
INPUT:   Current strategy rules + 6 months of market data
PROCESS:
  Step 1: Define all rules in testable pseudocode
  Step 2: Run on 5-month training period
  Step 3: Record: total trades, WR, avg RR, Sharpe, max DD, profit factor
  Step 4: Run on 1-month OOS period (never seen before)
  Step 5: Compare IS vs OOS performance
  Step 6: If OOS Sharpe < IS Sharpe * 0.75 → run parameter grid search
  Step 7: Grid search: test all parameter combinations
  Step 8: Validate best params on OOS period
  Step 9: Report results

OUTPUT:  backtest_report_[TRADER]_[DATE].md (use SHARED_SYSTEMS backtest template)
SUBMIT:  If OOS improvement > 8%: submit to ATLAS for approval
         If no improvement: log as "current params are stable"
ATLAS GATE: Must pass 5-gate approval check before going live
TIME:    ~3–5 hours
```

### L3-B: New Setup Discovery

```
INPUT:   3–5 years of price/volume data on covered markets
PROCESS:
  Step 1: Define search criteria for "interesting" patterns:
            - 3+ bar formation
            - Volume condition
            - Directional bias
            - Subsequent 5-day price movement
  Step 2: Scan data for all occurrences
  Step 3: Calculate forward returns for each occurrence
  Step 4: Filter: win rate > 55%, sample > 20 occurrences
  Step 5: Define entry, stop, and target rules for the pattern
  Step 6: Forward test on last 30 days (true OOS)

OUTPUT:  new_setup_proposal_[NAME]_[DATE].md
         Must include: pattern definition, entry rules, stop rules,
         backtest stats, OOS validation, why it fits this trader's style
SUBMIT:  new_setup_proposal → ATLAS inbox
         ATLAS gate: same 5-gate approval + fits trader identity check
TIME:    ~4–6 hours
```

### L3-C: Cross-Asset Correlation Research

```
INPUT:   90 days of price data for 4 assets not in current coverage
PROCESS:
  For each pair (current_asset, new_asset):
    Calculate: Pearson correlation on daily returns
    Calculate: lead/lag correlation (does A predict B 1–3 days ahead?)
    Test: if A moves >1% in direction D, what does B do in next 2 days?

OUTPUT:  correlation_research_[DATE].md
         Table: asset_pair | pearson_r | lag_correlation | predictive_signal
         If r > 0.65 or lag_r > 0.50: submit as correlation_signal_proposal
SUBMIT:  correlation_signal_proposal → ATLAS inbox
         Include: how to use signal, example filter rule, backtest stats
TIME:    ~3–4 hours
```

### L3-D: Strategy Stress Test

```
INPUT:   Strategy rules + historical data from 3 worst market periods:
         (ATLAS provides these: e.g., Covid crash, 2022 rate hike crash, etc.)
PROCESS:
  For each stress period:
    Run strategy as-is
    Record: max drawdown, worst day, which specific rule caused most losses
    Identify: the one rule that, if modified, reduces stress-period loss most
    Propose: defensive rule addition or parameter modification

OUTPUT:  stress_test_report_[DATE].md
         Per-period analysis + consolidated defensive rule proposals
SUBMIT:  stress_test_proposals → ATLAS inbox
         Label priority: CRITICAL / HIGH / MEDIUM
TIME:    ~3–4 hours
```

---

## Evolution Task Progress Tracking

All tasks are logged and tracked to prevent repetition:

```json
{
  "trader": "REX",
  "task_id": "L3-A-20260418",
  "task_name": "FULL_BACKTEST_CYCLE",
  "started_at": "2026-04-18T22:30:00Z",
  "status": "IN_PROGRESS",
  "progress_pct": 45,
  "current_step": "Running OOS validation",
  "paused_at": null,
  "resume_context": null,
  "completed_at": null,
  "finding_summary": null,
  "submitted_to_atlas": false
}
```

**Tasks can be paused** (market setup appeared) and **resumed** (market went quiet again).
Progress is saved to disk so no work is lost.

---

## Evolution Productivity Metrics (ATLAS tracks monthly)

```
Per trader:
  - evolution_hours_this_month
  - tasks_completed
  - proposals_submitted
  - proposals_approved
  - proposals_rejected
  - live_improvements_from_evolution (rules changed that stayed live > 30 days)
  - estimated_pnl_improvement_from_evolution

Team:
  - total_rule_changes_this_month
  - avg_sharpe_improvement_from_changes
  - strategies_retired (degraded beyond recovery)
  - new_setups_added
```

---

## Evolution Leaderboard (Friendly Competition Among Traders)

ATLAS maintains a monthly evolution leaderboard. Traders with more
approved proposals receive slightly higher base allocation (up to +3%):

```
EVOLUTION LEADERBOARD — APRIL 2026

Rank  Trader   Tasks  Proposals  Approved  Live Improvements
──────────────────────────────────────────────────────────────
  1   CIPHER      14         6         5     Sharpe +0.4 avg
  2   REX         10         4         3     WR +9% on bull flag
  3   NOVA         8         3         2     Profit factor +0.3
  4   GHOST       12         5         2     False entry -18%
  5   SAGE         7         2         2     Exit efficiency +12%
  6   VEGA         6         2         1     IV threshold refined
──────────────────────────────────────────────────────────────
Allocation bonus: CIPHER +2%, REX +1%
```

---

*"The market is always changing. The trader who evolves fastest wins."*
*— Evolution Engine v1.0, Olympus Trading Collective*
