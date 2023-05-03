# -*- coding: utf-8 -*-

class CamelCase(object):
	'''
	This Class turns stings into CamelCase except for a list of 'stop words'
	'''

	def __init__(self, *args):
		'''
		On inisialisation you can pass in keywords that you want to ignore.
		'''
		
		self.stop_words = ['a', 'is', 'and']

		for i in args:
			self.stop_words.append(i)

		

	def hump(self, s):
		'''
		Hump is a method that takes an inputted string and turns it into camel case format.
		'''

		results = []

		for word in s.split(' '):
			if word not in self.stop_words:
				word_converted_to_camel_case = word[0].upper() + word[1:]
				results.append(word_converted_to_camel_case)

			else:
				results.append(word)

		return ' '.join(results)


