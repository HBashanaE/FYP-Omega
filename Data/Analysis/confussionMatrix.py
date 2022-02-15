from nltk import metrics
from nltk.metrics import ConfusionMatrix
from tokenizer import tokenize
from unicodedata import normalize
from sequenceAlignment import alignSequences
from collections import defaultdict
import json

path = r'D:\Final Year Project\Data\Error data\OCR errors training - 1.csv'
## Read names
raw_names = open(path, 'r', encoding='utf-8').read()

## Normalize - Canonical Decomposition, followed by Canonical Composition
normalized_raw_names = normalize('NFC', raw_names.strip())

## Get name list
normalized_name_list = normalized_raw_names.split('\n')[1:100]

substitution_confussion_set = defaultdict(int)
deletion_confussion_set = defaultdict(int)
swap_confussion_set = defaultdict(int)
insertion_confussion_set = defaultdict(int)

def addToConfussionSets(aligned_original, aligned_error1):
  length = len(aligned_original)
  for i in range(1, length - 1):

      ## insertionl
      if(aligned_original[i] == '-'):
          prevChar = aligned_original[i - 1]
          currentChar = aligned_error1[i]
          insertion_confussion_set[f'{prevChar},{prevChar}{currentChar}'] += 1

      #deletion
      elif(aligned_error1[i] == '-'):
          prevChar = aligned_error1[i - 1]
          currentChar = aligned_original[i]
          deletion_confussion_set[f'{prevChar}{currentChar},{prevChar}'] += 1
      #swap
      elif(aligned_original[i] == aligned_error1[i + 1] and aligned_error1[i] == aligned_original[i + 1] and aligned_original[i] != aligned_original[i+1]):
          nextChar = aligned_original[i + 1]
          currentChar = aligned_original[i]
          swap_confussion_set[f'{currentChar}{nextChar},{nextChar}{currentChar}'] += 1
      #substitution
      elif(aligned_original[i] != aligned_error1[i]):
          original = aligned_original[i]
          error = aligned_error1[i]
          substitution_confussion_set[f'{original},{error}'] += 1
      #correct
      else:
            pass

for line in normalized_name_list:
 
    original, error1, error2 = line.split(',')
    tokenized_original = ['<s>'] + tokenize(original) + ['</s>']
    tokenized_error1 = ['<s>'] + tokenize(error1) + ['</s>']
    tokenized_error2 = ['<s>'] + tokenize(error2) + ['</s>']
    
    ## Align sequences
    aligned_original, aligned_error1 = alignSequences(tokenized_original, tokenized_error1)
    aligned_original, aligned_error2 = alignSequences(tokenized_original, tokenized_error2)

    addToConfussionSets(aligned_original, aligned_error1)
    addToConfussionSets(aligned_original, aligned_error2)

# print(confussion_set)
with open('data.json', 'w', encoding='utf-8') as outfile:
    json.dump(deletion_confussion_set, outfile, ensure_ascii=False)

with open(f'{path}/confussion_set_insertion.json', 'w', encoding='utf-8') as outfile:
    json.dump(insertion_confussion_set, outfile, ensure_ascii=False)

with open(f'{path}/confussion_set_substitution.json', 'w', encoding='utf-8') as outfile:
    json.dump(substitution_confussion_set, outfile, ensure_ascii=False)

with open(f'{path}/confussion_set_deletion.json', 'w', encoding='utf-8') as outfile:
    json.dump(deletion_confussion_set, outfile, ensure_ascii=False)

with open(f'{path}/confussion_set_swap.json', 'w', encoding='utf-8') as outfile:
    json.dump(swap_confussion_set, outfile, ensure_ascii=False)