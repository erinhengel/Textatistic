Textatistic
===========

Textatistic is a Python package to calculate the [Flesch Reading Ease], [Flesch-Kincaid], [Gunning Fog], [Simple Measure of Gobbledygook] (SMOG) and [Dale-Chall] readability indices. Additionally, it contains functions to count the number of sentences, characters, syllables and words, words with three or more syllables and words on an expanded Dale-Chall list of easy words.

Installation
------------

To install Textatistic, simply:
	
code-block:: bash
	$ pip install textatistic

Quickstart
----------

>>> from textatistic import Textatistic
>>> s = TextStatistic('There were a king with a large jaw and a queen with a plain face, on the throne of England; there were a king with a large jaw and a queen with a fair face, on the throne of France. In both countries it was clearer than crystal to the lords of the State preserves of loaves and fishes, that things in general were settled for ever.')
>>> s.dict()
	
List of functions
-----------------

- ``dash_clean``: replace em, en, etc. dashes with hyphens.
- ``hyphen_single``: remove hyphen in hyphenated single word, e.g., co-author.
- ``decimal_strip``: remove decimals and replace with plus sign (+).
- ``nonend_strip``: remove punctuation used in an obvious mid-sentence rhetorical manner.
- ``abbrv_strip``: replace abbreviations with their full text.
- ``punct_clean``: apply all punctuation cleaning functions.
- ``word_array``: generate list of words.
- ``sent_count``: count number of sentences.
- ``char_count``: count number of non-space characters.
- ``word_count``: count number of words.
- ``dalechall_count``: count number of words on Dale-Chall list.
- ``syblperword_count``: count number of syllables in a word.
- ``sybl_count``: count number of syllables.
- ``polysyblword_count``: count number of words with three or more syllables.
- ``flesch``: calculate the [Flesch Reading Ease] score.
- ``flesch_kincaid``: calculate the [Flesch-Kincaid] score.
- ``gunning_fog``: calculate the [Gunning Fog] score.
- ``smog``: calculate the [SMOG] score.
- ``dale_chall``: calculate the [Dale-Chall] score.

Documentation
-------------

Documentation is available at http://www.erinhengel.com/software/textatistic/.
