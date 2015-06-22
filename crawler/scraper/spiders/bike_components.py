""" The crawler for Bike Components (https://www.bike-components.de). """

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as Extractor
from scrapy.selector import Selector

from datetime import datetime

from ..items import PriceLoader, ReviewLoader, Review, Price

MANUFACTURER = 'Fulcrum'
RETAILER = 'bike-components.de'


class BikeComponents(CrawlSpider):
    allowed_domains = ['bike-components.de']
    start_urls = ['https://www.bike-components.de/en/Fulcrum/']
    rules = [Rule(Extractor(allow='/en/Fulcrum/\w+'), callback='parse_product'), Rule(Extractor(allow='page='))]


class BikeComponentsReviews(BikeComponents):
    name = 'bike-components-reviews'

    @staticmethod
    def parse_product(response):
        loader = ReviewLoader(item=Review(), response=response)
        s = Selector(response=response)

        title = s.xpath('//div[@id="module-product-item"]/div[3]/div[1]/h1/span/text()').extract()
        ratings = s.xpath('//*[@id="module-product-reviews-list"]/div/div[2]/div/div[1]/span/text()').extract()
        dates = s.xpath('//*[@id="module-product-reviews-list"]/div/div[2]/div/span/text()').extract()
        authors = s.xpath('//*[@id="module-product-reviews-list"]/div/div[2]/div/span/text()').extract()
        reviews = s.xpath('//*[@id="module-product-reviews-list"]/div/div[2]/div/p/text()').extract()

        # A single product page may contain multiple reviews.
        # From a scraping point of view, each review is one item.
        for rating, date, author, review in zip(ratings, dates, authors, reviews):
            loader.add_value('name', title)
            loader.add_value('url', response.url)
            loader.add_value('manufacturer', MANUFACTURER)
            loader.add_value('retailer', RETAILER)
            loader.add_value('rating', rating)
            loader.add_value('date', date)
            loader.add_value('author', author)
            loader.add_value('review', review)

            yield loader.load_item()


class BikeComponentsPrices(BikeComponents):
    name = 'bike-components-prices'

    @staticmethod
    def parse_product(response):
        loader = PriceLoader(item=Price(), response=response)
        s = Selector(response=response)

        title = s.xpath('//div[@id="module-product-item"]/div[3]/div[1]/h1/span/text()').extract()
        id_ = s.xpath('//div[@id="module-product-item-description"]/span[1]/span/text()').extract()
        prices_1 = s.xpath('//*[@id="module-product-item-description"]/div/ul/li/span[2]/text()').extract()
        prices_2 = s.xpath('//*[@id="module-product-item"]/div[3]/div[1]/div[2]/span/text()').extract()
        models = s.xpath('//*[@id="module-product-item-description"]/div/ul/li/span[1]/text()').extract()
        stocks = s.xpath('//*[@id="module-product-item-description"]/div/ul/li/span[3]/text()').extract()

        # A single product page may contain multiple models.
        for price_1, price_2, model, stock in zip(prices_1, prices_2, models, stocks):
            loader.add_value('price', price_1)
            loader.add_value('price', price_2)
            loader.add_value('hash', MANUFACTURER)
            loader.add_value('hash', RETAILER)
            loader.add_value('hash', title[0])
            loader.add_value('hash', model)
            loader.add_value('stock', stock)
            loader.add_value('name', title[0])
            loader.add_value('model', model)
            loader.add_value('slug', title[0])
            loader.add_value('id', id_[0])
            loader.add_value('url', response.url)
            loader.add_value('timestamp', datetime.now())
            loader.add_value('manufacturer', MANUFACTURER)
            loader.add_value('retailer', RETAILER)

            yield loader.load_item()
