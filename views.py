from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField, SubmitField
import csv

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'


class UploadForm(FlaskForm):
    file = FileField('Upload', validators=[FileRequired()])
    submit = SubmitField('Submit')


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
    form = UploadForm()
    if form.validate_on_submit():
        file_name = form.file.data.filename
        file_path = 'uploads/' + file_name
        form.file.data.save(file_path)
        status = '文件上传成功: ' + file_name
        return render_template('upload.html', form=form, upload_status=status)
    return render_template('upload.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=False)
