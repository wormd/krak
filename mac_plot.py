import pandas
from utility import *
import numpy
import matplotlib.pyplot as plt
import numpy as np

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

def plot_signal(ax1, signals, name=''):
    s = 'short_mavg'
    l = 'long_mavg'
    signals[[s,l]].plot(ax=ax1, lw=1.)
    ax1.plot(signals.loc[signals.positions == 1.0].index, 
            signals[s][signals.positions == 1.0],
            '^', markersize=10, color='m')

    ax1.plot(signals.loc[signals.positions == -1.0].index, 
    signals[s][signals.positions == -1.0],
    'v', markersize=10, color='k')

def run_on_funds(df, signals, funds, verbose = False):
    if verbose:
        print("Running simulation on: "+str(funds)+"eur")
    FEE = 0.26
    ret = []
    bought_1st_time = False
    for index, row in signals.query('positions==1.0 or positions==-1.0').iterrows():
        fee = funds/100*FEE
        funds -= fee
        value = df.loc[index, 'close']
        profit = 0.0
        if row.positions == 1.0: # buying
            if not bought_1st_time:
                profit = 0.0
            else:
                profit = funds - ret[len(ret)-1][1]
            bought_1st_time = True
            if verbose:
                print("On: "+str(index)+" buying "+"{:.2f}".format(funds)+"eur worth of BTC ("+str(value)+"), with a fee of: "+"{:.2f}".format(fee)+"eur")
        elif row.positions == -1.0: # selling
            if not bought_1st_time:
                continue
            last_index = ret[len(ret)-1][0]
            # funds = funds / last_buy_value * current_value
            funds = funds/df.loc[last_index, 'close'] * value
            profit = funds - ret[len(ret)-1][1]
            if verbose:
                print("On: "+str(index)+" selling "+"{:.2f}".format(funds)+"eur worth of BTC ("+str(value)+"), with a fee of: "+"{:.2f}".format(fee)+"eur")

        ret.append((index, funds, profit))
    return (pandas.DataFrame(ret, columns=['date', 'funds', 'profit']), funds)
        

def sharpe_ratio(df, verbose = False):
    ratio = np.sqrt(len(df.index)) * (df['profit'].mean() / df['profit'].std())
    if verbose:
        print('Sharpe ratio: '+str(ratio))
    return ratio


if __name__ == "__main__":
    df_daily = update_ohlc_data('zz_ohlc_1d', interval=60*24)
    df_hourly = update_ohlc_data('zz_ohlc_1h', interval=60)
    df_concat = pandas.concat([df_daily, df_hourly])
    #df_concat = df_concat.loc[df_concat.index.duplicated(keep='first')]

    signals = moving_average_crossover(df_daily, 142, 72, 0.0)
    signals2 = moving_average_crossover(df_hourly, 142, 72, 0.0)

    fig, (ax1,ax2) = plt.subplots(2)

    df_concat['close'].plot(ax=ax1, color='r', lw=1.)
    df_hourly['close'].plot(ax=ax2, color='r', lw=1.)

    plot_signal(ax1, signals, 'signals')
    plot_signal(ax2, signals2, 'signals2')

    res1, last = run_on_funds(df_daily, signals, 500, True)
    sratio1 = sharpe_ratio(res1, True)
    res2, last = run_on_funds(df_hourly, signals2, last, True)
    sratio2 = sharpe_ratio(res2, True)

    plt.show()