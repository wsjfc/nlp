#coding:utf_8
import jieba
import jieba.analyse
import jieba.posseg
from langconv import *
import extract
def Traditional2Simplified(sentence):
    '''
    将sentence中的繁体字转为简体字
    :param sentence: 待转换的句子
    :return: 将句子中繁体字转换为简体字之后的句子
    '''
    sentence = Converter('zh-hans').convert(sentence)
    return sentence

def Simplified2Traditional(sentence):
    '''
    将sentence中的简体字转为繁体字
    :param sentence: 待转换的句子
    :return: 将句子中简体字转换为繁体字之后的句子
    '''
    sentence = Converter('zh-hant').convert(sentence)
    return sentence

def dosegment_all(sentence):
    '''
    带词性标注，对句子进行分词，不排除停词等
    :param sentence:输入字符
    :return:
    '''
    sentence_seged = jieba.posseg.cut(sentence.strip())
    outstr = []
    for x in sentence_seged:
        outstr.append(x.word+"/"+x.flag)
    return outstr
def jiebalcut(sentence):
    linesp=jieba.lcut(sentence.strip(), cut_all=False)
    return linesp
def readData(path,ngrams,counttotal,count,n):
    con=[]
    context_tem=""
    respond=[]
    flag=1
    with  open(path,'r') as fileReader:
        lines = fileReader.readlines()  # 读取全部内容
        for line in lines:
            #linesimply=jiebalcut(line)
            linesimply=Traditional2Simplified(line)
            point=sentencescore(linesimply,ngrams,counttotal,count,n)
            if point<-50:
               flag=2
               continue
            #linesimply=dosegment_all(linesimply)
            if len(line)<=1:
                context_tem=""
                flag=1
                continue
            elif flag==2:
                continue
            elif flag==0:
                respond.append(linesimply)
                con.append(context_tem)
            else:
                flag=0
            context_tem=context_tem+' '+linesimply
    print("data loaded!")
    return con,respond

content = open("train_sample.txt").read()
#content = open("./train-data/train.txt").read()
ngrams,counttotal,count = extract.getNgrams(content, 2)
context,respond=readData("train_sample.txt",ngrams,counttotal,count,2)
print (context)
print(respond)
