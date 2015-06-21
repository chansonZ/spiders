""" This module contains all the pipelines used after the scraping is done.
    See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html.
"""

from scrapy.exceptions import DropItem


class DumpPriceDuplicates(object):

    def __init__(self):
        self.slugs = set()

    def process_item(self, item, spider):
        # This filter is just for scraping prices
        if 'prices' not in spider.name:
            return item
        if item['slug'] in self.slugs:
            raise DropItem('This product is a duplicate')
        else:
            self.slugs.add(item['slug'])
            return item


class DumpProductsWithoutReview(object):

    def __init__(self):
        pass

    @staticmethod
    def process_item(item, spider):
        # This filter is just for scraping reviews
        if 'reviews' not in spider.name:
            return item
        if 'review' not in item.keys():
            raise DropItem('No review written for this product')
        return item