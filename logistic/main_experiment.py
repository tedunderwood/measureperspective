#!/usr/bin/env python3

# main_experiment.py

import sys, os, csv
import numpy as np
import pandas as pd
import versatiletrainer2
import metaselector

import matplotlib.pyplot as plt

from scipy import stats

def fantasy_periods():
    if not os.path.isfile('../results/fantasy_periods.tsv'):
        with open('../results/fantasy_periods.tsv', mode = 'w', encoding = 'utf-8') as f:
            outline = 'name\tsize\tfloor\tceiling\tmeandate\taccuracy\tfeatures\tregularization\ti\n'
            f.write(outline)

    sourcefolder = '../data/'
    metadatapath = '../metadata/mastermetadata.csv'
    tags4positive = {'fantasy_loc', 'fantasy_oclc'}
    tags4negative = {'random'}
    sizecap = 80

    periods = [(1800, 1899), (1900, 1919), (1920, 1949), (1950, 1969), (1970, 1979), (1980, 1989), (1990, 1999), (2000, 2010)]

    for excludebelow, excludeabove in periods:
        for i in range (5):

            name = 'fantasy' + str(excludebelow) + 'to' + str(excludeabove) + 'v' + str(i)

            vocabpath = '../lexica/' + name + '.txt'

            metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist = versatiletrainer2.get_simple_data(sourcefolder, metadatapath, vocabpath, tags4positive, tags4negative, sizecap, excludebelow = excludebelow, excludeabove = excludeabove)

            c_range = [.0003, .001, .006, .02, 0.1, 0.7, 3, 12]
            featurestart = 1000
            featureend = 6100
            featurestep = 200
            modelparams = 'logistic', 16, featurestart, featureend, featurestep, c_range

            matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, '../modeloutput/' + name + '.csv')

            meandate = int(round(np.sum(metadata.firstpub) / len(metadata.firstpub)))

            with open('../results/fantasy_periods.tsv', mode = 'a', encoding = 'utf-8') as f:
                outline = name + '\t' + str(sizecap) + '\t' + str(excludebelow) + '\t' + str(excludeabove) + '\t' + str(meandate) + '\t' + str(maxaccuracy) + '\t' + str(features4max) + '\t' + str(best_regularization_coef) + '\t' + str(i) + '\n'
                f.write(outline)

def sf_periods():
    if not os.path.isfile('../results/sf_periods.tsv'):
        with open('../results/sf_periods.tsv', mode = 'w', encoding = 'utf-8') as f:
            outline = 'name\tsize\tfloor\tceiling\tmeandate\taccuracy\tfeatures\tregularization\ti\n'
            f.write(outline)

    sourcefolder = '../data/'
    metadatapath = '../metadata/mastermetadata.csv'
    tags4positive = {'sf_loc', 'sf_oclc'}
    tags4negative = {'random'}
    sizecap = 80

    periods = [(1800, 1899), (1900, 1919), (1920, 1949), (1950, 1969), (1970, 1979), (1980, 1989), (1990, 1999), (2000, 2010)]

    for excludebelow, excludeabove in periods:
        for i in range (5):

            name = 'sf' + str(excludebelow) + 'to' + str(excludeabove) + 'v' + str(i)

            vocabpath = '../lexica/' + name + '.txt'

            metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist = versatiletrainer2.get_simple_data(sourcefolder, metadatapath, vocabpath, tags4positive, tags4negative, sizecap, excludebelow = excludebelow, excludeabove = excludeabove)

            c_range = [.0003, .001, .006, .02, 0.1, 0.7, 3, 12]
            featurestart = 1000
            featureend = 6100
            featurestep = 200
            modelparams = 'logistic', 16, featurestart, featureend, featurestep, c_range

            matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, '../modeloutput/' + name + '.csv')

            meandate = int(round(np.sum(metadata.firstpub) / len(metadata.firstpub)))

            with open('../results/sf_periods.tsv', mode = 'a', encoding = 'utf-8') as f:
                outline = name + '\t' + str(sizecap) + '\t' + str(excludebelow) + '\t' + str(excludeabove) + '\t' + str(meandate) + '\t' + str(maxaccuracy) + '\t' + str(features4max) + '\t' + str(best_regularization_coef) + '\t' + str(i) + '\n'
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

def averagecorr(r1, r2):
    z1 = np.arctanh(r1)
    z2 = np.arctanh(r2)
    themean = (z1 + z2) / 2
    return np.tanh(themean)

def get_divergence(sampleA, sampleB):
    '''
    This function applies model a to b, and vice versa, and returns
    a couple of measures of divergence: notably lost accuracy and
    z-tranformed spearman correlation.
    '''

    # We start by constructing the paths to the sampleA
    # standard model criteria (.pkl) and
    # model output (.csv) on the examples
    # originally used to train it.

    # We're going to try applying the sampleA standard
    # criteria to another model's output, and vice-
    # versa.

    model1 = '../modeloutput/' + sampleA + '.pkl'
    meta1 = '../modeloutput/' + sampleA + '.csv'

    # Now we construct paths to the test model
    # criteria (.pkl) and output (.csv).

    model2 = '../modeloutput/' + sampleB + '.pkl'
    meta2 = '../modeloutput/' + sampleB + '.csv'

    model1on2 = versatiletrainer2.apply_pickled_model(model1, '../data/', '.tsv', meta2)
    model2on1 = versatiletrainer2.apply_pickled_model(model2, '../data/', '.tsv', meta1)

    spearman1on2 = np.arctanh(stats.spearmanr(model1on2.probability, model1on2.alien_model)[0])
    spearman2on1 = np.arctanh(stats.spearmanr(model2on1.probability, model2on1.alien_model)[0])
    spearman = (spearman1on2 + spearman2on1) / 2

    loss1on2 = accuracy_loss(model1on2)
    loss2on1 = accuracy_loss(model2on1)
    loss = (loss1on2 + loss2on1) / 2

    return spearman, loss, spearman1on2, spearman2on1, loss1on2, loss2on1


