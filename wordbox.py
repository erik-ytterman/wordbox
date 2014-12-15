#! /usr/bin/python3
import sys
import random
import itertools
import copy
import re

class treenode:
    state = None
    children = []
    
    def __init__(self, state):
        self.state = state

def treebuilder(node, maxdepth):
    if(len(node.state) == maxdepth):
        print("SOLUTION")
        for row in node.state:
            print(row)
        print("SOLUTION")
    
    for word in wordlist:
        matches = []
        for i, j in itertools.zip_longest(list(zip(*node.state)), list(zip(word)), fillvalue = ''):
            column = '%s%s' % (''.join(i),''.join(j)) 
            words = len([ w for w in wordlist if w.startswith(column) ])
            matches.append(words)
                  
        if not 0 in matches:
            print(20 * 'v')

            newstate = copy.deepcopy(node.state)
            newstate.append(word)
         
            newnode = treenode(newstate)

            print("PARTIAL")
            for row in newnode.state:
                print(row)
            print("PARTIAL")

            node.children.append(newnode)
            treebuilder(newnode, maxdepth)
    
    print(20 * '^')

maxdepth = 5
normalizer = lambda line: line.strip().upper()
worddata = [ normalizer(word) for word in open("swedish-word-list.txt", encoding="ISO-8859-1") ]
wordlist = tuple( { word for word in sorted(worddata) if len(word) == maxdepth } )
root = treenode([])

treebuilder(root, maxdepth)

