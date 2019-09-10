import numpy
import pandas
from sklearn import datasets
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

from protocol_dict import protocol_dict

dataset = pandas.read_csv("./features_all_in_one.csv")
X = dataset.drop('label', axis=1)
X = numpy.nan_to_num(X)
y = dataset['label'].apply(lambda x: protocol_dict[x])

# iris = datasets.load_iris()
#
# gnb = GaussianNB()
# y_pred = gnb.fit(iris.data, iris.target).predict(iris.data)
# print("Number of mislabeled points out of a total %d points : %d"
#       % (iris.data.shape[0], (iris.target != y_pred).sum()))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=0)
gnb = GaussianNB()
gnb.fit(X_train, y_train)

y_pred = gnb.predict(X_test)
print(classification_report(y_test, y_pred))
