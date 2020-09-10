from flask import Flask, render_template, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField, SubmitField, TextAreaField
from wtforms.validators import Required
import csv

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = '986v3n90d567cxn95n76vg74m'


class UploadForm(FlaskForm):
    file = FileField('Upload', validators=[FileRequired()])
    submit = SubmitField('Submit')


class TextForm(FlaskForm):
    content = TextAreaField('正文内容', validators=[Required()])
    signature = TextAreaField('邮件签名', validators=[Required()])
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
        flash('文件上传成功：' + file_name, category='success')
        return redirect(url_for('upload'))
    return render_template('upload.html', uploadform=form)


@app.route('/text/', methods=['GET', 'POST'])
def text():
    form = TextForm()
    if form.validate_on_submit():
        session['content'] = form.content
        session['signature'] = form.signature
        return redirect(url_for('text'))
    return render_template('text.html', textform=form, content=session.get('content'),
                           signature=session.get('signature'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=False)
