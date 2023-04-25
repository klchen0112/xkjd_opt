
char_to_code = {

}

with open("xkjd6.danzi.txt","r") as fl:
    for line in fl.readlines():
        char,code = line.split("\t")
        char_to_code[char] = code

with open("xkjd6.chaojizici.txt","r") as fl:
    for line in fl.readlines():
        char,code = line.split("\t")
        char_to_code[char] = code

with open("xkjd6.danzi.all.dict.txt","w+") as fl:
    for char,code in char_to_code.items():
        fl.write("{char}\t{code}".format(char=char,code = code))
