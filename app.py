from __future__ import print_function
import re
import subprocess
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
import datetime
import requests
from gcloud_api import *
from analysis import *

# This is a test commit to the second branch

'''
Here we define the download and the upload folder on the server
'''
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'

# The allowed extensions that can be uploaded on the webpage
ALLOWED_EXTENSIONS = {'flac', 'wav', 'mp3'}

# THIS IS A TEST FOR GITHUB

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# limit upload size upto 100mb
app.config['MAX_CONTENT_LENGTH'] = 150 * 1024 * 1024


@app.route('/downloads/')
def downloads():
    return render_template("downloads.html")


@app.route('/file/')
def return_file():
    return send_file('downloads/bal.csv',
                     attachment_filename='bal.csv', as_attachment=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    This the the landing page. It includes an upload and submit button
    :return:
    """

    if request.method == 'POST':
        listOfFiles = request.files.getlist("file")
        for file in listOfFiles:
            print("File Name: ", file.filename)
            if file.filename == '':
                print('No file selected')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                alpha = process_file(filename)
                return render_template('index.html', result=alpha)
                # uploaded_file(filename=filename)
        return render_template('index.html')
    return render_template('index.html')


@app.route('/process/<path>', methods=["GET"])
def process(path):
    return process_file(path)

def emptydir():
    """
    :return:
    """
    for folder in [UPLOAD_FOLDER, DOWNLOAD_FOLDER]:
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # We are not really using the filename arg but ya
    # filename = filename.split('.')[0] + ".csv"
    filename = "out.csv"
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
