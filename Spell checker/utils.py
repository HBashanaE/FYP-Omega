import numpy as np
from unicodedata import normalize

def one_hot_encode(arr, n_labels):
    
    one_hot = np.zeros((np.multiply(*arr.shape), n_labels), dtype=np.float32)
    
    one_hot[np.arange(one_hot.shape[0]), arr.flatten()] = 1.
    
    one_hot = one_hot.reshape((*arr.shape, n_labels))
    
    return one_hot

def preprocess(text):
    normalizedText = normalize('NFC', text)
    preprocessedName = ''
    for character in normalizedText:
            preprocessedName += character if( 3456 < ord(character) < 3583 or character == '\u200d' ) else ''
    return text

def tokenize(text):
    suffixesList = [ "්", "ා", "ැ", "ෑ", "ි", "ී", "ු", "ූ", "ෙ", "ේ", "ෛ", "ො", "ෝ" ,"ෞ","ෘ","ෲ"]
    tokens = []
    li = 1
    while li < len(text):
        prevChar, currentChar = text[li - 1], text[li]
        if(currentChar == '\u200d'):
                if(li < len(text) - 1):
                    if(prevChar == suffixesList[0] and (text[li + 1] == 'ර' or text[li + 1] == 'ය' or text[li + 1] == 'ද')):
                        tokens.append(tokens.pop()+currentChar+text[li + 1])
                        li += 1
        elif(currentChar in suffixesList):
            if(li != 1):
                tokens.append(f"{tokens.pop()}{currentChar}")
            else:
                tokens.append(f"{prevChar}{currentChar}")
        else:
            if(li == 1):
                tokens.append(prevChar)
            tokens.append(currentChar)
        li += 1
    return tokens