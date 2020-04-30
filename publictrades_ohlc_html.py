import krapi
from utility import *
from datetime import datetime as dt
import tabulate as tb
import logging

pk, sk = read_keys('keys.txt')
k = krapi.krapi(pk, sk)
k.setLogging(logging.INFO)

result, last = k.public_query('Trades', {'pair':'XBTEUR'})
if result is None:
    exit(-1)
for item in result:
    item[2] = datetime.fromtimestamp(item[2])

# sort by volume
result.sort(reverse = True, key = lambda x: x[1])
tab = tb.tabulate(result,
                  headers=['price', 'volume', 'time', 'buy/sell', 'market/limit', 'misc'],
                  tablefmt='html',
                  floatfmt='.5f')

print('Writing public/Trades to zzTrades.html')
write_html(tab, './zzTrades.html')


result, last = k.ohlc('XBTEUR', interval=1, )
if result is None:
    exit(-1)
for item in result:
    item[0] = dt.fromtimestamp(item[0])

tab = tb.tabulate(result, headers=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'],
                  tablefmt='html',
                  floatfmt='0.1f')

print('Writing public/OHLC to zzOhlc.html')
write_html(tab, './zzOhlc.html')
