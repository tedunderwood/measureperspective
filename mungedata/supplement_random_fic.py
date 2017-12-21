#!/usr/bin/env python3

# sample_random_fic.py

# Counts the fantasy and scifi,
# and then gets an at-least equal
# number of randomly-selected volumes
# in each decade


import csv, sys, math, random
import pandas as pd
from collections import Counter

def makeint(avalue):
    try:
        intval = int(avalue)
    except:
        intval = float('nan')

    return intval

fantasy_count = Counter()
sf_count = Counter()

sff = pd.read_csv('../rawdata/merged_sff.csv', index_col = 'docid')

for idx in sff.index:
    date = sff.loc[idx, 'firstpub']
    intdate = makeint(date)
    if not math.isnan(date):
        dec = (date // 10) * 10
        tags = sff.loc[idx, 'tags'].split('|')
        if 'sf_loc' in tags or 'sf_oclc' in tags:
            sf_count[dec] += 1
        elif 'fantasy_loc' in tags or 'fantasy_oclc' in tags:
            fantasy_count[dec] += 1

ceiling = dict()
for i in range(1800, 2010, 10):
    print()
    print(i)
    print('Fantasy: ' + str(fantasy_count[i]))
    print('Scifi: ' + str(sf_count[i]))
    maximum = max(fantasy_count[i], sf_count[i])
    if maximum < 1:
        ceiling[i] = 0
        continue
    else:
        tenpercent = maximum // 9
        if tenpercent < 3:
            tenpercent = 3
        ceiling[i] = maximum + tenpercent
        print(ceiling[i])

# now we have a dict of the number of vols we want in each decade

print('ceiling calculated')

# Let's figure out how many we have

have = pd.read_csv('../rawdata/edited_random_fiction.csv', index_col = 'docid', dtype = {'authordate': object, 'firstpub': int})

for docid in have.index:
    firstpub = int(have.loc[docid, 'firstpub'])
    dec = (firstpub // 10) * 10
    ceiling[dec] = ceiling[dec] -1

print()
for i in range(1800, 2010, 10):
    print(i, ceiling[i])
print()

decades = dict()
for i in range(1800, 2010, 10):
    decades[i] = set()

avoid = set(sff.index)

data = pd.read_csv('../rawdata/deduped_all_fiction.csv', index_col = 'docid', dtype = {'authordate': object})

for docid in data.index:

    if docid in avoid:
        continue
    # We're not going to duplicate vols we already have
    # as fantasy or science fiction. Logically, we could, but
    # a few scattered overlaps might create noise.

    date = makeint(data.loc[docid, 'inferreddate'])

    if math.isnan(date) or date < 1800:
        continue

    else:
        authordate = str(data.loc[docid, 'authordate']).strip('.')
        try:
            authordeath = int(authordate[-4 : ])
        except:
            authordeath = 2060

        if (authordeath + 2) < date:
            continue
            # we don't want books published long after
            # the author's death; we're aiming for contemporary

        genres = str(data.loc[docid, 'genres'])
        if 'Science fiction' in genres or 'Fantasy' in genres:
            continue

        subjects = str(data.loc[docid, 'subjects'])
        if 'Science fiction' in subjects or 'Fantasy' in subjects:
            continue

        # we don't want judgments about generic similarity to be
        # complicated by the sheer size of the genre contaminating
        # the random set as time passes

    dec = (date // 10) * 10
    if dec not in decades:
        decades[dec] = set()

    decades[dec].add(docid)

# now we have a dict of vols to be sampled in each decade

chosen = []

for dec in range(1800, 2010, 10):
    available = len(decades[dec])
    goal = ceiling[dec]
    if goal < 1:
        continue

    if goal > available:
        goal = available
        print(dec)

    sampled = random.sample(decades[dec], goal)

    chosen.extend(sampled)

random_fiction = data.loc[chosen]

random_fiction.to_csv('../rawdata/fiction_supplement.csv')



