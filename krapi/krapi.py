import requests
import time
import hashlib
import base64
import hmac
import urllib
import logging
from datetime import datetime as dt

class krapi:

    def __init__(self, pk, sk):
        self.pk = pk
        self.sk = sk
        self.api_url = 'https://api.kraken.com'
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'KrAPI'})
        self.counter = 0
    
    def setLogging(self, level):
        logging.basicConfig(level=level,
                format='[%(levelname)s] %(message)s', )


    def public_query(self, query, data={}):
        url_path = '/0/public/' + query

        r, l = self._query(url_path, data, False)
        return r, l


    def private_query(self, query, data={}):
        url_path = '/0/private/' + query

        r, l = self._query(url_path, data, True)
        return r, l


    def _query(self, url, data={}, private=False):
        headers=None
        if private:
            data['nonce'] = int(time.time() * 1000)
            headers = {
                'API-Key': self.pk,
                'API-Sign': self._sign(url, data)
            }

        logging.debug('Query Url: '+url)
        logging.debug('Data: '+str(data))
        if private:
            logging.debug('Private: yes'+', Headers: '+str(headers))
        else:
            logging.debug('Private: no')

        response = self.session.post(self.api_url + url, data=data, headers=headers)
        response = response.json()
        logging.debug('Raw Response: ' + str(response)[:100]+'...')
        
        if len(response['error']) > 0:
            logging.error(response['error'][0])
            return None, None

        last = None
        if 'last' in response:
            last = response['last']
            logging.debug('Last: '+str(last))

        return response['result'], last
            

    def _sign(self, url_path, data={}):
        first = (str(data['nonce']) + urllib.parse.urlencode(data)).encode()
        digested = hashlib.sha256(first).digest()

        string = url_path.encode() + digested

        digest = hmac.new(base64.b64decode(self.sk), string, hashlib.sha512).digest()

        return base64.b64encode(digest).decode()


    def ohlc(self, pair, interval=None, since=None):
        params = {'pair': pair}
        if interval:
            params['interval'] = interval
        if since:
            params['since'] = since

        result, last = self.public_query('OHLC', params)

        pair = list(result.keys())[0]

        return result[pair], last
