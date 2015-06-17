""" Crawler for Bike Components (https://www.bike-components.de). """

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.exceptions import DropItem

from datetime import datetime

from ..items import Product, BikeComponentsProductLoader


class BikeComponents(CrawlSpider):
    name = 'bike-components'
    allowed_domains = ['bike-components.de']
    start_urls = ['https://www.bike-components.de/en/Fulcrum/']

    products = LxmlLinkExtractor(allow='/en/Fulcrum/\w+')
    next_page = LxmlLinkExtractor(allow='page=')

    rules = [Rule(products, callback='parse_product'), Rule(next_page)]

    def parse_product(self, response):
        """ Parse a product from Bike Components. One product may have multiple models,
            in which case each model is scraped """

        # Paths that point to a single node
        title_xpath = '//*[@id="module-product-item"]/div[3]/div[1]/h1/span'
        id_xpath = '//*[@id="module-product-item-description"]/span[1]/span'

        # Paths that point to multiple nodes
        prices_xpath_1 = '//*[@id="module-product-item-description"]/div/ul/li/span[2]'
        prices_xpath_2 = '//*[@id="module-product-item"]/div[3]/div[1]/div[2]/span'
        models_xpath = '//*[@id="module-product-item-description"]/div/ul/li/span[1]'
        stocks_xpath = '//*[@id="module-product-item-description"]/div/ul/li/span[3]'

        loader = BikeComponentsProductLoader(item=Product(), response=response)

        prices_1 = response.xpath(prices_xpath_1).extract()
        prices_2 = response.xpath(prices_xpath_2).extract()
        models = response.xpath(models_xpath).extract()
        stocks = response.xpath(stocks_xpath).extract()

        try:
            models = zip(prices_1, prices_2, models, stocks)
        except:
            raise DropItem('Cannot scrape: %s' % response.url)

        for price_1, price_2, model, stock in models:

            loader.add_value('price', price_1)
            loader.add_value('price', price_2)

            loader.add_value('hash', 'bike-components')
            loader.add_value('hash', 'fulcrum')
            loader.add_xpath('hash', title_xpath)
            loader.add_value('hash', model)

            loader.add_value('stock', stock)

            loader.add_xpath('id', id_xpath)

            loader.add_value('url', response.url)
            loader.add_value('timestamp', datetime.today())
            loader.add_value('manufacturer', 'Fulcrum')
            loader.add_value('retailer', 'bike-components.de')

            yield loader.load_item()
