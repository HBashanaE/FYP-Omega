from LanguageModel import NeuralLanguageModel
from collections import defaultdict

class EvaluationMmodule():

    def __init__(self, dictionary, neuralModelpath) -> None:
        self.dictionary = defaultdict(dictionary, int)
        self.neural_model = NeuralLanguageModel(neuralModelpath)


    ## TODO: Check dictionary and return whether name is in the dictionary
    def isNameAccurate(self, name) -> bool:
        return self.dictionary(name) > 0


    ## TODO: Rank names using 
    def rankNames(self, suggestions):
        pass