import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pickle

from utils import one_hot_encode
from CharRNN import CharRNN

train_on_gpu = False
class NeuralLanguageModel():

    def __init__(self, path) -> None:
        device = torch.device("cpu")
        # model = CharRNN(*args, **kwargs)
        # model.load_state_dict(torch.load(PATH))
        model = torch.load(path, map_location=torch.device('cpu'))
        model.eval()
        model.to(device)
        self.model = model

    def prob(self, net, char, next_char, h=None, top_k=None):

        x = np.array([[net.char2int[char]]])
        x = one_hot_encode(x, len(net.chars))
        inputs = torch.from_numpy(x)

        y = np.array([[net.char2int[next_char]]])

        h = tuple([each.data for each in h])
        out, h = net(inputs, h)

        p = F.softmax(out, dim=1).data
        p = p.cpu()
        sorted, indices = torch.sort(p.squeeze(), descending=True)
        return sorted[indices.tolist().index(y[0][0])], h

    def getNameAccuracy(self, name):
        self.model.eval()

        chars = [ch for ch in name]
        h = self.model.init_hidden(1)
        probs = 0
        for ch_i in range(len(name) - 1):
            prob_i, h = self.prob(self.model, name[ch_i], name[ch_i + 1], h)
            probs += prob_i

        return probs.item()/len(name)

    def getNameAccuracyExp(self, name):
        self.model.eval()

        chars = [ch for ch in name]
        h = self.model.init_hidden(1)
        probs = 1
        for ch_i in range(len(name) - 1):
            prob_i, h = self.prob(self.model, name[ch_i], name[ch_i + 1], h)
            probs *= torch.exp(prob_i).item()

        return probs

    def getNameAccuracyMul(self, name):
        self.model.eval()

        chars = [ch for ch in name]
        h = self.model.init_hidden(1)
        probs = 1
        for ch_i in range(len(name) - 1):
            prob_i, h = self.prob(self.model, name[ch_i], name[ch_i + 1], h)
            probs *= prob_i.item()

        return probs

    def getNameAccuracyLog(self, name):
        self.model.eval()

        chars = [ch for ch in name]
        h = self.model.init_hidden(1)
        probs = 0
        for ch_i in range(len(name) - 1):
            prob_i, h = self.prob(self.model, name[ch_i], name[ch_i + 1], h)
            probs += torch.log(prob_i)

        return probs.item()/len(name)


class StatisticalLanguageModel():

    def __init__(self, path) -> None:
        with open(path, 'rb') as f:
            self.model = pickle.load(f)

    def getNameAccuracy(self, name, n):

        chars = [ch for ch in name]
        probs = 0
        if n==2:
            for ch_i in range(len(name) - 1):
                probs += self.model.score(chars[ch_i+1], [chars[ch_i]])
            return probs/(len(name) - 1)
        if n==3:
            for ch_i in range(len(name) - 2):
                probs += self.model.score(chars[ch_i+2], [chars[ch_i],chars[ch_i+1]])
            return probs/(len(name) - 2)        
        return 0   

    def getNameAccuracyExp(self, name, n):
        chars = [ch for ch in name]
        probs = 1
        if n==2:
            for ch_i in range(len(name) - 1):
                probs *= math.exp(self.model.score(chars[ch_i+1], [chars[ch_i]]))
            return probs
        if n==3:
            for ch_i in range(len(name) - 2):
                probs *= math.exp(self.model.score(chars[ch_i+2], [chars[ch_i],chars[ch_i+1]]))
            return probs
        return 0  


    def getNameAccuracyMul(self, name, n):
        chars = [ch for ch in name]
        probs = 1
        if n==2:
            for ch_i in range(len(name) - 1):
                probs *= self.model.score(chars[ch_i+1], [chars[ch_i]])
            return probs
        if n==3:
            for ch_i in range(len(name) - 2):
                probs *= self.model.score(chars[ch_i+2], [chars[ch_i],chars[ch_i+1]])
            return probs
        return 0    

    def getNameAccuracyLog(self, name, n):
        chars = [ch for ch in name]
        probs = 0
        if n==2:
            for ch_i in range(len(name) - 1):
                probs += self.model.logscore(chars[ch_i+1], [chars[ch_i]])
            return probs/(len(name) - 1)
        if n==3:
            for ch_i in range(len(name) - 2):
                probs += self.model.logscore(chars[ch_i+2], [chars[ch_i],chars[ch_i+1]])
            return probs/(len(name) - 2)
        return 0   
