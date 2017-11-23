# -*- coding: utf-8 -*-
import json
import requests
import time
import hmac
import hashlib
import urllib


class API(object):

    def __init__(self, api_key=None, api_secret=None):
        self.api_url = "https://api.bitflyer.jp"
        self.api_key = api_key
        self.api_secret = api_secret

    def request(self, endpoint, method="GET", params=None):
        url = self.api_url + endpoint
        body = ""
        auth_header = None

        if method == "POST":
            body = json.dumps(params)
        else:
            if params:
                body = "?" + urllib.parse.urlencode(params)

        if self.api_key and self.api_secret:
            access_timestamp = str(time.time())
            api_secret = str.encode(self.api_secret)
            text = str.encode(access_timestamp + method + endpoint + body)
            access_sign = hmac.new(api_secret,
                                   text,
                                   hashlib.sha256).hexdigest()
            auth_header = {
                "ACCESS-KEY": self.api_key,
                "ACCESS-TIMESTAMP": access_timestamp,
                "ACCESS-SIGN": access_sign,
                "Content-Type": "application/json"
            }

        try:
            with requests.Session() as s:
                if auth_header:
                    s.headers.update(auth_header)

                if method == "GET":
                    response = s.get(url, params=params)
                else:  # method == "POST":
                    response = s.post(url, data=json.dumps(params))
        except requests.RequestException as e:
            print(e)
            raise e

        content = ""
        if len(response.content) > 0:
            content = json.loads(response.content.decode("utf-8"))

        return content

    """HTTP Public API"""

    def board(self, **params):
        """Order Book

        API Type
        --------
        HTTP Public API

        Parameters
        ----------
        product_code: Designate "BTC_JPY", "FX_BTC_JPY" or "ETH_BTC".

        Docs
        ----
        https://lightning.bitflyer.jp/docs?lang=en#order-book
        """
        endpoint = "/v1/board"
        return self.request(endpoint, params=params)

    def ticker(self, **params):
        """Ticker

        API Type
        --------
        HTTP Public API

        Parameters
        ----------
        product_code: Designate "BTC_JPY", "FX_BTC_JPY" or "ETH_BTC".

        Docs
        ----
        https://lightning.bitflyer.jp/docs?lang=en#ticker
        """
        endpoint = "/v1/ticker"
        return self.request(endpoint, params=params)

    def executions(self, **params):
        """Execution History

        API Type
        --------
        HTTP Public API

        Parameters
        ----------
        product_code: Designate "BTC_JPY", "FX_BTC_JPY" or "ETH_BTC".
        count, before, after: See Pagination.

        Docs
        ----
        https://lightning.bitflyer.jp/docs?lang=en#execution-history
        """
        endpoint = "/v1/executions"
        return self.request(endpoint, params=params)

    def gethealth(self, **params):
        """Exchange status
        This will allow you to determine the current status of the exchange.

        API Type
        --------
        HTTP Public API

        Parameters
        ----------
        product_code: Designate "BTC_JPY", "FX_BTC_JPY" or "ETH_BTC".
        count, before, after: See Pagination.

        Response
        --------
        status: one of the following levels will be displayed
            NORMAL: The exchange is operating.
            BUSY: The exchange is experiencing heavy traffic.
            VERY BUSY: The exchange is experiencing extremely heavy traffic. There is a possibility that orders will fail or be processed after a delay.
            STOP: The exchange has been stopped. Orders will not be accepted.

        Docs
        ----
        https://lightning.bitflyer.jp/docs?lang=en#exchange-status
        """
        endpoint = "/v1/gethealth"
        return self.request(endpoint, params=params)

    def getchats(self, **params):
        """ Chat
        Get an instrument list

        API Type
        --------
        HTTP Public API

        Parameters
        ----------
        from_date: This accesses a list of any new messages after this date.

        Docs
        ----
        https://lightning.bitflyer.jp/docs?lang=en#chat
        """
        endpoint = "/v1/getchats"
        return self.request(endpoint, params=params)
