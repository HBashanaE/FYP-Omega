from os.path import dirname, join
import json
from collections import defaultdict

root_dirname = dirname(__file__)
confussion_set_insertion_path = join(
    root_dirname, 'Confussion Sets\confussion_set_insertion.json')
confussion_set_substitution_path = join(
    root_dirname, 'Confussion Sets\confussion_set_substitution.json')
confussion_set_deletion_path = join(
    root_dirname, 'Confussion Sets\confussion_set_deletion.json')

with open(confussion_set_substitution_path, 'r', encoding='utf-8') as json_file:
    confussion_set_substitution = json.load(json_file)

with open(confussion_set_insertion_path, 'r', encoding='utf-8') as json_file:
    confussion_set_insertion = json.load(json_file)

with open(confussion_set_deletion_path, 'r', encoding='utf-8') as json_file:
    confussion_set_deletion = json.load(json_file)

insertion_inverse_probabilities = defaultdict(list)
substitution_inverse_probabilities = defaultdict(list)
deletion_inverse_probabilities = defaultdict(list)

for key, value in confussion_set_insertion.items():
    x, y = key.split(',')
    y = y.replace(x, '')
    insertion_inverse_probabilities[x].append([y, value])

for key, value in confussion_set_substitution.items():
    x, y = key.split(',')
    substitution_inverse_probabilities[x].append([y, value])

for key, value in confussion_set_deletion.items():
    x, y = key.split(',')
    x = x.replace(y, '')
    deletion_inverse_probabilities[y].append([x, value])

with open(join(root_dirname, "Inverse probaility sets/insertion_probabilities.json"), "w", encoding='utf8') as outfile:
    json.dump(insertion_inverse_probabilities, outfile, ensure_ascii=False)

with open(join(root_dirname, "Inverse probaility sets/subbstitution_probabilities.json"), "w", encoding='utf8') as outfile:
    json.dump(substitution_inverse_probabilities, outfile, ensure_ascii=False)

with open(join(root_dirname, "Inverse probaility sets/deletion_probabilities.json"), "w", encoding='utf8') as outfile:
    json.dump(deletion_inverse_probabilities, outfile, ensure_ascii=False)
