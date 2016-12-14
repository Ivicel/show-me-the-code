import MySQLdb
import sys
from show0001 import make_active_codes


activation_codes = make_active_codes()
try:
	db = MySQLdb.connect(user='testuser', passwd='test@User123', db='test_db');
	c = db.cursor()
except:
	print("Can not find the database.")
	sys.exit(-1)
try:
	for code in activation_codes:
		c.execute('INSERT INTO activation_code (code) VALUES (%s)', (code,))
	db.commit()
except:
	print("Can not add codes to database.")
	sys.exit(-1)
finally:
	db.close()
print('All code has been added to database.')