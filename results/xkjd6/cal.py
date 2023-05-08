with open("xkjd6.dict.yaml","r") as dict_yaml:
    sum_same = 0
    line = dict_yaml.readline()
    pre_code = {}
    max_same_len = {}
    count_len = {}
    same_code = {}
    while line:
        char,code = line.strip().split()
        code_len = len(code)

        if code_len in pre_code and code == pre_code[code_len]:
            count_len[code_len] =  count_len[code_len] + 1
        else:
            if code_len in count_len:
                if count_len[code_len] > 1:
                    sum_same += count_len[code_len]
            if code_len not in max_same_len:
                max_same_len[code_len] = 1
                same_code[code_len] = code
            pre_code[code_len] = code
            count_len[code_len] = 1
        if count_len[code_len] > max_same_len[code_len]:
            same_code[code_len] = code
            max_same_len[code_len] = count_len[code_len]
        line = dict_yaml.readline()

    for code_len in max_same_len.keys():
        if count_len[code_len] > 1:
            sum_same += count_len[code_len]
        if count_len[code_len] > max_same_len[code_len]:
            max_same_len[code_len] = count_len[code_len]
        print("{wlen}: {code} {same_len}".format(wlen=code_len,code = same_code[code_len],same_len=max_same_len[code_len]))
    print("all same code {}".format(sum_same))
