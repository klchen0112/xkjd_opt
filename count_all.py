import os
import csv
from collections import Counter
from time import sleep
import jieba
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


def count_all_zh(str_que, counter_que):
    # 统计中文单字出现的次数
    jieba.set_dictionary("data/jieba/dict.txt.big")
    jieba.load_userdict("data/jieba/user.dict")
    while True:
        text = str_que.get()
        if isinstance(text, str):
            zh_counter = Counter()
            text = text.lower()
            # 分词
            words = jieba.lcut(text, cut_all=False)
            for word in words:
                # 统计中文单字出现的次数
                if len(word) == 1 and "\u4e00" <= word <= "\u9fff":  # 判断是否为中文字符
                    zh_counter[word] += 1
                # 统计中文单词出现的次数
                elif "\u4e00" <= word[0] <= "\u9fff":  # 判断是否以中文字符开头
                    zh_counter[word] += 1
            counter_que.put(zh_counter)
        elif text is None:
            break
        else:
            sleep(1)
    print("count complete")


def wiki_zh_text_gen(str_que):
    for text in wiki_zh_json_to_text_list():
        str_que.put(text)
    print("wiki_zh add complete")


def news_text_gen(str_que):
    for text in news_json_to_text_list():
        str_que.put(text)
    print("news add complete")


def baike_text_gen(str_que):
    for text in baike_to_text_list():
        str_que.put(text)
    print("baike add complete")


def web_text_gen(str_que):
    for text in webtext_to_text_list():
        str_que.put(text)
    print("web text add complete")


def translation_text_gen(str_que):
    for text in translation_to_text_list(with_en=False):
        str_que.put(text)
    print("translation text add complete")


def thucnews_text_gen(str_que):
    for text in thucnews_to_text_list():
        str_que.put(text)
    print("thucnews add complete")


def clean_chat_corpus_text_gen(str_que):
    for text in clean_chat_corpus_to_text_list():
        str_que.put(text)
    print("clean_chat_corpus add complete")


def update_count(cont_que):
    all_zh_counter = Counter()
    while True:
        item = cont_que.get()
        if item is None:
            break
        elif isinstance(item, Counter):
            all_zh_counter.update(item)
        else:
            sleep(1)
    print("counter complete")
    write_to_csv(all_zh_counter, "results/zh_counts.csv")


if __name__ == "__main__":
    # char_counts,two_gram_counts,three_gram_counts  = count_chars_and_ngrams( './data/src/en')
    # write_to_csv(char_counts, 'results/char_counts.csv')
    # write_to_csv(two_gram_counts, 'results/two_gram_counts.csv')
    # write_to_csv(three_gram_counts, 'results/three_gram_counts.csv')

    #
    str_que_size = 10
    str_que = Queue(str_que_size)

    max_cont_size = 10
    cont_que = Queue(max_cont_size)

    write_procs = []
    write_procs.append(Process(target=wiki_zh_text_gen, args=(str_que,)))

    write_procs.append(Process(target=news_text_gen, args=(str_que,)))

    write_procs.append(Process(target=baike_text_gen, args=(str_que,)))

    write_procs.append(Process(target=web_text_gen, args=(str_que,)))

    write_procs.append(Process(target=translation_text_gen, args=(str_que,)))

    write_procs.append(Process(target=thucnews_text_gen, args=(str_que,)))

    write_procs.append(Process(target=clean_chat_corpus_text_gen, args=(str_que,)))

    for write_proc in write_procs:
        write_proc.start()

    counter_gen_procs = []
    for i in range(8):
        counter_gen_procs.append(Process(target=count_all_zh, args=(str_que, cont_que)))
    for cont_proc in counter_gen_procs:
        cont_proc.start()

    all_count_proc = Process(target=update_count, args=(cont_que,))
    all_count_proc.start()
    # # 等待所有写入任务完成
    for write_proc in write_procs:
        write_proc.join()
    for i in range(8):
        str_que.put(None)
    for cont_proc in counter_gen_procs:
        cont_proc.join()
    cont_que.put(None)
    all_count_proc.join()
