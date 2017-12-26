#!/usr/bin/env python3

# methodological_experiment.py

import sys, os, csv
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
            featurestep = 300
            modelparams = 'logistic', 16, featurestart, featureend, featurestep, c_range

            matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, '../measuredivergence/modeloutput/' + name + '.csv', write_fullmodel = False)
            # It's important not to write fullmodel if you want the csvs
            # to accurately reflect terrible accuracy on diluted datasets.
            # write_fullmodel = False forces crossvalidation.

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
            featureend = 7500
            featurestep = 400
            modelparams = 'logistic', 16, featurestart, featureend, featurestep, c_range

            matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, '../measuredivergence/modeloutput/' + name + '.csv', write_fullmodel = False)
            # write_fullmodel = False forces crossvalidation.

            with open('../measuredivergence/modeldata.tsv', mode = 'a', encoding = 'utf-8') as f:
                outline = name + '\t' + str(size) + '\t' + str(ratio) + '\t' + str(maxaccuracy) + '\t' + str(features4max) + '\t' + str(best_regularization_coef) + '\n'
                f.write(outline)

def vary_fantasy_ratio_against_random():
    if not os.path.isfile('../measuredivergence/modeldata.tsv'):
        with open('../measuredivergence/modeldata.tsv', mode = 'w', encoding = 'utf-8') as f:
            outline = 'name\tsize\tratio\taccuracy\tfeatures\tregularization\n'
            f.write(outline)

    size = 80

    for iteration in [11, 12, 13]:

        ceiling = 105
        if iteration == 13:
            ceiling = 5

        for pct in range(0, ceiling, 5):
            ratio = pct / 100
            name = 'iter' + str(iteration) + '_size' + str(size) + '_ratio' + str(pct)

            vocabpath = '../measuredivergence/vocabularies/' + name + '.txt'
            tags4positive = {'fantasy_loc', 'fantasy_oclc'}
            tags4negative = {'random'}

            metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist = get_ratio_data(vocabpath, size, ratio, tags4positive, tags4negative, excludebelow = 0, excludeabove = 3000)

            c_range = [.00005, .0003, .001, .004, .012, 0.2, 0.8, 3]
            featurestart = 1600
            featureend = 6400
            featurestep = 400
            modelparams = 'logistic', 16, featurestart, featureend, featurestep, c_range

            matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, '../measuredivergence/modeloutput/' + name + '.csv', write_fullmodel = False)
            # write_fullmodel = False forces crossvalidation.

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

def get_divergences(gold, testname, itera, size, pct):
    '''
    This function gets several possible measures of divergence
    between two models.
    '''

    # We start by constructing the paths to the gold
    # standard model criteria (.pkl) and
    # model output (.csv) on the examples
    # originally used to train it.

    # We're going to try applying the gold standard
    # criteria to another model's output, and vice-
    # versa.

    model1 = '../measuredivergence/modeloutput/' + gold + '.pkl'
    meta1 = '../measuredivergence/modeloutput/' + gold + '.csv'

    # Now we construct paths to the test model
    # criteria (.pkl) and output (.csv).

    testpath = '../measuredivergence/modeloutput/' + testname
    model2 = testpath + '.pkl'
    meta2 = testpath + '.csv'

    model1on2 = versatiletrainer2.apply_pickled_model(model1, '../data/', '.tsv', meta2)
    model2on1 = versatiletrainer2.apply_pickled_model(model2, '../data/', '.tsv', meta1)

    pearson1on2 = stats.pearsonr(model1on2.probability, model1on2.alien_model)[0]
    pearson2on1 = stats.pearsonr(model2on1.probability, model2on1.alien_model)[0]
    pearson = averagecorr(pearson1on2, pearson2on1)

    spearman1on2 = stats.spearmanr(model1on2.probability, model1on2.alien_model)[0]
    spearman2on1 = stats.spearmanr(model2on1.probability, model2on1.alien_model)[0]
    spearman = averagecorr(spearman1on2, spearman2on1)

    loss1on2 = accuracy_loss(model1on2)
    loss2on1 = accuracy_loss(model2on1)
    loss = (loss1on2 + loss2on1) / 2

    kl1on2 = kldivergence(model1on2.probability, model1on2.alien_model)
    kl2on1 = kldivergence(model2on1.probability, model2on1.alien_model)
    kl = (kl1on2 + kl2on1) / 2

    return pearson, spearman, loss, kl, spearman1on2, spearman2on1, loss1on2, loss2on1

