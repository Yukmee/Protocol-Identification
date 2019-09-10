from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import metrics

import proc_csv
from protocol_dict import protocol_dict
import pandas as pd
import numpy as np
import pickle
import parse_pcap

# 生成新的 cvs 文件, 如果有必要
# parse_pcap.gen_csv()

X, y = proc_csv.process_csv('features_all_in_one')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.23, random_state=0)
regressor = DecisionTreeRegressor()
regressor.fit(X_train, y_train)  # MARK: 解决了'ValueError: Input contains NaN... too large for dtype('float32').'
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)
y_pred_a = classifier.predict(X_test)
y_pred = regressor.predict(X_test)

# Save model to disk
pickle.dump(regressor, open('saved_model.pkl', 'wb'))

# Loading model to compare the results
model = pickle.load(open('saved_model.pkl', 'rb'))
model_y_pred = model.predict(X_test)

# Print predictions from saved model.
df = pd.DataFrame({'Actual': y_test, 'Predicted': model_y_pred})
print(df)
print(classification_report(y_test, model_y_pred))
