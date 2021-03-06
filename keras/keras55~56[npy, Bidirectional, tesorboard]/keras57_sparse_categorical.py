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
model.add(Dense(10, activation='softmax')) # 이진분류로 출력

#3. 컴파일, 훈련 metrics=['acc']
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['acc'])
start = time.time()
es = EarlyStopping(monitor='loss', patience=5, mode='auto', verbose=1)
model.fit(x_train, y_train, epochs=1000, verbose=1, validation_split= 0.001, batch_size=128, callbacks=[es])
걸린시간 = round((time.time() - start) /60,1)

#4. 평가, 예측 predict 필요x acc로 판단

loss = model.evaluate(x_test, y_test)
ic('loss:', loss[0])
ic('accuracy', loss[1])
ic(f'{걸린시간}분')
# ic(loss)

'''
#############################################################################################
'sparse_catergorical_crossentropy'
분류모델 시 원핫 인코딩 후 카테고리컬 크로스엔트로피 했지만 위에있는 것 사용하면 원핫인코딩 안써도됨

#############################################################################################
'''


'''

ic| 'loss:', loss[0]: 0.02277880162000656
ic| 'accuracy', loss[1]: 0.9912999868392944

'''