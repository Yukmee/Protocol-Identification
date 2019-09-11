import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from protocol_dict import protocol_dict
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# 导入数据
dataset = pd.read_csv("./features_all_in_one.csv")

# 将数据分为输入数据和输出结果
X = dataset.drop('label', axis=1)
X = np.nan_to_num(X)
y = dataset['label'].apply(lambda x: protocol_dict[x])
num_folds = 2000
seed = 7
kfold = KFold(n_splits=num_folds, random_state=seed)
num_tree = 100
max_features = 8
model = RandomForestClassifier(n_estimators=num_tree, random_state=seed, max_features=max_features)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(pd.DataFrame({'Actual': y_test, 'Pred': y_pred}))
