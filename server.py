import pickle

from sklearn.metrics import classification_report

import parse_pcap
import protocol_dict
from collections import Counter
from flask import Flask, render_template, request
from flask_table import Table, Col
from werkzeug.utils import secure_filename

from utils import find_key_by_value

app = Flask(__name__)

uploaded_pcap_file_name = ''


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
    # y_test = df['label'].apply(lambda x: protocol_dict[x])

    # Loading model to compare the results
    model = pickle.load(open('saved_model.pkl', 'rb'))
    y_pred = model.predict(x_test)
    # sth = [find_key_by_value(x) for x in y_pred]
    # # 使用 Counter() 来列出元素的频率
    # sth_new = dict(Counter(sth))
    # total_session = len(y_pred)
    #
    # # Declare my table
    # class ItemTable(Table):
    #     proto = Col('协议')
    #     possibility = Col('可能性')
    #
    # # Get some objects
    # class Item(object):
    #     def __init__(self, proto, possibility):
    #         self.proto = proto
    #         self.possibility = possibility
    #
    # items = [Item(x, sth_new[x] / total_session) for x in sth_new]
    #
    # # Populate the table
    # table = ItemTable(items)

    from utils import gen_classification_report_html, gen_proto_prediction_table_html
    # input_dict = classification_report(y_test, y_pred, output_dict=True)
    proto_prediction_table = gen_proto_prediction_table_html(y_pred)
    return render_template('index.html',
                           # file_name=uploaded_pcap_file_name,
                           # output=f'{sth_new}',
                           proto_prediction_table=proto_prediction_table,
                           # classification_report_table=gen_classification_report_html(input_dict)
                           )


if __name__ == '__main__':
    app.run(debug=True)
