import requests
from pprint import pprint

POISE_API_KEY = ""

def get_search_single_page():

    url = "https://poise.network/api/v1/e-commerce/search/"

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
        "keyword": "cola",
        "page": 1,
        "output": "json",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=5)

    breakpoint()

    pprint(response.json())

if __name__ == "__main__":
    get_search_single_page()
