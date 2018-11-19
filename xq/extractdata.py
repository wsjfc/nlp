import re
import string
import operator
import string
from zhon.hanzi import punctuation
import math
import json
def cleanText(input):
    input = re.sub('\[[0-9]*\]', "", input) # 剔除类似[1]这样的引用标记
    input = re.sub(' +', " ", input) #  把连续多个空格替换成一个空格
    #input = re.sub("[+\.\?\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".encode("utf8"), "", input.encode("utf8"))
import re
import string
import operator
import string
from zhon.hanzi import punctuation
import math
import json
def cleanText(input):
    input = re.sub('\[[0-9]*\]', "", input) # 剔除类似[1]这样的引用标记
    input = re.sub(' +', " ", input) #  把连续多个空格替换成一个空格
    #input = re.sub("[+\.\?\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".encode("utf8"), "", input.encode("utf8"))
    trantab = str.maketrans({key: None for key in string.punctuation})
    input = input.translate(trantab)
    #input = input.encode("utf8")
	##########################################################################问题就在这里，要去除中文标点###########################################
    #input=re.sub('[\+\—\！\，\。\？\、\~\@\#\￥\%\……\&\*\（\）]', "", input)
    #input = input.decode("utf8")
    #########################################################################################################################
	#print (input)
    return input

def cleanInput(input):
    input = cleanText(input)
    input = re.sub('\n+', " ", input).lower() # 匹配换行用空格替换成空格
    cleanInput = []
    input = re.sub(' +', " ", input) #  把连续多个空格替换成一个空格
    #print (input)
    input = input.split(' ') #以空格为分隔符，返回列表
    #print (input)
    for item in input:
        if len(item) >= 1 or (item.lower() == 'a' or item.lower() == 'i'): #找出单词，包括i,a等单个单词
            cleanInput.append(item)
    return cleanInput

def getNgrams(input, n):
    input = cleanInput(input)
    output = {} # 构造字典i
    counttotal={} #统计词出现的个数
    count=len(input)#总词数
    for i in range(len(input)):
        if input[i] not in counttotal: #词频统计
            counttotal[input[i]] = 0 #典型的字典操作
        counttotal[input[i]] += 1

    for i in range(len(input)-n+1):
        ngramTemp = " ".join(input[i:i+n])
        if ngramTemp not in output: #词频统计
            output[ngramTemp] = 0 #典型的字典操作
        output[ngramTemp] += 1
    return output, counttotal, count

def contentscore(content,ngrams,counttotal,numword,n):
    content=cleanText(content)
    content = content.split('\n')
    point=[]
    for sentence in content:
        score=sentencescore(sentence,ngrams,counttotal,numword,n)
        point.append(score)
    return point

def sentencescore(sentence,ngrams,counttotal,numword,n):
    sentence = sentence.split(' ')
    score=0.0
    #print (sentence,len(sentence))
    if len(sentence)==1 and sentence[0] != '':
        score = math.log((counttotal[sentence[0]]+1.0)*1.0/(numword+1.0))
    elif len(sentence)>1:
        for i in range(len(sentence)-n+1):
            if i ==0:
                if sentence[i] in counttotal:
                    score += math.log((counttotal[sentence[i]]+1.0)*1.0/(numword+1.0))
                else:
                    score += math.log(1.0/(numword+1.0))
            elif " ".join(sentence[i:i+n]) in ngrams:
                score += math.log((ngrams[" ".join(sentence[i:i+n])]+1.0)*1.0/(counttotal[sentence[i]]+1.0))
            else :
                score += math.log(1.0/(counttotal[sentence[i]]+1.0))
    else:
        score=100.0
    return score

content = open("train_sample.txt").read()
#content = open("./train-data/train.txt").read()
ngrams,counttotal,count = getNgrams(content, 2)
print (ngrams)
with open('ngrams'+'.json','a') as outfile:
    json.dump(ngrams,outfile,ensure_ascii=False)
    outfile.write('\n')
with open('counttotal'+'.json','a') as outfile:
    json.dump(counttotal,outfile,ensure_ascii=False)
    outfile.write('\n')
#sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True) #=True 降序排列
#print(sortedNGrams)
point=contentscore(content,ngrams,counttotal,count,2)
print (ngrams,counttotal)
print (point)


   
