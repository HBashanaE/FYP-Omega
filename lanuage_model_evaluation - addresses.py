from os.path import isfile, join, dirname, join
from os import listdir
from unicodedata import normalize
import json

from Spell_Checker.LanguageModel import NeuralLanguageModel
from Spell_Checker.utils import preprocess
from Spell_Checker.CharRNN import CharRNN

root_dirname = dirname(__file__)
batch_size = 1024
n_hidden = 4
n_layers = 2
# neural_model_path = join(
#     root_dirname, f'Language_Model/Neural_Language_Model/Saved_Models/neural-model-tokenized-{batch_size}-{n_hidden}-{n_layers}.pth')

neural_model_path = join(
    root_dirname, f'Language_Model/Neural_Language_Model/Saved_Models/neural-model-base-char.pth')

neural_model = NeuralLanguageModel(neural_model_path)

def tokenize(text):
    return list(text)

def get_accuracy(error, original):
    error = ['<s>'] + tokenize(preprocess(error)) + ['</s>']
    original = ['<s>'] + tokenize(preprocess(original)) + ['</s>']
    original_name_accuracy_avg, error_name_accuracy_avg = neural_model.getNameAccuracy(
        original), neural_model.getNameAccuracy(error)
    original_name_accuracy_mul, error_name_accuracy_mul = neural_model.getNameAccuracyMul(
        original), neural_model.getNameAccuracyMul(error)
    original_name_accuracy_log, error_name_accuracy_log = neural_model.getNameAccuracyLog(
        original), neural_model.getNameAccuracyLog(error)
    original_name_accuracy_exp, error_name_accuracy_exp = neural_model.getNameAccuracyExp(
        original), neural_model.getNameAccuracyExp(error)
    return error_name_accuracy_avg, original_name_accuracy_avg, error_name_accuracy_mul, original_name_accuracy_mul, error_name_accuracy_log, original_name_accuracy_log, error_name_accuracy_exp, original_name_accuracy_exp

error_conunt = 0
preprocess_test_names = []

################## Evaluate OCR Errors #############
print('Starting OCR...')

path = join(
    root_dirname, 'Data/Error_Data/ocr_error_data/Address error data/address OCR errors testing - 1.csv')

raw_names_ocr = open(join(path), encoding='utf-8').readlines()[1:]
raw_names_ocr = ''.join(raw_names_ocr)

normalized_raw_names_ocr = normalize('NFC', raw_names_ocr.strip())
normalized_name_list_ocr = normalized_raw_names_ocr.split('\n')

