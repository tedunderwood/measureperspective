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

fantasy_periods()
