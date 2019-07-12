import numpy as np
import pandas as pd
def chiSquareTest(data):
    index = data.columns
    subChiSquare = pd.pivot_table(data, index=[index[0]], columns=[index[1]], aggfunc=len)
    columnSum = np.zeros(len(subChiSquare))
    rawSum = np.zeros(len(subChiSquare.columns))
    for k in range(len(rawSum)):
        rawSum[k] = np.sum(subChiSquare.iloc[:, k])
    for k in range(len(columnSum)):
        columnSum[k] = np.sum(subChiSquare.iloc[k, :])
    sumFreq = sum(rawSum)
    chiSquareValue = 0
    for raw in range(len(rawSum)):
        for column in range(len(columnSum)):
            expection = (rawSum[raw] * columnSum[column]) / (sumFreq)
            difference = expection - subChiSquare.iloc[column, raw]
            chiSquareValue += np.square(difference) / expection
    return chiSquareValue

def chiMerge(data,mergeIndex,targerIndex,maxBoxNum):
    index=[mergeIndex,targerIndex]
    freq=data.loc[:,index]
    freq=freq.sort_values(by=mergeIndex)
    chiMergeResult=list(range(len(freq)))
    for i in range(len(freq)-maxBoxNum):
        if(i==49):
            print("jhh")
        flag=0
        minChiValue=chiSquareTest(freq.iloc[chiMergeResult[0]:(chiMergeResult[1]+1),:])
        for j in range(1,len(chiMergeResult)-1):
            tempchi=chiSquareTest(freq.iloc[chiMergeResult[j]:(chiMergeResult[j+1]+1),:])
            if tempchi < minChiValue:
                flag = j
                minChiValue = tempchi
        del chiMergeResult[flag+1]
    result=[freq.iloc[i,0] for i in chiMergeResult]
    return result
df = pd.read_csv("chiTry.csv")
index=["性别","化妆","身高"]
rr=chiMerge(df,"身高","化妆",4)
print(rr)