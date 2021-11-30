from os.path import isfile, join, dirname, join
from os import listdir
from unicodedata import normalize
import json

from utils import tokenize, preprocess

from CharRNN import CharRNN
from LanguageModel import NeuralLanguageModel

root_dirname = dirname(__file__)
batch_size = 1024
n_hidden = 4
n_layers = 2
neural_model_path = join(
    root_dirname, f'../Data/neural-model-tokenized-{batch_size}-{n_hidden}-{n_layers}.pth')

neural_model = NeuralLanguageModel(neural_model_path)

path = join(
    root_dirname, '../error_data/ocr_error_data/OCR errors testing')
files = [f for f in listdir(path) if isfile(join(path, f))]

raw_names_ocr = []
for file in files:
    raw_names_ocr += open(join(path, file), encoding='utf-8').readlines()[1:]
raw_names_ocr = ''.join(raw_names_ocr)

normalized_raw_names_ocr = normalize('NFC', raw_names_ocr.strip())
normalized_name_list_ocr = normalized_raw_names_ocr.split('\n')


def get_accuracy(error, original):
    error = ['<s>'] + tokenize(preprocess(error)) + ['</s>']
    original = ['<s>'] + tokenize(preprocess(original)) + ['</s>']
    error_name_accuracy_avg, original_name_accuracy_avg = neural_model.getNameAccuracy(
        original), neural_model.getNameAccuracy(error)
    error_name_accuracy_mul, original_name_accuracy_mul = neural_model.getNameAccuracyMul(
        original), neural_model.getNameAccuracyMul(error)
    error_name_accuracy_log, original_name_accuracy_log = neural_model.getNameAccuracyLog(
        original), neural_model.getNameAccuracyLog(error)
    error_name_accuracy_exp, original_name_accuracy_exp = neural_model.getNameAccuracyExp(
        original), neural_model.getNameAccuracyExp(error)
    return error_name_accuracy_avg, original_name_accuracy_avg, error_name_accuracy_mul, original_name_accuracy_mul, error_name_accuracy_log, original_name_accuracy_log, error_name_accuracy_exp, original_name_accuracy_exp


################## Evaluate OCR Errors #############
print('Starting OCR...')

difference_avg = 0
difference_mul = 0
difference_log = 0
difference_exp = 0
negative_differences_avg = 0
negative_differences_mul = 0
negative_differences_log = 0
negative_differences_exp = 0
results = []
error_conunt = 0
preprocess_test_names = []
for i, line in enumerate(normalized_name_list_ocr[:100]):
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
            if norm_difference_avg < 0:
                negative_differences_avg += 1
            if norm_difference_mul < 0:
                negative_differences_mul += 1
            if norm_difference_log < 0:
                negative_differences_log += 1
            if norm_difference_exp < 0:
                negative_differences_exp += 1
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
            # print("Exception: {}".format(type(e).__name__))
            # print("Exception message: {}".format(e))
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
            if norm_difference_avg < 0:
                negative_differences_avg += 1
            if norm_difference_mul < 0:
                negative_differences_mul += 1
            if norm_difference_log < 0:
                negative_differences_log += 1
            if norm_difference_exp < 0:
                negative_differences_exp += 1
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
            # print("Exception: {}".format(type(e).__name__))
            # print("Exception message: {}".format(e))
            pass

with open(join(root_dirname, f"result_evaluation_language_model_ocr_{batch_size}_{n_hidden}_{n_layers}.json"), "w", encoding='utf-8') as outfile:
    json.dump({"results": results,
               "final_socre": {
                   "difference_avg": difference_avg/(i + 1),
                   "difference_mul": difference_mul/(i + 1),
                   "difference_log": difference_log/(i + 1),
                   "difference_exp": difference_exp/(i + 1),
                   "negative_differences_avg": negative_differences_avg/(i + 1),
                   "negative_differences_mul": negative_differences_mul/(i + 1),
                   "negative_differences_log": negative_differences_log/(i + 1),
                   "negative_differences_exp": negative_differences_exp/(i + 1)

               }}, outfile, ensure_ascii=False)


################## Evaluate Statistical Errors #############
print('Starting confussion set...')

with open(join(root_dirname, "../error_data/probabilistic_edit_distance_errors/confussion_edit_distance_errors_.csv"), "r", encoding='utf-8') as f:
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
negative_differences_avg = 0
negative_differences_mul = 0
negative_differences_log = 0
negative_differences_exp = 0
results = []
for i, line in enumerate(normalized_name_list_edit_distance[:100]):
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

        if norm_difference_avg < 0:
            negative_differences_avg += 1
        if norm_difference_mul < 0:
            negative_differences_mul += 1
        if norm_difference_log < 0:
            negative_differences_log += 1
        if norm_difference_exp < 0:
            negative_differences_exp += 1

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
            preprocess_test_names.append(error)
        # print("Exception: {}".format(type(e).__name__))
        # print("Exception message: {}".format(e))
        pass

with open(join(root_dirname, f"result_evaluation_language_model_edit_distance_{batch_size}_{n_hidden}_{n_layers}.json"), "w", encoding='utf-8') as outfile:
    json.dump({"results": results,
               "final_socre": {
                   "difference_avg": difference_avg/(i + 1),
                   "difference_mul": difference_mul/(i + 1),
                   "difference_log": difference_log/(i + 1),
                   "difference_exp": difference_exp/(i + 1),
                   "negative_differences_avg": negative_differences_avg/(i + 1),
                   "negative_differences_mul": negative_differences_mul/(i + 1),
                   "negative_differences_log": negative_differences_log/(i + 1),
                   "negative_differences_exp": negative_differences_exp/(i + 1)

               }}, outfile, ensure_ascii=False)


################## Evaluate Random Errors #############
print('Random...')

with open(join(root_dirname, "../error_data/random_error_data/Random errors.csv"), "r", encoding='utf-8') as f:
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
negative_differences_avg = 0
negative_differences_mul = 0
negative_differences_log = 0
negative_differences_exp = 0
results = []
for i, line in enumerate(normalized_name_list_random[:100]):
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

        if norm_difference_avg < 0:
            negative_differences_avg += 1
        if norm_difference_mul < 0:
            negative_differences_mul += 1
        if norm_difference_log < 0:
            negative_differences_log += 1
        if norm_difference_exp < 0:
            negative_differences_exp += 1

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
            preprocess_test_names.append(error)
        # print("Exception: {}".format(type(e).__name__))
        # print("Exception message: {}".format(e))
        pass

with open(join(root_dirname, f"result_evaluation_language_model_random_{batch_size}_{n_hidden}_{n_layers}.json"), "w", encoding='utf-8') as outfile:
    json.dump({"results": results,
               "final_socre": {
                   "difference_avg": difference_avg/(i + 1),
                   "difference_mul": difference_mul/(i + 1),
                   "difference_log": difference_log/(i + 1),
                   "difference_exp": difference_exp/(i + 1),
                   "negative_differences_avg": negative_differences_avg/(i + 1),
                   "negative_differences_mul": negative_differences_mul/(i + 1),
                   "negative_differences_log": negative_differences_log/(i + 1),
                   "negative_differences_exp": negative_differences_exp/(i + 1)

               }}, outfile, ensure_ascii=False)

print('Finish')
# print(error_conunt)

# with open(join(root_dirname, f"preprocess_test_names_{batch_size}_{n_hidden}_{n_layers}.txt"), "w", encoding='utf-8') as outfile:
#     outfile.write('\n'.join(preprocess_test_names))
