
class UserState:
	def __init__(self):
	    self.number = ''
	    self.word = ''
	    self.index = 0


class Rhymer:
	#dictionary of word lists.
	#keys are words and the value is a list of words that it rhymes with.
	dictRhymes = {'happy': ['pappy', 'sappy'], 'mad': ['sad', 'bad']}

	dictUsers = {}

	# get: retrieves a rhyme for a given word
	# returns string result
	def get(self, number, word):
		inDict = self.dictRhymes.has_key(word)
		if inDict:
			rhymingList = self.dictRhymes[word]
			idx = 0
			rhymingWord = rhymingList[idx]

			#now set user state.
			self.setUser(number,word,0)

			return rhymingWord + ' rhymes with ' + word
		else:
			return 'I have no rhymes for ' + word

	# learn: adds the given newWord into the list of the dictionary item for word
	# parameters
	#	word: 		base word
	#	newWord: 	word that rhymes with base word.
	def learn(self, number, word, newWord):
#		print 'learn'
#		print 'word:' + word
#		print 'new rhyme:' + newWord

		self.clearUser(number)
		inDict = self.dictRhymes.has_key(word)
#		print 'word = ' + word
#		print 'newWord = ' + newWord
#		print self.dictRhymes

		if inDict:
#			print 'In Dictionary'
			rhymingList = self.dictRhymes[word]
			if newWord in rhymingList:
				return newWord + ' already rhymes with ' + word
			else:		
#				print 'Adding to word list: ' + word
				rhymingList.append(newWord)
#				print self.dictRhymes
			return 'New rhyme added!'
		else:
			#create a new list.
#			print 'not in dictionary'
			rhymingList = []
			rhymingList.append(newWord)
			self.dictRhymes[word]=rhymingList
#			print self.dictRhymes
			return 'Learning ' + word + ' rhymes with ' + newWord

	# next: returns the next word in a rhyming sequence
	#		increments the users index in userState.
	# 		when it goes pass the end of the list, it removes the users state info
	#		to breaks the circle.  user will need to retrieve a new rhyme in order
	#		to list rhyming words.
	def next(self,number):
#		print 'next'
#		print self.dictUsers
		if self.haveUserState(number):
#			print '1'
			userState = self.dictUsers[number]
#			print userState.number 
#			print userState.word
#			print userState.index
			rhymingList = self.dictRhymes[userState.word]
#			print rhymingList
			idx = userState.index+1
#			print idx
#			print  len(rhymingList)
			if idx >= len(rhymingList):
				self.clearUser(number)
				return 'No more words'
			else:
				userState.index = idx
				return  rhymingList[idx] + ' rhymes with ' + userState.word
		else:
			return 'No current word (you need to find rhyme first)'

	# remove: removes the current word from it's word list.
	#		  resultant empty lists are removed from the dictionary.
	# parameters:
	#		number - phone number of the current user. used for state info.
	# returns
	#		message result
	def remove(self, number):
#		print 'removing a word'
#		print self.dictUsers
		if self.haveUserState(number):
#			print '1'
			userState = self.dictUsers[number]
			keyWord = userState.word
#			print userState.number 
#			print userState.word
#			print userState.index
			rhymingList = self.dictRhymes[userState.word]
#			print rhymingList

			idx = userState.index
#			print idx
			word = rhymingList[idx]	
			del rhymingList[idx]		
#			print rhymingList	
			if len(rhymingList) <= 0:
				#remove key from dictionary
				self.dictRhymes.pop(userState.word)
				self.clearUser(number)
				self.updateUserIndexes(keyWord,idx)
				return 'no more rhymes for ' + keyWord
			else:
				self.updateUserIndexes(keyWord,idx)
				return word + ' has been removed.'
		else:
			return 'No current word (you need to find rhyme first)'		

	# help: returns a short message with the available commands
	def help(self):
		return 'commands: rhyme, learn, n, r, help'

	# setUser:
	# parameters:
	#	number: phone number of the user
	#	word: 	current word in the sequence
	#	idx:	index of the word list that the user is on.
	def setUser(self, number,word, idx):
		# sets the users state
		if self.dictUsers.has_key(number):
			# found
			userState = self.dictUsers[number]
			userState.word = word
			userState.index = idx
			return
		else:
			userState = UserState()
			userState.number = number
			userState.word = word
			userState.index = 0
			self.dictUsers[number] = userState
			return

	# haveUserState: helper function to check if the user is currently viewing rhymes.
	# parameters:
	#	number - phone number of the user
	# returns:
	#	true, if user is in the state dictionary (currently viewing rhymes)
	#	false, if user has no state in dictionary (not currently viewing rhymes)
	def haveUserState(self, number):
#		print 'haveUserState'
		return self.dictUsers.has_key(number)

	# clearUser: removes the user from the userState dictionary
	def clearUser(self, number):
#		print 'clearUser'
		if self.dictUsers.has_key(number):
#			print 'user removed'
			self.dictUsers.pop(number)
#		else:
#			print 'user not found'
		return

	# updateUserIndexes: updates the user state info if words in the list that a users is
	#	currently viewing has been deleted.  (i.e. if userState.index > idx)
	def updateUserIndexes(self, word, idx):
#		print 'updating userState indexes'
		for key in self.dictUsers:
#			print 'key: ' + key
			user = self.dictUsers[key]
#			print user.number
#			print user.word
#			print user.index

			if user.word is word:
				if user.index >= idx:
#					print "updating index"
					user.index = user.index-1
		return