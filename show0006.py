#!/usr/bin/env python3
from show0004 import split_word
from stemming.porter2 import stem
import os, sys



if __name__ == '__main__':
	if len(sys.argv) < 2 and os.path.isfile(sys.argv[1]):
		print('Usage: ' + sys.argv[0] + 'filename')
		raise SystemExit
	all_words = set()
	all_words_count = {}
	for words in split_word(sys.argv[1]):
		for word in words:
			if word.lower() not in all_words:
				all_words.add(word)
				all_words_count[word.lower()] = 1
			else:
				all_words_count[word.lower()] += 10
	base = list(all_words_count.keys())[0]
	for key in all_words_count.keys():
		if all_words_count[key] > all_words_count[base]:
			base = key
	print('{word}: {count}'.format(word=base, count=all_words_count[base]))  
