#! /usr/bin/python3
import sys
import random

class treenode:
    

count = 5

normalizer = lambda line: line.strip().upper()

worddata = [ normalizer(word) for word in open("swedish-word-list.txt", encoding="ISO-8859-1") ]

wordlist = tuple( { word for word in sorted(worddata) if len(word) == count } )

rows = list()

for i in range(count):
    if not rows:
        candidates = wordlist
    else:
        candidates = ("APANS",)

    rows.append(random.choice(candidates))

def addnode(parent, candidates)

    
print("-" * 40)
for i, row in enumerate(rows):
    print(i, row)
