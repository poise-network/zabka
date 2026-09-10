import json

import requests
import scrapy
from scrapy.http import JsonRequest


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

        url = "https://poise.network/api/v1/e-commerce/products/"

        headers = {
            "Authorization": f"Bearer {self.POISE_API_KEY}",
            "Content-Type": "application/json",
        }

        # TESTING
        first_key, first_value = next(iter(categories.items()))
        categories = {first_key: first_value}

        for category_id in categories.keys():
            payload = {
                "platform": "android",
                "retailer": "zabka-jush",
                "country": "pl",
                "mode": "quick-delivery",
                "lat": 52.2356949,
                "lng": 20.9941515,
                "category_id": category_id,
                "page": 1,
                "output": "json"
            }

            yield JsonRequest(
                url=url,
                headers=headers,
                data=payload,
                callback=self.parse_products,
                meta={"page": 1, "category_id": category_id},
                dont_filter=True
            )

    def parse_products(self, response):
        data = response.json()

        if response.meta["page"] > 3:
            return

        if int(data['data']['categoryProducts']['total']) > 0:

            request = response.request.copy()
            payload = json.loads(request.body)
            payload["page"] += 1
            request.meta["page"] += 1
            
            paginated_request = response.request.replace(
                body=json.dumps(payload).encode(),
                dont_filter=True,
            )

            yield paginated_request

        products = data['data']['categoryProducts']['results']

        for product in products[:1]:  # Limit to first product for testing
            item = {}
            item['id'] = product.get('sku')
            item['name'] = product.get('name')

            yield product

    def get_categories(self):

        url = "https://poise.network/api/v1/e-commerce/categories/"

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
