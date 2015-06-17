""" The crawler for Bike Components (https://www.bike-components.de). """

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.exceptions import DropItem
from scrapy.selector import Selector

from datetime import datetime

from ..items import Product, BikeComponentsProductLoader


class BikeComponents(CrawlSpider):
    name = 'bike-components'
    allowed_domains = ['bike-components.de']
    start_urls = ['https://www.bike-components.de/en/Fulcrum/']

    products = LxmlLinkExtractor(allow='/en/Fulcrum/\w+')
    next_page = LxmlLinkExtractor(allow='page=')

    rules = [Rule(products, callback='parse_product_page'), Rule(next_page)]

    @staticmethod
    def parse_product_page(response):
        """ Parse a product from bike-components.de. A single product page may contains multiple
            sub-products (models). From a scraping point of view, each model is one product.
        """

        loader = BikeComponentsProductLoader(item=Product(), response=response)
        selector = Selector(response=response)

        # Paths that point to a single node
        title_xpath = '//div[@id="module-product-item"]/div[3]/div[1]/h1/span/text()'
        id_xpath = '//div[@id="module-product-item-description"]/span[1]/span/text()'

        title = selector.xpath(title_xpath).extract()
        id_ = selector.xpath(id_xpath).extract()

        # Paths that point to multiple nodes
        prices_xpath_1 = '//*[@id="module-product-item-description"]/div/ul/li/span[2]/text()'
        prices_xpath_2 = '//*[@id="module-product-item"]/div[3]/div[1]/div[2]/span/text()'
        models_xpath = '//*[@id="module-product-item-description"]/div/ul/li/span[1]/text()'
        stocks_xpath = '//*[@id="module-product-item-description"]/div/ul/li/span[3]/text()'

        prices_1 = selector.xpath(prices_xpath_1).extract()
        prices_2 = selector.xpath(prices_xpath_2).extract()
        models = selector.xpath(models_xpath).extract()
        stocks = selector.xpath(stocks_xpath).extract()

        try:
            models = zip(prices_1, prices_2, models, stocks)
        except:
            raise DropItem('Cannot scrape: %s' % response.url)

        for price_1, price_2, model, stock in models:

            loader.add_value('price', price_1)
            loader.add_value('price', price_2)

            loader.add_value('hash', u'bike-components')
            loader.add_value('hash', u'fulcrum')
            loader.add_value('hash', title[0])
            loader.add_value('hash', model)

            loader.add_value('stock', stock)

            loader.add_value('name', title[0])
            loader.add_value('id', id_[0])

            loader.add_value('url', response.url)
            loader.add_value('timestamp', datetime.now())
            loader.add_value('manufacturer', u'Fulcrum')
            loader.add_value('retailer', u'bike-components.de')

            yield loader.load_item()
