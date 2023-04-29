import csv
import os
from pypinyin import lazy_pinyin
from preset import PY_TO_JD, JD_TO_PY
from queue import Queue


class XKJDTree:
    char = ""
    code = ""
    children = {}
    freq = 0

    def __init__(self, char: str, code: str, freq: int) -> None:
        self.char = char
        self.code = code
        self.children = {}
        self.freq = freq

    def insert(self, code, char, freq, min_depth):
        char_len = len(char)
        cur = self
        cur_code = ""
        code_len = len(code)
        cur_depth = 0
        for i in range(code_len):
            c = code[i]
            cur_code = cur_code + c
            cur_depth += 1
            if cur.char == char:
                return True
            if c not in cur.children:
                if cur_depth >= min_depth:
                    cur.children[c] = [XKJDTree(char=char, code=cur_code, freq=freq)]
                    return True
                else:
                    cur.children[c] = [XKJDTree(char="", code="", freq=-1)]
                    cur = cur.children[c][0]
            else:
                if i + 1 == code_len:
                    for child in cur.children[c]:
                        if child.char == char_or_words and child.code == cur_code:
                            return True
                    if len(code) == 2 or len(code) == 3:
                        return False
                    cur.children[c].append(XKJDTree(char=char, code=cur_code, freq=-1))
                    return True
                else:
                    if cur.children[c][0].char == "" and cur_depth >= min_depth:
                        cur = cur.children[c][0]
                        cur.char = char
                        cur.code = cur_code
                        return True
                    cur = cur.children[c][0]
        return False


def gen_final_dict(root: XKJDTree):
    os.makedirs("results/xkjd6", exist_ok=True)
    node_que = Queue()
    node_que.put(root)
    with open("results/xkjd6/xkjd6.dict.yaml", "w") as dict_yaml:
        while not node_que.empty():
            now = node_que.get()
            if char != "" and code != "":
                dict_yaml.write("{char}\t{code}\n".format(char=now.char, code=now.code))
            for child_list in now.children.values():
                for child in child_list:
                    node_que.put(child)
        dict_yaml.close()
    print("gen dict complete")


if __name__ == "__main__":
    danzi_bihua_dict = {}
    danzi_code_dict = {}
    root_node = XKJDTree(char="", code="", freq=-1)
    with open("./data/src/xkjd6/xkjd6.danzi.final.txt", "r") as fl:
        for line in fl.readlines():
            char, code = line.split("\t")
            char = char.strip()
            code = code.strip()

            if len(code) != 6:
                print(char, code)
            if char not in danzi_code_dict:
                danzi_code_dict[char] = []
            danzi_code_dict[char].append(code)
            pinyin = code[0:2]
            bihua = code[2:]
            danzi_bihua_dict[char] = bihua

    with open("./results/zh_counts.csv", "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)
        for row in reader:
            char_or_words, frequency = row[0], row[1]
            word_len = len(char_or_words)
            pinyin = lazy_pinyin(char_or_words)

            if word_len == 1:
                if char_or_words in danzi_code_dict:
                    for code in danzi_code_dict[char_or_words]:
                        root_node.insert(code, char_or_words, frequency, word_len)
            else:
                if word_len == 2:
                    if char_or_words[1] not in danzi_bihua_dict:
                        continue
                    if pinyin[0] not in PY_TO_JD:
                        print(char_or_words)
                        print(pinyin[0])
                    short_code = (
                        PY_TO_JD[pinyin[0]][0] + danzi_bihua_dict[char_or_words[1]][:2]
                    )
                    if not root_node.insert(
                        short_code, char_or_words, frequency, 2
                    ):  # sb/sbb
                        if char_or_words[0] not in danzi_bihua_dict:
                            continue
                        code = (
                            PY_TO_JD[pinyin[0]]
                            + PY_TO_JD[pinyin[1]]
                            + danzi_bihua_dict[char_or_words[0]][0]
                            + danzi_bihua_dict[char_or_words[1]][0]
                        )
                        root_node.insert(code, char_or_words, frequency, 4)  # sysy
                else:
                    code_py = ""
                    code_bihua = ""
                    find_fail = False
                    for i in range(word_len):
                        if i == 3:
                            if (
                                "a" <= char_or_words[-1][0]
                                and char_or_words[-1][0] <= "z"
                            ):
                                find_fail = True
                                break
                            code_py = code_py + PY_TO_JD[pinyin[-1]][0]
                            if char_or_words[-1] not in danzi_bihua_dict:
                                find_fail = True
                                break
                            code_bihua = (
                                code_bihua + danzi_bihua_dict[char_or_words[-1]][0]
                            )
                            break
                        else:
                            if char_or_words[i] not in danzi_bihua_dict:
                                find_fail = True
                                break
                            code_py = code_py + PY_TO_JD[pinyin[i]][0]
                            code_bihua = (
                                code_bihua + danzi_bihua_dict[char_or_words[i]][0]
                            )
                    if not find_fail:
                        code_py_len = len(code_py)
                        code = code_py + code_bihua[: 6 - code_py_len]
                        root_node.insert(
                            code, char_or_words, frequency, min(word_len, 4)
                        )
    print("insert complete")
    gen_final_dict(root_node)

    with open("results/xkjd6/xkjd6.dict.yaml", "r") as dict_yaml:
        line = dict_yaml.readlines()
