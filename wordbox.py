#! /usr/bin/python3
import sys

#--------------------------------------------------------------
# Configuration
#--------------------------------------------------------------

maxdepth = columns = rows = 5

#--------------------------------------------------------------
# Data structures
#--------------------------------------------------------------

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

#--------------------------------------------------------------
# Algorithm
#--------------------------------------------------------------

def rowfinder(state, wordset):
    # Create keys from the columns of the present playfield 
    columnkeys = [ ''.join(t) for t in zip(*state) ]

    # Filter out the words, matching the key for each column
    columnwords = [ [ word for word in wordset if word.startswith(columnkey) ] for columnkey in columnkeys ]

    # Get the index of the row to be found (the playfield is a list of rows)
    row = len(state)

    # For every column in the playfield
    for column in range(columns):
        # Get the possible characters (charset) for every word position (column),
        # derived from the possible column words (columnwords)
        charset = { word[row] for word in columnwords[column] }

        # Reduce the full wordset, finding words with a charcter in the present
        # word position (column) matching the possible characters (charset) for
        # this columnm, until ony valid words are left
        wordset = { word for word in wordset if word[column] in charset }

    return wordset
        
def wordmatcher(state, wordset):
    if state == []:
        return wordset
    else:
        return rowfinder(state, wordset)

def treebuilder(node, depth, maxdepth, wordset, solutions):
    if depth < maxdepth:
        words = wordmatcher(node.state, wordset)

        for word in words:
            newnode = treenode(node.state, node)
            newnode.addword(word)
            
            node.addchild(newnode)
        
            treebuilder(newnode, depth + 1, maxdepth, wordset, solutions)
    else:
        solutions.append(node)

        print("%d solutons found..." % len(solutions))

#--------------------------------------------------------------
# Main program
#--------------------------------------------------------------
            
try:
    normalizer = lambda line: line.strip().upper()

    worddata = [ normalizer(word) for word in open("swedish-word-list.txt", encoding="ISO-8859-1") ]

    wordset = { word for word in sorted(worddata) if len(word) == columns }

    solutions = []

    root = treenode([], None)

    treebuilder(root, 0, maxdepth, wordset, solutions)

except KeyboardInterrupt:
    for solution in solutions:
        print(30 * 'v')
        for row in solution.state:
            print(row)
