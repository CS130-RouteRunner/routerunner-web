"""Useful utility functions"""
from itertools import *


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks
    https://docs.python.org/2/library/itertools.html#recipes
    """
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)
