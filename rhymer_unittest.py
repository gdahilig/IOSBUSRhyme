

import unittest
from rhymer import Rhymer 

class TestRhymer(unittest.TestCase):
	def setUp(self):
		#initalize the data with test values.
		Rhymer.dictRhymes = {'shoe': ['glue', 'mu', 'rue', 'hue'], 'phone': ['bone', 'loan']}
		self.rhymer = Rhymer()
		self.number = '+18188881234'
	
	def test_init(self):
		s = self.rhymer.help()
		self.assertEqual(s,'commands: rhyme, learn, n, r, help', 'invalid response')

# Test Get
	def test_Get_Found(self):
		s = self.rhymer.get('+18188881234','shoe')
		self.assertEqual(s, 'glue rhymes with shoe')

		s = self.rhymer.get('+18188881234','phone')
		self.assertEqual(s, 'bone rhymes with phone')

	# test failed search
	def test_Get_NotFound(self):
		s = self.rhymer.get('+18188881234','pizza')
		self.assertEqual(s, 'I have no rhymes for pizza')

# Test Learn
	def test_Learn_word(self):
		s = self.rhymer.learn(self.number,'gum', 'bum')
		self.assertEqual(s, 'Learning gum rhymes with bum')
		self.assertEqual(self.findWord('gum','bum'), True, 'word not in dictionary')

	def test_Learn_word_already_learned(self):
		s = self.rhymer.learn(self.number,'phone', 'loan')
		self.assertEqual(s, 'loan already rhymes with phone')

# Test Next
	def test_NextWord(self):
		s = self.rhymer.get('+18188881234','shoe')
		self.assertEqual(s, 'glue rhymes with shoe')
		s = self.rhymer.next('+18188881234')
		self.assertEqual(s, 'mu rhymes with shoe')
		s = self.rhymer.next('+18188881234')
		self.assertEqual(s, 'rue rhymes with shoe')
		s = self.rhymer.next('+18188881234')
		self.assertEqual(s, 'hue rhymes with shoe')
		s = self.rhymer.next('+18188881234')
		self.assertEqual(s, 'No more words')

	# test next 
	def test_NextWord2(self):
		s = self.rhymer.get('+18188881234','shoe')
		self.assertEqual(s, 'glue rhymes with shoe')
		s = self.rhymer.get('+18188881234','phone')
		self.assertEqual(s, 'bone rhymes with phone')
		s = self.rhymer.next('+18188881234')
		self.assertEqual(s, 'loan rhymes with phone')
		s = self.rhymer.next('+18188881234')

	# tests when next is called without a previous get.
	def test_Next_Outside_of_Get(self):
		s = self.rhymer.next('+18188881234')
		self.assertEqual(s, 'No current word (you need to find rhyme first)')

# Test Remove
	# Test simple remove
	def test_Remove(self):
		s = self.rhymer.get('+18188881234','phone')
		self.assertEqual(s, 'bone rhymes with phone')
		s = self.rhymer.remove('+18188881234')
		self.assertEqual(s, 'bone has been removed.')
		self.assertEqual(self.findWord('shoe', 'bone'), False)


	# test remove followed by next
	def test_Remove_2(self):
		s = self.rhymer.get('+18188881234','phone')
		self.assertEqual(s, 'bone rhymes with phone')
		s = self.rhymer.remove('+18188881234')
		self.assertEqual(s, 'bone has been removed.')
		self.assertEqual(self.findWord('shoe', 'bone'), False)

		s = self.rhymer.next('+18188881234')
		self.assertEqual(s, 'loan rhymes with phone')

	# test remove all items in the rhyme list.
	# 'phone': ['bone', 'loan']
	# note: key is removed when list is empty.
	def test_Remove_2(self):
		s = self.rhymer.get('+18188881234','phone')
		self.assertEqual(s, 'bone rhymes with phone')
		s = self.rhymer.remove('+18188881234')
		self.assertEqual(s, 'bone has been removed.')
		self.assertEqual(self.findWord('shoe', 'bone'), False)

		s = self.rhymer.next('+18188881234')
		self.assertEqual(s, 'loan rhymes with phone')

		s = self.rhymer.remove('+18188881234')
		self.assertEqual(s, 'no more rhymes for phone')

		#make sure list is no longer in dictionary.
		self.assertEqual(self.findWordList('phone'), False)


# Helper functions
	# helper function to check if word is in the dictionary of lists
	def findWordList(self, word):
		inDictionary = Rhymer.dictRhymes.has_key(word)
		# check if the key exists
		return inDictionary

	def findWord(self, word, newWord):
		inDictionary = Rhymer.dictRhymes.has_key(word)
		# check if the key exists
		if inDictionary == False:
			return False;
		
		rhymingList = Rhymer.dictRhymes[word]
		return newWord in rhymingList

if __name__ == '__main__':
    unittest.main()