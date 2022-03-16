from os.path import isfile, join, dirname, join
from os import listdir
from unicodedata import normalize
import json

from Spell_Checker.utils import tokenize_base, tokenize_full, preprocess

from Spell_Checker.CharRNN import CharRNN
from Spell_Checker.LanguageModel import StatisticalLanguageModel, NeuralLanguageModel
root_dirname = '/'.join(dirname(__file__).split('\\')[:-1])
batch_size = 1024
n_hidden = 4
n_layers = 2
full_neural_model_path = join(
    root_dirname, f'Language_Model/Neural_Language_Model/Saved_Models/neural-model-tokenized-{batch_size}-{n_hidden}-{n_layers}.pth')
base_neural_model_path = join(
    root_dirname, f'Language_Model/Neural_Language_Model/Saved_Models/neural-model-base-char.pth')
ngram_model_path = join(
    root_dirname, 'Language_Model/Ngram_Model/address - kn3.pickle')
print(ngram_model_path)

tok = 0 # base - 0 | full - 1
mod = 1 # stat - 0 | neu - 1

selected_model = NeuralLanguageModel(full_neural_model_path)
# selected_model = StatisticalLanguageModel(ngram_model_path)

path = join(
    root_dirname, 'Data/Error_Data/ocr_error_data/OCR errors testing')
files = [f for f in listdir(path) if isfile(join(path, f))]

raw_names_ocr = []
for file in files:
    raw_names_ocr += open(join(path, file), encoding='utf-8').readlines()[1:]
raw_names_ocr = ''.join(raw_names_ocr)

normalized_raw_names_ocr = normalize('NFC', raw_names_ocr.strip())
normalized_name_list_ocr = normalized_raw_names_ocr.split('\n')

def full_tokenize(text):
    return tokenize_full(preprocess(text))

output_suffix = ''
if(tok == 0):
    output_suffix = f'base_{"stat" if mod == 0 else "neural" }'
    tokenize = tokenize_base
    selected_model = StatisticalLanguageModel(ngram_model_path) if mod == 0 else NeuralLanguageModel(base_neural_model_path)
else:
    output_suffix = f'full_{"stat" if mod == 0 else "neural" }'
    tokenize = full_tokenize
    selected_model = StatisticalLanguageModel(ngram_model_path) if mod == 0 else NeuralLanguageModel(full_neural_model_path)


def get_accuracy(error, original):
    error = ['<s>'] + tokenize(error) + ['</s>']
    original = ['<s>'] + tokenize(original) + ['</s>']
    original_name_accuracy_avg, error_name_accuracy_avg = selected_model.getNameAccuracy(
        original), selected_model.getNameAccuracy(error)
    original_name_accuracy_mul, error_name_accuracy_mul = selected_model.getNameAccuracyMul(
        original), selected_model.getNameAccuracyMul(error)
    original_name_accuracy_log, error_name_accuracy_log = selected_model.getNameAccuracyLog(
        original), selected_model.getNameAccuracyLog(error)
    original_name_accuracy_exp, error_name_accuracy_exp = selected_model.getNameAccuracyExp(
        original), selected_model.getNameAccuracyExp(error)
    return (error_name_accuracy_avg, original_name_accuracy_avg,
            error_name_accuracy_mul, original_name_accuracy_mul,
            error_name_accuracy_log, original_name_accuracy_log,
            error_name_accuracy_exp, original_name_accuracy_exp)


def get_difference(error, original):
    error_name_accuracy_avg, original_name_accuracy_avg, error_name_accuracy_mul, original_name_accuracy_mul, error_name_accuracy_log, original_name_accuracy_log, error_name_accuracy_exp, original_name_accuracy_exp = get_accuracy(
        error, original)
    norm_difference_avg = (
        original_name_accuracy_avg - error_name_accuracy_avg)/abs(original_name_accuracy_avg)
    norm_difference_mul = (
        original_name_accuracy_mul - error_name_accuracy_mul)/abs(original_name_accuracy_mul)
    norm_difference_log = (
        original_name_accuracy_log - error_name_accuracy_log)/abs(original_name_accuracy_log)
    norm_difference_exp = (
        original_name_accuracy_exp - error_name_accuracy_exp)/abs(original_name_accuracy_exp)

    return (norm_difference_avg, norm_difference_mul, norm_difference_log, norm_difference_exp)


