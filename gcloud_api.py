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
    'Anish.mp3')
wav_file_name = os.path.join(
    os.path.dirname(__file__),
    'Audio_files',
    'Anish.wav')
convert = AudioSegment.from_mp3(file_name)
convert.set_channels(1)
##convert.export(wav_file_name, format="wav")

# Loads the audio into memory
with io.open(wav_file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    enable_word_time_offsets=True,
    enable_automatic_punctuation=True,
    language_code='en-US')

# Detects speech in the audio file
response = client.recognize(config, audio)

# The first result includes start and end time word offsets
result = response.results[0]
# First alternative is the most probable result
alternative = result.alternatives[0]
print(u"Transcript: {}".format(alternative.transcript))
# Print the start and end time of each word
for word in alternative.words:
    print(u"Word: {}".format(word.word))
    print(
        u"Start time: {} seconds {} nanos".format(
            word.start_time.seconds, word.start_time.nanos
        )
    )
    print(
        u"End time: {} seconds {} nanos".format(
            word.end_time.seconds, word.end_time.nanos
        )
    )
