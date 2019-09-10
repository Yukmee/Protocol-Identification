import numpy
import pandas
from sklearn import datasets
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB, BernoulliNB

from protocol_dict import protocol_dict

import proc_csv

# dataset = pandas.read_csv("./features_all_in_one.csv")
# X = dataset.drop('label', axis=1)
# X = numpy.nan_to_num(X)
# # MARK: - 处理负数
# X = numpy.where(X > 0, X, 0)
# y = dataset['label'].apply(lambda x: protocol_dict[x])


X, y = proc_csv.process_csv('features_all_in_one')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
# nb = GaussianNB()  # 0.31
# nb = MultinomialNB()  # 0.16
nb = ComplementNB()  # 0.20
# nb = BernoulliNB()  # 0.21
nb.fit(X_train, y_train)

y_pred = nb.predict(X_test)
print(classification_report(y_test, y_pred))
print(accuracy_score(y_test, y_pred))
