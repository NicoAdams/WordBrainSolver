# -- BOARD INFO HERE --

wordLengths = [4,7,5,4,5]
known = ["", "", "", "", ""]

board = []
board.append(list("eakeh"))
board.append(list("rtspa"))
board.append(list("ochet"))
board.append(list("shtec"))
board.append(list("tomdh"))

# -- SOLUTION CODE --

from en_dict import *
from wb_board import *

print "Loading dictionary..."
enDict = loadDefaultDict()

print "Solving..."
b = Board(board, enDict)
solutions = b.solveBoard(wordLengths, 1, known)

# Filters duplicate solutions
solutions = set(map(tuple, solutions))

for s in solutions: print s
print "Found", len(solutions), "solutions"

# b = Board(board, getDictFromFile("testdict"))
# path = ()
# path = tupleAppend(path, (0,0))
# path = tupleAppend(path, (1,1))
# path = tupleAppend(path, (2,0))
# print str(b)
# print
# print str(b.removePath(path))