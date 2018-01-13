#!/usr/bin/env python3

# create_character_table.py

# This script generates a summary table that I'll use for subsequent analysis.
# It uses data about characters created by BookNLP, and already available
# publicly through the "Dataverse" attached to "The Tranformation of
# Gender in English-Language Fiction."

import csv, sys, os
from collections import Counter
import pandas as pd

csv.field_size_limit(sys.maxsize)

wordcounts = Counter()

file1 = '/Users/tunder/data/character_table_18c19c.tsv'
file2 = '/Users/tunder/data/character_table_post1900.tsv'

# To start, let's create a list of the most common words
# in this dataset. This will reduce the size of the table
# we have to create.

def add2ctr(filename, ctr):
    with open(filename, encoding = 'utf-8') as f:
        reader = csv.DictReader(f, delimiter = '\t')
        for row in reader:
            words = row['words'].strip().split()
            for w in words:
                wordcounts[w] += 1

lexpath = 'lexicon.tsv'

if not os.path.isfile(lexpath):
    add2ctr(file1, wordcounts)
    add2ctr(file2, wordcounts)
    lexicon = wordcounts.most_common(10000)

    # The most_common() function returns a list of tuples
    # in the format (key, count of key).
    # Let's write that info.

    with open(lexpath, mode = 'w', encoding = 'utf-8') as f:
        for a, b in lexicon:
            f.write(str(a) + '\t' + str(b) + '\n')

    # But then only keep a set of keys.
    vocab = set([x[0] for x in lexicon])

else:
    vocab = set()
    with open(lexpath, encoding = 'utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            vocab.add(fields[0])

print('vocab created')
print()

# We're going to want author gender, so let's load some metadata.

meta = pd.read_csv('/Users/tunder/Dropbox/python/character/metadata/filtered_fiction_plus_18c.tsv', sep = '\t', index_col = 'docid')
meta = meta[~meta.index.duplicated(keep='first')]

# Now, time to go back through the raw data.

wordctbyyear = dict()
charctbyyear = dict()
wordtotals = Counter()
chartotals = Counter()

ontology = ['m', 'f', 'u']
authchartuples = []

for auth in ontology:
    for char in ontology:
        authchartuples.append((auth, char))

for i in range (1780, 2010):
    wordctbyyear[i] = dict()
    charctbyyear[i] = dict()
    wordtotals[i] = Counter()
    chartotals[i] = Counter()

    for act in authchartuples:
        wordctbyyear[i][act] = Counter()
        charctbyyear[i][act] = Counter()

def add2table(filename, wordctr, charctr, meta, errors, wordtotals, chartotals):
    with open(filename, encoding = 'utf-8') as f:
        reader = csv.DictReader(f, delimiter = '\t')
        ct = 0

        for row in reader:
            docid = row['docid']
            if docid in meta.index:
                authgender = meta.loc[docid, 'authgender']

            else:
                errors += 1
                continue

            ct += 1
            if ct % 1000 == 1:
                print(ct)

            chargender = row['gender']
            pubdate = int(row['pubdate'])
            act = (authgender, chargender)
            chartotals[pubdate][act] += 1

            words = row['words'].strip().split()

            already_added_to_charctr = set()

            for w in words:
                if w in vocab:
                    wordctr[pubdate][act][w] += 1
                    wordtotals[pubdate][act] += 1

                    if w not in already_added_to_charctr:
                        charctr[pubdate][act][w] += 1
                        already_added_to_charctr.add(w)

errors = 0

add2table(file1, wordctbyyear, charctbyyear, meta, errors, wordtotals, chartotals)
print('file 1 complete')

add2table(file2, wordctbyyear, charctbyyear, meta, errors, wordtotals, chartotals)
print('file 2 complete')

cols = ['year', 'authgender', 'chargender', 'word', 'wordct', 'charct']

with open('chartable.tsv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, delimiter = '\t', fieldnames = cols)
    writer.writeheader()
    for year, actable in wordctbyyear.items():
        for act, wordtable in actable.items():
            authgender, chargender = act
            for w, wct in wordtable.items():
                r = dict()
                r['year'] = year
                r['authgender'] = authgender
                r['chargender'] = chargender
                r['word'] = w
                r['wordct'] = wct
                r['charct'] = charctbyyear[year][act][w]
                writer.writerow(r)

cols = ['year', 'authgender', 'chargender', 'wordtotal', 'chartotal']

with open('totals.tsv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, delimiter = '\t', fieldnames = cols)
    writer.writeheader()
    for year in range(1780, 2010):
        for act in authchartuples:
            authgender, chargender = act
            r = dict()
            r['year'] = year
            r['authgender'] = authgender
            r['chargender'] = chargender
            r['wordtotal'] = wordtotals[year][act]
            r['chartotal'] = chartotals[year][act]
            writer.writerow(r)








