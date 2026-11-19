import requests
from pprint import pprint

POISE_API_KEY = ""

def get_products():

    url = "https://poise.network/api/v1/e-commerce/zabka/pdp/"

    headers = {
        "Authorization": f"Bearer {POISE_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "platform": "android",
        "country": "pl",
        "mode": "quick-delivery",
        "store_id": "zabka_pl_android_warszawa_01_210_szarych_szeregow_11",
        "product_id": "A0006778",
        "output": "json",
        "freshness": "fresh",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=5)

    pprint(response.json())

if __name__ == "__main__":
    get_products()
