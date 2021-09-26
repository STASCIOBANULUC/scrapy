import scrapy


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['price.ua']
    start_urls = ['https://price.ua/']
    pages_count = 51

    def start_requests(self):
        for page in range(1, 1 + self.pages_count):
            url = f"https://price.ua/ua/firms/page{page}.html"
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        for href in response.css('.product-item.firms-list.shop-item .rating-wrap a::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        item = {
            'url': response.request.url,
            "title": response.css('.block-ellipsis::text').extract(),
            'phone': response.css('.contact-table .td-value::text').extract()
        }
        yield item
