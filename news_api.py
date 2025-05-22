import requests
import re
from token_resolver import resolve_token

API_KEY = "4ab44d6d714e6a3f793342659c15efe45ad8bc39"

def escape_markdown(text):
    return re.sub(r'([*_`\[\]()~])', r'\\\1', text)

def get_news(query):
    token = query.lower()

    # Получаем символ токена через CoinGecko
    try:
        gecko_url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(gecko_url)
        tokens = response.json()
        symbol = None
        for coin in tokens:
            if coin["id"] == token or coin["name"].lower() == token:
                symbol = coin["symbol"].upper()
                break
        if not symbol:
            symbol = token.upper()
    except:
        symbol = token.upper()

    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={API_KEY}&currencies={symbol}"
    try:
        response = requests.get(url)
        print("🪵 [NEWS API] URL:", url)
        print("🪵 [NEWS API] Status Code:", response.status_code)

        if response.status_code != 200:
            return [f"CryptoPanic API error: {response.status_code}"]

        data = response.json()
        if 'results' not in data:
            return [f"CryptoPanic response missing 'results': {data}"]

        headlines = []
        for item in data['results'][:5]:
            title = item.get('title')
            link = item.get('url')
            if title and link:
                title = escape_markdown(title)
                headlines.append(f"[{title}]({link})")

        return headlines if headlines else ["No news found."]
    except Exception as e:
        return [f"Error when receiving news: {e}"]
