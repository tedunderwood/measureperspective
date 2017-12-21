# fusing_old_and_new_fiction.py

# This script concatenates my two
# fiction metadata sets.

import csv
import SonicScrewdriver as utils

secondfile = '../../noveltmmeta/pre1923hathifiction.csv'
firstfile = '../../noveltmmeta/incopyrightfiction.csv'

allrows = []

with open(firstfile, encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        allrows.append(row)

with open(secondfile, encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        allrows.append(row)

fieldnames = ['docid', 'recordid', 'oclc', 'locnum', 'author', 'authordate', 'imprint', 'inferreddate', 'place', 'enumcron', 'subjects', 'genres', 'title']

with open('../rawdata/all_fiction.csv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames, extrasaction = 'ignore')
    writer.writeheader()
    for row in allrows:
        if 'htid' in row:
            row['docid'] = row['htid']

        if 'inferreddate' not in row:
            row['inferreddate'] = utils.date_row(row)
        if 'authordate' not in row:
            row['authordate'] = ''
        if 'genres' not in row:
            genres = ''

        writer.writerow(row)
