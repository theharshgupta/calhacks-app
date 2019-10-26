# -*- coding: utf-8 -*-


""" Use DeepMoji to score texts for emoji distribution.

The resulting emoji ids (0-63) correspond to the mapping
in emoji_overview.png file at the root of the DeepMoji repo.

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
import sys
script = 'this must be set to equal input from webpage'
script=script.decode('utf-8')
whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ.')
#may be able to add in other punctuation in the whitelist.
updated_script = ''.join(filter(whitelist.__contains__, script))
sentence = []
string=''

for c in range(len(updated_x)):
    string = string + c
    if c=='.':
        sentence_list.append(string)
        string = ''


OUTPUT_PATH = 'test_sentences.csv'



def top_elements(array, k):
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]



maxlen = 30
batch_size = 32

with open(VOCAB_PATH, 'r') as f:
    vocabulary = json.load(f)
st = SentenceTokenizer(vocabulary, maxlen)
tokenized, _, _ = st.tokenize_sentences(TEST_SENTENCES)

model = deepmoji_emojis(maxlen, PRETRAINED_PATH)
model.summary()

prob = model.predict(tokenized)

# Find top emojis for each sentence. Emoji ids (0-63)
# correspond to the mapping in emoji_overview.png
# at the root of the DeepMoji repo.
scores = []
emotions = ['frustration','anger','excited','happy'(3),'neutral','disgust','joy'(6)]
mapping = [2,0,0,0,6,0,2,6,6,2,3,4,4,2,4,3,6,6,6,0,3,2,4,4,6,4,4,0,3,5,3,3,1,2,4,4,3,1,4,4,2,2,4,4,2,4,4,3,3,3,3,2,0,6,2,1,3,4,2,3,3,3,4,4]
for i, t in enumerate(TEST_SENTENCES):
    t_tokens = tokenized[i]
    t_score = [t]
    t_prob = prob[i]
    ind_top = top_elements(t_prob, 5)
    t_score.append(sum(t_prob[ind_top]))
    t_score.extend(ind_top)
    t_score.extend([t_prob[ind] for ind in ind_top])
    scores.append(emotions[mapping[t_score[2]]])
    #can also edit this to incorporate certainty of prediction
def f(scores):
    return scores
f()
