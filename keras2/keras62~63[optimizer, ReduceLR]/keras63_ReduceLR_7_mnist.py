import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import datasets
from tensorflow.keras.datasets import mnist
from icecream import ic
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder, RobustScaler, QuantileTransformer, PowerTransformer
from tensorflow.keras.callbacks import EarlyStopping
import time


#1. 데이터
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# ic(x_train.shape, y_train.shape) # (60000, 28, 28) (60000,) 흑백데이터 명시x
# ic(x_test.shape, y_test.shape) # (10000, 28, 28) (10000,)


# 전처리


x_train = x_train.reshape(60000, 28, 28, 1).astype('float32')/255 # 3차원 -> 4차원  // 데이터의 내용과 순서가 바뀌면 안됨
x_test = x_test.reshape(10000, 28, 28, 1).astype('float32')/255

# ic(x_train.shape) # (60000, 28, 28, 1)
# ic(x_test.shape) # (10000, 28, 28, 1)

ic(np.unique(y_train)) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
one = OneHotEncoder()
y_train = y_train.reshape(-1,1)
y_test = y_test.reshape(-1,1)
ic(y_train.shape)            # (60000,1)
ic(y_test.shape) # (10000, 1)
one.fit(y_train)
y_train = one.transform(y_train).toarray()
y_test = one.transform(y_test).toarray()

#2. 모델
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten

model = Sequential()
model.add(Conv2D(64, kernel_size=(2,2), padding='same', input_shape=(28, 28, 1)))
model.add(Conv2D(32, (2,2), activation='relu'))
model.add(MaxPooling2D())               
model.add(Conv2D(32, (2,2), activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(16, (2,2), activation='relu'))
model.add(MaxPooling2D())                      
model.add(Conv2D(16, (2,2), activation='relu'))                                                        
model.add(Flatten())                                          
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='softmax')) 

#3. 컴파일, 훈련 metrics=['acc']
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

optimizer = Adam(lr=0.001) 

es = EarlyStopping(monitor='val_loss', patience=50, mode='auto', verbose=1)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', patience=5, mode='auto', verbose=1, factor=0.05) 

model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['acc'])
start = time.time()
model.fit(x_train, y_train, epochs=1000, verbose=1, validation_split= 0.1, batch_size=128, callbacks=[es])
걸린시간 = round((time.time() - start) /60,1)

#4. 평가, 예측 predict 필요x acc로 판단

loss = model.evaluate(x_test, y_test)
y_predict = model.predict(x_test)
ic(y_predict)
ic('loss:', loss[0])
ic('accuracy', loss[1])
ic(f'{걸린시간}분')
# ic(loss)


'''
ReduceLR
ic| 'loss:', loss[0]: 0.059333037585020065
ic| 'accuracy', loss[1]: 0.9861000180244446

ic| 'loss:', loss[0]: 0.02277880162000656
ic| 'accuracy', loss[1]: 0.9912999868392944

'''