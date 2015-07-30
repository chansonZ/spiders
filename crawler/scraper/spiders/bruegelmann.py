# -*- coding: utf-8 -*-
""" The spiders for Bruegelmann (bruegelmann.de). """

from json import loads
from scrapy import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from crawler.scraper.utitlities import UrlBuilder, counted
from lxml.html import fromstring

from ..items import BruegelmannLoader, Price


RETAILER = 'Bruegelmann'
MANUFACTURER = 'schwalbe'
WEBSITE = 'http://www.bruegelmann.de/'


_product_url_xpath = '//a[contains(@class, "productLink")]/@href'
_manufacturer_id_xpath = '//*[@id="productListGallery"]/@data-manufacturerid'
_total_pages_xpath = '//*[@id="totalPages"]/@data-totalpages'


# SCRAPING NOTES:
# ===============
#
# The retailer Bruegelmann lists products on a single page with infinite scrolling.
# Once the first batch of product urls is collected, we send additional json requests
# to collect the rest of them. The actual scraping happens once we land on individual
# product pages.


class Bruegelmann(Spider):
    name = 'bruegelmann'
    allowed_domains = ['bruegelmann.de']
    start_urls = [WEBSITE + MANUFACTURER + '.html']
    item = None
    item_loader = None

    def __init__(self, *args, **kwargs):
        super(Bruegelmann, self).__init__(*args, **kwargs)
        self.response = None
        self.select = None
        self.loader = None
        self.product_urls = None

    def _register(self, response):
        self.response = response
        self.select = Selector(response=response)
        self.loader = BruegelmannLoader(self.item, response=self.response)
        self.product_urls = []

    def parse(self, response):
        self._register(response)
        self.wtf()
        self._collect_base_page_urls()

        # self.logger.info('%s %s products found', MANUFACTURER, self.parse_product.called())

    def _collect_base_page_urls(self):
        product_urls = self.select.xpath(_product_url_xpath).extract()
        self.product_urls.extend(product_urls)
        self._scroll_n_collect_more_urls()

    def _collect_urls_from_json(self, response):
        self._register(response)
        html_text = loads(self.response.body)
        html_tree = fromstring(html_text)
        product_urls = html_tree.xpath(_product_url_xpath)
        self.product_urls.extend(product_urls)

    def visit_products(self):
        for product_url in self.product_urls:
            yield Request(callback=self.parse_product, url=product_url)

    def _scroll_n_collect_more_urls(self):
        total_pages = int(self.select.xpath(_total_pages_xpath).extract()[0])
        manufacturer_id = int(self.select.xpath(_manufacturer_id_xpath).extract()[0])

        query = {'intPage': None, 'intManufacturerId': manufacturer_id}
        ajax_url = UrlBuilder(WEBSITE).with_path('filter')

        for query['intPage'] in range(1, total_pages):
            yield Request(callback=self._collect_urls_from_json(), url=ajax_url.with_params(query))

    @counted
    def parse_product(self, response):
        pass

    def wtf(self):
        pass


class BruegelmannPrice(Bruegelmann):
    item = Price()


