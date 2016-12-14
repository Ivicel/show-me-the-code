#!/usr/bin/env python3
import sys, re



# 以 # 开头的注释, 不统计跟在语句后的注释
# 以 """ 和 ''' 的多行注释， 不能区别语句里使用"""和'''的多行字符
# 

"""
hello
"""

if len(sys.argv) < 2:
	print('Usage: {script} filename'.format(script=sys.argv[0]))
	raise SystemExit
code_lines, empty_lines, comment_lines = 0, 0, 0
doc_str1 = r"'{3}[\s\S]*?'{3}"
doc_str2 = r'"{3}[\s\S]*?"{3}'
# doc_str1 = r"""(?<=%s)[\s\S]*?(?=%s)""" % ('"""', '"""')
# doc_str2 = r"""(?<=%s)[\s\S]*?(?=%s)""" % ("'''", "'''")
with open(sys.argv[1]) as f:
	lines = f.read()
	# 空行
	empty_lines += len(re.findall(r'^\s*?$', lines, re.M))
	# 以 # 开头的注释
	comment_lines += len(re.findall(r'^\s*#', lines, re.M))	
	lines = re.sub(r'^\s*#.*$', '', lines, flags=re.M)
	# doc string
	for doc_str in [doc_str1, doc_str2]:
		for doc_str_lines in re.findall(doc_str, lines):
			comment_lines += len(doc_str_lines.split('\n'))	
		lines = re.sub(doc_str, '', lines)
	lines = [line.strip() for line in lines.split('\n')]
	for line in lines:
		if line != '':
			code_lines += 1
print('code lines: %d' % code_lines)
print('empty lines: %d' % empty_lines)
print('comment lines: %d' % comment_lines)