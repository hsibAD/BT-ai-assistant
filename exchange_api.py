import requests
from binance_symbols import BINANCE_SYMBOLS

def get_binance_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}USDT"
    try:
        response = requests.get(url)
        print("🪵 [BINANCE API] URL:", url)
        print("🪵 [BINANCE API] Status:", response.status_code)
        print("🪵 [BINANCE API] Text:", response.text)

        if response.status_code != 200:
            return None, f"Binance API error: {response.status_code}. {response.text}"

        data = response.json()
        return float(data['price']), None
    except Exception as e:
        return None, f"Exception: {e}"

def get_price(token_name):
    token_name = token_name.lower()

    # 1. Попробовать через заранее известную мапу
    symbol = BINANCE_SYMBOLS.get(token_name)
    if symbol:
        price, error = get_binance_price(symbol)
        if price is not None:
            return f"Current price on Binance: {price} USDT"
        else:
            return error

    # 2. Если не найден в мапе — попробовать найти через CoinGecko
    try:
        gecko_url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(gecko_url)
        tokens = response.json()

        for coin in tokens:
            if coin["id"] == token_name or coin["name"].lower() == token_name:
                symbol = coin["symbol"]
                price, error = get_binance_price(symbol)
                if price is not None:
                    return f"Current price on Binance: {price} USDT"
                else:
                    return error
        return f"❌ Could not match '{token_name}' with any CoinGecko or Binance token."
    except Exception as e:
        return f"CoinGecko lookup failed: {e}"
