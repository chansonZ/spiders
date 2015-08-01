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
        self.logger.debug('Preparing the spider for %s products', manufacturer.upper())
        self.start_urls = ['http://' + self.name + '/' + manufacturer + '.html']

        self.max_page_scroll = None
        self.total_products = None
        self.manufacturer_id = None

        self._ajax_basket = set()

    def parse(self, response):
        select = Selector(response=response)

        self.manufacturer_id = select.xpath(self._manufacturer_id_xpath).extract()[0]
        self.max_page_scroll = int(select.xpath(self._total_pages_xpath).extract()[0])
        self.total_products = int(select.xpath(self._total_products_xpath).extract()[0])

        self.logger.debug('Found %s products paginated across 1 landing page + %s paginated pages',
                          self.total_products,
                          self.max_page_scroll)

        initial_products = select.xpath(self._product_urls_xpath).extract()
        paginated_products = list(self._build_pagination())

        for product_url in initial_products:
            yield Request(callback=self.parse_product, url=product_url)

        if self.max_page_scroll > 1:
            for page_nb, ajax_url in paginated_products:
                yield Request(callback=self.parse_json,
                              url=ajax_url,
                              meta={'page_nb': page_nb})

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

    def _build_pagination(self):
        # The order of the query parameters seems to matter!
        query = {'intManufacturerId': self.manufacturer_id,
                 'intPage': None,
                 'totalPages': self.max_page_scroll}

        ajax_url = UrlObject(self.name).with_path('ajax/filter').with_params(query)

        for page_nb in range(1, self.max_page_scroll):
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


