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

train_on_gpu = False

dirname = os.path.dirname(__file__)
dictionaryPath = os.path.join(
    dirname, '../Data/combined all names - dictionary - train.json')
neuralModelPath = os.path.join(dirname, f'../Data/neural-model-tokenized-{1024}-{4}-{2}.pth')
ngramModelPath = os.path.join(dirname, '../ngram_model/my_classifier.pickle')

insertionPath = os.path.join(
    dirname, '../error_model/Probability sets/insertion_probabilities.json')
deletionPath = os.path.join(
    dirname, '../error_model/Probability sets/deletion_probabilities.json')
substitutionPath = os.path.join(
    dirname, '../error_model/Probability sets/substitution_probabilities.json')


spellChecker = SpellChecker(
    dictionaryPath, neuralModelPath, ngramModelPath, insertionPath, deletionPath, substitutionPath)

errorData = os.path.join(
    dirname, '../error_data/ocr_error_data/OCR errors testing/OCR errors testing - 1.csv')


errors = pd.read_csv(errorData,encoding='utf8')
truePositive = 0
trueNegative=0
falsePositive = 0
falseNegative = 0
correctSuggestion = 0
incorrectSuggestion = 0
rank = [0]*10

# print('Starting evaluation - OCR...')
# for index, row in errors.iterrows():
#     if index>1000:
#         break
#     for font in ['Malith','Abhaya']:
#         try:
#             malSuggestions = spellChecker.correctSpelling(row[font])
#         except:
#             continue
#         for index, suggest in enumerate(malSuggestions):
#             if suggest[1]==row['original']:
#                 if suggest[1]==row[font]:
#                     trueNegative+=1
#                 else:
#                     truePositive+=1
#                 rank[index]+=1
#                 break
#         else:
#             if row['original']==row[font]:
#                 falseNegative+=1
#             else:
#                 falsePositive+=1

# with open(os.path.join(dirname, "evaluation_result_spellchecker_ocr-addresses.json"), "w",encoding='utf8') as outfile:
#     json.dump({"truePositive": truePositive, "trueNegative": trueNegative, "falsePositive": falsePositive, "falseNegative": falseNegative,
#                 "correctSuggestion": correctSuggestion,  "incorrectSuggestion": incorrectSuggestion, "rank": rank}, outfile, ensure_ascii=False)

print('Starting evaluation - Statistical...')

with open(os.path.join(dirname, "../error_data/probabilistic_edit_distance_errors/confussion_edit_distance_errors_addresses.csv"), "r", encoding='utf-8') as f:
    raw_names_confussion_edit_distance = f.readlines()[1:]
raw_names_confussion_edit_distance = ''.join(
    raw_names_confussion_edit_distance)

name_list_edit_distance = raw_names_confussion_edit_distance.split(
    '\n')

truePositive = 0
trueNegative=0
falsePositive = 0
falseNegative = 0
correctSuggestion = 0
incorrectSuggestion = 0
rank = [0]*10

for i, line in enumerate(name_list_edit_distance[:1000]):
    original, error = line.split(',')
   
    try:
        malSuggestions = spellChecker.correctSpelling(error)
    except:
        print(error)
        continue
    for index, suggest in enumerate(malSuggestions):
        if suggest[1]==original:
            if suggest[1]==error:
                trueNegative+=1
            else:
                truePositive+=1
            rank[index]+=1
            break
    else:
        if original==error:
            falseNegative+=1
        else:
            falsePositive+=1

with open(os.path.join(dirname, "evaluation_result_spellchecker_statistical-addresses.json"), "w",encoding='utf8') as outfile:
    json.dump({"truePositive": truePositive, "trueNegative": trueNegative, "falsePositive": falsePositive, "falseNegative": falseNegative,
                "correctSuggestion": correctSuggestion,  "incorrectSuggestion": incorrectSuggestion, "rank": rank}, outfile, ensure_ascii=False)


print('Starting evaluation - Random...')

with open(os.path.join(dirname, "../error_data/random_error_data/addresses Random errors.csv"), "r", encoding='utf-8') as f:
    raw_names_random = f.readlines()[1:]
raw_names_random = ''.join(
    raw_names_random)

name_list_random = raw_names_random.split(
    '\n')

truePositive = 0
trueNegative=0
falsePositive = 0
falseNegative = 0
correctSuggestion = 0
incorrectSuggestion = 0
rank = [0]*10

for i, line in enumerate(name_list_random[:1000]):
    original, error = line.split(',')
   
    try:
        malSuggestions = spellChecker.correctSpelling(error)
    except:
        print(error)
        continue
    for index, suggest in enumerate(malSuggestions):
        if suggest[1]==original:
            if suggest[1]==error:
                trueNegative+=1
            else:
                truePositive+=1
            rank[index]+=1
            break
    else:
        if original==error:
            falseNegative+=1
        else:
            falsePositive+=1

with open(os.path.join(dirname, "evaluation_result_spellchecker_random-addresses.json"), "w",encoding='utf8') as outfile:
    json.dump({"truePositive": truePositive, "trueNegative": trueNegative, "falsePositive": falsePositive, "falseNegative": falseNegative,
                "correctSuggestion": correctSuggestion,  "incorrectSuggestion": incorrectSuggestion, "rank": rank}, outfile, ensure_ascii=False)
print('Evaluation completed')