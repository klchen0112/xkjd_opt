import os
import csv
from collections import Counter
from time import sleep
import jieba
from pypinyin import lazy_pinyin
from multiprocessing import Queue, Process

from data_loader import (
    wiki_zh_json_to_text_list,
    news_json_to_text_list,
    baike_to_text_list,
    webtext_to_text_list,
    translation_to_text_list,
    thucnews_to_text_list,
    clean_chat_corpus_to_text_list,
)


def count_chars_and_ngrams(text):
    char_counts = Counter()
    two_gram_counts = Counter()
    three_gram_counts = Counter()

    text = text.lower()
    # text = text.translate({ " " : None,
    #      "\n" : None,
    #      "\r" : None,
    #      "\t":None,}
    # )
    char_counts.update(text)

    split_content = text.split()
    # Count tuples of 2 and 3
    for word in split_content:
        if len(word) > 1:
            two_gram_counts.update([word[i : i + 2] for i in range(len(word) - 1)])
        if len(word) > 2:
            three_gram_counts.update([word[i : i + 3] for i in range(len(word) - 2)])

    return char_counts, two_gram_counts, three_gram_counts


def write_to_csv(counts, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["character", "count"])
        for character, count in counts.most_common():
            if " " in character or "\t" in character or "\n" in character:
                continue
            only_english_char = True
            for c in character:
                if not c.isalpha():
                    only_english_char = False
                    break
            if not only_english_char:
                continue
            writer.writerow([character, count])


def count_all_zh(text):
    # 统计中文单字出现的次数

    zh_counter = Counter()
    text = text.lower()
    # 分词
    words = jieba.lcut(text, cut_all=False,use_paddle=True)
    for word in words:
        # 统计中文单字出现的次数
        if len(word) == 1 and "\u4e00" <= word <= "\u9fff":  # 判断是否为中文字符
            zh_counter[word] += 1
        # 统计中文单词出现的次数
        elif "\u4e00" <= word[0] <= "\u9fff":  # 判断是否以中文字符开头
            zh_counter[word] += 1

    return zh_counter


def wiki_zh_counter(
    que,
):
    jieba.set_dictionary("data/jieba/dict.txt.big")
    jieba.load_userdict("data/jieba/user.dict")
    jieba.enable_parallel()
    zh_counter = Counter()
    for text in wiki_zh_json_to_text_list():
        zh_counter.update(count_all_zh(text))
    que.put(zh_counter, block=True)
    print("wiki_zh complete")


def news_counter(que):
    jieba.set_dictionary("data/jieba/dict.txt.big")
    jieba.load_userdict("data/jieba/user.dict")
    jieba.enable_parallel()
    zh_counter = Counter()
    for text in news_json_to_text_list():
        zh_counter.update(count_all_zh(text))
    que.put(zh_counter, block=True)
    print("news complete")


def baike_counter(que):
    jieba.set_dictionary("data/jieba/dict.txt.big")
    jieba.load_userdict("data/jieba/user.dict")
    # jieba.enable_parallel()
    zh_counter = Counter()
    for text in baike_to_text_list():
        zh_counter.update(count_all_zh(text))
    que.put(zh_counter, block=True)
    print("baike complete")


def webtext_counter(que):
    jieba.set_dictionary("data/jieba/dict.txt.big")
    jieba.load_userdict("data/jieba/user.dict")
    jieba.enable_parallel()
    zh_counter = Counter()
    for text in webtext_to_text_list():
        zh_counter.update(count_all_zh(text))
    que.put(zh_counter, block=True)
    print("webtext complete")


def translation_counter(que):
    jieba.set_dictionary("data/jieba/dict.txt.big")
    jieba.load_userdict("data/jieba/user.dict")
    jieba.enable_parallel()
    zh_counter = Counter()
    for text in translation_to_text_list(with_en=False):
        zh_counter.update(count_all_zh(text))
    que.put(zh_counter, block=True)
    print("translation_counter complete")


def thucnews_counter(que):
    jieba.set_dictionary("data/jieba/dict.txt.big")
    jieba.load_userdict("data/jieba/user.dict")
    jieba.enable_parallel()
    zh_counter = Counter()
    for text in thucnews_to_text_list():
        zh_counter.update(count_all_zh(text))
    que.put(zh_counter, block=True)
    print("thucnew complete")


def clean_chat_corpus_counter(que):
    jieba.set_dictionary("data/jieba/dict.txt.big")
    jieba.load_userdict("data/jieba/user.dict")
    jieba.enable_parallel()
    zh_counter = Counter()
    for text in clean_chat_corpus_to_text_list():
        zh_counter.update(count_all_zh(text))
    que.put(zh_counter, block=True)
    print("clean_chat_corpus complete")


def update_conter(que):
    all_zh_counter = Counter()
    while True:
        item = que.get()
        if item is None:
            break
        if isinstance(item, Counter):
            all_zh_counter.update(item)
        sleep(5)
    write_to_csv(all_zh_counter, "results/zh_counts.csv")


if __name__ == "__main__":
    # char_counts,two_gram_counts,three_gram_counts  = count_chars_and_ngrams( './data/src/en')
    # write_to_csv(char_counts, 'results/char_counts.csv')
    # write_to_csv(two_gram_counts, 'results/two_gram_counts.csv')
    # write_to_csv(three_gram_counts, 'results/three_gram_counts.csv')

    #
    que = Queue()
    read_proc = Process(target=update_conter, args=(que,))
    read_proc.start()

    write_procs = []
    write_procs.append(Process(target=wiki_zh_counter, args=(que,)))

    write_procs.append(Process(target=news_counter, args=(que,)))

    write_procs.append(Process(target=baike_counter, args=(que,)))

    write_procs.append(Process(target=webtext_counter, args=(que,)))

    write_procs.append(Process(target=translation_counter, args=(que,)))

    write_procs.append(Process(target=thucnews_counter, args=(que,)))

    write_procs.append(Process(target=clean_chat_corpus_counter, args=(que,)))

    for write_proc in write_procs:
        write_proc.start()
    # 等待所有写入任务完成
    for write_proc in write_procs:
        write_proc.join()

    que.put(None)
    print("add que")
    read_proc.join()
