from evaluationModule import EvaluationMmodule
from suggestionGenerator import SuggestionGenerator
from utils import preprocess
import json

class SpellChecker():

    def __init__(self, dictionaryPath, neuralModelpath, insertions, deletions, substitutions) -> None:
        with open(dictionaryPath, 'r', encoding='utf-8') as json_file:
            dictionary = json.load(json_file)
        self.evaluationModule = EvaluationMmodule(dictionary, neuralModelpath)
        self.suggestionGenerator = SuggestionGenerator(insertions, deletions, substitutions)

    def correctSpelling(self, errorName):
        isAccurate = self.evaluationModule.isNameAccurate(preprocess(errorName))
        if(isAccurate):
            suggestions = self.suggestionGenerator.generateSuggestions(errorName)
            # rankedSuggestions = self.evaluationModule.rankNames(suggestions)
            print(suggestions)
        else:
            suggestions = self.suggestionGenerator.generateSuggestions(errorName)
            # rankedSuggestions = self.evaluationModule.rankNames(suggestions)
            print(suggestions)