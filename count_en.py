import os
import csv
from collections import Counter
import jieba
from pypinyin import lazy_pinyin


def count_chars_and_ngrams(folder_path):
    char_counts = Counter()
    two_gram_counts = Counter()
    three_gram_counts = Counter()
    for fpath,dirs,files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith('.txt'):
                continue
            with open(os.path.join(fpath, file_name), 'r', encoding='utf-8') as f:
                text = f.read().lower()
                text = text.translate(
                    { " " : None,
                     "\n" : None,
                     "\r" : None,
                     "\t":None,}
                )
                char_counts.update(text)


                split_content = text.split()
                # Count tuples of 2 and 3
                for word in split_content:
                    if len(word) > 1:
                        two_gram_counts.update([word[i:i+2] for i in range(len(word)-1)])
                    if len(word) > 2:
                        three_gram_counts.update([word[i:i+3] for i in range(len(word)-2)])

    return char_counts,two_gram_counts,three_gram_counts


def write_to_csv(counts, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f,delimiter="\t")
        writer.writerow(['character', 'count'])
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




def count_zh(folder_path):

    # 统计中文单字出现的次数
    zh_counter = Counter()

    for fpath,dirs,files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith('.txt'):
                continue
            with open(os.path.join(fpath, file_name), 'r', encoding='utf-8') as f:
                text = f.read().lower()
                # 分词
                words = jieba.lcut(text)
                for word in words:
                    # 统计中文单字出现的次数
                    if len(word) == 1 and '\u4e00' <= word <= '\u9fff':  # 判断是否为中文字符
                        zh_counter[word] += 1
                    # 统计中文单词出现的次数
                    elif '\u4e00' <= word[0] <= '\u9fff':  # 判断是否以中文字符开头
                        zh_counter[word] += 1

    return zh_counter


if __name__ == "__main__":
    char_counts,two_gram_counts,three_gram_counts  = count_chars_and_ngrams( './data/src/en')
    write_to_csv(char_counts, 'results/char_counts.csv')
    write_to_csv(two_gram_counts, 'results/two_gram_counts.csv')
    write_to_csv(three_gram_counts, 'results/three_gram_counts.csv')
