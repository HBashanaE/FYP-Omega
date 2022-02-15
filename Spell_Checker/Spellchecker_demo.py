from os.path import isfile, join, dirname, join
from os import listdir
import json
from CharRNN import CharRNN
from spellchecker import SpellChecker
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from utils import one_hot_encode, preprocess, tokenize
import os
import pandas as pd
from unicodedata import normalize

train_on_gpu = False

dirname_ = dirname(os.path.abspath(__file__)).split('\\')[:-1]
dirname_ = '/'.join(dirname_)
dictionaryPath = dirname_ + '/Data/combined all names - dictionary - train.json'
neuralModelPath = dirname_ + '/Data/neural-model-tokenized-1024-2-4.pth'
ngramModelPath = dirname_ + '/ngram_model/ngram_KN3.pickle'

insertionPath = dirname_ + '/error_model/Probability sets/insertion_probabilities.json'
deletionPath = dirname_ + '/error_model/Probability sets/deletion_probabilities.json'
substitutionPath = dirname_ + '/error_model/Probability sets/substitution_probabilities.json'

spellChecker = SpellChecker(
    dictionaryPath, neuralModelPath, ngramModelPath, insertionPath, deletionPath, substitutionPath)


names = [('රෂ්ණි', ['රෂිණි']),
        ('වෙල්ලසාම්', ['වෙල්ලසාමි']),
        ('අබදුල්', ['අබ්දුල්']),
        ('පතිරණා', ['පතිරණ']),
        ('කමල', ['කමල්', 'කමලා']),
        ('සුමනතිරන්', ['සුමන්තිරන්'])]

for error, correct in names:
    suggestions = [x[1] + ' <==' if x[1] in correct else x[1] for x in spellChecker.correctSpelling(error)]
    f = open('demo.txt', 'a', encoding='utf-8')
    f.write('==========================================================\n')
    f.write(f'Input: {error}\n')
    f.write(f'Expexted output(s): {" ".join(correct)}\n')
    f.write('Suggestions: \n')
    f.write('\n'.join(suggestions + ['']))
    f.write('==========================================================\n')

