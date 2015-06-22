""" This module specifies how we process each product on each website. """

from scrapy import Field, Item
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst, Identity

from .utilities import slugify, asciify, force_lower, strip_edges, squeeze_seperators, parse_rating, parse_date
from .utilities import parse_price, parse_stock, trim_edges, SLUG_DELIMITER, parse_author


DEFAULT_PROCESSORS = {'input_processor': Identity(),
                      'output_processor': TakeFirst()}


class Product(Item):
    name = Field(**DEFAULT_PROCESSORS)
    model = Field(**DEFAULT_PROCESSORS)
    slug = Field(**DEFAULT_PROCESSORS)
    hash = Field(**DEFAULT_PROCESSORS)
    url = Field(**DEFAULT_PROCESSORS)
    id = Field(**DEFAULT_PROCESSORS)
    retailer = Field(**DEFAULT_PROCESSORS)
    manufacturer = Field(**DEFAULT_PROCESSORS)


class Price(Product):
    price = Field(**DEFAULT_PROCESSORS)
    timestamp = Field(**DEFAULT_PROCESSORS)
    stock = Field(**DEFAULT_PROCESSORS)


class Review(Product):
    review = Field(**DEFAULT_PROCESSORS)
    date = Field(**DEFAULT_PROCESSORS)
    author = Field(**DEFAULT_PROCESSORS)
    rating = Field(**DEFAULT_PROCESSORS)


class ProductLoader(ItemLoader):
    id_in = MapCompose(strip_edges)
    name_in = MapCompose(strip_edges)
    slug_in = MapCompose(strip_edges, asciify, slugify, force_lower, squeeze_seperators, trim_edges)
    hash_in = MapCompose(strip_edges, asciify, slugify, force_lower, squeeze_seperators, trim_edges)
    hash_out = Join(separator=SLUG_DELIMITER)


class PriceLoader(ProductLoader):
    stock_in = MapCompose(parse_stock)
    price_in = MapCompose(strip_edges, parse_price)


class ReviewLoader(ProductLoader):
    review_in = MapCompose(strip_edges)
    rating_in = MapCompose(strip_edges, parse_rating)
    author_in = MapCompose(strip_edges, parse_author)
    date_in = MapCompose(strip_edges, parse_date)
