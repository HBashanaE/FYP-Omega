class SuggestionGenerator():

    def __init__(self, insertions, deletions, substitutions) -> None:
        self.insertions = insertions
        self.deletions = deletions
        self.substitutions = substitutions

    def generateSuggestions(self, error):
        suggestions = []
        padded = error[:-1]
        padded.insert(0,'<s>')
        for idx, letter in enumerate(padded):
            for correction in self.insertions[letter]:
                suggestion = error[:idx] + [correction[0]] + error[idx:]
                suggestions.append((suggestion,correction[1]))
        
        for idx, letter in enumerate(padded):
            for correction in self.deletions[letter]:
                suggestion = error[:idx] + error[idx:]
                suggestions.append((suggestion,correction[1]))

        
        for idx, letter in enumerate(error):
            for correction in self.substitutions[letter]:
                suggestion = error[:idx] + [correction[0]] + error[idx+1:]
                suggestions.append((suggestion,correction[1]))   

        return suggestions            
