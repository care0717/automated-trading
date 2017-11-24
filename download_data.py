# -*- coding: utf-8 -*-
import json
import pandas as pd
import requests
import time
#time_stamp = "&toTs=1497034799"
time_stamp = ""
start_time = 1435125599
now = time.time()
count = int((now-start_time)/3600/2001) + 1

res = []
coin_list=[ "ETC", "ETH", "BCH", "XRP", "LTC"]

for i in range(count):
  print(i)
  url = 'https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=JPY&limit=2000&e=bitFlyer' + time_stamp
  data = requests.get(url).json()["Data"]
  res = data + res
  time_stamp = "&toTs=" + str(data[0]['time'] - 1)
res = pd.DataFrame.from_dict(res)[:-1]
for c in coin_list:
  time_stamp = "" 
  tmp = []
  for i in range(count):
    print(i)
    url = 'https://min-api.cryptocompare.com/data/histohour?fsym='+ c +'&tsym=USD&limit=2000&e=poloniex' + time_stamp
    data = requests.get(url).json()["Data"]
    tmp = data + tmp
    time_stamp = "&toTs=" + str(data[0]['time'] - 1)
  tmp = pd.DataFrame.from_dict(tmp)[:-1]
  tmp.rename(columns={'close': c}, inplace=True)
  res = pd.concat([res, tmp[c]], axis=1)
  
res[res.time >= start_time].to_csv("bitflyer_BTCJPY_.csv", index=False)