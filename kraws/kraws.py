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
        self.url_token = 'https://api.kraken.com/0/private/GetWebSocketsToken'

    def public_subscribe(self, query, callback):
        self._subscribe(query, callback, None)

    def private_subscribe(self, query, callback):
        self._subscribe(query, callback, self.get_token())

    def _subscribe(self, query, callback, token):
        ws = ws_conn(callback, query, token)

    def get_token(self):
        self.session = requests.Session()

        data = {'nonce': int(time.time() * 1000)}

        kr = krapi.krapi(self.pk, self.sk)
        headers = {
            'API-Key': self.pk,
            'API-Sign': kr._sign(self.url_token, data)
        }

        self.response = self.session.post(self.url_token, data, headers=headers)
        return self.response.json()['result']['token']


class ws_conn():
    def __init__(self, callback, query, token):
        self.callback = callback
        self.token = token
        self.query = query

        logging.basicConfig(level=logging.DEBUG,
                            format='[%(levelname)s] (%(threadName)-10s) %(message)s', )
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
        self.callback(self, msg)

    def on_open(self):
        logging.info('++ Connected ++')
        message = {
            'event': 'subscribe',
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
