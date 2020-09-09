from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import csv

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    name = 'Test User'
    return render_template('index.html', name=name)


@app.route('/bnkdata/')
def bnkdata():
    output = []
    with open('bnkdata.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过第一行读取
        for row in reader:
            output.append(row)

    return render_template('bnkdata.html', data=output)


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if request.files:
            f = request.files['file']
            f.save('uploads/' + f.filename)
            status = '文件上传成功: ' + f.filename
            return render_template('upload.html', upload_status=status)
        status = '请选择上传文件'
        return render_template('upload.html', upload_status=status)
    return render_template('upload.html')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=False)
