# -*- coding: utf-8 -*-
import numpy
import pandas
import matplotlib.pyplot as plt
#import pydot
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.callbacks import EarlyStopping
from keras.utils import plot_model




class Prediction:
  def __init__(self):
    self.model = Sequential()
    self.length_of_sequences = 24
    self.in_neurons = 10
    self.out_neurons = 1
    self.hidden_neurons = 128

  def load_data(self, data, n_prev):
    X, Y = [], []
    for i in range(len(data) - n_prev):
      X.append(data.iloc[i:(i + n_prev)].as_matrix())
      if data.iloc[i + n_prev][0] > data.iloc[i + n_prev - 1][0]:
        tmp = 1
      else:
        tmp = 0
      Y.append([tmp])
    retX = numpy.array(X)
    retY = numpy.array(Y)
    return retX, retY

  def create_model(self, weights_path=None):
    self.model.add(LSTM(32,
                   batch_input_shape=(
                       None, self.length_of_sequences, self.in_neurons),
                   return_sequences=True))
    self.model.add(Dropout(0.2))
    self.model.add(LSTM(32, return_sequences=True))  # 32次元のベクトルを一つ出力する
    self.model.add(Dropout(0.2))
    self.model.add(LSTM(32, return_sequences=True))  # 32次元のベクトルを一つ出力する
    self.model.add(Dropout(0.2))
    self.model.add(LSTM(32, return_sequences=True))  # 32次元のベクトルを一つ出力する
    self.model.add(Dropout(0.2))
    self.model.add(LSTM(32))  # 32次元のベクトルを一つ出力する
    self.model.add(Dropout(0.2))
#    self.model.add(Activation("relu"))
    self.model.add(Dense(self.out_neurons))
    self.model.add(Activation("sigmoid"))
    if weights_path:
      self.model.load_weights(weights_path)
    self.model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])


  def predict(self, X_test):
    self.model.predict(X_test)

def plot_history(history):
  # 精度の履歴をプロット
  plt.plot(history.history['acc'],"o-",label="accuracy")
  plt.plot(history.history['val_acc'],"o-",label="val_acc")
  plt.title('model accuracy')
  plt.xlabel('epoch')
  plt.ylabel('accuracy')
  plt.legend(loc="lower right")
  plt.show()

  # 損失の履歴をプロット
  plt.plot(history.history['loss'],"o-",label="loss",)
  plt.plot(history.history['val_loss'],"o-",label="val_loss")
  plt.title('model loss')
  plt.xlabel('epoch')
  plt.ylabel('loss')
  plt.legend(loc='lower right')
  plt.show()

if __name__ == "__main__":

  prediction = Prediction()

  # データ準備
  data = pandas.read_csv('./bitflyer_BTCJPY_.csv')
  info_list = [#'close', 'high', 'low',
                  'volumefrom', 'volumeto',
                   "ETC", 'ETH', 'BCH', 'XRP', 'LTC']
  data.columns = ['close', 'high', 'low',
                  'open', 'date'] + info_list
  
  
  # 終値のデータを標準化
  
  for i in info_list:
    data[i]=data[i]/max(data[i])
  data['close'] = data['close']/1000000
  data['low'] = data['low']/1000000
  data['high'] = data['high']/1000000

  info_list = info_list + ['close', 'high', 'low']
  data = data.sort_values(by='date')
  data = data.reset_index(drop=True)
  data = data.loc[:, ['date']+ info_list]

  # 2割をテストデータへ
  split_pos = int(len(data)*0.8)
  x_train, y_train = prediction.load_data(
      data[info_list], prediction.length_of_sequences)
  x_test,  y_test = prediction.load_data(
      data[info_list].iloc[split_pos:], prediction.length_of_sequences)
  print(x_train.shape)
  prediction.create_model()#'bitflyer_weights_which_LSTM2.h5')
  plot_model(prediction.model, to_file='model.png', show_shapes=True, show_layer_names=True)
  res = prediction.model.fit(x_train, y_train, batch_size=10,
   nb_epoch=100, validation_split=0.2)#, callbacks=[EarlyStopping()])
  prediction.model.save_weights('bitflyer_weights_which_ooi.h5')
  predicted = prediction.model.predict(x_test)
  result = pandas.DataFrame(predicted)
  result.columns = ['predict']
  result['actual'] = y_test
  #print((numpy.array(result['actual'])-numpy.array(result['predict'])).mean(axis=0))
  result.plot()
  
  plot_history(res)
