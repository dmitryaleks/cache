import sys
import string
import time
import random
import redis

cache = redis.Redis(host='localhost', port=6379, db=0, password='pwd')

rateEvtSec = int(sys.argv[1])
testLoadTimeSec = int(sys.argv[2])

delayBwEventsSec = 1./rateEvtSec
totalEvents = rateEvtSec * testLoadTimeSec

for i in range(totalEvents):
    token = ''.join(random.choices(string.ascii_letters, k=3))
    if (i%2 == 0):
        cache.get(token)
    else:
        value = ''.join(random.choices(string.ascii_letters, k=16))
        cache.set(token, value)
    time.sleep(delayBwEventsSec)

