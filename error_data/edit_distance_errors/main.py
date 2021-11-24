import random
import json
from Error import Error

upper = 1000
upperThreashold = 500
lowerThreashold = 400

EB1 = []
EB2 = []
EB3 = []
EB4 = []
EB5 = []



def findErrors(text):
    errors = []
    for i in range(len(text)):
        letter = text[i]
        if letter == "්":
            errors.append(Error(0, i))
        elif letter == "ා":
            errors.append(Error(0, i))
        elif letter == "‌ෙ":
            errors.append(Error(0, i))
        elif letter == "ෘ":
            errors.append(Error(0, i))
        elif letter == "ෟ":
            errors.append(Error(0, i))
        elif letter == "ඃ":
            errors.append(Error(0, i))

        elif letter == "ැ":
            errors.append(Error(1, i))

        elif letter == "ෑ":
            errors.append(Error(2, i))

        elif letter == "ි":
            errors.append(Error(3, i))

        elif letter == "ී":
            errors.append(Error(4, i))

        elif letter == "ු":
            errors.append(Error(5, i))

        elif letter == "ූ":
            errors.append(Error(6, i))

        elif letter == "ේ":
            errors.append(Error(7, i))

        elif letter == "ෛ":
            errors.append(Error(7, i))

        elif letter == "ො":
            errors.append(Error(9, i))

        elif letter == "ෝ":
            errors.append(Error(10, i))

        elif letter == "ෞ":
            errors.append(Error(11, i))

        elif letter == "ආ":
            errors.append(Error(12, i))

        elif letter == "ඇ":
            errors.append(Error(13, i))

        elif letter == "ඈ":
            errors.append(Error(14, i))

        elif letter == "ඌ":
            errors.append(Error(15, i))

        elif letter == "ඒ":
            errors.append(Error(16, i))

        elif letter == "ඓ":
            errors.append(Error(16, i))

        elif letter == "ඕ":
            errors.append(Error(17, i))

        elif letter == "ඖ":
            errors.append(Error(17, i))

        elif letter == "ං":
            errors.append(Error(18, i))

        elif letter == "ක":
            errors.append(Error(19, i))

        elif letter == "ඛ":
            errors.append(Error(20, i))

        elif letter == "ග":
            errors.append(Error(21, i))

        elif letter == "ඝ":
            errors.append(Error(22, i))

        elif letter == "ඟ":
            errors.append(Error(22, i))

        elif letter == "ච":
            errors.append(Error(23, i))

        elif letter == "ඡ":
            errors.append(Error(24, i))

        elif letter == "ජ":
            errors.append(Error(25, i))

        elif letter == "ට":
            errors.append(Error(26, i))

        elif letter == "ඨ":
            errors.append(Error(27, i))

        elif letter == "ඪ":
            errors.append(Error(28, i))

        elif letter == "ණ":
            errors.append(Error(29, i))

        elif letter == "ත":
            errors.append(Error(30, i))

        elif letter == "ථ":
            errors.append(Error(31, i))

        elif letter == "ධ":
            errors.append(Error(32, i))

        elif letter == "න":
            errors.append(Error(31, i))

        elif letter == "ඳ":
            errors.append(Error(32, i))

        elif letter == "ද":
            errors.append(Error(33, i))
        
        elif letter == "බ":
            errors.append(Error(34, i))

        elif letter == "භ":
            errors.append(Error(35, i))

        elif letter == "ඹ":
            errors.append(Error(35, i))

        elif letter == "ව":
            errors.append(Error(36, i))

        elif letter == "ශ":
            errors.append(Error(37, i))

        elif letter == "ෂ":
            errors.append(Error(38, i))

        elif letter == "ස":
            errors.append(Error(39, i))

        elif letter == "ළ":
            errors.append(Error(46, i))

    return errors

def choiceErrors(errors, n):
    choice = set()
    if len(errors) > n:
        for i in range(n):
            choice.add(errors.pop(random.choice([i for i in range(len(errors))])))
    else:
        choice = set(errors)
    return choice

l = []
with open('SortedSinhalaNamesNew.txt', 'r', encoding='utf-8') as f:
    n = 500
    l = f.readlines()
    r = 4000 ## random.randint(0, len(l) - n)
    l = l[r: r+n]

errorCorrectNamePairs = []
n = 3
for name in l:
    errors = findErrors(name.strip())
    if len(errors) > 0:
        chosenErrors = choiceErrors(errors, n)
        # print(chosenErrors)
        if(len(chosenErrors) != n):
            continue
        s = name
        for e in chosenErrors:
            s = e.performError(s)
        s = s.replace('0', '').replace('x', 'න්')
        if s not in l:
            errorCorrectNamePairs.append((s.strip(), name.strip()))
            # with open("a.txt", "a", encoding="utf-8") as f:
            #     f.write(s)

with open(f'{n}errorCorrect.txt', 'w', encoding="utf-8") as f:
    f.write(json.dumps(errorCorrectNamePairs))
with open(f'{n}errorCorrectView.txt', 'w', encoding="utf-8") as f:
    f.write(str(errorCorrectNamePairs))