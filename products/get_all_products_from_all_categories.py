import requests
from pprint import pprint

import time
import random

POISE_API_KEY = ""

PLATFORM = "android"
COUNTRY = "pl"
MODE = "quick-delivery"
STORE_ID = "zabka_pl_android_warszawa_01_210_szarych_szeregow_11"

def get_all_products_from_all_categories():

    categories = get_categories().json()
 
    category_ids = [category['id'] for category in categories]
    category_names = [category['name'] for category in categories]

    products = {}

    # Iterate over categories
    for id, name in zip(category_ids, category_names):

        print(f"Retrieving products for category: {name} (ID: {id})")

        products[id] = []
        
        keep_requesting = True
        page = 1

        while keep_requesting:
                
            url = "https://poise.network/api/v1/e-commerce/zabka/products/"

            headers = {
                "Authorization": f"Bearer {POISE_API_KEY}",
                "Content-Type": "application/json",
            }

            payload = {
                "platform": PLATFORM,
                "country": COUNTRY,
                "mode": MODE,
                "store_id": STORE_ID,
                "category_id": id,
                "page": page,
                "output": "json",
                "freshness": "fresh",
            }

            print(f"Requesting page {page}...")

            response = requests.post(url, headers=headers, json=payload, timeout=5)
            current_page_count = len(response.json()['data']['categoryProducts']['results'])
            
            print(f"Got {current_page_count} products on page {page}...")


            if len(response.json()['data']['categoryProducts']['results']) != 0:
                
                products[id].extend(response.json()['data']['categoryProducts']['results'])
                page += 1
                # Add a random delay between requests to avoid overwhelming the retailer server
                time.sleep(random.uniform(0.5, 1.0))
            else:
                keep_requesting = False

        print(f"Total products retrieved for category {name}: {len(products[id])}")

    pprint(products)


def get_categories():

    url = "https://poise.network/api/v1/e-commerce/zabka/categories/"

    headers = {
        "Authorization": f"Bearer {POISE_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "platform": PLATFORM,
        "country": COUNTRY,
        "mode": MODE,
        "store_id": STORE_ID,
        "output": "json",
        "freshness": "fresh",
    }

    return requests.post(url, headers=headers, json=payload, timeout=5)

if __name__ == "__main__":
    get_all_products_from_all_categories()
