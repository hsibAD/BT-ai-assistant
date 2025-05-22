import requests
import time

def resolve_token(keyword):
    try:
        keyword = keyword.lower()

        # Загружаем топ-250 токенов (по капитализации)
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&page=1")
        ranked_tokens = response.json()

        # 1. Строгое совпадение по symbol, id, name
        for coin in ranked_tokens:
            if coin["symbol"].lower() == keyword \
                or coin["id"] == keyword \
                or coin["name"].lower() == keyword:

                time.sleep(1)
                return coin["id"]

        # 2. Частичное совпадение (например "sol" найдёт "solana")
        for coin in ranked_tokens:
            if keyword in coin["symbol"].lower() \
                or keyword in coin["id"] \
                or keyword in coin["name"].lower():
                
                time.sleep(1)
                return coin["id"]

        return None
    except Exception as e:
        print(f"Token resolution failed: {e}")
        return None
