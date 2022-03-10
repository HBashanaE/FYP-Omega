from collections import defaultdict
import pickle

from Spell_Checker.LanguageModel import NeuralLanguageModel

class EvaluationMmodule():

    def __init__(self, dictionary, neuralModelpath, ngramModelPath) -> None:
        self.dictionary = defaultdict(int, dictionary)
        self.neural_model = NeuralLanguageModel(neuralModelpath)
        
        with open(ngramModelPath, 'rb') as f:
            self.ngramModel = pickle.load(f)

    def isNameAccurate(self, name) -> bool:
        return self.dictionary[name] > 0

    def rankNames(self, suggestions):
        ranking = []
        for suggestion in suggestions:
            if self.dictionary[''.join(suggestion[0])] > 0:
                ranking.append((suggestion[1], ''.join(suggestion[0])))
            else:
                # accuracy = self.neural_model.getNameAccuracy(['<s>'] + list(''.join(suggestion[0])) + ['</s>'])
                accuracy = self.nGramProbability(['<s>'] + suggestion[0] + ['</s>'])
                # accuracy = (self.nGramProbability(['<s>'] + suggestion[0] + ['</s>']) + self.neural_model.getNameAccuracy(['<s>'] + suggestion[0] + ['</s>']))/2
                ranking.append((accuracy* suggestion[1], ''.join(suggestion[0])))
        return sorted(ranking,reverse=True)[:10]

    def nGramProbability(self, suggestion):
        probability = 0
        for i in range(len(suggestion)-1):
            probability += (self.ngramModel.score(suggestion[i+1], [suggestion[i]]))
        return probability/(len(suggestion)-1)
