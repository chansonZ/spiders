""" The crawler for Bike Components (https://www.bike-components.de). """

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as Extractor
from scrapy.selector import Selector

from datetime import datetime

from ..items import Product, BikeComponentsProductLoader


class BikeComponents(CrawlSpider):
    name = 'bike-components'
    allowed_domains = ['bike-components.de']
    start_urls = ['https://www.bike-components.de/en/Fulcrum/']
    rules = [Rule(Extractor(allow='/en/Fulcrum/\w+'), callback='parse_product_page'), Rule(Extractor(allow='page='))]


class BikeComponentsReviews(BikeComponents):
    name = 'bike-components-reviews'

    @staticmethod
    def parse_product_page(response):
        loader = BikeComponentsProductLoader(item=Product(), response=response)

        loader.add_xpath('reviews', '//*[@id="module-product-reviews-list"]/div/div[2]/div/div[1]/span/text()')
        loader.add_xpath('reviews', '//*[@id="module-product-reviews-list"]/div/div[2]/div/span/text()')
        loader.add_xpath('reviews', '//*[@id="module-product-reviews-list"]/div/div[2]/div/p/text()')

        return loader.load_item()


class BikeComponentsProducts(BikeComponents):
    name = 'bike-components-products'

    @staticmethod
    def parse_product_page(response):
        loader = BikeComponentsProductLoader(item=Product(), response=response)
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
            loader.add_value('manufacturer', u'Fulcrum')
            loader.add_value('retailer', u'bike-components.de')

            yield loader.load_item()
