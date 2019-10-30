# -*- coding: utf-8 -*-


""" Use DeepMoji to score texts for emoji distribution.

The resulting emoji ids (0-63) correspond to the mapping
in emoji_overview.png file at the root of the DeepMoji repo.

These 64 results were mapped to emotions that can be displayed by the audio analysis tool.

Writes the result to a csv file.
"""
from __future__ import print_function, division
import example_helper
import json
import csv
import numpy as np
from deepmoji.sentence_tokenizer import SentenceTokenizer
from deepmoji.model_def import deepmoji_emojis
from deepmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH
import os

current_path = os.getcwd()
path = current_path + '/'+"Google_voice_data/google_data.json"

with open(path, 'r') as f:
    j = json.load(f)

audio_tagged = eval(sys.argv[1])

all_words_dict_list = j['words']
words = []
gtime_stamps = []
deep_affects_time_stamps = []
audio_emotions = []

for word in audio_tagged:
    deep_affects_time_stamps.append(word["end"])
    audio_emotions.append(word["emotion"])

for word_dict in all_words_dict_list:
    words.append(word_dict['word'])
    gtime_stamps.append(float(word_dict['end_time']) / 1000)
    # gtime_stamps are in seconds

clauses = []
string = ''
pos = 0
l = min(len(words), len(gtime_stamps))
for i in range(l):
    if pos < len(deep_affects_time_stamps):
        t = deep_affects_time_stamps[pos]
        if gtime_stamps[i] >= t or i == (l - 1):
            string = string + words[i]
            clauses.append(string)
            string = ''
            pos += 1
        else:
            string = string + words[i] + ' '


def top_elements(array, k):
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]


maxlen = 30
batch_size = 32

with open(VOCAB_PATH, 'r') as f:
    vocabulary = json.load(f)
st = SentenceTokenizer(vocabulary, maxlen)
tokenized, _, _ = st.tokenize_sentences(clauses)

model = deepmoji_emojis(maxlen, PRETRAINED_PATH)
model.summary()

prob = model.predict(tokenized)

# Find top emojis for each sentence. Emoji ids (0-63)
# correspond to the mapping in emoji_overview.png
# at the root of the DeepMoji repo.
scores = []
emotions = ['frustration', 'anger', 'excited', 'happy', 'neutral', 'disgust', 'joy']
mapping = [2, 0, 0, 0, 6, 0, 2, 6, 6, 2, 3, 4, 4, 2, 4, 3, 6, 6, 6, 0, 3, 2, 4, 4, 6, 4, 4, 0, 3, 5, 3, 3, 1, 2, 4, 4,
           3, 1, 4, 4, 2, 2, 4, 4, 2, 4, 4, 3, 3, 3, 3, 2, 0, 6, 2, 1, 3, 4, 2, 3, 3, 3, 4, 4]
for i, t in enumerate(clauses):
    t_tokens = tokenized[i]
    t_score = [t]
    t_prob = prob[i]
    ind_top = top_elements(t_prob, 5)
    t_score.append(sum(t_prob[ind_top]))
    t_score.extend(ind_top)
    t_score.extend([t_prob[ind] for ind in ind_top])
    scores.append(emotions[mapping[t_score[2]]])
    # can also edit this to incorporate certainty of prediction


def f(scores, audio_emotions):
    l = min(len(audio_emotions), len(scores))
    n_correct = 0
    for i in range(l):
        if audio_emotions[i] == scores[i]:
            n_correct += 1
    return float(n_correct) / l


y = f(scores, audio_emotions)


# y is the percentage of the clauses that match between the text sentiment and audio_emotion sentiment

def f2(scores, audio_emotions):
    l = min(len(audio_emotions), len(scores))
    n = 0
    n_correct = 0
    for i in range(l):
        if scores[i] != 'neutral':
            n += 1
            if audio_emotions[i] == scores[i]:
                n_correct += 1
    return float(n_correct) / n


y2 = f2(scores, audio_emotions)


# y2 is the percentage of clauses that match between scores and audio_emotions when only
# looking at clauses that were not classified in the text portion as being neutral


def get_audio_annotations(clauses, audio_emotions):
    audio_annotations = {}
    for i in range(min(len(clauses), len(audio_emotions))):
        audio_annotations[clauses[i]] = audio_emotions[i]
    filename = current_path + 'audio_annotations.json'
    datastore = audio_annotations
    with open(filename, 'w') as f:
            json.dump(datastore, f)


def get_text_annotations(clauses, scores):
    text_annotations = {}
    for i in range(min(len(clauses), len(scores))):
        text_annotations[clauses[i]] = scores[i]
    filename = current_path+'text_annotations.json'
    datastore = text_annotations
    with open(filename, 'w') as f:
            json.dump(datastore, f)
