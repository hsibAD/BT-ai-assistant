import requests

def get_market_data(token):
    url = f"https://api.coingecko.com/api/v3/coins/{token.lower()}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return f"CoinGecko API error: {response.status_code}"

        data = response.json()
        market_cap = data['market_data']['market_cap']['usd']
        rank = data['market_cap_rank']
        return f"Market Cap: {market_cap} USD\r\nRank: #{rank}"
    except Exception as e:
        return f"Failed to retrieve market data: {e}"
