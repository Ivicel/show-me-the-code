#!/usr/bin/env python3
import os, re

filter_words = []
with open('filter_words.txt', 'r') as fp:
	while True:
		word = fp.readline().strip()
		if not word:
			break
		filter_words.append(word)

while True:
	try:
		word = input('>>>')
		for w in filter_words:
			word = re.sub(w, len(w) * '*', word)
		print(word)
	except KeyboardInterrupt:
		raise SystemExit
