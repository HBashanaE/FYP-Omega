import os
import random
import json
import sys


dirname = os.path.dirname(__file__)
test_names_path = os.path.join(dirname, '../../Data/addresses - cleaned.txt')
substitution_probabilities_path = os.path.join(dirname, '../../error_model/Inverse probaility sets/substitution_probabilities.json')
insertion_probabilities_path = os.path.join(dirname, '../../error_model/Inverse probaility sets/insertion_probabilities.json')

with open(test_names_path, 'r', encoding='utf-8') as f:
    test_names = f.readlines()

with open(substitution_probabilities_path, 'r', encoding='utf-8') as json_file:
    substitution_probabilities = json.load(json_file)

with open(insertion_probabilities_path, 'r', encoding='utf-8') as json_file:
    insertion_probabilities = json.load(json_file)

def tokenize(text):
    suffixesList = ["්", "ා", "ැ", "ෑ", "ි", "ී", "ු",
                    "ූ", "ෙ", "ේ", "ෛ", "ො", "ෝ", "ෞ", "ෘ", "ෲ"]
    tokens = []
    li = 1
    while li < len(text):
        prevChar, currentChar = text[li - 1], text[li]
        if(currentChar == '\u200d'):
            if(li < len(text) - 1):
                if(prevChar == suffixesList[0] and (text[li + 1] == 'ර' or text[li + 1] == 'ය' or text[li + 1] == 'ද')):
                    tokens.append(tokens.pop()+currentChar+text[li + 1])
                    li += 1
        elif(currentChar in suffixesList):
            if(li != 1):
                tokens.append(f"{tokens.pop()}{currentChar}")
            else:
                tokens.append(f"{prevChar}{currentChar}")
        else:
            if(li == 1):
                tokens.append(prevChar)
            tokens.append(currentChar)
        li += 1
    return tokens

def generate_substitution_error(name, i):
    character = name[i]
    weights = []
    substitutions = []
    for sub, weight in substitution_probabilities[character]:
        substitutions.append(sub)
        weights.append(weight)
    errorName = name[:]
    errorName[i] = random.choices(substitutions, weights=weights)[0]
    return errorName

def generate_insertion_error(name, i):
    character = name[i]
    weights = []
    insertions = []
    for ins, weight in insertion_probabilities[character]:
        insertions.append(ins)
        weights.append(weight)
    errorName = name[:i+1] + random.choices(insertions, weights=weights) + name[i+1:]
    return errorName

original_error = ['original,error']
for name in test_names:
    name = name.strip()

    tokenized_name = tokenize(name)
    i = random.randint(0, len(tokenized_name) - 1)
    try:
        error = generate_substitution_error(tokenized_name, i)
        original_error.append(f'{name},{"".join(error)}')
    except:
        pass #no data for chosen character

    i = random.randint(0, len(tokenized_name) - 1)
    try:
        error = generate_insertion_error(tokenized_name, i)
        original_error.append(f'{name},{"".join(error)}')
    except:
        pass #no data for chosen character

with open(os.path.join(dirname, 'confussion_edit_distance_errors_addresses.csv'), 'w', encoding='utf-8') as out_file:
    out_file.write('\n'.join(original_error))

# print(generate_insertion_error(tokenize('යසිත්'), 1))