difference_avg = 0
difference_mul = 0
difference_log = 0
difference_exp = 0
positive_differences_avg = 0
positive_differences_mul = 0
positive_differences_log = 0
positive_differences_exp = 0
results = []
for i, line in enumerate(normalized_name_list_ocr[:1000]):
    original, error_malith, error_abhaya = line.split(',')

    if(original != error_malith):
        try:
            error_name_accuracy_avg, original_name_accuracy_avg, error_name_accuracy_mul, original_name_accuracy_mul, error_name_accuracy_log, original_name_accuracy_log, error_name_accuracy_exp, original_name_accuracy_exp = get_accuracy(
                error_malith, original)
            norm_difference_avg = (
                original_name_accuracy_avg - error_name_accuracy_avg)/original_name_accuracy_avg
            norm_difference_mul = (
                original_name_accuracy_mul - error_name_accuracy_mul)/original_name_accuracy_mul
            norm_difference_log = (
                original_name_accuracy_log - error_name_accuracy_log)/original_name_accuracy_log
            norm_difference_exp = (
                original_name_accuracy_exp - error_name_accuracy_exp)/original_name_accuracy_exp
            difference_avg += norm_difference_avg
            difference_mul += norm_difference_mul
            difference_log += norm_difference_log
            difference_exp += norm_difference_exp
            if norm_difference_avg > 0:
                positive_differences_avg += 1
            if norm_difference_mul > 0:
                positive_differences_mul += 1
            if norm_difference_log > 0:
                positive_differences_log += 1
            if norm_difference_exp > 0:
                positive_differences_exp += 1
            results.append({"original_name": original,
                            "error_name": error_malith,
                            "error_name_accuracy_avg": error_name_accuracy_avg,
                            "original_name_accuracy_avg": original_name_accuracy_avg,
                            "error_name_accuracy_mul": error_name_accuracy_mul,
                            "original_name_accuracy_mul": original_name_accuracy_mul,
                            "error_name_accuracy_log": error_name_accuracy_log,
                            "original_name_accuracy_log": original_name_accuracy_log,
                            "error_name_accuracy_exp": error_name_accuracy_exp,
                            "original_name_accuracy_exp": original_name_accuracy_exp,
                            "norm_difference_avg": norm_difference_avg,
                            "norm_difference_mul": norm_difference_mul,
                            "norm_difference_log": norm_difference_log,
                            "norm_difference_exp": norm_difference_exp
                            })
        except Exception as e:
            error_conunt += 1
            if(type(e).__name__ == 'KeyError'):
                preprocess_test_names.append(error_malith)
            pass
    if(original != error_abhaya):
        try:
            error_name_accuracy_avg, original_name_accuracy_avg, error_name_accuracy_mul, original_name_accuracy_mul, error_name_accuracy_log, original_name_accuracy_log, error_name_accuracy_exp, original_name_accuracy_exp = get_accuracy(
                error_malith, original)
            norm_difference_avg = (
                original_name_accuracy_avg - error_name_accuracy_avg)/original_name_accuracy_avg
            norm_difference_mul = (
                original_name_accuracy_mul - error_name_accuracy_mul)/original_name_accuracy_mul
            norm_difference_log = (
                original_name_accuracy_log - error_name_accuracy_log)/original_name_accuracy_log
            norm_difference_exp = (
                original_name_accuracy_exp - error_name_accuracy_exp)/original_name_accuracy_exp
            difference_avg += norm_difference_avg
            difference_mul += norm_difference_mul
            difference_log += norm_difference_log
            difference_exp += norm_difference_exp
            if norm_difference_avg > 0:
                positive_differences_avg += 1
            if norm_difference_mul > 0:
                positive_differences_mul += 1
            if norm_difference_log > 0:
                positive_differences_log += 1
            if norm_difference_exp > 0:
                positive_differences_exp += 1
            results.append({"original_name": original,
                            "error_name": error_malith,
                            "error_name_accuracy_avg": error_name_accuracy_avg,
                            "original_name_accuracy_avg": original_name_accuracy_avg,
                            "error_name_accuracy_mul": error_name_accuracy_mul,
                            "original_name_accuracy_mul": original_name_accuracy_mul,
                            "error_name_accuracy_log": error_name_accuracy_log,
                            "original_name_accuracy_log": original_name_accuracy_log,
                            "error_name_accuracy_exp": error_name_accuracy_exp,
                            "original_name_accuracy_exp": original_name_accuracy_exp,
                            "norm_difference_avg": norm_difference_avg,
                            "norm_difference_mul": norm_difference_mul,
                            "norm_difference_log": norm_difference_log,
                            "norm_difference_exp": norm_difference_exp
                            })
        except Exception as e:
            error_conunt += 1
            if(type(e).__name__ == 'KeyError'):
                preprocess_test_names.append(error_abhaya)
            pass

with open(join(root_dirname, f"result_evaluation_language_model_ocr_base-address.json"), "w", encoding='utf-8') as outfile:
    json.dump({
                # "results": results,
               "final_socre": {
                   "difference_avg": difference_avg/(i + 1),
                   "difference_mul": difference_mul/(i + 1),
                   "difference_log": difference_log/(i + 1),
                   "difference_exp": difference_exp/(i + 1),
                   "positive_differences_avg": positive_differences_avg/(i + 1),
                   "positive_differences_mul": positive_differences_mul/(i + 1),
                   "positive_differences_log": positive_differences_log/(i + 1),
                   "positive_differences_exp": positive_differences_exp/(i + 1)

               }}, outfile, ensure_ascii=False)


