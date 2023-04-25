with open("./xkjd6.danzi.final.txt","r") as fl:
    for line in fl.readlines():
        char,code = line.split("\t")
        char = char.strip()
        code = code.strip()
        if len(code) != 6:
            print(char,code)

