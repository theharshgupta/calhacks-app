import io
import os

# Imports the Google Cloud client library
from itertools import chain

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from pydub import AudioSegment

# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
file_name = os.path.join(
    os.path.dirname(__file__),
    'Audio_files',
    'emotions.mp3')
wav_file_name = os.path.join(
    os.path.dirname(__file__),
    'Audio_files',
    'emotions.wav')
convert = AudioSegment.from_mp3(file_name)
convert.set_channels(1)
##convert.export(wav_file_name, format="wav")

# Loads the audio into memory
with io.open(wav_file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code='en-US')

# Detects speech in the audio file
response = client.recognize(config, audio)

for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))
transcript = result.alternatives[0].transcript
