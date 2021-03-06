from tensorflow.keras.datasets import cifar10 # 칼라 데이터 (32,32,3)
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import datasets
from icecream import ic

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

ic(x_train.shape, y_train.shape) 
ic(x_test.shape, y_test.shape) 

ic(x_train[0])
ic(y_train[0])

plt.imshow(x_train[1])
plt.show()