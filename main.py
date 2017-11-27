# -*- coding: utf-8 -*-

from lib import pybitflyer
from bitflyer_learn import *
import requests
from sklearn import preprocessing
import numpy as np
import pandas as pd
from download_data import *



if __name__ == '__main__':
  length_of_sequences = 24
  data = fetch_last_data(length_of_sequences+10)
  info_list = [  # 'close', 'high', 'low',
    'volumefrom', 'volumeto',
    "ETC", 'ETH', 'BCH', 'XRP', 'LTC']
  data.columns = ['close', 'high', 'low',
          'open', 'date'] + info_list

  for i in info_list:
    data[i] = data[i] / max(data[i])
  data['close'] = data['close'] / 1100000
  data['low'] = data['low'] / 1100000
  data['high'] = data['high'] / 1100000

  info_list = info_list + ['close', 'high', 'low']
  data = data.sort_values(by='date')
  data = data.reset_index(drop=True)
  data = data.loc[:, ['date'] + info_list]
  prediction = Prediction()

  x, y = prediction.load_data(
    data[info_list], length_of_sequences)
  y.append("*")
  retX = prediction.create_predict_data(data[info_list], length_of_sequences)

  print(data['close'])#*data.std(axis=0)+data.mean(axis=0))  
  #print(retX)
  
  prediction.length_of_sequences = length_of_sequences
  prediction.create_model('bitflyer_weights_which_lstm64-32.h5')
  predicted = prediction.model.predict(retX)
  #for i in range(len(predicted)):
  #  predicted[i].append(y[i])
  print(predicted)