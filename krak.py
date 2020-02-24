import krapi

import datetime
import time
import calendar

with open('keys.txt','r') as fp:
	pk = fp.readline().rstrip()
	sk = fp.readline().rstrip()

print('e')
k = krapi.kraken(pk, sk)
k.debug = True

k.public_trades('XBTEUR')
k.public_asset_pairs()

#k.ohlc('XBTEUR')


# def date_nix(str_date):
#     return calendar.timegm(str_date.timetuple())

# def date(start, end, ofs):
#     req_data = {'type': 'all',
#                 'trades': 'true',
#                 'start': str(date_nix(start)),
#                 'end': str(date_nix(end)),
#                 'ofs': str(ofs)
#                 }
#     return req_data

# data = []
# count = 0
# for i in range(1,11):
#     start_date = datetime.datetime(2020, i+1, 1)
#     end_date = datetime.datetime(2020, i+2, 29)
#     th = k.private_query('TradesHistory', date(start_date, end_date, 1))
#     time.sleep(.25)
#     print(th)
#     th_error = th['error']
#     try:
#         if int(th['result']['count'])>0:
#             count += th['result']['count']
#             data.append(pd.DataFrame.from_dict(th['result']['trades']).transpose())
#     except Exception as e:
#         print(e)

