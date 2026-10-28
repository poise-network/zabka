import requests
from pprint import pprint

POISE_API_KEY = ""

def get_products():

    url = "https://poise.network/api/v1/e-commerce/pdp/"

    headers = {
        "Authorization": f"Bearer {POISE_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "platform": "android",
        "retailer": "zabka-jush",
        "country": "pl",
        "mode": "quick-delivery",
        "lat": 52.2356949,
        "lng": 20.9941515,
        "product_id": "A0006778",
        "output": "json",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=5)

    pprint(response.json())

if __name__ == "__main__":
    get_products()