def write_a_row(r, outfile, columns):
    with open(outfile, mode = 'a', encoding = 'utf-8') as f:
        scribe = csv.DictWriter(f, fieldnames = columns, delimiter = '\t')
        scribe.writerow(r)

def sf2fantasy_divergence():

    columns = ['testype', 'name1', 'name2', 'acc1', 'acc2', 'spearman', 'spear1on2', 'spear2on1', 'loss', 'loss1on2', 'loss2on1', 'meandate', 'ceiling', 'floor']

    outfile = '../results/sf2fantasy.tsv'

    if not os.path.isfile(outfile):
        with open(outfile, mode = 'a', encoding = 'utf-8') as f:
            scribe = csv.DictWriter(f, delimiter = '\t', fieldnames = columns)
            scribe.writeheader()

    fantasymodels = pd.read_csv('../results/fantasy_periods.tsv', sep = '\t')
    sfmodels = pd.read_csv('../results/sf_periods.tsv', sep = '\t')

    # We group both sets by the "ceiling" columns, which is just a way of grouping models
    # that cover the same period. ("Meandate" is a better representation of central
    # tendency, but it can vary from one model to the next.)

    fantasy_grouped = fantasymodels.groupby('ceiling')
    sf_grouped = sfmodels.groupby('ceiling')

    fangroups = dict()
    sfgroups = dict()

    for ceiling, group in fantasy_grouped:
        fangroups[ceiling] = group

    for ceiling, group in sf_grouped:
        sfgroups[ceiling] = group

    for ceiling, fangroup in fangroups.items():
        for i1 in fangroup.index:

            # For each fantasy model in this ceiling group,
            # first, we test it against other fantasy models
            # in the same group.

            for i2 in fangroup.index:
                if i1 == i2:
                    continue
                    # we don't test a model against itself

                r = dict()
                r['testype'] = 'fantasyself'
                r['ceiling'] = ceiling
                r['floor'] = fangroup.loc[i1, 'floor']
                r['name1'] = fangroup.loc[i1, 'name']
                r['name2'] = fangroup.loc[i2, 'name']
                r['spearman'], r['loss'], r['spear1on2'], r['spear2on1'], r['loss1on2'], r['loss2on1'] = get_divergence(r['name1'], r['name2'])
                r['acc1'] = fangroup.loc[i1, 'accuracy']
                r['acc2'] = fangroup.loc[i2, 'accuracy']
                r['meandate'] = (fangroup.loc[i1, 'meandate'] + fangroup.loc[i2, 'meandate']) / 2

                write_a_row(r, outfile, columns)

            sfgroup = sfgroups[ceiling]
            for idx in sfgroup.index:

                r = dict()
                r['testype'] = 'cross'
                r['ceiling'] = ceiling
                r['floor'] = fangroup.loc[i1, 'floor']
                r['name1'] = fangroup.loc[i1, 'name']
                r['name2'] = sfgroup.loc[idx, 'name']
                r['spearman'], r['loss'], r['spear1on2'], r['spear2on1'], r['loss1on2'], r['loss2on1'] = get_divergence(r['name1'], r['name2'])
                r['acc1'] = fangroup.loc[i1, 'accuracy']
                r['acc2'] = sfgroup.loc[idx, 'accuracy']
                r['meandate'] = (fangroup.loc[i1, 'meandate'] + sfgroup.loc[idx, 'meandate']) / 2

                write_a_row(r, outfile, columns)

    # Now sf versus itself

    for ceiling, sfgroup in sfgroups.items():
        for i1 in sfgroup.index:

            # For each sf model in this ceiling group,
            # we test it against other sf models
            # in the same group.

            for i2 in sfgroup.index:
                if i1 == i2:
                    continue
                    # we don't test a model against itself

                r = dict()
                r['testype'] = 'sfself'
                r['ceiling'] = ceiling
                r['floor'] = sfgroup.loc[i1, 'floor']
                r['name1'] = sfgroup.loc[i1, 'name']
                r['name2'] = sfgroup.loc[i2, 'name']
                r['spearman'], r['loss'], r['spear1on2'], r['spear2on1'], r['loss1on2'], r['loss2on1'] = get_divergence(r['name1'], r['name2'])
                r['acc1'] = sfgroup.loc[i1, 'accuracy']
                r['acc2'] = sfgroup.loc[i2, 'accuracy']
                r['meandate'] = (sfgroup.loc[i1, 'meandate'] + sfgroup.loc[i2, 'meandate']) / 2

                write_a_row(r, outfile, columns)

sf2fantasy_divergence()
