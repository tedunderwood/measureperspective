#!/usr/bin/env python3

# experiment.py

import sys, os
import numpy as np
import pandas as pd
from collections import Counter

# thresholds = [1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]

thresholds = [1900, 1920, 1950, 1970, 1980, 1990, 2000, 2010]

def get_threshold(date):
    global thresholds
    for t in thresholds:
        if t > date:
            return t
    return 2010

md = pd.read_csv('mastermetadata.csv')

def splittags(tags):
    if type(tags) == float:
        return set()
    else:
        return set(tags.split('|'))

fantasy = Counter()
scifi = Counter()
random = Counter()


for idx, row in md.iterrows():
    date = int(row['firstpub'])
    thresh = get_threshold(date)
    genres = splittags(row['tags'])

    if 'fantasy_loc' in genres or 'fantasy_oclc' in genres:
        fantasy[thresh] += 1
    if 'sf_loc' in genres or 'sf_oclc' in genres:
        scifi[thresh] += 1
    if 'random' in genres:
        random[thresh] += 1


for t in thresholds:
    print(t)
    print('Fantasy: ' + str(fantasy[t]))
    print('SF: ' + str(scifi[t]))
    print('Random: ' + str(random[t]))
    print()


