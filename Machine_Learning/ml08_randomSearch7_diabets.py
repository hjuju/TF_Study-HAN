# 실습

# 모델: RandomForestClassifier

# 실습
# m07_1 최적의 파라미터 값을 가지고 model 구성 결과 도출

import numpy as np
from sklearn.datasets import load_diabetes
from icecream import ic
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.svm import LinearSVC, SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression # 로지스틱회귀는 분류모델(회귀모델 X)
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import warnings
warnings.filterwarnings('ignore') # 경고무시
from sklearn.metrics import accuracy_score, r2_score

### 머신러닝(evaluate -> score)

datasets = load_diabetes()
print(datasets.DESCR)
print(datasets.feature_names)

# 1. 데이터
x = datasets.data
y = datasets.target
ic(x.shape, y.shape)  # (150, 4), (150,)->(150, 3)



from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV, RandomizedSearchCV

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, shuffle=True, random_state=66)




# 2. 모델(머신러닝에서는 정의만 해주면 됨)



# model = SVC()
# Acc:  [0.96666667 0.96666667 1.         0.93333333 0.96666667] 평균 Acc: 0.9667

# model = KNeighborsClassifier()
# Acc:  [0.96666667 0.96666667 1.         0.9        0.96666667] 평균 Acc: 0.96

# model = LogisticRegression()
# Acc:  [1.         0.96666667 1.         0.9        0.96666667] 평균 Acc: 0.9667

# model = DecisionTreeClassifier()
# Acc:  [0.96666667 0.96666667 1.         0.9        0.93333333] 평균 Acc: 0.9533

# model = RandomForestClassifier()
# Acc:  [0.96666667 0.93333333 1.         0.86666667 0.96666667] 평균 Acc: 0.9467

# model = LinearSVC()
# Acc:  [0.96666667 0.96666667 1.         0.9        1.        ] 평균 Acc: 0.9667

n_splits=5

kfold = KFold(n_splits=n_splits, shuffle=True, random_state=66)

parameter = [ {'n_jobs':[-1], 'n_estimators':[1, 10, 100],'max_depth':[6,8,10,12], 'min_samples_leaf':[8,12,18], 'min_samples_split':[8,16,20]},
              {'n_jobs':[-1], 'n_estimators':[50, 80],'max_depth':[10, 12], 'min_samples_leaf':[12,18], 'min_samples_split':[16,20], 'criterion':['mse', 'mae']},
              {'n_jobs':[-1], 'n_estimators':[100, 200, 300],'max_depth':[8,10,12,20], 'min_samples_leaf':[12,18,26], 'min_samples_split':[2, 8,16,20]}
] 
# n_estimators = epoch, n_jobs = cpu사용

model = RandomizedSearchCV(RandomForestRegressor(), parameter, cv=kfold, verbose=1) # 사용할 모델, parameter(정의), cv 명시 /  텐서플로로 하면 모델에 텐서플로 모델이 들어가면 됨
# model = SVC(C=1, kernel='linear')

model.fit(x_train,y_train)

print('최적의 매개변수: ', model.best_estimator_) # cv를 통해 나온 값 / GridSearchCV를 통해서만 출력 가능
print("best_score: ", model.best_score_)


y_predict = model.predict(x_test)
r2 = r2_score(y_test, y_predict)
ic(r2)
'''
print("정답률: ", accuracy_score(y_test, y_predict))
# 위아래 녀석들은 같은 녀석들
print("model.score: ", model.score(x_test, y_test))


최적의 매개변수:  RandomForestRegressor(max_depth=16, min_samples_leaf=10, min_samples_split=10,
                      n_estimators=30, n_jobs=-1)
best_score:  0.49395060656297823
ic| r2: 0.4101611305950771

최적의 매개변수:  RandomForestRegressor(max_depth=6, min_samples_leaf=8, min_samples_split=20,
                      n_estimators=10, n_jobs=-1)
best_score:  0.49378790729620164
ic| r2: 0.41246578067357176

Fitting 5 folds for each of 10 candidates, totalling 50 fits
최적의 매개변수:  RandomForestRegressor(max_depth=20, min_samples_leaf=12, min_samples_split=16,
                      n_estimators=200, n_jobs=-1)
best_score:  0.4833399078750384
ic| r2: 0.4248536244725669

'''







