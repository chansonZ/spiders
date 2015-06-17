""" This module defines the product item for all websites and
    specifies how we scrape each field on each website.
"""

from scrapy import Field, Item
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst

from .utilities import slugify, asciify, force_lower, strip_blanks
from .utilities import parse_price, parse_stock


class Product(Item):
    """ Product specifications. """

    name = Field()
    hash = Field()
    url = Field()
    id = Field()

    price = Field()
    vat = Field()
    currency = Field()

    retailer = Field()
    manufacturer = Field()

    timestamp = Field()
    stock = Field()


class ProductLoader(ItemLoader):
    """ Default product loader. """

    name_out = TakeFirst()
    hash_out = TakeFirst()
    url_out = TakeFirst()
    id_out = TakeFirst()
    price_out = TakeFirst()
    vat_out = TakeFirst()
    currency_out = TakeFirst()
    retailer_out = TakeFirst()
    manufacturer_out = TakeFirst()
    timestamp_out = TakeFirst()
    stock_out = TakeFirst()


class BikeComponentsProductLoader(ProductLoader):
    """ Product loader for bike-components.de. """

    name_in = MapCompose(strip_blanks, asciify, slugify, force_lower)
    hash_in = MapCompose(strip_blanks, asciify, slugify, force_lower)
    price_in = MapCompose(strip_blanks, parse_price)
    stock_in = MapCompose(parse_stock)
    id_in = MapCompose(strip_blanks)

    hash_out = Join(separator='-')
