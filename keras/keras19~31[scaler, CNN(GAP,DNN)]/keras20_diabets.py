# 1. 로스와 R2로 평가
# MIN MAX와 스탠다드 결과들 명시


from operator import mod
import numpy as np
from numpy.matrixlib.defmatrix import matrix
# import pandas as pd
from sklearn.datasets import load_diabetes
from icecream import ic
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import time


#1. 데이터
datasets = load_diabetes()

x = datasets.data
y = datasets.target

ic(x.shape, y.shape) # x.shape: (442, 10), y.shape: (442,)

# ic(datasets.feature_names)
# # ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']
# ic(datasets.DESCR)

# ic(y[:30]) # 30개 데이터 출력

# ic(np.min(y), np.max(y)) # 최소, 최대값 

x_train, x_test, y_train, y_test = train_test_split(x,y, train_size=0.7, random_state=60) # train 309, test 133


from sklearn.preprocessing import MinMaxScaler, StandardScaler
scaler = StandardScaler()
# scaler = MinMaxScaler()
scaler.fit(x_train) # xtrain에 대해서만 스케일러 해줌
x_train = scaler.transform(x_train) # 전체 데이터로 스케일링 하면 과적합이 될 수 있기때문에 나누어서 스케일링 해줌
x_test = scaler.transform(x_test) # 비율에 맞춰서 스케일링



#2. 모델 구성
model = Sequential()
model.add(Dense(400, input_shape=(10,), activation='relu'))
model.add(Dense(300, activation='relu'))
model.add(Dense(200, activation='relu'))
model.add(Dense(150, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(1))


#3. 컴파일, 훈련

model.compile(loss='mse', optimizer='adam', metrics=['mae'])
start = time.time()
model.fit(x_train, y_train, epochs=500, verbose=2, batch_size=8, validation_split=0.3, shuffle=True)
end = time.time() - start

#4. 평가, 예측
loss = model.evaluate(x_test, y_test)
ic(loss)

y_predict = model.predict(x_test)
# ic(y_predict)

r2 = r2_score(y_test, y_predict)
ic(r2)

ic(end)

'''
ic| r2: 0.5237891323534569
mse, R2

StandartScarler

model.add(Dense(400, input_shape=(10,), activation='relu'))
model.add(Dense(300, activation='relu'))
model.add(Dense(200, activation='relu'))
model.add(Dense(150, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(1))

ic| loss: [5613.01806640625, 58.31141662597656]
ic| r2: 0.08331197983861416
ic| end: 19.18168306350708
model.fit(x_train, y_train, epochs=500, verbose=2, batch_size=32, validation_split=0.3, shuffle=True)

ic| loss: [2994.5498046875, 43.93509292602539]
ic| r2: 0.5109460950812429
ic| end: 4.535871505737305
model.fit(x_train, y_train, epochs=100, verbose=2, batch_size=32, validation_split=0.3, shuffle=True)

'''

# 과제 1 0.62까지 올리기
