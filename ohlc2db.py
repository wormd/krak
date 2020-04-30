from utility import *
import pandas as pd
import kraws
import logging
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import text


def _heartbeat(msg):
    if 'event' in msg:
        if msg['event'] == "heartbeat":
            return True
    return False


class ohlc2db:
    def __init__(self):
        self.hasht = {}
        self.tables = []
        user, pwd = read_vars('db_login.txt', 2)
        engine = create_engine("mysql://"+user+":"+pwd+"@localhost/krak")
        with engine.connect() as self.conn:
            ret = self.conn.execute("SELECT * FROM data")
            pk, sk = read_keys('keys2.txt')
            kr = kraws.kraws(pk, sk)
            #kr.setLogging(logging.DEBUG)
            for i in ret:
                self.tables.append([*i, engine.connect()])
                kr.ohlc(pairs=[i[4]], reqid=i[0], interval=i[3], callback = self.handler)
                # kr.public_subscribe({'event': 'subscribe', "pair": [i[4]],"reqid": i[0],
                #                         "subscription": {"interval": i[3],"name": "ohlc"}},
                #                     self.handler)

    def handler(self, ws, msg):
        if 'channelID' in msg:
            self.hasht[str(msg['channelID'])] = msg['reqid']
        elif 'connectionID' in msg:
            pass
        elif _heartbeat(msg):
            pass
        else: # subscription message
            channel_id = str(msg[0])
            target = self.tables[self.hasht[channel_id]]
            cols = ['date','date2','open','high','low','close', 'vwap', 'volume','count']
            msg[1][0] = "'"+str(dt.fromtimestamp(float(msg[1][0])))+"'"
            msg[1][1] = "'"+str(dt.fromtimestamp(float(msg[1][1])))+"'"
            ret = target[5].execute("INSERT INTO "+target[1]+'('
                +','.join(cols)
                +') VALUES('
                +','.join(map(str, msg[1]))+')')
            ret.close()
            print("Inserted row in: "+target[1]+'\n', end='')


if __name__ == "__main__":
    obj = ohlc2db()