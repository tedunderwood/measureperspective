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

def get_ratio_data(vocabpath, sizecap, ratio, tags4positive, tags4negative, excludebelow = 0, excludeabove = 3000):

    ''' Loads metadata, selects instances for the positive
    and negative classes (using a ratio to dilute the positive
    class with negative instances), creates a lexicon if one doesn't
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
    numfeatures = 8000

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

    orderedIDs, classdictionary = metaselector.dilute_positive_class(metadata, sizecap, tags4positive, tags4negative, ratio)

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

def vary_sf_ratio_against_random():
    if not os.path.isfile('../measuredivergence/modeldata.tsv'):
        with open('../measuredivergence/modeldata.tsv', mode = 'w', encoding = 'utf-8') as f:
            outline = 'name\tsize\tratio\taccuracy\tfeatures\tregularization\n'
            f.write(outline)

    size = 80

    for iteration in [5, 6, 7]:

        ceiling = 105
        if iteration == 7:
            ceiling = 5

        for pct in range(0, ceiling, 5):
            ratio = pct / 100
            name = 'iter' + str(iteration) + '_size' + str(size) + '_ratio' + str(pct)

            vocabpath = '../measuredivergence/vocabularies/' + name + '.txt'
            tags4positive = {'sf_loc', 'sf_oclc'}
            tags4negative = {'random'}

            metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist = get_ratio_data(vocabpath, size, ratio, tags4positive, tags4negative, excludebelow = 0, excludeabove = 3000)

            c_range = [.00005, .0003, .001, .004, .012, 0.2, 0.8]
            featurestart = 1000
            featureend = 6000
            featurestep = 200
            modelparams = 'logistic', 20, featurestart, featureend, featurestep, c_range
            tags4positive = size
            tags4negative = ratio

            matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, '../measuredivergence/modeloutput/' + name + '.csv', write_fullmodel = True)

            with open('../measuredivergence/modeldata.tsv', mode = 'a', encoding = 'utf-8') as f:
                outline = name + '\t' + str(size) + '\t' + str(ratio) + '\t' + str(maxaccuracy) + '\t' + str(features4max) + '\t' + str(best_regularization_coef) + '\n'
                f.write(outline)

def vary_fantasy_ratio_against_sf():
    if not os.path.isfile('../measuredivergence/modeldata.tsv'):
        with open('../measuredivergence/modeldata.tsv', mode = 'w', encoding = 'utf-8') as f:
            outline = 'name\tsize\tratio\taccuracy\tfeatures\tregularization\n'
            f.write(outline)

    size = 80

    for iteration in [8, 9, 10]:

        ceiling = 105
        if iteration == 10:
            ceiling = 5

        for pct in range(0, ceiling, 5):
            ratio = pct / 100
            name = 'iter' + str(iteration) + '_size' + str(size) + '_ratio' + str(pct)

            vocabpath = '../measuredivergence/vocabularies/' + name + '.txt'
            tags4positive = {'fantasy_loc', 'fantasy_oclc'}
            tags4negative = {'sf_loc', 'sf_oclc'}

            metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist = get_ratio_data(vocabpath, size, ratio, tags4positive, tags4negative, excludebelow = 0, excludeabove = 3000)

            c_range = [.00005, .0003, .001, .004, .012, 0.2, 0.8, 3]
            featurestart = 2000
            featureend = 8000
            featurestep = 200
            modelparams = 'logistic', 12, featurestart, featureend, featurestep, c_range
            tags4positive = size
            tags4negative = ratio

            matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, '../measuredivergence/modeloutput/' + name + '.csv', write_fullmodel = True)

            with open('../measuredivergence/modeldata.tsv', mode = 'a', encoding = 'utf-8') as f:
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

def kldivergence(p, q):
    """Kullback-Leibler divergence D(P || Q) for discrete distributions
    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
    Discrete probability distributions.
    """
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)

    return np.sum(np.where(p != 0, p * np.log(p / q), 0))

def averagecorr(r1, r2):
    z1 = np.arctanh(r1)
    z2 = np.arctanh(r2)
    themean = (z1 + z2) / 2
    return np.tanh(themean)

def measure_sf_divergences():
    if not os.path.isfile('../measuredivergence/divergences.tsv'):
        with open('../measuredivergence/divergences.tsv', mode = 'a', encoding = 'utf-8') as f:
            outline = 'name1\tname2\tsize1\tsize2\tacc1\tacc2\tratiodiff\tpearson\tspearman\tspearman2on1\tloss\tkl\n'
            f.write(outline)

    goldstandards = ['iter5_size80_ratio0', 'iter6_size80_ratio0', 'iter7_size80_ratio0']
    size = 80

    modeldata = pd.read_csv('../measuredivergence/modeldata.tsv', sep = '\t', index_col = 'name')

    for gold in goldstandards:
        for itera in [5, 6]:
            for pct in range(0, 105, 5):
                ratio = pct / 100

                model1 = '../measuredivergence/modeloutput/' + gold + '.pkl'
                meta1 = '../measuredivergence/modeloutput/' + gold + '.csv'

                testpath = '../measuredivergence/modeloutput/iter' + str(itera) + '_size' + str(size) + '_ratio' + str(pct)

                testname = 'iter' + str(itera) + '_size' + str(size) + '_ratio' + str(pct)

                if testname == gold:
                    continue
                    # we don't test a model against itself.
                if testname != 'iter7_size80_ratio0' and ratio != 0:
                    continue
                    # we're extending previous work

                model2 = testpath + '.pkl'
                meta2 = testpath + '.csv'

                acc1 = modeldata.loc[gold, 'accuracy']
                acc2 = modeldata.loc[testname, 'accuracy']

                model1on2 = versatiletrainer2.apply_pickled_model(model1, '../data/', '.tsv', meta2)
                model2on1 = versatiletrainer2.apply_pickled_model(model2, '../data/', '.tsv', meta1)

                pearson1on2 = stats.pearsonr(model1on2.probability, model1on2.alien_model)[0]
                pearson2on1 = stats.pearsonr(model2on1.probability, model2on1.alien_model)[0]
                pearson = averagecorr(pearson1on2, pearson2on1)

                spearman1on2 = stats.spearmanr(model1on2.probability, model1on2.alien_model)[0]
                spearman2on1 = stats.spearmanr(model2on1.probability, model2on1.alien_model)[0]
                spearman = averagecorr(pearson1on2, pearson2on1)

                loss1on2 = accuracy_loss(model1on2)
                loss2on1 = accuracy_loss(model2on1)
                loss = (loss1on2 + loss2on1) / 2

                kl1on2 = kldivergence(model1on2.probability, model1on2.alien_model)
                kl2on1 = kldivergence(model2on1.probability, model2on1.alien_model)
                kl = (kl1on2 + kl2on1) / 2

                with open('../measuredivergence/divergences.tsv', mode = 'a', encoding = 'utf-8') as f:
                    outline = gold + '\t' + testname + '\t' +str(size) + '\t' + str(size) + '\t' + str(acc1) + '\t' + str(acc2) + '\t' + str(ratio) + '\t' + str(pearson) + '\t' + str(spearman) + '\t' + str(spearman2on1) + '\t' + str(loss) + '\t' + str(kl) + '\n'
                    f.write(outline)

vary_fantasy_ratio_against_sf()



