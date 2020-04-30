import requests
import websocket
import json
import threading
import time
import logging
import sys

sys.path.append("..")
import krapi


class kraws:
    def __init__(self, pk, sk):
        self.pk = pk
        self.sk = sk

    def public_subscribe(self, query, callback):
        self._subscribe(query, callback, None)

    def private_subscribe(self, query, callback):
        self._subscribe(query, callback, self.get_token())

    def _subscribe(self, query, callback, token):
        ws = ws_conn(callback, query, token)

    def get_token(self):
        self.session = requests.Session()
        kr = krapi.krapi(self.pk, self.sk)        
        resp = kr.private_query('GetWebSocketsToken')
        print(resp)
        return resp['token']

    def setLogging(self, level):
        logging.basicConfig(level=level,
                            format='[%(levelname)s] (%(threadName)-10s) %(message)s', 
                        )

    def ohlc(self, pairs, reqid, interval, callback):
        self.public_subscribe({'event': 'subscribe', "pair": pairs,"reqid": reqid,
            "subscription": {"interval": interval,"name": "ohlc"}},
            callback)

class ws_conn():
    def __init__(self, callback, query, token):
        self.callback = callback
        self.token = token
        self.query = query

        self.url_pub = 'wss://ws.kraken.com'
        self.url_pri = 'wss://ws-auth.kraken.com'

        self.message = None
        self.trace = False

        self.subscription = None

        if self.trace:
            websocket.enableTrace(True)

        url = self.setUrl()

        logging.debug('++ Opening Connection ++')
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open)

        self.ws.keep_running = True

        thread = threading.Thread(target=self.ws.run_forever)
        # thread.daemon = True
        thread.start()

    def setUrl(self):
        url = ''
        if self.token:
            url = self.url_pri
        else:
            url = self.url_pub
        return url

    def on_message(self, msg):
        dejson = json.loads(msg)

        if 'channelID' in dejson:
            self.subscription = msg
            self.id = dejson['channelID']
            logging.info('Subscribed with id: ' + str(self.id))

        if 'errorMessage' in dejson:
            logging.error(dejson['errorMessage'])
            self.ws.close()

        logging.debug(msg)
        self.callback(self, dejson)

    def on_open(self):
        logging.info('++ Connected ++')
        message = {
            **self.query
        }
        if self.token:
            message['token'] = self.token

        data = json.dumps(message)
        logging.debug('>>> ' + data)
        self.ws.send(data)

    def on_error(self, msg):
        pass

    def on_close(self):
        print('++ closed connection ++')