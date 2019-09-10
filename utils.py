# 将字典变成表格的 html
# {'1': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 0}, '2': {'precision': 0.0,
# 'recall': 0.0, 'f1-score': 0.0, 'support': 15}, '3': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support':
# 7}, '4': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 7}, '5': {'precision': 0.0, 'recall': 0.0,
# 'f1-score': 0.0, 'support': 14}, '6': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 20},
# '7': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 39}, '8': {'precision': 0.0, 'recall': 0.0,
# 'f1-score': 0.0, 'support': 22}, '9': {'precision': 0.5462962962962963, 'recall': 0.5412844036697247, 'f1-score':
# 0.543778801843318, 'support': 109}, '10': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 9},
# '11': {'precision': 0.40358744394618834, 'recall': 0.9574468085106383, 'f1-score': 0.5678233438485805, 'support':
# 94}, '12': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 16}, '13': {'precision': 0.0,
# 'recall': 0.0, 'f1-score': 0.0, 'support': 24}, '14': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0,
# 'support': 14}, '15': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 14}, '16': {'precision': 0.0,
# 'recall': 0.0, 'f1-score': 0.0, 'support': 12}, '17': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0,
# 'support': 6}, '18': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 105}, '19': {'precision': 0.0,
# 'recall': 0.0, 'f1-score': 0.0, 'support': 1}, '20': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support':
# 1}, '21': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 36}, '23': {'precision':
# 0.3045977011494253, 'recall': 0.5196078431372549, 'f1-score': 0.3840579710144928, 'support': 102},
# '25': {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 9}, '26': {'precision': 0.06206896551724138,
# 'recall': 1.0, 'f1-score': 0.1168831168831169, 'support': 9}, '27': {'precision': 0.0, 'recall': 0.0, 'f1-score':
# 0.0, 'support': 1}, '28': {'precision': 0.058823529411764705, 'recall': 0.1111111111111111, 'f1-score':
# 0.07692307692307691, 'support': 9}, 'accuracy': 0.30503597122302156, 'macro avg': {'precision':
# 0.05289899755080447, 'recall': 0.12036346793956651, 'f1-score': 0.06497947348125327, 'support': 695},
# 'weighted avg': {'precision': 0.18653311366739633, 'recall': 0.30503597122302156, 'f1-score': 0.2209574856265068,
# 'support': 695}}
from collections import Counter

from flask_table import Table, Col

from protocol_dict import protocol_dict


def gen_classification_report_html(input_dict):
    # Declare my table
    class ItemTable(Table):
        proto = Col('协议')
        precision = Col('Precision/精确率')
        recall = Col('Recall/召回率')
        f1_score = Col('F1-分数')
        support = Col('Support/支持度')

    # Get some objects
    class Item(object):
        def __init__(self, proto, precision, recall, f1_score, support):
            self.proto = find_key_by_value(proto)
            self.precision = precision
            self.recall = recall
            self.f1_score = f1_score
            self.support = support

    items = input_dict

    # Populate the table
    rendered_html = ItemTable(items)
    return rendered_html


def gen_proto_prediction_table_html(y_pred):
    sth = [find_key_by_value(x) for x in y_pred]
    # 使用 Counter() 来列出元素的频率
    sth_new = dict(Counter(sth))
    total_session = len(y_pred)

    # Declare my table
    class ItemTable(Table):
        proto = Col('协议')
        possibility = Col('可能性')

    # Get some objects
    class Item(object):
        def __init__(self, proto, possibility):
            self.proto = proto
            self.possibility = possibility

    items = [Item(x, sth_new[x] / total_session) for x in sth_new]

    # Populate the table
    table = ItemTable(items)
    return table


# Helper Methods
def find_key_by_value(x):
    for key in protocol_dict.keys():
        if protocol_dict[key] == x:
            return key
