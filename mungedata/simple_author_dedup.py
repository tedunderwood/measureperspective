# simple_author_dedup.py

# the goal here is simply to go
# through a list of author names
# and find close matches
# that ought to be treated
# as the same person

import sys, csv
import pandas as pd
from difflib import SequenceMatcher

args = sys.argv[1:]

authorset = set()

for path in args:
    df = pd.read_csv('../metadata/' + path)
    for auth in df.author:
        if type(auth) == str and len(auth) > 1:
            authorset.add(auth)

delim = "), "

authorgroups = dict()

for auth in authorset:
    if len(auth) < 2:
        continue
    if auth.startswith('('):
        # a nasty thing sometimes happens
        # like (Herbert George), Wells, H. G.
        if delim in auth:
            parts = auth.split(delim)
            alternate = parts[1] + ' ' + parts[0] + ')'
            print(auth, alternate)
            lastname = alternate.split(',')[0].lower()
        else:
            print("ERROR", auth)
            lastname = auth.split(',')[0].lower()
    else:
        lastname = auth.split(',')[0].lower()

    if lastname in authorgroups:
        authorgroups[lastname].append(auth)
    else:
        authorgroups[lastname] = [auth]

translations = dict()

with open('translationtable.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        translations[row['name']] = row['bettername']

notamatch = dict()

# with open('notmatches.tsv', encoding = 'utf-8') as f:
#     for line in f:
#         parts = line.strip().split('\t')
#         notamatch[parts[0]] = parts[1]

for lastname, group in authorgroups.items():
    for authA in group:
        if authA in translations:
            continue
        for authB in group:
            if authA == authB:
                continue
                # literal equality
            if authB in notamatch and authA in notamatch[authB]:
                continue

            a = authA.strip(",. 0123456789")
            b = authB.strip(",. 0123456789")

            if a == b:
                translations[authA] = a
                translations[authB] = b
                matched = True
                continue

            setA = set(a.replace(',', ' ').replace('(', ' ').lower().split())
            setB = set(b.replace(',', ' ').replace('(', ' ').lower().split())
            unionlen = len(setA.union(setB))

            intersectlen = 0
            for aword in setA:
                if aword in setB:
                    intersectlen += 1
                elif aword[0] in setB:
                    intersectlen += 1
                    # because we count initials as matches

            if (intersectlen / unionlen) > 0.7:
                print(authA + " || " + authB)
                user = input('match? ')
                if user == 'y':
                    translateto = input('best name: ')
                    translations[authA] = translateto
                    translations[authB] = translateto
                    matched = True
                else:
                    if authA not in notamatch:
                        notamatch[authA] = set()
                    if authB not in notamatch:
                        notamatch[authB] = set()
                    notamatch[authA].add(authB)
                    notamatch[authB].add(authA)

with open('translationtable.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('name\tbettername\n')
    for k, v in translations.items():
        if k != v:
            f.write(k + '\t' + v + '\n')

with open('notmatches.tsv', mode = 'w', encoding = 'utf-8') as f:
    for k, v in notamatch.items():
        for v1 in v:
            f.write(k + '\t' + v1 + '\n')













