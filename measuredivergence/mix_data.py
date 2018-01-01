#!/usr/bin/env python3

# mix_data.py

import sys, os, csv, random
import numpy as np
import pandas as pd

meta = pd.read_csv('partitionmeta/part1.csv', index_col = 'docid')
detectives = meta.index[meta['tags'] == 'detective'].tolist()
masterfantasy = meta.index[meta['tags'] == 'fantasy'].tolist()
randmeta = meta[meta.tags == 'random']

moreneeded = 100 - len(detectives)

for ratio in [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]:

    fantasy = random.sample(masterfantasy, len(detectives))
    counter = 0

    if not os.path.exists('mix/' + str(ratio)):
        os.makedirs('mix/' + str(ratio))

    rows = []
    rownames = []

    for f, d in zip(fantasy, detectives):

        fraction = ratio / 100

        fantdf = pd.read_csv('../data/' + f + '.tsv', sep = '\t', index_col = 'feature')
        detectdf = pd.read_csv('../data/' + d + '.tsv', sep = '\t', index_col = 'feature')

        wordsinfantasy = set(fantdf.index)
        wordsindetective = set(detectdf.index)
        inboth = wordsinfantasy.intersection(wordsindetective)

        interdf = fantdf.loc[inboth]

        numtochange = int(len(inboth) * fraction)
        tochange = random.sample(inboth, numtochange)
        for i in tochange:
            if type(i) != str:
                continue
            else:
                dval = float(detectdf.loc[i, 'frequency'])
                interdf.loc[i, 'frequency'] = dval

        onlyfantasy = wordsinfantasy - inboth
        numtotake = int(len(onlyfantasy) * (1 - fraction))
        fantasywords = random.sample(onlyfantasy, numtotake)
        uniquefant = fantdf.loc[fantasywords]

        onlydetective = wordsindetective - inboth
        numtotake = int(len(onlydetective) * fraction)
        detectivewords = random.sample(onlydetective, numtotake)
        uniquedetect = detectdf.loc[detectivewords]

        thisfile = pd.concat([interdf, uniquefant, uniquedetect])
        filename = 'mix/' + str(ratio) + '/mixed_' + str(counter) + '.tsv'
        thisfile.to_csv(filename, sep = '\t')
        counter += 1

        if ratio < 50:
            row = meta.loc[f]
        elif ratio > 50:
            row = meta.loc[d]
        else:
            whim = random.choice([d, f])
            row = meta.loc[whim]

        rowname = 'mixed_' + str(counter)
        rownames.append(rowname)
        rows.append(row)

    outmeta = pd.DataFrame(rows, index = rownames)
    outmeta = pd.concat([outmeta, randmeta])
    outmeta.to_csv('mix/meta' + str(ratio) + '.csv', index_label = 'docid')










