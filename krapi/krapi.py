import requests
import time
import hashlib
import base64
import hmac
import urllib
import datetime
import tabulate

class kraken:
    
    def __init__(self, pk, sk):
        self.pk = pk
        self.sk = sk
        self.api_url = 'https://api.kraken.com'
        self.session = requests.Session()
        self.session.headers.update({'User-Agent':'KrAPI'})
        self.response = None
        self.counter = 0
        self.debug = True

    def public_query(self, query, data={}):
        url_path = '/0/public/'+query
        
        query_url = self.api_url+url_path
        self.response = self.session.post(query_url, data)
        return self.response.json()


    def private_query(self, query, data={}):

        url_path = '/0/private/'+query
        data['nonce'] = int(time.time()*1000)
        
        headers = {
            'API-Key': self.pk,
            'API-Sign': self._sign(url_path, data)
        }

        query_url = self.api_url+url_path
        self.response = self.session.post(query_url, data, headers=headers)

        return self.response.json()
   

    def _sign(self, url_path, data={}):
        first = (str(data['nonce'])+urllib.parse.urlencode(data)).encode()
        digested_first = hashlib.sha256(first).digest()

        string = url_path.encode()+digested_first

        digest = hmac.new(base64.b64decode(self.sk), string, hashlib.sha512).digest()

        return base64.b64encode(digest).decode()


    def _write_output(self, data, file):
        header = """ 
        <html><head><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" 
        integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        </head><body>
                """

        footer = "</body></html>"

        data = data.replace("<table>","<table class='table'")

        data = header + data + footer
    
        with open(file, 'w+') as fp:
            fp.write(data)
            fp.close()


    def public_trades(self, pair):

        resp = self.public_query('Trades', {'pair': pair})

        if resp['error']:
            for error in resp['error']:
                print("ERROR: "+error)

        if self.debug and 'result' in resp:
            for key in resp['result']:
                if key == 'last':
                    break

                result = resp['result'][key]
                
                #result.sort(reverse = True, key = lambda x: x[1]) # sort by volume
                for item in result:
                    item[2] = datetime.datetime.fromtimestamp(item[2])

                    tab = tabulate.tabulate(result, 
                    headers=['price', 'volume', 'time', 'buy/sell', 'market/limit', 'misc'],
                    tablefmt='html',
                    floatfmt='.5f')

                    self._write_output(tab, './PublicTrades.html')

        return resp

    def ohlc(self, pair):
	    # resp = self.public_query('OHLC', {'pair': pair})
	    # print(resp)
        pass

    def public_asset_pairs(self):
       
        resp = self.public_query('AssetPairs')

        if resp['error']:
            for error in resp['error']:
                print("ERROR: "+error)

        for pair in resp['result']:
            pass

        print(resp)
