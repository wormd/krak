import krapi
import datetime as dt
import plotly.graph_objects as go
import pandas

with open('keys.txt', 'r') as fp:
    pk = fp.readline().rstrip()
    sk = fp.readline().rstrip()

k = krapi.krapi(pk, sk)
k.debug = True

# k.public_asset_pairs()

since = dt.datetime(2019, 6, 6).timestamp()

result = k.ohlc('XBTEUR', interval=60 * 24, since=since)
for i in result:
    i[0] = dt.datetime.fromtimestamp(i[0])

df = pandas.DataFrame(result, columns=['date', 'open', 'high',
                                       'low', 'close', 'vwap', 'volume', 'count'])

fig = go.Figure(data=go.Candlestick(x=df['date'],
                                    open=df['open'],
                                    high=df['high'],
                                    low=df['low'],
                                    close=df['close']))

fig.show()
