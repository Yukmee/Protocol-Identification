# from sklearn import datasets
# from sklearn import naive_bayes
# from sklearn import svm
#
# # Loading an example dataset
# iris = datasets.load_iris()
# digits = datasets.load_digits()
#
# # print(digits.data)
# # print(digits.target)
# # print(digits.images[0])
#
# # Learning and predicting
# clf = svm.SVC(gamma=0.001, C=100.)
# clf.fit(digits.data[:-1], digits.target[:-1])
#
# clf.predict(digits.data[-1:])

# Transforming target in regression
from sklearn.compose import TransformedTargetRegressor
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import QuantileTransformer

boston = load_boston()
X = boston.data
y = boston.target

regressor = LinearRegression()
transformer = QuantileTransformer(output_distribution='normal')
regr = TransformedTargetRegressor(regressor=regressor,
                                  transformer=transformer)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

regr.fit(X_train, y_train)
print('R2 score: {0:.2f}'.format(regr.score(X_test, y_test)))

raw_target_regr = LinearRegression().fit(X_train, y_train)
print('R2 score: {0:.2f}'.format(raw_target_regr.score(X_test, y_test)))

