from evaluationModule import EvaluationMmodule
from suggestionGenerator import SuggestionGenerator

class SpellChecker():

    def __init__(self, dictionary) -> None:
        self.evaluationModule = EvaluationMmodule(dictionary, r'D:\Final Year Project\Data\model.pth')
        self.suggestionGenerator = SuggestionGenerator()
        pass

    def correctSpelling(self, errorName):
        isAccurate = self.evaluationModule.isNameAccurate(errorName)
        if(isAccurate):
            suggestions = self.suggestionGenerator.generateSuggestions(errorName)
            rankedSuggestions = self.evaluationModule.rankNames(suggestions)
        else:
            suggestions = self.suggestionGenerator.generateSuggestions(errorName)
            rankedSuggestions = self.evaluationModule.rankNames(suggestions)