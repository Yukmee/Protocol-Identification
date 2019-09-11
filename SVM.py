import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
import pandas as pd
# import parse_pcap
from protocol_dict import protocol_dict

# parse_pcap.gen_csv()
dataset = pd.read_csv("./features_all_in_one.csv")
X = dataset.drop('label', axis=1)
X = np.nan_to_num(X)
y = dataset['label'].apply(lambda x: protocol_dict[x])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
svc = SVC(kernel='rbf', probability=True)
grid = GridSearchCV(SVC(), param_grid={"C": [1000, 10000, 100000], "gamma": [0.01, 0.001]}, cv=100)
grid.fit(X_train, y_train)
y_pred = grid.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print(df)