def measure_sf_divergences():

    columns = ['name1', 'name2', 'size', 'acc1', 'acc2', 'ratiodiff', 'pearson', 'spearman', 'spear1on2', 'spear2on1', 'loss', 'loss1on2', 'loss2on1', 'kl']

    if not os.path.isfile('../measuredivergence/sf_divergences.tsv'):
        with open('../measuredivergence/sf_divergences.tsv', mode = 'a', encoding = 'utf-8') as f:
            scribe = csv.DictWriter(f, delimiter = '\t', fieldnames = columns)
            scribe.writeheader()

    goldstandards = ['iter5_size80_ratio0', 'iter6_size80_ratio0', 'iter7_size80_ratio0']
    size = 80

    modeldata = pd.read_csv('../measuredivergence/modeldata.tsv', sep = '\t', index_col = 'name')

    for gold in goldstandards:
        for itera in [5, 6]:
            for pct in range(0, 105, 5):
                ratio = pct / 100

                testname = 'iter' + str(itera) + '_size' + str(size) + '_ratio' + str(pct)

                if testname == gold:
                    continue
                    # we don't test a model against itself
                else:
                    row = dict()
                    row['pearson'], row['spearman'], row['loss'], row['kl'], row['spear1on2'], row['spear2on1'], row['loss1on2'], row['loss2on1'] = get_divergences(gold, testname, itera, size, pct)

                row['name1'] = gold
                row['name2'] = testname
                row['size'] = size
                row['acc1'] = modeldata.loc[gold, 'accuracy']
                row['acc2'] = modeldata.loc[testname, 'accuracy']
                row['ratiodiff'] = ratio

                with open('../measuredivergence/sf_divergences.tsv', mode = 'a', encoding = 'utf-8') as f:
                    scribe = csv.DictWriter(f, delimiter = '\t', fieldnames = columns)
                    scribe.writerow(row)

def measure_fsf_divergences():

    columns = ['name1', 'name2', 'size', 'acc1', 'acc2', 'ratiodiff', 'pearson', 'spearman', 'spear1on2', 'spear2on1', 'loss', 'loss1on2', 'loss2on1', 'kl']

    if not os.path.isfile('../measuredivergence/fsf_divergences.tsv'):
        with open('../measuredivergence/fsf_divergences.tsv', mode = 'a', encoding = 'utf-8') as f:
            scribe = csv.DictWriter(f, delimiter = '\t', fieldnames = columns)
            scribe.writeheader()

    goldstandards = ['iter8_size80_ratio0', 'iter9_size80_ratio0', 'iter10_size80_ratio0']
    size = 80

    modeldata = pd.read_csv('../measuredivergence/modeldata.tsv', sep = '\t', index_col = 'name')

    for gold in goldstandards:
        for itera in [8, 9]:
            for pct in range(0, 105, 5):
                ratio = pct / 100

                testname = 'iter' + str(itera) + '_size' + str(size) + '_ratio' + str(pct)

                if testname == gold:
                    continue
                    # we don't test a model against itself
                else:
                    row = dict()
                    row['pearson'], row['spearman'], row['loss'], row['kl'], row['spear1on2'], row['spear2on1'], row['loss1on2'], row['loss2on1'] = get_divergences(gold, testname, itera, size, pct)

                row['name1'] = gold
                row['name2'] = testname
                row['size'] = size
                row['acc1'] = modeldata.loc[gold, 'accuracy']
                row['acc2'] = modeldata.loc[testname, 'accuracy']
                row['ratiodiff'] = ratio

                with open('../measuredivergence/fsf_divergences.tsv', mode = 'a', encoding = 'utf-8') as f:
                    scribe = csv.DictWriter(f, delimiter = '\t', fieldnames = columns)
                    scribe.writerow(row)

def measure_fantasy_divergences():

    columns = ['name1', 'name2', 'size', 'acc1', 'acc2', 'ratiodiff', 'pearson', 'spearman', 'spear1on2', 'spear2on1', 'loss', 'loss1on2', 'loss2on1', 'kl']

    if not os.path.isfile('../measuredivergence/fantasy_divergences.tsv'):
        with open('../measuredivergence/fantasy_divergences.tsv', mode = 'a', encoding = 'utf-8') as f:
            scribe = csv.DictWriter(f, delimiter = '\t', fieldnames = columns)
            scribe.writeheader()

    goldstandards = ['iter11_size80_ratio0', 'iter12_size80_ratio0', 'iter13_size80_ratio0']
    size = 80

    modeldata = pd.read_csv('../measuredivergence/modeldata.tsv', sep = '\t', index_col = 'name')

    for gold in goldstandards:
        for itera in [11, 12]:
            for pct in range(0, 105, 5):
                ratio = pct / 100

                testname = 'iter' + str(itera) + '_size' + str(size) + '_ratio' + str(pct)

                if testname == gold:
                    continue
                    # we don't test a model against itself
                else:
                    row = dict()
                    row['pearson'], row['spearman'], row['loss'], row['kl'], row['spear1on2'], row['spear2on1'], row['loss1on2'], row['loss2on1'] = get_divergences(gold, testname, itera, size, pct)

                row['name1'] = gold
                row['name2'] = testname
                row['size'] = size
                row['acc1'] = modeldata.loc[gold, 'accuracy']
                row['acc2'] = modeldata.loc[testname, 'accuracy']
                row['ratiodiff'] = ratio

                with open('../measuredivergence/fantasy_divergences.tsv', mode = 'a', encoding = 'utf-8') as f:
                    scribe = csv.DictWriter(f, delimiter = '\t', fieldnames = columns)
                    scribe.writerow(row)

measure_fantasy_divergences()



