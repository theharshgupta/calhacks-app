from __future__ import print_function
import requests
import base64
import time
#import deepaffects
#from deepaffects.rest import ApiException
from pprint import pprint

# In this program, we are calling the url and making a get request to that using Harsh's API key
# We send the mp3 file we want to upload decoded audio in the body_json of the requests

url = "https://proxy.api.deepaffects.com/audio/generic/api/v2/sync/recognise_emotion?apikey" \
      "=7h1YbhaMje9IBTrUTDGNa8KGABD1n9cn"

headers = {'Content-Type': "application/json"}

with open("anish.mp3", 'rb') as fin:
    audio_content = fin.read()

audio_decoded = base64.b64encode(audio_content).decode('utf-8')

body_json = {"content": audio_decoded,
             "encoding": "MPEG Audio",
             "language_code": "en-US",
             "sample_rate": 48000}

data = requests.post(url=url, json=body_json, headers=headers)
with open('results.txt', 'w') as output:
    output.write(data.text)
