import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from utils import one_hot_encode

train_on_gpu = False

class NeuralLanguageModel():

    def __init__(self, path) -> None:
        device = torch.device("cpu")
        model = torch.load(path)
        model.to(device)
        self.model = model
        

    def prob(self, net, char, next_char, h=None, top_k=None):
        
        x = np.array([[net.char2int[char]]])
        x = one_hot_encode(x, len(net.chars))
        inputs = torch.from_numpy(x)

        y = np.array([[net.char2int[next_char]]])

        # inputs = inputs.cuda()
        
        h = tuple([each.data for each in h])
        out, h = net(inputs, h)

        p = F.softmax(out, dim=1).data
        p = p.cpu()
        sorted, indices = torch.sort(p.squeeze(), descending=True)
        return sorted[indices.tolist().index(y[0][0])], h

    def getNameAccuracy(self, name):
        self.model.eval() # eval mode
    
        # First off, run through the prime characters
        chars = [ch for ch in name]
        h = self.model.init_hidden(1)
        probs = 0
        for ch_i in range(len(name) - 1):
            prob_i, h = self.prob(self.model, name[ch_i], name[ch_i + 1], h)
            probs += prob_i
            

        return probs/len(name)
        # return self.model.predict()


class StatisticalLanguageModel():
    def __init__(self) -> None:
        pass

    def getNameAccuracy(self, name):
        pass
