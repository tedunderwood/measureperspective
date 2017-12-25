#!/usr/bin/env python3

# metaselector.py

# Functions that select positive and negative
# instances to be used in a model.

# Loosely based on metafilter.py, but I'm adopting
# a different strategy. Instead of building a single
# function that does everything; I'm going to allow
# many different ways of generating the same data
# structures. That way you won't always have to pass
# a million parameters not needed for a specific problem.

# Loosely there are two stages here. First, load a
# metadata file and prune away any rows that need to be
# excluded. If necessary, create columns with standard names.
# This returns simply a pandas dataframe.

# Next, select positive and negative instances, using one
# of a variety of systems. This returns a list of
# IDstouse and a classdictionary.

import random, math
import pandas as pd
import numpy as np

def add_standard_date(metadata, datecols):
    ''' Adds a 'std_date' column to the metadata table, and
    fills it using best available non-missing date in one of
    several other columns'''

    rowcount = metadata.shape[0]
    zeroes = np.zeros(rowcount, dtype = 'int16')
    metadata = metadata.assign(std_date = zeroes)

    for rowidx in metadata.index:
        for col in datecols:

            try:
                intdate = int(metadata.loc[rowidx, col])
            except:
                intdate = float('nan')
                print(rowidx, metadata.loc[rowidx, col], col)

            if not math.isnan(intdate) and intdate > 1:
                metadata.loc[rowidx, 'std_date'] = intdate
                break

    return metadata

def tags2tagset(x):
    ''' function that will be applied to transform
    fantasy|science-fiction into {'fantasy', 'science-fiction'} '''
    if type(x) == float:
        return set()
    else:
        return set(x.split('|'))

def load_metadata(metapath, docidsindata, excludebelow, excludeabove, indexcol = 'docid', datecols = ['firstpub'], genrecol = 'tags'):
    '''
    Very basic function that reads a pandas dataframe,
       * filters for availability of the data,
       * creates a standard column for volume date (std_date)
       * creates a column of sets that contain genretags (tagset)
       * and then trims the dataframe using chronological limits.
    '''

    metadata = pd.read_csv(metapath, index_col = indexcol)

    initialrowct = metadata.shape[0]
    docidsindata = set(metadata.index) & set(docidsindata)
    metadata = metadata.loc[docidsindata]
    filteredrowct = metadata.shape[0]

    if initialrowct != filteredrowct:
        difference = initialrowct - filteredrowct
        print('We started with ' + str(initialrowct) + ' rows in metadata, but')
        print('lost ' + str(difference) + ' that were missing in the data folder.')

    # A situation that very often happens: I want to use date of first publication
    # where I have it, but I have left many blanks in that column where I don't
    # have the info. In that situation, you can provide two date columns,
    # and add_standard_date will use #1, if nonmissing, or #2.

    metadata = add_standard_date(metadata, datecols)

    # Now we transform a column of pipe-separated genre tags (fantasy|scifi)
    # into a column of sets that can more easily be tested.

    column_of_sets = metadata[genrecol].apply(tags2tagset)
    metadata = metadata.assign(tagset = column_of_sets)

    # Finally filter by date. Notice that both limits are inclusive.

    metadata = metadata[(metadata.std_date >= excludebelow) & (metadata.std_date <= excludeabove)]

    return metadata

def match_negatives(metadata, positives, allnegatives):
    '''
    A selection strategy that attempts to closely match the
    dates of positive and negative instances.
    '''

    random.shuffle(allnegatives)

    negatives = []

    # then, we would like to get negative instances
    # as close as possible to the dates of the positive ones,
    # but with some stochastic variation

    for instance in positives:
        targetdate = metadata.loc[instance, 'std_date']
        tuplelist = []

        for candidate in allnegatives:
            diff = abs(targetdate - metadata.loc[candidate, 'std_date'])
            tuplelist.append((diff, candidate))

        tuplelist.sort(key = lambda x: x[0])
        # we only sort by the distances between voldate
        # and targetdate; alphabetic sort on the second
        # element of the tuple, docid, is forbidden.

        if len(tuplelist) < 2:
            k = len(tuplelist)
        else:
            k = 2

        contestants = [x[1] for x in tuplelist[0 : k]]

        choice = random.sample(contestants, 1)[0]

        allnegatives.pop(allnegatives.index(choice))
        negatives.append(choice)

    return negatives

