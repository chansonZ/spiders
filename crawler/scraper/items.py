# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item
from datetime import datetime


class Product(Item):
    date = datetime.today()
    description = Field()
    price = Field()


