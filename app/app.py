#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, url_for, render_template, request, redirect, jsonify, send_from_directory
import dazai
import os
import inspect
import time
import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
import json
import datetime


app = Flask(__name__)

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
)

app.logger.setLevel(logging.INFO)

debug_log = os.path.join(app.root_path, 'logs/debug.log')

debug_file_handler = RotatingFileHandler(
    debug_log, maxBytes=100000, backupCount=10
)

debug_file_handler.setLevel(logging.INFO)
debug_file_handler.setFormatter(formatter)
app.logger.addHandler(debug_file_handler)

error_log = os.path.join(app.root_path, 'logs/error.log')
error_file_handler = RotatingFileHandler(
    error_log, maxBytes=100000, backupCount=10
)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)
app.logger.addHandler(error_file_handler)

@app.route('/')
def root():
    return redirect(url_for('start'))

@app.route('/dazai/')
def start():
    return redirect(url_for('markdown'))

@app.route('/dazai/md/', methods=['GET', 'POST'])
def markdown():
    
    if request.method == 'GET':
        return render_template('index.html', text="GETされたよ！")

    if request.method == 'POST':
        contents = json.loads(request.data.decode('utf-8'))
        print(contents)
        try:
            d = datetime.datetime.today()
            pdf_path = dazai.make_book(
            {  
              "booktitle": contents['booktitle'],
              "aut": contents['aut'],
              "prt": contents['prt'],
              "pbl": contents['pbl'],
              "contact": contents['contact'],
              "prt_url":  contents['prt_url'],
              "rights": d.strftime("(C) %Y " + contents['rights']),
              "date": d.strftime("%Y年%m月%d日"),
              "pubhistory": d.strftime("%Y年%m月%d日 v1.0.0版発行")
              },
              contents['preface'],
              [contents['markdown']]
            )
        # pdf_path = "book.pdf"
        
        except:
            response = jsonify({'results':{'pdf_filename': None}})
            response.status_code = 500
            return response

        response = jsonify({'results':{'pdf_filename': pdf_path}})
        response.status_code = 201
        return response

    else:
        return render_template('index.html', text="", is_error=True)

if __name__ == '__main__':
    app.run(debug=True)
