# -*- coding: utf-8 -*-
import numpy
import pandas
import matplotlib.pyplot as plt

from sklearn import preprocessing
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM


class Prediction:
  def __init__(self):
    self.model = Sequential()
    self.length_of_sequences = 10
    self.in_out_neurons = 1
    self.hidden_neurons = 300

  def load_data(self, data, n_prev=10):
    X, Y = [], []
    for i in range(len(data) - n_prev):
      X.append(data.iloc[i:(i + n_prev)].as_matrix())
      Y.append(data.iloc[i + n_prev].as_matrix())
    retX = numpy.array(X)
    retY = numpy.array(Y)
    return retX, retY

  def create_model(self, weights_path=None):
    self.model.add(LSTM(self.hidden_neurons,
                   batch_input_shape=(
                       None, self.length_of_sequences, self.in_out_neurons),
                   return_sequences=False))
    self.model.add(Dense(self.in_out_neurons))
    self.model.add(Activation("linear"))
    if weights_path:
      self.model.load_weights(weights_path)
    self.model.compile(loss="mape", optimizer="adam")
    #return self


  def train(self, X_train, y_train):
    #model = self.create_model()
    # 学習
    self.model.fit(X_train, y_train, batch_size=10, nb_epoch=10)
    #return self


if __name__ == "__main__":

  prediction = Prediction()

  # データ準備
  data = None
  data_ = pandas.read_csv('./bitflyer_BTCJPY.csv')
  data = data_ if (data is None) else pandas.concat([data, data_])
  data.columns = ['close', 'high', 'low',
                  'open', 'date', 'volumefrom', 'volumeto']
  #data['date'] = pandas.to_datetime(data['date'], format='%Y-%m-%d')
  # 終値のデータを標準化
  data['close'] = preprocessing.scale(data['close'])
  data = data.sort_values(by='date')
  data = data.reset_index(drop=True)
  data = data.loc[:, ['date', 'close']]
  #print(data)
  # 2割をテストデータへ
  split_pos = int(len(data) * 0.8)
  x_train, y_train = prediction.load_data(
      data[['close']].iloc[0:split_pos], prediction.length_of_sequences)
  x_test,  y_test = prediction.load_data(
      data[['close']].iloc[split_pos:], prediction.length_of_sequences)
  #print(x_test)
  #print(y_test)
  prediction.create_model('bitflyer_weights.h5')
  prediction.train(x_train, y_train)
  prediction.model.save_weights('bitflyer_weights.h5')

  predicted = prediction.model.predict(x_test)
  result = pandas.DataFrame(predicted)
  result.columns = ['predict']
  result['actual'] = y_test
  result.plot()
  plt.show()
