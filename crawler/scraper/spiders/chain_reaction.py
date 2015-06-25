# -*- coding: utf-8 -*-
""" The crawler for Chain Reaction (https://www.chainreactioncycles.com). """


from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as Extractor
from scrapy.selector import Selector
from datetime import datetime
from ..items import Review, Price, ChainReactionPriceLoader, ChainReactionReviewLoader


RETAILER = 'Chain Reaction'
MANUFACTURER = 'Fulcrum'


class ChainReaction(CrawlSpider):
    name = 'chain-reaction'
    allowed_domains = ['chainreactioncycles.com']
    start_urls = ['http://www.chainreactioncycles.com/de/de/fulcrum']
    rules = [Rule(Extractor(allow='/de/fulcrum-\w+'), callback='parse_product'), Rule(Extractor(allow='page='))]

    response = None


class ChainReactionPrices(ChainReaction):
    name = 'chain-reaction-prices'

    def parse_product(self, response):
        self.response = response

        selector = Selector(response=response)

        ids = selector.re('"skuId":"(\w+)"')
        savings = selector.re('"SAVE":"(\d+)%"')
        options = selector.re('"Option":"(.+?)"')
        prices = selector.re(r'"RP":".(\d+\.\d{2})"')
        name = selector.re('productDisplayName="(.+?)"')

        items = self.load(prices, savings, ids, name[0], options)
        return items

    def load(self, prices, savings, ids, name, options):

        for price, saving, option, id_ in zip(prices, savings, options, ids):
            loader = ChainReactionPriceLoader(item=Price(), response=self.response)

            loader.add_value('id', id_)
            loader.add_value('timestamp', datetime.now())
            loader.add_value('price', price)
            loader.add_value('saving', saving)
            loader.add_value('hash', RETAILER)
            loader.add_value('hash', name)
            loader.add_value('hash', option)
            loader.add_value('slug', name)
            loader.add_value('slug', option)
            loader.add_value('model', option)
            loader.add_value('name', name)
            loader.add_value('retailer', RETAILER)
            loader.add_value('manufacturer', MANUFACTURER)

            yield loader.load_item()


class ChainReactionReviews(ChainReaction):
    name = 'chain-reaction-reviews'

    response = None
    selector = None
    item = None
    loader = None

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