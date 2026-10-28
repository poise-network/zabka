import requests
from pprint import pprint
import time
import random

POISE_API_KEY = ""

PLATFORM = "android"
RETAILER = "zabka-jush"
COUNTRY = "pl"
MODE = "quick-delivery"
LAT = 52.2356949
LNG = 20.9941515
KEYWORD = "cola"

def get_all_pdp_pages_per_search_keyword():
    
    products = get_100_search_results_single_keyword()
    product_ids = {product['sku'] for product in products}

    pdps = []

    print(f"Retrieving PDP pages for products returned by search for {KEYWORD}...")

    for product_id in product_ids:
        url = "https://poise.network/api/v1/e-commerce/pdp/"

        headers = {
            "Authorization": f"Bearer {POISE_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "platform": PLATFORM,
            "retailer": RETAILER,
            "country": COUNTRY,
            "mode": MODE,
            "lat": LAT,
            "lng": LNG,
            "product_id": product_id,
            "output": "json",
        }

        print(f"Requesting pdp page for product {product_id}...")

        response = requests.post(url, headers=headers, json=payload, timeout=5)

        print(f"Got pdp page for product {product_id}...")

        pdps.append(response.json())

        time.sleep(random.uniform(0.5, 1.0))

    pdp_descriptions = [{'id': pdp['data']['product']['id'],
                         'description': pdp['data']['product']['description']} for pdp in pdps]
    
    pprint(pdp_descriptions)

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
            "platform": PLATFORM,
            "retailer": RETAILER,
            "country": COUNTRY,
            "mode": MODE,
            "lat": LAT,
            "lng": LNG,
            "keyword": KEYWORD,
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

    return search_results

if __name__ == "__main__":
    get_all_pdp_pages_per_search_keyword()