import io
import os
import json

# Imports the Google Cloud client library
from itertools import chain

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from pydub import AudioSegment


def gcloud_speech_to_text(file):
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_path = os.path.join(
        ## os.path.dirname(__file__),
        'Audio_files',
        file)

    # Loads the audio into memory
    with io.open(file_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
        language_code='en-US')

    # Detects speech in the audio file
    response = parse_gcloud_recognize_response(client.recognize(config, audio))
    save_dict_as_json(response, "Google_voice_data/" + file + ".json")
    return response


def parse_gcloud_recognize_response(response):
    """Parse the Google Cloud Recognize Response into a dictionary"""
    data = response.results[0].alternatives[0]
    result = {"transcript": data.transcript, "confidence": data.confidence}

    words = []
    for word in data.words:
        word_dict = {"word": word.word,
                     "start_time": word.start_time.seconds * 1e3 + word.start_time.nanos / 1e6,
                     "end_time": word.end_time.seconds * 1e3 + word.end_time.nanos / 1e6}
        words.append(word_dict)

    result["words"] = words

    return result


def save_dict_as_json(d, file_path):
    with open(file_path, "w") as f:
        f.write(json.dumps(d))


def get_gcloud_timestamps(response_dict):
    """Get the timestamps of words from a Google Cloud Recognize Response dictionary.
        A timestamp is a 2D tuple of the start time and end time in milliseconds"""
    timestamps = []

    for word in response_dict["words"]:
        timestamps.append((word["start_time"], word["end_time"]))

    return timestamps

def save_score_data():
    subprocess.Popen(["api/python2.7/bin/python", "DeepMoji-main/examples/score_texts_emojis.py"])
