class Trie:
	
	def __init__(self, value=""):
		self.value = value
		self.children = {}
		self.end = False
	
	def getRest(self, word):
		return word[len(self.value):]
	
	def addWord(self, word):
		rest = self.getRest(word)
		
		if rest == "":
			self.end = True
			return
		
		nextVal = rest[0]
		if nextVal not in self.children:
			self.children[nextVal] = Trie(nextVal)
		child = self.children[nextVal]
		
		child.addWord(rest)
		
	def contains(self, word):
		rest = self.getRest(word)
		
		if rest == "":
			return self.end
		
		if rest[0] not in self.children:
			return False
		
		return self.children[rest[0]].contains(rest)
	
	def getChild(self, value):
		# Returns the child Trie with value "value", else returns False
		if value not in self.children:
			return None
		return self.children[value]
		
	def isWordEnd(self):
		# Returns true if this trie marks the end of a word
		return self.end
	
	def limit(self, prefix):
		# Returns a new trie whose words are limited to those that start
		# with the letters in prefix
		if len(prefix) == 0:
			return self
		
		child = self.getChild(prefix[0])
		if child is None:
			return None
		
		newChild = child.limit(prefix[1:])
		if newChild is None:
			return None
		
		newTrie = Trie(self.value)
		newTrie.children = {newChild.value: newChild}
		newTrie.end = self.end
		return newTrie 
	
	
	
	def __str__(self):
		return self._toStrAux(0)
	
	def _toStrAux(self, indent):
		result = ("| " * (indent-1))
		if indent > 0:
			result += "|-"
		
		result += self.value
		
		if self.end:
			result += "!"
		
		result += "\n"
		
		for value in self.children:
			newIndent = indent + 1
			result += self.children[value]._toStrAux(newIndent)
		return result

def getDictFromFile(path):
	trie = Trie()
	lines = open(path).readlines()
	for word in lines:
		word = word.strip()
		trie.addWord(word.strip())
	return trie

def loadDefaultDict():
	return getDictFromFile("en_dict.txt")