################## Evaluate Statistical Errors #############
print('Starting confussion set...')

with open(join(root_dirname, "Data/Error_Data/probabilistic_edit_distance_errors/confussion_edit_distance_errors_addresses.csv"), "r", encoding='utf-8') as f:
    raw_names_confussion_edit_distance = f.readlines()[1:]
raw_names_confussion_edit_distance = ''.join(
    raw_names_confussion_edit_distance)

normalized_raw_names_edit_distance = normalize(
    'NFC', raw_names_confussion_edit_distance.strip())
normalized_name_list_edit_distance = normalized_raw_names_edit_distance.split(
    '\n')

difference_avg = 0
difference_mul = 0
difference_log = 0
difference_exp = 0
positive_differences_avg = 0
positive_differences_mul = 0
positive_differences_log = 0
positive_differences_exp = 0
results = []
for i, line in enumerate(normalized_name_list_edit_distance[:1000]):
    original, error = line.split(',')
    try:
        error_name_accuracy_avg, original_name_accuracy_avg, error_name_accuracy_mul, original_name_accuracy_mul, error_name_accuracy_log, original_name_accuracy_log, error_name_accuracy_exp, original_name_accuracy_exp = get_accuracy(
            error, original)
        norm_difference_avg = (
            original_name_accuracy_avg - error_name_accuracy_avg)/original_name_accuracy_avg
        norm_difference_mul = (
            original_name_accuracy_mul - error_name_accuracy_mul)/original_name_accuracy_mul
        norm_difference_log = (
            original_name_accuracy_log - error_name_accuracy_log)/original_name_accuracy_log
        norm_difference_exp = (
            original_name_accuracy_exp - error_name_accuracy_exp)/original_name_accuracy_exp
        difference_avg += norm_difference_avg
        difference_mul += norm_difference_mul
        difference_log += norm_difference_log
        difference_exp += norm_difference_exp

        if norm_difference_avg > 0:
            positive_differences_avg += 1
        if norm_difference_mul > 0:
            positive_differences_mul += 1
        if norm_difference_log > 0:
            positive_differences_log += 1
        if norm_difference_exp > 0:
            positive_differences_exp += 1

        results.append({"original_name": original,
                        "error_name": error,
                        "error_name_accuracy_avg": error_name_accuracy_avg,
                        "original_name_accuracy_avg": original_name_accuracy_avg,
                        "error_name_accuracy_mul": error_name_accuracy_mul,
                        "original_name_accuracy_mul": original_name_accuracy_mul,
                        "error_name_accuracy_log": error_name_accuracy_log,
                        "original_name_accuracy_log": original_name_accuracy_log,
                        "error_name_accuracy_exp": error_name_accuracy_exp,
                        "original_name_accuracy_exp": original_name_accuracy_exp,
                        "norm_difference_avg": norm_difference_avg,
                        "norm_difference_mul": norm_difference_mul,
                        "norm_difference_log": norm_difference_log,
                        "norm_difference_exp": norm_difference_exp
                        })
    except Exception as e:
        error_conunt += 1
        if(type(e).__name__ == 'KeyError'):
            preprocess_test_names.append(error)
        # print("Exception: {}".format(type(e).__name__))
        # print("Exception message: {}".format(e))
        pass

with open(join(root_dirname, f"result_evaluation_language_model_edit_distance_base-address.json"), "w", encoding='utf-8') as outfile:
    json.dump({
                # "results": results,
               "final_socre": {
                   "difference_avg": difference_avg/(i + 1),
                   "difference_mul": difference_mul/(i + 1),
                   "difference_log": difference_log/(i + 1),
                   "difference_exp": difference_exp/(i + 1),
                   "positive_differences_avg": positive_differences_avg/(i + 1),
                   "positive_differences_mul": positive_differences_mul/(i + 1),
                   "positive_differences_log": positive_differences_log/(i + 1),
                   "positive_differences_exp": positive_differences_exp/(i + 1)

               }}, outfile, ensure_ascii=False)


