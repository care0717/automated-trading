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
  data = fetch_last_data(length_of_sequences+300)
  info_list = [  # 'close', 'high', 'low',
    'volumefrom', 'volumeto',
    "ETC", 'ETH', 'BCH', 'XRP', 'LTC']
  data.columns = ['close', 'high', 'low',
          'open', 'date'] + info_list

  info_list = info_list + ['close', 'high', 'low']

  for i in info_list:
    data[i] = data[i] / max(data[i])

  
  data = data.sort_values(by='date')
  data = data.reset_index(drop=True)
  data = data.loc[:, ['date'] + info_list]
  prediction = Prediction()

  x, y = prediction.load_data(
    data[info_list], length_of_sequences)
  y = np.append(y, 10)
  retX = prediction.create_predict_data(data[info_list], length_of_sequences)

  print(data['close'])#*data.std(axis=0)+data.mean(axis=0))  
  #print(retX)
  
  prediction.length_of_sequences = length_of_sequences
  prediction.create_model('bitflyer_weights_which_lstm64-32.h5')
  predicted = prediction.model.predict(retX)
  res = []
  score = 0
  score_for_buy = 0
  score_for_sell = 0
  l = len(predicted)-1
  buy_count = 0
  sell_count = 0
  for i in range(l):
    res.append(np.append(predicted[i], y[i]))
    predicted_round = int(round(predicted[i][0]))
    print(predicted[i][0], predicted_round, y[i])
    if predicted_round == y[i]:
      score += 1.0/(l)
    if predicted_round == 1:
      buy_count += 1
      if predicted_round == y[i]: 
        score_for_buy += 1
    else: 
      sell_count += 1
      if predicted_round == y[i]:
        score_for_sell += 1
  
  score_for_buy /= buy_count
  score_for_sell /= sell_count

  print("score", score)
  print("score_buy", score_for_buy)
  print("score_sell", score_for_sell)

  print("future", predicted[l][0])