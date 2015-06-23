# -*- coding: utf-8 -*-
""" This module contains input processors for items loaders. """


from string import ascii_letters, digits
from re import match, sub
from time import strptime
from unicodedata import normalize
from datetime import datetime


slug_delimiter = '-'

_empty_string = ''
_multiple_delimiters = '%s{2,}' % slug_delimiter
_seperator_at_edges = r'^-|-$'
_author = r'(?P<author>^.+?)(?= on)'
_date = r'(?:.*)(?P<date>\d{2}\.\d{2}\.\d{4})'
_price = r'(?P<price>(\d+\.)*\d+,\d{2})'


def parse_stock(input_string):
    return bool('in stock' in input_string)

def parse_rating(rating_string):
    return int(rating_string[0])

def parse_author(author_and_date):
    return match(_author, author_and_date).group('author')

def parse_date(author_and_date):
    return datetime(*strptime(match(_date, author_and_date).group('date'), '%d.%m.%Y')[0:6])

def trim_edges(text):
    return sub(_seperator_at_edges, _empty_string, text)

def strip_edges(text):
    return text.strip()

def squeeze_seperators(input_string):
    return sub(_multiple_delimiters, slug_delimiter, input_string)

def slugify(text):
    return _empty_string.join([c if c in ascii_letters + digits else slug_delimiter for c in text])

def asciify(text):
    return text if isinstance(text, str) else normalize('NFKD', text).encode('ASCII', 'ignore')

def force_lower(text):
    return text.lower()

def parse_price(raw_price):
    return float(match(_price, raw_price).group('price').replace('.', _empty_string).replace(',', '.'))


if __name__ == '__main__':
    pass
