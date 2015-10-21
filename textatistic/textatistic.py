#-*- coding: utf-8 -*-
"""
Textatistic is a simple program, written in Python, to calculate common readability indices and text characteristics. Basic usage:

    >>> from textatistics import Textatistics
    >>> s = TextStatistic('There were a king with a large jaw and a queen with a plain face, on the throne of England; there were a king with a large jaw and a queen with a fair face, on the throne of France. In both countries it was clearer than crystal to the lords of the State preserves of loaves and fishes, that things in general were settled for ever.')
    
Full documentation at <http://www.erinhengel.com/software/textatistic>.

:copyright: (c) 2015 by Erin Hengel.
:license: Apache 2.0, see LICENSE for more details.
"""

import string
import re
import csv
from math import sqrt
from hyphen import Hyphenator


class EasyWordList(object):
    """Object containing Dale-Chall list of easy words."""
    
    def __init__(self, file='./dale_chall.txt'):
        self.list = open(file, 'r').read().splitlines()
        
class Abbreviations(object):
    """Object containing abbreviations & their replacements."""
    
    def __init__(self, file='./abbreviations.txt', append=None, modify=None, remove=None):
        with open(file, 'r') as fh:
            self.list = list(csv.reader(fh))
        if append:
            self.list = self.list + append
        if modify:
            for item in modify:
                index = int(list(sum(self.list, [])).index(item[0]) / 2)
                self.list[index] = item
        if remove:
            for item in remove:
                self.list.remove(item)


class Textatistic(object):
    """Object containing every text statistic and readability score."""
    def __init__(self, text, replacements=Abbreviations(), hyphen=Hyphenator('en_US'), easy_words=EasyWordList()):
            
        text = punct_clean(text, replacements)
        self.sent_count = sent_count(text, replacements, True)
        self.char_count = char_count(text, replacements, True)
        
        text = word_array(text, replacements, True)
        self.word_count = word_count(text, replacements, True)
        self.dale_chall_list_count = dale_chall_list_count(text, replacements, easy_words, True)
        
        sybl_list = sybl_count(text, replacements, hyphen, True)
        self.sybl_count = sybl_list['sybl_count']
        self.poly_sybl_word_count = sybl_list['poly_sybl_word_count']
        
        self.counts = {
            'word': self.word_count,
            'sentence': self.sent_count,
            'syllable': self.sybl_count,
            'dale_chall_list': self.dale_chall_list_count,
            'poly_sybl_word': self.poly_sybl_word_count
        }
        
        self.flesch = flesch(vars=self.counts)
        self.flesch_kincaid = flesch_kincaid(vars=self.counts)
        self.gunning_fog = gunning_fog(vars=self.counts)
        self.smog = smog(vars=self.counts)
        self.dale_chall = dale_chall(vars=self.counts)
        
        self.scores = {
            'flesch': self.flesch,
            'flesch_kincaid': self.flesch_kincaid,
            'gunning_fog': self.gunning_fog,
            'smog': self.smog,
            'dale_chall': self.dale_chall
        }
    
    def dict(self):
        return self.__dict__
        
def dash_clean(text):
    """Replace em, en, etc. dashes with hypens."""
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    return text
    
def hyphen_single(text, prepped=False):
    """Remove hyphen in hyphenated single word, e.g., co-author."""
    if not prepped:
        text = dash_clean(text)
    text = text.replace("co-", "co")
    text = text.replace("Co-", "Co")
    return text


def decimal_strip(text):
    """Remove decimals and replace with +."""
    return re.sub("\.([0-9])", "+\\1", text)
    

def nonend_strip(text):
    """Remove punctuation used in an obvious mid-sentence rhetorical manner."""
    text = re.sub(r'[\?!]+\)[\.\?!]+', ').', text)
    text = re.sub(r'[\?!]+\)\s*[\-]+', ') -', text)
    return text


def abbrv_strip(text, replacements=Abbreviations()):
    """Replace abbreviations with their full text per abbreviations.txt."""
    for item in replacements.list:
        if item[0][:2] in ["r'", 'r"']:
            text = re.compile(item[0][2:-1]).sub(item[1], text)
        else:
            text = text.replace(*item)
    return text


def punct_clean(text, replacements=Abbreviations()):
    """Apply all punctuation cleaning functions."""
    text = dash_clean(text)
    text = hyphen_single(text, prepped=True)
    text = decimal_strip(text)
    text = nonend_strip(text)
    return abbrv_strip(text, replacements)
    
    
def word_array(text, replacements=Abbreviations(), prepped=False):
    """Generate list of words in text."""
    if not prepped:
        text = punct_clean(text, replacements)
    return text.replace("-", ' ').translate(str.maketrans("", "", string.punctuation)).split()
    

def sent_count(text, replacements=Abbreviations(), prepped=False):
    """Count number of sentences in text."""
    if not prepped:
        text = punct_clean(text, replacements)
    return text.count('.') + text.count('!') + text.count('?')


def char_count(text, replacements=Abbreviations(), prepped=False):
    if not prepped:
        text = punct_clean(text, replacements)
    return len(''.join(text.split()))


