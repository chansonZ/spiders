from scrapy import Spider
from scraper.items import Product
from re import compile, match


def clean(text):
    junk = [r'\n', r'\r']

    for j in junk:
        pattern = compile(j)
        text = pattern.sub('', text)

    return text.strip()


class BikeComponents(Spider):
    name = 'bike-components'
    allowed_domains = ['bike-components.de']
    start_urls = ['https://www.bike-components.de/advanced_search_result.php?keywords=fulcrum']

    def parse(self, response):
        prices_xpath = '//*[@id="grid-content"]/div/div[2]/ul/li/a/span/text()'
        description_xpath = '//*[@id="grid-content"]/div/div[2]/ul/li/a/h2/text()'

        prices = response.xpath(prices_xpath).extract()
        descriptions = response.xpath(description_xpath).extract()

        product = Product()

        for price, description in zip(prices, descriptions):
            product['price'] = self.parse_price(price)
            product['description'] = self.parse_description(description)
            yield product

    @staticmethod
    def parse_price(raw_price):
        matched = match('(\d+,\d{2})', clean(raw_price))
        if matched:
            return float(matched.group(0).replace(',', '.'))
        else:
            return None

    @staticmethod
    def parse_description(raw_description):
        return clean(raw_description)


class ChainReaction():
    name = 'chain-reaction'
    start_urls = 'http://www.chainreactioncycles.com/de/de/s?q=fulcrum'
    allowed_domain = 'chainreactioncycles.com'

    def parse(self, response):
        prices_xpath = '//*[@id="grid-view"]/div[13]/div/div/ul/li[5]/span'
        descriptions_xpath = '//*[@id="grid-view"]/div[13]/div/div/ul/li[3]/a'

        prices = response.xpath(prices_xpath)
        descriptions = response.xpath(descriptions_xpath)

        product = Product()

        for price, description in zip(prices, descriptions):
