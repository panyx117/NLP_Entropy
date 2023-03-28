# -*- coding: gbk -*-
import jieba
import math
import re

def process(file_name):#数据预处理
    punctuation = u'[A-Za-z0-9_.!+-=——,$%^，。？、~@#￥%……&*《》<>「」{}【】()/]（）'#定义正则表达式用于删除各种符号
    with open(file_name,'r',encoding='ANSI') as f:
        corpus = f.read()
        corpus = re.sub(punctuation,'',corpus)
        corpus = corpus.replace('\n','')
        corpus = corpus.replace('\u3000','')
        f.close()
    return corpus

def get_unitf(words):#统计一元词词频
    unitf_dic = {}#包括后面用于统计词频的字典在内，key为词，value为词出现次数
    for w in words:
        unitf_dic[w] = unitf_dic.get(w, 0) + 1
    return unitf_dic

def unigram(file_name,flag):#计算一元模型信息熵
    corpus = process(file_name)

    if flag == 0:
        words = list(jieba.cut(corpus))
    if flag == 1:
        words = [char for char in corpus]

    unitf = get_unitf(words)
    unisum = sum(item[1] for item in unitf.items())
    unientropy = 0
    for item in unitf.items():
        unientropy += -(item[1] / unisum) * math.log(item[1] / unisum, 2)
    print('unigram一元模型信息熵： ',unientropy)


def get_bitf(words):#统计二元词词频
    bitf_dic = {}
    for i in range(len(words)-1):
        bitf_dic[(words[i], words[i+1])] = bitf_dic.get((words[i], words[i+1]), 0) + 1
    return bitf_dic

def bigram(file_name, flag):#计算二元模型信息熵
    corpus = process(file_name)

    if flag == 0:
        words = list(jieba.cut(corpus))
    if flag == 1:
        words = [char for char in corpus]

    unitf = get_unitf(words)
    bitf = get_bitf(words)
    bisum = sum(item[1] for item in bitf.items())
    bientropy = 0
    for item in bitf.items():
        jp_xy = item[1] / bisum # 计算联合概率p(x,y)
        cp_xy = item[1] / unitf[item[0][0]] # 计算条件概率p(x|y)
        bientropy += -jp_xy * math.log(cp_xy, 2)
    print('bigram二元模型信息熵： ',bientropy)


def get_tritf(words):#统计三元词词频
    tritf_dic = {}
    for i in range(len(words)-2):
        tritf_dic[((words[i], words[i+1]), words[i+2])] = tritf_dic.get(((words[i], words[i+1]), words[i+2]), 0) + 1
    return tritf_dic

def trigram(file_name, flag):#计算三元模型信息熵
    corpus = process(file_name)

    if flag == 0:
        words = list(jieba.cut(corpus))
    if flag == 1:
        words = [char for char in corpus]

    bitf = get_bitf(words)
    tritf = get_tritf(words)
    trisum = sum(item[1] for item in tritf.items())
    trientropy = 0
    for item in tritf.items():
        jp_xy = item[1] / trisum  # 计算联合概率p(x,y)
        cp_xy = item[1] / bitf[item[0][0]]  # 计算条件概率p(x|y)
        trientropy += -jp_xy * math.log(cp_xy, 2)
    print('trigram三元模型信息熵： ',trientropy)


if __name__ == "__main__":
    files = [['D:/语料库/白马啸西风.txt'],
             ['D:/语料库/碧血剑.txt'],
             ['D:/语料库/飞狐外传.txt'],
             ['D:/语料库/连城诀.txt'],
             ['D:/语料库/鹿鼎记.txt'],
             ['D:/语料库/三十三剑客图.txt'],
             ['D:/语料库/射雕英雄传.txt'],
             ['D:/语料库/神雕侠侣.txt'],
             ['D:/语料库/书剑恩仇录.txt'],
             ['D:/语料库/天龙八部.txt'],
             ['D:/语料库/侠客行.txt'],
             ['D:/语料库/笑傲江湖.txt'],
             ['D:/语料库/雪山飞狐.txt'],
             ['D:/语料库/倚天屠龙记.txt'],
             ['D:/语料库/鸳鸯刀.txt'],
             ['D:/语料库/越女剑.txt']]
    files_inf = ["《白马啸西风》", "《碧血剑》", "《飞狐外传》", "《连城诀》", "《鹿鼎记》", "《三十三剑客图》", "《射雕英雄传》", 
                 "《神雕侠侣》", "《书剑恩仇录》", "《天龙八部》", "《侠客行》", "《笑傲江湖》",
                 "《雪山飞狐》", "《倚天屠龙记》", "《鸳鸯刀》", "《越女剑》"]

    print('\n\n------------以词为单位计算信息熵------------')
    for i, file in enumerate(files):
        print('----------------------------------------------------------')
        print('语料库小说名：', files_inf[i],  '单位：词')
        unigram(file[0],0)
        bigram(file[0],0)
        trigram(file[0],0)

    print('\n\n------------以字为单位计算信息熵------------')
    for i, file in enumerate(files):
        print('----------------------------------------------------------')
        print('语料库小说名：', files_inf[i],  '单位：字')
        unigram(file[0],1)
        bigram(file[0],1)
        trigram(file[0],1)
