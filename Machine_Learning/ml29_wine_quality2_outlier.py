import numpy as np
import pandas as pd
from scipy.sparse import data
from sklearn import datasets
from sklearn.datasets import load_wine
from icecream import ic
from xgboost import XGBClassifier

aaa = np.array([[1,2,10000,3,4,6,7,8,90,100,5000],
                [1000,2000,3,4000,5000,6000,7000,8,9000,10000,1001]])
                
#1. 데이터
datasets = pd.read_csv('../_data/wine/winequality-white.csv', index_col=None, header=0, sep=';')

# ic(datasets.head())

# ic(datasets.shape) # (4898, 12)
# ic(datasets.describe())

datasets = datasets.values
# ic(datasets)

x = datasets[:,:11]
y = datasets[:,11]

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x,y, train_size=0.8, shuffle=True, random_state=66)

def outlier(data_out):
    lis = []
    for i in range(data_out.shape[1]):
        quartile_1, q2, quartile_3 = np.percentile(data_out[:, i], [25, 50, 75])
        print("Q1 : ", quartile_1)
        print("Q2 : ", q2)
        print("Q3 : ", quartile_3)
        iqr = quartile_3 - quartile_1
        print("IQR : ", iqr)
        lower_bound = quartile_1 - (iqr * 1.5)
        upper_bound = quartile_3 + (iqr * 1.5)
        print('lower_bound: ', lower_bound)
        print('upper_bound: ', upper_bound)

        m = np.where((data_out[:, i]>upper_bound) | (data_out[:, i]<lower_bound))
        n = np.count_nonzero((data_out[:, i]>upper_bound) | (data_out[:, i]<lower_bound))
        lis.append([i+1,'columns', m, 'outlier_num :', n])

    return np.array(lis)

outliers_loc = outlier(aaa)
print("outlier at :", outliers_loc) 



# scaler = StandardScaler()
# x_train = scaler.fit_transform(x_train)
# x_test = scaler.transform(x_test)

#2. 모델
# model = XGBClassifier(n_jobs=-1)

# model.fit(x_train, y_train)

# score = model.score(x_test, y_test)

# print('acc: ', score) 

# # acc:  0.6816326530612244