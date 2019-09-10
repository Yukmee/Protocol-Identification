import pickle
from abc import ABC

import parse_pcap
import protocol_dict
from collections import Counter
from flask import Flask, render_template, request
from flask_table import Table, Col
from werkzeug.utils import secure_filename

app = Flask(__name__)

uploaded_pcap_file_name = ''


# Helper Methods
def find_key_by_value(x):
    for key in protocol_dict.protocol_dict.keys():
        if protocol_dict.protocol_dict[key] == x:
            return key


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    global uploaded_pcap_file_name
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'./saved_pcaps/{secure_filename(f.filename)}')
        uploaded_pcap_file_name = f.filename
        # uploaded_pcap_file_name = f.filename
        return render_template('index.html', test_var=f'{uploaded_pcap_file_name}文件成功上传!')


@app.route('/predict', methods=['GET'])
def predict():
    # 先将 pcap 变成 DataFrame
    df = parse_pcap.export_to_df(uploaded_pcap_file_name)
    x_test = df.drop('label', axis=1)

    # Loading model to compare the results
    model = pickle.load(open('saved_model.pkl', 'rb'))
    y_pred = model.predict(x_test)
    sth = [find_key_by_value(x) for x in y_pred]
    # 使用 Counter() 来列出元素的频率
    sth_new = dict(Counter(sth))
    total_session = len(y_pred)

    # Declare your table
    class ItemTable(Table):
        proto = Col('协议')
        possibility = Col('可能性')

    # Get some objects
    class Item(object):
        def __init__(self, proto, possibility):
            self.proto = proto
            self.possibility = possibility

    # items = [Item('Name1', 'Description1'),
    #          Item('Name2', 'Description2'),
    #          Item('Name3', 'Description3')]
    # Or, equivalently, some dicts
    items = [dict(proto='Name1', possibility='Description1'),
             dict(proto='Name2', possibility='Description2'),
             dict(proto='Name3', possibility='Description3')]

    items = [Item(x, sth_new[x] / total_session) for x in sth_new]

    # Populate the table
    table = ItemTable(items)

    # return render_template('index.html',
    #                        file_name=uploaded_pcap_file_name,
    #                        output=f'{sth_new}',
    #                        table=table
    #                        )

    return render_template('index.html',
                           table=table
                           )


if __name__ == '__main__':
    app.run(debug=True)
