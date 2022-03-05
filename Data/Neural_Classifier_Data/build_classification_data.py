from os.path import isfile, join, dirname, join
from os import listdir
import pandas as pd
from sklearn.model_selection import train_test_split
from io import StringIO

from preprocess import preprocess

root_dirname = dirname(__file__)

training_path = join(
    root_dirname, '../Error_Data/ocr_error_data/OCR error training')

df_raw_names_ocr_training = [pd.read_csv(join(training_path, file)) for file in listdir(training_path) if isfile(join(training_path, file))]
df_raw_names_ocr_training = pd.concat(df_raw_names_ocr_training, axis=0)
df_raw_names_ocr_training.reset_index(inplace=True, drop=True)

content = 'name,label\n'
for index, row in df_raw_names_ocr_training.iterrows():
    original = row['original']
    error_malith = row['Malith']
    error_abhaya = row['Abhaya']
    preprocessed_original = preprocess(original)
    preprocessed_error_malith = preprocess(error_malith)
    preprocessed_error_abhaya = preprocess(error_abhaya)
    content += f'{original},1\n'
    if(preprocessed_original != preprocessed_error_malith):
        content += f'{error_malith},0\n'
    if(preprocessed_original != preprocessed_error_abhaya):
        content += f'{error_abhaya},0\n'
train_valid_ratio = 0.9
df_raw = pd.read_csv(StringIO(content))

df_correct = df_raw[df_raw['label'] == 1]
df_error = df_raw[df_raw['label'] == 0]

df_correct_train, df_correct_valid = train_test_split(df_correct, train_size = train_valid_ratio, random_state = 1)
df_error_train, df_error_valid = train_test_split(df_error, train_size = train_valid_ratio, random_state = 1)

df_train = pd.concat([df_correct_train, df_error_train], ignore_index=True, sort=False)
df_valid = pd.concat([df_correct_valid, df_error_valid], ignore_index=True, sort=False)

df_train.to_csv(join(root_dirname , 'Train', 'classification_training_names.csv'), encoding='utf-8', index=False)
df_valid.to_csv(join(root_dirname , 'Train', 'classification_validation_names.csv'), encoding='utf-8', index=False)

testing_path = join(
    root_dirname, '../Error_Data/ocr_error_data/OCR errors testing')

df_raw_names_ocr_testing = [pd.read_csv(join(testing_path, file)) for file in listdir(testing_path) if isfile(join(testing_path, file))]
df_raw_names_ocr_testing = pd.concat(df_raw_names_ocr_testing, axis=0)
df_raw_names_ocr_testing.reset_index(inplace=True, drop=True)

content = 'name,label\n'
for index, row in df_raw_names_ocr_testing.iterrows():
    try:
        original = row['original']
        error_malith = row['Malith']
        error_abhaya = row['Abhaya']
        preprocessed_original = preprocess(original)
        preprocessed_error_malith = preprocess(error_malith)
        preprocessed_error_abhaya = preprocess(error_abhaya)
        content += f'{original},1\n'
        if(preprocessed_original != preprocessed_error_malith):
            content += f'{error_malith},0\n'
        if(preprocessed_original != preprocessed_error_abhaya):
            content += f'{error_abhaya},0\n'
    except:
        print(row)

open(join(root_dirname , 'Test', 'classification_testing_names.csv'), 'w', encoding='utf-8').write(content)