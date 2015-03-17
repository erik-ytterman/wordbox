#! /usr/bin/python3
import sys

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

row:          An integer with the index for the next word in the
              playfield list that we are trying to find

columnkeys:   A list containing the key used to filter out possible
              words for a specific column

columnwords:  A list containing the possible words for a specific
              column

parent:       A reference to the parent node in the tree, with 
              value None if this is the root node.

children:     References to all child nodes.
"""
class treenode:
   state = None

   columnkeys = None
   columnwords = None
   charsets = None
   row = 0
   rowwords = None

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
      node.columnkeys = [ ''.join(t) for t in zip(*node.state) ]

      # Filter out the words, matching the "key" for each column
      node.columnwords = [ [ word for word in wordset if word.startswith(columnkey) ] for columnkey in node.columnkeys ]
   
      # Get the index of the next row to be found 
      node.row = len(node.state)

      # Get the possible characters (charset) for every word position (column),
      # derived from the possible column words (columnwords)
      node.charsets = [ { word[node.row] for word in node.columnwords[column] } for column in range(columns) ]

      # For every column in the playfield, filter away words that does not match
      for column in range(columns):
         rowwords = { word for word in rowwords if word[column] in node.charsets[column] }
         # Reduce the full wordset, finding words with a charcter in the present
         # word position (column) matching the possible characters (charset) for
         # this columnm, until ony valid words are left

      # Store possible rows in solution treez
      node.rowwords = rowwords

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

def backtracker(node, track = []):
   if not node.parent == None:
      backtracker(node.parent, track)
      
   track.append(node)

   return track

#--------------------------------------------------------------
# Helpers
#--------------------------------------------------------------

def loadwords(filename = "swedish-word-list.txt"):
   normalizer = lambda line: line.strip().upper()
   worddata = [ normalizer(word) for word in open(filename, encoding="ISO-8859-1") ]
   wordset = { word for word in sorted(worddata) if len(word) == columns }
   
   return wordset

def printnode(node):
   # Print state
   print(30 * str(node.row))
   for row in node.state:
      print(row)
      
   # Print column keys and words
   if not node.columnkeys == None:
      print(30 * "-")
      for i, columnkey in enumerate(node.columnkeys):
         if len(node.columnwords[i]) <= 7:
            print("Key for column: %d is %s -> %s" % (i, columnkey, node.columnwords[i]))
         else:
            print("Key for column: %d is %s -> %s" % (i, columnkey, "MANY"))
            
   if not node.charsets == None:
      print(30 * "+")
      for i, charset in enumerate(node.charsets):
         print("Charset for column: %d is %s" % (i, charset))
      if len(node.rowwords) <= 7:
         print("Possible words: %s" % (node.rowwords))
      else:
         print("Possible words: %s" % ("MANY"))

   print(30 * str(node.row))

#--------------------------------------------------------------
# Main program
#--------------------------------------------------------------
            
try:
   wordset = loadwords()
   root = treenode([], None)
   treebuilder(root, 0, rows, wordset, solutions)

except KeyboardInterrupt:
   print(30 * 'x')
   print("User interrupt")
   print(30 * 'x')

finally:
   stages = backtracker(solutions[0])
   for stage in stages:
      printnode(stage)
