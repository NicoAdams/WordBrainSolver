# -- BOARD INFO HERE --

wordLengths = [2,6,4,7,6]
known = ["no", "pigsty", "", "", "poison"]

board = []
board.append(list("ensty"))
board.append(list("aiois"))
board.append(list("nncrg"))
board.append(list("okaio"))
board.append(list("pponp"))

solveFor = 5

# -- SOLUTION CODE --

from en_dict import *
from wb_board import *

print "Loading dictionary..."
enDict = loadDefaultDict()

print "Solving..."
b = Board(board, enDict)
solutions = b.solveBoard(wordLengths, solveFor, known)

# Filters duplicate solutions
solutions = set(map(tuple, solutions))

print 
print "Found", len(solutions), "unique solutions:"
for s in solutions: print ", ".join(list(s))
