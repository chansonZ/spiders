from scrapy import Spider
from ..items import Product
from re import compile, match


def clean(text):
    junk = [r'\n', r'\r']

    for j in junk:
        pattern = compile(j)
        text = pattern.sub('', text)

    return text.strip()


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
            pass