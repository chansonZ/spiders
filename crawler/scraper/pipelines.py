""" This module contains all the pipelines used after the scraping is done.
    See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html.
"""

from scrapy.exceptions import DropItem


class DumpDuplicates(object):

    def __init__(self):
        self.id = set()

    def process_item_bla(self, item):
        if item['id'] in self.ids:
            raise DropItem('This product is a duplicate')
        else:
            self.ids.add(item['id'])
            return item


class DumpProductsWithoutReview(object):

    def __init__(self):
        pass

    @staticmethod
    def process_item(item, spider):
        if 'reviews' not in spider.name:
            return item
        if 'review' not in item.keys():
            raise DropItem('No review written for this product')
        return item