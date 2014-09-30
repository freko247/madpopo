# -*- coding:utf-8 -*-
'''Simple sentiment analysis.
AFINN-111 is as of June 2011 the most recent version of AFINN, download at:
http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip

A linguistics professor was lecturing to her class one day. "In English,"
she said, "A double negative forms a positive. In some languages, though, such
as Russian, a double negative is still a negative. However, there is no
language wherein a double positive can form a negative." A voice from the back
of the room piped up, "Yeah . . .right."
'''

import math
import re
filenameAFINN = 'AFINN/AFINN-111.txt'
try:
    afinn = dict(map(lambda (w, s): (w, int(s)), [
        ws.strip().split('\t') for ws in open(filenameAFINN)]))
except IOError:
    print "AFINN/AFINN-111.txt could not be found, it can be downloaded at:" \
          + "http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/" \
          + "imm6010.zip'"
pattern_split = re.compile(r"\W+")


def sentiment(text):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence.
    """
    words = pattern_split.split(text.lower())
    sentiments = map(lambda word: afinn.get(word, 0), words)
    if sentiments:
        sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
    else:
        sentiment = 0
    return sentiment
