#!/usr/bin/env python3

# experiment.py

import sys, os
import numpy as np
import pandas as pd
import versatiletrainer2
import metaselector

import matplotlib.pyplot as plt

from scipy import stats

def first_experiment():

    sourcefolder = '../data/'
    metadatapath = '../metadata/mastermetadata.csv'
    vocabpath = '../modeloutput/experimentalvocab.txt'
    tags4positive = {'fantasy_loc', 'fantasy_oclc'}
    tags4negative = {'sf_loc', 'sf_oclc'}
    sizecap = 200

    metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist = versatiletrainer2.get_simple_data(sourcefolder, metadatapath, vocabpath, tags4positive, tags4negative, sizecap)

    c_range = [.004, .012, 0.3, 0.8, 2]
    featurestart = 3000
    featureend = 4400
    featurestep = 100
    modelparams = 'logistic', 10, featurestart, featureend, featurestep, c_range

    matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, 'first_experiment', '../modeloutput/first_experiment.csv')

    plt.rcParams["figure.figsize"] = [9.0, 6.0]
    plt.matshow(matrix, origin = 'lower', cmap = plt.cm.YlOrRd)
    plt.show()

def get_ratio_data(vocabpath, sizecap, ratio, excludebelow = 0, excludeabove = 3000):

    ''' Loads metadata, selects instances for the positive
    and negative classes (using a ratio to blend two positive
    classes), creates a lexicon if one doesn't
    already exist, and creates a pandas dataframe storing
    texts as rows and words/features as columns. A refactored
    and simplified version of get_data_for_model().
    '''

    holdout_authors = True
    freqs_already_normalized = True
    verbose = False
    datecols = ['firstpub']
    indexcol = ['docid']
    extension = '.tsv'
    genrecol = 'tags'
    numfeatures = 6000

    tags4positive1 = {'fantasy_loc', 'fantasy_oclc'}
    tags4positive2 = {'random'}
    tags4negative = {'sf_loc', 'sf_oclc'}

    sourcefolder = '../data/'
    metadatapath = '../metadata/mastermetadata.csv'

    # Get a list of files.
    allthefiles = os.listdir(sourcefolder)

    volumeIDsinfolder = list()
    volumepaths = list()
    numchars2trim = len(extension)

    for filename in allthefiles:

        if filename.endswith(extension):
            volID = filename[0 : -numchars2trim]
            # The volume ID is basically the filename minus its extension.
            volumeIDsinfolder.append(volID)

    metadata = metaselector.load_metadata(metadatapath, volumeIDsinfolder, excludebelow, excludeabove, indexcol = indexcol, datecols = datecols, genrecol = genrecol)

    # That function returns a pandas dataframe which is guaranteed to be indexed by indexcol,
    # and to contain a numeric column 'std_date' as well as a column 'tagset' which contains
    # sets of genre tags for each row. It has also been filtered so it only contains volumes
    # in the folder, and none whose date is below excludebelow or above excludeabove.

    orderedIDs, classdictionary = metaselector.set_positive_ratio(metadata, sizecap, tags4positive1, tags4positive2, ratio, tags4negative)

    metadata = metadata.loc[orderedIDs]
    # Limits the metadata data frame to rows we are actually using
    # (those selected in select_instances).

    # We now create an ordered list of id-path tuples.

    volspresent = [(x, sourcefolder + x + extension) for x in orderedIDs]
    print(len(volspresent))

    print('Building vocabulary.')

    vocablist = versatiletrainer2.get_vocablist(vocabpath, volspresent, n = numfeatures)

    numfeatures = len(vocablist)

    print()
    print("Number of features: " + str(numfeatures))

    # For each volume, we're going to create a list of volumes that should be
    # excluded from the training set when it is to be predicted. More precisely,
    # we're going to create a list of their *indexes*, so that we can easily
    # remove rows from the training matrix.

    authormatches = [ [] for x in orderedIDs]

    # Now we proceed to enlarge that list by identifying, for each volume,
    # a set of indexes that have the same author. Obvs, there will always be at least one.
    # We exclude a vol from it's own training set.

    if holdout_authors:
        for idx1, anid in enumerate(orderedIDs):
            thisauthor = metadata.loc[anid, 'author']
            authormatches[idx1] = list(np.flatnonzero(metadata['author'] == thisauthor))

    for alist in authormatches:
        alist.sort(reverse = True)

    print()
    print('Authors matched.')
    print()

    # I am reversing the order of indexes so that I can delete them from
    # back to front, without changing indexes yet to be deleted.
    # This will become important in the modelingprocess module.

    masterdata, classvector = versatiletrainer2.get_dataframe(volspresent, classdictionary, vocablist, freqs_already_normalized)

    return metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist

