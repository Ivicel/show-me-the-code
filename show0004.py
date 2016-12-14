import re, sys



def split_word(file):
	english_split = re.compile(r'(?:[A-Z.]+[A-Z])|[a-zA-Z]+(?:[\'’][a-zA-Z]*|(?:-[a-zA-Z]+)*)|\$?(?:\d+,?(?=\d{3}))+\d+(?:\.\d+)?%?|\.{3}')
	with open(file) as f:
		line = f.readline()
		while line:
			words = english_split.findall(line)
			line = f.readline()
			yield words


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Usage: %s filename' % sys.argv[0])
	length = 0
	for word in split_word(sys.argv[1]):
		print(word)
		length += len(word)
	print('amount: %d' % length)