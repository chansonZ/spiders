# -*- coding: utf-8 -*-
""" This module contains input processors for items loaders. """


from string import ascii_letters, digits
from re import match, sub
from time import strptime
from unicodedata import normalize
from datetime import datetime


NOTHING = ''
SLUG_DELIMITER = '-'
MULTIPLE_DELIMITERS = '%s{2,}' % SLUG_DELIMITER
SEPERATOR_AT_EDGES = r'^-|-$'

AUTHOR = r'(?P<author>^.+?)(?= on)'
DATE = r'(?:.*)(?P<date>\d{2}\.\d{2}\.\d{4})'
PRICE = r'(?P<price>(\d+\.)*\d+,\d{2})'


def parse_stock(input_string):
    return bool('in stock' in input_string)

def parse_rating(rating_string):
    return int(rating_string[0])

def parse_author(author_and_date):
    return match(AUTHOR, author_and_date).group('author')

def parse_date(author_and_date):
    return datetime(*strptime(match(DATE, author_and_date).group('date'), '%d.%m.%Y')[0:6])

def trim_edges(text):
    return sub(SEPERATOR_AT_EDGES, NOTHING, text)

def strip_edges(text):
    return text.strip()

def squeeze_seperators(input_string):
    return sub(MULTIPLE_DELIMITERS, SLUG_DELIMITER, input_string)

def slugify(text):
    return NOTHING.join([c if c in ascii_letters + digits else SLUG_DELIMITER for c in text])

def asciify(text):
    return text if isinstance(text, str) else normalize('NFKD', text).encode('ASCII', 'ignore')

def force_lower(text):
    return text.lower()

def parse_price(raw_price):
    return float(match(PRICE, raw_price).group('price').replace('.', NOTHING).replace(',', '.'))


if __name__ == '__main__':
    """ Test the module. """
    print(parse_date('lklk lrjkvfvfv.. on  hkfr 02.12.2344'))
