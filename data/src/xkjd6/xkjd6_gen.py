
from audioop import bias


char_to_code = {

}

with open("./xkjd6.danzi.txt","r") as fl:
    for line in fl.readlines():
        char,code = line.split("\t")
        char = char.strip()
        code = code.strip()
        if char not in char_to_code:
            char_to_code[char] = []
        char_to_code[char].append(code)




with open("./xkjd6.chaojizici.txt","r") as fl:
    for line in fl.readlines():
        char,code = line.split("\t")
        char = char.strip()
        code = code.strip()
        if char not in char_to_code:
            char_to_code[char] = []
        char_to_code[char].append(code)

with open("./xkjd6.danzi.all.txt","w+") as fl,open("./xkjd6.danzi.less.txt","w+") as fl2:
    for char,code_list in char_to_code.items():
        if len(char) > 1:
            print(char,code_list)
        pinyin_to_bihua = {}
        for code in code_list:
            pinyin = code[0:2]
            bihua = code[2:]
            if pinyin not in pinyin_to_bihua:
                pinyin_to_bihua[pinyin] = bihua
            else:
                if len(bihua) > len(pinyin_to_bihua[pinyin]):
                    pinyin_to_bihua[pinyin] = bihua

        for pinyin,bihua in pinyin_to_bihua.items():
            if len(bihua) == 4:
                fl.write("{char}\t{code}\n".format(char=char,code = pinyin + bihua))
            else:
                fl2.write("{char}\t{code}\n".format(char=char,code = pinyin + bihua))
