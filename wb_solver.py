# -- BOARD INFO HERE --

wordLength = 4
hint = ""

board = []
board.append(["s","h"])
board.append(["i","t"])

# -- SOLUTION CODE --

from en_dict import *
from wb_board import *

print "Loading dictionary..."
enDict = loadDefaultDict()

print "Solving..."
b = Board(board, enDict)
paths = b.findPaths(wordLength)
# words = filter(lambda x: x[0:len(hint)]==hint, words)
words = map(b.pathToWord, paths)

print "Found", len(words), "words"
for w in words:
	print w