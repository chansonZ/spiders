# -*- coding: utf-8 -*-
""" The spider for Bruegelmann (bruegelmann.de). """


from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as Extractor
from scrapy.selector import Selector
from datetime import datetime
from ..items import Review, Price, BruegelmannPriceLoader, ChainReactionReviewLoader, BruegelmannReviewLoader


RETAILER = 'Bruegelmann'
MANUFACTURER = 'Fulcrum'


# SCRAPING NOTES:
#
# The retailer Bruegelmann only has 15 Fulcrum products, all on the Fulcrum brand page.
# On individual product pages, there's no options or models to choose from and all the
# comments are there. In short, it's a straightforward scraping exercise.


class Bruegelmann(CrawlSpider):
    name = 'bruegelmann'
    allowed_domains = ['bruegelmann.de']
    start_urls = ['http://www.bruegelmann.de/fulcrum.html']
    rules = [Rule(Extractor(allow='bruegelmann.de/fulcrum-\w+'), callback='parse_product')]

    response = None
    selector = None
    item = None
    loader = None

    def _register(self, response):
        self.response = response
        self.selector = Selector(response=response)
        self.item = response.meta['item'] if 'item' in response.meta.keys() else Review()
        self.loader = BruegelmannReviewLoader(self.item, response=self.response)


class BruegelmannPrices(Bruegelmann):
    name = 'bruegelmann-prices'

    def parse_product(self, response):
        self.response = response

        selector = Selector(response=response)

        id_ = selector.xpath('//*[@id="ProductsInfo"]/span[2]/text()').extract()
        saving = selector.xpath('//*[@id="productPriceContainer"]/div[2]/div/span/text()').extract()
        price = selector.xpath('//*[@id="productPriceContainer"]/div[2]/span/text()').extract()
        name = selector.xpath('//*[@id="ProductsInfo"]/h1/text()').extract()

        return self.load(price, saving, id_, name)

    def load(self, price, saving, id_, name):
        loader = BruegelmannPriceLoader(item=Price(), response=self.response)

        loader.add_value('id', id_)
        loader.add_value('timestamp', datetime.now())
        loader.add_value('price', price)
        loader.add_value('saving', saving)
        loader.add_value('hash', RETAILER)
        loader.add_value('hash', name)
        loader.add_value('slug', name)
        loader.add_value('name', name)
        loader.add_value('retailer', RETAILER)
        loader.add_value('manufacturer', MANUFACTURER)

        return loader.load_item()


class BruegelmannReviews(Bruegelmann):
    name = 'bruegelmann-reviews'

    def _register(self, response):
        self.response = response
        self.selector = Selector(response=response)
        self.item = response.meta['item'] if 'item' in response.meta.keys() else Review()
        self.loader = ChainReactionReviewLoader(self.item, response=self.response)

    def parse_product(self, response):
        self._register(response)

        self.loader.add_value('slug', self.selector.re('productDisplayName="(.+?)"'))
        self.loader.add_value('name', self.selector.re('productDisplayName="(.+?)"'))
        self.loader.add_value('retailer', RETAILER)
        self.loader.add_value('manufacturer', MANUFACTURER)

        request = Request(response.url + '/reviews.djs?format=embeddedhtml', callback=self.parse_reviews)
        request.meta['item'] = self.loader.load_item()

        return request

    def parse_reviews(self, response):
        self._register(response)

        self.loader.add_value('review', 'review')
        self.loader.add_value('author', 'author')
        self.loader.add_value('date', 'date')

        return self.loader.load_item()