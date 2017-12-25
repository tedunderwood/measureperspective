#!/usr/bin/env python3

# dedup2earliest.py

import csv, sys
from difflib import SequenceMatcher
import pandas as pd

def titleregularize(title):
    title = str(title)
    if title == 'nan':
        title = ''

    if '|' in title:
        title = title.split('|')[0]

    title = title.lower().strip('/ .,:-')
    title = title.replace('the', 'x')
    if len(title) < 4:
        title = title + "    "
    if len(title) > 18:
        title = title[0 : 18]

    firstchars = title[0:3]

    return title, firstchars

def authorregularize(author):
    author = str(author)
    if author == 'nan':
        author = ''

    if '|' in author:
        author = author.split('|')[0]

    author = author.strip('/ ,.:123456789-').lower()
    return author

def isitamatch(t, a, title, author):
    m = SequenceMatcher(None, title, t)
    ratio = m.real_quick_ratio()
    if ratio > 0.8:
        betterratio = m.ratio()
        n = SequenceMatcher(None, author, a)
        authorratio = n.ratio()
        if betterratio > 0.9 and authorratio > 0.7:
            return True
        else:
            return False
    else:
        return False

## MAIN

args = sys.argv

if len(args) < 3:
    print('This script requires an infile and outfile as arguments.')
    print('It assumes they both are located in ../rawdata/')
    sys.exit(0)

infile = '../rawdata/' + args[1]
outfile = '../rawdata/' + args[2]

data = pd.read_csv(infile,
    dtype = {'docid': object, 'title': object, 'author': object, 'enumcron': object})
data.set_index('docid', inplace = True)

blocked_titles = dict()

for i in data.index:
    docid = i
    author = data.loc[i, 'author']
    title = data.loc[i, 'title']
    enumcron = str(data.loc[i, 'enumcron'])
    if len(enumcron) > 0 and enumcron != 'nan':
        title = title + ' ' + enumcron

    if len(title) < 2:
        continue

    title, firstchars = titleregularize(title)
    author = authorregularize(author)
    date = int(data.loc[i, 'inferreddate'])
    if date < 100:
        date = 3000

    # The reason being, that we want to accept the
    # earliest date, without treating the default
    # date of zero as an "earliest." We'd like to
    # take a specific date if one is available.

    if firstchars not in blocked_titles:
        blocked_titles[firstchars] = set()

    blocked_titles[firstchars].add((title, author, date, docid))

print('Titles divided into blocks.')

retained = set()
retained_exact_titles = dict()

for i in data.index:
    docid = i
    author = data.loc[i, 'author']
    title = data.loc[i, 'title']
    enumcron = str(data.loc[i, 'enumcron'])
    if len(enumcron) > 0 and enumcron != 'nan':
        title = title + ' ' + enumcron

    includedbc = str(data.loc[i, 'includedbc'])

    exacttitle = title
    if exacttitle in retained_exact_titles:
        retained_exact_titles[exacttitle].add(includedbc)
        continue
        # if this exact title is already in our retained set,
        # then we already have the earliest copy

    if len(title) < 2:
        retained.add(docid)
        continue

    title, firstchars = titleregularize(title)

    author = authorregularize(author)
    date = int(data.loc[i, 'inferreddate'])
    if date < 100:
        date = 3000

    if firstchars in blocked_titles:

        mindate = date
        best_docid = docid

        candidates = blocked_titles[firstchars]
        for oth_title, oth_author, oth_date, oth_docid in candidates:
            if oth_date >= mindate:
                continue
                # we want the earliest example only
                # and the matching process is slow, so this
                # saves time

            is_matching = isitamatch(title, author, oth_title, oth_author)

            if is_matching:
                mindate = oth_date
                best_docid = oth_docid

        retained.add(best_docid)
        retained_exact_titles[exacttitle] = set()
        retained_exact_titles[exacttitle].add(includedbc)

    else:
        retained.add(docid)

print('Of the original ' + str(len(list(data.index))) + ' rows,')
print('only ' + str(len(retained)) + ' were retained.')

newdata = data.loc[list(retained)]
for i in newdata.index:
    title = newdata.loc[i, 'title']
    enumcron = str(newdata.loc[i, 'enumcron'])
    if len(enumcron) > 0 and enumcron != 'nan':
        title = title + ' ' + enumcron
    if title in retained_exact_titles:
        includedbc = str(newdata.loc[i, 'includedbc'])
        retained_exact_titles[title].add(includedbc)
        newincl = '|'.join(retained_exact_titles[title])
        newdata.loc[i, 'includedbc'] = newincl

newdata.to_csv(outfile)







