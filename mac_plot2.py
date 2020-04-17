import pandas
from utility import *
import numpy
import matplotlib.pyplot as plt
import mac_plot as mac

def run_on_funds(df, signals, funds):
    print("Running simulation on: "+str(funds)+"eur")
    FEE = 0.26
    ret = []
    bought_1st_time = False
    for index, row in signals.query('positions==1.0 or positions==-1.0').iterrows():
        fee = funds/100*FEE
        funds -= fee
        value = df.loc[index, 'close']

        if row.positions == 1.0: # buying
            bought_1st_time = True            
            print("On: "+str(index)+" buying "+"{:.2f}".format(funds)+"eur worth of BTC ("+str(value)+"), with a fee of: "+"{:.2f}".format(fee)+"eur")
        elif row.positions == -1.0: # selling
            if not bought_1st_time:
                continue
            last_index = ret[len(ret)-1][0]
            # funds = funds / last_buy_value * current_value
            funds = funds/df.loc[last_index, 'close'] * value
            print("On: "+str(index)+" selling "+"{:.2f}".format(funds)+"eur worth of BTC ("+str(value)+"), with a fee of: "+"{:.2f}".format(fee)+"eur")

        ret.append((index, funds))
    return ret
        

#################################

df_daily = update_ohlc_data('zz_ohlc_1d', interval=60*24)
df_hourly = update_ohlc_data('zz_ohlc_1h', interval=60)
df_concat = pandas.concat([df_daily, df_hourly])
#df_concat = df_concat.loc[df_concat.index.duplicated(keep='first')]

signals = mac.moving_average_crossover(df_daily, 50, 10, 0.0)
signals2 = mac.moving_average_crossover(df_hourly, 240, 96, 0.0)

fig, (ax1,ax2) = plt.subplots(2)

df_concat['close'].plot(ax=ax1, color='r', lw=1.)
df_hourly['close'].plot(ax=ax2, color='r', lw=1.)

mac.plot_signal(ax1, signals, 'signals')
mac.plot_signal(ax2, signals2, 'signals2')

res = run_on_funds(df_daily, signals, 500)
res = run_on_funds(df_hourly, signals2, res[len(res)-1][1])

plt.show()

