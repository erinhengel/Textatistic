#!/usr/bin/python

from hyphen import Hyphenator, dict_info
import string
import re
import csv
from math import sqrt


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class EasyWordList(object):
    """Object containing Dale-Chall list of easy words."""
    
    def __init__(self, file='./dalechall.txt'):
        self.list = open(file, 'r').read().splitlines()
        
class TextReplacements(object):
    """Object containing abbreviations & their replacements."""
    
    def __init__(self, file='./abbreviations.txt'):
        with open(file, 'r') as fh:
            self.list = list(csv.reader(fh))


class TextStatistic(object):
    """Object containing every text statistic and readability score."""
    def __init__(self, text, easy_words=EasyWordList(), replacements=TextReplacements(), hyphen=Hyphenator('en_US')):
            
        text = period_strip(text, replacements)
        self.sentence_count = sentence_count(text, True)
        self.character_count = character_count(text, True)
        
        text = punct_strip(text)
        self.word_count = word_count(text, True)
        self.dalechall_count = dalechall_count(text, easy_words, True)
        
        syllable_list = syllable_counts(text, hyphen, True)
        self.syllable_count = syllable_list['syllable_count']
        self.polysyllableword_count = syllable_list['polysyllableword_count']
        
        params = {'word_c':self.word_count, 'sentence_c':self.sentence_count, 'syllable_c':self.syllable_count, 'dalechall_c': self.dalechall_count, 'polysyllableword_c':self.polysyllableword_count}
        self.flesch_score = flesch_score(vars=params)
        self.fleschkincaid_score = fleschkincaid_score(vars=params)
        self.fog_score = fog_score(vars=params)
        self.smog_score = smog_score(vars=params)
        self.dalechall_score = dalechall_score(vars=params)
    
    def dict(self):
        return self.__dict__


def abbrv_strip(text, replacements):
    for item in replacements.list:
        text = text.replace(*item)
        
    return text


def decimal_strip(text):
    return re.sub("\.[0-9]", "00", text)
    
    
def punct_strip(text):
    return text.replace("-", ' ').translate(str.maketrans("", "", string.punctuation)).split()


def period_strip(text, replacements):
    text = decimal_strip(text)
    return abbrv_strip(text, replacements)
    

def sentence_count(text, prepped=False):
    if not prepped: text = period_strip(text)
    return text.count('.') + text.count('!') + text.count('?')


def character_count(text, prepped=False):
    if not prepped: text = period_strip(text)
    return len(''.join(text.split()))


def word_count(text, prepped=False):
    if not prepped: text = punct_strip(period_strip(text))
    return len(text)


def dalechall_count(text, easy_words, prepped=False):
    if not prepped: text = punct_strip(period_strip(text))
    difficult = 0
    for word in text:
        word = word.lower()
        if not is_number(word):
            try:
                easy_words.list.index(word)
            except ValueError:
                difficult += 1
    return difficult


def syllableperword_count(word, hyphen):
    return max(1, len(hyphen.syllables(word)))


def syllable_counts(text, hyphen, prepped=False):
    if not prepped: text = punct_strip(period_strip(text))
    syllable_count = 0
    polysyllableword_count = 0
    for word in text:
        syllableperword_c = syllableperword_count(word, hyphen)
        syllable_count += syllableperword_c
        if syllableperword_c >= 3: polysyllableword_count += 1
    return {'syllable_count': syllable_count, 'polysyllableword_count': polysyllableword_count}


def flesch_score(text=None, hyphen=None, vars=None):
    if text:
        text = period_strip(text)
        vars['sentence_c'] = sentence_count(text, True)
        text = punct_strip(text)
        vars['word_c'] = word_count(text, True)
        vars['syllable_c'] = syllable_counts(text, hyphen, True)['syllable_count']

    return 206.835 - 1.015 * (vars['word_c'] / vars['sentence_c']) - 84.6 * (vars['syllable_c'] / vars['word_c'])


def fleschkincaid_score(text=None, hyphen=None, vars=None):
    if text:
        text = period_strip(text)
        vars['sentence_c'] = sentence_count(text, True)
        text = punct_strip(text)
        vars['word_c'] = word_count(text, True)
        vars['syllable_c'] = syllable_counts(text, hyphen, True)['syllable_count']

    return 0.39 * (vars['word_c'] / vars['sentence_c']) + 11.8 * (vars['syllable_c'] / vars['word_c']) - 15.59
    
    
def fog_score(text=None, hyphen=None, vars=None):
    if text:
        text = period_strip(text)
        vars['sentence_c'] = sentence_count(text, True)
        text = punct_strip(text)
        vars['word_c'] = word_count(text, True)
        vars['polysyllableword_c'] = syllable_counts(text, hyphen, True)['polysyllableword_count']

    return 0.4 * ((vars['word_c'] / vars['sentence_c']) + 100 * (vars['polysyllableword_c'] / vars['word_c']))
    
    
def smog_score(text=None, hyphen=None, vars=None):
    if text:
        text = period_strip(text)
        vars['sentence_c'] = sentence_count(text, True)
        text = punct_strip(text)
        vars['polysyllableword_c'] = syllable_counts(text, hyphen, True)['polysyllableword_count']

    return 1.0430 * sqrt(vars['polysyllableword_c'] * (30 / vars['sentence_c'])) + 3.1291
    
    
def dalechall_score(text=None, easy_words=None, vars=None):
    if text:
        text = period_strip(text)
        vars['sentence_c'] = sentence_count(text, True)
        text = punct_strip(text)
        vars['word_c'] = word_count(text, True)
        vars['dalechall_c'] = dalechall_count(text, easy_words, True)
    
    vars['cons'] = 0
    if vars['dalechall_c'] / vars['word_c'] > 0.05: vars['cons'] = 3.6365
        
    return vars['cons'] + 0.1579 * (vars['dalechall_c'] / vars['word_c']) * 100 + 0.0496 * (vars['word_c'] / vars['sentence_c'])

