# -*- coding: utf-8 -*-
""" This module contains useful text processing functions used by items loaders. """

from string import ascii_letters, digits
from re import match, sub
from unicodedata import normalize

SEPERATOR = '-'


def parse_reviews(raw_reviews):
    return raw_reviews # [raw_reviews[i::3] for i in range(0, int(len(raw_reviews)/3))]


def trim_edges(input_string):
    return sub(r'^-|-$', '', input_string)


def squeeze_seperators(input_string):
    return sub('%s{2,}' % SEPERATOR, SEPERATOR, input_string)


def slugify(dirty_string):
    return ''.join([c if c in ascii_letters+digits else SEPERATOR for c in dirty_string])


def asciify(unicode_string):
    return normalize('NFKD', unicode_string).encode('ASCII', 'ignore')


def force_lower(input_string):
    return input_string.lower()


def parse_price(raw_price):
    return float(match(r'((\d+\.)*\d+,\d{2})', raw_price).group(0).replace('.', '').replace(',', '.'))


def strip_blanks(input_string):
    return input_string.strip()


def parse_stock(input_string):
    a = bool('in stock' in input_string)
    return a

if __name__ == '__main__':
    """ Test the module. """
    pass