def varying_ratios():
    if not os.path.isfile('../measuredivergence/modelstats.tsv'):
        with open('../measuredivergence/modelstats.tsv', mode = 'w', encoding = 'utf-8') as f:
            outline = 'name\tsize\tratio\taccuracy\tfeatures\tregularization\n'
            f.write(outline)

    for size in [160]:
        for pct in range(0, 110, 10):
            ratio = pct / 100
            name = 'iter4_size' + str(size) + '_ratio' + str(pct)
            vocabpath = '../measuredivergence/vocabularies/' + name + '.txt'
            metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist = get_ratio_data(vocabpath, size, ratio, excludebelow = 0, excludeabove = 3000)

            c_range = [.0001, .0003, .001, .004, .012, 0.3, 0.8, 2]
            featurestart = 1000
            featureend = 6000
            featurestep = 200
            modelparams = 'logistic', 20, featurestart, featureend, featurestep, c_range
            tags4positive = size
            tags4negative = ratio

            matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, '../measuredivergence/modeloutput/' + name + '.csv')

            with open('../measuredivergence/modelstats.tsv', mode = 'a', encoding = 'utf-8') as f:
                outline = name + '\t' + str(size) + '\t' + str(ratio) + '\t' + str(maxaccuracy) + '\t' + str(features4max) + '\t' + str(best_regularization_coef) + '\n'
                f.write(outline)

def accuracy(df, column):
    totalcount = len(df.realclass)
    tp = sum((df.realclass > 0.5) & (df[column] > 0.5))
    tn = sum((df.realclass <= 0.5) & (df[column] <= 0.5))
    fp = sum((df.realclass <= 0.5) & (df[column] > 0.5))
    fn = sum((df.realclass > 0.5) & (df[column] <= 0.5))
    assert totalcount == (tp + fp + tn + fn)

    return (tp + tn) / totalcount

def accuracy_loss(df):

    return accuracy(df, 'probability') - accuracy(df, 'alien_model')

def kl(p, q):
    """Kullback-Leibler divergence D(P || Q) for discrete distributions
    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
    Discrete probability distributions.
    """
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)

    return np.sum(np.where(p != 0, p * np.log(p / q), 0))

def compare_models():
    if not os.path.isfile('../measuredivergence/160results.tsv'):
        with open('../measuredivergence/160results.tsv', mode = 'a', encoding = 'utf-8') as f:
            outline = 'name1\tname2\tsize1\tsize2\tratiodiff\tpearson\tspearman\tloss1on2\tkl1on2\n'
            f.write(outline)

    for size in [160]:
        for pct in range(0, 110, 10):
            for size2 in [160]:
                for pct2 in range(0, 110, 10):
                    for itera in [4]:
                        for itera2 in [4]:
                            if size2 != size or pct2 != pct or itera2 != itera:
                                continue

                            name1 = '../measuredivergence/modeloutput/iter' + str(itera) + '_size' + str(size) + '_ratio' + str(pct)
                            name2 = '../measuredivergence/modeloutput/iter' + str(itera2) + '_size' + str(size2) + '_ratio' + str(pct2)

                            model1 = name1 + '.pkl'
                            meta2 = name2 + '.csv'

                            model1on2 = versatiletrainer2.apply_pickled_model(model1, '../data/', '.tsv', meta2)

                            pearson1on2 = stats.pearsonr(model1on2.probability, model1on2.alien_model)[0]
                            spearman1on2 = stats.spearmanr(model1on2.probability, model1on2.alien_model)[0]
                            loss1on2 = accuracy_loss(model1on2)
                            kl1on2 = kl(model1on2.probability, model1on2.alien_model)

                            name1 = 'iter' + str(itera) + '_size' + str(size) + '_ratio' + str(pct)
                            name2 = 'iter' + str(itera2) + '_size' + str(size2) + '_ratio' + str(pct2)

                            with open('../measuredivergence/160results.tsv', mode = 'a', encoding = 'utf-8') as f:
                                outline = name1 + '\t' + name2 + '\t' +str(size) + '\t' + str(size2) + '\t' + str(abs(pct - pct2)) + '\t' + str(pearson1on2) + '\t' + str(spearman1on2) + '\t' + str(loss1on2) + '\t' + str(kl1on2) + '\n'
                                f.write(outline)


compare_models()



