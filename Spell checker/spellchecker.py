from evaluationModule import EvaluationMmodule
from suggestionGenerator import SuggestionGenerator
from utils import preprocess
import json


class SpellChecker():

    def __init__(self, dictionaryPath, neuralModelpath, ngramModelPath, insertionPath, deletionPath, substitutionPath) -> None:
        with open(dictionaryPath, 'r', encoding='utf-8') as json_file:
            dictionary = json.load(json_file)
        self.evaluationModule = EvaluationMmodule(dictionary, neuralModelpath, ngramModelPath)
        with open(insertionPath, 'r', encoding='utf-8') as json_file:
            insertions = json.load(json_file)
        with open(deletionPath, 'r', encoding='utf-8') as json_file:
            deletions = json.load(json_file)
        with open(substitutionPath, 'r', encoding='utf-8') as json_file:
            substitutions = json.load(json_file)
        self.suggestionGenerator = SuggestionGenerator(
            insertions, deletions, substitutions, 0.95)

    def correctSpelling(self, errorName):
        errorName = preprocess(errorName)
        isAccurate = self.evaluationModule.isNameAccurate(
            preprocess(errorName))
        # if(isAccurate):
        #     suggestions = self.suggestionGenerator.generateSuggestions(
        #         errorName)
        #     top10Suggestions = suggestions
        #     rankedSuggestions = self.evaluationModule.rankNames(
        #         top10Suggestions)
        #     return [(1.0, errorName)] + rankedSuggestions
        # else:
        suggestions = self.suggestionGenerator.generateSuggestions(
            errorName)
        top10Suggestions = suggestions
        rankedSuggestions = self.evaluationModule.rankNames(
            top10Suggestions)
        return rankedSuggestions
