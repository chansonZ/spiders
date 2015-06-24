""" The crawler for Bike Components (https://www.bike-components.de). """


from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as Extractor
from scrapy.selector import Selector
from datetime import datetime
from ..items import BikeComponentsPriceLoader, BikeComponentsReviewLoader, Review, Price


class BikeComponents(CrawlSpider):
    allowed_domains = ['bike-components.de']
    start_urls = ['https://www.bike-components.de/en/Fulcrum/']
    rules = [Rule(Extractor(allow='/en/Fulcrum/\w+'), callback='parse_product'), Rule(Extractor(allow='page='))]
    manufacturer = 'Fulcrum'
    retailer = 'Bike Components'

class BikeComponentsReviews(BikeComponents):
    name = 'bike-components-reviews'

    def parse_product(self, response):
        loader = BikeComponentsReviewLoader(item=Review(), response=response)
        s = Selector(response=response)

        title = s.xpath('//div[@id="module-product-item"]/div[3]/div[1]/h1/span/text()').extract()
        ratings = s.xpath('//*[@id="module-product-reviews-list"]/div/div[2]/div/div[1]/span/text()').extract()
        dates = s.xpath('//*[@id="module-product-reviews-list"]/div/div[2]/div/span/text()').extract()
        authors = s.xpath('//*[@id="module-product-reviews-list"]/div/div[2]/div/span/text()').extract()
        reviews = s.xpath('//*[@id="module-product-reviews-list"]/div/div[2]/div/p/text()').extract()

        # A single product page may contain multiple reviews.
        # From a scraping point of view, each review is one item.
        for rating, date, author, review in zip(ratings, dates, authors, reviews):
            loader.add_value('name', title)
            loader.add_value('url', response.url)
            loader.add_value('manufacturer', self.manufacturer)
            loader.add_value('retailer', self.retailer)
            loader.add_value('rating', rating)
            loader.add_value('date', date)
            loader.add_value('author', author)
            loader.add_value('review', review)

            yield loader.load_item()


class BikeComponentsPrices(BikeComponents):
    name = 'bike-components-prices'

    def parse_product(self, response):
        l = BikeComponentsPriceLoader(item=Price(), response=response)
        s = Selector(response=response)

        title = s.xpath('//div[@id="module-product-item"]/div[3]/div[1]/h1/span/text()').extract()
        id_ = s.xpath('//div[@id="module-product-item-description"]/span[1]/span/text()').extract()
        prices_1 = s.xpath('//*[@id="module-product-item-description"]/div/ul/li/span[2]/text()').extract()
        prices_2 = s.xpath('//*[@id="module-product-item"]/div[3]/div[1]/div[2]/span/text()').extract()
        models = s.xpath('//*[@id="module-product-item-description"]/div/ul/li/span[1]/text()').extract()
        stocks = s.xpath('//*[@id="module-product-item-description"]/div/ul/li/span[3]/text()').extract()

        # A single product page may contain multiple models.
        # From a scraping point of view, each model is one item.
        for price_1, price_2, model, stock in zip(prices_1, prices_2, models, stocks):
            l.add_value('price', price_1)
            l.add_value('price', price_2)
            l.add_value('hash', self.manufacturer)
            l.add_value('hash', self.retailer)
            l.add_value('hash', title[0])
            l.add_value('hash', model)
            l.add_value('stock', stock)
            l.add_value('name', title[0])
            l.add_value('model', model)
            l.add_value('slug', title[0])
            l.add_value('id', id_[0])
            l.add_value('url', response.url)
            l.add_value('timestamp', datetime.now())
            l.add_value('manufacturer', self.manufacturer)
            l.add_value('retailer', self.retailer)

            yield l.load_item()
