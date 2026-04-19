# 🏛️ OLYMPUS TRADING TEAM
## Master Project Documentation

---

```
    ╔═══════════════════════════════════════════════════════╗
    ║              OLYMPUS TRADING COLLECTIVE               ║
    ║         "Elite by design. Adaptive by nature."        ║
    ╚═══════════════════════════════════════════════════════╝

                         ┌─────────┐
                         │  ATLAS  │  Chief Trading Officer
                         │ (Leader)│  Macro Regime + Orchestration
                         └────┬────┘
              ┌───────────────┼───────────────┐
              │               │               │
       ┌──────┴──┐     ┌──────┴──┐     ┌──────┴──┐
       │  GHOST  │     │  NOVA   │     │   REX   │
       │ Scalper │     │Momentum │     │Breakout │
       └─────────┘     └─────────┘     └─────────┘
              │               │               │
       ┌──────┴──┐     ┌──────┴──┐     ┌──────┴──┐
       │  SAGE   │     │  VEGA   │     │ CIPHER  │
       │Mean Rev.│     │ Options │     │  Quant  │
       └─────────┘     └─────────┘     └─────────┘
```

---

## Team Roster

| # | Codename | Role | Style | Timeframe | Markets |
|---|----------|------|-------|-----------|---------|
| L | **ATLAS** | Chief Trading Officer | Macro + Orchestration | Weekly/Daily | All |
| 1 | **GHOST** | Scalper | Pure price action + order flow | 1m–15m | Crypto, Futures |
| 2 | **NOVA** | Momentum Trader | Trend riding + relative strength | 4H–3D | Equities, Crypto |
| 3 | **REX** | Breakout Specialist | Pattern completion + S/R flips | Daily–10D | Equities, Crypto |
| 4 | **SAGE** | Mean Reversion | Overextension fades, stat extremes | 4H–4D | Equities, Crypto |
| 5 | **VEGA** | Options & Vol | IV plays, premium collection, hedging | Event-driven | Options, Index |
| 6 | **CIPHER** | Algorithmic/Quant | Multi-factor models, pairs, algo exec | 15m–5D | All |

---

## Project File Structure

```
trading-team/
│
├── README.md                          ← This file (master overview)
├── TEAM_LEADER.md                     ← ATLAS — CTO profile & systems
│
├── GHOST_scalper.md                   ← Ghost — Scalper profile
├── NOVA_momentum.md                   ← Nova — Momentum profile
├── REX_breakout.md                    ← Rex — Breakout profile
├── SAGE_mean_reversion.md             ← Sage — Mean Reversion profile
├── VEGA_options_vol.md                ← Vega — Options/Vol profile
├── CIPHER_algo_quant.md               ← Cipher — Algo/Quant profile
│
├── SHARED_SYSTEMS.md                  ← Shared infrastructure all traders use
│
│── runtime/                           ← Live session data
│   ├── ATLAS/
│   │   ├── SESSION-STATE.md
│   │   ├── MEMORY.md
│   │   ├── regime_log.json
│   │   ├── capital_allocation.json
│   │   └── consensus_signals.json
│   │
│   ├── GHOST/
│   │   ├── SESSION-STATE.md
│   │   ├── MEMORY.md
│   │   └── data/ghost_trades.json
│   │
│   ├── NOVA/
│   │   ├── SESSION-STATE.md
│   │   ├── MEMORY.md
│   │   └── data/nova_trades.json
│   │
│   ├── REX/
│   │   ├── SESSION-STATE.md
│   │   ├── MEMORY.md
│   │   └── data/rex_trades.json
│   │
│   ├── SAGE/
│   │   ├── SESSION-STATE.md
│   │   ├── MEMORY.md
│   │   └── data/sage_trades.json
│   │
│   ├── VEGA/
│   │   ├── SESSION-STATE.md
│   │   ├── MEMORY.md
│   │   └── data/vega_trades.json
│   │
│   └── CIPHER/
│       ├── SESSION-STATE.md
│       ├── MEMORY.md
│       ├── strategies/
│       └── data/cipher_trades.json
│
└── team_portfolio_pnl.json            ← Master P&L across all traders
```

---

## How the Team Works Together

### 1. Daily Workflow

```
06:00 UTC — ATLAS wakes up
  → Classifies today's market regime
  → Sets capital allocation per trader
  → Broadcasts DAILY_BRIEF to all traders

06:30 UTC — Traders run their morning scans
  → Each trader identifies their best setups
  → Submits SIGNAL_CARDS to ATLAS

07:00 UTC — ATLAS aggregates signals
  → Runs consensus scoring model
  → Approves high-conviction trades
  → Sets risk limits for the day

07:30 UTC — Market open / Session begins
  → GHOST starts scalping (if regime allows)
  → NOVA/REX/SAGE/VEGA/CIPHER execute their setups

Throughout session:
  → Each trader logs every trade in real-time
  → ATLAS monitors total portfolio exposure
  → ATLAS pauses traders who breach daily loss limits

22:00 UTC — Session ends
  → All traders submit session logs
  → ATLAS runs post-session review
  → Learning files updated across all agents
  → Next-day regime forecast generated
```

