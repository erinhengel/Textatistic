#-*- coding: utf-8 -*-
"""
Textatistic is a simple program, written in Python, to calculate common
readability indices and text characteristics. Basic usage:

    >>> from textatistics import Textatistics
    >>> s = TextStatistic('A lot of text.')
    ...
    >>> s.counts
    ...
    >>> s.scores
    ...
    
Full documentation at <http://www.erinhengel.com/software/textatistic>.

:copyright: (c) 2015 by Erin Hengel.
:license: Apache 2.0, see LICENSE for more details.

"""

__title__ = 'textatistic'
__version__ = '0.1'
__author__ = 'Erin Hengel'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2015 Erin Hengel'

from .textatistic import *
