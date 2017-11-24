# -*- coding: utf-8 -*-

from lib import pybitflyer
from bitflyer_learn import *
import requests
from sklearn import preprocessing
import numpy
import pandas as pd

def create_target_data(data, n_prev):
  X = []
  tmp = []
  for i in data:
    tmp.append([i])
  data = tmp
  for i in range(len(data) - n_prev):
    X.append(data[i+1:(i + 1 + n_prev)])
  retX = numpy.array(X)
  return retX

if __name__ == '__main__':


  length_of_sequences = 24
 
  #url = 'https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=JPY&limit='+str(length_of_sequences+1)+'&e=bitFlyer'
  #data = requests.get(url).json()["Data"]
  #now_data = pd.DataFrame.from_dict(data)
  #print(now_data)

  data_ = pandas.read_csv('./bitflyer_BTCJPY.csv')
  data_.columns = ['close', 'high', 'low',
                  'open', 'time', 'volumefrom', 'volumeto']
  #data_ = data_.append(now_data, ignore_index=True)
  scaled_data = preprocessing.scale(data_['close'])
  #print(data_['close']/1000000)
  
  retX = create_target_data(scaled_data[-(length_of_sequences+3):-1], length_of_sequences)

  data = numpy.array(data_['close'])
  print(retX)#*data.std(axis=0)+data.mean(axis=0))
  
  prediction = Prediction()
  prediction.length_of_sequences = length_of_sequences
  prediction.create_model('bitflyer_weights.h5')
  predicted = prediction.model.predict(retX)
  mean = 0
  price = (predicted+mean)*data.std(axis=0)+data.mean(axis=0)
  #before_price = now_data['close'][length_of_sequences-1]
  #print(predicted, price, before_price)
  #if price > before_price :
  #  print("買い")
  #else:
  #  print("うり")
