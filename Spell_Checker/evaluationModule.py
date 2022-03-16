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
        dictSuggestions = []
        maxWordScore = 0
        for suggestion in suggestions:
            word = ''.join(suggestion[0])
            # if self.dictionary[word] > 0:
            #     dictSuggestions.append((suggestion[1], word))
            # else:
            #accuracy = self.neural_model.getNameAccuracy(['<s>'] + list(word) + ['</s>'])
            accuracy = self.nGramProbability(['<s>','<s>'] + suggestion[0] + ['</s>','</s>'])
            maxWordScore = max(maxWordScore,accuracy)
            # accuracy = (self.nGramProbability(['<s>'] + suggestion[0] + ['</s>']) + self.neural_model.getNameAccuracy(['<s>'] + suggestion[0] + ['</s>']))/2
            ranking.append((accuracy , word))
        # for suggestion in dictSuggestions:
        #     ranking.append((maxWordScore*self.dictionary[suggestion[1]], suggestion[1]))
        return sorted(ranking,reverse=True,key=lambda tup: tup[0])[:10]
        #return ranking

    def nGramProbability(self, suggestion):
        probability = 0
        for i in range(len(suggestion)-2):
            probability += (self.ngramModel.logscore(suggestion[i+2], [suggestion[i],suggestion[i+1]]))
        return probability/(len(suggestion)-2)
