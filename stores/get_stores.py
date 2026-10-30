import requests
from pprint import pprint

POISE_API_KEY = ""

def get_stores():

    url = "https://poise.network/api/v1/e-commerce/stores/"

    headers = {
        "Authorization": f"Bearer {POISE_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "retailer": "zabka-jush",
        "platform": "android",
        "country": "pl",
        "mode": "quick-delivery",
        "freshness": "cached"
    }

    response = requests.post(url, headers=headers, json=payload, timeout=5)

    pprint(response.json())

if __name__ == "__main__":
    get_stores()
