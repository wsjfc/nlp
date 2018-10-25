#coding:utf_8
def readData(path):
    context=[]
    context_tem=""
    question=[]
    answer=[]
    flag=1
    with  open(path,'r') as fileReader:
        lines = fileReader.readlines()  # 读取全部内容
        for line in lines:
            if len(line)<=1:
               context.append([context_tem])
               flag=1
               continue
            if flag==1:
                answer.append(line)
                flag=2
            if flag==2:
                question.append(line)
                flag=3
            if flag==3:
                context_tem=context_tem+str(line)

    print("data loaded!")
    return context,question,answer
context=[]
question=[]
answer=[]
context,question,answer=readData("train_reverse.txt")

