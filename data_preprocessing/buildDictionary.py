from collections import Counter
import json

def buildDictionary(sourcePath, destinationPath, train=True):
    allNames = open(sourcePath, 'r', encoding='utf-8').read().split('\n')
    nameDictionary = Counter(allNames)
    with open(destinationPath, 'w', encoding='utf-8') as outfile:
        json.dump(nameDictionary, outfile, ensure_ascii=False)

buildDictionary(r'D:\Final Year Project\Codes\FYP-Omega\Data\combined all names - cleaned - train.txt', r'D:\Final Year Project\Codes\FYP-Omega\Data\combined all names - dictionary - train.json')