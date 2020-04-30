from mac_plot import *
from numpy import arange

def populate_pairs(minmax, ratios):
    pairs = []
    for ratio in arange(ratios[0], ratios[1], 0.25):
        for n in arange(minmax[0], minmax[1], 2.0):
            c = n*ratio
            if c > minmax[1]:
                break
            pairs.append((int(c), int(n)))
    return pairs



if __name__ == "__main__":
    ratios = []
    df = update_ohlc_data('zz_ohlc_1d', interval=60*24)
    #df = update_ohlc_data('zz_ohlc_1h', interval=60)

    win_pairs = populate_pairs([5, 200], [2, 6.25])
    
    for longw, shortw in win_pairs:
        signals = moving_average_crossover(df, longw, shortw, 0.0)
        res, last = run_on_funds(df, signals, 500, False)
        sratio = sharpe_ratio(res, False)
        ratios.append((sratio, longw, shortw, round(longw/shortw, 2)))
    
    ratios = list(filter(lambda x: x[0] > 1.0, ratios))
    ratios.sort(reverse=True, key = lambda x: x[0])
    print(ratios)

    