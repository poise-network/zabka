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

class SearchSpider(scrapy.Spider):
    name = "search"
    allowed_domains = ["poise.network"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    POISE_API_KEY = ""

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS": 1,
    }

    async def start(self):

        path = os.path.join('static', 'data', 'keywords.json')
        with open(path, 'r') as f:
            keywords = json.load(f)

        url = f"{POISE_API_URL}/api/v1/e-commerce/search/"

        headers = {
            "Authorization": f"Bearer {self.POISE_API_KEY}",
            "Content-Type": "application/json",
        }

        for keyword in keywords:
            payload = {
                "platform": "android",
                "retailer": "zabka-jush",
                "country": "pl",
                "mode": "quick-delivery",
                "lat": 52.2356949,
                "lng": 20.9941515,
                "keyword": keyword,
                "page": 1,
                "output": "json"
            }

            yield JsonRequest(
                url=url,
                headers=headers,
                data=payload,
                callback=self.parse_search,
                meta={"page": 1,
                      "keyword": keyword},
                dont_filter=True
            )

    def pagination(callback):
        def wrapper(self, response, *args, **kwargs):
            data = response.json()

            yield from callback(self, response, *args, **kwargs)

            if len(data['data']['productSearch']['results']) > 0:

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

    @pagination
    def parse_search(self, response):
        data = response.json()

        products = data['data']['productSearch']['results']

        for product in products:  # Limit to first product for testing
            item = {}
            item['id'] = product.get('sku')
            item['keyword'] = response.meta.get('keyword')
            item['name'] = product.get('name')
            item['page'] = response.meta.get('page')

            yield item