################## Evaluate Random Errors #############
print('Random...')

with open(join(root_dirname, "Data/Error_Data/random_error_data/addresses Random errors.csv"), "r", encoding='utf-8') as f:
    raw_names_random = f.readlines()[1:]
raw_names_random = ''.join(
    raw_names_random)

normalized_names_random = normalize(
    'NFC', raw_names_random.strip())
normalized_name_list_random = normalized_names_random.split(
    '\n')

difference_avg = 0
difference_mul = 0
difference_log = 0
difference_exp = 0
positive_differences_avg = 0
positive_differences_mul = 0
positive_differences_log = 0
positive_differences_exp = 0
results = []
for i, line in enumerate(normalized_name_list_random[:1000]):
    if(len(line.split(',')) != 2):
        continue
    original, error = line.split(',')
    try:
        error_name_accuracy_avg, original_name_accuracy_avg, error_name_accuracy_mul, original_name_accuracy_mul, error_name_accuracy_log, original_name_accuracy_log, error_name_accuracy_exp, original_name_accuracy_exp = get_accuracy(
            error, original)
        norm_difference_avg = (
            original_name_accuracy_avg - error_name_accuracy_avg)/original_name_accuracy_avg
        norm_difference_mul = (
            original_name_accuracy_mul - error_name_accuracy_mul)/original_name_accuracy_mul
        norm_difference_log = (
            original_name_accuracy_log - error_name_accuracy_log)/original_name_accuracy_log
        norm_difference_exp = (
            original_name_accuracy_exp - error_name_accuracy_exp)/original_name_accuracy_exp
        difference_avg += norm_difference_avg
        difference_mul += norm_difference_mul
        difference_log += norm_difference_log
        difference_exp += norm_difference_exp

        if norm_difference_avg > 0:
            positive_differences_avg += 1
        if norm_difference_mul > 0:
            positive_differences_mul += 1
        if norm_difference_log > 0:
            positive_differences_log += 1
        if norm_difference_exp > 0:
            positive_differences_exp += 1

        results.append({"original_name": original,
                        "error_name": error,
                        "error_name_accuracy_avg": error_name_accuracy_avg,
                        "original_name_accuracy_avg": original_name_accuracy_avg,
                        "error_name_accuracy_mul": error_name_accuracy_mul,
                        "original_name_accuracy_mul": original_name_accuracy_mul,
                        "error_name_accuracy_log": error_name_accuracy_log,
                        "original_name_accuracy_log": original_name_accuracy_log,
                        "error_name_accuracy_exp": error_name_accuracy_exp,
                        "original_name_accuracy_exp": original_name_accuracy_exp,
                        "norm_difference_avg": norm_difference_avg,
                        "norm_difference_mul": norm_difference_mul,
                        "norm_difference_log": norm_difference_log,
                        "norm_difference_exp": norm_difference_exp
                        })
    except Exception as e:
        error_conunt += 1
        if(type(e).__name__ == 'KeyError'):
            preprocess_test_names.append(error)
        pass

with open(join(root_dirname, f"result_evaluation_language_model_random_base-address.json"), "w", encoding='utf-8') as outfile:
    json.dump({
                # "results": results,
               "final_socre": {
                   "difference_avg": difference_avg/(i + 1),
                   "difference_mul": difference_mul/(i + 1),
                   "difference_log": difference_log/(i + 1),
                   "difference_exp": difference_exp/(i + 1),
                   "positive_differences_avg": positive_differences_avg/(i + 1),
                   "positive_differences_mul": positive_differences_mul/(i + 1),
                   "positive_differences_log": positive_differences_log/(i + 1),
                   "positive_differences_exp": positive_differences_exp/(i + 1)

               }}, outfile, ensure_ascii=False)

print('Finish')