################## Evaluate OCR Errors #############
print('Starting OCR...')

difference_avg = 0
difference_mul = 0
difference_log = 0
difference_exp = 0
positive_differences_avg = 0
positive_differences_mul = 0
positive_differences_log = 0
positive_differences_exp = 0
results = []
error_conunt = 0
preprocess_test_names = []
count = 0
for i, line in enumerate(normalized_name_list_ocr[:1000]):
    original, error_malith, error_abhaya = line.split(',')

    if(original != error_malith):
        try:
            (norm_difference_avg, norm_difference_mul, norm_difference_log,
             norm_difference_exp) = get_difference(error_malith, original)
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
            # results.append({"original_name": original,
            #                 "error_name": error_malith,
            #                 "error_name_accuracy_avg": error_name_accuracy_avg,
            #                 "original_name_accuracy_avg": original_name_accuracy_avg,
            #                 "error_name_accuracy_mul": error_name_accuracy_mul,
            #                 "original_name_accuracy_mul": original_name_accuracy_mul,
            #                 "error_name_accuracy_log": error_name_accuracy_log,
            #                 "original_name_accuracy_log": original_name_accuracy_log,
            #                 "error_name_accuracy_exp": error_name_accuracy_exp,
            #                 "original_name_accuracy_exp": original_name_accuracy_exp,
            #                 "norm_difference_avg": norm_difference_avg,
            #                 "norm_difference_mul": norm_difference_mul,
            #                 "norm_difference_log": norm_difference_log,
            #                 "norm_difference_exp": norm_difference_exp
            #                 })
            count += 1
        except Exception as e:
            error_conunt += 1
            if(type(e).__name__ == 'KeyError'):
                preprocess_test_names.append(error_malith)
            # print("Exception: {}".format(type(e).__name__))
            # print("Exception message: {}".format(e))
            pass
    if(original != error_abhaya):
        try:
            (norm_difference_avg, norm_difference_mul, norm_difference_log,
             norm_difference_exp) = get_difference(error_abhaya, original)
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
            # results.append({"original_name": original,
            #                 "error_name": error_malith,
            #                 "error_name_accuracy_avg": error_name_accuracy_avg,
            #                 "original_name_accuracy_avg": original_name_accuracy_avg,
            #                 "error_name_accuracy_mul": error_name_accuracy_mul,
            #                 "original_name_accuracy_mul": original_name_accuracy_mul,
            #                 "error_name_accuracy_log": error_name_accuracy_log,
            #                 "original_name_accuracy_log": original_name_accuracy_log,
            #                 "error_name_accuracy_exp": error_name_accuracy_exp,
            #                 "original_name_accuracy_exp": original_name_accuracy_exp,
            #                 "norm_difference_avg": norm_difference_avg,
            #                 "norm_difference_mul": norm_difference_mul,
            #                 "norm_difference_log": norm_difference_log,
            #                 "norm_difference_exp": norm_difference_exp
            #                 })
            count += 1
        except Exception as e:
            error_conunt += 1
            if(type(e).__name__ == 'KeyError'):
                preprocess_test_names.append(error_abhaya)
            # print("Exception: {}".format(type(e).__name__))
            # print("Exception message: {}".format(e))
            pass

with open(join(root_dirname, 'eval_results', f"result_evaluation_language_model_{output_suffix}_ocr.json"), "w", encoding='utf-8') as outfile:
    json.dump({
                # "results": results,
               "final_socre": {
                   "difference_avg": difference_avg/(count + 1),
                   "difference_mul": difference_mul/(count + 1),
                   "difference_log": difference_log/(count + 1),
                   "difference_exp": difference_exp/(count + 1),
                   "positive_differences_avg": positive_differences_avg/(count + 1),
                   "positive_differences_mul": positive_differences_mul/(count + 1),
                   "positive_differences_log": positive_differences_log/(count + 1),
                   "positive_differences_exp": positive_differences_exp/(count + 1)

               }}, outfile, ensure_ascii=False)


