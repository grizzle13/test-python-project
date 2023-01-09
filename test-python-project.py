# %% Import packages

import os
import pathlib

import flask
import matplotlib.pyplot as plt
import pandas as pd
from flask import flash, redirect, request
from werkzeug.utils import secure_filename

# from collections.abc import Sequence # Keeps throwing an error - seems to be associated with a change in Python 3.10+
# import tkinter as tk           # This would open a dialog to select a file but
# from tkinter import filedialog # it doesn't seem to work with the venv
# file_path = filedialog.askopenfilename()

# %% Start up API (I think...)
upload_dir = "/tmp/data/uploads"
allowed_extensions = {"xls", "xlsx", "csv"}

app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config["UPLOAD_FOLDER"] = upload_dir
app.config["MAX_CONTENT_LENGTH"] = 10 * 1000 * 1000  # 10 MB file limit


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


@app.route("/files", methods=["GET"])
def upload_handler():
    with open("/tmp/data/uploads/data.json", "r") as f:
        return f.read()


@app.route("/files/new", methods=["POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(filepath)
            return "uploaded"
            # return redirect(url_for('download_file', name=filename))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """


@app.route("/simulate", methods=["POST"])
def simulate():
    # do your fancy nuclear stuff here
    # pass in a filename as input, go look on local disk for a match, and then use the corresponding data
    filename = request.json["filename"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    data = pd.read_excel(filepath)

    return data.to_json(orient="records")
    # data_dir = r"/Users/briggssa/Repos/test-python-project/"
    # data_file = r"TestView_Data_1E-6_20221209.xlsx"
    # data_type = pathlib.Path(data_file).suffix
    # data_path = data_dir
    # data_path += data_file
    # if data_type == ".xlsx":
    #     data_name = data_file[0:-5]
    #     data = pd.read_excel(data_path)
    # elif data_type == ".csv":
    #     data_name = data_file[0:-4]
    #     data = pd.read_csv(data_path)
    # else:
    #     print("Invalid data type")
    #     stop()
    #
    # sample_area = 0.025  # in^2
    # sample_gaugelength = 1.13  # in
    # Strain = (data.Stroke - data.Stroke[0]) / sample_gaugelength
    # Stress_psi = data.Load / sample_area
    # Stress_MPa = Stress_psi * 0.00689476
    # plt.plot(Strain, Stress_MPa)
    # plt.xlabel("Strain")
    # plt.ylabel("Stress (MPa)")
    # plt.title(
    #     "Stress/Strain Plot for 316L in Molten FLiNaK at a Strain Rate of 1e-6 (in/in)/sec"
    # )
    # plot_file_type = ".png"
    # plot_out_path = (
    #     data_dir  # Will output plot in same directory with same name as input file
    # )
    # plot_out_path += data_name
    # plot_out_path += plot_file_type
    # plt.grid(True)
    # plt.savefig(plot_out_path)
    # plt.show()


app.run()

# %% Import raw data


## The following lines will plot the raw data
# plt.plot(data.Stroke, data.Load)
# plt.xlabel('Stroke (in)')
# plt.ylabel('Load (lbs)')
# plt.savefig('/Users/briggssa/Repos/test-python-project/true_data_raw.png')
# plt.show()

# %% Process raw data and plot processed data
