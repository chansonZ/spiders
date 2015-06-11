""" This is the crawler and scraper for the Bike Components retailer at https://www.bike-components.de. """

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

from re import compile, match, search
from datetime import datetime

from ..items import Product


def clean(text):
    junk = ['\n', '\r', '/', ' ', '-Fulcrum|-fulcrum', '--']
    substitutes = ['', '', '-', '', '', '-']

    for j, s in zip(junk, substitutes):
        pattern = compile(j)
        text = pattern.sub(s, text)

    leading_non_alpha_numerical = compile('^[^a-zA-Z]+')
    text = leading_non_alpha_numerical.sub('', text).lower()

    return text.strip()


class BikeComponents(CrawlSpider):
    name = 'bike-components'
    allowed_domains = ['bike-components.de']
    start_urls = ['https://www.bike-components.de/en/Fulcrum/']

    products = LxmlLinkExtractor(allow='/en/Fulcrum/\w+')
    next_page = LxmlLinkExtractor(allow='page=')

    rules = [Rule(products, callback='parse_product'), Rule(next_page)]

    def parse_product(self, response):
        product = Product()

        prices_xpath = '//*[@id="module-product-item-description"]/div/ul/li/span[2]/text()'
        models_xpath = '//*[@id="module-product-item-description"]/div/ul/li/span[1]/text()'

        prices = response.xpath(prices_xpath).extract()
        models = response.xpath(models_xpath).extract()

        for price, model in zip(prices, models):
            product['price'] = self.parse_price(price)
            product['id'] = self.parse_id(response, model)
            product['retailer'] = 'bike-components'
            product['url'] = response.url
            product['date'] = datetime.today()
            yield product

    @staticmethod
    def parse_price(raw_price):
        matched = match(r'(\d+,\d{2})', raw_price)
        return float(matched.group(0).replace(',', '.'))

    def parse_id(self, response, raw_description):
        matched = search(r'/([^/]*)/$', response.url)
        model = matched.group(0)
        description = '-'.join([self.name, model, raw_description])
        return clean(description)