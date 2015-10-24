Textatistic
===========

Textatistic is a Python package to calculate the `Flesch Reading Ease <https://en.wikipedia.org/wiki/Flesch–Kincaid_readability_tests>`_, `Flesch-Kincaid <https://en.wikipedia.org/wiki/Flesch–Kincaid_readability_tests>`_, `Gunning Fog <https://en.wikipedia.org/wiki/Gunning_fog_index>`_, `Simple Measure of Gobbledygook <https://en.wikipedia.org/wiki/SMOG>`_ (SMOG) and `Dale-Chall <http://www.readabilityformulas.com/new-dale-chall-readability-formula.php>`_ readability indices. Textatistic also contains functions to count the number of sentences, characters, syllables, words, words with three or more syllables and words on an expanded Dale-Chall list of easy words.

Installation
------------
	
.. code-block:: bash

	$ pip install textatistic

Quickstart
----------

.. code-block:: python

	>>> from textatistic import Textatistic
	
	# Generate object of readability statistics.
	>>> text = 'There was a king with a large jaw. There was a queen with a plain face.'
	>>> s = Textatistic(text)
	
	# Return sentence count.
	>>> s.sent_count
	2
	
	# Return Flesch Reading Ease score.
	>>> s.flesch_score
	114.11500000000001
	
	# Return dictionary of character/word/syllable counts.
	>>> s.counts
	...
	
	# Return dictionary of readability scores.
	>>> s.scores
	...
	
	# Return dictionary of all attribute values.
	>>> s.dict()
	...


Table of attributes
+++++++++++++++++++

+-------------------------+-----------------------------------------------------------------------------------+ 
| ``char_count``          | number of non-space characters.                                                   | 
+-------------------------+-----------------------------------------------------------------------------------+
| ``notdalechall_count``  | number of words not on Dale-Chall list of words understood by 80% of 4th graders. | 
+-------------------------+-----------------------------------------------------------------------------------+
| ``polysyblword_count``  | number of words with three or more syllables.                                     | 
+-------------------------+-----------------------------------------------------------------------------------+
| ``sent_count``          | number of sentences.                                                              | 
+-------------------------+-----------------------------------------------------------------------------------+
| ``sybl_count``          | number of syllables.                                                              | 
+-------------------------+-----------------------------------------------------------------------------------+
| ``word_count``          | number of words.                                                                  | 
+-------------------------+-----------------------------------------------------------------------------------+
| ``dalechall_score``     | Dale-Chall score.                                                                 | 
+-------------------------+-----------------------------------------------------------------------------------+
| ``flesch_score``        | Flesch Reading Ease score.                                                        | 
+-------------------------+-----------------------------------------------------------------------------------+
| ``fleschkincaid_score`` | Flesch-Kincaid score.                                                             | 
+-------------------------+-----------------------------------------------------------------------------------+
| ``gunningfog_score``    | Gunning Fog score.                                                                | 
+-------------------------+-----------------------------------------------------------------------------------+
| ``smog_score``          | SMOG score.                                                                       | 
+-------------------------+-----------------------------------------------------------------------------------+

Documentation
-------------

Detailed documentation available at `erinhengel.com <http://www.erinhengel.com/software/textatistic/>`_. 
