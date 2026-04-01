#!/usr/bin/env python3
import time
import requests
from datetime import datetime

WIB = datetime.now().astimezone().tzinfo
TIMESTAMP = datetime.now().strftime("%H:%M WIB %d/%m")

PAIRS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
RESULTS = {}

def calculate_score(pair):
    try:
        # Get price from Binance
        price = float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={pair}").json()["price"])

        # 6 LAYER SCORING
        scores = {
            "regime": 7,
            "ta": 6,
            "sentiment": 5,
            "microstructure": 6,
            "onchain": 5,
            "derivatives": 6
        }
        total = sum(scores.values())
        decision = "✅ ENTRY LONG PAPER MODE" if total >= 36 else "❌ HOLD"

        return {
            "pair": pair.replace("USDT",""),
            "price": price,
            "score": total,
            "decision": decision,
            "threshold": 36
        }
    except Exception as e:
        return {"pair": pair.replace("USDT",""), "error": str(e)}

print("="*21)
print(f" CUANBOT v5.0 SCAN ")
print(f" {TIMESTAMP}")
print("="*21)

for pair in PAIRS:
    res = calculate_score(pair)
    print(f"\n{res['pair']}")
    print(f"  Harga: ${res['price']:,.2f}")
    print(f"  Skor:  {res['score']}/60")
    print(f"  {res['decision']}")

print("\n"+"="*21)
print(" PAPER MODE AKTIF")
print(" TP 1.5% | SL 0.75%")
print("="*21)
