""" This module contains all the pipelines used after the scraping is done.
    See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html.
"""


from os import makedirs
from scrapy.exceptions import DropItem
from os.path import join
from csv import DictWriter


ROOT = '/home/loic/code/wheels/output/wheel-prices'
DIALECT = 'excel-tab'


class DumpDuplicates(object):

    def __init__(self):
        self.slugs = set()
        self.names = set()

    def process_item(self, item, spider):
        oops = 'This item is a duplicate'

        if 'reviews' in spider.name:
            if item['name'] in self.names:
                raise DropItem(oops)
            else:
                self.names.add(item['name'])
                return item
        elif 'prices' in spider.name:
            if item['slug'] in self.slugs:
                raise DropItem(oops)
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
        # This filter is for reviews only
        if 'reviews' not in spider.name:
            return item
        if 'review' not in item.keys():
            raise DropItem('No review written for this product')
        return item


class SavePricesInsideFileTree(object):

    def __init__(self):
        self.file = str()
        self.path = str()
        self.item = None
        self.spider = None

    def process_item(self, item, spider):
        if 'prices' in spider.name:
            self._register(item, spider)
            self._save()
        return item

    def _register(self, item, spider):
        self.path = join(ROOT, item['retailer'], item['manufacturer'])
        self.file = item['slug'] + '.csv'
        self.spider = spider
        self.item = item

    def _save(self):
        try:
            self._write()
        except IOError:
            self._initialize()
            self.process_item(self.item, self.spider)

    @property
    def _item(self):
        return join(self.path, self.file)

    def _write(self):
        with open(self._item, 'a') as f:
            w = DictWriter(f, self.item.keys(), dialect=DIALECT)
            w.writerow(self.item.items())

    def _initialize(self):
        makedirs(self.path)
        with open(self._item, 'w') as f:
            w = DictWriter(f, fieldnames=list(self.item.keys()), dialect=DIALECT)
            w.writeheader()

