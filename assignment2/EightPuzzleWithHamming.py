'''EightPuzzleWithHamming.py

by Russell Kook
UWNetID: Russkook
Student number: 1620672

Assignment 2, in CSE 415, Winter 2020.

This file augments EightPUzzle.py with heuristic information,
so that it can be used by an A* implementation.
count the number of tiles out of place, but not the blank,
in order to maintain admissibility

'''

from EightPuzzle import *

order = [[0,1,2],[3,4,5],[6,7,8]]

def h(s):
  count = 0
  for i in range(3):
      for j in range(3):
        if (s.b[i][j] != order[i][j]):
          count = count + 1

  return count

# A simple test:
#print(h('Nantes'))
