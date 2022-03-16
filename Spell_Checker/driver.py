import json
from spellchecker import SpellChecker
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from utils import one_hot_encode, preprocess, tokenize_full
import os
import pandas as pd

train_on_gpu = False


class CharRNN(nn.Module):

    def __init__(self, tokens, n_hidden=512, n_layers=3,
                 drop_prob=0.3, lr=0.001):
        super().__init__()
        self.drop_prob = drop_prob
        self.n_layers = n_layers
        self.n_hidden = n_hidden
        self.lr = lr

        self.chars = tokens
        self.int2char = dict(enumerate(self.chars))
        self.char2int = {ch: ii for ii, ch in self.int2char.items()}

        self.lstm = nn.LSTM(len(self.chars), n_hidden, n_layers,
                            dropout=drop_prob, batch_first=True)

        self.dropout = nn.Dropout(drop_prob)

        self.fc = nn.Linear(n_hidden, len(self.chars))

    def forward(self, x, hidden):
        ''' Forward pass through the network. 
            These inputs are x, and the hidden/cell state `hidden`. '''

        r_output, hidden = self.lstm(x, hidden)

        out = self.dropout(r_output)

        out = out.contiguous().view(-1, self.n_hidden)

        out = self.fc(out)

        return out, hidden

    def init_hidden(self, batch_size):
        weight = next(self.parameters()).data

        if (train_on_gpu):
            hidden = (weight.new(self.n_layers, batch_size, self.n_hidden).zero_().cuda(),
                      weight.new(self.n_layers, batch_size, self.n_hidden).zero_().cuda())
        else:
            hidden = (weight.new(self.n_layers, batch_size, self.n_hidden).zero_(),
                      weight.new(self.n_layers, batch_size, self.n_hidden).zero_())

        return hidden


dirname = os.path.dirname(__file__)
dictionaryPath = os.path.join(
    dirname, '../Data/Names/combined all names - dictionary - train.json')
neuralModelPath = os.path.join(dirname, '../Language_Model/Neural_Language_Model/Saved_Models/nn-model-tokenized.pth')
ngramModelPath = os.path.join(dirname, '../Language_Model/Ngram_Model/my_classifier.pickle')

insertionPath = os.path.join(
    dirname, '../error_model/Probability sets/insertion_probabilities.json')
deletionPath = os.path.join(
    dirname, '../error_model/Probability sets/deletion_probabilities.json')
substitutionPath = os.path.join(
    dirname, '../error_model/Probability sets/substitution_probabilities.json')


spellChecker = SpellChecker(
    dictionaryPath, neuralModelPath, ngramModelPath, insertionPath, deletionPath, substitutionPath)         

suggestions = spellChecker.correctSpelling('යසත')
# with open("sample.json", "w",encoding='utf8') as outfile:
#     json.dump(suggestions, outfile, ensure_ascii=False)
print(suggestions)
