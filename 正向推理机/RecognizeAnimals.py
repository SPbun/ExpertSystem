#!/usr/bin/env python
# coding: utf-8

# In[170]:


import sys,codecs,uniout,time
def LoadFile(filename):
    #load database from a file
    #filename = "./database.txt"
    res = []
    #split rule with dot
    with codecs.open(filename,'r','gb2312') as f:
        for line in f.readlines():
            if filename == 'condition.txt':
                return line.split(',')
            res.append(line.split(','))
    return res
    


# In[109]:


def SetupDatabase(RawData=[]):
    #生成规则数据库，每条规则用一个list和一个字符串表示表示，前者代表条件and，后者字符串代表推理结果
    RuleDatabase = []
    for rule in RawData:
        tmp = []
        condition = rule[:-1]
        result = rule[len(rule)-1]
        result = "".join(result.split())
        tmp.append(condition)
        tmp.append(result)
        RuleDatabase.append(tmp)
    return RuleDatabase


# In[192]:


def Deduction(RuleDatabase=[],condition = []):
    #每轮推理使用所有规则，遍历规则，将符合条件的结论加入到condition中，知道condition不再变化，推理结束
    #每条rule由一个list表示条件和str表示结论
    #condition_init 是condition的初始值
    condition_init = []
    for item in condition:
        condition_init.append(item)
    
    #used 是在推理过程中使用的条件集合
    used = []
    
    #conditionNum 是条件个数
    conditionNum = len(condition)-1
    
    while True:
        condition_pre = condition
        #遍历条件
        for rule in RuleDatabase:
            
            #结论不在条件中并且可以推理的，加入到条件集合中 
            if not rule[1] in condition and  set(rule[0]) <= set(condition):
                #输出推理步骤
                print "通过条件",
                for con in rule[0]:
                    print con ,
                print u"推出 " + rule[1]
                time.sleep(1)
                
                condition.append(rule[1])
                #使用过的条件加入到used集合中
                for conditionUsed in rule[0]:
                    used.append(conditionUsed)
        #没有变化的时候停止
        if condition_pre == condition:
            break
    
   
    #去除condition集合和used集合，condition_init集合中的交集元素
    condition = list(set(condition)-set(used)-set(condition_init))
    
    
    
    return condition


# In[193]:


def main():
    #读入规则数据库文件和条件文件
    RawDatabase = LoadFile('database.txt')
    condition = LoadFile('condition.txt')

    #生成规则数据库
    RuleDatabase = SetupDatabase(RawDatabase)
    
    #使用规则进行推理
    DeductionResult = Deduction(RuleDatabase,condition)
    
    print u"推理结果是："
    for res in DeductionResult:
        print res


# In[194]:


if __name__=='__main__':
    main()

