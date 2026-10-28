import time
import random

import requests
from pprint import pprint

POISE_API_KEY = ""

CATEGORY = {'name': "WARZYWA I OWOCE",
            'id': "5d9cd9d1-9883-4bf4-aac5-4a6c484c2cc4"}

def get_all_pdp_pages_per_category():

    products = get_all_products_per_category()
    # Extract product IDs from the products list. Remove duplicates
    product_ids = {product['sku'] for product in products}

    pdps = []

    print(f"Retrieving PDP pages for products in category {CATEGORY['name']}...")

    for product_id in product_ids:
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


def get_all_products_per_category():

    category = CATEGORY

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

    return products

if __name__ == "__main__":
    get_all_pdp_pages_per_category()