import time
import random

import requests
from pprint import pprint

POISE_API_KEY = ""

def get_all_products_per_category():

    category = {'name': "WARZYWA I OWOCE",
                'id': "5d9cd9d1-9883-4bf4-aac5-4a6c484c2cc4"}

    products = []
    keep_requesting = True
    page = 1

    while keep_requesting:
            
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
            "category_id": category['id'],
            "page": page,
            "output": "json",
        }

        print(f"Requesting page {page}...")

        response = requests.post(url, headers=headers, json=payload, timeout=5)
        current_page_count = len(response.json()['data']['categoryProducts']['results'])
        
        print(f"Got {current_page_count} products on page {page}...")

        if current_page_count != 0:
            products.extend(response.json()['data']['categoryProducts']['results'])
            page += 1
            # Add a random delay between requests to avoid overwhelming the retailer server
            time.sleep(random.uniform(0.5, 1.0))
        else:
            keep_requesting = False
            
    print(f"Total products retrieved: {len(products)} for category {category['name']}.")

if __name__ == "__main__":
    get_all_products_per_category()
