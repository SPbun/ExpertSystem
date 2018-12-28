#!/usr/bin/env python
# coding: utf-8

# In[19]:



#决策树类,MAX节点是等待AI落子，MIN节点是等待玩家落子
class DecisionTree:
    
    #扩展所有子节点
    def createChildNode(self):
        #遍历所有落点，没有落子的都扩展，当为MAX节点时
        if self.pri =='MAX':
            for i in range(0,9):
                if self.location[i] == 0:
                    tmp = [self.location[j] for j in range(0,9)]
                    tmp[i] = 1
                    self.childNode.append(tmp)
        #当为MIN节点时
        elif self.pri == 'MIN':
            for i in range(0,9):
                if self.location[i] == 0:
                    tmp = [self.location[j] for j in range(0,9)]
                    tmp[i] = -1
                    self.childNode.append(tmp)            
            
        
    #计算叶子节点的值
    def caculateValue(self):
        #形成行向量和列向量矩阵
        rowVector = [[self.location[i] for i in range(0,3)],
                     [self.location[i] for i in range(3,6)],
                     [self.location[i] for i in range(6,9)]]
        columnVector = [[self.location[i] for i in range(0,9,3)],
                        [self.location[i] for i in range(1,9,3)],
                        [self.location[i] for i in range(2,9,3)]]
        crossVector = [[self.location[i] for i in range(0,9,4)],
                       [self.location[i] for i in range(2,9,2)]]
        
        #判断是否有胜负关系出现
        playerWin = [-1,-1,-1]
        AIWin = [1,1,1]
        result = 0
        if playerWin in rowVector or playerWin in columnVector or playerWin in crossVector:
            result = -999
            return result
        #AI胜
        elif AIWin in rowVector or AIWin in columnVector or playerWin in crossVector:
            result = 999
            return result
        
        #判断形势，行列对角线占领数
        for item in rowVector:
            if 1 in item and 0 not in item:
                result = result + item.count(1)
            elif 0 in item and 1 not in item:
                result = result - item.count(-1)
        
        for item in columnVector:
            if 1 in item and 0 not in item:
                result = result + item.count(1)
            elif 0 in item and 1 not in item:
                result = result - item.count(-1)
        
        for item in crossVector:
            if 1 in item and 0 not in item:
                result = result + item.count(1)
            elif 0 in item and 1 not in item:
                result = result - item.count(-1)
        
        return result
        
    #判断两个棋局的不同落子点
    def tellDifference(self,locationA,locationB):
        for i in range(0,9):
            if not locationA[i] == locationB[i]:
                return i
    
    #判断α-β剪枝
    def cutChunck(self):
        #如果该节点是MAX节点，如果祖先节点的值比它小，则剪枝
        if self.pri == 'MAX':
            tmpPreNode = self.preNode
            while not tmpPreNode == None:
                if not tmpPreNode.value == None and self.value >= tmpPreNode.value and tmpPreNode.pri == 'MIN':
                    self.childNode = []
                    break
                else :
                    tmpPreNode = tmpPreNode.preNode
        #如果该节点是MIN节点，如果祖先节点的值比它大，则剪枝
        elif self.pri == 'MIN':
            tmpPreNode = self.preNode
            while not tmpPreNode == None:
                if not tmpPreNode.value == None and self.value <= tmpPreNode.value and tmpPreNode.pri == 'MAX':
                    self.childNode = []
                    break
                else :
                    tmpPreNode = tmpPreNode.preNode
    
    def evaluate(self):
        if self.chac == 'ROOT':
            #根节点，拓展所有子节点
            self.createChildNode()
            #从子节点中取第一个进行拓展
            while not len(self.childNode)==0:
                tmpValue = DecisionTree(preNode = self)
                if tmpValue >= self.value:
                    self.value = tmpValue
                    self.nextStep = self.tellDifference(self.location,self.childNode[0])
                self.childNode.remove(self.childNode[0])    
            return self.nextStep
            
        elif self.chac == 'LEAF':
            #叶子节点，计算当前值，返回值
            self.value = self.caculateValue()
            return self.value
        elif self.chac == 'GENERAL':
            #一般节点，拓展节点，进行剪枝
            self.createChildNode()
            while not len(self.childNode)==0:
                #极大值点取最大值，极小值点取最小值
                if self.pri =='MAX':
                    tmpValue = DecisionTree(preNode = self)
                    if tmpValue > self.value:
                        self.value = tmpValue
                elif self.pri =='MIN':
                    tmpValue = DecisionTree(preNode = self)
                    if tmpValue < self.value or self.value == None:
                        self.value = tmpValue
                #进行剪枝
                self.childNode.remove(self.childNode[0])
                self.cutChunck()
            return self.value
        
        
        
    
    #初始化函数：输入初始棋盘
    def __init__(self,location = [],preNode = None):

        #为根节点时
        if preNode == None:
            self.pri = 'MAX'
            self.location = location 
            self.childNode = []
            self.preNode = None
            self.chac = 'ROOT'
            self.value = -999
            self.nextStep = None
            self.evaluate()
        
        elif not preNode == None:
            #根据上一节点判断该节点是极大值点还是极小值点
            self.pri = None
            if preNode.pri == 'MAX':
                self.pri = 'MIN'
            else:
                self.pri ='MAX'
        
            self.location = preNode.childNode[0]
            self.childNode = []
            self.preNode = preNode
            self.value = None
            self.chac = None
        
            #判断是否为叶子节点
            if not (0 in self.location or self.caculateValue() == 999 or self.caculateValue() == -999):
                self.chac = 'LEAF'
                #return self.caculateValue()
            else :
                self.chac = 'GENERAL'
        
            self.evaluate()
    
    #初始化函数：计算叶子节点
