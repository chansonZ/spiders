""" This module specifies how we scrape each website. """

from scrapy import Field, Item
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst, Compose

from .utilities import slugify, asciify, force_lower, strip_blanks, squeeze_seperators
from .utilities import parse_price, parse_stock, trim_edges, SEPERATOR


class Product(Item):
    """ Product specifications. """

    name = Field()
    model = Field()
    slug = Field()
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

    reviews = Field()


class ProductLoader(ItemLoader):
    """ Default product loader. """

    name_out = TakeFirst()
    model_out = TakeFirst()
    slug_out = TakeFirst()
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
    reviews_out = TakeFirst()


class BikeComponentsProductLoader(ProductLoader):
    """ Product loader for bike-components.de. """

    name_in = MapCompose(strip_blanks)
    slug_in = MapCompose(strip_blanks, asciify, slugify, force_lower, squeeze_seperators, trim_edges)
    hash_in = MapCompose(strip_blanks, asciify, slugify, force_lower, squeeze_seperators, trim_edges)
    price_in = MapCompose(strip_blanks, parse_price)
    stock_in = MapCompose(parse_stock)
    id_in = MapCompose(strip_blanks)
    reviews_in = MapCompose(strip_blanks)

    hash_out = Join(separator=SEPERATOR)
    reviews_out = Join(separator=SEPERATOR)