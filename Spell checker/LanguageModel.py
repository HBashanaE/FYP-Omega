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

class CharRNN(nn.Module):
    
    def __init__(self, tokens, n_hidden=512, n_layers=3,
                               drop_prob=0.3, lr=0.001):
        super().__init__()
        self.drop_prob = drop_prob
        self.n_layers = n_layers
        self.n_hidden = n_hidden
        self.lr = lr
        
        # creating character dictionaries
        self.chars = tokens
        self.int2char = dict(enumerate(self.chars))
        self.char2int = {ch: ii for ii, ch in self.int2char.items()}
        
        ## TODO: define the LSTM
        self.lstm = nn.LSTM(len(self.chars), n_hidden, n_layers, 
                            dropout=drop_prob, batch_first=True)
        
        ## TODO: define a dropout layer
        self.dropout = nn.Dropout(drop_prob)
        
        ## TODO: define the final, fully-connected output layer
        self.fc = nn.Linear(n_hidden, len(self.chars))
      
    
    def forward(self, x, hidden):
        ''' Forward pass through the network. 
            These inputs are x, and the hidden/cell state `hidden`. '''
                
        ## TODO: Get the outputs and the new hidden state from the lstm
        r_output, hidden = self.lstm(x, hidden)
        
        ## TODO: pass through a dropout layer
        out = self.dropout(r_output)
        
        # Stack up LSTM outputs using view
        # you may need to use contiguous to reshape the output
        out = out.contiguous().view(-1, self.n_hidden)
        
        ## TODO: put x through the fully-connected layer
        out = self.fc(out)
        
        # return the final output and the hidden state
        return out, hidden
    
    
    def init_hidden(self, batch_size):
        ''' Initializes hidden state '''
        # Create two new tensors with sizes n_layers x batch_size x n_hidden,
        # initialized to zero, for hidden state and cell state of LSTM
        weight = next(self.parameters()).data
        
        if (train_on_gpu):
            hidden = (weight.new(self.n_layers, batch_size, self.n_hidden).zero_().cuda(),
                  weight.new(self.n_layers, batch_size, self.n_hidden).zero_().cuda())
        else:
            hidden = (weight.new(self.n_layers, batch_size, self.n_hidden).zero_(),
                      weight.new(self.n_layers, batch_size, self.n_hidden).zero_())
        
        return hidden
