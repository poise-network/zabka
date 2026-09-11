import json
import os

import requests
import scrapy
from scrapy.http import JsonRequest
from dotenv import load_dotenv

load_dotenv()

POISE_API_DOMAIN = os.getenv("POISE_API_DOMAIN")
#POISE_API_DOMAIN = "localhost:8000"
POISE_API_URL = f"http://{POISE_API_DOMAIN}" if 'localhost' in POISE_API_DOMAIN else f"https://{POISE_API_DOMAIN}"


def paginate(callback):
    def wrapper(self, response, *args, **kwargs):
        data = response.json()

        yield from callback(self, response, *args, **kwargs)

        if int(data['data']['categoryProducts']['total']) > 0:

            request = response.request.copy()
            payload = json.loads(request.body)
            payload["page"] += 1
            request.meta["page"] += 1

            paginated_request = request.replace(
                body=json.dumps(payload).encode(),
                dont_filter=True,
            )

            yield paginated_request

    return wrapper


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["poise.network"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    POISE_API_KEY = ""

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS": 1,
    }

    async def start(self):

        categories = self.get_categories()

        url = f"{POISE_API_URL}/api/v1/e-commerce/products/"

        headers = {
            "Authorization": f"Bearer {self.POISE_API_KEY}",
            "Content-Type": "application/json",
        }

        # TESTING
        cat_items = iter(categories.items())
        categories = {}
        for i in range(3):  # Limit to first category for testing
            first_key, first_value = next(cat_items)
            categories.update({first_key: first_value})
        #categories = {'5d9cd9d1-9883-4bf4-aac5-4a6c484c2cc4': 'WARZYWA I OWOCE'}

        for id in categories.keys():
            payload = {
                "platform": "android",
                "retailer": "zabka-jush",
                "country": "pl",
                "mode": "quick-delivery",
                "lat": 52.2356949,
                "lng": 20.9941515,
                "category_id": id,
                "page": 1,
                "output": "json"
            }

            yield JsonRequest(
                url=url,
                headers=headers,
                data=payload,
                callback=self.parse_products,
                meta={"page": 1, "category_id": id},
                dont_filter=True
            )

    @paginate
    def parse_products(self, response):
        data = response.json()

        products = data['data']['categoryProducts']['results']

        for product in products:  # Limit to first product for testing
            item = {}
            item['id'] = product.get('sku')
            item['name'] = product.get('name')

            yield item

    def get_categories(self):

        url = f"{POISE_API_URL}/api/v1/e-commerce/categories/"

        headers = {
            "Authorization": f"Bearer {self.POISE_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "retailer": "zabka-jush",
            "platform": "android",
            "country": "pl",
            "mode": "quick-delivery",
            "lat": 52.2356949,
            "lng": 20.9941515,
            "output": "json",
        }

        response = requests.post(url, headers=headers, json=payload).json()

        return self.parse_categories(response)

    def parse_categories(self, response):

        results = response["data"]["categories"]["results"]

        return self.collect_categories(results)

    def collect_categories(self, category_items):
        categories = {}

        for category in category_items:
            id = category.get("id")
            name = category.get("name")

            if id and name:
                categories[id] = name

            children = category.get("children") or []
            child_categories = self.collect_categories(children)
            categories.update(child_categories)

        return categories
