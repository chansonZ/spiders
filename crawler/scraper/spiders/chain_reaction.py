# -*- coding: utf-8 -*-
""" The crawler for Bike Components (https://www.bike-components.de). """


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
    manufacturer = 'Fulcrum'
    retailer = name


class ChainReactionPrices(ChainReaction):
    name = 'chain-reaction-prices'

    def parse_product(self, response):
        s = Selector(response=response)

        prices = s.re(r'"RP":".(\d+\.\d{2})"')
        savings = s.re('"SAVE":"(\d+)%"')
        ids = s.re('"skuId":"(\w+)"')
        name = s.re('productDisplayName="(.+?)"')
        options = s.re('"Option":"(.+?)"')

        for price, saving, id_, option in zip(prices, savings, ids, options):
            l = ChainReactionPriceLoader(item=Price(), response=response)

            l.add_value('timestamp', datetime.now())
            l.add_value('price', price)
            l.add_value('saving', saving)
            l.add_value('hash', self.retailer)
            l.add_value('hash', name[0])
            l.add_value('hash', option)
            l.add_value('slug', name[0])
            l.add_value('slug', option)
            l.add_value('model', option)
            l.add_value('name', name[0])
            l.add_value('id', id_)
            l.add_value('retailer', self.retailer)
            l.add_value('manufacturer', self.manufacturer)

            yield l.load_item()

