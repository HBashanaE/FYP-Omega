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

raw_names_ocr = []
for file in files:
  raw_names_ocr +=  open(join(path, file), encoding='utf-8').readlines()[1:]
raw_names_ocr = ''.join(raw_names_ocr)

normalized_raw_names_ocr = normalize('NFC', raw_names_ocr.strip())
normalized_name_list_ocr = normalized_raw_names_ocr.split('\n')

 
def get_accuracy(error, original):
    error = tokenize(error)
    original = tokenize(original)
    return neural_model.getNameAccuracy(original), neural_model.getNameAccuracy(error)

print('Starting OCR...')

difference = 0
negative_differences = 0
results = []
for i, line in enumerate(normalized_name_list_ocr):
    original, error_malith, error_abhaya = line.split(',')
    
    if(original != error_malith):
        try:
            error_name_accuracy, original_name_accuracy = get_accuracy(error_malith, original)
            norm_difference = (original_name_accuracy - error_name_accuracy)/original_name_accuracy
            difference += norm_difference
            if norm_difference<0:
                negative_differences+=1
            results.append({"original_name": original, "error_name": error_malith, "error_name_accuracy":error_name_accuracy, "original_name_accuracy": original_name_accuracy, "normalized_difference": norm_difference})
        except:
            pass
    if(original != error_abhaya):
        try:
            error_name_accuracy, original_name_accuracy = get_accuracy(error_abhaya, original)
            norm_difference = (original_name_accuracy - error_name_accuracy)/original_name_accuracy
            difference += norm_difference
            if norm_difference<0:
                negative_differences+=1
            results.append({"original_name": original, "error_name": error_abhaya, "error_name_accuracy":error_name_accuracy, "original_name_accuracy": original_name_accuracy, "normalized_difference": norm_difference})
        except:
            pass

with open(join(root_dirname, "result_evaluation_language_model_ocr.json"), "w", encoding='utf-8') as outfile:
    json.dump({"results": results, "final_socre": difference/(i + 1)}, outfile, ensure_ascii=False)

print('Starting confussion set...')

with open(join(root_dirname, "../Error data/Edit distance errors - confussion/confussion_edit_distance_errors_.csv"), "r", encoding='utf-8') as f:
    raw_names_confussion_edit_distance = f.readlines()[1:]
raw_names_confussion_edit_distance = ''.join(raw_names_confussion_edit_distance)

normalized_raw_names_edit_distance = normalize('NFC', raw_names_confussion_edit_distance.strip())
normalized_name_list_edit_distance = normalized_raw_names_edit_distance.split('\n')

difference = 0
results = []
for i, line in enumerate(normalized_name_list_edit_distance):
    original, error = line.split(',')
    try:
        error_name_accuracy, original_name_accuracy = get_accuracy(error, original)
        difference += (error_name_accuracy - original_name_accuracy)
        results.append({"original_name": original, "error_anme": error, "error_name_accuracy":error_name_accuracy, "original_name_accuracy": original_name_accuracy})
    except:
        pass

with open(join(root_dirname, "result_evaluation_language_model_edit_distance.json"), "w", encoding='utf-8') as outfile:
    json.dump({"results": results, "final_socre": difference/(i + 1)}, outfile, ensure_ascii=False)

print('Finish')
