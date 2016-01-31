# -- BOARD INFO HERE --

wordLength = 3
hint = ""

board = []
board.append(["w","e","t","e","."])
board.append(["i","g","n","e","."])
board.append(["g","a","r","c","."])
board.append(["b","n","c","e","n"])
board.append(["b","a","p","c","a"])

# -- SOLUTION CODE --

from en_dict import *
from wb_board import *

print "Loading dictionary..."
enDict = loadDefaultDict()

print "Solving..."
b = Board(board, enDict)
words = b.findWords(wordLength)
words = filter(lambda x: x[0:len(hint)]==hint, words)

print "Found", len(words), "words"
for w in words:
	print w