from random import seed, choice
from datetime import datetime

def make_active_codes(code_length=13):
	active_code = set()
	count = 0
	upper_letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
		'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	seed(datetime.now())
	while True:
		if count == 200:
			break
		each_code = ''
		for i in range(0, code_length):
			each_code += choice(upper_letter)
		if each_code not in active_code:
			active_code.add(each_code)
			count = count + 1
	return active_code

if __name__ == '__main__':
	count = 1
	for code in make_active_codes():
		print('%d: %s' % (count, code))
		count += 1