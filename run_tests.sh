#!/bin/bash

# OLYMPUS VERIFICATION SUITE

echo "----------------------------------------"
echo "🏛️ OLYMPUS SYSTEM VERIFICATION"
echo "----------------------------------------"

# 1. Check Directory Structure
echo "Step 1: Verifying directory and file structure..."
python3 tests/verify_structure.py
if [ $? -ne 0 ]; then
    echo "FAILED: System structure is incomplete."
    exit 1
fi

# 2. Check JSON Validity
echo "Step 2: Verifying integrity of initialized data files..."
python3 tests/verify_json_validity.py
if [ $? -ne 0 ]; then
    echo "FAILED: One or more JSON files are corrupted or invalid."
    exit 1
fi

# 3. Check Documentation
echo "Step 3: Checking documentation coverage..."
REQUIRED_MD=("README.md" "TEAM_LEADER.md" "GHOST_scalper.md" "NOVA_momentum.md" "REX_breakout.md" "SAGE_mean_reversion.md" "VEGA_options_vol.md" "CIPHER_algo_quant.md" "SHARED_SYSTEMS.md" "EVOLUTION_ENGINE.md" "OPERATIONS.md")
for doc in "${REQUIRED_MD[@]}"; do
    if [ ! -f "$doc" ]; then
        echo "❌ Missing core documentation: $doc"
        exit 1
    fi
done
echo "✅ Core documentation is complete."

echo "----------------------------------------"
echo "🏛️ ALL SYSTEMS GO"
echo "----------------------------------------"
