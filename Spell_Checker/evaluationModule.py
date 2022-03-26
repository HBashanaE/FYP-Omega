from collections import defaultdict
import pickle

from LanguageModel import NeuralLanguageModel, StatisticalLanguageModel

class EvaluationModule():

    def __init__(self, dictionary, neuralModelpath, ngramModelPath) -> None:
        self.dictionary = defaultdict(int, dictionary)
        self.neural_model = NeuralLanguageModel(neuralModelpath)
        self.ngramModel = StatisticalLanguageModel(ngramModelPath)

    def isNameAccurate(self, name) -> bool:
        return self.dictionary[name] > 0

    def rankNames(self, suggestions):
        ranking = []
        for suggestion in suggestions:
            word = ''.join(suggestion[0])
            # if self.dictionary[word] > 0:
            #     dictSuggestions.append((suggestion[1], word))
            # else:
            #accuracy = self.neural_model.getNameAccuracy(['<s>'] + list(word) + ['</s>'])
            accuracy = self.ngramModel.getNameAccuracyLog(['<s>','<s>'] + suggestion[0] + ['</s>','</s>'], 3)
            # accuracy = (self.nGramProbability(['<s>'] + suggestion[0] + ['</s>']) + self.neural_model.getNameAccuracy(['<s>'] + suggestion[0] + ['</s>']))/2
            ranking.append((accuracy , word))
        return sorted(ranking,reverse=True,key=lambda tup: tup[0])[:10]
        #return ranking
