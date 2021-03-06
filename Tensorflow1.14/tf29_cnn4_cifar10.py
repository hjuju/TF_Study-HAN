# from keras import datasets
# import tensorflow as tf
# import numpy as np
# from icecream import ic
# from keras.models import Sequential
# from keras.layers import Conv2D, MaxPool2D, Flatten
# from tensorflow.python.ops.variables import global_variables_initializer

# tf.set_random_seed(66)

# from keras.datasets import cifar10

# (x_train, y_train), (x_test, y_test) = cifar10.load_data()

# from keras.utils import to_categorical
# y_train = to_categorical(y_train)
# y_test = to_categorical(y_test)

# x_train = x_train.reshape(50000, 32, 32, 3).astype('float32')/255
# x_test = x_test.reshape(10000, 32, 32, 3).astype('float32')/255

# from keras.optimizers import Adam

# learning_rate = 0.0001
# training_epochs = 15
# batch_size = 100
# total_batch = int(len(x_train)/batch_size)

# x = tf.placeholder(tf.float32, [None, 32, 32, 3])
# y = tf.placeholder(tf.float32, [None, 10])

# # 모델구성

# # layer 1
# w1 = tf.get_variable('w1', shape=[2, 2, 3, 32])
#                                 # [kernel_size(3,3), input(1), output(32)]
# L1 = tf.nn.conv2d(x, w1, strides=[1, 1, 1, 1], padding='SAME')
#                     # [1(차원맞춤), stride, 1(차원맞춤)]
# L1 = tf.nn.relu(L1) # activation 
# L1_maxpool = tf.nn.max_pool(L1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME') 

# # Variable과의 차이점: Vriable은 초기값을 반드시 지정해줘야한다(랜덤으로 넣어줬음-> random_normal) / 초기값이 자동으로 넣어짐, 하지만 네이밍설정과 shape설정 해줘야함

# # model = Sequential()
# # model.add(Conv2D(filters=32, kernel_size=(3,3), strides=1, input_shape=(28,28,1), padding='same'))
# # model.add(MaxPool2D)

# ic(w1)         # (3, 3, 1, 32)
# ic(L1)         # ( ?, 28, 28, 32)
# ic(L1_maxpool) # (?, 14, 14, 32)

# # layer 2
# w2 = tf.get_variable('w2', shape=[2, 2, 32, 64])
# L2 = tf.nn.conv2d(L1_maxpool, w2, strides=[1,1,1,1], padding='SAME')
# L2 = tf.nn.relu(L2)
# L2_maxpool = tf.nn.max_pool(L2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# ic(L2)          # (?, 14, 14, 64)
# ic(L2_maxpool)  # (?, 7, 7, 64)

# # layer 3
# w3 = tf.get_variable('w3', shape=[2, 2, 64, 128])
# L3 = tf.nn.conv2d(L2_maxpool, w3, strides=[1,1,1,1], padding='SAME')
# L3 = tf.nn.relu(L3)
# L3_maxpool = tf.nn.max_pool(L3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# ic(L3)          # (?, 7, 7, 128)
# ic(L3_maxpool)  # (?, 4, 4, 128)

# # layer 4
# w4 = tf.get_variable('w4', shape=[2, 2, 128, 64], initializer=tf.contrib.layers.xavier_initializer())
# L4 = tf.nn.conv2d(L3_maxpool, w4, strides=[1,1,1,1], padding='VALID')
# L4 = tf.nn.relu(L4)
# L4_maxpool = tf.nn.max_pool(L4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# ic(L4)          # (?, 4, 4, 64)
# ic(L4_maxpool)  # (?, 2, 2, 64)

# # Flatten
# L_flat = tf.reshape(L4_maxpool, [-1, 2*2*64])
# ic(L_flat) # (?, 256)

# # layer5 DNN
# w5 = tf.get_variable('w5', shape=[2*2*64, 64])
# b5 = tf.Variable(tf.random_normal([64]), name='b1')
# L5 = tf.matmul(L_flat, w5) + b5
# L5 = tf.nn.relu(L5)
# L5 = tf.nn.dropout(L5, keep_prob=0.2)
# ic(L5) # (?, 64)

