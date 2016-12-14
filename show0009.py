#!/usr/bin/env python3

import sys, re
from urllib.request import urlopen

if len(sys.argv) < 2:
	raise SystemExit('Usage: %s url' % sys.argv[1])

response = urlopen(sys.argv[1])
text = response.read().decode('utf-8')
all_links = re.findall(r'<a[\s\S]*?</a>', text)
for link in all_links:
	href = re.search(r'href="([\s\S]*?)"', link)
	href = href.group(1).strip() if href is not None else ''
	link_text = re.sub(r'</?[a-z]+.*?>', '', link).strip()
	print(link_text)
	print(href)
	print('-----------------------------\n')