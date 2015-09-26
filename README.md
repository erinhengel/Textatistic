# Introduction
text_statistics is a simple program to calculate the following readability statistics:

1. Flesch Reading Ease
2. Flesch-Kincaid
3. Gunning Fog
4. SMOG
5. Dale-Chall

# Other functions
Additionally, it offers several text processing functions:

1.  abbrv\_strip: replace abbreviations with the full text versions in abbreviations.txt
2.  decimal\_strip: strip decimals out of numbers and replace with 0
3.  punct\_strip: strip out punctuation
4.  period\_strip: strip out all full stops
5.  sentence\_count: return number of sentences
6.  character count\_count: return number of non-punctuation characters
7.  word\_count: return number of words
8.  syllable\_counts: return dictionary containing syllable\_count (number of syllables) and polysyllableword\_count (number of words with 3+ syllables)
9.  syllableperword\_count: number of syllables per word
10.  dalechall\_count: number of words on the expanded Dale-Chall list.
