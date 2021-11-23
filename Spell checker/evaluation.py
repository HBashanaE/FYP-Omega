# from os.path import isfile, join, dirname, join
# from os import listdir
# from unicodedata import normalize
# from CharRNN import CharRNN
# from driver import spellChecker
# from multiprocessing import Pool
# from multiprocessing import Process


# dirname = dirname(__file__)

# path = join(
#     dirname, '../Error data/OCR Error Data/OCR error training')
# files = [f for f in listdir(path) if isfile(join(path, f))]

# raw_names = []
# for file in files:
#   raw_names +=  open(join(path, file), encoding='utf-8').readlines()[1:]
# raw_names = ''.join(raw_names)

# normalized_raw_names = normalize('NFC', raw_names.strip())
# normalized_name_list = normalized_raw_names.split('\n')

# corrected = 0
# not_corrected = 0

# def isCorrected(error, original):
#     try:
#         suggestions = spellChecker.correctSpelling(error)
#         if(any(original == s[1] for s in suggestions)):
#             return 1
#         else:
#             return 0
#     except:
#         return -1

# def evaluate(normalized_name_list):
#     corrected, not_corrected = 0, 0
#     for i, line in enumerate(normalized_name_list):
#         original, error_malith, error_abhaya = line.split(',')
#         if(original != error_malith):
#             r = isCorrected(error_malith, original)
#             if(r == 1):
#                 corrected += 1
#             elif(r == 0):
#                 not_corrected += 1
#             else:
#                 pass
#         if(original != error_abhaya):
#             r = isCorrected(error_malith, error_abhaya)
#             if(r == 1):
#                 corrected += 1
#             elif(r == 0):
#                 not_corrected += 1
#             else:
#                 pass
#     return corrected, not_corrected


# with Pool(1) as p:
#     # a = p.starmap(evaluate, [(1, 2), (2, 3), (3, 4)])
#     a = p.map(evaluate, [normalized_name_list[0:10], normalized_name_list[10:20], normalized_name_list[20:30]])
#     print(a)


# a = evaluate(normalized_name_list[0:10])
# print(a)

# for i, line in enumerate(normalized_name_list):
#     original, error_malith, error_abhaya = line.split(',')
#     if(original != error_malith):
#         r = isCorrected(error_malith, original)
#         if(r == 1):
#             corrected += 1
#         elif(r == 0):
#             not_corrected += 1
#         else:
#             pass
#     if(original != error_abhaya):
#         r = isCorrected(error_malith, error_abhaya)
#         if(r == 1):
#             corrected += 1
#         elif(r == 0):
#             not_corrected += 1
#         else:
#             pass
#     if(i != 0 and i % 100 == 0):
#         print(corrected, not_corrected)
        

# print('Final', corrected, not_corrected)


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
neuralModelPath = os.path.join(dirname, '../Data/neural-model-base-char.pth')
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

print('Starting evaluation...')
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

with open(os.path.join(dirname, "evaluation_result.json"), "w",encoding='utf8') as outfile:
    json.dump({"truePositive": truePositive, "trueNegative": trueNegative, "falsePositive": falsePositive, "falseNegative": falseNegative,
                "correctSuggestion": correctSuggestion,  "incorrectSuggestion": incorrectSuggestion, "rank": rank}, outfile, ensure_ascii=False)

print('Evaluation completed')