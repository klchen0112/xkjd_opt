import json
import os

def wiki_zh_json_to_text_list(folder_path = None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/wiki_zh"
    for fpath,dirs,files in os.walk(folder_path):
        for file_name in files:
            with open(os.path.join(fpath, file_name), 'r', encoding='utf-8') as fl:
                text_json =  json.load(fl)
                for text in text_json:
                    yield text['title']
                    yield text['text']

def news_json_to_text_list(folder_path = None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/new2016"
    for fpath,dirs,files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("json"):
                continue
            with open(os.path.join(fpath, file_name), 'r', encoding='utf-8') as fl:
                text_json =  json.load(fl)
                for text in text_json:
                    yield text['title']
                    yield text['content']

def baike_to_text_list(folder_path = None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/baike_qa"
    for fpath,dirs,files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("json"):
                continue
            with open(os.path.join(fpath, file_name), 'r', encoding='utf-8') as fl:
                text_json =  json.load(fl)
                for text in text_json:
                    yield text['title']
                    yield text['answer']


def webtext_to_text_list(folder_path = None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/web_text"
    for fpath,dirs,files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("json"):
                continue
            with open(os.path.join(fpath, file_name), 'r', encoding='utf-8') as fl:
                text_json =  json.load(fl)
                for text in text_json:
                    yield text['title']
                    yield text['content']

def webtext_to_text_list(folder_path = None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/translation"
    for fpath,dirs,files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("json"):
                continue
            with open(os.path.join(fpath, file_name), 'r', encoding='utf-8') as fl:
                text_json =  json.load(fl)
                for text in text_json:
                    yield text['english']
                    yield text['chinese']
