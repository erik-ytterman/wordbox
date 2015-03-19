#! /usr/bin/python3
import sys

from wordboxutils.loaders import loadwords
from wordboxutils.reporting import printnode

#--------------------------------------------------------------
# Data types
#--------------------------------------------------------------

"""
The class treenode is used to contain the present state when 
searching for solutions.

The class has three members:

state:        A list containing the playfield state. Every member 
              is a row in the playfield. The first member (0) is 
              the topmost row, the last (len(state)-1) is the 
              bottom row.

parent:       A reference to the parent node in the tree, with 
              value None if this is the root node.

children:     References to all child nodes.
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
def rowfinder(node, wordset):
   # Filter wordset if there are words in the playfield
   # otherwise, every word is a candidate
   rowwords = wordset

   if not node.state == []:
      # Create "keys" from the columns of the present playfield 
      columnkeys = [ ''.join(t) for t in zip(*node.state) ]

      # Filter out the words, matching the "key" for each column
      columnwords = [ [ word for word in wordset if word.startswith(columnkey) ] for columnkey in columnkeys ]
   
      # Get the index of the next row to be found 
      row = len(node.state)

      # Get the possible characters (charset) for every word position (column),
      # derived from the possible column words (columnwords)
      charsets = [ { word[row] for word in columnwords[column] } for column in range(columns) ]

      # For every column in the playfield, filter away words that does not match
      for column in range(columns):
         rowwords = { word for word in rowwords if word[column] in charsets[column] }
         # Reduce the full wordset, finding words with a charcter in the present
         # word position (column) matching the possible characters (charset) for
         # this columnm, until ony valid words are left
   return rowwords

"""
The treebuilder function build a solution tree, one level 
for each row in the playfield. 
"""
def treebuilder(node, depth, rows, wordset, solutions):
   if len(solutions) < 1:
      if depth == rows:
         node.row = depth
         solutions.append(node)
         print("%d solutions found..." % len(solutions))

      else:
         words = rowfinder(node, wordset)
         
         for word in words:
            newnode = treenode(node.state, node)
            newnode.addword(word)
            node.addchild(newnode)
            
            treebuilder(newnode, depth + 1, rows, wordset, solutions)

"""
The backtracker function is used to restore the path upwards 
in the tree to build a backtrack (list of tree nodes created) 
for a specific solution. 

Observe that this function is recursing to the 'top' node of 
the tree (parent == None) first, and add the elements of the 
track when returning

The function take two parameters:

node:    The solutuion node (leaf) in the tree

track:   The path to the solution, modified for each recursion

The function returns:

A list of solution tree nodest, with the top node of the tree
first and the solution node (leaf) last
"""
def backtracker(node, track = []):
   if not node.parent == None:
      backtracker(node.parent, track)
      
   track.append(node)

   return track

#--------------------------------------------------------------
# Main program
#--------------------------------------------------------------
            
try:
   wordset = loadwords(columns)
   root = treenode([], None)
   treebuilder(root, 0, rows, wordset, solutions)

except KeyboardInterrupt:
   print(30 * 'x')
   print("User interrupt")
   print(30 * 'x')

finally:
   stages = backtracker(solutions[0])
   for i, node in enumerate(stages):
      printnode(i, node)
