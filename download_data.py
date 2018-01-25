# -*- coding: utf-8 -*-
import json
import pandas as pd
import requests
import time
#time_stamp = "&toTs=1497034799"

def download_data(num, start_time):
  time_stamp = ""
  num = str(num)
  now = time.time()
  count = int((now-start_time)/3600/2001) + 1
  res = []
  coin_list=[ "ETC", "ETH", "BTC", "LTC", "XMR",  "DASH"]
  for i in range(count):
    print(i)
    url = 'https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=JPY&limit='+ num +'&e=bitFlyer' + time_stamp
    data = requests.get(url).json()["Data"]
    res = data + res
    time_stamp = "&toTs=" + str(data[0]['time'] - 1)
  res = pd.DataFrame.from_dict(res)[:-1]
#  for i in range(len(res)-24):
 #   average(res.iloc[i:i+24])

  for c in coin_list:
    time_stamp = "" 
    tmp = []
    print(c)
    for i in range(count):
      url = 'https://min-api.cryptocompare.com/data/histohour?fsym='+ c +'&tsym=USD&limit='+ num +'&e=poloniex' + time_stamp
      data = requests.get(url).json()["Data"]
      tmp = data + tmp
      #print(data)
      time_stamp = "&toTs=" + str(data[0]['time'] - 1)
    tmp = pd.DataFrame.from_dict(tmp)[:-1]
    tmp.rename(columns={'close': c}, inplace=True)
    res = pd.concat([res, tmp[c]], axis=1)
  return res


def fetch_last_data(num):
  res = []
  num = str(num)
  coin_list=[ "ETC", "ETH", "BCH", "XRP", "LTC"]
  url = 'https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=JPY&limit='+ num +'&e=bitFlyer'
  data = requests.get(url).json()["Data"]
  res = data + res
  res = pd.DataFrame.from_dict(res)[:-1]
  for c in coin_list:
    url = 'https://min-api.cryptocompare.com/data/histohour?fsym='+ c +'&tsym=USD&limit='+ num +'&e=poloniex'
    data = requests.get(url).json()["Data"]
    data = pd.DataFrame.from_dict(data)[:-1]
    data.rename(columns={'close': c}, inplace=True)
    res = pd.concat([res, data[c]], axis=1)
  return res


if __name__ == '__main__':
  start_time = 1472260800 # 1435125599　はじめはすてる
  res = download_data(2000, start_time)
  res[res.time >= start_time].to_csv("bitflyer_BTCJPY_.csv", index=False)
