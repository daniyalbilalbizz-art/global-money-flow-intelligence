"""Provenance-aware public market data adapter."""
from datetime import datetime, timezone
import requests

BASE = "https://data-api.binance.vision"

def get_binance_ticker(symbol="BTCUSDT", timeout=10):
    response = requests.get(BASE + "/api/v3/ticker/24hr", params={"symbol": symbol.upper()}, timeout=timeout, headers={"User-Agent": "GMF-OS/0.1"})
    response.raise_for_status()
    item = response.json()
    return {"symbol": item["symbol"], "last_price": float(item["lastPrice"]), "price_change_pct_24h": float(item["priceChangePercent"]), "volume_base_24h": float(item["volume"]), "source": "Binance public 24h ticker", "source_url": BASE + "/api/v3/ticker/24hr?symbol=" + symbol.upper(), "retrieved_at": datetime.now(timezone.utc).isoformat(), "classification": "reported_market_data"}
