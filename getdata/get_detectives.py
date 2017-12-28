# get_detectives.py

import pandas as pd
meta = pd.read_csv('/Users/tunder/Dropbox/book/chapter2/metadata/concatenatedmeta.csv', index_col = 'docid')

selections = []

for idx in meta.index:
    tags = meta.loc[idx, 'tags'].split(' | ')
    if 'locdetective' in tags or 'det100' in tags and idx[0].isalpha():
        selections.append(idx)

selected = meta.loc[selections]

selected.to_csv('../rawdata/thedetectives.csv')


