from unicodedata import normalize
from os import error
import requests
import json

userName = input('Enter username: ')
password = input('Enter password: ')

proxies = {
    "http": f"http://{userName}:{password}@cache2.uom.lk:3128/"
}

path = r'D:\Final Year Project\Data\Error data\OCR errors training - 1.csv'
## Read names
raw_names = open(path, 'r', encoding='utf-8').read()

## Normalize - Canonical Decomposition, followed by Canonical Composition
normalized_raw_names = normalize('NFC', raw_names.strip())

## Get name list
normalized_name_list = normalized_raw_names.split('\n')[1:]

correctCount = 0
incorrectCount = 0

for line in normalized_name_list[:5]:
 
    original, error_malith, error_abhaya = line.split(',')
    print(original, error_malith, error_abhaya)
    r_malith = requests.get(f"http://helabasa.projects.uom.lk/morphy/fasttext/execute?word={error_malith}", proxies=proxies)
    r_abhaya = requests.get(f"http://helabasa.projects.uom.lk/morphy/fasttext/execute?word={error_malith}", proxies=proxies)
    try:
        suggestions = json.loads(r.content.decode('utf-8'))
        # print('Suggestions', suggestions)
        for suggestion in suggestions:
            if(suggestion[0] == original):
                correctCount += 1
                break
        else:
            incorrectCount += 1
    except:
        pass
print(correctCount, incorrectCount)


        
