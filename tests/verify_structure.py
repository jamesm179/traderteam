import os
import sys

def verify_structure():
    expected_files = [
        "README.md",
        "TEAM_LEADER.md",
        "GHOST_scalper.md",
        "NOVA_momentum.md",
        "REX_breakout.md",
        "SAGE_mean_reversion.md",
        "VEGA_options_vol.md",
        "CIPHER_algo_quant.md",
        "SHARED_SYSTEMS.md",
        "EVOLUTION_ENGINE.md",
        "OPERATIONS.md",
        "team_portfolio_pnl.json",
        "runtime/ATLAS/SESSION-STATE.md",
        "runtime/ATLAS/MEMORY.md",
        "runtime/ATLAS/regime_log.json",
        "runtime/ATLAS/capital_allocation.json",
        "runtime/ATLAS/consensus_signals.json",
        "runtime/ATLAS/inbox.json",
        "runtime/ATLAS/backtest_queue.json",
        "runtime/ATLAS/evolution_status.json",
        "runtime/ATLAS/evolution_leaderboard.json",
        "runtime/ATLAS/team_learnings.md"
    ]

    traders = ["GHOST", "NOVA", "REX", "SAGE", "VEGA", "CIPHER"]
    for t in traders:
        expected_files.append(f"runtime/{t}/SESSION-STATE.md")
        expected_files.append(f"runtime/{t}/MEMORY.md")
        expected_files.append(f"runtime/{t}/data/{t.lower()}_trades.json")
        expected_files.append(f"runtime/{t}/data/rejected_setups.json")
        expected_files.append(f"runtime/{t}/sr_levels.json")
        expected_files.append(f"runtime/{t}/.learnings/LEARNINGS.md")
        expected_files.append(f"runtime/{t}/.learnings/ERRORS.md")
        expected_files.append(f"runtime/{t}/.learnings/LOSS_REVIEWS.md")
        expected_files.append(f"runtime/{t}/.learnings/REGIME_ANALYSIS.md")
        expected_files.append(f"runtime/{t}/.learnings/SETUP_AUDITS.md")

    # Special files for specific traders
    expected_files.append("runtime/NOVA/watchlist.json")
    expected_files.append("runtime/NOVA/.learnings/MISTAKE_TAXONOMY.md")
    expected_files.append("runtime/REX/.learnings/HARD_RULES.md")
    expected_files.append("runtime/SAGE/statistics/reversion_stats.json")
    expected_files.append("runtime/VEGA/vol_dashboard.json")
    expected_files.append("runtime/VEGA/flow_alerts/unusual_activity.json")

    for i in range(1, 5):
        expected_files.append(f"runtime/CIPHER/strategies/C{i}_" + ["momentum", "pairs", "adaptive_rsi", "orb"][i-1] + ".json")

    missing = []
    for f in expected_files:
        if not os.path.exists(f):
            missing.append(f)

    if missing:
        print("❌ Structure Verification Failed. Missing files:")
        for f in missing:
            print(f"  - {f}")
        return False

    print("✅ Project structure verified successfully.")
    return True

if __name__ == "__main__":
    if not verify_structure():
        sys.exit(1)
