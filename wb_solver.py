# -- BOARD INFO HERE --

wordLengths = [5,6,4,3,4,3]

known = ["" for i in range(len(wordLengths))]
known[0] = "igloo"
# known[1] = "paddle"

board = []
board.append(list("lorfe"))
board.append(list("oddal"))
board.append(list("ooged"))
board.append(list("lgmdp"))
board.append(list("gikoa"))

# Number of words to solve for
solveFor = 6

# True if should print solutions when they are first found
printAsFound = True

# -- SOLUTION CODE --

from en_dict import *
from wb_board import *

print "Loading dictionary..."
enDict = loadDefaultDict()

print "Solving..."
b = Board(board, enDict, verbose=printAsFound)
solutions = b.solveBoard(wordLengths, solveFor, known)

# Filters duplicate solutions
solutions = set(map(tuple, solutions))

print "Found", len(solutions), "unique solutions"
if not printAsFound:
	for s in solutions: print ", ".join(map(str, list(s)))
