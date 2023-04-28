import csv


class XKJDTree:
    char = ""
    pinyin = ""
    code = ""
    full = False
    childs = {}
    def __init__(self,char : str) -> None:
        self.char = char

    def insert(self,code,char):
        if len(char) == 1:
            assert 'a' <= code[0] and code[0] <= 'z'
            assert 'a' <= code[1] and code[2] <= 'z'
        cur = self
        cur_code = ""
        code_len = len(code)
        for i in range(code_len):
            c = code[i]
            if i + 1 != code_len:
                nxt_c = code[i + 1 ]
            cur_code = cur_code + c
            if c not in cur.childs:
                cur.childs[c] = [XKJDTree(char=char)]
                break
            else:
                if len(cur.childs[c]) == 1 and nxt_c in cur.childs[c]:
                    cur.childs[c].append(XKJDTree(char=char))
                else:
                    cur = cur.childs[c]



JD_S2K = {
    'q': 'q',
    'w': 'w',
    'r': 'r',
    't': 't',
    'y': 'y',
    'p': 'p',
    's': 's',
    'd': 'd',
    'f': 'f',
    'g': 'g',
    'h': 'h',
    'j': 'j',
    'k': 'k',
    'l': 'l',
    'z': 'z',
    'x': 'x',
    'c': 'c',
    'b': 'b',
    'n': 'n',
    'm': 'm',
    'zh': ['q','f'],
    'ch': ['w','j'],
    'sh': 'e',
}

JD_Y2K = {
    'ua': 'q',
    'iu': 'q',
    'ei': 'w',
    'un': 'w',
    'e': 'e',
    'eng': 'r',
    'uan': 't',
    'ong': 'y',
    'iong': 'y',
    'ang': 'p',
    'a': 's',
    'ia': 's',
    'ou': 'd',
    'ie': 'd',
    'an': 'f',
    'uai': 'd',
    'ing': 'd',
    'ai': 'h',
    'ue': 'h',
    'u': 'j',
    'er': 'j',
    'i': 'k',
    'uo': 'l',
    'v': 'l',
    'o': 'l',
    'ao': 'z',
    'iang': 'x',
    'uang': ['m','x'],
    'iao': 'c',
    'in': 'b',
    'ui': 'b',
    'en': 'k',
    'ian': 'm',
}
danzi_dict = {}
with open("./data/src/xkjd6/xkjd6.danzi.final.txt","r") as fl:
    for line in fl.readlines():
        char,code = line.split("\t")
        char = char.strip()
        code = code.strip()
        if len(code) != 6:
            print(char,code)

        pinyin = code[0:2]
        bihua = code[2:]
        if char not in danzi_dict:
            danzi_dict[char] = {pinyin:bihua}
        else:
            danzi_dict[char][pinyin] = bihua


with open("./results/zh_counts.csv", 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f,delimiter="\t")
        for row in reader:
            print(row)
