import requests
from pprint import pprint

POISE_API_KEY = ""

def get_search_single_page():

    url = "https://poise.network/api/v1/e-commerce/zabka/search/"

    headers = {
        "Authorization": f"Bearer {POISE_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "platform": "android",
        "country": "pl",
        "mode": "quick-delivery",
        "store_id": "zabka_pl_android_warszawa_01_210_szarych_szeregow_11",
        "keyword": "cola",
        "page": 1,
        "output": "json",
        "freshness": "fresh",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=5)

    pprint(response.json())

if __name__ == "__main__":
    get_search_single_page()