# # layer6 DNN
# w6 = tf.get_variable('w6', shape=[64, 32])
# b6 = tf.Variable(tf.random_normal([32]), name='b2')
# L6 = tf.matmul(L5, w6) + b6
# L6 = tf.nn.relu(L6)
# L6 = tf.nn.dropout(L6, keep_prob=0.2)
# ic(L6) # (?, 32)

# # layer7 softmax

# w7 = tf.get_variable('w7', shape=[32, 10])
# b7 = tf.Variable(tf.random_normal([10]), name='b3')
# L7 = tf.matmul(L6, w7) + b7
# hypothesis = tf.nn.softmax(L7)
# ic(hypothesis) # (?, 32)

# loss = tf.reduce_mean(-tf.reduce_sum(y * tf.log(hypothesis), axis=1))

# optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

# sess = tf.Session()
# sess.run(global_variables_initializer())

# for epochs in range(training_epochs):
#     avg_loss = 0

#     for i in range(total_batch): # 1.../600번 훈련 -> len(여기서는 60,000)/배치사이즈(여기서는 100) 으로 계산
#         start = i * batch_size
#         end = start + batch_size
#         batch_x, batch_y = x_train[start:end], y_train[start:end]

#         feed_dict = {x:batch_x, y: batch_y}

#         batch_loss, _ = sess.run([loss, optimizer], feed_dict=feed_dict)

#         avg_loss += batch_loss/total_batch # 600번씩 15번 돌아감

#     print('Epoch: ', '%04d' %(epochs + 1), 'loss: {:.9f}'.format(avg_loss)) # epoch당 출력값을 뽑아줌

# print("훈련 종료")

# pred = tf.equal(tf.argmax(hypothesis, 1) , tf.argmax(y,1)) # 10개의 softmax 출력물

# acc = tf.reduce_mean(tf.cast(pred, tf.float32))
# print('ACC: ', sess.run(acc, feed_dict={x:x_test, y:y_test}))










import tensorflow as tf
import numpy as np
from icecream import ic
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten
from tensorflow.python.ops.variables import global_variables_initializer

tf.set_random_seed(66)

from keras.datasets import cifar10

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

