# -*- coding: utf-8 -*-
import json
import pandas as pd
import requests
import time
#time_stamp = "&toTs=1497034799

def download_data(period):  
  before_data=pd.read_csv("bitflyer_BTC_"+str(period)+".csv")
  print(before_data["time"][len(before_data.index)-1])
  after = before_data["time"][len(before_data.index)-1]-period 
  
  coin_list=[ "ETC", "ETH", "BTC" , "LTC", "DASH"]
  market_list=["poloniex", "bitfinex", "kraken",  "bittrex"]
  url = 'https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc?periods='+str(period)+'&after='+str(after)
  data = requests.get(url).json()["result"][str(period)]
  res = pd.DataFrame.from_dict(data)[:-2]
  res.columns=["time", "open", "high", "low", "close", "volume", "nazo" ]
  res.drop("nazo", axis=1)
  
  url = 'https://api.cryptowat.ch/markets/bitflyer/ethbtc/ohlc?periods='+str(period)+'&after='+str(after)
  data = requests.get(url).json()["result"][str(period)]
    
  tmp = pd.DataFrame.from_dict(data)[:-2]
  tmp.columns=["time", "open", "high", "low", "close", "volume", "nazo"]
  tmp.rename(columns={'close': "bitflyerETH"}, inplace=True)

  res = pd.concat([res, tmp["bitflyerETH"]], axis=1)

  url = 'https://api.cryptowat.ch/markets/quoine/btcjpy/ohlc?periods='+str(period)+'&after='+str(after)
  data = requests.get(url).json()["result"][str(period)]
    
  tmp = pd.DataFrame.from_dict(data)[:-2]
  tmp.columns=["time", "open", "high", "low", "close", "volume", "nazo"]
  tmp.rename(columns={'close': "quoineBTC"}, inplace=True)

  res = pd.concat([res, tmp["quoineBTC"]], axis=1)

  for c in coin_list:

    for m in market_list:
      print(m)
      if m=="bittrex" or m=="poloniex":
        url = 'https://api.cryptowat.ch/markets/'+str(m)+'/'+c+'usdt/ohlc?periods='+str(period)+'&after='+str(after)
      else:
        url = 'https://api.cryptowat.ch/markets/'+str(m)+'/'+c+'usd/ohlc?periods='+str(period)+'&after='+str(after)

      data = requests.get(url).json()["result"][str(period)]
      tmp = pd.DataFrame.from_dict(data)[:-2]
      tmp.columns=["time", "open", "high", "low", "close", "volume", "nazo"]
      tmp.rename(columns={'close': m+c}, inplace=True)

      res = pd.concat([res, tmp[m+c]], axis=1)
  res = res[res.time > before_data["time"][len(before_data.index)-1]]
  
  return pd.concat([before_data, res])


if __name__ == '__main__':
  period = int(input())
  res = download_data(period)
  res.to_csv("bitflyer_BTC_"+str(period)+".csv", index=False)
