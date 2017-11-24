# -*- coding: utf-8 -*-
import json
import pandas as pd
import requests

#time_stamp = "&toTs=1497034799"
time_stamp = ""
res = []
for i in range(19):
  print(i)
  url = 'https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=JPY&limit=2000&e=bitFlyer' + time_stamp
  data = requests.get(url).json()["Data"]
  res = data + res
  time_stamp = "&toTs=" + str(data[0]['time'] - 1)
pd.DataFrame.from_dict(res).to_csv("bitflyer_BTCJPY.csv", index=False)
