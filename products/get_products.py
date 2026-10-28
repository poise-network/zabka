import requests
from pprint import pprint

POISE_API_KEY = ""

def get_products():

    url = "https://poise.network/api/v1/e-commerce/products/"

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
        "category_id": "5d9cd9d1-9883-4bf4-aac5-4a6c484c2cc4",
        "page": 1,
        "output": "json",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=5)

    pprint(response.json())

if __name__ == "__main__":
    get_products()
