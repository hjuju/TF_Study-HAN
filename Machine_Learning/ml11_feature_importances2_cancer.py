from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
datasets = load_breast_cancer()

# 1. 데이터

x = datasets.data
y = datasets.target

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, shuffle=True, random_state=66)

#2. 모델
# model = DecisionTreeClassifier(max_depth=3)
# model = RandomForestClassifier()
# model = GradientBoostingClassifier()
model = XGBClassifier()
# 수치보고 어떤것이 더 괜찮은지 확인

#3. 훈련
model.fit(x_train, y_train)

#4. 평가, 예측
acc = model.score(x_test, y_test)
print('acc:', acc)

print(model.feature_importances_)

import matplotlib.pyplot as plt
import numpy as np

def plot_feature_importance_dataset(model): 
    n_feature = datasets.data.shape[1]
    plt.barh(np.arange(n_feature), model.feature_importances_, align='center')
    plt.yticks(np.arange(n_feature), datasets.feature_names)
    plt.xlabel("feature Importances")
    plt.ylabel("features")
    plt.ylim(-1, n_feature)

plot_feature_importance_dataset(model)
plt.show()


'''
Randomforest
acc: 0.9707602339181286
[0.04350061 0.017755   0.04002309 0.07472769 0.00471458 0.00422661
 0.03655759 0.08434649 0.00426325 0.00361065 0.02795009 0.00603968
 0.00557691 0.05293222 0.0033239  0.00412285 0.00639897 0.0045418
 0.0026363  0.00650061 0.10209429 0.0153486  0.1910064  0.10667007
 0.00887877 0.00781246 0.02794611 0.08632617 0.01191361 0.00825462]

DecisionTreeClassifier
 acc: 0.9415204678362573
[0.         0.03031902 0.         0.         0.         0.
 0.         0.         0.         0.01588139 0.         0.
 0.         0.         0.         0.         0.         0.
 0.         0.         0.         0.01965322 0.         0.81972968
 0.         0.         0.         0.1144167  0.         0.        ]

'''