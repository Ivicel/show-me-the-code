#!/usr/bin/env python3
from urllib.request import urlopen
import os, re


url = 'http://tieba.baidu.com/p/2166231880'
response = urlopen('http://tieba.baidu.com/p/2166231880')
page_source = response.read().decode('utf-8')
imgs = re.findall(r'<img.*?class="BDE_Image"[\s\S]*?>', page_source)
count = 0
for img in imgs:
	src = re.search(r'src="([\s\S]*?)"', img)
	if src is not None:
		src = src.group(1)
		print('Get picture from: ', src)
		response = urlopen(src)
		postfix = src[src.rindex('.'):]
		fp = open('image' + str(count) + postfix, 'wb')
		fp.write(response.read())
		fp.close()
		count += 1