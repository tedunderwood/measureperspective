import shutil, os, glob
import pandas as pd

for ratio in [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]:
    metafile = 'partitionmeta/meta' + str(ratio) + '.csv'
    df = pd.read_csv(metafile, index_col = 'docid')
    for i in df.index:
        if df.loc[i, 'tags'] != 'random':
            continue
        outpath = 'mix/' + str(ratio) + '/' + i + '.tsv'
        shutil.copyfile('../data/' + i + '.tsv', outpath)


