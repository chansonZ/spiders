""" This module specifies how we scrape each website. """

from scrapy import Field, Item
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst, Compose, Identity

from .utilities import slugify, asciify, force_lower, strip_blanks, squeeze_seperators
from .utilities import parse_price, parse_stock, trim_edges, SEPERATOR, parse_reviews

DEFAULT_PROCESSORS = {'output_processor': TakeFirst()}


class Product(Item):
    name = Field(**DEFAULT_PROCESSORS)
    model = Field(**DEFAULT_PROCESSORS)
    slug = Field(**DEFAULT_PROCESSORS)
    hash = Field(**DEFAULT_PROCESSORS)
    url = Field(**DEFAULT_PROCESSORS)
    id = Field(**DEFAULT_PROCESSORS)
    price = Field(**DEFAULT_PROCESSORS)
    retailer = Field(**DEFAULT_PROCESSORS)
    manufacturer = Field(**DEFAULT_PROCESSORS)
    timestamp = Field(**DEFAULT_PROCESSORS)
    stock = Field(**DEFAULT_PROCESSORS)


class Review(Item):
    text = Field(**DEFAULT_PROCESSORS)
    date = Field(**DEFAULT_PROCESSORS)
    author = Field(**DEFAULT_PROCESSORS)
    rating = Field(**DEFAULT_PROCESSORS)


class BikeComponentsProductLoader(ItemLoader):
    """ Product loader for bike-components.de. """

    name_in = MapCompose(strip_blanks)
    slug_in = MapCompose(strip_blanks, asciify, slugify, force_lower, squeeze_seperators, trim_edges)
    hash_in = MapCompose(strip_blanks, asciify, slugify, force_lower, squeeze_seperators, trim_edges)
    price_in = MapCompose(strip_blanks, parse_price)
    stock_in = MapCompose(parse_stock)
    id_in = MapCompose(strip_blanks)

    hash_out = Join(separator=SEPERATOR)


class BikeComponentsReviewLoader(ItemLoader):
    pass