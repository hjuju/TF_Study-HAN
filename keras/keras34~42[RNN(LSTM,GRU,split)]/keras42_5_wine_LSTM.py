from sklearn.preprocessing import MaxAbsScaler, RobustScaler, QuantileTransformer, PowerTransformer, StandardScaler, OneHotEncoder
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np
from sklearn.datasets import load_iris
from icecream import ic
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import time
from sklearn.metrics import r2_score
import pandas as pd



#1. 데이터
datasets = pd.read_csv('../_data/winequality-white.csv', sep=';', index_col=None, header=0 )

# ic(datasets)

x = datasets.iloc[:,0:11]
y = datasets.iloc[:,[-1]]

# ic(x, y)
# ic(x.shape, y.shape) 

ic(np.unique(y))

y = OneHotEncoder().fit_transform(y).toarray()


# ic(y)



x_train, x_test, y_train, y_test = train_test_split(x,y, train_size=0.7, random_state=60) # train 309, test 133

# scaler = QuantileTransformer()
# scaler = StandardScaler()
# scaler = PowerTransformer()
scaler = RobustScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)

ic(x_train.shape, x_test.shape)





model = Sequential()
model.add(LSTM(512, activation='relu', input_shape=(10,1)))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu'))
model.add(Dense(7, activation='softmax'))

model.summary()

#3. 컴파일, 훈련

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
es = EarlyStopping(monitor='acc', patience=20, mode='auto', verbose=1)
start = time.time()
model.fit(x_train, y_train, epochs=1000, verbose=1, validation_split=0.2, batch_size=32, shuffle=True, callbacks=[es])
걸린시간 = round((time.time() - start) /60,1)

#4. 평가, 예측

y_predict = model.predict(x_test)
loss = model.evaluate(x_test, y_test)
ic(loss[0])
ic(loss[1])
ic(f'{걸린시간}분')

'''
LSTM
ic| loss[0]: 3.4180045127868652
ic| loss[1]: 0.5802721381187439
ic| f'{걸린시간}분': '7.4분'

CNN + Conv1D + GAP

loss =  0.22041136026382446
accuracy =  0.9666666388511658
ic| f'{걸린시간}분': '0.2분'

CNN + Conv2D + GAP

RobustScaler
ic| 'loss:', loss[0]: 2.623243570327759
ic| 'accuracy', loss[1]: 0.7346938848495483
'''
