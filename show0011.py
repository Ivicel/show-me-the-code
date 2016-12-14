#!/usr/bin/env python3
import os


filter_words = set()
with open('filter_words.txt', 'r') as fp:
	while True:
		word = fp.readline().strip()
		if not word:
			break
		if word not in filter_words:
			filter_words.add(word)
print('Input your words')		
while True:
	w = input('>>> ')
	if w in filter_words:
		print('Freedom')
	else:
		print('Human Right')