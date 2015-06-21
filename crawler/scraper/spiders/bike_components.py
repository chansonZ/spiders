""" The crawler for Bike Components (https://www.bike-components.de). """

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as Extractor
from scrapy.selector import Selector

from datetime import datetime

from ..items import Product, BikeComponentsPriceLoader, BikeComponentsReviewLoader, Review, Price

MANUFACTURER = u'Fulcrum'
RETAILER = u'bike-components.de'


class BikeComponents(CrawlSpider):
    allowed_domains = ['bike-components.de']
    start_urls = ['https://www.bike-components.de/en/Fulcrum/']
    rules = [Rule(Extractor(allow='/en/Fulcrum/\w+'), callback='parse_product_page'), Rule(Extractor(allow='page='))]


class BikeComponentsReviews(BikeComponents):
    name = 'bike-components-reviews'

    @staticmethod
    def parse_product_page(response):
        loader = BikeComponentsReviewLoader(item=Review(), response=response)

        loader.add_xpath('name', '//div[@id="module-product-item"]/div[3]/div[1]/h1/span/text()')
        loader.add_xpath('rating', '//*[@id="module-product-reviews-list"]/div/div[2]/div/div[1]/span/text()')
        loader.add_xpath('date', '//*[@id="module-product-reviews-list"]/div/div[2]/div/span/text()')
        loader.add_xpath('author', '//*[@id="module-product-reviews-list"]/div/div[2]/div/span/text()')
        loader.add_xpath('review', '//*[@id="module-product-reviews-list"]/div/div[2]/div/p/text()')

        loader.add_value('url', response.url)
        loader.add_value('manufacturer', MANUFACTURER)
        loader.add_value('retailer', RETAILER)

        return loader.load_item()


class BikeComponentsPrices(BikeComponents):
    name = 'bike-components-prices'

    @staticmethod
    def parse_product_page(response):
        loader = BikeComponentsPriceLoader(item=Price(), response=response)
        selector = Selector(response=response)

        title_xpath = '//div[@id="module-product-item"]/div[3]/div[1]/h1/span/text()'
        id_xpath = '//div[@id="module-product-item-description"]/span[1]/span/text()'

        title = selector.xpath(title_xpath).extract()
        id_ = selector.xpath(id_xpath).extract()

        # Parse a product from bike-components.de. A single product page may contains multiple
        # sub-products (models). From a scraping point of view, each model is one product.

        prices_xpath_1 = '//*[@id="module-product-item-description"]/div/ul/li/span[2]/text()'
        prices_xpath_2 = '//*[@id="module-product-item"]/div[3]/div[1]/div[2]/span/text()'
        models_xpath = '//*[@id="module-product-item-description"]/div/ul/li/span[1]/text()'
        stocks_xpath = '//*[@id="module-product-item-description"]/div/ul/li/span[3]/text()'

        prices_1 = selector.xpath(prices_xpath_1).extract()
        prices_2 = selector.xpath(prices_xpath_2).extract()
        models = selector.xpath(models_xpath).extract()
        stocks = selector.xpath(stocks_xpath).extract()

        for price_1, price_2, model, stock in zip(prices_1, prices_2, models, stocks):

            loader.add_value('price', price_1)
            loader.add_value('price', price_2)

            loader.add_value('hash', u'bike-components')
            loader.add_value('hash', u'fulcrum')
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
