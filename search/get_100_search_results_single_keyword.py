import requests
from pprint import pprint
import time
import random

POISE_API_KEY = ""

def get_100_search_results_single_keyword():

    # Search returns 24 items in the first page, and then 12 items in the subsequent pages.
    page = 1
    search_results = []

    while page <= 8:  # Limit to 8 pages for testing (24 + 7*12 = 108 items)

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
            "page": page,
            "output": "json",
        }

        response = requests.post(url, headers=headers, json=payload, timeout=5)

        if len(response.json()['data']['productSearch']['results']) != 0:
            print(f"Page {page}: Retrieved {len(response.json()['data']['productSearch']['results'])} products")
            search_results.extend(response.json()['data']['productSearch']['results'])
            page += 1
            time.sleep(random.uniform(0.5, 1.0))
        else:
            print(f"No more products found on page {page}. Stopping search.")
            break

    search_results = search_results[:100]  # Limit to first 100 items

    pprint(response.json())

if __name__ == "__main__":
    get_100_search_results_single_keyword()
