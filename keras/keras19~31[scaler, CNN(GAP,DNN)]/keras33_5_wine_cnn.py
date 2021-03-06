from sklearn.preprocessing import MaxAbsScaler, RobustScaler, QuantileTransformer, PowerTransformer, StandardScaler, OneHotEncoder, MinMaxScaler
# 1. 로스와 R2로 평가
# MIN MAX와 스탠다드 결과들 명시
import pandas as pd
from tensorflow.keras.callbacks import EarlyStopping
from operator import mod
import numpy as np
from numpy.matrixlib.defmatrix import matrix
# import pandas as pd
from sklearn.datasets import load_iris
from icecream import ic
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, GlobalAveragePooling2D, MaxPool2D, Flatten
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import time
from tensorflow.python.keras.constraints import MinMaxNorm
from tensorflow.python.keras.layers.core import Dropout
from tensorflow.keras.utils import to_categorical

#1. 데이터
datasets = pd.read_csv('../_data/winequality-white.csv', sep=';',
                        index_col=None, header=0)

# print(datasets)
# print(datasets.shape) # (4898, 12)


datasets_np = datasets.to_numpy()
ic(datasets_np)
x = datasets_np[:,0:11]

y = datasets_np[:,[-1]]

# ic(x.shape, y.shape) # x.shape: (150, 4), y.shape: (150,)

ic(y)

one = OneHotEncoder()
one.fit(y)
y = one.transform(y).toarray()



x_train, x_test, y_train, y_test = train_test_split(x,y, train_size=0.8, random_state=60) # train 309, test 133


# scaler = QuantileTransformer()
# scaler = StandardScaler()
#scaler = PowerTransformer()
scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1, 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1, 1)


ic(y.shape, x.shape)
# ic(x_train.shape[0], x_test.shape[1])




# 2. 모델 구성
model = Sequential()
model.add(Conv2D(256, kernel_size=(2,2), padding='same', activation='relu', input_shape=(11,1,1)))  
model.add(Conv2D(128, (2,2), padding='same', activation='relu'))
model.add(Dropout(0.3))                                      
model.add(Conv2D(128, (2,2), padding='same', activation='relu')) 
model.add(Conv2D(64, (2,2), padding='same', activation='relu'))
model.add(Dropout(0.3))                        
model.add(Conv2D(64, (2,2), padding='same', activation='relu'))
model.add(Conv2D(32, (2,2), padding='same', activation='relu'))
model.add(GlobalAveragePooling2D())                                       
model.add(Dense(7, activation='softmax'))


#3. 컴파일, 훈련

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
es = EarlyStopping(monitor='acc', patience=10, mode='auto', verbose=1)
start = time.time()
model.fit(x_train, y_train, epochs=1000, verbose=1, validation_split=0.2, batch_size=16, shuffle=True, callbacks=[es])
걸린시간 = round((time.time() - start) /60,1)

#4. 평가, 예측
loss = model.evaluate(x_test, y_test)

y_predict = model.predict(x_test)
# ic(y_predict)

print('loss = ', loss[0])
print('accuracy = ', loss[1])

ic(f'{걸린시간}분')

'''
CNN + Conv1D + GAP

loss =  0.22041136026382446
accuracy =  0.9666666388511658
ic| f'{걸린시간}분': '0.2분'

CNN + Conv2D + GAP


RobustScaler
ic| 'loss:', loss[0]: 2.623243570327759
ic| 'accuracy', loss[1]: 0.7346938848495483

'''