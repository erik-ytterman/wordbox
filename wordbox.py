#! /usr/bin/python3
import sys
import random
import re

# Contain playfield state
class playstate:
    data = None
    size = (0,0)

    def __init__(self, rows, columns):
        self.size = (rows, columns)
        self.data = [ [ '.' for i in range(columns) ] for j in range(rows) ]

    def getsize(self):
        return self.size

    def setrow(self, word, index):
        self.data[index] = list(word)

    def getrow(self, index):
        return ''.join(self.data[index])

    def getkeys(self):
        return [ ''.join(t) for t in tuple(zip(*self.data)) ]

    def dumptext(self, index = None):
        if index == None:
            for row in self.data:
                print(''.join(row))
        else:
            print(self.data[index])

# Validate playfield state
class statevalidator:
    wordlist = None

# Find possible new playfield states
class statefinder:
    wordlist = None

    def __init__(self, wordlist):
        print(len(wordlist))
        self.wordlist = wordlist

    def states(state):
        return

# Store playfield state graph
class treenode:
    state = None
    children = []

    def __init__(self, state):
        self.state = state

##########################################################################################

def treebuilder(rootnode):
    return None

count = 5

normalizer = lambda line: line.strip().upper()

worddata = [ normalizer(word) for word in open("swedish-word-list.txt", encoding="ISO-8859-1") ]

wordlist = tuple( { word for word in sorted(worddata) if len(word) == count } )

state = playstate(count, count)

validator = statevalidator()

finder = statefinder(wordlist)

print(50 * '-');
state.dumptext()

state.setrow("BEPAN",0)
state.setrow("URNAN",1)

print(50 * '-');
state.dumptext()

print(50 * '-');

keys = state.getkeys()

for key in keys:
    print("Matching '" + key + "' ...")
    words = [ w for w in wordlist if re.match(key, w) ]
    print(words)
