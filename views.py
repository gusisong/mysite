from flask import Flask, render_template, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms.validators import DataRequired
from wtforms import FileField, SubmitField, TextAreaField
from flask_sqlalchemy import SQLAlchemy
import os
import csv

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = '986v3n90d567cxn95n76vg74m'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class UploadForm(FlaskForm):
    file = FileField('Upload', validators=[FileRequired()])
    submit = SubmitField('Submit')


class TextForm(FlaskForm):
    content = TextAreaField('正文内容', validators=[DataRequired()])
    signature = TextAreaField('邮件签名', validators=[DataRequired()])
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
