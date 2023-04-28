import json
import os

def wiki_zh_json_to_text_list(folder_path = None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/wiki_zh"
    for fpath,dirs,files in os.walk(folder_path):
        for file_name in files:
            if file_name == '.DS_Store':
                continue
            with open(os.path.join(fpath, file_name), 'r', encoding='utf-8') as fl:
                for line in fl.readlines():
                    text_json =  json.loads(line)

                    yield text_json['title']
                    yield text_json['text']

def news_json_to_text_list(folder_path = None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/new2016"
    for fpath,dirs,files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("json"):
                continue
            with open(os.path.join(fpath, file_name), 'r', encoding='utf-8') as fl:
                for line in fl.readlines():
                    text_json =  json.loads(line)
                    yield text_json['title']
                    yield text_json['content']

def baike_to_text_list(folder_path = None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/baike_qa"
    for fpath,dirs,files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("json"):
                continue
            with open(os.path.join(fpath, file_name), 'r', encoding='utf-8') as fl:

                for line in fl.readlines():
                    text_json =  json.loads(line)

                    yield text_json['title']
                    yield text_json['answer']


def webtext_to_text_list(folder_path = None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/web_text"
    for fpath,dirs,files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("json"):
                continue
            with open(os.path.join(fpath, file_name), 'r', encoding='utf-8') as fl:
                for line in fl.readlines():
                    text_json =  json.loads(line)

                    yield text_json['title']
                    yield text_json['content']



def translation_to_text_list(folder_path = None,with_en = True):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/translation"
    for fpath,dirs,files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("json"):
                continue
            with open(os.path.join(fpath, file_name), 'r', encoding='utf-8') as fl:
                for line in fl.readlines():
                    text_json =  json.loads(line)

                    if with_en:
                        yield text_json['english']
                    yield text_json['chinese']
