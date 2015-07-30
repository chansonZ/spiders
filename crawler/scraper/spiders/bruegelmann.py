# -*- coding: utf-8 -*-
""" The spiders for Bruegelmann (bruegelmann.de). """

# SCRAPING NOTES:
# ===============
#
# The retailer Bruegelmann lists products on a single page with infinite scrolling.
# Once the first batch of product urls is collected, we send additional json requests
# to collect the rest of them. The actual scraping happens once we land on individual
# product pages.


from json import loads
from scrapy import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from crawler.scraper.utitlities import UrlBuilder, counted
from lxml.html import fromstring

from ..items import Price


RETAILER = 'Bruegelmann'
MANUFACTURER = 'schwalbe'
WEBSITE = UrlBuilder('www.bruegelmann.de')

_product_url_xpath = '//a[contains(@class, "productLink")]/@href'
_manufacturer_id_xpath = '//*[@id="productListGallery"]/@data-manufacturerid'
_total_pages_xpath = '//*[@id="totalPages"]/@data-totalpages'


class Bruegelmann(Spider):
    name = 'bruegelmann'
    allowed_domains = [str(WEBSITE)]
    start_urls = [str(WEBSITE.with_path(MANUFACTURER + '.html'))]

    def parse(self, response):
        select = Selector(response=response)

        product_urls = select.xpath(_product_url_xpath).extract()
        self.visit_products(product_urls)

        total_pages = int(select.xpath(_total_pages_xpath).extract()[0])
        manufacturer_id = int(select.xpath(_manufacturer_id_xpath).extract()[0])

        query = {'intPage': None, 'intManufacturerId': manufacturer_id}
        ajax_url = WEBSITE.with_path('filter')

        for query['intPage'] in range(1, total_pages):
            yield Request(callback=self._collect_urls_from_json, url=str(ajax_url.with_params(query)))

    def visit_products(self, product_urls):
        for product_url in product_urls:
            yield Request(callback=self.parse_product, url=product_url)

    def _collect_urls_from_json(self, response):
        select = Selector(response=response)

        html_text = loads(select.response.body)
        html_tree = fromstring(html_text)
        product_urls = html_tree.xpath(_product_url_xpath)

        self.visit_products(product_urls)

    @counted
    def parse_product(self, response):
        pass


class BruegelmannPrice(Bruegelmann):
    item = Price()


