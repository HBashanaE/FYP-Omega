from collections import defaultdict
from operator import itemgetter

import Levenshtein

from Spell_Checker.utils import tokenize_full

class SuggestionGenerator():

    def __init__(self, dictionary, insertions, deletions, substitutions, baseProbability) -> None:
        self.insertions = insertions
        self.deletions = deletions
        self.substitutions = substitutions
        self.baseProbability = baseProbability
        self.dictionary = defaultdict(int, dictionary)

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

        max_score = max(suggestions, key=itemgetter(1))[1]
        icm_suggestions = [sug[0] for sug in suggestions]

        for x, y in self.dictionary.items():
            if (0 < Levenshtein.distance(x, error) < 3) and (x not in icm_suggestions):
                suggestions.append((tokenize_full(x), max_score*y))

        return sorted(suggestions, key=lambda tup: tup[1], reverse=True)
