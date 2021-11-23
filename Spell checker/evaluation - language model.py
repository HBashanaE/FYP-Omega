from os.path import isfile, join, dirname, join
from os import listdir
from unicodedata import normalize
import json

from utils import tokenize

from CharRNN import CharRNN
from LanguageModel import NeuralLanguageModel

root_dirname = dirname(__file__)
neural_model_path = join(root_dirname, '../Data/nn-model-tokenized.pth')

neural_model = NeuralLanguageModel(neural_model_path)

path = join(
    root_dirname, '../Error data/OCR Error Data/OCR errors testing')
files = [f for f in listdir(path) if isfile(join(path, f))]

raw_names = []
for file in files:
  raw_names +=  open(join(path, file), encoding='utf-8').readlines()[1:]
raw_names = ''.join(raw_names)

normalized_raw_names = normalize('NFC', raw_names.strip())
normalized_name_list = normalized_raw_names.split('\n')

 
def get_accuracy(error, original):
    error = tokenize(error)
    original = tokenize(original)
    return neural_model.getNameAccuracy(original), neural_model.getNameAccuracy(error)

difference = 0
results = []
for i, line in enumerate(normalized_name_list):
    original, error_malith, error_abhaya = line.split(',')
    
    if(original != error_malith):
        try:
            error_name_accuracy, original_name_accuracy = get_accuracy(error_malith, original)
            difference += (error_name_accuracy - original_name_accuracy)
            results.append({"original_name": original, "error_anme": error_malith, "error_name_accuracy":error_name_accuracy, "original_name_accuracy": original_name_accuracy})
        except:
            pass
    if(original != error_abhaya):
        try:
            error_name_accuracy, original_name_accuracy = get_accuracy(error_abhaya, original)
            difference += (error_name_accuracy - original_name_accuracy)
            results.append({"original_name": original, "error_anme": error_abhaya, "error_name_accuracy":error_name_accuracy, "original_name_accuracy": original_name_accuracy})
        except:
            pass


    # if(i != 0 and i % 100 == 0):
    #     print(corrected, not_corrected)
print(difference / (i + 1))

with open(join(root_dirname, "result_evaluation_language_model.json"), "w", encoding='utf-8') as outfile:
    json.dump({"results": results, "final_socre": difference}, outfile, ensure_ascii=False)