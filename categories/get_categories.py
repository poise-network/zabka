import requests
from pprint import pprint

POISE_API_KEY = ""

def request_categories():

    url = "https://poise.network/api/v1/e-commerce/zabka/categories/"

    headers = {
        "Authorization": f"Bearer {POISE_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "platform": "android",
        "country": "pl",
        "mode": "quick-delivery",
        "lat": 52.2356949,
        "lng": 20.9941515,
        "output": "json",
        "freshness": "fresh",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=5)

    pprint(response.json())

if __name__ == "__main__":
    request_categories()
