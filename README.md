# Introduction
text_statistics is a simple program to calculate the following readability statistics:

1. `flesch_score`: Flesch Reading Ease
2. `fleschkincaid_score`: Flesch-Kincaid
3. `fog_score`: Gunning Fog
4. `smog_score`: SMOG
5. `dalechall_score`: Dale-Chall

# Other functions

1.  `abbrv_strip`: replace abbreviations with the full text versions (`abbreviations.txt`)
2.  `decimal_strip`: strip decimals out of numbers and replace with 0
3.  `punct_strip`: strip out punctuation
4.  `eriod_strip`: strip out all full stops
5.  `sentence_count`: return number of sentences
6.  `character_count`: return number of non-punctuation characters
7.  `word_count`: return number of words
8.  `syllable_counts`: return dictionary containing `syllable_count` (number of syllables) and `polysyllableword_count` (number of words with 3+ syllables)
9.  `syllableperword_count`: number of syllables per word
10.  `dalechall_count`: number of words on the expanded Dale-Chall list (`dalechall.txt`)

# Usage

todo
