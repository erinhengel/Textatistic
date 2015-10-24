#!/usr/bin/python
from hyphen import Hyphenator
from datetime import datetime, date, time, timedelta

from textatistic import Textatistic, Abbreviations
import textatistic

abbr = Abbreviations(append=[['dog', 'cat'], ['mouse', 'elephant']], modify=[['i.e.', 'XXX'], ['cf.', 'YYY']], remove=[['U. N.', 'United Nations']])
abbr.list[0][1] == "XXX"
abbr.list[-1][0] == "mouse"
try:
    abbr.list.index(['U. N.', 'United Nations'])
    print("Found U.N.")
except ValueError:
    pass

text_sample = 'There were a king with a large jaw and a queen with a plain face, on the throne of England; there were a king with a large jaw and a queen with a fair face, on the throne of France. In both countries it was clearer—than-crystal to the lords of the State preserves of loaves and fishes, that things in general were settled for ever (who would have thought?!)—The Jacksonian Five ate a cake. We also ate a cake (and that suprised me!!). Here is my co-author. This is a decimal 0.835.'

iterate = 1000
suma = 0
for i in range(iterate):
    start = datetime.now()
    Textatistic(text_sample)
    end = datetime.now()
    delta = end - start
    suma += timedelta.total_seconds(delta)

print(str(iterate) + " Texatstic iterations")
print(str(round(suma, 4)) + " seconds\n\n")

print("punct_clean text")
print(textatistic.punct_clean(text_sample) + "\n\n")

print("word_array list")
print(textatistic.word_array(text_sample))