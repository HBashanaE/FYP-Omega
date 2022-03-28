import json

from Spell_Checker.evaluationModule import EvaluationMmodule
from Spell_Checker.suggestionGenerator import SuggestionGenerator
from Spell_Checker.utils import preprocess


class SpellChecker():

    def __init__(self, dictionaryPath, neural_model_path, statistical_model_path, insertionPath, deletionPath, substitutionPath) -> None:
        statistical_model_config = {
            "path": statistical_model_path,
            "type": 'Stat'
        }

        neural_model_config = {
            "path": neural_model_path,
            "type": 'Neural'
        }
        model_config = statistical_model_config  # or neural_model_config

        with open(dictionaryPath, 'r', encoding='utf-8') as json_file:
            dictionary = json.load(json_file)
        self.evaluationModule = EvaluationMmodule(dictionary, model_config)
        with open(insertionPath, 'r', encoding='utf-8') as json_file:
            insertions = json.load(json_file)
        with open(deletionPath, 'r', encoding='utf-8') as json_file:
            deletions = json.load(json_file)
        with open(substitutionPath, 'r', encoding='utf-8') as json_file:
            substitutions = json.load(json_file)
        self.suggestionGenerator = SuggestionGenerator(
            dictionary, insertions, deletions, substitutions, 0.95)

    def correctSpelling(self, errorName):
        errorName = preprocess(errorName)
        suggestions = self.suggestionGenerator.generateSuggestions(
            errorName)
        top10Suggestions = suggestions
        rankedSuggestions = self.evaluationModule.rankNames(
            top10Suggestions)
        return rankedSuggestions
