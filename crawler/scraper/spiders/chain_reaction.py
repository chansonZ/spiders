from scrapy.contrib.spiders import CrawlSpider


class ChainReaction(CrawlSpider):
    name = 'chain-reaction'
    start_urls = 'http://www.chainreactioncycles.com/de/de/s?q=fulcrum'
    allowed_domain = 'chainreactioncycles.com'

    def parse_product(self, response):
        pass