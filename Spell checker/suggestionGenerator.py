from unicodedata import normalize as unicodeNormalize
import regex as re

class SuggestionGenerator():

    def __init__(self, insertions, deletions, substitutions, baseProbability) -> None:
        self.insertions = insertions
        self.deletions = deletions
        self.substitutions = substitutions
        self.baseProbability = baseProbability

    #error -> (list) tokenized error word
    def generateSuggestions(self, error):
        tokenizedError = self.tokenize(error)
        suggestions = [(tokenizedError,self.baseProbability)]
        padded = tokenizedError[:-1]
        padded.insert(0,'<s>')
        for idx, letter in enumerate(padded[1:]):
            if letter in self.insertions:
                for correction in self.insertions[letter]:
                    if correction[0]==padded[idx-1]:
                        suggestion = tokenizedError[:idx] + tokenizedError[idx+1:]
                        suggestions.append((suggestion,correction[1]))
        
        for idx, letter in enumerate(padded):
            if letter in self.deletions:
                for correction in self.deletions[letter]:
                    suggestion = tokenizedError[:idx] + [correction[0]] + tokenizedError[idx:]
                    suggestions.append((suggestion,correction[1]))

        
        for idx, letter in enumerate(tokenizedError):
            if letter in self.substitutions:
                for correction in self.substitutions[letter]:
                    suggestion = tokenizedError[:idx] + [correction[0]] + tokenizedError[idx+1:]
                    suggestions.append((suggestion,correction[1]))   

        return suggestions

    



    def tokenize(text):
        suffixesList = [ 
        "්", 
        "ා", 
        "ැ", 
        "ෑ", 
        "ි", 
        "ී", 
        "ු", 
        "ූ", 
        "ෙ", 
        "ේ", 
        "ෛ", 
        "ො", 
        "ෝ" ,
        "ෞ",
        "ෘ",
        "ෲ"
        ]
        tokens = []
        li = 1
        while li < len(text):
        # for li in range(1, len(text)):
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
