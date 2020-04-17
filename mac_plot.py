import pandas
from utility import *
import numpy
import matplotlib.pyplot as plt

def moving_average_crossover(df, long_window = 100, short_window = 40, incr = 0.0):
    signals = pandas.DataFrame(index=df.index)
    signals['signal'] = 0.0

    signals['short_mavg'] = df['close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = df['close'].rolling(window=long_window, min_periods=1, center=False).mean()
    if incr != 0.0:
        signals['short_mavg'] = signals['short_mavg'] - signals['short_mavg']*(incr/2)
        signals['long_mavg'] = signals['long_mavg'] + signals['long_mavg']*(incr/2)

    signals['signal'][short_window:] = numpy.where(
        signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:],
        1.0, 0.0)

    signals['positions'] = signals['signal'].diff()
    
    return signals

df = update_ohlc_data('zz_ohlc_1d', interval=60*24)
signals = moving_average_crossover(df, 20, 8)

fig = plt.figure()
ax1 = fig.add_subplot(111,  ylabel='XBTEUR')
df['close'].plot(ax=ax1, color='r', lw=2.)

plot_signal(ax1, signals, 'signals')

plt.show()

