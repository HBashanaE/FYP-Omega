from unicodedata import normalize
from tokenizer import tokenize
import re

filePath = r'D:/Final Year Project/Data/names-utf8.txt'
names = open(filePath, 'r', encoding='utf-8').read()

names = re.split(' |\n',names.strip())

names = [normalize('NFD', name.strip()) for name in names]
# uniqueNames = sorted(list(set(names)))


cleanedNames = []

for line in names:
    if(len(line) < 2):
            continue
    if(len(tokenize(line)) < 3):
            continue
    line = line.replace('fප', 'ෆ')
    line = line.replace('Fප', 'ෆ')
    for name in line.split('.'):
        cleanedName = ''
        for character in name:
            cleanedName += character if( 3456 < ord(character) < 3583 or character == '\u200d' ) else ''
        if(len(cleanedName) < 2):
            continue
        if(len(tokenize(cleanedName)) < 3):
            continue
        cleanedNames.append(cleanedName)

filePath = r'D:\Final Year Project\Data\Cleaned data\initial dataset - cleaned.txt'
open(filePath, 'w', encoding='utf-8').write('\n'.join(cleanedNames))