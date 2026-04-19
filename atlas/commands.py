import re
from atlas.core import ATLAS

class CommandHandler:
    def __init__(self, atlas: ATLAS):
        self.atlas = atlas

    def handle(self, command_text: str):
        command_text = command_text.strip().upper()

        # CAPITAL COMMANDS
        if "SET TOTAL CAPITAL TO $" in command_text:
            match = re.search(r"\$(\d+(?:,\d+)?(?:\.\d+)?)", command_text)
            if match:
                amount = float(match.group(1).replace(",", ""))
                self.atlas.set_total_capital(amount)
                return f"Total capital set to ${amount:,.2f}"

        if "SET MAX DAILY LOSS TO " in command_text:
            match = re.search(r"(\d+(?:\.\d+)?)%", command_text)
            if match:
                percent = float(match.group(1))
                self.atlas.set_max_daily_loss(percent)
                return f"Max daily loss set to {percent}%"

        if "INCREASE " in command_text and " ALLOCATION BY " in command_text:
             match = re.search(r"INCREASE (\w+)(?:'S)? ALLOCATION BY (\d+(?:\.\d+)?)%", command_text)
             if match:
                 trader_name = match.group(1)
                 percent = float(match.group(2)) / 100.0
                 if trader_name in self.atlas.allocations:
                     self.atlas.allocations[trader_name] += percent
                     self.atlas.rebalance_allocations(self.atlas.allocations)
                     return f"Increased {trader_name}'s allocation by {percent*100}%"

        # CONTROL COMMANDS
        if command_text == "PAUSE ALL TRADING":
            self.atlas.is_paused = True
            for trader in self.atlas.traders.values():
                trader.pause("Global pause")
            return "All trading PAUSED"

        if command_text == "RESUME TRADING":
            self.atlas.is_paused = False
            for trader in self.atlas.traders.values():
                trader.resume()
            return "Trading RESUMED"

        if command_text.startswith("PAUSE "):
            trader_name = command_text.replace("PAUSE ", "").strip()
            if trader_name in self.atlas.traders:
                self.atlas.traders[trader_name].pause("Manual pause")
                return f"Trader {trader_name} PAUSED"

        if command_text == "KILL SWITCH":
            for trader in self.atlas.traders.values():
                trader.pause("KILL SWITCH triggered")
                # In real life, close all positions here
            return "EMERGENCY KILL SWITCH: All positions flat, all traders paused."

        # MARKET COMMANDS
        if "ADD " in command_text and " TO THE WATCHLIST" in command_text:
            match = re.search(r"ADD (\w+) TO THE WATCHLIST", command_text)
            if match:
                asset = match.group(1)
                if asset not in self.atlas.watchlist:
                    self.atlas.watchlist.append(asset)
                    return f"Added {asset} to the watchlist"

        if "FOCUS ON CRYPTO ONLY" in command_text:
            self.atlas.watchlist = ["BTC", "ETH", "SOL", "ADA", "DOT"]
            return "Market focus shifted to CRYPTO ONLY."

        if "AVOID ALL STOCKS" in command_text:
            self.atlas.watchlist = [a for a in self.atlas.watchlist if a not in ["SPX", "TSLA", "AAPL"]]
            return "Stocks removed from watchlist."

        # REPORTING COMMANDS
        if "GIVE ME TODAY'S SUMMARY" in command_text or "GIVE ME TODAY’S SUMMARY" in command_text:
             from atlas.reporting import generate_daily_report
             return generate_daily_report(self.atlas)

        return "Command not recognized or not yet implemented."
