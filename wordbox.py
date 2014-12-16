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

def printsolution(node, recurse = False):
    if not node == None:
        for row in node.state:
            print(row)
        
        if recurse:
            print(30 * '-')
            printpath(node.parent)

def treebuilder(node, depth, maxdepth, wordset):
    if depth < maxdepth:
        for word in wordmatcher(node.state, wordset):
            newnode = treenode(node.state, node)
            
            newnode.state.append(word)
            
            node.children.append(newnode)
        
            treebuilder(newnode, depth + 1, maxdepth, wordset)
    else:
        print(30 * 'v')
        printsolution(node)
        print(30 * '^')

maxdepth = 5
normalizer = lambda line: line.strip().upper()
worddata = [ normalizer(word) for word in open("swedish-word-list.txt", encoding="ISO-8859-1") ]
wordset = { word for word in sorted(worddata) if len(word) == maxdepth }

root = treenode([], None)
treebuilder(root, 0, maxdepth, wordset)


