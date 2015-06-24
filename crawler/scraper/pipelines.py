""" This module contains all the pipelines. See http://doc.scrapy.org/en/latest/topics/item-pipeline.html. """


from genericpath import isfile
from os import makedirs
from os.path import exists, dirname, abspath
from scrapy.exceptions import DropItem
from os.path import join
from csv import DictWriter, writer


class DumpDuplicates(object):

    def __init__(self):
        self.reviews = set()
        self.hashes = set()

    def process_item(self, item, spider):
        oops = 'This item is a duplicate'
        if 'reviews' in spider.name:
            if item['review'] in self.reviews:
                raise DropItem(oops)
            else:
                self.reviews.add(item['review'])
        elif 'prices' in spider.name:
            if item['hash'] in self.hashes:
                raise DropItem(oops)
            else:
                self.hashes.add(item['hash'])
        return item


class CheckMissingFields(object):

    def __init__(self):
        pass

    @staticmethod
    def process_item(item, spider):
        if 'reviews' in spider.name:
            if 'review' not in item.keys():
                raise DropItem('No review field for this product')
        elif 'prices' in spider.name:
            if 'hash' not in item.keys():
                raise DropItem('No hash field for this product')
            if 'slug' not in item.keys():
                raise DropItem('No slug field for this product')
            if 'retailer' not in item.keys():
                raise DropItem('No retailer field for this product')
            if 'manufacturer' not in item.keys():
                raise DropItem('No manufacturer field for this product')
        return item


class SavePricesToFileTree(object):

    _CSV_FIELDS = ['timestamp', 'price', 'stock']
    _CSV_HEADER = ['slug', 'model', 'manufacturer', 'retailer', 'id', 'url']
    _ROOT_DIR = abspath(join(dirname(__file__), '../..', 'output', 'wheel-prices'))

    def __init__(self):
        self.file = None
        self.path = None
        self.item = None

    def process_item(self, item, spider):
        if 'prices' in spider.name:
            self._register(item)
            if isfile(self._csv_file):
                self._write()
            else:
                self._initialize()
                self.process_item(item, spider)
        return item

    def _register(self, item):
        self.path = join(self._ROOT_DIR, item['retailer'], item['manufacturer'])
        self.file = item['slug'] + '.csv'
        self.item = item

    @property
    def _csv_file(self):
        return join(self.path, self.file)

    def _write(self):
        with open(self._csv_file, 'a') as f:
            w = DictWriter(f, self._CSV_FIELDS)
            w.writerow(self._squeeze_out(self._CSV_FIELDS, self.item))

    def _initialize(self):
        if not exists(self.path):
            makedirs(self.path)
        self._create_file()

    def _create_file(self):
        with open(self._csv_file, 'w') as f:
            w = writer(f, delimiter='=')
            for key, value in self._squeeze_out(self._CSV_HEADER, self.item).items():
                w.writerow([key, value])
            w = writer(f, delimiter=',')
            w.writerow(self._CSV_FIELDS)

    @staticmethod
    def _squeeze_out(subset_keys, item):
        """ Extract a subset of a dictionary. """
        # Taken from http://code.activestate.com/recipes/115417-subset-of-a-dictionary/
        return reduce(lambda x, y: x.update({y[0]: y[1]}) or x, map(None, subset_keys, map(item.get, subset_keys)), {})