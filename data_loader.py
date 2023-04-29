import json
import os


def wiki_zh_json_to_text_list(folder_path=None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/wiki_zh"
    for fpath, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name == ".DS_Store":
                continue
            if file_name.endswith(".zip"):
                continue
            if file_name == ".gitignore":
                continue
            with open(os.path.join(fpath, file_name), "r", encoding="utf-8") as fl:
                line = fl.readline()
                while line:
                    text_json = json.loads(line)

                    yield text_json["title"]
                    yield text_json["text"]
                    line = fl.readline()


def news_json_to_text_list(folder_path=None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/new2016"
    for fpath, dirs, files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("json"):
                continue
            with open(os.path.join(fpath, file_name), "r", encoding="utf-8") as fl:
                line = fl.readline()
                while line:
                    text_json = json.loads(line)
                    yield text_json["title"]
                    yield text_json["content"]
                    line = fl.readline()


def baike_to_text_list(folder_path=None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/baike_qa"
    for fpath, dirs, files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("json"):
                continue
            with open(os.path.join(fpath, file_name), "r", encoding="utf-8") as fl:
                line = fl.readline()
                while line:
                    text_json = json.loads(line)

                    yield text_json["title"]
                    yield text_json["answer"]
                    line = fl.readline()


def webtext_to_text_list(folder_path=None):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/web_text"
    for fpath, dirs, files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("json"):
                continue
            with open(os.path.join(fpath, file_name), "r", encoding="utf-8") as fl:
                line = fl.readline()
                while line:
                    text_json = json.loads(line)

                    yield text_json["title"]
                    yield text_json["content"]

                    line = fl.readline()


def translation_to_text_list(folder_path=None, with_en=True):
    if folder_path is None:
        folder_path = "./data/src/chinese_corpus/translation"
    for fpath, dirs, files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("json"):
                continue
            with open(os.path.join(fpath, file_name), "r", encoding="utf-8") as fl:
                line = fl.readline()
                while line:
                    text_json = json.loads(line)

                    if with_en:
                        yield text_json["english"]
                    yield text_json["chinese"]
                    line = fl.readline()


def thucnews_to_text_list(
    folder_path=None,
):
    if folder_path is None:
        folder_path = "./data/src/THUCNews"
    for fpath, dirs, files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("txt"):
                continue
            with open(os.path.join(fpath, file_name), "r", encoding="utf-8") as fl:
                yield fl.read()


def clean_chat_corpus_to_text_list(
    folder_path=None,
):
    if folder_path is None:
        folder_path = "./data/src/clean_chat_corpus"
    for fpath, dirs, files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith("tsv"):
                continue
            with open(os.path.join(fpath, file_name), "r", encoding="utf-8") as fl:
                yield fl.read()
