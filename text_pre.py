from abc import abstractmethod
from pypinyin import lazy_pinyin
import jieba

class TextProcessBase:
    @abstractmethod
    def convert_all_to_lower_case_letters(self,text:str) ->str:
        raise NotImplementedError


class XKJDTextProcess(TextProcessBase):
    danzi_dict = {}
    def __init__(self,danzi_path = "./data/src/xkjd6/xkjd6.danzi.final.txt") -> None:
        super().__init__()
        with open(danzi_path,"r") as danzi_file:
            for line in danzi_file.readlines():
                char,code = line.strip().split('\t')
                pinyin,bihua = code[0:2],code[2:]
                if char not in self.danzi_dict:
                    self.danzi_dict[char] = {pinyin: bihua}
                else:
                    self.danzi_dict[pinyin] = bihua
    def convert_all_to_lower_case_letters(self, text : str) -> str:
        text_cut = jieba.lcut(text)
        result_str = ""
        for word in text_cut:
            if word[0].isalpha():
                result_str = result_str + word
            else:
                pinyin = lazy_pinyin(word)
