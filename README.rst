#### Motivation

Most programs that calculate readability scores rely on unclear, inconsistent and possibly inaccurate algorithms to count words, sentences and syllables and determine whether a word is on Dale-Chall's easy word list. Additionally, features of the text—particularly full stops used in abbreviations and decimals in numbers—frequently underestimate average words per sentence and syllables per word.

To transparently handle these issues and eliminate ambiguity in how the readability scores were calculated, I wrote the Python module `Textatistic` and released it under a Creative Commons license.

#### Installation

Install `Textatistic` with pip (possibly as root):

	$ pip install textatistic

`Textastistic` works with Python 3.4; I do not know if it works with earlier versions. If you have a Mac, Python 2.7 is pre-installed by default; upgrade at [python.org](http://www.python.org "python.org") and use `pip3` instead of `pip` during installation.

To install from source, download the latest version on [github.com](http://www.github.com "github.com") and run the following command (probably as root):

	$ python setup.py install

If you have more than one version of python installed, `python` may point to an earlier copy---definitely the case with Mac OS unless you've altered the command definition after installing Python 3.4. If so, replace `python` with `python3` above.

#### Quickstart

Begin by importing the Textatistic module:

	>>> from textatistic import Textatistic

The function `Textatistic` returns an object containing every text statistic and readability score `Textatistic` calculates. For example

	s = TextStatistic('There were a king with a large jaw and a queen with a plain face, on the throne of England; there were a king with a large jaw and a queen with a fair face, on the throne of France. In both countries it was clearer than crystal to the lords of the State preserves of loaves and fishes, that things in general were settled for ever.')

returns a `Textatistic` object I've named `s`. We can return all text statistics and readability scores using this object. For example, the following command returns the number of sentences in the sample text:

	>>> print(s.sentence_count)  
	2

To print the Flesch Reading Ease score:

	>>> print(s.flesch_score)  
	80.65638059701494

Every statistic contained in `s` can be similarly printed. The table below lists them. Section X describes in detail how each is calculated. Functions ending in `score` return a readability score. Those ending in `count` or `counts` return a character, syllable or word count. The last five functions end in `strip`; they return the original text without punctuation, decimals, etc.---useful to verify that the text has been appropriately processed before relevant statistics were calculated (see Section X).

- `flesch_score`: Flesch Reading Ease score
- `fleschkincaid_score`: Flesch-Kincaid score
- `fog_score`: Gunning Fog score
- `smog_score`: Dale-Chall score
- `sentence_count`: Number of sentences
- `character_count`: Number of non-punctuation characters
- `word_count`: Number of words
- `syb_counts`: Dictionary of `syllable_count` (number of syllables) and `polyword_count` (number of words with 3+ syllables)
- `sybperword_count`: Number of syllables per word
- `dalechall_count`: Number of words on the expanded Dale-Chall list
- `abbrv_strip`: Original text with abbreviations spelled out
- `decimal_strip`: Original text with decimals replaced by 0
- `nonend_strip `: Original text without non-sentence-ending full stops, question marks and exclamation points
- `word_array`: array of words (stripped of all punctuation)

`s.dict()` returns a dictionary containing all statistics in Table X. Call `scores` and `counts` to return dictionaries of only the readability scores and word/syllable/character counts, respectively:

	>>> s.counts
	{'dale_chall_list': 5, 'sentence': 2, 'poly_sybl_word': 1, 'word': 77, 'syllable': 85}

#### Calling individual functions

Instead of returning an object with all statistics calculated by `Textatistic`, you can call them separately. For example, to find just the word count:

	>>> import textatistic
	>>> textatistic.word_count('This is a joke, right?')
	5

Note, however, that calling `Textatistic` is more efficient than individually calling each function if you need more than one or two different readability scores. This could save substantial time if you're evaluating a large number of text samples.

All five readability functions can take the actual word, syllable, etc. counts needed to calculate them as inputs. For example, if you knew a passage of text had 35 words, three sentences and 62 syllables, pass those values in a dictionary directly to `flesch` instead of the text itself:

	params = {'word': 35, 'sentence': 3, 'syllable': 62}
	>>> textatistic.flesch(vars=params)
	45.1304761904762

#### Hyphenator

`Textatistic` counts syllables using the Python module `PyHyphen`, itself based on the C library `libhyphen`. `libhyphen` is used by TeX's typesetting system and in most open source text processing software, including [OpenOffice](http://www.openoffice.org "OpenOffice"). By default, `Textatistic` uses PyHyphen's American English Hyphenator. To change the locale, manually import `PyHyphen`'s `Hyphenator` class and call and object of it with the desired location/language, e.g.:

	>>> from hyphen import Hyphenator
	>>> nz = Hyphenator('en_nz')

For all `Textatistic` functions, simply indicate you want to use a different Hyphenator with the `hyphen` argument:

	textatistic.word_count('This is a short sentence.', hypen=nz)

See [PyHyphen's documentation](https://pypi.python.org/pypi/PyHyphen/ "PyHyphen documentation") for instructions on downloading and installing additional dictionaries---including those in other languages. Note, however, that readability tests were created for and tested on American English. The components which determine sentence complexity in one language may be very different to those in another---thus reducing (or eliminating) scores' accuracy. Also, the Dale-Chall function should only be used with American English text, since the list it depends on to determine "hard words" is itself only in American English.

#### Abbreviations

To determine sentence count, `Textatistic` replaces common abbreviations with their full text---otherwise the periods they use would over estimate sentence counts. The file `abbreviations.txt`, stored in the package contents, maintains an explicit list of all such text replacements. To view the contents of that file, import the `Abbreviations` class from `Textatistic`, create an `Abbreviations` object and  list its contents:

	>>> from textatistic import Abbreviations
	>>> abbr = Abbreviations()
	>>> abbr.list
	[['i.e.', 'id est'], ['i. e.', 'id est'], ['e.g.', 'exempli gratia'], ['e. g.', 'exempli gratia'], ['i.i.d.', 'independently and identically distributed'], ['et al.', 'et alii'], ['etc.', 'etcetera'], ['St.', 'Saint'], ['U.S.', 'United States'], ['U. S.', 'United States'], ['U.K.', 'United Kingdom'], ['U. K.', 'United Kingdom'], ['U.N.', 'United Nations'], ['U. N.', 'United Nations'], ['Roe v. Wade', 'Roe versus Wade'], ['Inc.', 'Incorporated'], ['Sec.', 'Section'], ['Vol.', 'Volume'], ['cf.', 'confer'], [' pp.', ' pages'], [' ff.', ' folio'], ['Dr.', 'Doctor'], ['viz.', 'videlicet']]

`abbr.list` returns a list of lists. Each element in the outermost list, e.g., `['e.g.', 'exampli gratia']`, indicates a single abbreviation and its replacement. The first element in the inner list---`'e.g.'` in the example---is the abbreviation; the second element---`'exampli gratia'`---is what will replace it.

The list is specific to my own work---particularly the abbreviation replacements---and may be irrelevant and/or incomplete for yours. If you are using `Textatistic` for serious analysis definitely heavily scrutinise each replacement---and determine elements to remove from or add to it.

Note also that this list replaces abbreviations with their entire text only if those abbreviations are marked with full stops. Thus, U.S. is replaced with United States but US is not. If you are using `Textatistic` in a relative analysis of text samples and they all use one or the other, this should be fine; if, on the other hand, your text samples sometimes use U.S. and other times US, add US to the list of replacements or manually change the samples to make them uniform.

To add abbreviation replacements, simply provide them as a list of lists using the `append` keyword argument---making sure to follow the order described above: the first element of each inner list is the text to be replaced, the second the text that will replace it. The following example adds two pointless substitutions:

	adds = [['dog', 'cat'], ['mouse', 'elephant']]
	>>> abbr = Abbreviations(append=adds)

As when using your own `Hyphenator` object, indicate the new `TextReplacement` object you wish to use in all `Textatistic` functions, this time with the `abbreviations` argument:

	>>> text = 'One is a word. Two is a number.'
	>>> s = Textatistic(text, abbreviations=abbr)

Should you wish to modify an existing text substitution---for example, replace `e.g.` with `eg` instead of `'example gratis'`---use the `modify` keyword. Similarly, to remove a substitution, use `remove`:

	>>> mods = [['e.g.', 'eg']]
	>>> dels = [['U. K.', 'United Kingdom']]
	>>> abbr = Abbreviations(modify=mods, remove=dels)

When these replacements are actually made in the evaluated text, they are done so in order. Items are appended to the end of the list, but those only modified remain in their original order. Thus, simply appending `['e.g.', 'eg']` won't have any effect on replacements---because they've already been replaced by `'exampli gratia' `.

It is also possible to add regular expressions in lieu of the exact text to be replaced. When doing so, indicate the regular expressions using precisely the same syntax employed by `re.sub()`---only make sure to preface the string with `r` (otherwise optional for `re.sub()`). For example, to append the regular expression `([a-z]\.){4}`---i.e., a lowercase abbreviation with four letters, like a.b.c.d.--- and replace it with xxxx, you'd type

	regex_adds = [[r"([a-z]\.){4}", "xxxx"]]
	>>> abbr = Abbreviations(append=regex_adds)

Finally, you may wish to throw out my entire abbreviations list and substitute your own. To do so, create a file with two comma-separated columns, the first of which contains the abbreviation and the second what replaces it. For example, assume I created such a file in my current working directory called `my_abbrvs.txt`. It would look something like this

	"dog", "cat"
	"pencil", "eraser"
	"person", "human"

To import this list instead of my abbreviations, use the `file` argument keyword:

	>>> abbr = Abbreviations(file=my_abbrvs.txt)

Finally, a note of warning. When defining abbreviations, do so carefully. For example, consider the substitution `[' pp.', ' pages']`. pp. is preceded by a space to prevent inadvertent deletion of an actual full stop. Without it, "This sentence ends with app." would become "This sentence ends with pages". Special care should be taken when using regular expressions, since their odd syntax may make it particularly easy to overlook such mistakes.

#### Dale-Chall easy word list

The Dale-Chall easy word list consists of 3,000 words understood by 80 percent of fourth-grade readers (aged 9--10). Only singular nouns and verb infinitives are listed, but according to the [Dale-Chall instructions](http://www.jstor.org/stable/40011418 "Using a Computer to Calculate the Dale-Chall Formula"), the list encompasses any alternate form of such words: "eat" includes "ate", etc.

I considered several algorithms that might identify alternate forms of words but in the end decided it would be simpler (and faster) to use a single, comprehensive list of all possible forms of words on the original Dale-Chall list.

Since I couldn't find one already created, I had to make my own. To do so, I used Python's Pattern library to generate every conceivable alternate form of each word I could think of, including verb tenses, comparative and superlative adjective forms and plural nouns.

In total, the generated list included over 14,000 words---many of which were gibberish. To get rid of nonsense (although, admittedly, including such words is probably harmless), the text of 94 English novels published online with Project Gutenberg were matched with words on the expanded list. Words not found in any of the novels were deleted.

You may, however, wish to use your own list of Dale-Chall easy words---maybe one that only includes the 3,000 original words. If that's the case, make sure each word on your list is separated by a carriage return and then call the `EasyWordList` class object with the file argument. All `Textatistic` would then need to explicitly reference that list with the keyword argument `easy_words`. For example, if such a file named `my_words.txt` were in your current working directory, you'd import and use it like so

	>>> from textatistic import EasyWordList, Textatistic
	>>> my_easy_words = EasyWordList(file=my_words.txt)
	>>> s = Textatistic(easy_words=my_easy_words)

If my Dale-Chall list omits some word (and it undoubtedly does) or you find more gibberish in it, please make a request on [Github.com](http://www.github.com "GitHub") (or just [email me](mailto:erin@erinhengel.com "Email Erin") directly).


#### Persistence

If you plan to evaluate a large number of text samples, you may save time by opening an instance of PyHyphen's `Hyphenator` class, the extended list of Dale-Chall words and file containing abbreviations