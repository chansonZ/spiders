# -*- coding: utf-8 -*-
""" The spiders for Bruegelmann (www.bruegelmann.de). """

# SCRAPING NOTES:
# ===============
#
# The retailer Bruegelmann lists products on a single page with infinite scrolling.
# Once the first batch of product urls is collected, we send additional json requests
# to collect the rest of them. The actual scraping happens once we land on individual
# product pages.

from collections import OrderedDict
from json import loads
from scrapy import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from lxml.html import fromstring

from ..items import Price
from ..utilities import Url, count_me


class Bruegelmann(Spider):
    name = 'www.bruegelmann.de'
    allowed_domains = [name]

    _product_urls_xpath = '//a[contains(@class, "productLink")]/@href'
    _manufacturer_id_xpath = '//*[@id="productListGallery"]/@data-manufacturerid'
    _total_pages_xpath = '//*[@id="totalPages"]/@data-totalpages'
    _total_products_xpath = '//*[@id="totalListProducts"]/span/text()'

    def __init__(self, manufacturer=None, *args, **kwargs):
        super(Bruegelmann, self).__init__(*args, **kwargs)

        if not manufacturer:
            raise ValueError('Please specify a manufacturer parameter.')

        self.manufacturer = manufacturer
        self.start_urls = ['http://' + self.name + '/' + manufacturer + '.html']

        self.max_page_scroll = None
        self.total_products = None
        self.manufacturer_id = None

        self._ajax_basket = set()

        self.logger.debug('Preparing the spider for %s products', manufacturer.upper())

    def parse(self, response):
        select = Selector(response=response)

        self.manufacturer_id = select.xpath(self._manufacturer_id_xpath).extract()[0]
        self.max_page_scroll = int(select.xpath(self._total_pages_xpath).extract()[0])
        self.total_products = int(select.xpath(self._total_products_xpath).extract()[0])

        self.logger.debug('Scraping %s products across 1 initial page + %s paginated pages',
                          self.total_products,
                          self.max_page_scroll)

        initial_products_urls = select.xpath(self._product_urls_xpath).extract()
        pagination_urls = list(self._build_ajax_urls())

        for product_url in initial_products_urls:
            yield Request(callback=self.parse_product, url=product_url)

        if self.max_page_scroll > 1:
            for page_nb, page_url in pagination_urls:
                yield Request(callback=self.parse_json, url=page_url, meta={'page_nb': page_nb})

    @count_me
    def parse_json(self, response):
        json = loads(response.body)
        html_text = json[u'content']
        html_tree = fromstring(html_text)
        product_urls = html_tree.xpath(self._product_urls_xpath)

        for product_url in product_urls:
            yield Request(callback=self.parse_product, url=product_url)

        self.logger.debug('Found %s products on page %s of %s',
                          len(product_urls),
                          response.meta['page_nb'],
                          self.max_page_scroll)

        if product_urls:
            self._ajax_basket.add(response.meta['page_nb'])

    def _build_ajax_urls(self):
        query = OrderedDict(intManufacturerId=self.manufacturer_id, intPage=None, totalPages=self.max_page_scroll)
        ajax_url = Url(self.name).with_path('ajax/filter').with_params(query)

        for page_nb in range(1, self.max_page_scroll + 1):
            page = {'intPage': page_nb}
            yield page_nb, str(ajax_url.with_params(page))

    @count_me
    def parse_product(self, response):
        pass

    def close(self, reason):
        self.logger.debug('Successful ajax calls to pages %s. Spider closed (%s)',
                          sorted(self._ajax_basket),
                          reason)


class BruegelmannPrice(Bruegelmann):
    pass


