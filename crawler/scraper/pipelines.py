""" This module contains all the pipelines used after the scraping is done.
    See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html.
"""

from scrapy.exceptions import DropItem


class CheckDuplicates(object):

    def __init__(self):
        self.ids = set()

    def check_id(self, item, spider):
        if item['id'] in self.ids:
            raise DropItem('Duplicate item found for %s' % item['name'])
        else:
            self.ids.add(item['id'])
            return item


class CheckReview(object):

    def __init__(self):
        pass

    def check_review(self, item, spider):
        pass