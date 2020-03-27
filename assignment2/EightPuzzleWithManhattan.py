'''EightPuzzleWithManhattan.py
Farmer_Fox.py
by Russell Kook
UWNetID: Russkook
Student number: 1620672

Assignment 2, in CSE 415, Winter 2020.
 
This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
Total of Manhattan distances for the 8 tiles

'''

from EightPuzzle import *

order = [[0,1,2],[3,4,5],[6,7,8]]

def h(s):
  count = 0
  for i in range(3):
      for j in range(3):
        value = s.b[i][j]
        if(value != 0):
          expectedJ = value % 3
          expectedI = value // 3
          dj = j - expectedJ
          di = i - expectedI
          count = count + abs(dj) + abs(di)
  return count

# A simple test:
#print(h('Nantes'))
