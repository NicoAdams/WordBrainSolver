# Adds a new element to a tuple
def tupleAppend(t, e):
	l = len(t)
	return tuple( (t[i] if i<l else e) for i in range(l+1))

class Board:
	def __init__(self, values, trie):
		""" 
		values: A matrix of the letters on the board
		trie: A Trie containing all allowed words
		"""
		self.values = values
		self.trie = trie
		
		# The length of a side of the board 
		self.size = len(values)
	
	def copy(self):
		# Copies the boards values. Does not copy the trie
		newValues = map(lambda x: list(x), self.values)
		return Board(newValues, self.trie)
	
	def __str__(self):
		return "\n".join(map(lambda row: "".join(row), self.values))
		
	def valueAt(self, row, col):
		# coord: A tuple containing (row, col) of current point
		return self.values[row][col]
	
	def setValueAt(self, row, col, value):
		self.values[row][col] = value
		
	def getNeighbors(self, coord):
		# Returns a list of valid neighbors to coord given the board size
		neighbors = [(coord[0]+x, coord[1]+y) \
			for x in range(-1,2) \
			for y in range(-1,2)]
		validCoord = lambda c: \
			all([c[i] >= 0 and c[i] < self.size for i in range(2)]) \
			and not c == coord
		return filter(validCoord, neighbors)
	
	def pathToWord(self, path):
		# Converts a list of tuples representing a path on the board to a word
		return "".join(map(lambda x: self.valueAt(*x), path))
	
	def findPaths(self, wordLen):
		# Returns a list of all valid word paths of length wordLen on the board
		paths = set()
		for x in range(self.size):
			for y in range(self.size):
				coord = (x,y)
				
				# Gets the current word
				value = self.valueAt(*coord)
				currPath = tupleAppend((), coord)
				
				# Gets the current trie
				currTrie = self.trie.getChild(value)
				if currTrie is None:
					# If no word in the trie starts with this letter, skips
					continue
				
				paths = paths.union( \
					self._findPathsAux(wordLen-1, currPath, coord, set(), currTrie) \
				)
		return paths
	
	def _findPathsAux(self, wordLen, currPath, currCoord, seen, currTrie):
		# visited: A set containing all visited coordinates
		
		# Adds the current coord to seen
		seen.add(currCoord)
		
		# Obtains all neighbors that have not yet been visited		
		neighbors = [n for n in self.getNeighbors(currCoord) if n not in seen]
		
		paths = set()
		for newCoord in neighbors:
			value = self.valueAt(*newCoord)
			newPath = tupleAppend(currPath, newCoord)
			
			# Gets the next trie, or skips this coord if no valid words in current trie
			newTrie = currTrie.getChild(value)
			if newTrie is None:
				continue
			
			newWordLen = wordLen-1
			if newWordLen == 0 and newTrie.isWordEnd():
				# Have a valid word!
				paths.add(newPath)
			else:
				# Adds all valid word paths extending from this coordinate
				paths = paths.union( \
					self._findPathsAux(newWordLen, newPath, newCoord, set(seen), newTrie) \
				)
		
		return paths
	
	def removePath(self, path):
		# Returns a copy of the current board with path removed
		
		newBoard = self.copy()
		blankVal = "."
		
		# Determines which letters to move down
		toMoveDown = [[0 for x in range(self.size)] for y in range(self.size)]
		for coord in path:
			row = coord[0]
			col = coord[1]
			
			# Removes the letter
			newBoard.setValueAt(row, col, blankVal)
			
			# Signals letters above to move down
			for rowAbove in range(row):
				toMoveDown[rowAbove][col] += 1
		
		# Moves them down
		for row in range(self.size-1, -1, -1):
			for col in range(self.size):
				currVal = newBoard.valueAt(row, col)
				currMoveDown = toMoveDown[row][col]
				newBoard.setValueAt(row+currMoveDown, col, currVal)
				if currMoveDown > 0:
					newBoard.setValueAt(row, col, blankVal)
		
		return newBoard
		
	def solveBoard(self, wordLengths, numWords, known):
		# Screens the knowns for impossible words
		for k in known:
			newTrie = self.trie.limit(k)
			if newTrie is None:
				print "No words could be obtained from '"+k+"'"
				return []
		
		# Finds solutions
		return self._solveBoardAux(wordLengths[:numWords], known, self.trie, [])
	
	def _solveBoardAux(self, wordLengths, known, baseTrie, solution):
		
		# Deals with known info
		
		currKnown = known[0]
		if len(currKnown) > 0:
			# Calculates the new limited trie
			newTrie = self.trie.limit(currKnown)
			
			# Creates a new board which obeys this trie
			newBoard = self.copy()
			newBoard.trie = newTrie
			
			# Removes the known information
			newKnown = list(known)
			newKnown[0] = ""
			
			# Solves the board with the limited trie
			return newBoard._solveBoardAux(wordLengths, newKnown, baseTrie, solution)
		
		# If no info is known, searches for solutions in the current trie
		currWordLength = wordLengths[0]
		paths = self.findPaths(currWordLength)
		
		solutions = []
		for path in paths:
			
			word = self.pathToWord(path)
			newSolution = list(solution)
			newSolution.append(word)
			
			if len(wordLengths) == 1:
				solutions.append(newSolution)
			else:
				# Creates a new board with the original trie
				newBoard = self.removePath(path)
				newBoard.trie = baseTrie
				
				currSolutions = newBoard._solveBoardAux( \
					wordLengths[1:], known[1:], baseTrie, solution=newSolution \
				)
				solutions.extend(currSolutions)
		
		return solutions
	