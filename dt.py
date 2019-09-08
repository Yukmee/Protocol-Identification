from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import metrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataset = pd.read_csv("./features_all_in_one.csv")
print(dataset.shape)
X = dataset.drop('label',axis=1)
y = dataset['label']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.05,random_state=0)
regressor = DecisionTreeRegressor()
regressor.fit(X_train, y_train)
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)
y_pred_a = classifier.predict(X_test)
y_pred = regressor.predict(X_test)
print(confusion_matrix(y_test, y_pred_a))
print(classification_report(y_test, y_pred_a))
df=pd.DataFrame({'Actual':y_test, 'Predicted':y_pred})
print(df)
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))