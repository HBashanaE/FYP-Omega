from os.path import dirname, join
import random
import json
from unicodedata import normalize

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


# අ ආ ඇ ඈ ඉ ඊ උ ඌ ඍ ඎ ඏ ඐ එ ඒ ඓ ඔ ඕ ඖ ක ඛ ග ඝ ඞ ඟ ච ඡ ජ ඣ ඤ ඥ ඦ ට ඨ ඩ ඪ ණ ඬ ත ථ ද ධ න ඳ ප ඵ බ භ ම ඹ ය ර ල ව ශ ෂ ස හ ළ ෆ  ්  ා ැ ෑ ි ී ු  ූ  ෘ ෙ ේ ෛ ො ෝ ෞ ෟ ෦ ෧ ෨ ෩ ෪ ෫ ෬ ෭ ෮ ෯ ෲ ෳ ෴
if __name__ == "__main__":
    name = "බුද්ධිප්‍රිය"
    # print(list(name))
    # print(list(preprocess(name)))
    root_dirname = dirname(__file__)
    names = open(join(root_dirname, "../error_data/ocr_error_data/OCR error training/OCR errors training - 1.csv"), 'r', encoding='utf-8').readlines()
    selected_names = random.sample(names, 250)
    with open(join(root_dirname, 'result.txt'), 'a', encoding='utf-8') as f:
        for i, name in enumerate(selected_names):
            # print(list(name.strip()), list(preprocess(name)))
            # print(name.strip(), preprocess(name))
            _, e1, e2 = name.split(',')
            name = e2
            f.write(f'{json.dumps(list(name.strip()), ensure_ascii=False)} {json.dumps(list(preprocess(name)), ensure_ascii=False)}\n')
            f.write(f'{name.strip()} {preprocess(name)}\n')
