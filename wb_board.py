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
	
	def valueAt(self, coord):
		# coord: A tuple containing (row, col) of current point
		return self.values[coord[0]][coord[1]]
		
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
		return "".join(map(self.valueAt, path))
	
	def findPaths(self, wordLen):
		# Returns a list of all valid word paths of length wordLen on the board
		paths = set()
		for x in range(self.size):
			for y in range(self.size):
				coord = (x,y)
				
				# Gets the current word
				value = self.valueAt(coord)
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
			value = self.valueAt(newCoord)
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
		# Returns all the possible boards
		pass
