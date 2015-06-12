# -*- coding: utf-8 -*-
""" Define here the models for your scraped items. See http://doc.scrapy.org/en/latest/topics/items.html. """

from crawler import Field, Item


class Product(Item):
    manufacturer = Field()
    price = Field()
    date = Field()
    id = Field()
    retailer = Field()
    url = Field()

