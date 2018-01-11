# -*- coding: utf-8 -*-
import json
import pandas as pd
import requests
import time
#time_stamp = "&toTs=1497034799"

def download_data(period):  
  #before_data=pd.read_csv("bitflyer_BTC_"+str(period)+".csv")
  
  after = 1483196400#before_data["time"][len(before_data.index)-1]-period 
  
  coin_list=[ "ETC", "ETH", "BTC"]
  market_list=["bitfinex", "kraken",  "bittrex"]
  url = 'https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc?periods='+str(period)+'&after='+str(after)
  data = requests.get(url).json()["result"][str(period)]
  res = pd.DataFrame.from_dict(data)[:-1]
  res.columns=["time", "open", "high", "low", "close", "volume", "nazo" ]
  res.drop("nazo", axis=1)


  for c in coin_list:
    print(c)
    url = 'https://api.cryptowat.ch/markets/poloniex/'+str(c)+'usdt/ohlc?periods='+str(period)+'&after='+str(after)
    data = requests.get(url).json()["result"][str(period)]
    
    tmp = pd.DataFrame.from_dict(data)[:-1]
    tmp.columns=["time", "open", "high", "low", "close", "volume", "nazo"]
    tmp.rename(columns={'close': c}, inplace=True)

    res = pd.concat([res, tmp[c]], axis=1)
  for m in market_list:
    print(m)
    if m=="bittrex":
      url = 'https://api.cryptowat.ch/markets/'+str(m)+'/btcusdt/ohlc?periods='+str(period)+'&after='+str(after)
    else:
      url = 'https://api.cryptowat.ch/markets/'+str(m)+'/btcusd/ohlc?periods='+str(period)+'&after='+str(after)

    data = requests.get(url).json()["result"][str(period)]
    tmp = pd.DataFrame.from_dict(data)[:-1]
    tmp.columns=["time", "open", "high", "low", "close", "volume", "nazo"]
    tmp.rename(columns={'close': m}, inplace=True)

    res = pd.concat([res, tmp[m]], axis=1)
  #res = res[res.time > before_data["time"][len(before_data.index)-1]]
  
  return res#pd.concat([before_data, res])


if __name__ == '__main__':
  period = 60
  res = download_data(period)
  res.to_csv("bitflyer_BTC_"+str(period)+"_.csv", index=False)
