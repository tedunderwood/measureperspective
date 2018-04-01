#!/usr/bin/env python3

# mungezscores.py

import sys, os, csv, random
import numpy as np
import pandas as pd

keepers = ['Stranger in a strange land.', 'Player piano.', 'The dying earth',
            'The left hand of darkness', 'SF; the best of the best.']

data = pd.read_csv('sf1940_new_surprises.tsv', sep = '\t')

def justvol(docid):
    if '_' in docid:
        return docid.split('_')[0]
    else:
        return docid

data = data.assign(volid = data.docid.apply(justvol))

sacreddates = set()
otherdates = set()

for k in keepers:
    for idx in data.index:
        if data.loc[idx, 'title'] == k:
            date = data.loc[idx, 'firstpub']
            sacreddates.add(date)
            break

grouped = data.groupby('volid')

rows = []
for k, df in grouped:
    if list(df.tags)[0] == 'random':
        continue

    o = dict()
    o['title'] = list(df.title)[0]
    o['firstpub'] = list(df.firstpub)[0]

    if o['title'] in keepers:
        o['colour'] = 'black'
    elif o['firstpub'] in sacreddates:
        continue
    elif o['firstpub']+1 in sacreddates:
        continue
    elif o['firstpub']-1 in sacreddates:
        continue
    elif o['firstpub'] in otherdates:
        continue
    else:
        otherdates.add(o['firstpub'])
        o['colour'] = 'gray'

    o['volid'] = k
    o['diff'] = np.mean(df['diff'])
    o['alien'] = np.mean(df.alien)
    o['original'] = np.mean(df.original)
    o['author'] = list(df.author)[0]

    rows.append(o)

cols = ['volid', 'diff', 'alien', 'original', 'firstpub', 'colour', 'author', 'title']

with open('sf1940_means.tsv', mode = 'w', encoding = 'utf-8') as f:
    scribe = csv.DictWriter(f, delimiter = '\t', fieldnames = cols)
    scribe.writeheader()
    for o in rows:
        scribe.writerow(o)

