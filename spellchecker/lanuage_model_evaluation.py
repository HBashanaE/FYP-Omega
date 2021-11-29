from os.path import isfile, join, dirname, join
from os import listdir
from unicodedata import normalize
import json

from utils import tokenize, preprocess

from CharRNN import CharRNN
from LanguageModel import NeuralLanguageModel

root_dirname = dirname(__file__)
batch_size = 2048
n_hidden = 2
n_layers = 2
neural_model_path = join(root_dirname, f'../Data/neural-model-tokenized-{batch_size}-{n_hidden}-{n_layers}.pth')

neural_model = NeuralLanguageModel(neural_model_path)

path = join(
    root_dirname, '../error_data/ocr_error_data/OCR errors testing')
files = [f for f in listdir(path) if isfile(join(path, f))]

raw_names_ocr = []
for file in files:
  raw_names_ocr +=  open(join(path, file), encoding='utf-8').readlines()[1:]
raw_names_ocr = ''.join(raw_names_ocr)

normalized_raw_names_ocr = normalize('NFC', raw_names_ocr.strip())
normalized_name_list_ocr = normalized_raw_names_ocr.split('\n')

 
def get_accuracy(error, original):
    error = ['<s>'] + tokenize(preprocess(error)) + ['</s>']
    original = ['<s>'] + tokenize(preprocess(original)) + ['</s>']
    return neural_model.getNameAccuracy(original), neural_model.getNameAccuracy(error)

print('Starting OCR...')

difference = 0
negative_differences = 0
results = []
error_conunt = 0
preprocess_test_names = []
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
        except Exception as e:
            error_conunt += 1
            if( type(e).__name__ == 'KeyError'):
                preprocess_test_names.append(error_malith)
            # print("Exception: {}".format(type(e).__name__))
            # print("Exception message: {}".format(e))
            pass
    if(original != error_abhaya):
        try:
            error_name_accuracy, original_name_accuracy = get_accuracy(error_abhaya, original)
            norm_difference = (original_name_accuracy - error_name_accuracy)/original_name_accuracy
            difference += norm_difference
            if norm_difference<0:
                negative_differences+=1
            results.append({"original_name": original, "error_name": error_abhaya, "error_name_accuracy":error_name_accuracy, "original_name_accuracy": original_name_accuracy, "normalized_difference": norm_difference})
        except Exception as e:
            error_conunt += 1
            if( type(e).__name__ == 'KeyError'):
                preprocess_test_names.append(error_abhaya)
            # print("Exception: {}".format(type(e).__name__))
            # print("Exception message: {}".format(e))
            pass

with open(join(root_dirname, "result_evaluation_language_model_ocr_{batch_size}_{n_hidden}_{n_layers}.json"), "w", encoding='utf-8') as outfile:
    json.dump({"results": results, "final_socre": difference/(i + 1)}, outfile, ensure_ascii=False)

print('Starting confussion set...')

with open(join(root_dirname, "../error_data/probabilistic_edit_distance_errors/confussion_edit_distance_errors_.csv"), "r", encoding='utf-8') as f:
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
    except Exception as e:
        error_conunt += 1
        if( type(e).__name__ == 'KeyError'):
                preprocess_test_names.append(error)
        # print("Exception: {}".format(type(e).__name__))
        # print("Exception message: {}".format(e))
        pass

with open(join(root_dirname, f"result_evaluation_language_model_edit_distance_{batch_size}_{n_hidden}_{n_layers}.json"), "w", encoding='utf-8') as outfile:
    json.dump({"results": results, "final_socre": difference/(i + 1)}, outfile, ensure_ascii=False)

print('Finish')
# print(error_conunt)

# with open(join(root_dirname, f"preprocess_test_names_{batch_size}_{n_hidden}_{n_layers}.txt"), "w", encoding='utf-8') as outfile:
#     outfile.write('\n'.join(preprocess_test_names))
