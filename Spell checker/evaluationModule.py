from LanguageModel import NeuralLanguageModel
from collections import defaultdict


class EvaluationMmodule():

    def __init__(self, dictionary, neuralModelpath) -> None:
        self.dictionary = defaultdict(int, dictionary)
        self.neural_model = NeuralLanguageModel(neuralModelpath)

    def isNameAccurate(self, name) -> bool:
        return self.dictionary[name] > 0

    def rankNames(self, suggestions):
        ranking = []
        for suggestion in suggestions:
            if self.dictionary[''.join(suggestion[0])] > 0:
                ranking.append((suggestion[1], ''.join(suggestion[0])))
            else:
                accuracy = self.neural_model.getNameAccuracy(
                    ['<s>'] + suggestion[0] + ['</s>'])
                ranking.append((accuracy* suggestion[1], ''.join(suggestion[0])))
        return sorted(ranking,reverse=True)[:10]

# 