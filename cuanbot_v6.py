#!/usr/bin/env python3
# CUANBOT v6.0 STATIC EXECUTOR
# NO AI, NO LLM, NO GUESSING
# 100% DETERMINISTIC

import os
import hmac
import hashlib
import requests
import time

# ==============================================
#                         CONFIGURATION
# ==============================================
API_KEY    = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
CHAT_ID    = os.getenv('TELEGRAM_CHAT_ID')
BOT_TOKEN  = os.getenv('TELEGRAM_BOT_TOKEN')

RISK_PER_POS   = 0.0025
STOP_LOSS    = 0.0075
TAKE_PROFIT  = 0.015
BASE_URL     = "https://api.binance.com"

def telegram(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
            "chat_id": CHAT_ID, "text": text, "disable_web_page_preview": True
        }, timeout=10)
    except:
        pass

def binance_request(method, path, params=None):
    params = params or []
    server_time = requests.get(f"{BASE_URL}/api/v3/time").json()["serverTime"]
    params.append( ("timestamp", str(server_time)) )
    query = "&".join([ f"{k}={v}" for k,v in params ])
    sig = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    headers = { "X-MBX-APIKEY": API_KEY }
    url = f"{BASE_URL}{path}?{query}&signature={sig}"
    r = requests.request(method, url, headers=headers, timeout=15)
    try:
        return r.json()
    except:
        return { "error": True, "text": r.text }

def get_usdt_balance():
    acc = binance_request("GET", "/api/v3/account")
    if "balances" not in acc:
        return 0.0
    for b in acc["balances"]:
        if b["asset"] == "USDT":
            return float(b["free"])
    return 0.0

def calculate_position_size():
    bal = get_usdt_balance()
    risk_amount = bal * RISK_PER_POS
    return round( risk_amount / STOP_LOSS, 2 )

def open_long_market(pair, usdt_amount):
    return binance_request("POST", "/api/v3/order", [
        ("symbol", pair), ("side", "BUY"), ("type", "MARKET"), ("quoteOrderQty", str(usdt_amount))
    ])

def place_oco_stop(pair, entry_price, quantity):
    tp = round(entry_price * (1 + TAKE_PROFIT), 2)
    sl = round(entry_price * (1 - STOP_LOSS), 2)
    
    return binance_request("POST", "/api/v3/orderList", [
        ("symbol", pair), ("orderListType", "OCO"),
        ("side", "SELL"), ("quantity", str(quantity)),
        ("price", str(tp)),
        ("stopPrice", str(sl)), ("stopLimitPrice", str(sl)), ("stopLimitTimeInForce", "GTC")
    ])

def close_position(pair):
    asset = pair.replace("USDT", "")
    acc = binance_request("GET", "/api/v3/account")
    for b in acc["balances"]:
        if b["asset"] == asset:
            qty = float(b["free"])
            if qty <= 0: return {"msg": "No balance"}
            return binance_request("POST", "/api/v3/order", [
                ("symbol", pair), ("side", "SELL"), ("type", "MARKET"), ("quantity", f"{qty:.8f}")
            ])

if __name__ == "__main__":
    telegram("✅ CUANBOT v6 STARTED")
