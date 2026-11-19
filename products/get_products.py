import requests
from pprint import pprint

POISE_API_KEY = ""

def get_products():

    url = "https://poise.network/api/v1/e-commerce/zabka/products/"

    headers = {
        "Authorization": f"Bearer {POISE_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "platform": "android",
        "country": "pl",
        "mode": "quick-delivery",
        "store_id": "zabka_pl_android_warszawa_01_210_szarych_szeregow_11",
        "category_id": "5d9cd9d1-9883-4bf4-aac5-4a6c484c2cc4",
        "page": 1,
        "output": "json",
        "freshness": "fresh",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=5)

    pprint(response.json())

if __name__ == "__main__":
    get_products()
