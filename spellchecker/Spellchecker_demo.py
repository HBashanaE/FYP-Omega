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
neuralModelPath = dirname_ + '/Data/neuralModel.pth'
ngramModelPath = dirname_ + '/N-gram Model/ngram_KN3.pickle'

insertionPath = dirname_ + '/Error model/Probability sets/insertion_probabilities.json'
deletionPath = dirname_ + '/Error model/Probability sets/deletion_probabilities.json'
substitutionPath = dirname_ + '/Error model/Probability sets/substitution_probabilities.json'
print(dirname_)

spellChecker = SpellChecker(
    dictionaryPath, neuralModelPath, ngramModelPath, insertionPath, deletionPath, substitutionPath)

while True:
    print([x[1] for x in spellChecker.correctSpelling(input('Enter name :'))])

