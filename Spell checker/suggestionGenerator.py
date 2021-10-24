from unicodedata import normalize as unicodeNormalize
import regex as re
from utils import tokenize


class SuggestionGenerator():

    def __init__(self, insertions, deletions, substitutions, baseProbability) -> None:
        self.insertions = insertions
        self.deletions = deletions
        self.substitutions = substitutions
        self.baseProbability = baseProbability

    # error -> (list) tokenized error word
    def generateSuggestions(self, error):
        tokenizedError = tokenize(error)
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

        return suggestions
