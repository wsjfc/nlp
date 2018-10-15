
# coding: utf-8

# In[10]:


from numpy import *
import re
#初始实验数据
def loaddata():
    postinglist=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classvec=[0,1,0,1,0,1]
    return postinglist,classvec
#统计所有的单词
def createlist(data):
    vocset=set([])
    for words in data:
        vocset=set(words)|vocset
    return list(vocset)
#把单词变为向量,而且依据词袋模型，记录答案词出现的概率
def word2vec(data,posting):
    returnlist=[0]*len(data)
    for word in posting:
        if word in data:
            returnlist[data.index(word)]+=1
    return returnlist
#计算概率
def trainNB0(trainmatrix,traincategory):
    numtrainDocs=len(trainmatrix)
    numwords=len(trainmatrix[0])
    pabsive=sum(traincategory)/float(numtrainDocs)
    p0num=ones(numwords);p1num=ones(numwords)#有一个0乘积也都是0.所以初始化为1
    p0denom=2.0;p1denom=2.0
    for i in range(numtrainDocs):
        if traincategory[i]==1:
            p1num += trainmatrix[i]
            p1denom += sum(trainmatrix[i])
        else:
            p0num += trainmatrix[i]
            p0denom += sum(trainmatrix[i])
    p1vect=log(p1num/p1denom)
    p0vect=log(p0num/p0denom)#log避免下溢，太小的话，计算机约为0
    return p0vect,p1vect,pabsive
#测试算法
def testingNB():
    data,label=loaddata()
    myvocablist=createlist(data)
    trainmat=sumdatalist(myvocablist,data)
    p0vect,p1vect,pabsive=trainNB0(trainmat,label)
    testentry=['love','my','dalmation']
    thisDoc=array(word2vec(myvocablist,testentry))
    print testentry,classify(thisDoc,p0vect,p1vect,pabsive)
    testentry=['stupid','garbage']
    thisDoc=array(word2vec(myvocablist,testentry))
    print testentry,classify(thisDoc,p0vect,p1vect,pabsive)
#贝叶斯分类算法    
def classify( testentry,p0vect,p1vect,pabsive):
    p0=sum(testentry*p0vect)+log(1-pabsive)
    p1=sum(testentry*p1vect)+log(pabsive)
    if p1>p0:
        return 1
    else:
        return 0
#把词信息生成矩阵    
def sumdatalist(myvocablist,data):
    trainmat=[]
    for line in data:
        trainmat.append(word2vec(myvocablist,line))
    return trainmat
#文本切分
def textparse(string):
    list=re.split(r'\W*',string)
    return [tok.lower() for tok in list if len(tok)>2]
#邮件区分
def spamtest():
    doclist=[];classlist=[];fulltext=[]
    for i in range(1,26):
        wordlist=textparse(open('Desktop/machinelearninginaction/Ch04/email/spam/%d.txt' %i).read())#textparse把文本切分了
        doclist.append(wordlist)#矩阵
        fulltext.extend(wordlist)#list
        classlist.append(1)
        wordlist=textparse(open('Desktop/machinelearninginaction/Ch04/email/ham/%d.txt' %i).read())
        doclist.append(wordlist)
        fulltext.extend(wordlist)
        classlist.append(0)
    
    vacablist=createlist(doclist)#全部收集
    trainingset=range(50)#两个文件夹共50个
    textset=[]#装随机列表，随机的这些数用来测试
    for i in range(10):
        randindex=int(random.uniform(0,len(trainingset)))#生成0-50之间的数
        textset.append(trainingset[randindex])
        del(trainingset[randindex]) #去掉10个数
    trainmat=[]
    trainingclass=[]
    #print trainingset
    for docindex in trainingset:
        trainmat.append(word2vec(vacablist,doclist[docindex]))
        trainingclass.append(classlist[docindex])
    p0vect,p1vect,pabsive=trainNB0(array(trainmat),array(trainingclass))#使用array
    count=0
    for index in textset:
        wordvector=word2vec(vacablist,doclist[index])
        answer=classify(array(wordvector),p0vect,p1vect,pabsive)
        #print answer,classlist[index]
        if answer!=classlist[index]:
            count=count+1
            print doclist[index]
    print float(count)/len(textset)
        








#testingNB()
spamtest()

