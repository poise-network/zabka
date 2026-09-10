import scrapy


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["poise.network"]
    start_urls = ["https://poise.network"]

    def parse(self, response):
        pass
