'''
@Author: your name
@Date: 2020-02-22 09:59:15
@LastEditTime: 2020-02-23 22:07:42
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \machinelearning\test.py
'''
import numpy as np
import pandas as pd
import random
import math



'''
@description: 根据频率将数据切分为训练集和测试集
@param {type} 训练数据集的比例
@return: 
'''
def randomSplitData(dataset,percent):
    #打乱数据集的索引
    indexcol=list(dataset.index)
    random.shuffle(indexcol)
    dataset.index=indexcol
    #根据比例划分数据集
    recordcounts=dataset.shape[0]
    rowsplit=(int)(recordcounts*percent)
    trainset=dataset.iloc[0:rowsplit,:]
    testset=dataset.iloc[rowsplit:recordcounts,:]
    #重新排列测试数据集的索引
    testset.index=range(0,testset.shape[0])
    return trainset,testset

'''
@description:构建高斯分类器
@param {type} 训练数据集、测试数据集
@return: 
'''
def gsnp_classify(train,test):
    #根据训练数据集，计算每个类别的方差和均值
    labels=train.iloc[:,-1].value_counts().index
    means=[] 
    stds=[]
    for label in labels:
        #取出该类的数据
        filter=train.iloc[:,-1]==label
        filterset=train.loc[filter,:]
        samelabelset=filterset.iloc[:,:-1]
        #计算方差和均值
        mean=samelabelset.means()
        std=np.sum((samelabelset-mean)**2/samelabelset.shape[0])
        means.append(mean)
        stds.append(std)
    #将均值和方差转换为dataframe的形式
    meandf=pd.DataFrame(means,index=labels)
    stddf=pd.DataFrame(stds,index=labels)
    #预测测试数据集
    predicts=[]
    for rowindex in range(0,test.shape[0]):
        rowdata=test.iloc[:,:-1].tolist()
        #计算概率
        percentmatrix= np.exp((rowdata-meandf)**2/-2*stddf*2)*(1/np.sqrt(2*np.pi*stddf*2))
        percent=1
        for featureindex in test.shape[1]-1:
            percent*=percentmatrix[featureindex]
        cla=percent.index[np.argmax(percent.values)]
        predicts.append(cla)
    test['perdicts']=predicts
    #计算模型准确率
    



dataset= pd.read_csv("E:\\Projects\\examples\\machinelearning\\naive_base\\iris.txt",header=None)
trainpercent=0.7
train,test=randomSplitData(dataset,trainpercent)
gsnp_classify(train,test)


        
    





 

    

