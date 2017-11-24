import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pylab as plt
from sklearn import linear_model  # scikit-learnライブラリの関数を使用します
import seaborn as sns

data = pd.read_csv("bitflyer_BTCJPY.csv")
data.head()
data2 = np.array(data)

day_ago = 25  # 何日前までのデータを使用するのかを設定
num_sihyou = 1  # 終値

X = np.zeros((len(data2), day_ago * num_sihyou))

# 終値をfor文でday_ago日前まで一気に追加する
for i in range(0, day_ago):
  X[i:len(data2), i] = data2[0:len(data2) - i, 0]

Y = np.zeros(len(data2))
# 何日後を値段の差を予測するのか決めます
pre_day = 1
Y[0:len(Y) - pre_day] = X[pre_day:len(X), 0] - X[0:len(X) - pre_day, 0]

# 【重要】X, Yを正規化します
original_X = np.copy(X)  # コピーするときは、そのままイコールではダメ
tmp_mean = np.zeros(len(X))

for i in range(day_ago, len(X)):
  tmp_mean[i] = np.mean(original_X[i - day_ago + 1:i + 1, 0])  # 25日分の平均値
  for j in range(0, X.shape[1]):
    X[i, j] = (X[i, j] - tmp_mean[i])  # Xを正規化
  Y[i] = Y[i]  # X同士の引き算しているので、Yはそのまま
X_train = X[200:20000, :]  # 次のプログラムで200日平均を使うので、それ以降を学習データに使用します
Y_train = Y[200:20000]

X_test = X[20000:len(X) - pre_day, :]
Y_test = Y[20000:len(Y) - pre_day]

linear_reg_model = linear_model.LinearRegression()
linear_reg_model.fit(X_train, Y_train)  # モデルに対して、学習データをフィットさせ係数を学習させます

print("回帰式モデルの係数")
print(linear_reg_model.intercept_)
print(linear_reg_model.coef_)

Y_pred = linear_reg_model.predict(X_test)  # 予測する

result = pd.DataFrame(Y_pred)  # 予測
result.columns = ['Y_pred']
result['Y_test'] = Y_test

sns.set_style('darkgrid')
sns.regplot(x='Y_pred', y='Y_test', data=result)  # plotする


# 正答率を計算
success_num = 0
for i in range(len(Y_pred)):
    if Y_pred[i] * Y_test[i] >= 0:
        success_num += 1

print("予測日数：" + str(len(Y_pred)) + "、正答日数：" + str(success_num) +
      "正答率：" + str(success_num / len(Y_pred) * 100))
sum_2017 = 0

for i in range(0, len(Y_test)):  # len()で要素数を取得しています
    if Y_pred[i] >= 0:
        sum_2017 += Y_test[i]
    else:
        sum_2017 -= Y_test[i]

print("2017年の利益合計：%1.3lf" % sum_2017)


# 予測結果の総和グラフを描くーーーーーーーーー
total_return = np.zeros(len(Y_test))

if Y_pred[i] >= 0:  # 2017年の初日を格納
    total_return[0] = Y_test[i]
else:
    total_return[0] = -Y_test[i]

for i in range(1, len(result)):  # 2017年の2日以降を格納
    if Y_pred[i] >= 0:
        total_return[i] = total_return[i - 1] + Y_test[i]
    else:
        total_return[i] = total_return[i - 1] - Y_test[i]

#plt.plot(total_return)
