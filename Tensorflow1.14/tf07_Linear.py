import tensorflow as tf
tf.set_random_seed(66)

x_train = [1,2,3]
y_train = [1,2,3]

W = tf.Variable(1, dtype=tf.float32) # 랜덤하게 내맘대로 넣어준 값
b = tf.Variable(1, dtype= tf.float32) # 초기값

hypothesis = x_train * W + b # 모델구현 / 훈련할때 예측한 y값
# f(x) = wx + b

loss = tf.reduce_mean(tf.square(hypothesis - y_train)) # mse
            # 평균        제곱      오차   => mse

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01) 
train = optimizer.minimize(loss) # loss의 최소값을 찾아줌

#### 그래프 형태로 만들어줌 출력하려면 sessrun에 넣어줘야함

sess = tf.Session()
sess.run(tf.global_variables_initializer()) # 출력하기전에 gvi 해줌

for step in range(2001): # -> 2000번 epochs
    sess.run(train)
    if step % 20 == 0: # 20번마다 출력 시킴
        print(step, sess.run(loss), sess.run(W), sess.run(b))