### 2. Self-Learning Cascade

```
TRADE OCCURS
    │
    ▼
TRADER logs trade with full context
    │
    ▼
TRADER runs weekly pattern analysis
    │
    ├── Win pattern found → reinforce rule
    ├── Loss pattern found → propose rule change
    └── No pattern → continue accumulating data
    │
    ▼
ATLAS aggregates all trader learnings
    │
    ▼
ATLAS runs monthly regime performance analysis
    │
    └── Which traders perform in which regimes → update capital allocation
```

### 3. Strategy Self-Improvement Pipeline

```
STEP 1: Trade logging (real-time)
         Every trade logged with 15+ context variables

STEP 2: Pattern detection (weekly)
         Automated analysis of loss patterns
         Identify which conditions correlate with wins/losses

STEP 3: Parameter optimization (monthly)
         Grid search over parameter space
         Backtest on historical data

STEP 4: Walk-forward validation (CIPHER standard, applied to all)
         6-month train, 1-month OOS validation
         Accept only if OOS performance holds

STEP 5: ATLAS review & approval
         No parameter change goes live without ATLAS reviewing it
         Human-in-the-loop checkpoint

STEP 6: Gradual deployment
         New params at 50% size for first 2 weeks
         Full size only after validation in live conditions

STEP 7: Continuous monitoring
         If new params underperform → automatic revert
```

---

## Capital Allocation Philosophy

### Base Allocation (Normal Conditions)
```
Total Team Capital: 100%

ATLAS: No direct trading capital (overhead role)
GHOST:  15% (high frequency, lower per-trade size)
NOVA:   20% (trend riding, medium-term holds)
REX:    20% (breakout plays, higher conviction)
SAGE:   15% (counter-trend, needs room for adverse excursion)
VEGA:   15% (options premium, hedging function)
CIPHER: 15% (diversified across 4 strategies)
```

### Allocation Shifts by Regime (ATLAS controls this)
```
See ATLAS profile for dynamic allocation table per regime.
Key principle: Allocate more to traders whose style MATCHES the current regime.
```

---

## Risk Architecture

```
TIER 1 — Individual Trade Risk (Each Trader)
  → Max 1.5–2% account risk per trade
  → Each trader manages their own stop losses

TIER 2 — Daily Trader Risk (ATLAS-monitored)
  → Max 2% account loss per trader per day
  → Breach → trader suspended for the session

TIER 3 — Portfolio Risk (ATLAS)
  → Max 6% total portfolio loss per day
  → Max 40% correlated directional exposure
  → If hit → all traders go to 50% size or flat

TIER 4 — Regime Risk (ATLAS)
  → In "CHOPPY/AVOID" regimes → everyone at 50% max size
  → In "HIGH VOL EVENT" → only VEGA and CIPHER trade
```

---

## Performance Monitoring Dashboard

| Metric | Target | Alert Level | Owner |
|--------|--------|-------------|-------|
| Team Daily P&L | > 0% | < -4% | ATLAS |
| Team Sharpe (rolling 4w) | > 1.5 | < 1.0 | ATLAS |
| GHOST Win Rate | > 58% | < 50% | GHOST |
| NOVA Profit Factor | > 2.0 | < 1.5 | NOVA |
| REX Avg R:R | > 3.0 | < 2.0 | REX |
| SAGE Time-to-Mean | < 5 days | > 7 days | SAGE |
| VEGA Premium Win Rate | > 65% | < 55% | VEGA |
| CIPHER OOS Sharpe | > 1.5 | < 1.0 | CIPHER |

---

## Philosophy Statements (Each Trader's Core Identity)

> **ATLAS:** *"Strategy is easy. Execution is everything. Knowing when to pause is wisdom."*

> **GHOST:** *"I am the ghost in the machine. No noise. No emotion. Just the flow."*

> **NOVA:** *"Stars don't flicker. They burn. Be the asset that's already on fire."*

> **REX:** *"The market compresses like a spring. I wait. I wait. Then I ride the explosion."*

> **SAGE:** *"Extreme fear is not the end. It is the signal."*

> **VEGA:** *"Price is what you see. Volatility is what you feel. I trade the feeling."*

> **CIPHER:** *"The algorithm is not the edge. The willingness to update it is."*

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-04-18 | Initial team creation |
| — | — | (All future changes logged here) |

---

*Built on the principle that elite performance comes from the system, not just the individual.*
*OLYMPUS TRADING COLLECTIVE — Version 1.0.0*
