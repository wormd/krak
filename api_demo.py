import krapi
from utility import *
import logging

pk, sk = read_keys('keys2.txt')
k = krapi.krapi(pk, sk)
#k.setLogging(logging.DEBUG)
k.setLogging(logging.ERROR)

r, l = k.public_query('AssetPairs')
r = list(r.keys())
print("Pairs: " + str(r))

r, l = k.private_query('Balance')
print("Current Balances: " + str(r))