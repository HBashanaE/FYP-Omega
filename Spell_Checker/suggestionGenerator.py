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
        sug_list = [tokenizedError]
        padded = tokenizedError[:-1]
        padded.insert(0, '<s>')
        for idx, letter in enumerate(padded[1:]):
            if letter in self.insertions:
                for correction in self.insertions[letter]:
                    if correction[0] == padded[idx-1]:
                        suggestion = tokenizedError[:idx] + \
                            tokenizedError[idx+1:]
                        if suggestion not in sug_list:
                            suggestions.append((suggestion, correction[1]))
                            sug_list.append(suggestion)

        for idx, letter in enumerate(padded):
            if letter in self.deletions:
                for correction in self.deletions[letter]:
                    suggestion = tokenizedError[:idx] + \
                        [correction[0]] + tokenizedError[idx:]
                        if suggestion not in sug_list:
                            suggestions.append((suggestion, correction[1]))
                            sug_list.append(suggestion)

        for idx, letter in enumerate(tokenizedError):
            if letter in self.substitutions:
                for correction in self.substitutions[letter]:
                    suggestion = tokenizedError[:idx] + \
                        [correction[0]] + tokenizedError[idx+1:]
                        if suggestion not in sug_list:
                            suggestions.append((suggestion, correction[1]))
                            sug_list.append(suggestion)

        max_score = max(suggestions, key=itemgetter(1))[1]

        for x, y in self.dictionary.items():
            if (0 < Levenshtein.distance(x, error) < 3) and (x not in sug_list):
                suggestion = tokenize_full(x)
                suggestions.append((suggestion, max_score*y))
                sug_list.append(suggestion)
                

        return suggestions
