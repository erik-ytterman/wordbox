#! /usr/bin/python3
import sys
import random

# Contain playfield state
class state:
    data = None
    
    def __init__(self, rows, columns):
        self.data = [ [ '*' for i in range(columns) ] for j in range(rows) ]

    def setrow(self, word, index):
        if len(word) <= len(self.data):
            for i, char in enumerate(list(word)): 
                self.data[index][i] = char
        else:
            raise Exception

    def getrow(self, index):
        return ''.join([char for char in self.data[index]])
        
    def setcol(self, word, index):
        if len(word) <= len(self.data):
            for i, char in enumerate(word):
                self.data[i][index] = char
        else:
            raise Exception

    def getcol(self, index):
        cols = list(zip(*self.data))
        return ''.join(cols[index])

    def dumptext(self, index = None):
        if index == None:
            for row in self.data:
                print(''.join(row))
        else:
            print(self.data[index])

# Validate playfield state
class validator:
    wordlist = None

# Find possible new playfield states
class finder:
    wordlist = None

# Store playfield state graph
class tree:
    state = None
    children = []


#################################################################################################

count = 5

normalizer = lambda line: line.strip().upper()

worddata = [ normalizer(word) for word in open("swedish-word-list.txt", encoding="ISO-8859-1") ]

wordlist = tuple( { word for word in sorted(worddata) if len(word) == count } )

s = state(14, 17)

print(50 * "E")

# Row manipulation

s.setrow("APANS", 3);

print(40 * "R")

print(s.getrow(3))
print(s.getrow(4))

print(40 * "R")

s.dumptext()

# Column manipulation

s.setcol("APANS", 3);

print(40 * "C")

print(s.getcol(3))
print(s.getcol(4))

print(40 * "C")

s.dumptext()

print(50 * "E")
