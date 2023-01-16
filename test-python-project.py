
# %% Import packages

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import scipy as sp
import pandas as pd
import os
import flask
from flask import Flask, flash, request, session, redirect, url_for, jsonify, escape
from werkzeug.utils import secure_filename
import pathlib
from io import BytesIO
import base64
# from collections.abc import Sequence # Keeps throwing an error - seems to be associated with a change in Python 3.10+
# import tkinter as tk           # This would open a dialog to select a file but
# from tkinter import filedialog # it doesn't seem to work with the venv
# file_path = filedialog.askopenfilename()

# %% Start up API (I think...)
upload_dir = r'/tmp/data/uploads'
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

allowed_extensions = {'xls', 'xlsx', 'csv'}

app = flask.Flask(__name__)

app.secret_key = 'dummykey'

app.config['DEBUG'] = False
app.config['UPLOAD_FOLDER'] = upload_dir
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000 # 10 MB file limit

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('upload_file'))

@app.route('/files', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        filename = secure_filename(file.filename)
        session['filename'] = filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(filepath)
            return redirect(url_for('make_plot'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# session['my_var'] = 'my_value'
#     return redirect(url_for('b'))

@app.route('/plot', methods=['GET'])
def make_plot():
    if request.method == 'GET':
        # %% Import raw data
        data_dir = app.config["UPLOAD_FOLDER"]
        data_file = session.get('filename', None)
        # data_dir = r'/Users/briggssa/Repos/test-python-project/'
        # data_file = r'TestView_Data_1E-6_20221209.xlsx'
        data_type = pathlib.Path(data_file).suffix
        data_path = [data_dir, data_file]
        data_path = '/'.join(data_path)
        # data_path = data_dir
        # data_path += data_file
        if data_type == '.xlsx':
            data_name = data_file[0:-5]
            data = pd.read_excel(data_path)
        elif data_type == '.csv':
            data_name = data_file[0:-4]
            data = pd.read_csv(data_path)
        else:
            print('Invalid data type')
            stop()

        ## The following lines will plot the raw data
        # plt.plot(data.Stroke, data.Load)
        # plt.xlabel('Stroke (in)')
        # plt.ylabel('Load (lbs)')
        # plt.savefig('/Users/briggssa/Repos/test-python-project/true_data_raw.png')
        # plt.show()

        # %% Process raw data and plot processed data
        sample_area = 0.025 # in^2
        sample_gaugelength = 1.13 # in
        Strain = (data.Stroke - data.Stroke[0]) / sample_gaugelength
        Stress_psi = data.Load / sample_area
        Stress_MPa = Stress_psi * 0.00689476
        fig = plt.figure()
        plt.plot(Strain, Stress_MPa)
        plt.xlabel('Strain')
        plt.ylabel('Stress (MPa)')
        plt.title('Stress/Strain Plot for 316L in Molten FLiNaK at a Strain Rate of 1e-6 (in/in)/sec')
        plot_file_type = '.png'
        plot_out_path = [data_dir, '/', data_name, plot_file_type]
        # plot_out_path = [data_dir, '/', data_name]
        plot_out_path = ''.join(plot_out_path)
        # plot_out_path = data_dir # Will output plot in same directory with same name as input file
        # plot_out_path += data_name
        # plot_out_path += plot_file_type
        plt.grid(True)
        plt.savefig(plot_out_path)
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        # plt.show()
    return f"<img src='data:image/png;base64,{data}'/>"
    # return 'plotting finished'

app.run()