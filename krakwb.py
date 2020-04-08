import kraws
import json

def callback(ws, msg):
    pass

def ohlc_5_xbteur(ws, msg):
    pass

def ohlc_5_xbtusd(ws, msg):
    pass

def ohlc_1_xbteur(ws, msg):
    pass

def another(ws, msg):
    pass


a = kraws.kraws('a','b')
a.public_subscribe({"pair": ["XBT/EUR"],
						"subscription": {"interval": 5,"name": "ohlc"}
					}, ohlc_5_xbteur)
a.public_subscribe({"pair": ["XBT/USD"],
                        "subscription": {"interval": 5,"name": "ohlc"}
                    }, ohlc_5_xbtusd)
# a.public_subscribe({"pair": ["XBT/EUR"],
#                         "subscription": {"interval": 1,"name": "ohlc"}
#                     }, ohlc_1_xbteur)

# a.private_subscribe(
#     {
#       "TDLH43-DVQXD-2KHVYY": {
#         "cost": "1000000.00000",
#         "fee": "1600.00000",
#         "margin": "0.00000",
#         "ordertxid": "TDLH43-DVQXD-2KHVYY",
#         "ordertype": "limit",
#         "pair": "XBT/EUR",
#         "postxid": "OGTT3Y-C6I3P-XRI6HX",
#         "price": "100000.00000",
#         "time": "1560516023.070651",
#         "type": "sell",
#         "vol": "1000000000.00000000"
#         }
#     }, another)


