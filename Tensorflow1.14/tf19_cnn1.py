from keras import datasets
import tensorflow as tf
import numpy as np
from icecream import ic
from keras.models import Sequential
from keras.layers import Conv2D

tf.set_random_seed(66)

from keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

from keras.utils import to_categorical
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

x_train = x_train.reshape(60000, 28, 28, 1).astype('float32')/255
x_test = x_test.reshape(10000, 28, 28, 1).astype('float32')/255

from keras.optimizers import Adam

learning_rate = 0.001
training_epochs = 15
batch_size = 100
total_batch = int(len(x_train)/batch_size)

x = tf.placeholder(tf.float32, [None, 28, 28, 1])
y = tf.placeholder(tf.float32, [None, 10])

# 모델구성

w1 = tf.get_variable('w1', shape=[3, 3, 1, 32])
                                # [kernel_size(3,3), input(1), output(32)]
L1 = tf.nn.conv2d(x, w1, strides=[1, 1, 1, 1], padding='SAME')
                    # [1(차원맞춤), stride, 1(차원맞춤)]
# Variable과의 차이점: Vriable은 초기값을 반드시 지정해줘야한다(랜덤으로 넣어줬음-> random_normal) / 초기값이 자동으로 넣어짐, 하지만 네이밍설정과 shape설정 해줘야함

# model = Sequential()
# model.add(Conv2D(filters=32, kernel_size=(3,3), strides=1, input_shape=(28,28,1), padding='same'))

print(w1) # (3, 3, 1, 32)
print(L1) # ( ?, 28, 28, 32)



## get_variable ##
# sess = tf.Session()
# sess.run(tf.global_variables_initializer())
# ic(np.min(sess.run(w1)))
# ic(np.max(sess.run(w1)))
# ic(np.mean(sess.run(w1)))
# ic(np.median(sess.run(w1)))


# print(sess.run(w1))
# print(w1)