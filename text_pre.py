from abc import abstractmethod


class TextProcessBase:
    @abstractmethod
    def convert_all_to_lower_case_letters(self,text):
        raise NotImplementedError


