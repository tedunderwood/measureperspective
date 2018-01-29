#!/usr/bin/env python3

# main_experiment.py

import sys, os, csv, random, pickle
import numpy as np
import pandas as pd

# FUNCTIONS GET DEFINED BELOW.

def addtodict(d1, d2):
    for k, v in d2.items():
        if k in d1:
            d1[k].append(v)
        else:
            d1[k] = [v]

def get_features(wordcounts, wordlist):
    numwords = len(wordlist)
    wordvec = np.zeros(numwords)
    for idx, word in enumerate(wordlist):
        if word in wordcounts:
            wordvec[idx] = wordcounts[word]

    return wordvec

def get_dataframe(tsvpath, vocablist):
    '''
    Given a vocabulary list, and list of volumes, this actually creates the
    pandas dataframe with volumes as rows and words (or other features) as
    columns.
    '''

    voldata = list()
    classvector = list()

    with open(tsvpath, encoding = 'utf-8') as f:
        voldict = dict()
        totalcount = 0
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) > 2 or len(fields) < 2:
                continue

            word = fields[0]
            if fields[1] == 'frequency':
                continue
            count = float(fields[1])
            voldict[word] = count
            totalcount += count

    features = get_features(voldict, vocablist)
    voldata.append(features)

    masterdata = pd.DataFrame(voldata)

    return masterdata

def get_word_diffs(modelname, atsv):

    modelpath = '../modeloutput/' + modelname + '.pkl'

    with open(modelpath, 'rb') as input:
        modeldict = pickle.load(input)

    vocablist = modeldict['vocabulary']
    scaler = modeldict['scaler']

    tsvpath = '../data/' + atsv
    masterdata = get_dataframe(tsvpath, vocablist)
    # True, there, means frequencies already normalized to be relative freqs.
    standarddata = scaler.transform(masterdata)

    coefspath = '../modeloutput/' + modelname + '.coefs.csv'
    coefs = dict()
    with open(coefspath, encoding = 'utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            word = row[0]

            coef = float(row[1])
            coefs[word] = coef

    numwords = len(vocablist)
    coefvec = np.zeros(numwords)
    for idx, word in enumerate(vocablist):
        if word in coefs:
            coefvec[idx] = coefs[word]

    print(standarddata)
    assert len(coefvec) == len(standarddata[0])

    products = coefvec * standarddata[0]

    diffs = dict()
    for idx, word in enumerate(vocablist):
        diffs[word] = products[idx]

    return diffs

date = int(sys.argv[1])
atsv = sys.argv[2]

periods = [(1870, 1899), (1900, 1929), (1930, 1959), (1960, 1989), (1990, 2010), (1880, 1909), (1910, 1939), (1940, 1969), (1970, 1999), (1890, 1919), (1920, 1949), (1950, 1979), (1980, 2009)]

# identify the periods at issue

for floor, ceiling in periods:
    if ceiling+ 1 == date:
        f1, c1 = floor, ceiling
    if floor == date:
        f2, c2 = floor, ceiling

new = dict()
old = dict()

for i in range(5):
    for j in range(5):
        for part in [1, 2]:

            name1 = 'rccsf'+ str(f1) + '_' + str(c1) + '_' + str(i) + '_' + str(part)
            name2 = 'rccsf'+ str(f2) + '_' + str(c2) + '_' + str(j) + '_' + str(part)

            olddiffs = get_word_diffs(name1, atsv)
            newdiffs = get_word_diffs(name2, atsv)
            addtodict(old, olddiffs)
            addtodict(new, newdiffs)

allwords = set([x for x in old.keys()]).union(set([x for x in new.keys()]))

with open('crudemetrics/surprisein' + str(date) + '_' + atsv, mode = 'w', encoding = 'utf-8') as f:
    scribe = csv.DictWriter(f, fieldnames = ['word', 'coef'], delimiter = '\t')
    scribe.writeheader()

    for w in allwords:
        if w in old:
            oldcoef = sum(old[w]) / len(old[w])
        else:
            oldcoef = 0

        if w in new:
            newcoef = sum(new[w]) / len(new[w])
        else:
            newcoef = 0

        o = dict()
        o['word'] = w
        o['coef'] = newcoef - oldcoef
        scribe.writerow(o)



