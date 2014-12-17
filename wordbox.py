#! /usr/bin/python3
import sys

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

def treebuilder(node, depth, maxdepth, wordset, solutions, iterations = 0):
    if depth == 1:
        print("Progress: " + str(iterations / len(wordset)))
        iterations += 1

    if depth < maxdepth:
        words = wordmatcher(node.state, wordset)

        if debug:
            print((depth * 3 * " ") + "Iterating over " + str(len(words)) + " on depth " + str(depth) + " in tree...", file=log)

        for word in words:
            newnode = treenode(node.state, node)
            newnode.addword(word)
            
            node.addchild(newnode)

            if debug:
                print((depth * 3 * " ") + word, file=log)
        
            treebuilder(newnode, depth + 1, maxdepth, wordset, solutions, iterations)
    else:
        solutions.append(node)

        print("Solutions found: " + str(len(solutions)))
            
        if debug:
            print((depth * 3 * " ") + "Solution: " + str(len(solutions)), file=log)
            for row in node.state:
                print((depth * 3 * " ") + row, file=log)

debug = False

try:
    if debug:
        log = open("solution_trace.log", 'w')

    maxdepth = 5
    
    normalizer = lambda line: line.strip().upper()
    worddata = [ normalizer(word) for word in open("swedish-word-list.txt", encoding="ISO-8859-1") ]
    wordset = { word for word in sorted(worddata) if len(word) == maxdepth }

    solutions = []
    root = treenode([], None)

    treebuilder(root, 0, maxdepth, wordset, solutions)
except KeyboardInterrupt:
    out = open("solution_list.txt", 'w')

    for solution in solutions:
        print(30 * 'v')
        for row in solution.state:
            print(row)

        print(30 * 'v', file=out)
        for row in solution.state:
            print(row, file=out)

    out.close()
finally:
    if debug:
        log.close()
