#!/usr/bin/env python3

# just_concatenate

import pandas as pd

existing = pd.read_csv('../rawdata/edited_random_fiction.csv', index_col = 'docid')
new = pd.read_csv('../rawdata/fiction_supplement.csv', index_col = 'docid')

exist_ids = set(existing.index)
new_ids = set(new.index)

print('Overlap: ' + str(len(exist_ids.intersection(new_ids))))

new_master = pd.concat([existing, new])
new_master.sort(columns = 'firstpub', inplace = True)
new_master.to_csv('../rawdata/new_edited_random_fiction.csv')