################## Evaluate Statistical Errors #############
print('Starting confussion set...')

with open(join(root_dirname, "Data/Error_Data/probabilistic_edit_distance_errors/confussion_edit_distance_errors_.csv"), "r", encoding='utf-8') as f:
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
        (norm_difference_avg, norm_difference_mul, norm_difference_log,
             norm_difference_exp) = get_difference(error, original)
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

        # results.append({"original_name": original,
        #                 "error_name": error_malith,
        #                 "error_name_accuracy_avg": error_name_accuracy_avg,
        #                 "original_name_accuracy_avg": original_name_accuracy_avg,
        #                 "error_name_accuracy_mul": error_name_accuracy_mul,
        #                 "original_name_accuracy_mul": original_name_accuracy_mul,
        #                 "error_name_accuracy_log": error_name_accuracy_log,
        #                 "original_name_accuracy_log": original_name_accuracy_log,
        #                 "error_name_accuracy_exp": error_name_accuracy_exp,
        #                 "original_name_accuracy_exp": original_name_accuracy_exp,
        #                 "norm_difference_avg": norm_difference_avg,
        #                 "norm_difference_mul": norm_difference_mul,
        #                 "norm_difference_log": norm_difference_log,
        #                 "norm_difference_exp": norm_difference_exp
        #                 })
    except Exception as e:
        error_conunt += 1
        if(type(e).__name__ == 'KeyError'):
            preprocess_test_names.append(error)
        # print("Exception: {}".format(type(e).__name__))
        # print("Exception message: {}".format(e))
        pass

with open(join(root_dirname, 'eval_results', f"result_evaluation_language_model_{output_suffix}_edit_distance.json"), "w", encoding='utf-8') as outfile:
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

with open(join(root_dirname, "Data/Error_Data/random_error_data/Random errors.csv"), "r", encoding='utf-8') as f:
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
count = 0
for i, line in enumerate(normalized_name_list_random[:1000]):
    if(len(line.split(',')) != 2):
        continue
    original, error = line.split(',')
    try:
        (norm_difference_avg, norm_difference_mul, norm_difference_log,
             norm_difference_exp) = get_difference(error, original)
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

        # results.append({"original_name": original,
        #                 "error_name": error_malith,
        #                 "error_name_accuracy_avg": error_name_accuracy_avg,
        #                 "original_name_accuracy_avg": original_name_accuracy_avg,
        #                 "error_name_accuracy_mul": error_name_accuracy_mul,
        #                 "original_name_accuracy_mul": original_name_accuracy_mul,
        #                 "error_name_accuracy_log": error_name_accuracy_log,
        #                 "original_name_accuracy_log": original_name_accuracy_log,
        #                 "error_name_accuracy_exp": error_name_accuracy_exp,
        #                 "original_name_accuracy_exp": original_name_accuracy_exp,
        #                 "norm_difference_avg": norm_difference_avg,
        #                 "norm_difference_mul": norm_difference_mul,
        #                 "norm_difference_log": norm_difference_log,
        #                 "norm_difference_exp": norm_difference_exp
        #                 })
        count += 1
    except Exception as e:
        error_conunt += 1
        if(type(e).__name__ == 'KeyError'):
            preprocess_test_names.append(error)
        # print("Exception: {}".format(type(e).__name__))
        # print("Exception message: {}".format(e))
        pass

with open(join(root_dirname, 'eval_results', f"result_evaluation_language_model_{output_suffix}_random.json"), "w", encoding='utf-8') as outfile:
    json.dump({
                # "results": results,
               "final_socre": {
                   "difference_avg": difference_avg/(count + 1),
                   "difference_mul": difference_mul/(count + 1),
                   "difference_log": difference_log/(count + 1),
                   "difference_exp": difference_exp/(count + 1),
                   "positive_differences_avg": positive_differences_avg/(count + 1),
                   "positive_differences_mul": positive_differences_mul/(count + 1),
                   "positive_differences_log": positive_differences_log/(count + 1),
                   "positive_differences_exp": positive_differences_exp/(count + 1)

               }}, outfile, ensure_ascii=False)

print('Finish')