ic(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

from keras.utils import to_categorical
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

x_train = x_train.reshape(50000, 32, 32, 3).astype('float32')/255
x_test = x_test.reshape(10000, 32, 32, 3).astype('float32')/255

from keras.optimizers import Adam

learning_rate = 0.0001
training_epochs = 3
batch_size = 100
total_batch = int(len(x_train)/batch_size)

x = tf.placeholder(tf.float32, [None, 32, 32, 3])
y = tf.placeholder(tf.float32, [None, 10])

# 모델구성

# layer 1
w1 = tf.get_variable('w1', shape=[2, 2, 3, 1024])
                                # [kernel_size(3,3), input(1), output(32)]
L1 = tf.nn.conv2d(x, w1, strides=[1, 1, 1, 1], padding='SAME')
                    # [1(차원맞춤), stride, 1(차원맞춤)]
L1 = tf.nn.relu(L1) # activation 
L1_maxpool = tf.nn.max_pool(L1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME') 

# Variable과의 차이점: Vriable은 초기값을 반드시 지정해줘야한다(랜덤으로 넣어줬음-> random_normal) / 초기값이 자동으로 넣어짐, 하지만 네이밍설정과 shape설정 해줘야함

# model = Sequential()
# model.add(Conv2D(filters=32, kernel_size=(3,3), strides=1, input_shape=(28,28,1), padding='same'))
# model.add(MaxPool2D)

ic(w1)         # (3, 3, 1, 32)
ic(L1)         # ( ?, 28, 28, 32)
ic(L1_maxpool) # (?, 14, 14, 32)

# layer 2
w2 = tf.get_variable('w2', shape=[2, 2, 1024, 512])
L2 = tf.nn.conv2d(L1_maxpool, w2, strides=[1,1,1,1], padding='SAME')
L2 = tf.nn.relu(L2)
L2_maxpool = tf.nn.max_pool(L2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

ic(L2)          # (?, 14, 14, 64)
ic(L2_maxpool)  # (?, 7, 7, 64)

# layer 3
w3 = tf.get_variable('w3', shape=[2, 2, 512, 256])
L3 = tf.nn.conv2d(L2_maxpool, w3, strides=[1,1,1,1], padding='SAME')
L3 = tf.nn.relu(L3)
L3_maxpool = tf.nn.max_pool(L3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

ic(L3)          # (?, 7, 7, 128)
ic(L3_maxpool)  # (?, 4, 4, 128)

# layer 4
w4 = tf.get_variable('w4', shape=[2, 2, 256, 128], initializer=tf.contrib.layers.xavier_initializer())
L4 = tf.nn.conv2d(L3_maxpool, w4, strides=[1,1,1,1], padding='SAME')
L4 = tf.nn.relu(L4)
L4_maxpool = tf.nn.max_pool(L4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

ic(L4)          # (?, 4, 4, 64)
ic(L4_maxpool)  # (?, 2, 2, 64)

# layer 5
w5 = tf.get_variable('w5', shape=[2, 2, 128, 64], initializer=tf.contrib.layers.xavier_initializer())
L5 = tf.nn.conv2d(L4_maxpool, w5, strides=[1,1,1,1], padding='SAME')
L5 = tf.nn.relu(L5)
L5_maxpool = tf.nn.max_pool(L5, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

ic(L5)          # (?, 4, 4, 64)
ic(L5_maxpool)  # (?, 2, 2, 64)

# Flatten
L_flat = tf.reshape(L5_maxpool, [-1, 2*2*64])
ic(L_flat) # (?, 256)

# layer6 DNN
w6 = tf.get_variable('w6', shape=[2*2*64, 64])
b6 = tf.Variable(tf.random_normal([64]), name='b1')
L6 = tf.matmul(L_flat, w6) + b6
L6 = tf.nn.relu(L6)
L6 = tf.nn.dropout(L6, keep_prob=0.2)
ic(L6) # (?, 64)

# layer7 DNN
w7 = tf.get_variable('w7', shape=[64, 32])
b7 = tf.Variable(tf.random_normal([32]), name='b2')
L7 = tf.matmul(L6, w7) + b7
L7 = tf.nn.relu(L7)
L7= tf.nn.dropout(L7, keep_prob=0.2)
ic(L7) # (?, 32)

# layer8 softmax

w8 = tf.get_variable('w8', shape=[32, 10])
b8 = tf.Variable(tf.random_normal([10]), name='b3')
L8 = tf.matmul(L7, w8) + b8
hypothesis = tf.nn.softmax(L8)
ic(hypothesis) # (?, 32)

loss = tf.reduce_mean(-tf.reduce_sum(y * tf.math.log(hypothesis), axis=1))

optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

sess = tf.Session()
sess.run(global_variables_initializer())

for epochs in range(training_epochs):
    avg_loss = 0

    for i in range(total_batch): # 1.../600번 훈련 -> len(여기서는 60,000)/배치사이즈(여기서는 100) 으로 계산
        start = i * batch_size
        end = start + batch_size
        batch_x, batch_y = x_train[start:end], y_train[start:end]

        feed_dict = {x:batch_x, y: batch_y}

        batch_loss, _ = sess.run([loss, optimizer], feed_dict=feed_dict)

        avg_loss += batch_loss/total_batch # 600번씩 15번 돌아감

    print('Epoch: ', '%04d' %(epochs + 1), 'loss: {:.9f}'.format(avg_loss)) # epoch당 출력값을 뽑아줌

print("훈련 종료")

pred = tf.equal(tf.argmax(hypothesis, 1) , tf.argmax(y,1)) # 10개의 softmax 출력물

acc = tf.reduce_mean(tf.cast(pred, tf.float32))
print('ACC: ', sess.run(acc, feed_dict={x:x_test, y:y_test}))

# 0.7 이상
