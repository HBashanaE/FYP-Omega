def tokenize(text):
    suffixesList = ["්", "ා", "ැ", "ෑ", "ි", "ී", "ු",
        "ූ", "ෙ", "ේ", "ෛ", "ො", "ෝ", "ෞ", "ෘ", "ෲ"]
    tokens = []
    li = 1
    while li < len(text):
        prevChar, currentChar = text[li - 1], text[li]
        if(currentChar == '\u200d'):
                if(li < len(text) - 1):
                    if(prevChar == suffixesList[0] and (text[li + 1] == 'ර' or text[li + 1] == 'ය' or text[li + 1] == 'ද')):
                        if(li != 1):
                            tokens.append(tokens.pop()+currentChar+text[li + 1])
                        else:
                            # ignore '\u200d' when it is the first character
                            tokens.append(currentChar+text[li + 1])
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