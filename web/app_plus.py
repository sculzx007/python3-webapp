#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'lzx'

#针对上一个app.py，使用模版来进行改进

from flask import Flask, request, render_template
import jinja2

app = Flask(__name__)

#于flask框架是通过装饰器在内部自动把URL和函数关联起来
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']

    #需要从request对象读取表单的内容
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return render_template('signin-ok.html', username=username)
    return render_template('form.html', message = 'Bad username or password', username=username)

if __name__ == '__main__':
    app.run()