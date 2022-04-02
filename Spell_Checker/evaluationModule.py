from collections import defaultdict

from Spell_Checker.LanguageModel import NeuralLanguageModel, StatisticalLanguageModel

class EvaluationModule():

    def __init__(self, dictionary, model_config) -> None:
        self.dictionary = defaultdict(int, dictionary)
        if(model_config['path'] == None):
            raise ValueError('Define a model path')
        if(model_config['type'] == 'Neural'):
            self.model = NeuralLanguageModel(model_config['path'])
        else:
            self.model = StatisticalLanguageModel(model_config['path'])
        

    def isNameAccurate(self, name) -> bool:
        return self.dictionary[name] > 0

    def rankNames(self, suggestions):
        ranking = []
        maxWordScore = 0
        for suggestion in suggestions:
            word = ''.join(suggestion[0])
            accuracy = self.model.getNameAccuracyLog(suggestion[0])
            maxWordScore = max(maxWordScore,accuracy)
            ranking.append((accuracy , word))
        return sorted(ranking,reverse=True,key=lambda tup: tup[0])[:10]
