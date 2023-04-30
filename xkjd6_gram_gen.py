from count_all import (
    wiki_zh_text_gen,
    news_text_gen,
    baike_text_gen,
    web_text_gen,
    translation_text_gen,
    thucnews_text_gen,
    clean_chat_corpus_text_gen,
    zh_fiction_gen,
    en_fiction_gen,
    write_to_csv,
)

from collections import Counter
from multiprocessing import Queue, Process
import jieba
from time import sleep


def count_chars_and_ngrams(str_after_que: Queue):
    char_counts = Counter()
    two_gram_counts = Counter()
    three_gram_counts = Counter()
    while True:
        text = str_after_que.get()
        if isinstance(text, str):
            text = text.lower()
            text = text.replace("\r\n", " ")
            text = text.replace("\t", " ")
            text = text.replace("\n", " ")
            char_counts.update(text)

            split_content = text.split()
            # Count tuples of 2 and 3
            for word in split_content:
                if len(word) > 1:
                    two_gram_counts.update(
                        [word[i : i + 2] for i in range(len(word) - 1)]
                    )
                if len(word) > 2:
                    three_gram_counts.update(
                        [word[i : i + 3] for i in range(len(word) - 2)]
                    )
        elif text is None:
            break
        else:
            sleep(2)
    write_to_csv(char_counts, "results/char_counts.csv")
    write_to_csv(two_gram_counts, "results/two_gram_counts.csv")
    write_to_csv(three_gram_counts, "results/three_gram_counts.csv")


def xkjd_process(str_pre_que, str_after_que, words_dict):
    jieba.set_dictionary("data/jieba/dict.txt.big")
    jieba.load_userdict("data/jieba/user.dict")
    while True:
        text = str_pre_que.get()
        if isinstance(text, str):
            result_str = ""
            for word in jieba.lcut(text):
                if word in words_dict:
                    result_str += words_dict[word]
                else:
                    result_str += word
            str_after_que.put(result_str)
        elif text is None:
            break
        else:
            sleep(2)


if __name__ == "__main__":
    # char_counts,two_gram_counts,three_gram_counts  = count_chars_and_ngrams( './data/src/en')
    # write_to_csv(char_counts, 'results/char_counts.csv')
    # write_to_csv(two_gram_counts, 'results/two_gram_counts.csv')
    # write_to_csv(three_gram_counts, 'results/three_gram_counts.csv')

    words_dict = {}
    with open("results/xkjd6/xkjd6.dict.yaml", "r") as fl:
        for line in fl.readlines():
            char, code = line.strip().split("\t")
            words_dict[char] = code
    n_xkjd_process = 8
    str_que = Queue(n_xkjd_process + 2)

    xkjd_que = Queue(n_xkjd_process + 2)

    write_procs = []

    write_procs.append(Process(target=clean_chat_corpus_text_gen, args=(str_que,)))

    write_procs.append(Process(target=thucnews_text_gen, args=(str_que,)))

    write_procs.append(Process(target=wiki_zh_text_gen, args=(str_que,)))

    write_procs.append(Process(target=news_text_gen, args=(str_que,)))

    write_procs.append(Process(target=baike_text_gen, args=(str_que,)))

    write_procs.append(Process(target=web_text_gen, args=(str_que,)))

    write_procs.append(Process(target=translation_text_gen, args=(str_que,)))

    write_procs.append(Process(target=en_fiction_gen, args=(str_que,)))

    write_procs.append(Process(target=zh_fiction_gen, args=(str_que,)))
    for write_proc in write_procs:
        write_proc.start()

    xkjd_procs = []
    for i in range(n_xkjd_process):
        xkjd_procs.append(
            Process(target=xkjd_process, args=(str_que, xkjd_que, words_dict))
        )
    for xkjd_proc in xkjd_procs:
        xkjd_proc.start()

    all_count_proc = Process(target=count_chars_and_ngrams, args=(xkjd_que,))
    all_count_proc.start()
    # # 等待所有写入任务完成
    for write_proc in write_procs:
        write_proc.join()
    for i in range(n_xkjd_process):
        str_que.put(None)
    for xkjd_proc in xkjd_procs:
        xkjd_proc.join()
    xkjd_que.put(None)
    all_count_proc.join()
