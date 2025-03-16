import aiohttp
import asyncio
import pandas as pd

# API endpoints for the exchanges
EXCHANGE_URLS = {
    "OKX": "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT",
    "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT",
    "Bitget": "https://api.bitget.com/api/v2/market/ticker?symbol=BTCUSDT_SPBL",
    "Upbit": "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
}

async def fetch_price(session, name, url):
    """Fetch price from an exchange."""
    try:
        async with session.get(url) as response:
            data = await response.json()
            if name == "OKX":
                return name, float(data['data'][0]['last'])
            elif name == "KuCoin":
                return name, float(data['data']['price'])
            elif name == "Bitget":
                return name, float(data['data']['close'])
            elif name == "Upbit":
                return name, float(data[0]['trade_price'])
    except Exception:
        return name, None

async def get_prices():
    """Fetch prices from all exchanges asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_price(session, name, url) for name, url in EXCHANGE_URLS.items()]
        return dict(await asyncio.gather(*tasks))

def compare_prices():
    """Compare Upbit price with others and print differences."""
    prices = asyncio.run(get_prices())
    upbit_price = prices.get("Upbit")

    if upbit_price is None:
        print("Failed to fetch Upbit price")
        return

    print("\nExchange Price Differences from Upbit:\n")
    for name, price in prices.items():
        if name != "Upbit" and price is not None:
            diff_percent = ((upbit_price - price) / price) * 100
            print(f"{name}: {price} | Difference: {round(diff_percent, 2)}%")

if __name__ == "__main__":
    compare_prices()
