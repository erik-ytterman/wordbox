#! /usr/bin/python3
import sys
import random
import itertools
import copy
import re

class treenode:
    state = None
    parent = None
    children = []
    
    def __init__(self, state, parent):
        self.parent = parent
        self.state = list(state)

    def addword(self, word):
        self.state.append(word)

    def addchild(self, childnode):
        self.children.append(childnode)

def charmatcher(word, charsets):
    return ( False not in [ word[i] in charsets[i] for i in range(max(len(word), len(charsets))) ] )
        
def wordmatcher(state, wordset):
    if state == []:
        return wordset
    else:
        # Extract the possible words in the columns, filtered by the previous words
        columnkeys = [ ''.join(t) for t in zip(*state) ]

        # Extract possible words for every column
        words = [ [ w for w in wordset if w.startswith(columnkey) ] for columnkey in columnkeys ]
        
        # Extract and "uniqify" possible letters per position in row to be selected
        charsets = [ set([ l[len(state)] for l in word ]) for word in words ]

        return { word for word in wordset if charmatcher(word, charsets) }

def treebuilder(node, depth, maxdepth, wordset, solutions):
    if depth < maxdepth:
        for word in wordmatcher(node.state, wordset):
            newnode = treenode(node.state, node)
            newnode.addword(word)
            
            node.addchild(newnode)
        
            treebuilder(newnode, depth + 1, maxdepth, wordset, solutions)
    else:
        solutions.append(node)
        print("Solutions found: " + str(len(solutions)))

maxdepth = 5
normalizer = lambda line: line.strip().upper()
worddata = [ normalizer(word) for word in open("swedish-word-list.txt", encoding="ISO-8859-1") ]
wordset = { word for word in sorted(worddata) if len(word) == maxdepth }

solutions = []

try:
    root = treenode([], None)
    treebuilder(root, 0, maxdepth, wordset, solutions)
except KeyboardInterrupt:
    for solution in solutions:
        print(30 * 'v')
        for row in solution.state:
            print(row)
