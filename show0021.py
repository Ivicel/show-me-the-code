from hashlib import sha256
import hmac, os, time, random, string



def generate_password_hash(password, salt=None):
	if salt is None:
		choices = string.ascii_letters + '0123456789'
		salt = ''
		for i in range(0, 8):
			salt += random.choice(choices)
	if not isinstance(password, bytes):
		password = password.encode('utf-8')
	result = hmac.new(password, salt.encode('utf-8'), sha256).hexdigest()
	return '%s$%s$%s' % ('sha256', salt, result)

def verify_password(password, password_hash):
	method, salt, old_password_hash = password_hash.split('$')
	return generate_password_hash(password, salt) == password_hash



if __name__ == '__main__':
	password_hash = generate_password_hash('asdfghjkl;')
	print(verify_password('asdfghjkl;', password_hash))