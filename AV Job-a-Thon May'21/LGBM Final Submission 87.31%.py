# -*- coding: utf-8 -*-
"""Job a thon submission 1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1986s_WnlvpWr6R2hZ7T9mhkFnn8JnbZb
"""

import numpy as np 
import pandas as pd

# Reading the Test and Train Dataset Provided to Us

test =  pd.read_csv('/content/test_mSzZ8RL.csv') 
train = pd.read_csv( '/content/train_s3TEQDk.csv')

# Separating the ID Columns from both the Test and Train Dataset

train_id=train['ID']
train=train.drop('ID', axis=1)
test_id=test['ID']
test=test.drop('ID', axis=1)

#Setting the Null Values to a random value that will be later used in the Label encoder

train['Credit_Product'][pd.isnull(train['Credit_Product'])] = "other"
test['Credit_Product'][pd.isnull(test['Credit_Product'])] = "other"

#Importing Label Encoder From SKLearn to encode the Strings value in to categorially encoded data

from sklearn.preprocessing  import LabelEncoder 

le = LabelEncoder()
var = ['Gender', 'Region_Code', 'Occupation', 'Channel_Code', 'Credit_Product', 'Is_Active']

for i in var:
  train[i] = le.fit_transform(train[i])
  test[i] = le.fit_transform(test[i])


#Redistributing the Prediction Column from the Train dataset in X and Y train


ytrain=train['Is_Lead'].values
xtrain=train.drop(['Is_Lead'], axis=1)

#forming a New Numpy array of the individual X and Y train


X = train.drop(['Is_Lead', 'Vintage', 'Avg_Account_Balance'], axis=1).values
y = train['Is_Lead'].values
X_test = test.drop(['Vintage', 'Avg_Account_Balance'], axis=1).values


from sklearn.preprocessing import MaxAbsScaler

transformer = MaxAbsScaler().fit(X)
X = transformer.transform(X)
X_test = transformer.transform(X_test)

#importing Stratified K fold and LightGBM for model Formation

from sklearn.model_selection import StratifiedKFold

import lightgbm as lgb

skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
params = {'n_estimators': 20000, 'n_jobs': -1, 'random_state': 2, 'learning_rate': 0.012564209621859385, 'colsample_bytree': 0.48762749309989595}

model = lgb.LGBMClassifier(**params)


#Training the model

predictions = np.zeros(test.shape[0])

for i, (train_id, valid_id) in enumerate(skf.split(xtrain,ytrain)):
    print("fold ", i)  
    X_train, y_train = X[train_id], y[train_id]
    X_valid, y_valid = X[valid_id], y[valid_id]
    model.fit(X_train, y_train, eval_set =[(X_valid, y_valid)],  early_stopping_rounds=200, verbose=1000, eval_metric='auc')

    predictions += model.predict_proba(X_test)[:,1]

#final prediction value is calculated 

finals = predictions/5


#Forming the final submission CSV File


df = pd.DataFrame()
df['ID']=test_id
df['Is_Lead']=finals
df.to_csv('file_name.csv', index=False)

