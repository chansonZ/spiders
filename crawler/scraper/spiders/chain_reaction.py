# -*- coding: utf-8 -*-
""" The crawler for Chain Reaction (https://www.chainreactioncycles.com). """


from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as Extractor
from scrapy.selector import Selector
from datetime import datetime
from ..items import Review, Price, ChainReactionPriceLoader


class ChainReaction(CrawlSpider):
    name = 'chain-reaction'
    allowed_domains = ['chainreactioncycles.com']
    start_urls = ['http://www.chainreactioncycles.com/de/de/fulcrum']
    rules = [Rule(Extractor(allow='/de/fulcrum-\w+'), callback='parse_product'), Rule(Extractor(allow='page='))]
    response = None

    def parse_product(self, response):
        self.response = response
        selector = Selector(response=response)

        ids = selector.re('"skuId":"(\w+)"')
        savings = selector.re('"SAVE":"(\d+)%"')
        options = selector.re('"Option":"(.+?)"')
        prices = selector.re(r'"RP":".(\d+\.\d{2})"')
        name = selector.re('productDisplayName="(.+?)"')

        return self.load(prices, savings, ids, name[0], options)

    def load(self, *fields):
        pass


class ChainReactionPrices(ChainReaction):
    name = 'chain-reaction-prices'

    def load(self, prices, savings, ids, name, options):

        for price, saving, option in zip(prices, savings, options):
            loader = ChainReactionPriceLoader(item=Price(), response=self.response)

            loader.add_value('timestamp', datetime.now())
            loader.add_value('price', price)
            loader.add_value('saving', saving)
            loader.add_value('hash', 'Chain Reaction')
            loader.add_value('hash', name)
            loader.add_value('hash', option)
            loader.add_value('slug', name)
            loader.add_value('slug', option)
            loader.add_value('model', option)
            loader.add_value('name', name)
            loader.add_value('retailer', 'Chain Reaction')
            loader.add_value('manufacturer', 'Fulcrum')
            yield loader.load_item()


class ChainReactionReviews(ChainReaction):
    name = 'chain-reaction-reviews'