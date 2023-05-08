import os
import chardet

if __name__ == '__main__':
    for root, dirs, files in os.walk("data/src"):
        for fname in files:
            if not fname.endswith(".txt"):
                continue
            fpath = os.path.join(root, fname)
            # with open(fpath,'rb') as fl:
            #     cur_encoding = chardet.detect(fl.read())['encoding']
            # if cur_encoding == 'gb2312':
            #     cur_encoding = 'gbk'

            try:
                with open(fpath, "r",encoding='utf-8') as fl:
                        1
            except UnicodeDecodeError:
                print(fpath)
    print("zh fiction complete")
