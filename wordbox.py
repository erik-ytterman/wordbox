#! /usr/bin/python3
import sys
import random
import copy
import re

from functools import reduce

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

    def dumptext(self, index = None, indent = 0):
        if index == None:
            for row in self.data:
                print(indent * " " + ''.join(row))
        else:
            print(self.data[index])

##########################################################################################

count = 5

normalizer = lambda line: line.strip().upper()

worddata = [ normalizer(word) for word in open("swedish-word-list.txt", encoding="ISO-8859-1") ]

wordlist = tuple( { word for word in sorted(worddata) if len(word) == count } )

state = []
choice = []

for row in range(3):
    print(10 * 'R' + 40 * str(row))

    sample = random.choice(wordlist)
    choice.append(list(sample))

    for c in choice:
        print(c)

    print(10 * 'S' + 40 * str(row))

    L = [ (i, ''.join(column), tuple([ w for w in wordlist if w.startswith(''.join(column)) ]) ) for i, column in enumerate(zip(*choice)) ]
    
    for i,l in enumerate(L): 
        print(10 * "C" + 40 * str(i))
        print(len(l[2]), l)

    print(10 * 'R' + 40 * str(row))

'''
class treenode:
    state = None
    children = []

    def __init__(self, state):
        self.state = state

def buildtree(level, node):
    for j, word in enumerate(wordlist):
        if(level < count):
            state = playstate(count, count)
            state.data = copy.deepcopy(node.state.data)
            state.size = copy.copy(node.state.size)

            state.setrow(word, level)
            
            results = [ [ w for w in wordlist if re.match(key, w) ] for key in state.getkeys() ]
        
            if not [] in results:
                print("Level: " + str(level))
                state.dumptext()
                newnode = treenode(state)
                node.children.append(newnode)
                buildtree(level+1, newnode)
        else:
            print("SOLUTION!")
            node.state.dumptext()

        if( j % 100 == 0 ):
            sys.stdout.write('+')
            sys.stdout.flush()

state = playstate(count, count)
root = treenode(state)

buildtree(0, root)
'''
