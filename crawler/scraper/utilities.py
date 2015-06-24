# -*- coding: utf-8 -*-
""" This module contains input processors for items loaders. """


from string import ascii_letters, digits
from re import match, sub
from time import strptime
from unicodedata import normalize
from datetime import datetime


SLUG_SEPERATOR = '-'

_multiple_seperators_regex = '%s{2,}' % SLUG_SEPERATOR
_edge_seperators_regex = r'^-|-$'
_author_regex = r'(?P<author>^.+?)(?= on)'
_date_regex = r'(?:.*)(?P<date>\d{2}\.\d{2}\.\d{4})'
_price_regex = r'(?P<price>(\d+\.)*\d+,\d{2})'


def parse_stock(input_string):
    return 'stock' in input_string.lower()

def parse_rating(rating_string):
    return rating_string[0]

def parse_author(author_and_date):
    return match(_author_regex, author_and_date).group('author')

def parse_date(author_and_date):
    return datetime(*strptime(match(_date_regex, author_and_date).group('date'), '%d.%m.%Y')[0:6])

def trim_edges(text):
    return sub(_edge_seperators_regex, '', text)

def strip_edges(text):
    return text.strip()

def squeeze_seperators(input_string):
    return sub(_multiple_seperators_regex, SLUG_SEPERATOR, input_string)

def slugify(text):
    return ''.join([c if c in ascii_letters + digits else SLUG_SEPERATOR for c in text])

def asciify(text):
    return text if isinstance(text, str) else normalize('NFKD', text).encode('ASCII', 'ignore')

def force_lower(text):
    return text.lower()

def parse_price(raw_price):
    return match(_price_regex, raw_price).group('price').replace('.', '').replace(',', '.')


if __name__ == '__main__':
    pass
