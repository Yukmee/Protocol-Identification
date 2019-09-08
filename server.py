import pickle

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', output=['a', 'b'])


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'./saved_pcaps/{secure_filename(f.filename)}')
        return render_template('index.html', test_var='文件成功上传!')


if __name__ == '__main__':
    app.run(debug=True)
