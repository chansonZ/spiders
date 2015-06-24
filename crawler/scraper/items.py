""" This module specifies how we process each product on each website. """


from scrapy import Field, Item
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst, Identity
from .utilities import slugify, asciify, force_lower, strip_edges, squeeze_seperators, parse_rating, parse_date
from .utilities import parse_price, parse_stock, trim_edges, parse_author, SLUG_SEPERATOR


#####################################################################################################################

_default_processors = {'input_processor': Identity(), 'output_processor': TakeFirst()}

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

#####################################################################################################################

class BikeComponentsLoader(ItemLoader):
    model_in = MapCompose(asciify)
    id_in = MapCompose(strip_edges, asciify)
    name_in = MapCompose(strip_edges)
    slug_in = MapCompose(strip_edges, asciify, slugify, force_lower, squeeze_seperators, trim_edges)
    hash_in = MapCompose(strip_edges, asciify, slugify, force_lower, squeeze_seperators, trim_edges)
    hash_out = Join(separator=SLUG_SEPERATOR)
    retailer_in = MapCompose(asciify)
    manufacturer_in = MapCompose(asciify)

class BikeComponentsPriceLoader(BikeComponentsLoader):
    stock_in = MapCompose(parse_stock)
    price_in = MapCompose(strip_edges, parse_price, float)

class BikeComponentsReviewLoader(BikeComponentsLoader):
    review_in = MapCompose(strip_edges)
    rating_in = MapCompose(strip_edges, parse_rating)
    author_in = MapCompose(strip_edges, parse_author)
    date_in = MapCompose(strip_edges, parse_date)

#####################################################################################################################

class ChainReactionLoader(ItemLoader):
    model_in = MapCompose(asciify)
    id_in = MapCompose(asciify)
    name_in = MapCompose()
    slug_in = MapCompose(asciify, slugify, force_lower, squeeze_seperators, trim_edges)
    slug_out = Join(separator=SLUG_SEPERATOR)
    hash_in = MapCompose(asciify, slugify, force_lower, squeeze_seperators, trim_edges)
    hash_out = Join(separator=SLUG_SEPERATOR)
    retailer_in = MapCompose(asciify)
    manufacturer_in = MapCompose(asciify)

class ChainReactionPriceLoader(ChainReactionLoader):
    price_in = MapCompose(asciify, float)
    saving_in = MapCompose(asciify, float)

class ChainReactionReviewLoader(ChainReactionLoader):
    pass
