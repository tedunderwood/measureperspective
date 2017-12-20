#!/usr/bin/env python3

# sample_recent.py

# This is a very mungy sort of datamunging
# script. In effect, I'm trying to abbreviate
# my labor. I've gone through manually and
# dated/culled fantasy and SF up to 1950.

# I can't keep doing that manually for the
# more than 2000 vols that remain, so I'm
# going to randomly sample 40 vols a decade.


import csv, sys, math, random
import pandas as pd

def makeint(avalue):
    try:
        intval = int(avalue)
    except:
        intval = float('nan')

    return intval


def sample_recent_books(infile):

    decades = dict()
    for i in range(1720, 2010, 10):
        decades[i] = set()

    unassigned = dict()
    for i in range(1720, 2010, 10):
        unassigned[i] = set()

    earlyvols = set()

    data = pd.read_csv(infile, index_col = 'docid', dtype = {'authordate': object})

    for docid in data.index:
        first = makeint(data.loc[docid, 'firstpub'])
        inferred = makeint(data.loc[docid, 'inferreddate'])

        if math.isnan(inferred):
            print('error')
            continue
            # nothing to be done with this

        else:
            authordate = str(data.loc[docid, 'authordate']).strip('.')
            try:
                authordeath = int(authordate[-4 : ])
            except:
                authordeath = 2060

            pubdec = (inferred // 10) * 10
            # the decade that this was published in


        if math.isnan(first):
            # this book has no first publication date
            # should we consider selecting it randomly?

            if authordeath < inferred:
                # no, we're not going to select this randomly,
                # because we have good reason to think it was
                # published after the author died
                # however ...

                if authordeath < 1950:
                    earlyvols.add(docid)

            else:

                unassigned[pubdec].add(docid)

        else:
            # this volume has a first publication date
            # we know we want it

            firstpubdec = (first // 10) * 10
            decades[firstpubdec].add(docid)

    # Now we have sorted the docids into those already reliably
    # dated (mostlt early), and a bunch that are not (all late).

    # randomly get 40 a decade

    for dec in range(1950, 2010, 10):
        max = len(unassigned[dec])
        if max < 40:
            k = max
        else:
            k = 40

        sampled = random.sample(unassigned[dec], k)

        decades[dec] = set(sampled) | decades[dec]

    allchosen = list()
    for dec in range(1800, 2010, 10):
        allchosen.extend(decades[dec])

    allchosen.extend(list(earlyvols))

    chosendata = data.loc[allchosen]

    return chosendata

chosensf = sample_recent_books('../rawdata/edited_sf.csv')

chosensf.to_csv('../rawdata/chosen_sf.csv')

chosenfantasy = sample_recent_books('../rawdata/edited_fantasy.csv')

chosenfantasy.to_csv('../rawdata/chosen_fantasy.csv')



