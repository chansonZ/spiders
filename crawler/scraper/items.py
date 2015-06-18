""" This module specifies how we scrape each website. """

from scrapy import Field, Item
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst, Compose, Identity

from .utilities import slugify, asciify, force_lower, strip_blanks, squeeze_seperators
from .utilities import parse_price, parse_stock, trim_edges, SEPERATOR, parse_reviews

DEFAULT_OUTPUT_PROCESSOR = TakeFirst()


class Product(Item):
    name = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    model = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    slug = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    hash = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    url = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    id = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    price = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    retailer = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    manufacturer = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    timestamp = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    stock = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)


class Review(Item):
    text = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    date = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    author = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)
    rating = Field(output_processor=DEFAULT_OUTPUT_PROCESSOR)


class BikeComponentsProductLoader(ItemLoader):
    """ Product loader for bike-components.de. """

    name_in = MapCompose(strip_blanks)
    slug_in = MapCompose(strip_blanks, asciify, slugify, force_lower, squeeze_seperators, trim_edges)
    hash_in = MapCompose(strip_blanks, asciify, slugify, force_lower, squeeze_seperators, trim_edges)
    price_in = MapCompose(strip_blanks, parse_price)
    stock_in = MapCompose(parse_stock)
    id_in = MapCompose(strip_blanks)

    hash_out = Join(separator=SEPERATOR)
    reviews_out = Identity()