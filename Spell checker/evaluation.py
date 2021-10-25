from os.path import isfile, join, dirname, join
from os import listdir
from unicodedata import normalize
from CharRNN import CharRNN
from driver import spellChecker


dirname = dirname(__file__)

path = join(
    dirname, '../Error data/OCR Error Data/OCR error training')
files = [f for f in listdir(path) if isfile(join(path, f))]

raw_names = []
for file in files:
  raw_names +=  open(join(path, file), encoding='utf-8').readlines()[1:]
raw_names = ''.join(raw_names)

normalized_raw_names = normalize('NFC', raw_names.strip())
normalized_name_list = normalized_raw_names.split('\n')

corrected = 0
not_corrected = 0

for line in normalized_name_list:
    original, error_malith, error_abhaya = line.split(',')
    if(original != error_malith):
        try:
            suggestions = spellChecker.correctSpelling(error_malith)
            if(any(original == s[1] for s in suggestions)):
                corrected += 1
            else:
                not_corrected += 1
        except:
            pass
    if(original != error_abhaya):
        try:
            suggestions = spellChecker.correctSpelling(error_abhaya)
            if(any(original == s[1] for s in suggestions)):
                corrected += 1
            else:
                not_corrected += 1
        except:
            pass

print(corrected, not_corrected)