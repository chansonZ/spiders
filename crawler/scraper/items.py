""" This module specifies how we process the fields that we scrape. """


from scrapy import Field, Item
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst, Identity
from .utilities import slugify, asciify, force_lower, strip_edges, squeeze_seperators, parse_rating, parse_date
from .utilities import parse_price, parse_stock, trim_edges, parse_author, SLUG_SEPERATOR


_default_processors = {'input_processor': Identity(), 'output_processor': TakeFirst()}
_sanitize = [strip_edges, asciify, slugify, force_lower, squeeze_seperators, trim_edges, str]


################################################################
# Generic processors

class Product(Item):
    name = Field(**_default_processors)
    model = Field(**_default_processors)
    slug = Field(**_default_processors)
    hash = Field(**_default_processors)
    url = Field(**_default_processors)
    id = Field(**_default_processors)
    retailer = Field(**_default_processors)
    manufacturer = Field(**_default_processors)

class Price(Product):
    price = Field(**_default_processors)
    timestamp = Field(**_default_processors)
    stock = Field(**_default_processors)
    saving = Field(**_default_processors)

class Review(Product):
    review = Field(**_default_processors)
    date = Field(**_default_processors)
    author = Field(**_default_processors)
    rating = Field(**_default_processors)


################################################################
# Processors for bike-components.de

class BikeComponentsLoader(ItemLoader):
    model_in = MapCompose(asciify, str)
    id_in = MapCompose(strip_edges, asciify, str)
    name_in = MapCompose(strip_edges, unicode)
    slug_in = MapCompose(*_sanitize)
    hash_in = MapCompose(*_sanitize)
    hash_out = Join(separator=SLUG_SEPERATOR)
    retailer_in = MapCompose(*_sanitize)
    manufacturer_in = MapCompose(*_sanitize)


class BikeComponentsPriceLoader(BikeComponentsLoader):
    stock_in = MapCompose(parse_stock, bool)
    price_in = MapCompose(strip_edges, parse_price, float)


class BikeComponentsReviewLoader(BikeComponentsLoader):
    review_in = MapCompose(strip_edges, unicode)
    rating_in = MapCompose(strip_edges, parse_rating, int)
    author_in = MapCompose(strip_edges, parse_author, unicode)
    date_in = MapCompose(strip_edges, parse_date)


################################################################
# Processors for chainreactioncycles.com

class ChainReactionLoader(ItemLoader):
    model_in = MapCompose(asciify, str)
    id_in = MapCompose(asciify, str)
    name_in = MapCompose(unicode)
    slug_in = MapCompose(*_sanitize)
    slug_out = Join(separator=SLUG_SEPERATOR)
    hash_in = MapCompose(*_sanitize)
    hash_out = Join(separator=SLUG_SEPERATOR)
    retailer_in = MapCompose(*_sanitize)
    manufacturer_in = MapCompose(*_sanitize)


class ChainReactionPriceLoader(ChainReactionLoader):
    price_in = MapCompose(asciify, float)
    saving_in = MapCompose(asciify, float)


class ChainReactionReviewLoader(ChainReactionLoader):
    pass
