import torch
class NeuralLanguageModel():

    def __init__(self, path) -> None:
        with open(path) as f:
            self.model = torch.load(f)

    def getNameAccuracy(self, name):
        return self.model.predict()


class StatisticalLanguageModel():
    def __init__(self) -> None:
        pass

    def getNameAccuracy(self, name):
        pass

        