#-*- coding: utf-8 -*-

import string
import re
import csv
import os
from math import sqrt
from hyphen import Hyphenator


class EasyWords(object):
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
    
    def __init__(self, text, abbr=Abbreviations(), hyphen=Hyphenator('en_US'), easy=EasyWords()):
            
        text = punct_clean(text, abbr)
        self.sent_count = sent_count(text, abbr, True)
        self.char_count = char_count(text, abbr, True)
        
        text = word_array(text, abbr, True)
        self.word_count = word_count(text, abbr, True)
        self.notdalechall_count = notdalechall_count(text, abbr, easy, True)
        
        sybl_list = sybl_counts(text, abbr, hyphen, True)
        self.sybl_count = sybl_list['sybl_count']
        self.polysyblword_count = sybl_list['polysyblword_count']
        
        self.counts = {
            'char_count': self.char_count,
            'word_count': self.word_count,
            'sent_count': self.sent_count,
            'sybl_count': self.sybl_count,
            'notdalechall_count': self.notdalechall_count,
            'polysyblword_count': self.polysyblword_count
        }
        
        self.flesch_score = flesch_score(vars=self.counts)
        self.fleschkincaid_score = fleschkincaid_score(vars=self.counts)
        self.gunningfog_score = gunningfog_score(vars=self.counts)
        self.smog_score = smog_score(vars=self.counts)
        self.dalechall_score = dalechall_score(vars=self.counts)
        
        self.scores = {
            'flesch_score': self.flesch_score,
            'fleschkincaid_score': self.fleschkincaid_score,
            'gunningfog_score': self.gunningfog_score,
            'smog_score': self.smog_score,
            'dalechall_score': self.dalechall_score
        }
    
    def dict(self):
        dict = self.counts
        dict.update(self.scores)
        return dict


# Prepare text.

def punct_clean(text, abbr=Abbreviations()):
    """ 1. Replace em, en, etc. dashes with hyphens.
        2. Remove hyphens in hyphenated single words, e.g., co-author.
        3. Remove decimals and replace with a plus sign (+).
        4. Remove punctuation used in an obvious mid-sentence rhetorical manner.
        5. Replace abbreviations with their full text per abbr keyword.
    """
    
    # Replace em, en, etc. dashes with hyphens.
    text = text.replace("–", "-")
    text = text.replace("—", "-")    
    
    # Remove hyphens in hyphenated single words, e.g., co-author.
    text = text.replace("co-", "co")
    text = text.replace("Co-", "Co")
    
    # Remove decimals and replace with plus sign (+).
    text = re.sub("\.([0-9])", "+\\1", text)
    
    # Remove punctuation used in an obvious mid-sentence rhetorical manner.
    text = re.sub(r'[\?!]+\)[\.\?!]+', ').', text)
    text = re.sub(r'[\?!]+\)\s*[\-]+', ') -', text)
    
    # Replace abbreviations with their full text per abbr.
    for item in abbr.list:
        if item[0][:2] in ["r'", 'r"']:
            text = re.compile(item[0][2:-1]).sub(item[1], text)
        else:
            text = text.replace(*item)    
    return text


def word_array(text, abbr=Abbreviations(), prepped=False):
    """Generate list of words."""
    if not prepped:
        text = punct_clean(text, abbr)
    return text.replace("-", ' ').translate(str.maketrans("", "", string.punctuation)).split()


# Calculate text statistics.

def char_count(text, abbr=Abbreviations(), prepped=False):
    """Count number of non-space characters."""
    if not prepped:
        text = punct_clean(text, abbr)
    return len(''.join(text.split()))


def notdalechall_count(text, abbr=Abbreviations(), easy=EasyWords(), prepped=False):
    """Count number of words not on Dale-Chall list."""
    if not prepped:
        text = word_array(text, abbr)
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


def sent_count(text, abbr=Abbreviations(), prepped=False):
    """Count number of sentences."""
    if not prepped:
        text = punct_clean(text, abbr)
    return text.count('.') + text.count('!') + text.count('?')


def sybl_counts(text, abbr=Abbreviations(), hyphen=Hyphenator('en_US'), prepped=False):
    """Count number of syllables in text, return in sybl_count;
    count number of words with three or more syllables, return
    in polysyblword_count.
    """
    if not prepped:
        text = word_array(text, abbr)
    sybl_count = 0
    polysyblword_count = 0
    for word in text:
        syblperword_c = max(1, len(hyphen.syllables(word)))
        sybl_count += syblperword_c
        if syblperword_c >= 3: polysyblword_count += 1
    return {'sybl_count': sybl_count, 'polysyblword_count': polysyblword_count}


def word_count(text, abbr=Abbreviations(), prepped=False):
    """Count number of words."""
    if not prepped:
        text = word_array(text, abbr)
    return len(text)


# Calculate readability scores.

def dalechall_score(text=None, abbr=None, easy=None, vars={}):
    """Calculate Dale-Chall score."""
    if text:
        if not abbr:
            abbr = Abbreviations()
        if not easy:
            easy = EasyWords()
        text = punct_clean(text, abbr)
        vars['sent_count'] = sent_count(text, abbr, True)
        text = word_array(text, abbr, True)
        vars['word_count'] = word_count(text, abbr, True)
        vars['notdalechall_count'] = notdalechall_count(text, abbr, easy, True)
    if vars['notdalechall_count'] / vars['word_count'] > 0.05:
        cons = 3.6365
    else:
        cons = 0
    return cons + 15.79 * (vars['notdalechall_count'] / vars['word_count']) + 0.0496 * (vars['word_count'] / vars['sent_count'])


def flesch_score(text=None, abbr=None, hyphen=None, vars={}):
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


def fleschkincaid_score(text=None, abbr=None, hyphen=None, vars={}):
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
    return - 15.59 + 0.39 * (vars['word_count'] / vars['sent_count']) + 11.8 * (vars['sybl_count'] / vars['word_count'])


def gunningfog_score(text=None, abbr=None, hyphen=None, vars={}):
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


def smog_score(text=None, abbr=None, hyphen=None, vars={}):
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
    return 3.1291 + 1.0430 * sqrt(30 * (vars['polysyblword_count'] / vars['sent_count']))
