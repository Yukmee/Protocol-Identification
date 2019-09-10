import numpy
import pandas

from protocol_dict import protocol_dict


def process_csv(filename):
    dataset = pandas.read_csv(f"./{filename}.csv")
    X = dataset.drop('label', axis=1)
    # X = X.fillna(X.mean())
    # print(f'!!!{np.where(np.isnan(X))}')
    X = numpy.nan_to_num(X)
    X = numpy.where(X > 0, X, 0)  # MARK: - 处理负数
    y = dataset['label'].apply(lambda x: protocol_dict[x])
    return X, y
