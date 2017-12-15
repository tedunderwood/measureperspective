# intersection_of_sf.py

# This script uses Library of Congress tags,
# plus a list of volumes called "science fiction"
# by the OCLC, to extract Hathi vols likely to
# be SF. Some further manual grooming
# will be required.

import csv
from difflib import SequenceMatcher
import SonicScrewdriver as utils

def titleregularize(title):

    title = title.lower().strip('/ .,:-')
    title = title.replace('the', 'x')
    if len(title) < 4:
        title = title + "    "
    firstchars = title[0:3]

    return title, firstchars

def authorregularize(author):
    author = author.strip('/ ,.:123456789-').lower()
    return author

oclc = set()
sftitles = dict()

with open('../rawdata/oclc_science_fiction.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        oclc.add(row['oclcwi'])
        if len(row['title']) > 10:
            title, firstchars = titleregularize(row['title'])
            author = authorregularize(row['author'].split('|')[0])
            if firstchars not in sftitles:
                sftitles[firstchars] = set()

            sftitles[firstchars].add((title, author))

def isitsf(row):

    global oclc, sftitles

    sf = False
    reason = ''

    if 'Science fiction' in row['subjects']:
        sf = True
        reason = 'taggedsf'
    elif 'Science fiction' in row['imprint']:
        sf = True
        reason = 'taggedsf'
    elif row['oclc'] in oclc:
        sf = True
        reason = 'oclcid'
    else:
        title = row['title']
        firstpart = title.split('|')[0]
        if len(firstpart) < 10:
            return sf, reason

        title, firstchars = titleregularize(firstpart)

        if firstchars not in sftitles:
            return sf, reason

        author = authorregularize(row['author'])

        for t, a in sftitles[firstchars]:
            m = SequenceMatcher(None, title, t)
            ratio = m.real_quick_ratio()
            if ratio > 0.8:
                betterratio = m.ratio()
                n = SequenceMatcher(None, author, a)
                authorratio = n.ratio()
                if betterratio > 0.9 and authorratio > 0.7:
                    print(t, title, a, author)
                    sf = True
                    reason = 'fuzzymatch'

    return sf, reason

counter = 0
fuzzycounter = 0
reasons = dict()
allsf = []

def get_matches(filepath, allsf, counter, fuzzycounter, reasons):
    with open(filepath, encoding = 'utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            if counter  % 100 == 1:
                print(counter)
            counter += 1

            if 'htid' in row:
                docid = row['htid']
            else:
                docid = row['docid']

            sf, reason = isitsf(row)

            if sf:
                allsf.append(row)
                reasons[docid] = reason

                if reason == 'fuzzymatch':
                    fuzzycounter += 1

    return allsf, counter, fuzzycounter, reasons

secondfile = '../../noveltmmeta/pre1923hathifiction.csv'
firstfile = '../../noveltmmeta/incopyrightfiction.csv'

allsf, counter, fuzzycounter, reasons = get_matches(firstfile, allsf, counter, fuzzycounter, reasons)

print()
print('A total of ' + str(counter) + ' volumes were scanned.')
print()

allsf, counter, fuzzycounter, reasons = get_matches(secondfile, allsf, counter, fuzzycounter, reasons)

fieldnames = ['docid', 'recordid', 'oclc', 'locnum', 'includedbc', 'author', 'authordate', 'imprint', 'inferreddate', 'place', 'enumcron', 'subjects', 'genres', 'title']

print()
print('A total of ' + str(counter) + ' volumes were scanned.')
print()
print('A total of ' + str(fuzzycounter) + ' volumes were fuzzymatched.')
print()

with open('../rawdata/sf_intersection.csv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames, extrasaction = 'ignore')
    writer.writeheader()
    for row in allsf:
        if 'htid' in row:
            row['docid'] = row['htid']
        row['includedbc'] = reasons[row['docid']]

        if 'inferreddate' not in row:
            row['inferreddate'] = utils.date_row(row)
        if 'authordate' not in row:
            row['authordate'] = ''
        if 'genres' not in row:
            genres = ''

        if ' / |' in row['title']:
            row['title'] = row['title'].split(' / |')[0]

        writer.writerow(row)
