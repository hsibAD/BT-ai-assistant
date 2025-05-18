import requests

def resolve_token(keyword):
    keyword = keyword.lower()

    try:
        # получаем топ-500 реальных токенов
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 250,
            "page": 1
        }

        top_tokens = []
        for page in range(1, 3):  # 250 * 2 = топ 500
            params["page"] = page
            resp = requests.get(url, params=params)
            top_tokens.extend(resp.json())

        # сначала точное совпадение по symbol (если keyword похож на символ)
        if keyword.isalpha() and len(keyword) <= 5:
            for coin in top_tokens:
                if coin["symbol"].lower() == keyword:
                    return coin["id"]

        # затем точное совпадение по id или name
        for coin in top_tokens:
            if coin["id"] == keyword or coin["name"].lower() == keyword:
                return coin["id"]

        return None  # ничего не нашли в топе
    except Exception as e:
        print(f"❌ Token resolution failed: {e}")
        return None
