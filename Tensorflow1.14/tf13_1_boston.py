# 실습

from sklearn.datasets import load_boston
import tensorflow as tf
from sklearn.model_selection import train_test_split
tf.set_random_seed(66)

datasets = load_boston()
x_data = datasets.data
y_data = datasets.target

print(x_data.shape, y_data.shape) # (506, 13) (506,)

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, random_state=66, shuffle=True)

x = tf.compat.v1.placeholder(tf.float32, shape=[None, 13])
y = tf.compat.v1.placeholder(tf.float32, shape=[None, ])

w = tf.compat.v1.Variable(tf.random.normal([13,1], name='weight')) 
b = tf.compat.v1.Variable(tf.random.normal([1], name='bias'))

hypothesis = tf.matmul(x, w) + b # 출력되는 y값에 tf.sigmoid로 묶어서 0과1사이로 출력

# cost = -tf.reduce_mean(y*tf.log(hypothesis)+(1- y)*tf.log(1-hypothesis)) # binary_crossentropy 결과값이 -로 나와서 -붙여줘야함
cost = tf.reduce_mean(tf.square(hypothesis - y))

# optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.00001)
optimizer = tf.train.AdamOptimizer(learning_rate=0.000001) 
train = optimizer.minimize(cost)

sess = tf.compat.v1.Session()
sess.run(tf.global_variables_initializer())

from sklearn.metrics import r2_score
#3 훈련

for epochs in range(5001):
    _, cost_val, hy_val = sess.run([train, cost, hypothesis], 
              feed_dict={x:x_train, y:y_train})

    if epochs % 100 == 0:
        print(epochs, ", cost : ", cost_val, "\n", hy_val)


predicted = sess.run(hypothesis, feed_dict={x:x_test})
print("스코어 : ", r2_score(y_test, predicted))
print(y_data.shape)
print(hy_val.shape)

# 최종 결론값은 r2_score
