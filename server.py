import pickle
import parse_pcap
import protocol_dict
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

uploaded_pcap_file_name = ''


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
    # 按出现频率排序
    y_pred.sort()
    sth = [find_key_by_value(x) for x in y_pred]

    return render_template('index.html',
                           file_name=uploaded_pcap_file_name,
                           output=f'{sth}')


if __name__ == '__main__':
    app.run(debug=True)
