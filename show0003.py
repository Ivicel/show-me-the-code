import redis
from show0001 import make_active_codes


r = redis.Redis(host='localhost')
r.sadd('activation_codes', make_active_codes())
print('All codes have been added.')