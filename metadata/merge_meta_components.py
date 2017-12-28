#!/usr/bin/env python3

# merge_meta_components.py

# This script builds a master metadata
# file from components stored in the same
# directory. I hope this will make it easy
# to build and expand the metadata, while
# also documenting how it was constructed.

import pandas as pd

import glob, csv

# Because HathiTrust volumes have been divided into slices
# of (roughly) equal size, I'm going to have two id
# columns: htid (HathiTrust vol id) and docid (the id
# attached to the actual slice file in the data folder).

# There can be one or more docids per htid.

# Each docid is paired to a token count, which is
# found in one of several parsing_metadata files.

htid2docs = dict()
doc2tokens = dict()

parsing_paths = glob.glob('parsing*.tsv')
for p in parsing_paths:
    with open(p, encoding = 'utf-8') as f:
        reader = csv.DictReader(f, delimiter = '\t')
        for row in reader:
            docid = row['path'][8 : -4]
            # that's a kloodge
            htid = row['htid']
            if htid not in htid2docs:
                htid2docs[htid] = []
            htid2docs[htid].append(docid)
            doc2tokens[docid] = row['totaltokens']

# Load all the dataframes holding metadata.

component_paths = ['random.csv', 'loc_oclc.csv', 'supernatural.csv', 'oslerbailey.csv', 'thedetectives.csv']
components = []

for p in component_paths:
    df = pd.read_csv(p, index_col = 'docid')
    components.append(df)

    # I need to flag a source of confusion here; the thing that counts as 'docid'
    # in the component files is going to turn into 'htid' in the slice-
    # level metadata.

# Now, for each htid, gather all genre tags in a set.
# We are assuming that some htids will occur in more
# than one component file, so their genre tags will
# need to be aggregated

htid2tagset = dict()

for c in components:
    for idx, row in c.iterrows():
        tags = set(row['tags'].split('|'))
        if idx in htid2tagset:
            htid2tagset[idx] = htid2tagset[idx] | tags
        else:
            htid2tagset[idx] = tags

# Now we're going to build up a dataframe from rows

rows = []

existing_columns = list(components[1].columns.values)
existing_columns.pop(existing_columns.index('place'))
# we just don't need it

# I use loc_oclc.csv for that because I like the order of the columns there.

alreadyused = set()
overlap = 0

for c in components:
    for htid, row in c.iterrows():
        if htid in alreadyused:
            overlap += 1
            continue
            # we've already written this file

        if htid in htid2docs:
            alreadyused.add(htid)
            for docid in htid2docs[htid]:
                newrow = dict()
                newrow['docid'] = docid
                newrow['htid'] = htid
                newrow['tokens'] = doc2tokens[docid]
                for col in existing_columns:
                    newrow[col] = row[col]
                newrow['tags'] = '|'.join(htid2tagset[htid])
                rows.append(newrow)

newmetafile = pd.DataFrame(rows)

columns = ['docid', 'htid', 'tokens', 'tags', 'author', 'authordate', 'imprint', 'inferreddate', 'firstpub', 'enumcron', 'subjects', 'genres', 'title']
newmetafile = newmetafile.loc[ : , columns]

newmetafile.to_csv('newmastermetadata.csv', index = False)









