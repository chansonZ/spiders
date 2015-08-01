# -*- coding: utf-8 -*-
""" The spiders for Bruegelmann (www.bruegelmann.de). """

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
from lxml.html import fromstring

from ..items import Price
from ..utilities import UrlObject, count_me

MANUFACTURER = 'mavic'

_product_urls_xpath = '//a[contains(@class, "productLink")]/@href'
_manufacturer_id_xpath = '//*[@id="productListGallery"]/@data-manufacturerid'
_total_pages_xpath = '//*[@id="totalPages"]/@data-totalpages'


class Bruegelmann(Spider):
    name = 'www.bruegelmann.de'
    allowed_domains = [name]
    start_urls = ['http://' + name + '/' + MANUFACTURER + '.html']

    def __init__(self, *args, **kwargs):
        super(Bruegelmann, self).__init__(*args, **kwargs)
        self._requests = []

    def parse(self, response):
        select = Selector(response=response)

        product_urls = select.xpath(_product_urls_xpath).extract()
        max_page_scroll = int(select.xpath(_total_pages_xpath).extract()[0])
        manufacturer_id = select.xpath(_manufacturer_id_xpath).extract()[0]

        self._collect_requests(product_urls, self.parse_product)

        if max_page_scroll > 1:
            ajax_urls = list(self._build_ajax_urls(manufacturer_id, max_page_scroll))
            self._collect_requests(ajax_urls, self.parse_json)

        self.logger.debug('Total number of requests: %s', len(self._requests))
        return self._requests

    def parse_json(self, response):
        json = loads(response.body)

        # The json dict fails when keys are native strings: why?
        html_text = json[u'content']
        html_tree = fromstring(html_text)

        product_urls = html_tree.xpath(_product_urls_xpath)
        self.logger.debug('%s: %s products in the JSON object', response.url, len(product_urls))
        self._collect_requests(product_urls, self.parse_product)

    def _build_ajax_urls(self, manufacturer_id, max_page_scroll):
        query = {'intManufacturerId': manufacturer_id, 'totalPages': max_page_scroll}
        ajax_url = UrlObject(self.name).with_path('ajax/filter').with_params(query)

        for page_nb in range(1, max_page_scroll):
            page = {'intPage': page_nb}
            yield str(ajax_url.with_params(page))

    def _collect_requests(self, urls, callback):
        requests = [Request(callback=callback, url=url) for url in urls]
        self._requests.extend(requests)
        self.logger.debug('Built %s requests for %s', len(requests), callback.__name__)

    @count_me
    def parse_product(self, response):
        pass


class BruegelmannPrice(Bruegelmann):
    item = Price()


