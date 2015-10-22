Textatistic
===========

``Textatistic`` is a Python package to calculate the `Flesch Reading Ease <https://en.wikipedia.org/wiki/Flesch–Kincaid_readability_tests>`_, `Flesch-Kincaid <https://en.wikipedia.org/wiki/Flesch–Kincaid_readability_tests>`_, `Gunning Fog <https://en.wikipedia.org/wiki/Gunning_fog_index>`_, `Simple Measure of Gobbledygook <https://en.wikipedia.org/wiki/SMOG>`_ (SMOG) and `Dale-Chall <http://www.readabilityformulas.com/new-dale-chall-readability-formula.php>`_ readability indices. Additionally, it contains functions to count the number of sentences, characters, syllables and words, words with three or more syllables and words on an expanded Dale-Chall list of easy words.

Documentation
-------------

Detailed documentation available at `erinhengel.com <http://www.erinhengel.com/software/textatistic/>`_. Source code on `GitHub.com <https://github.com/erinhengel/Textatistic>`_.

Installation
------------

To install Textatistic, simply:
	
.. code-block:: bash

	$ pip install textatistic

Quickstart
----------

.. code-block:: python

	>>> from textatistic import Textatistic
	
	# Generate object with all readability statistics.
	>>> text = 'There was a king with a large jaw. There was a queen with a plain face.'
	>>> s = Textatistic(text)
	
	# Return sentence count.
	>>> s.sent_count
	2
	
	# Return Flesch Reading Ease.
	>>> s.flesch
	114.11500000000001
	
	# Return dictionary of all attribute values.
	>>> s.dict()
	...
	

Textatistic attributes
----------------------


+------------------------+-----------------------------------------------------------------------+ 
| Attribute              | Function                                                              | 
+========================+=======================================================================+ 
| ``dash_clean``         | replace em, en, etc. dashes with hyphens.                             | 
+------------------------+-----------------------------------------------------------------------+ 
| ``hyphen_single``      | remove hyphen in hyphenated single word, e.g., co-author.             | 
+------------------------+-----------------------------------------------------------------------+ 
| ``decimal_strip``      | remove decimals and replace with plus sign (+).                       | 
+------------------------+-----------------------------------------------------------------------+ 
| ``nonend_strip``       | remove punctuation used in an obvious mid-sentence rhetorical manner. | 
+------------------------+-----------------------------------------------------------------------+ 
| ``abbrv_strip``        | replace abbreviations with their full text.                           | 
+------------------------+-----------------------------------------------------------------------+ 
| ``punct_clean``        | apply all punctuation cleaning functions.                             | 
+------------------------+-----------------------------------------------------------------------+ 
| ``word_array``         | generate list of words.                                               | 
+------------------------+-----------------------------------------------------------------------+
| ``sent_count``         | count number of sentences.                                            | 
+------------------------+-----------------------------------------------------------------------+
| ``char_count``         | count number of non-space characters.                                 | 
+------------------------+-----------------------------------------------------------------------+
| ``word_count``         | count number of words.                                                | 
+------------------------+-----------------------------------------------------------------------+
| ``dalechall_count``    | count number of words on Dale-Chall list.                             | 
+------------------------+-----------------------------------------------------------------------+
| ``syblperword_count``  | count number of syllables in a word.                                  | 
+------------------------+-----------------------------------------------------------------------+
| ``sybl_count``         | count number of syllables.                                            | 
+------------------------+-----------------------------------------------------------------------+
| ``polysyblword_count`` | calculate the Flesch Reading Ease score.                              | 
+------------------------+-----------------------------------------------------------------------+
| ``flesch_kincaid``     | calculate the Flesch-Kincaid score.                                   | 
+------------------------+-----------------------------------------------------------------------+
| ``gunning_fog``        | alculate the Gunning Fog score.                                       | 
+------------------------+-----------------------------------------------------------------------+



- ````: 
- ````: 
- ````: 
- ````: c
- ``smog``: calculate the SMOG score.
- ``dale_chall``: calculate the Dale-Chall score.
