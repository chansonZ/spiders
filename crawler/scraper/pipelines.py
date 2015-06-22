""" This module contains all the pipelines used after the scraping is done.
    See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html.
"""
from genericpath import isfile

from os import makedirs
from os.path import exists
from scrapy.exceptions import DropItem
from os.path import join
from csv import DictWriter, writer


ROOT_FOLDER = '/home/loic/code/wheels/output/wheel-prices'
CSV_FIELDS = ['timestamp', 'price', 'stock']
CSV_HEADER = ['slug', 'model', 'manufacturer', 'retailer', 'id', 'url']


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
        elif 'prices' in spider.name:
            if item['slug'] in self.slugs:
                raise DropItem(oops)
            else:
                self.slugs.add(item['slug'])
        return item


class DumpProductsWithoutReview(object):

    def __init__(self):
        pass

    @staticmethod
    def process_item(item, spider):
        if 'reviews' in spider.name:
            if 'review' not in item.keys():
                raise DropItem('No review for this product')
        return item


class SavePricesToFileTree(object):

    def __init__(self):
        self.file = str()
        self.path = str()
        self.item = None
        self.spider = None

    def process_item(self, item, spider):
        if 'prices' in spider.name:
            self._register(item, spider)
            if isfile(self._item_file):
                self._write_row()
            else:
                self._initialize()
                self.process_item(self.item, self.spider)
        return item

    def _register(self, item, spider):
        self.path = join(ROOT_FOLDER, item['retailer'], item['manufacturer'])
        self.file = item['slug'] + '.csv'
        self.item = item
        self.spider = spider

    @property
    def _item_file(self):
        return join(self.path, self.file)

    def _write_row(self):
        with open(self._item_file, 'a') as f:
            w = DictWriter(f, CSV_FIELDS)
            w.writerow(self._extract(CSV_FIELDS, self.item))

    def _initialize(self):
        if not exists(self.path):
            makedirs(self.path)
        self._write_header()

    def _write_header(self):
        with open(self._item_file, 'w') as f:
            w = writer(f, delimiter='=')
            for key, value in self._extract(CSV_HEADER, self.item).items():
                w.writerow([key, value])
            w = writer(f, delimiter=',')
            w.writerow(CSV_FIELDS)

    @staticmethod
    def _extract(keys, item):
        """ Extract a subset of a dictionary. """
        # Taken from http://code.activestate.com/recipes/115417-subset-of-a-dictionary/
        return reduce(lambda x, y: x.update({y[0]: y[1]}) or x, map(None, keys, map(item.get, keys)), {})
