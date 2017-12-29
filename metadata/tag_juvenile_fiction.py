#!/usr/bin/env python3

# tag_juvenile_fiction.py

# I've already gone through fantasy and sf manually,
# but I may have missed some things, and I haven't
# gone through the random fiction yet.

# So let's go through and make sure that everything
# librarians have tagged "juvenile" also has a tag
# in our metadata.

import sys, os, re
import numpy as np
import pandas as pd
from collections import Counter

def get_those_blasted_kids(meta):
    dates = []

    for idx in meta.index:
        juv = False

        tags = set(meta.loc[idx, 'tags'].split('|'))
        genres = str(meta.loc[idx, 'genres']).lower().replace('|', ' ').split()
        subjects = str(meta.loc[idx, 'subjects']).lower().replace('|', ' ').split()

        if 'juvenile' in genres or 'juvenile' in subjects:
            juv = True
        elif "children's" in genres or "children's" in subjects:
            juv = True

        if juv and 'juv' not in tags:
            tags.add('juv')
            meta.loc[idx, 'tags'] = '|'.join(tags)
            print(meta.loc[idx])
            dates.append(meta.loc[idx, 'firstpub'])

    return meta, dates

meta = pd.read_csv('random.csv', index_col = 'docid')
meta, dates1 = get_those_blasted_kids(meta)
meta.to_csv('newrandom.csv')
print(dates1)

meta = pd.read_csv('loc_oclc.csv', index_col = 'docid')
meta, dates2 = get_those_blasted_kids(meta)
meta.to_csv('newloc_oclc.csv')
print(dates2)



