#!/usr/bin/env python3

# request pingwest article from article web page
from urllib.request import urlopen
import re, sys
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
	def __init__(self):
		# HTMLParser.__init__(self)
		super().__init__()
		self.div_counts = 0
		self.article = []
		self.paragraph = ''

	def handle_starttag(self, tag, attrs):
		if tag == 'div':
			self.div_counts += 1
		if tag == 'p':
			for attr in attrs:
				if attr == ('class', 'post-footer-wx'):
					self.reset()

	def handle_endtag(self, tag):
		if tag == 'div':
			self.div_counts -= 1
		if self.div_counts == 0:
			self.article.append(self.paragraph)
			self.reset()
		if tag == 'p':
			self.article.append(self.paragraph)
			self.paragraph = ''

	def handle_data(self, data):
		self.paragraph += data

	def handle_startendtag(self, tag, attrs):
		for attr in attrs:
			if attr[0] == 'src' or attr[0] == 'href':
				self.paragraph += '<' + attr[1] + '>'

if len(sys.argv) < 2:
	raise SystemExit('Usage: {script} url'.format(script=sys.argv[0]))
response = urlopen(sys.argv[1])
page = response.read().decode('utf-8')
title = re.findall(r'<div\s+class=["\']post-head["\'][\s\S]*?</div>', page)
paragraphs = re.findall(r'<div[\s.]*?id=["\']sc-container["\'][\s\S]*</div>', page)
# print(paragraphs[0])
if len(title) == 0:
	raise SystemExit("找不到文章标题")
if len(paragraphs) == 0:
	raise SystemExit("找不到文章内容")
string = re.search(r'<h1[\s\S]*?>([\s\S]*?)</h1>', title[0])
title = string.group(1).strip() if string is not None else ''
print(title, '\n')
paragraphs = paragraphs[0].replace('\n', '')
parser = MyHTMLParser()
try:
	parser.feed(paragraphs)
except:
	for p in parser.article:
		print(p)