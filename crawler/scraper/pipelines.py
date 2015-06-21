""" This module contains all the pipelines used after the scraping is done.
    See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html.
"""

from scrapy.exceptions import DropItem


class DumpDuplicates(object):

    def __init__(self):
        self.slugs = set()
        self.names = set()

    def process_item(self, item, spider):
        if 'reviews' in spider.name:
            if item['name'] in self.names:
                raise DropItem('This item is a duplicate')
            else:
                self.names.add(item['name'])
                return item
        elif 'prices' in spider.name:
            if item['slug'] in self.slugs:
                raise DropItem('This item is a duplicate')
            else:
                self.slugs.add(item['slug'])
                return item
        else:
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
