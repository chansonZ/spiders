""" This module has all the pipelines. See http://doc.scrapy.org/en/latest/topics/item-pipeline.html. """


from genericpath import isfile
from os import makedirs
from os.path import exists
from scrapy.exceptions import DropItem
from os.path import join
from csv import DictWriter, writer


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
    ROOT_FOLDER = '/home/loic/code/wheels/output/wheel-prices'
    CSV_FIELDS = ['timestamp', 'price', 'stock']
    CSV_HEADER = ['slug', 'model', 'manufacturer', 'retailer', 'id', 'url']

    def __init__(self):
        self.file = str()
        self.path = str()
        self.item = None

    def process_item(self, item, spider):
        if 'prices' in spider.name:
            self._register(item)
            if isfile(self._csv_file):
                self._write()
                return item
            else:
                self._initialize()
                self.process_item(item, spider)

    def _register(self, item):
        self.path = join(self.ROOT_FOLDER, item['retailer'], item['manufacturer'])
        self.file = item['slug'] + '.csv'
        self.item = item

    @property
    def _csv_file(self):
        return join(self.path, self.file)

    def _write(self):
        with open(self._csv_file, 'a') as f:
            w = DictWriter(f, self.CSV_FIELDS)
            w.writerow(self._squeeze_out(self.CSV_FIELDS, self.item))

    def _initialize(self):
        if not exists(self.path):
            makedirs(self.path)
        self._create_file()

    def _create_file(self):
        with open(self._csv_file, 'w') as f:
            # Write meta-info to header
            w = writer(f, delimiter='=')
            for key, value in self._squeeze_out(self.CSV_HEADER, self.item).items():
                w.writerow([key, value])
            # List column names.
            w = writer(f, delimiter=',')
            w.writerow(self.CSV_FIELDS)

    @staticmethod
    def _squeeze_out(subset_keys, item):
        """ Extract a subset of a dictionary. """
        # Taken from http://code.activestate.com/recipes/115417-subset-of-a-dictionary/
        return reduce(lambda x, y: x.update({y[0]: y[1]}) or x, map(None, subset_keys, map(item.get, subset_keys)), {})
