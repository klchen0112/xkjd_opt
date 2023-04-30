from abc import abstractmethod
from pypinyin import lazy_pinyin
import jieba
from pypinyin_dict.phrase_pinyin_data import large_pinyin

class TextProcessBase:
    @abstractmethod
    def convert_all_to_lower_case_letters(self,text:str) ->str:
        raise NotImplementedError


class XKJDTextProcess(TextProcessBase):
    words_dict = {}

    def __init__(self,words_dict,max_len,prefix_dict,user_dict) -> None:
        super().__init__()
        self.words_dict = words_dict
        self.max_len = max_len
        self.prefix_dict = prefix_dict
        self.user_dict = user_dict
    def convert_all_to_lower_case_letters(self, text : str) -> str:
        

