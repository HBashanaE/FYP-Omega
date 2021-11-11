import json
from spellchecker import SpellChecker
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from utils import one_hot_encode, preprocess, tokenize
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
    dirname, '../Data/combined all names - dictionary - train.json')
neuralModelPath = os.path.join(dirname, '../Data/model(1).pth')
ngramModelPath = os.path.join(dirname, '../N-gram Model/my_classifier.pickle')

insertionPath = os.path.join(
    dirname, '../Error model/Probability sets/insertion_probabilities.json')
deletionPath = os.path.join(
    dirname, '../Error model/Probability sets/deletion_probabilities.json')
substitutionPath = os.path.join(
    dirname, '../Error model/Probability sets/substitution_probabilities.json')


spellChecker = SpellChecker(
    dictionaryPath, neuralModelPath, ngramModelPath, insertionPath, deletionPath, substitutionPath)

errorData = os.path.join(
    dirname, '../Error data/OCR Error Data/OCR errors testing/OCR errors testing - 1.csv')


errors = pd.read_csv(errorData,encoding='utf8')
truePositive = 0
trueNegative=0
falsePositive = 0
falseNegative = 0
correctSuggestion = 0
incorrectSuggestion = 0
rank = [0]*10
for index, row in errors.iterrows():
    if index>1000:
        break
    for font in ['Malith','Abhaya']:
        try:
            malSuggestions = spellChecker.correctSpelling(row[font])
        except:
            continue
        for index, suggest in enumerate(malSuggestions):
            if suggest[1]==row['original']:
                if suggest[1]==row[font]:
                    trueNegative+=1
                else:
                    truePositive+=1
                rank[index]+=1
                break
        else:
            if row['original']==row[font]:
                falseNegative+=1
            else:
                falsePositive+=1

print(f'{truePositive =}\n{trueNegative=}\n{falsePositive = }\n{falseNegative = }\n{correctSuggestion = }\n{incorrectSuggestion = }\n{rank}')            

# suggestions = spellChecker.correctSpelling('යසත්')
# with open("sample.json", "w",encoding='utf8') as outfile:
#     json.dump(suggestions, outfile, ensure_ascii=False)
#print(suggestions)
