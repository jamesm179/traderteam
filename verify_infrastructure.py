import json
import os
from shared_infrastructure import RiskModule, send_to_atlas

def test_risk_module():
    print("Testing RiskModule...")
    risk = RiskModule("TESTER", 100000)

    # Test initial state
    allowed, reason = risk.can_trade()
    assert allowed == True
    assert reason == "OK"

    # Test position sizing
    size = risk.calculate_position_size(100, 95)
    # risk_amount = 100000 * 0.015 = 1500
    # distance = (100-95)/100 = 0.05
    # size = 1500 / 0.05 = 30000
    # max size = 100000 * 0.25 = 25000
    assert size == 25000

    # Test daily loss limit
    risk.log_trade_result(-2500) # -2.5%
    allowed, reason = risk.can_trade()
    assert allowed == False
    assert "Daily loss limit" in reason

    # Reset for consecutive losses test
    risk = RiskModule("TESTER", 100000)
    for _ in range(3):
        risk.log_trade_result(-100)
    allowed, reason = risk.can_trade()
    assert allowed == True

    risk.log_trade_result(-100) # 4th loss
    allowed, reason = risk.can_trade()
    assert allowed == False
    assert "4 consecutive losses" in reason

    print("RiskModule tests passed!")

def test_communication():
    print("Testing Communication...")
    inbox_path = "runtime/ATLAS/inbox.json"
    if os.path.exists(inbox_path):
        os.remove(inbox_path)

    send_to_atlas("SIGNAL_CARD", {"asset": "BTC", "direction": "long"}, trader_id="NOVA")

    with open(inbox_path, 'r') as f:
        messages = json.load(f)

    assert len(messages) == 1
    assert messages[0]["from"] == "NOVA"
    assert messages[0]["type"] == "SIGNAL_CARD"
    assert messages[0]["payload"]["asset"] == "BTC"

    print("Communication tests passed!")

if __name__ == "__main__":
    try:
        test_risk_module()
        test_communication()
        print("All infrastructure tests passed successfully!")
    except Exception as e:
        print(f"Tests failed: {e}")
        exit(1)
