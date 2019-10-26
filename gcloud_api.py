import io
import os

# Imports the Google Cloud client library
from itertools import chain

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from pydub import AudioSegment


def gcloud_speech_to_text(file_name):
    # Instantiates a client
    client = speech.SpeechClient()
    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
        language_code='en-US')

    # Detects speech in the audio file
    return client.recognize(config, audio)
