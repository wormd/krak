import kraws
import json
from utility import *


def callback(ws, msg):
    pass


def ohlc_5_xbteur(ws, msg):
    pass


def ohlc_5_xbtusd(ws, msg):
    pass


def ohlc_1_xbteur(ws, msg):
    pass


def another(ws, msg):
    print('msg: '+msg)

pk, sk = read_keys('keys2.txt')
a = kraws.kraws(pk, sk)
a.public_subscribe({'event': 'subscribe',
                    "pair": ["XBT/EUR"],
                    "subscription": {"interval": 5, "name": "ohlc"}
                    }, ohlc_5_xbteur)
a.public_subscribe({'event': 'subscribe',
                    "pair": ["XBT/USD"],
                    "subscription": {"interval": 5, "name": "ohlc"}
                    }, ohlc_5_xbtusd)
a.public_subscribe({'event': 'subscribe',
                    "pair": ["XBT/EUR"],
                    "subscription": {"interval": 1,"name": "ohlc"}
                    }, ohlc_1_xbteur)

a.private_subscribe(
    {
    "event": "addOrder",
    "ordertype": "limit",
    "pair": "XBT/USD",
    "price": "500",
    "type": "buy",
    "volume": "10"
     }, another)
