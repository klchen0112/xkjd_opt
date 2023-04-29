import csv
import os
from pypinyin import lazy_pinyin
from preset import PY_TO_JD, JD_TO_PY
from queue import Queue


class XKJDTree:
    char = ""
    code = ""
    children = {}

    def __init__(self, char: str, code: str) -> None:
        self.char = char
        self.code = code
        self.children = {}

    def insert(self, code, char):
        if len(char) == 1:
            assert "a" <= code[0] and code[0] <= "z"
            assert "a" <= code[1] and code[1] <= "z"
        char_len = len(char)
        cur = self
        cur_code = ""
        code_len = len(code)
        for i in range(code_len):
            c = code[i]
            cur_code = cur_code + c
            if c not in cur.children:
                cur.children[c] = [XKJDTree(char=char, code=cur_code)]
                return True
            else:
                if i + 1 == code_len:
                    cur.children[c].append(XKJDTree(char=char, code=cur_code))
                    return True
                else:
                    cur = cur.children[c][0]
        return False


def gen_final_dict(root: XKJDTree):
    os.makedirs("results/xkjd6", exist_ok=True)
    node_que = Queue()
    node_que.put(root)
    with open("results/xkjd6/xkjd6.dict.yaml", "w") as dict_yaml:
        while not node_que.empty():
            now = node_que.get()
            dict_yaml.write("{char}\t{code}\n".format(char=now.char, code=now.code))
            for child_list in now.children.values():
                for child in child_list:
                    node_que.put(child)
        dict_yaml.close()


if __name__ == "__main__":
    danzi_bihua_dict = {}
    danzi_code_dict = {}
    with open("./data/src/xkjd6/xkjd6.danzi.final.txt", "r") as fl:
        for line in fl.readlines():
            char, code = line.split("\t")
            char = char.strip()
            code = code.strip()

            if len(code) != 6:
                print(char, code)
            danzi_code_dict[char] = code
            pinyin = code[0:2]
            bihua = code[2:]
            danzi_bihua_dict[char] = bihua

    root_node = XKJDTree("", "")

    with open("./results/zh_counts.csv", "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)
        rows = []
        for row in reader:
            rows.append([row[0],int(row[1])])
        rows = sorted(rows,key = lambda x: (len(x[0]),-x[1]))
        for row in rows:
            char_or_words, frequency = row[0], row[1]
            word_len = len(char_or_words)
            pinyin = lazy_pinyin(char_or_words)
            if word_len == 1:
                if char_or_words in danzi_code_dict:
                    root_node.insert(danzi_code_dict[char_or_words], char_or_words)
            elif word_len == 2:
                if char_or_words[1] not in danzi_bihua_dict:
                    continue
                short_code = (
                    PY_TO_JD[pinyin[0]][0] + danzi_bihua_dict[char_or_words[1]][:2]
                )
                if not root_node.insert(short_code, char_or_words):
                    if char_or_words[0] not in danzi_bihua_dict:
                        continue
                    code = (
                        PY_TO_JD[pinyin[0]]
                        + PY_TO_JD[pinyin[1]]
                        + danzi_bihua_dict[char_or_words[0]]
                        + danzi_bihua_dict[char_or_words[1]]
                    )
                    root_node.insert(code, char_or_words)
            elif word_len == 3:
                code_py = ""
                code_bihua = ""
                find_fail = False
                for i in range(word_len):
                    if char_or_words[i] not in danzi_bihua_dict:
                        find_fail = True
                        break
                    code_py = code_py + PY_TO_JD[pinyin[i]][0]
                    code_bihua = code_bihua + danzi_bihua_dict[char_or_words[i]][0]
                if not find_fail:
                    code = code_py + code_bihua
                    root_node.insert(code, char_or_words)
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
                            code_bihua + danzi_bihua_dict[char_or_words[-1]]
                        )
                        break
                    else:
                        if char_or_words[i] not in danzi_bihua_dict:
                            find_fail = True
                            break
                        code_py = code_py + PY_TO_JD[pinyin[i]][0]
                        code_bihua = code_bihua + danzi_bihua_dict[char_or_words[i]]
                if not find_fail:
                    code_py_len = len(code_py)
                    code = code_py + code_bihua[: 6 - code_py_len]
                    root_node.insert(code, char_or_words)
    gen_final_dict(root_node)
    with open("results/xkjd6/xkjd6.dict.yaml", "r") as dict_yaml:
        line = dict_yaml.readlines()

