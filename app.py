from __future__ import print_function
import re
import subprocess
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
import datetime
import requests
from gcloud_api import *

'''
Here we define the download and the upload folder on the server
'''
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'

# The allowed extensions that can be uploaded on the webpage
ALLOWED_EXTENSIONS = {'pdf', 'csv', 'mp3'}

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
    if os.path.isfile('downloads/out.csv'):
        os.remove('downloads/out.csv')
    if os.path.isfile('downloads/bal.csv'):
        os.remove('downloads/bal.csv')

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
                process_file(path=os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # uploaded_file(filename=filename)
        return render_template('downloads.html')
    return render_template('index.html')


def process_file(path):
    """
    Calls the relevant functions once the file is uploaded by the user. Right now we are calling the emotion tagging
    function
    :param path: path to the audio file
    :return: Nothing
    """
    emotion_tagging(path=path)
    save_score_data()
    get_clause_emotions(path=path)
    #the function above returns the clause/emotion dictionary which can be used to display the scripts.


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


def emotion_tagging(path):
    # In this program, we are calling the url and making a get request to that using Harsh's API key
    # We send the mp3 file we want to upload decoded audio in the body_json of the requests

    """
    This function takes the path of the audio file and calls the DeepAffects API.

    :param path: path to the audio file, uploaded, present locally
    :return: json response from the API
    """
    # Just for testing, we are commenting the API Calls and just returning the API Response as JSON
    """
    url = "https://proxy.api.deepaffects.com/audio/generic/api/v2/sync/recognise_emotion?apikey" \
          "=7h1YbhaMje9IBTrUTDGNa8KGABD1n9cn"

    headers = {'Content-Type': "application/json"}

    with open(path, 'rb') as fin:
        audio_content = fin.read()
    audio_decoded = base64.b64encode(audio_content).decode('utf-8')

    body_json = {"content": audio_decoded,
                 "encoding": "MPEG Audio",
                 "language_code": "en-US",
                 "sample_rate": 48000}

    # text_body_json = {"content": ""}

    data = requests.post(url=url, json=body_json, headers=headers)
    with open('audio-analysis/results.txt', 'w') as output:
        output.write(data.text)
    pprint(data.text)
    """

    json_result = [{"end": 3.0, "start": 0.0, "emotion": "neutral"}, {"end": 6.0, "start": 3.0, "emotion": "happy"},
                   {"end": 8.856, "start": 6.0, "emotion": "excited"}]
    print(json_result)
    return json_result


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # We are not really using the filename arg but ya
    # filename = filename.split('.')[0] + ".csv"
    filename = "out.csv"
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)


def get_clause_emotions(filename):
    # loads audio file-filename and returns clause_and_emotion dictionary.
    gresponse = gcloud_speech_to_text(filename)
    deepresponse = emotion_tagging(filename)

    deep_affects_time_stamps = []
    audio_emotions = []

    google_words = gresponse["words"]
    gtime_stamps = []
    words = []

    for word in google_words:

        words.append(word["word"])
        gtime_stamps.append(float(word['end_time']) / 1000)

    for tag in deepresponse:
        deep_affects_time_stamps.append(tag["end"])
        audio_emotions.append(tag["emotion"])

    dpeffects = {}
    string = ''
    pos = 0
    l = min(len(words), len(gtime_stamps))
    for i in range(l):
        if pos < len(deep_affects_time_stamps):
            t = deep_affects_time_stamps[pos]
            if gtime_stamps[i] >= t or i == (l - 1):
                string = string + words[i] + '.'
                dpeffects[string] = deep_affects_time_stamps[pos]
                string = ''
                pos += 1
            else:
                string = string + words[i] + ' '
    return dpeffects

def answer(filename):
    dpeffects, = get_clause_emotions(filename)
    return json.dumps(dpeffects)


def tone_analyzer():
    # API KEY rNiB7aYI-pVZQ_6I-U-D_avkVNsOUUYMf9n5dXOhrjHc
    # https://gateway.watsonplatform.net/tone-analyzer/api

    url = "https://proxy.api.deepaffects.com/audio/generic/api/v2/sync/recognise_emotion?apikey" \
          "=7h1YbhaMje9IBTrUTDGNa8KGABD1n9cn"

    headers = {'Content-Type': "application/json"}

    # with open(path, 'rb') as fin:
    #     audio_content = fin.read()
    # audio_decoded = base64.b64encode(audio_content).decode('utf-8')

    body_json = {"content": "12",
                 "encoding": "MPEG Audio",
                 "language_code": "en-US",
                 "sample_rate": 48000}

    """
    curl -X GET -u "apikey:rNiB7aYI-pVZQ_6I-U-D_avkVNsOUUYMf9n5dXOhrjHchttps://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21
    &text=Team%2C%20I%20know%20that%20times%20are%20tough%21%20Product%20sales%20have
    %20been%20disappointing%20for%20the%20past%20three%20quarters.%20We%20have%20a%20
    competitive%20product%2C%20but%20we%20need%20to%20do%20a%20better%20job%20of%20
    selling%20it%21"
    """
    data = requests.post(url=url, json=body_json, headers=headers)
