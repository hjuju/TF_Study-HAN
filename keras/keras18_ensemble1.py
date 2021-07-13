import numpy as np
from icecream import ic
from tensorflow.python.ops.gen_control_flow_ops import merge
x1 = np.array([range(100), range(301, 401), range(1, 101)])
x2 = np.array([range(101, 201), range(411, 511), range(100, 200)])
x1 = np.transpose(x1)
x2 = np.transpose(x2)
y = np.array(range(1001, 1101))


ic(x1.shape, x2.shape, y.shape) # ic| x1.shape: (100, 3), x2.shape: (100, 3), y1.shape: (100,)

from sklearn.model_selection import train_test_split
x1_train, x1_test, x2_train, x2_test, y_train, y_test = train_test_split(x1, x2, y, train_size=70, random_state=60)

#2. 모델 구성(앙상블 모델)

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input

#2-1 모델1
input1 = Input(shape=(3,))
dense1 = Dense(10, activation='relu', name='dense1')(input1)
dense2 = Dense(7, activation='relu', name='dense2')(dense1)
dense3 = Dense(5, activation='relu',name='dense3')(dense2)
output1 = Dense(11,name='output1')(dense3)

#2-2 모델2
input2 = Input(shape=(3,))
dense11 = Dense(10, activation='relu', name='dense11')(input2)
dense12 = Dense(10, activation='relu', name='dense12')(dense11)
dense13 = Dense(10, activation='relu', name='dense13')(dense12)
dense14 = Dense(10, activation='relu', name='dense14')(dense13)
output2 = Dense(12, name='output2')(dense14) # concatenate할 땐 1을 안줘도 됨

from tensorflow.keras.layers import concatenate, Concatenate

merge1 = concatenate([output1, output2]) # 첫번째 와 마지막 모델의 아웃풋을 병합 / merge도 layer
merge2 = Dense(10)(merge1)
merge3 = Dense(5, activation='relu')(merge2)
last_output = Dense(1)(merge3) # 마지막 layer 표현 방식(함수형 모델의 마지막 아웃풋 처럼 만들어주면 됨)

# 모델 연결
model = Model(inputs=[input1,input2],outputs=last_output) # 두개 이상 넣어주는 것이니 리스트 형태로



model.summary()

#3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
model.fit([x1_train, x2_train], y_train, epochs=100, batch_size=8, verbose=1)

#4. 평가, 예측
loss = model.evaluate([x1_test, x2_test], y_test)
ic(loss)
result = model.predict([x1_test, x2_test])
ic(result)
