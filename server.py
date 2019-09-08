import pickle
import parse_pcap
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

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
    # Loading model to compare the results
    model = pickle.load(open('saved_model.pkl', 'rb'))

    # TODO: - Implement this!!!
    # 先将 pcap 变成 DataFrame
    df = parse_pcap.export_to_df(uploaded_pcap_file_name)
    print(df)
    # model_y_pred = model.predict(X_test)

    return render_template('index.html', output='...')


if __name__ == '__main__':
    app.run(debug=True)
