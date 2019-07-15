import numpy as np
import pandas as pd

class chiSquare():
    def chiSquareTest(self,data):
        """
        :param data: 一个nX2的dataframe
        :return: 卡方值
        """
        index = data.columns
        subChiSquare = pd.pivot_table(data, index=[index[0]], columns=[index[1]], aggfunc=len, fill_value=0)  # 生成平频数表
        columnSum = np.zeros(len(subChiSquare))  # 右侧每一行的和
        rawSum = np.zeros(len(subChiSquare.columns))  # 下侧每一列的和
        # 分别计算
        for k in range(len(rawSum)):
            rawSum[k] = np.sum(subChiSquare.iloc[:, k])
        for k in range(len(columnSum)):
            columnSum[k] = np.sum(subChiSquare.iloc[k, :])
        sumFreq = sum(rawSum)  # 计算总数
        chiSquareValue = 0
        for raw in range(len(rawSum)):
            for column in range(len(columnSum)):
                expection = (rawSum[raw] * columnSum[column]) / (sumFreq)  # 每一格的期望
                difference = expection - subChiSquare.iloc[column, raw]  # 期望和实际频数的差
                chiSquareValue += np.square(difference) / expection  # 该格子的卡方值
        return chiSquareValue

    def chiMerge(self,data,mergeIndex, targetIndex, maxBoxNum):
        """
        :param data: dataframe类型，所需要的data
        :param mergeIndex: dataframe列名，所要分箱的列
        :param targetIndex: dataframe列名，分箱所依据的列
        :param maxBoxNum: int类型，最大箱子数
        :return:list，其中每一个值为分段的左端点(左闭右开)
        """
        index = [mergeIndex, targetIndex]
        freq = data.loc[:, index]  # 提取出所需要的两列
        freq = freq.sort_values(by=mergeIndex)  # 要分箱的列要进行排序
        chiMergeResult = list(range(len(freq)))  # 记录每一个点对应的自然位置
        for i in range(len(freq) - maxBoxNum):  # 一共要进行len(freq)-maxBoxNum的合并
            flag = 0
            minChiValue = self.chiSquareTest(freq.iloc[chiMergeResult[0]:(chiMergeResult[1] + 1), :])
            for j in range(1, len(chiMergeResult) - 1):  # 遍历查找最小的卡方值
                tempchi = self.chiSquareTest(freq.iloc[chiMergeResult[j]:(chiMergeResult[j + 1] + 1), :])
                if tempchi < minChiValue:
                    flag = j
                    minChiValue = tempchi
            del chiMergeResult[flag + 1]  # 因为认为区间是左闭右开，所以去掉flag+1的点
        result = [freq.iloc[i, 0] for i in chiMergeResult]
        return result

    def IV(self,data,boxList,boxIndex,targetIndex):
        """
        :param data: :param data: dataframe,数据
        :param boxList: list,chiMerge所返回的list
        :param boxIndex:dataframe列名，被分箱的列
        :param targetIndex: dataframe列名，编码所需要的依据列，阳性为1，阴性为0
        :return: list，每个元素为对应的WOE编码
        """
        IV_value=0
        positive=data.loc[:,targetIndex].sum()#样本阳性总数
        negative=len(data)-positive#样本阴性综述
        for i in range(len(boxList)-1):
            subData=data[np.logical_and(data.loc[:,boxIndex]>=boxList[i],data.loc[:,boxIndex]<boxList[i+1])]
            subPositive = subData.loc[:, targetIndex].sum()  # 箱子阳性总数
            subNegative = len(subData) - subPositive  # 箱子阴性总数
            positiveRate=subPositive/positive
            negativeRate=subNegative/negative
            subWOE=np.log(positiveRate/negativeRate)
            IV_i=(positiveRate-negativeRate)*subWOE
            IV_value+=IV_i
        return IV_value



if __name__ == "__main__":
    df = pd.read_csv("chiTry2.csv")
    index = ["性别", "化妆", "身高"]
    chi=chiSquare()
    rr = chi.chiMerge(df,"身高", "化妆",4)
    print(rr)
    kk=chi.IV(df,rr,"身高","etc")
    print(kk)