def select_instances(metadata, sizecap, tags4positive, tags4negative, forbid4positive = {'allnegative'}, forbid4negative = {'allpositive'}, negative_strategy = 'random'):

    '''Selects instances of the positive class and negative class, trying to
    hit sizecap,but not allowing imbalanced classes. For both positive and
    negative classes, we have a set of tags necessary for inclusion, and those
    that forbid inclusion. This allows us to treat overlapping categories
    in a variety of ways. Default behavior is that all positive tags are
    forbidden in negative class, and vice-versa. But this can be overridden.'''

    if 'allnegative' in forbid4positive:
        forbid4positive = tags4negative

    if 'allpositive' in forbid4negative:
        forbid4negative = tags4positive

    allnegatives = []
    allpositives = []
    weird_counter = 0

    for idx, row in metadata.iterrows():
        posintersect = len(row['tagset'] & tags4positive)
        negintersect = len(row['tagset'] & tags4negative)

        if posintersect and not negintersect:
            pos = True
        else:
            pos = False

        if negintersect and not posintersect:
            neg = True
        else:
            neg = False

        if pos and neg:
            # in the odd case where an instance could belong
            # to either class, we aim for balanced classes
            # (this should rarely happen in practice)

            weird_counter += 1

            if len(allpositives) > len(allnegatives):
                allnegatives.append(idx)
            else:
                allpositives.append(idx)

        elif pos:
            allpositives.append(idx)

        elif neg:
            allnegatives.append(idx)

    # now let's decide how many instances per class

    numpositive = len(allpositives)
    numnegative = len(allnegatives)

    numinstances = min(sizecap, numpositive, numnegative)

    print()
    print('We have ' + str(numpositive) + ' potential positive instances and')
    print(str(numnegative) + ' potential negative instances. Choosing only')
    print(str(numinstances) + ' of each class.')

    if weird_counter:
        print('By the way, there were ' + str(weird_counter) + ' instances')
        print('that could have belonged to either class.')

    print()

    # we randomly sample positive instances
    positives = random.sample(allpositives, numinstances)

    # Now there are two different ways to select
    # negative instances. If it's just random, that's simple

    if negative_strategy == 'random':
        negatives = random.sample(allnegatives, numinstances)

    # but we can also closely match dates

    else:
        negatives = match_negatives(metadata, positives, allnegatives)

    orderedIDs = []
    classdictionary = dict()

    for anid in positives:
        orderedIDs.append(anid)
        classdictionary[anid] = 1

    for anid in negatives:
        orderedIDs.append(anid)
        classdictionary[anid] = 0

    print('Instances chosen.')

    return orderedIDs, classdictionary

def set_positive_ratio(metadata, sizecap, tags4positive1, tags4positive2, ratio, tags4negative):

    '''An experimental function that allows the user to adjust the balance of two different
    positive classes. The classes are treated as exclusive.'''

    allnegatives = []
    allpositive1 = []
    allpositive2 = []

    for idx, row in metadata.iterrows():
        pos1intersect = len(row['tagset'] & tags4positive1)
        pos2intersect = len(row['tagset'] & tags4positive2)
        negintersect = len(row['tagset'] & tags4negative)

        if pos1intersect and not pos2intersect:
            allpositive1.append(idx)

        elif pos2intersect and not pos1intersect:
            allpositive2.append(idx)

        elif negintersect:
            allnegatives.append(idx)

    print()
    print('Selecting ' + str(sizecap) + ' instances at a ratio of ' + str(ratio) + '.')
    print()

    positive1ct = int(sizecap * ratio)
    positive2ct = int(sizecap - positive1ct)

    # we randomly sample positive instances
    positives = random.sample(allpositive1, positive1ct)
    positives.extend(random.sample(allpositive2, positive2ct))

    negatives = random.sample(allnegatives, sizecap)

    orderedIDs = []
    classdictionary = dict()

    for anid in positives:
        orderedIDs.append(anid)
        classdictionary[anid] = 1

    for anid in negatives:
        orderedIDs.append(anid)
        classdictionary[anid] = 0

    print('Instances chosen.')

    return orderedIDs, classdictionary

def dilute_positive_class(metadata, sizecap, tags4positive, tags4negative, ratio):

    '''An experimental function that allows the user to dilute the positive class with negative examples in a fixed ratio, blurring the model.'''

    allnegatives = []
    allpositives = []

    for idx, row in metadata.iterrows():
        posintersect = len(row['tagset'] & tags4positive)
        negintersect = len(row['tagset'] & tags4negative)

        if posintersect and not negintersect:
            allpositives.append(idx)

        elif negintersect:
            allnegatives.append(idx)

    print()
    print('Selecting ' + str(sizecap) + ' instances at a ratio of ' + str(ratio) + '.')
    print()

    dilution_ct = int(sizecap * ratio)
    real_positive_ct = int(sizecap - dilution_ct)

    # we randomly sample positive instances

    real_positives = random.sample(allpositives, real_positive_ct)

    dilution = random.sample(allnegatives, dilution_ct)

    for d in dilution:
        allnegatives.pop(allnegatives.index(d))
        # we don't want instances on both sides of the
        # boundary

    real_positives.extend(dilution)

    negatives = random.sample(allnegatives, sizecap)

    orderedIDs = []
    classdictionary = dict()

    for anid in real_positives:
        orderedIDs.append(anid)
        classdictionary[anid] = 1

    for anid in negatives:
        orderedIDs.append(anid)
        classdictionary[anid] = 0

    print('Instances chosen.')

    return orderedIDs, classdictionary






















