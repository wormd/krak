import krapi
from datetime import datetime as dt
import plotly.graph_objects as go
import pandas
from utility import *

pk, sk = read_keys('keys.txt')
k = krapi.krapi(pk, sk)
k.debug = True

# k.public_asset_pairs()
since = dt(2019, 6, 6).timestamp()
result,last = k.ohlc('XBTEUR', interval=60 * 24, since=since)
if result is None:
    exit(-1)
for i in result:
    i[0] = dt.fromtimestamp(i[0])

df = pandas.DataFrame(result, columns=['date', 'open', 'high',
                                       'low', 'close', 'vwap', 'volume', 'count'])

fig = go.Figure(data=go.Candlestick(x=df['date'],
                                    open=df['open'],
                                    high=df['high'],
                                    low=df['low'],
                                    close=df['close']))

fig.show()
