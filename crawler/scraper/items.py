""" This module defines the product item for all websites and
    specifies how we scrape each field on each website.
"""

from scrapy import Field, Item
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst, Compose, Identity

from w3lib.html import remove_tags

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
    """ Generic product loader. """
    pass


class BikeComponentsProductLoader(ProductLoader):
    """ Product loader for the bike-components.de store. """

    name_in = Compose(remove_tags, strip_blanks, asciify, slugify, force_lower)
    name_out = Identity()

    hash_in = MapCompose(remove_tags, strip_blanks, asciify, slugify, force_lower)
    hash_out = Join(separator='-')

    id_in = MapCompose(remove_tags)

    price_in = MapCompose(remove_tags, strip_blanks, parse_price)
    price_out = TakeFirst()

    stock_in = MapCompose(parse_stock)
    stock_out = Identity()
