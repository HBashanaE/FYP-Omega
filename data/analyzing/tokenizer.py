from unicodedata import normalize

def tokenize(text):
    suffixesList = ["්", "ා", "ැ", "ෑ", "ි", "ී", "ු",
                    "ූ", "ෙ", "ේ", "ෛ", "ො", "ෝ", "ෞ", "ෘ", "ෲ"]
    tokens = []
    li = 1
    text = preprocess(text)
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


def preprocess(name):
    name = name.replace('fප', 'ෆ')
    name = name.replace('Fප', 'ෆ')
    name = list(name)
    vowels = "අ ආ ඇ ඈ ඉ ඊ උ ඌ ඍ ඎ ඏ ඐ එ ඒ ඓ ඔ ඕ ඖ".split()
    consonants = "ක ඛ ග ඝ ඞ ඟ ච ඡ ජ ඣ ඤ ඥ ඦ ට ඨ ඩ ඪ ණ ඬ ත ථ ද ධ න ඳ ප ඵ බ භ ම ඹ ය ර ල ව ශ ෂ ස හ ළ ෆ".split()
    cannot_followed_by_pillam = "ආ ඇ ඈ ඉ ඊ ඌ ඍ ඎ ඐ ඒ ඓ ඕ ඖ".split()
    can_followed_by_only_a_specific_pillam = "අ උ ඏ එ ඔ".split()
    pillam = "්  ා ැ ෑ ි ී ු  ූ  ෘ ෙ ේ ෛ ො ෝ ෞ  ෲ ෳ".split()
    pillam_cannot_followed_by_pillam = "්  ා ැ ෑ ි ී ු  ූ  ෘ  ේ ෛ ෝ ෞ  ෲ ෳ".split()
    pillam_can_followed_by_only_specific_pillam = " ා  ෙ ො".split()
    preprocessed_name = ''
    i = 0
    while True:
        if(i > len(name) - 1):
            break
        character = name[i]
        next_character = name[i+1] if i < len(name) - 1 else None
        previous_character = name[i-1] if i > 0 else None
        if(character in pillam):
            if(previous_character == None or previous_character in cannot_followed_by_pillam or previous_character in pillam_cannot_followed_by_pillam):
                # print(0, i)
                name.pop(i)
                i -= 1
            elif(not any([(previous_character in consonants),
                          (previous_character ==
                           can_followed_by_only_a_specific_pillam[0] and character == pillam[1]),
                          (previous_character ==
                 can_followed_by_only_a_specific_pillam[1] and character == pillam[-1]),
                          (previous_character ==
                 can_followed_by_only_a_specific_pillam[2] and character == pillam[-1]),
                          (previous_character == can_followed_by_only_a_specific_pillam[3] and (
                    character == pillam[0] or character == pillam[9])),
                (previous_character == can_followed_by_only_a_specific_pillam[3] and (
                    character == pillam[0] or character == pillam[-1])),
                (previous_character ==
                 pillam_can_followed_by_only_specific_pillam[0] and character == pillam[0]),
                (previous_character == pillam_can_followed_by_only_specific_pillam[1] and (
                    character == pillam[0] or character == pillam[1])),
                (previous_character ==
                 pillam_can_followed_by_only_specific_pillam[2] and character == pillam[0]),
            ])):
                # pass
                # print(1, i)
                name.pop(i)
            else:
                # print(2, i)
                # remove characters out of unicode range
                preprocessed_name += character if(3456 <
                                                  ord(character) < 3583) else ''
        elif(character == '\u200d' and (previous_character != pillam[0] or (next_character != 'ර' and next_character != 'ය'))):
            # print(3, i)
            name.pop(i)
            i -= 1
        # elif(character in vowels and i != 0):
        #     # print(4, i)
        #     name.pop(i)
        #     i -= 1
        else:
            # print(5, i)
            # remove characters out of unicode range
            preprocessed_name += character if(3456 < ord(character)
                                              < 3583 or character == '\u200d') else ''
        i += 1
    return normalize("NFC", preprocessed_name)