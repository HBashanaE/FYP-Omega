from collections import defaultdict

from pandas import read_excel
from preprocess import preprocess
from tokenizer import tokenize

excluded_list = [
    "පාර",
    "මාවත",
    "වත්ත",
    "පටුමග",
    "කොටස",
    "වන",
    "දකුණ",
    "උතුර",
    "නිවාස",
    "පෙදෙස",
    "ජනපදය",
    "කණුව",
    "යාය",
    "වීදිය",
    "පහල",
    "නිවස",
    "ගෙදර",
    "බටහිර",
    "ඇල",
    "නව",
    "ඉහළ",
    "නැගෙනහිර",
    "අසල",
    "නගරය",
    "ඉහල",
    "පහළ",
    "වැව",
    "උයන",
    "කන්ද",
    "හන්දිය",
    "ගම්මානය",
    "දකුණු",
    "පරණ",
    "හරස්",
    "උතුරු",
    "උඩ",
    "පුර",
    "මැද",
    "පාසල",
    "විහාර",
    "කුඩා",
    "යුනිට්",
    "පළමු",
    "අදියර",
    "දුම්රිය"
]


my_sheet = 'Sheet1'
file_name = r'D:\Final Year Project\Data\addresses.xlsx'
df = read_excel(file_name, sheet_name = my_sheet, header=None)
raw_addresses = df[0]
all_names = []
all_names_with_frequency = defaultdict(int)
for i, address in enumerate(raw_addresses):
    names = address.split()
    for name in names:
        name = preprocess(name)
        if(len(tokenize(name)) > 1 and name not in excluded_list):
            all_names.append(name)
            all_names_with_frequency[name] += 1
all_names_with_frequency_sorted = [k for k, v in sorted(all_names_with_frequency.items(), key=lambda item: item[1], reverse=True)]

# print(all_names_with_frequency_sorted)

# with open(r'D:\Final Year Project\Codes\FYP-Omega\Data\unique addresses - not cleaned.txt', 'w', encoding='utf-8') as f:
#     f.write('\n'.join(all_names_with_frequency_sorted))
# with open(r'D:\Final Year Project\Codes\FYP-Omega\Data\addresses - not cleaned.txt', 'w', encoding='utf-8') as f:
#     f.write('\n'.join(all_names))
with open(r'D:\Final Year Project\Codes\FYP-Omega\Data\addresses - cleaned.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_names))

