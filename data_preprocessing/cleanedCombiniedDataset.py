from tokenizer import tokenize

filePath = r'D:/Final Year Project/Data/Combined/combined all names.txt'
# print(len(tokenize('එම්')))
names = open(filePath, 'r', encoding='utf-8').readlines()
cleanedNames = []

for line in names:
    # print(len(tokenize(line)), line, 'line')
    if(len(tokenize(line)) < 3):
            continue
    line = line.replace('fප', 'ෆ')
    line = line.replace('Fප', 'ෆ')
    for name in line.split('.'):
        # print(len(tokenize(name)), name, 'name')
        
        cleanedName = ''
        for character in name:
            cleanedName += character if( 3456 < ord(character) < 3583 or character == '\u200d' ) else ''
        if(len(cleanedName) < 2):
            continue
        if(len(tokenize(cleanedName)) < 3):
            continue
        cleanedNames.append(cleanedName)

# print(cleanedNames)

filePath = r'D:\Final Year Project\Data\Cleaned data\combined all names - cleaned.txt'
open(filePath, 'w', encoding='utf-8').write('\n'.join(cleanedNames))
