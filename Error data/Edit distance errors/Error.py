import random

class Error:

    def __init__(self, type, index):
        self.type = type
        self.index = index

    def getSubError(self, n):
        e = random.choice([i for i in range(n)])
        return e


    def performError(self, text):
        type = self.type
        index = self.index

        if type == 0:
            return text[:index] + '0' + text[index+1:]
        elif type == 1:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + '0' + text[index+1:]
            else:
                return text[:index] + 'ෑ' + text[index+1:]
        elif type == 2:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + '0' + text[index+1:]
            else:
                return text[:index] + 'ැ' + text[index+1:]
        elif type == 3:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + '0' + text[index+1:]
            else:
                return text[:index] + 'ී' + text[index+1:]
        elif type == 4:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + '0' + text[index+1:]
            else:
                return text[:index] + 'ි' + text[index+1:]
        elif type == 5:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + '0' + text[index+1:]
            else:
                return text[:index] + 'ූ' + text[index+1:]
        elif type == 6:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + '0' + text[index+1:]
            else:
                return text[:index] + 'ු' + text[index+1:]
        elif type == 7:
            return text[:index] + 'ෙ' + text[index+1:]
        elif type == 8:
            return text[:index] + 'ෙ' + text[index+1:]
        elif type == 9:
            return text[:index] + 'ෙ' + text[index+1:]
        elif type == 10:
            return text[:index] + 'ො' + text[index+1:]
        elif type == 11:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + 'ෙ' + text[index+1:]
            else:
                return text[:index] + 'ෟ' + text[index+1:]
        elif type == 12:
            return text[:index] + 'අ' + text[index+1:]
        elif type == 13:
            return text[:index] + 'ඈ' + text[index+1:]
        elif type == 14:
            return text[:index] + 'ඇ' + text[index+1:]
        elif type == 15:
            return text[:index] + 'උ' + text[index+1:]
        elif type == 16:
            return text[:index] + '‍එ' + text[index+1:]
        elif type == 17:
            return text[:index] + 'ඔ' + text[index+1:]
        elif type == 18:
            return text[:index] + 'x' + text[index+1:]
        elif type == 19:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + 'ඛ' + text[index+1:]
            else:
                return text[:index] + 'ත' + text[index+1:]
        elif type == 20:
            return text[:index] + 'ත' + text[index+1:]
        elif type == 21:
            return text[:index] + 'ඟ' + text[index+1:]
        elif type == 22:
            return text[:index] + 'ග' + text[index+1:]
        elif type == 23:
            return text[:index] + 'ව' + text[index+1:]
        elif type == 24:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + 'ච' + text[index+1:]
            else:
                return text[:index] + 'ජ' + text[index+1:]
        elif type == 25:
            return text[:index] + 'ඡ' + text[index+1:]
        elif type == 26:
            return text[:index] + 'ම' + text[index+1:]
        elif type == 27:
            return text[:index] + 'ට' + text[index+1:]
        elif type == 28:
            return text[:index] + 'ඩ' + text[index+1:]
        elif type == 29:
            return text[:index] + 'න' + text[index+1:]
        elif type == 30:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + 'ක' + text[index+1:]
            else:
                return text[:index] + 'න' + text[index+1:]
        elif type == 31:
            return text[:index] + 'ත' + text[index+1:]
        elif type == 32:
            return text[:index] + 'ද' + text[index+1:]
        elif type == 33:
            return text[:index] + 'ඳ' + text[index+1:]
        elif type == 34:
            return text[:index] + 'ඛ' + text[index+1:]
        elif type == 35:
            return text[:index] + 'බ' + text[index+1:]
        elif type == 36:
            return text[:index] + 'ච' + text[index+1:]
        elif type == 37:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + 'ෂ' + text[index+1:]
            else:
                return text[:index] + 'ස' + text[index+1:]
        elif type == 38:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + 'ශ' + text[index+1:]
            else:
                return text[:index] + 'ස' + text[index+1:]
        elif type == 39:
            e = self.getSubError(2)
            if e == 0:
                return text[:index] + 'ශ' + text[index+1:]
            else:
                return text[:index] + 'ෂ' + text[index+1:]
        elif type == 40:
            return text[:index] + 'ල' + text[index+1:]
      