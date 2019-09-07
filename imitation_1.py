import pandas as pd
from sklearn.linear_model import LinearRegression

dataset = pd.read_csv('features_all_in_one.csv')
X = dataset.iloc[:, 1:]
Y = dataset.iloc[:, :1]

_label_dict = {'vpn_icq_chat1a': 1, 'spotify2': 2, 'skype_file4': 3, 'scpDown4': 4, 'ICQchat1': 5, 'facebookchat1': 6,
               'gmailchat1': 7, 'icq_chat_3a': 8, 'email2b': 9, 'skype_file5': 10, 'icq_chat_3b': 11, 'skype_file1': 12,
               'facebook_chat_4a': 13, 'aim_chat_3a': 14, 'ICQchat2': 15, 'facebookchat2': 16, 'AIMchat2': 17,
               'aim_chat_3b': 18, 'vpn_icq_chat1b': 19, 'vpn_aim_chat1b': 20, 'facebookchat3': 21, 'vpn_email2a': 22,
               'email2a': 23, 'vpn_skype_chat1a': 24, 'AIMchat1': 25, 'scpUp3': 26, 'vpn_aim_chat1a': 27, 'scpUp5': 28}

''' 只用到了一次的函数，不妨注释掉
def gen_labels_dict():
    i = 0
    labels_set = set(list(Y['label']))
    labels_dict = dict()
    for label in labels_set:
        i += 1
        labels_dict[label] = i
    return labels_dict
'''

y = Y['label'].apply(lambda x: _label_dict[x])

# Fitting model with training data
regressor = LinearRegression()
regressor.fit(X, y)
regressor.predict([2211115158, 24411, 2211116036, 53, 17, 1, 0, 63])



