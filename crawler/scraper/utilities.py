# -*- coding: utf-8 -*-
""" This module contains useful text processing functions used by items loaders. """

from string import ascii_letters, digits
from re import match
from unicodedata import normalize


def slugify(dirty_string):
    return ''.join([c if c in ascii_letters+digits else '-' for c in dirty_string])


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

    text = u'    öüsdüjp&56%$/$/%")")oihdv 920707,08€   '
    print 'input text = %s' % text

    a = force_lower(text)
    print 'force_lower = %s' % a

    b = asciify(text)
    print 'asciify = %s' % b

    c = slugify(text)
    print 'slugify = %s' % c

    d = strip_blanks(text)
    print 'strip_whitespace = %s' % d

    price = u'300,08€'
    print 'input text = %s' % price

    e = parse_price(price)
    print 'parse_price = %s' % e

    out_of_stock = u'delivery period approx. 2-7 days'
    print 'out_of_stock = %s' % out_of_stock

    s = parse_stock(out_of_stock)
    print 'parse_stock = %s' % s

    in_stock = u'in stock'
    print 'in_stock = %s' % in_stock

    s = parse_stock(in_stock)
    print 'parse_stock = %s' % s


