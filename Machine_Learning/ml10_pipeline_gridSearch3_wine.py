# 실습

# 모델: RandomForestClassifier

# 실습
# m07_1 최적의 파라미터 값을 가지고 model 구성 결과 도출

import numpy as np
from sklearn.datasets import load_wine
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
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, PowerTransformer, QuantileTransformer

### 머신러닝(evaluate -> score)

datasets = load_wine()


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

# parameter = [ {'n_jobs':[-1], 'n_estimators':[1, 10, 100],'max_depth':[6,8,10,12], 'min_samples_leaf':[8,12,18], 'min_samples_split':[8,16,20]},
#               {'n_jobs':[-1], 'n_estimators':[2, 30, 200],'max_depth':[10,16], 'min_samples_leaf':[10,14], 'min_samples_split':[4,10,30]},
#               {'n_jobs':[-1], 'n_estimators':[50, 80],'max_depth':[10, 12], 'min_samples_leaf':[12,18], 'min_samples_split':[16,20], 'criterion':['entropy', 'gini']}
# ]


md = 'RF__'
parameter = [ {f'{md}n_jobs':[-1], f'{md}n_estimators':[1, 10, 100], f'{md}max_depth':[6,8,10,12], f'{md}min_samples_leaf':[8,12,18], f'{md}min_samples_split':[8,16,20]},
              {f'{md}n_jobs':[-1], f'{md}n_estimators':[2, 30, 200],f'{md}max_depth':[10,16], f'{md}min_samples_leaf':[10,14], f'{md}min_samples_split':[4,10,30]},
              {f'{md}n_jobs':[-1], f'{md}n_estimators':[50, 80],f'{md}max_depth':[10, 12], f'{md}min_samples_leaf':[12,18], f'{md}min_samples_split':[16,20], f'{md}criterion':['entropy', 'gini']}
]
              
# n_estimators = epoch, n_jobs = cpu사용

# pipe = make_pipeline(MinMaxScaler(), RandomForestClassifier())

pipe = Pipeline([("scaler", MinMaxScaler()), ("RF", RandomForestClassifier())])

model = RandomizedSearchCV(pipe, parameter, cv=kfold, verbose=1) 

model.fit(x_train,y_train)

print('최적의 매개변수: ', model.best_estimator_) # cv를 통해 나온 값 / GridSearchCV를 통해서만 출력 가능
print("best_score: ", model.best_params_)
print("best_score: ", model.best_score_)


y_predict = model.predict(x_test)
acc= accuracy_score(y_test, y_predict)
ic(acc)

'''

Fitting 5 folds for each of 10 candidates, totalling 50 fits
최적의 매개변수:  Pipeline(steps=[('scaler', MinMaxScaler()),
                ('RF',
                 RandomForestClassifier(max_depth=8, min_samples_leaf=18,
                                        min_samples_split=8, n_estimators=10,
                                        n_jobs=-1))])
best_score:  {'RF__n_jobs': -1, 'RF__n_estimators': 10, 'RF__min_samples_split': 8, 'RF__min_samples_leaf': 18, 'RF__max_depth': 8}
best_score:  0.9507389162561577
ic| acc: 0.9444444444444444

Fitting 5 folds for each of 108 candidates, totalling 540 fits
최적의 매개변수:  Pipeline(steps=[('scaler', MinMaxScaler()),
                ('RF',
                 RandomForestClassifier(max_depth=6, min_samples_leaf=18,
                                        min_samples_split=16, n_estimators=10,
                                        n_jobs=-1))])
best_score:  {'RF__max_depth': 6, 'RF__min_samples_leaf': 18, 'RF__min_samples_split': 16, 'RF__n_estimators': 10, 'RF__n_jobs': -1}
best_score:  0.9716748768472907
ic| acc: 1.0
'''







