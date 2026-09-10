import scrapy
from scrapy.http import JsonRequest


class CategoriesSpider(scrapy.Spider):
    name = "categories"
    allowed_domains = ["poise.network"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    POISE_API_KEY = ""

    async def start(self):

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

        yield JsonRequest(
            url=url,
            headers=headers,
            data=payload,
            callback=self.parse_categories,
            dont_filter=True
        )

    def parse_categories(self, response):
        data = response.json()
        results = data["data"]["categories"]["results"]

        categories = self.collect_categories(results)

        yield categories

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
