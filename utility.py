import os
import krapi
import pandas
from datetime import datetime as dt
import matplotlib.pyplot as plt
import numpy


def write_html(data, file):
    header = """ 
    <html><head><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" 
    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    </head><body>
            """

    footer = "</body></html>"

    data = data.replace("<table>", "<table class='table'")

    data = header + data + footer

    with open(file, 'w+') as fp:
        fp.write(data)
        fp.close()


def read_keys(file):
    with open(file, 'r') as fp:
        pk = fp.readline().rstrip()
        sk = fp.readline().rstrip()
        return pk, sk


def read_vars(file, iter = 1):
    try:
        with open(file, 'r') as fp:
            vars = []
            for i in range(0, iter):
                vars.append(fp.readline().rstrip())
            if len(vars) == 1:
                return vars[0]
            else:
                return tuple(vars)
    except IOError:
        return None
    

def get_path(file):
    return file[0:file[0:len(file)-1].rfind('/')]


def write_vars(file, *args):
    path = get_path(file)
    if not os.path.exists(path):
        os.mkdir(path)
    with open(file, 'w+') as fp:
        for i in args:
            if i:
                fp.write(str(i)+'\r\n')


def update_ohlc_data(path = None, pair = 'XBTEUR', interval = 60*24):
    FOLDERPATH = 'charts'
    if path is not None:
        FOLDERPATH = path
    SINCEPATH = FOLDERPATH+'/since.txt'
    DATAPATH = FOLDERPATH+'/data.csv'

    pk, sk = read_keys('keys.txt')
    k = krapi.krapi(pk, sk)
    #k.setLogging(logging.DEBUG)

    df = None
    dateparse = lambda dates: [dt.strptime(d, '%Y-%m-%d %H:%M:%S') for d in dates]

    if not os.path.isdir(FOLDERPATH):
        os.mkdir(FOLDERPATH)
    if os.path.isfile(DATAPATH):
        df = pandas.read_csv(DATAPATH, parse_dates=True, index_col='date') # date_parser=dateparse
    
    since = read_vars(SINCEPATH, 1)
    result, last = k.ohlc(pair, interval=interval, since=since)
    if result is None:
        exit(-1)

    if len(result) == 1:
            return df
    
    write_vars(SINCEPATH, last)

    new = pandas.DataFrame(result, columns=['date', 'open', 'high',
                                        'low', 'close', 'vwap', 'volume', 'count'])

    new.set_index('date', inplace=True)
    new.index = pandas.to_datetime(new.index, unit='s')
    
    new = new.astype({'open':'float64', 'high':'float64', 'low':'float64',
        'close':'float64', 'vwap':'float64', 'volume':'float64'})

    if df is None:
        new.to_csv(DATAPATH)
    else:
        df.drop(df.tail(1).index, inplace=True)
        new = pandas.concat([df, new])
        new.to_csv(DATAPATH)
    return new