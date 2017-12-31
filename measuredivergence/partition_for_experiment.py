#!/usr/bin/env python3

# partition_for_experiment.py

# The goal here is to create two metadata files,
# containing the same genres but two different
# random selections of them

# A) Partition A has random 1800-1930,
# a random half of fantasy-supernatural 1800-1930,
# and detective 1800-1930.

# B) Partition B has the same genres,
# but a different random half of them

import random, math
import pandas as pd
import numpy as np

def tags2tagset(x):
    ''' function that will be applied to transform
    fantasy|science-fiction into {'fantasy', 'science-fiction'} '''
    if type(x) == float:
        return set()
    else:
        return set(x.split('|'))

master = pd.read_csv('../metadata/mastermetadata.csv', index_col = 'docid')
column_of_sets = master['tags'].apply(tags2tagset)
df = master.assign(tagset = column_of_sets)

mainstream = df[df['tagset'].map(lambda tagset: ('random' in tagset) or ('randomB' in tagset))]
fantasy = df[df['tagset'].map(lambda tagset: ('fantasy_loc' in tagset) or ('fantasy_oclc' in tagset) or ('supernat' in tagset))]
detective = df[df['tagset'].map(lambda tagset: ('detective' in tagset))]

mainstream = mainstream[mainstream.firstpub < 1930]
detective = detective[detective.firstpub < 1930]
fantasy = fantasy[fantasy.firstpub < 1930]

for idx, row in mainstream.iterrows():
    if type(row['author']) != str:
        mainstream.loc[idx, 'author'] = random.choice(['A anonymous', 'B anonymous', 'C anonymous', 'X anonymous', 'Y anonymous', 'Z anonymous'])

mainstream.sort_values(by = 'author', inplace = True)
detective.sort_values(by = 'author', inplace = True)
fantasy.sort_values(by = 'author', inplace = True)

for idx in mainstream.index:
    mainstream.loc[idx, 'tags'] = 'random'

for idx in fantasy.index:
    fantasy.loc[idx, 'tags'] = 'fantasy'

mainstream = mainstream.drop('tagset', 1)
detective = detective.drop('tagset', 1)
fantasy = fantasy.drop('tagset', 1)

print(mainstream.shape)
print(detective.shape)
print(fantasy.shape)

main1, main2 = np.array_split(mainstream, 2)
fant1, fant2 = np.array_split(fantasy, 2)
dete1, dete2 = np.array_split(detective, 2)

partition1 = pd.concat([main1, dete1, fant1])
partition2 = pd.concat([main2, dete2, fant2])

partition1.to_csv('partitionmeta/part1.csv')
partition2.to_csv('partitionmeta/part2.csv')





