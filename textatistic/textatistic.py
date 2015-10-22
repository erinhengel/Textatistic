#-*- coding: utf-8 -*-

import string
import re
import csv
import os
from math import sqrt
from hyphen import Hyphenator

def get_data(path):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

class EasyWordList(object):
    """Object containing Dale-Chall list of easy words."""
    
    def __init__(self, file=None):
        if not file:
            file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dale_chall.txt')
        self.list = open(file, 'r').read().splitlines()
        
class Abbreviations(object):
    """Object containing abbreviations & their replacements."""
    
    def __init__(self, file=None, append=None, modify=None, remove=None):
        if not file:
            file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'abbreviations.txt')
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
    
    def __init__(self, text, abbr=Abbreviations(), hyphen=Hyphenator('en_US'), easy=EasyWordList()):
            
        text = punct_clean(text, abbr)
        self.sent_count = sent_count(text, abbr, True)
        self.char_count = char_count(text, abbr, True)
        
        text = word_array(text, abbr, True)
        self.word_count = word_count(text, abbr, True)
        self.dalechall_count = dalechall_count(text, abbr, easy, True)
        
        sybl_list = sybl_counts(text, abbr, hyphen, True)
        self.sybl_count = sybl_list['sybl_count']
        self.polysyblword_count = sybl_list['polysyblword_count']
        
        self.counts = {
            'word_count': self.word_count,
            'sent_count': self.sent_count,
            'sybl_count': self.sybl_count,
            'dalechall_count': self.dalechall_count,
            'polysyblword_count': self.polysyblword_count
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
    """Replace em, en, etc. dashes with hyphens."""
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
    """Remove decimals and replace with plus sign (+)."""
    return re.sub("\.([0-9])", "+\\1", text)
    

def nonend_strip(text):
    """Remove punctuation used in an obvious mid-sentence rhetorical manner."""
    text = re.sub(r'[\?!]+\)[\.\?!]+', ').', text)
    text = re.sub(r'[\?!]+\)\s*[\-]+', ') -', text)
    return text


def abbrv_strip(text, abbr=Abbreviations()):
    """Replace abbreviations with their full text per abbreviations.txt."""
    for item in abbr.list:
        if item[0][:2] in ["r'", 'r"']:
            text = re.compile(item[0][2:-1]).sub(item[1], text)
        else:
            text = text.replace(*item)
    return text


def punct_clean(text, abbr=Abbreviations()):
    """Apply all punctuation cleaning functions."""
    text = dash_clean(text)
    text = hyphen_single(text, prepped=True)
    text = decimal_strip(text)
    text = nonend_strip(text)
    return abbrv_strip(text, abbr)
    
    
def word_array(text, abbr=Abbreviations(), prepped=False):
    """Generate list of words."""
    if not prepped:
        text = punct_clean(text, abbr)
    return text.replace("-", ' ').translate(str.maketrans("", "", string.punctuation)).split()
    

def sent_count(text, abbr=Abbreviations(), prepped=False):
    """Count number of sentences."""
    if not prepped:
        text = punct_clean(text, abbr)
    return text.count('.') + text.count('!') + text.count('?')


def char_count(text, abbr=Abbreviations(), prepped=False):
    """Count number of non-space characters."""
    if not prepped:
        text = punct_clean(text, abbr)
    return len(''.join(text.split()))


def word_count(text, abbr=Abbreviations(), prepped=False):
    """Count number of words."""
    if not prepped:
        text = word_array(punct_clean(text, abbr), abbr, prepped=True)
    return len(text)


def dalechall_count(text, abbr=Abbreviations(), easy=EasyWordList(), prepped=False):
    """Count number of words on Dale-Chall list."""
    if not prepped:
        text = word_array(punct_clean(text, abbr), abbr, True)
    difficult = 0
    for word in text:
        word = word.lower()
        try:
            float(word)
        except ValueError:
            try:
                easy.list.index(word)
            except ValueError:
                difficult += 1
    return difficult


def syblperword_count(word, hyphen=Hyphenator('en_US')):
    """Count number of syllables in a word."""
    return max(1, len(hyphen.syllables(word)))


def sybl_counts(text, abbr=Abbreviations(), hyphen=Hyphenator('en_US'), prepped=False):
    """Count number of syllables in text, return in sybl_count;
    count number of words with three or more syllables, return
    in polysyblword_count.
    """
    if not prepped:
        text = word_array(punct_clean(text, abbr), abbr, True)
    sybl_count = 0
    polysyblword_count = 0
    for word in text:
        syblperword_c = syblperword_count(word, hyphen)
        sybl_count += syblperword_c
        if syblperword_c >= 3: polysyblword_count += 1
    return {'sybl_count': sybl_count, 'polysyblword_count': polysyblword_count}


def flesch(text=None, abbr=None, hyphen=None, vars={}):
    """Calculate Flesch Reading Ease score."""
    if text:
        if not abbr:
            abbr = Abbreviations()
        if not hyphen:
            hyphen = Hyphenator('en_US')
        text = punct_clean(text, abbr)
        vars['sent_count'] = sent_count(text, abbr, True)
        text = word_array(text, abbr, True)
        vars['word_count'] = word_count(text, abbr, True)
        vars['sybl_count'] = sybl_counts(text, abbr, hyphen, True)['sybl_count']
    return 206.835 - 1.015 * (vars['word_count'] / vars['sent_count']) - 84.6 * (vars['sybl_count'] / vars['word_count'])


def flesch_kincaid(text=None, abbr=None, hyphen=None, vars={}):
    """Calculate Flesch-Kincaid score."""
    if text:
        if not abbr:
            abbr = Abbreviations()
        if not hyphen:
            hyphen = Hyphenator('en_US')
        text = punct_clean(text, abbr)
        vars['sent_count'] = sent_count(text, abbr, True)
        text = word_array(text, abbr, True)
        vars['word_count'] = word_count(text, abbr, True)
        vars['sybl_count'] = sybl_counts(text, abbr, hyphen, True)['sybl_count']
    return 0.39 * (vars['word_count'] / vars['sent_count']) + 11.8 * (vars['sybl_count'] / vars['word_count']) - 15.59
    
    
def gunning_fog(text=None, abbr=None, hyphen=None, vars={}):
    """Calculate Gunning Fog score."""
    if text:
        if not abbr:
            abbr = Abbreviations()
        if not hyphen:
            hyphen = Hyphenator('en_US')
        text = punct_clean(text, abbr)
        vars['sent_count'] = sent_count(text, abbr, True)
        text = word_array(text, abbr, True)
        vars['word_count'] = word_count(text, abbr, True)
        vars['polysyblword_count'] = sybl_counts(text, abbr, hyphen, True)['polysyblword_count']
    return 0.4 * ((vars['word_count'] / vars['sent_count']) + 100 * (vars['polysyblword_count'] / vars['word_count']))
    
    
def smog(text=None, abbr=None, hyphen=None, vars={}):
    """Calculate SMOG score."""
    if text:
        if not abbr:
            abbr = Abbreviations()
        if not hyphen:
            hyphen = Hyphenator('en_US')
        text = punct_clean(text, abbr)
        vars['sent_count'] = sent_count(text, abbr, True)
        text = word_array(text, abbr, True)
        vars['polysyblword_count'] = sybl_counts(text, abbr, hyphen, True)['polysyblword_count']
    return 1.0430 * sqrt(vars['polysyblword_count'] * (30 / vars['sent_count'])) + 3.1291
    
    
def dale_chall(text=None, abbr=None, easy=None, vars={}):
    """Calculate Dale-Chall score."""
    if text:
        if not abbr:
            abbr = Abbreviations()
        if not easy:
            easy = EasyWordList()
        text = punct_clean(text, abbr)
        vars['sent_count'] = sent_count(text, abbr, True)
        text = word_array(text, abbr, True)
        vars['word_count'] = word_count(text, abbr, True)
        vars['dalechall_count'] = dalechall_count(text, abbr, easy, True)
    cons = 0
    if vars['dalechall_count'] / vars['word_count'] > 0.05:
        cons = 3.6365
    return cons + 15.79 * (vars['dalechall_count'] / vars['word_count']) + 0.0496 * (vars['word_count'] / vars['sent_count'])