def word_count(text, replacements=Abbreviations(), prepped=False):
    """Count number of words in text."""
    if not prepped:
        text = word_array(punct_clean(text, replacements), replacements, prepped=True)
    return len(text)


def dale_chall_list_count(text, replacements=Abbreviations(), easy_words=EasyWordList(), prepped=False):
    """Count number of words on Dale-Chall list."""
    if not prepped:
        text = word_array(punct_clean(text, replacements), replacements, True)
    difficult = 0
    for word in text:
        word = word.lower()
        try:
            float(word)
        except ValueError:
            try:
                easy_words.list.index(word)
            except ValueError:
                difficult += 1
    return difficult


def syblperword_count(word, hyphen=Hyphenator('en_US')):
    """Count number of syllables in a word."""
    return max(1, len(hyphen.syllables(word)))


def sybl_count(text, replacements=Abbreviations(), hyphen=Hyphenator('en_US'), prepped=False):
    """Count number of syllables in text, return in sybl_count;
    Count number of words with three or more syllables, return
    in poly_sybl_word_count.
    """
    if not prepped:
        text = word_array(punct_clean(text, replacements), replacements, True)
    sybl_count = 0
    poly_sybl_word_count = 0
    for word in text:
        syblperword_c = syblperword_count(word, hyphen)
        sybl_count += syblperword_c
        if syblperword_c >= 3: poly_sybl_word_count += 1
    return {'sybl_count': sybl_count, 'poly_sybl_word_count': poly_sybl_word_count}


def flesch(text=None, replacements=None, hyphen=None, vars={}):
    """Calculate Flesch Reading Ease score."""
    if text:
        if not replacements:
            replacements = Abbreviations()
        if not hyphen:
            hyphen = Hyphenator('en_US')        
        text = punct_clean(text, replacements)
        vars['sentence'] = sent_count(text, replacements, True)
        text = word_array(text, replacements, True)
        vars['word'] = word_count(text, replacements, True)
        vars['syllable'] = sybl_count(text, replacements, hyphen, True)['sybl_count']
    return 206.835 - 1.015 * (vars['word'] / vars['sentence']) - 84.6 * (vars['syllable'] / vars['word'])


def flesch_kincaid(text=None, replacements=None, hyphen=None, vars={}):
    """Calculate Flesch-Kincaid score."""
    if text:
        if not replacements:
            replacements = Abbreviations()
        if not hyphen:
            hyphen = Hyphenator('en_US')        
        text = punct_clean(text, replacements)
        vars['sentence'] = sent_count(text, replacements, True)
        text = word_array(text, replacements, True)
        vars['word'] = word_count(text, replacements, True)
        vars['syllable'] = sybl_count(text, replacements, hyphen, True)['sybl_count']
    return 0.39 * (vars['word'] / vars['sentence']) + 11.8 * (vars['syllable'] / vars['word']) - 15.59
    
    
def gunning_fog(text=None, replacements=None, hyphen=None, vars={}):
    """Calculate Gunning Fog score."""
    if text:
        if not replacements:
            replacements = Abbreviations()
        if not hyphen:
            hyphen = Hyphenator('en_US')        
        text = punct_clean(text, replacements)
        vars['sentence'] = sent_count(text, replacements, True)
        text = word_array(text, replacements, True)
        vars['word'] = word_count(text, replacements, True)
        vars['poly_sybl_word'] = sybl_count(text, replacements, hyphen, True)['poly_sybl_word_count']
    return 0.4 * ((vars['word'] / vars['sentence']) + 100 * (vars['poly_sybl_word'] / vars['word']))
    
    
def smog(text=None, replacements=None, hyphen=None, vars={}):
    """Calculate SMOG score."""
    if text:
        if not replacements:
            replacements = Abbreviations()
        if not hyphen:
            hyphen = Hyphenator('en_US')
        text = punct_clean(text, replacements)
        vars['sentence'] = sent_count(text, replacements, True)
        text = word_array(text, replacements, True)
        vars['poly_sybl_word'] = sybl_count(text, replacements, hyphen, True)['poly_sybl_word_count']
    return 1.0430 * sqrt(vars['poly_sybl_word'] * (30 / vars['sentence'])) + 3.1291
    
    
def dale_chall(text=None, replacements=None, easy_words=None, vars={}):
    """Calculate Dale-Chall score."""
    if text:
        if not replacements:
            replacements = Abbreviations()
        if not easy_words:
            easy_words = EasyWordList()
        text = punct_clean(text, replacements)
        vars['sentence'] = sent_count(text, replacements, True)
        text = word_array(text, replacements, True)
        vars['word'] = word_count(text, replacements, True)
        vars['dale_chall_list'] = dale_chall_list_count(text, replacements, easy_words, True)
    cons = 0
    if vars['dale_chall_list'] / vars['word'] > 0.05:
        cons = 3.6365
    return cons + 15.79 * (vars['dale_chall_list'] / vars['word']) + 0.0496 * (vars['word'] / vars['sentence'])

