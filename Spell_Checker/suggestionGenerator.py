import os
from unicodedata import normalize as unicodeNormalize
import regex as re
import json

from Spell_Checker.utils import tokenize_full

class SuggestionGenerator():

    def __init__(self, insertions, deletions, substitutions, baseProbability) -> None:
        self.insertions = insertions
        self.deletions = deletions
        self.substitutions = substitutions
        self.baseProbability = baseProbability

    # error -> (list) tokenized error word
    def generateSuggestions(self, error):
        tokenizedError = tokenize_full(error)
        suggestions = [(tokenizedError, self.baseProbability)]
        padded = tokenizedError[:-1]
        padded.insert(0, '<s>')
        for idx, letter in enumerate(padded[1:]):
            if letter in self.insertions:
                for correction in self.insertions[letter]:
                    if correction[0] == padded[idx-1]:
                        suggestion = tokenizedError[:idx] + \
                            tokenizedError[idx+1:]
                        suggestions.append((suggestion, correction[1]))

        for idx, letter in enumerate(padded):
            if letter in self.deletions:
                for correction in self.deletions[letter]:
                    suggestion = tokenizedError[:idx] + \
                        [correction[0]] + tokenizedError[idx:]
                    suggestions.append((suggestion, correction[1]))

        for idx, letter in enumerate(tokenizedError):
            if letter in self.substitutions:
                for correction in self.substitutions[letter]:
                    suggestion = tokenizedError[:idx] + \
                        [correction[0]] + tokenizedError[idx+1:]
                    suggestions.append((suggestion, correction[1]))

        return sorted(suggestions, key=lambda tup: tup[1], reverse=True)

dirname = os.path.dirname(__file__)

insertionPath = os.path.join(
    dirname, '../error_model/Probability sets/insertion_probabilities.json')
deletionPath = os.path.join(
    dirname, '../error_model/Probability sets/deletion_probabilities.json')
substitutionPath = os.path.join(
    dirname, '../error_model/Probability sets/substitution_probabilities.json')


with open(insertionPath, 'r', encoding='utf-8') as json_file:
    insertions = json.load(json_file)
with open(deletionPath, 'r', encoding='utf-8') as json_file:
    deletions = json.load(json_file)
with open(substitutionPath, 'r', encoding='utf-8') as json_file:
    substitutions = json.load(json_file)

suggestionGenerator = SuggestionGenerator(insertions, deletions, substitutions, 0.95)
with open("sample.json", "w",encoding='utf8') as outfile:
    json.dump(sorted(suggestionGenerator.generateSuggestions('ඉසන්'), key=lambda tup: tup[1], reverse=True), outfile, ensure_ascii=False)
