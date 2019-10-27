from __future__ import print_function

import json

import requests
import traceback

from gcloud_api import gcloud_speech_to_text


def process_file(path):
    """
    Calls the relevant functions once the file is uploaded by the user. Right now we are calling the emotion tagging
    function
    :param path: path to the audio file
    :return: Nothing
    """
    emotion_tagging(path)
    dpeffects, clauses = get_clause_emotions(path)
    tone_dict = tone_analyzer(clauses)

    return json.dumps({'audio': dpeffects, 'text': tone_dict})
    # save_score_data()
    # get_clause_emotions(path=path)
    # the function above returns the clause/emotion dictionary which can be used to display the scripts.


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
    clauses = []
    for i in range(l):
        if pos < len(deep_affects_time_stamps):
            t = deep_affects_time_stamps[pos]
            if gtime_stamps[i] >= t or i == (l - 1):
                string = string + words[i] + '.'
                dpeffects[string] = audio_emotions[pos]
                clauses.append(string)
                string = ''
                pos += 1
            else:
                string = string + words[i] + ' '
    return dpeffects, clauses


def tone_analyzer(clauses):
    # API KEY rNiB7aYI-pVZQ_6I-U-D_avkVNsOUUYMf9n5dXOhrjHc
    # https://gateway.watsonplatform.net/tone-analyzer/api
    api_key = "rNiB7aYI-pVZQ_6I-U-D_avkVNsOUUYMf9n5dXOhrjHc"

    username = 'apikey'
    password = api_key
    watsonUrl = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21'
    headers = {"content-type": "text/plain"}
    data = ''
    for clause in clauses:
        data = data + clause + ' '
    try:
        r = requests.post(watsonUrl, auth=(username, password), headers=headers, data=data)
        print("IBM Watson \n\n\n", r.text)
        emotions = []
        mapping = {"joy": "joy", "sadness": "neutral", "fear": "neutral", "disgust": "disgust", "anger": "anger"}
        x = eval(r.text)
        watson = {}
        for sentence in x["sentences_tone"]:
            #above is correct
            s = sentence["text"]
            emotion = sentence["tones"]
            if emotion:
                emotion = emotion[0]['tone_id']
                watson[s] = mapping[emotion]
            else:
                watson[s] = "neutral"
            # ex. watson data {"sentences_tone":[{"sentence_id":0,"text":"Ping pong is the best sport in the world.","tones":[{"score":0.822188,"tone_id":"joy","tone_name":"Joy"}]},{"sentence_id":1,"text":"I like Chinese people.","tones":[{"score":0.88939,"tone_id":"tentative","tone_name":"Tentative"}]},{"sentence_id":2,"text":"I fucking hate PG&E they are horrible and they should make changes in their management.","tones":[{"score":0.827514,"tone_id":"anger","tone_name":"Anger"}]},{"sentence_id":3,"text":"This company is bankrupt.","tones":[{"score":0.72178,"tone_id":"sadness","tone_name":"Sadness"}]}]}
        return watson
    except Exception:
        return traceback.format_exc()


def answer(filename):
    dpeffects, = get_clause_emotions(filename)
    return json.dumps(dpeffects)