#     def __int__(self,preNode):
#         #根据上一节点判断该节点是极大值点还是极小值点
#         self.pri = None
#         if preNode.pri == 'MAX':
#             self.pri = 'MIN'
#         else:
#             self.pri ='MAX'
        
#         self.location = preNode.childNode[0]
#         self.childNode = []
#         self.preNode = preNode
#         self.value = None
#         self.chac = None
        
#         #判断是否为叶子节点
#         if not 0 in location or caculateVaule() == 999 or caculateValue() == -999:
#             self.chac = 'LEAF'
#             return caculateValue()
#         else :
#             self.chac = 'GENERAL'
        
#         self.evaluate()
    


# In[20]:


def printLocation(locationA):
    location = [locationA[x] for x in range(0,9)]
    for i in range(0,9):
        if location[i] == 1:
            location[i] = '√'
        elif location[i] == -1:
            location[i] = '×'
        else :
            location[i] = ' '
            
    for i in range(0,9,3):
        print str(location[i]) + ' ' + str(location[i+1]) + ' ' + str(location[i+2])

def judgeLocation(location):
    #形成行向量和列向量矩阵
        rowVector = [[location[i] for i in range(0,3)],
                     [location[i] for i in range(3,6)],
                     [location[i] for i in range(6,9)]]
        columnVector = [[location[i] for i in range(0,9,3)],
                        [location[i] for i in range(1,9,3)],
                        [location[i] for i in range(2,9,3)]]
        crossVector = [[location[i] for i in range(0,9,4)],
                       [location[i] for i in range(2,9,2)]]
        
        #判断是否有胜负关系出现
        playerWin = [-1,-1,-1]
        AIWin = [1,1,1]
        result = 0
        #玩家胜
        if playerWin in rowVector or playerWin in columnVector or playerWin in crossVector:
            result = -999
            return result
        #AI胜
        elif AIWin in rowVector or AIWin in columnVector or AIWin in crossVector:
            result = 999
            return result



def main():
    
    print u'***井字棋博弈***'
    print u'输入方法：输入行列数对，eg：2,3 表示第二行第三列，行列用逗号隔开'
    print u'输入0:玩家先手 输入1:AI先手'
    judge = int(raw_input())
    if  not judge == 0 and  not judge == 1:
        print u'输入错误'
        exit()
    location = [0,0,0,
                0,0,0,
                0,0,0]
    #玩家先手时应该输入第一步
    if judge == 0:
        print u'玩家先手，请输入落子点'
        point = raw_input()
        raw = int(point[0])
        column = int(point[2])
        location[(raw-1)*3 + (column-1)] = -1
    else :
        print u'AI先手'
    
    while True:
        if not 0 in location:
            printLocation(location)
            print u'平局！'
            break
        elif judgeLocation(location)==999:
            printLocation(location)
            print u'AI获胜！'
            break
        elif judgeLocation(location)==-999:
            printLocation(location)
            print u'玩家获胜!'
            break
        
        print u'AI思考中****'
        
        nextStep = DecisionTree(location=location)
        
        location[nextStep.nextStep] = 1
        printLocation(location)
        
        if not 0 in location and not judgeLocation(location)==999 and not judgeLocation(location)==-999:
            printLocation(location)
            print u'平局！'
            break
        elif judgeLocation(location)==999:
            printLocation(location)
            print u'AI获胜！'
            break
        elif judgeLocation(location)==-999:
            printLocation(location)
            print u'玩家获胜!'
            break        
        
        print u'选择下一步落点'
        while True:
            point = raw_input()
            raw = int(point[0])
            column = int(point[2])
            if location[(raw-1)*3 + (column-1)] == 0:
                break
            print u'输入值有误，请重新输入'
        
        location[(raw-1)*3 + (column-1)] = -1





main()






