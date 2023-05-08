import os
os.makedirs("xkjd_split",exist_ok=True)

with open("xkjd6.dict.yaml","r") as dict_yaml,open("xkjd6.extendted.dict.yaml","w+") as xkjd6_extendted:
    xkjd6_extendted.writelines("# Rime dictionary\n# encoding: utf-8\n# 键道6 扩展词库控制\n---\nname: xkjd6.extended\nversion: \"Q1\"\nsort: original\nuse_preset_vocabulary: false\nimport_tables:\n")
    line = dict_yaml.readline()
    count  = 0
    max_every_dict = 100000
    n_th = 0
    cur_file = open("xkjd_split/xkjd6.{}.dict.yaml")
    while line:
        char,code = line.strip().split("\t")


    dict_yaml.close()
    xkjd6_extendted.close()
