from os.path import isfile, join, dirname, join
from os import listdir

from utils import tokenize, preprocess

root_dirname = dirname(__file__)
path = join(
    root_dirname, '../error_data/ocr_error_data/OCR error training')
files = [f for f in listdir(path) if isfile(join(path, f))]

raw_names_ocr = []
for file in files:
    raw_names_ocr += open(join(path, file), encoding='utf-8').readlines()[1:]
raw_names_ocr = ''.join(raw_names_ocr)

name_list_ocr = raw_names_ocr.split('\n')

content = 'name,label\n'
for i, line in enumerate(name_list_ocr[:50000]):
    original, error_malith, error_abhaya = line.split(',')
    content += f'{original},1\n'
    if(original != error_malith):
        content += f'{error_malith},0\n'
    if(original != error_abhaya):
        content += f'{error_abhaya},0\n'

open(join(root_dirname, 'names_labels_training.csv'), 'w', encoding='utf-8').write(content)