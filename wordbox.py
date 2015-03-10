#! /usr/bin/python3
import sys

#--------------------------------------------------------------
# Data types
#--------------------------------------------------------------

"""
The class treenode is used to contain the present state when 
searching for solutions.

The class has three members:

state:     A list containing the playfield state. Every member 
           is a row in the playfield. The first member (0) is 
           the topmost row, the last (len(state)-1) is the 
           bottom row.

parent:    A reference to the parent node in the tree, with 
           value None if this is the root node.

children:  References to all child nodes.
"""
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
# Configuration and global data
#--------------------------------------------------------------

"""
Configure number of rows and columns in the playfield. At 
present only square (rows = columns) playfields are supported.
"""
rows = columns = 5

"""
Define a list that will contain references to the valid 
solutions found in the solution tree leafs.
"""
solutions = []

#--------------------------------------------------------------
# Algorithm
#--------------------------------------------------------------

"""
The rowfinder function is used to filter out all valid words 
for the next row (empty) row in the playfield. For an empty 
playfield (state) no processing will take place, as all words 
are potentially valid, thus returning the same set of words
passed as input.

The function take two parameters:

state:   The present playfield state, see details in the 
         treenode class description

wordset: A complete set of possible words

The function returns:

A set of words that are valid for the next (empty) row in 
the playfield, given the present playfield state
"""
def rowfinder(state, wordset):
   # Filter wordset if there are words in the playfield
   # otherwise, every word is a candidate
   if not state == []:
      # Create "keys" from the columns of the present playfield 
      columnkeys = [ ''.join(t) for t in zip(*state) ]

      # Filter out the words, matching the "key" for each column
      columnwords = [ [ word for word in wordset if word.startswith(columnkey) ] for columnkey in columnkeys ]
   
      # Get the index of the next row to be found 
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

"""
The treebuilder function build a solution tree, one level 
for each row in the playfield. 
"""
def treebuilder(node, depth, rows, wordset, solutions):
   if depth == rows:
      solutions.append(node)
      print("%d solutons found..." % len(solutions))

   else:
      words = rowfinder(node.state, wordset)
      
      for word in words:
         newnode = treenode(node.state, node)
         newnode.addword(word)
         node.addchild(newnode)
            
         treebuilder(newnode, depth + 1, rows, wordset, solutions)

#--------------------------------------------------------------
# Main program
#--------------------------------------------------------------
            
try:
   normalizer = lambda line: line.strip().upper()
   worddata = [ normalizer(word) for word in open("swedish-word-list.txt", encoding="ISO-8859-1") ]
   wordset = { word for word in sorted(worddata) if len(word) == columns }
   
   root = treenode([], None)
   treebuilder(root, 0, rows, wordset, solutions)

except KeyboardInterrupt:
   print(30 * 'x')
   print("User interrupt")
   print(30 * 'x')

finally:
   for solution in solutions:
      print(30 * 'v')
      for row in solution.state:
         print(row)
